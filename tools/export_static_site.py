#!/usr/bin/env python3
"""export_static_site.py — Phase 29-2 数据静态化。

把两套核心资产导出为前端可直接 fetch 的静态 JSON 分片（GitHub Pages 无后端）：

    源 1  data/modes_data.json   -> modes 列表（3162 -> 按 mode_code 首现去重 3152）
    源 2  api/protreptic.db      -> figures 表（501 行）

产物（默认落在 web/public/data/，Vite 会原样复制进 dist/）：

    figures.index.json          轻量索引            目标 gzip <= 80 KB（t_d7faccc5 重锚: W9-F 回填后实测 65571 B）
    figures/{code}.json         501 个详情分片
    modes/index-{0..7}.json     3092 条摘要（去重 3152 - 隔离 60），md5(mode_code)%8 均分
                                                        单片 gzip <= 200 KB
    modes/by-figure/{fc}.json   304 个「某人的 10 条模式」分片（按 figure_code 原值分组）
    meta.json                   构建时间戳 + 各产物条数 + sha256

Phase31-R3：by-figure 与 index 两份产物共用清洗后的 domain_zh/domain_en
（散文值压成短标签，规则见下方 "domain 字段清洗" 注释），消除双口径。

Phase32-F1：modes/index-*.json 与 modes/by-figure/*.json **两路产出都套用**
tools/_quarantine.py 的共享隔离名单（is_quarantined / drop_quarantined_modes，
本文件不另写名单副本）。此前 by-figure 只在分组处跳过隔离人物的整片，
而摘要索引仍按全量 modes 投影、保留模式 related_modes 里指向隔离模式的引用
也没清 —— 于是 8 个 modes/index-*.json 里有 6 片仍含已隔离的虚构人物
H-SX-001「苏咸」（10 条模式 M393-M402），线上 /modes 列表照旧显示它们。

同时输出 docs/architecture/static_data_manifest.json 供数据治理卡引用。

踩坑规则（依据 docs/architecture/web_pages_migration_assessment.md §3.2，必须遵守）：
  x 不要按 H- 前缀分片 —— 2858 条里有 1670 条的 figure_code 是旧式三字母 slug
    （HCM / SUK / AlGhazali …），按前缀会把它们全挤进一个 1.78 MB 的分片。
  v 按 figure_code 原值分组 -> 恰好 283 片。
  x 不要生成单个全量模式文件 —— 18.92 MB raw / 7.4 MB gzip，移动端不可接受。
  v 摘要索引只放 8 个轻字段（定义全文只出现在 by-figure 分片里）。

用法：
    python3 tools/export_static_site.py                      # 写到 web/public/data
    python3 tools/export_static_site.py --out public/data    # 相对仓库根
    python3 tools/export_static_site.py --no-assert-counts   # 数据基线变化时

退出码：0 成功；1 条数/体积断言失败或输入缺失。
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _quarantine import QUARANTINE, drop_quarantined_modes, is_quarantined  # noqa: E402
from source_link_index import load_index, resolve_source_chapter  # noqa: E402

# ---------------------------------------------------------------- 常量

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "web" / "public" / "data"
MODES_JSON = REPO_ROOT / "data" / "modes_data.json"
DB_PATH = REPO_ROOT / "api" / "protreptic.db"
MANIFEST_PATH = REPO_ROOT / "docs" / "architecture" / "static_data_manifest.json"

SENTINEL = ".static_site_export"
N_SHARDS = 8
GZIP_LEVEL = 9

# Phase21-R8 (2026-09-24) 遗留清档（卡 t_3669eb4a）：EXPECT_FIGURES 1057 -> 1056
# Phase21-W4 (2026-09-24, 卡 t_536073f4) 名录修复：EXPECT_FIGURES 1056 -> 1054（重建后实测；双码清档 -2，重键净 0；清单见卡报告）
# Phase21-W4 (2026-09-24, 卡 t_ee203180) 模板废件 27 码清档：EXPECT_FIGURES 1054 -> 1027（重建后实测；清档 -27）
EXPECT_FIGURES = 1028
# Phase21-R4 (2026-09-22) site-data rebuild anchor update: EXPECT_MODES 3132 -> 3152
# (曾子 M-ZX-* 的 +10 已含于上批；本卡 +10 班固 M-BG-001~010 与 +10 董仲舒 M01~M10 归一回填
# 去重口径 —— 净 +20：3008 条目的空模式码降至 10 条壳 + 10 班固入库),
# EXPECT_BY_FIGURE 304 -> 306 (曾子/班固 各 +1 分片)。EXPECT_FIGURES unchanged.
# Phase21-R6 (2026-09-23, card t_10089b19) anchor bump: 3152 -> 3252 (+100 A-group modes)
# Phase21-R6B (2026-09-23, card t_f3aabe2c) anchor bump: 3252 -> 3261
# (+10 王震 M-WZ-001~010 迁入，M392 重编号为 M-WZ-011 净 0，M391 归档去重 -1；空模式码壳 10 条口径不变；
# EXPECT_BY_FIGURE 316 / EXPECT_FIGURES 1057 unchanged)
# Phase21-R8 (2026-09-23, card t_8c521af7) anchor bump: 3261 -> 3271 (+10 H-HZX-002/王祥 M-WX-001~010 入库；空模式码壳 10 条口径不变；
# EXPECT_BY_FIGURE 316 -> 317（+1 分片）；EXPECT_FIGURES 1057 unchanged)
# Phase21-R8 (2026-09-23, card t_08bbb73d) anchor bump: 3271 -> 3281 (+10 H-LUORQ-001/罗瑞卿 M-LUORQ-001~010 入库，顶层旧块替换不涉模式计数；空模式码壳 10 条口径不变；
# EXPECT_BY_FIGURE 317 -> 318（+1 分片）；EXPECT_FIGURES 1057 unchanged)
# Phase21-R9 (2026-09-24, card t_ce457734) anchor bump: 3281 -> 3291 (+10 H-AZJ-001/安子介 M-AZJ-001~010 入库；顶层块新增不涉模式计数；空模式码壳 10 条口径不变；
# EXPECT_BY_FIGURE 318 -> 319（+1 分片）；EXPECT_FIGURES 1027 unchanged)
# Phase21-R9 (2026-09-24, card t_a7d233f0) anchor bump: 3291 -> 3301 (+10 H-SHF-001/沈复 M-SHF-001~010 入库；顶层块新增不涉模式计数；空模式码壳 10 条口径不变；
# EXPECT_BY_FIGURE 319 -> 320（+1 分片）；EXPECT_FIGURES 1027 unchanged）。注：锚点为 R9 两卡并集口径（t_ce457734 安子介 + t_a7d233f0 沈复）
# Phase21-HLX (2026-09-24, card t_4c8d02d0) anchor bump: 3311 -> 3321 (+10 M-HLX-001~010 入库，去重口径净 +10；3331 raw - 空 code 10 = 3321)；EXPECT_BY_FIGURE 321 -> 322（+1 分片）；EXPECT_FIGURES 1028 -> 1029
# Phase21-IQB+HLX+KSGL+LMNJ (2026-09-24, card t_30a3e702 收尾): 3301 -> 3331（+30 M-* 入库，去重口径净 +30；3341 raw - 空 code 10 = 3331）；EXPECT_BY_FIGURE 320 -> 323（+3 分片，SHF+IQB+HLX 各 +1）
EXPECT_MODES = 3331
EXPECT_BY_FIGURE = 323

# 卡 t_d7faccc5: W9-F 回填 504 条真名后实测 65571 B（名字空值口径 34796 B）；
# 原 50 KB 预算系空名态口径，重锚 80 KB（含 ~20% 余量，覆盖 104 占位码后续补名）。
LIMIT_INDEX_GZIP = 80 * 1024
LIMIT_MODE_SHARD_GZIP = 200 * 1024

SUMMARY_FIELDS = (
    "mode_code",
    "figure_code",
    "figure_name",
    "name_zh",
    "name_en",
    "category",
    "domain_zh",
    "domain_en",
)

FIGURE_JSON_COLS = ("modes", "domains", "historical_domains")

SAFE_NAME = re.compile(r"[A-Za-z0-9._-]+")


# name_zh / name_en 在源 data/modes_data.json 里有 574/2858 条是历史三元组
# [中文, English, 分类]（thinking_modes 表里是标量）。原样导出会让消费方
# String(数组) 渲染成 "剪纸即兴法,Papercut-Improvisation Method,创作发生方法论/…"
# 串进 /modes 卡片、/graph 节点与下拉、/compare 对照表——导出层统一折成标量，
# 前端加载器另有同口径兜底（api/modeIndex.ts / api/compareData.ts）。
CJK_RE = re.compile(r"[㐀-鿿豈-﫿]")


def pick_name(value, want_cjk: bool) -> str:
    """标量直接返回；三元组取首个满足「是否含汉字」要求的元素，找不到返回空串。"""
    if value is None:
        return ""
    items = value if isinstance(value, list) else [value]
    for item in items:
        s = str(item).strip() if item is not None else ""
        if s and (bool(CJK_RE.search(s)) == want_cjk):
            return s
    return ""


def normalize_name_fields(modes: list) -> int:
    """折平名称字段，返回被改写的模式条数（用于日志与回归断言）。"""
    changed = 0
    for m in modes:
        zh, en = m.get("name_zh"), m.get("name_en")
        if not isinstance(zh, list) and not isinstance(en, list):
            continue
        m["name_zh"] = pick_name(zh, True) or pick_name(zh, False)
        m["name_en"] = pick_name(en, False) or pick_name(zh, False)
        changed += 1
    return changed


# ---------------------------------------------------------- domain 字段清洗
# Phase31-R3. 源 data/modes_data.json 里 domain_zh / domain_en 混装两种写法:
# 1447/2858 条是领域短标签 (多为 "主领域/次领域", 如 "道德哲学/心学"),
# 其余 1411 条是整段散文 (其中 452 条开头就是 definition_zh 的副本,
# M-AMP-001 长达 366 字符). 原样导出会让 /minds/:code 卡片的领域徽标与
# /compare 的领域分布表出现整段叙述, 而且同一字段在 modes/index-*.json 与
# modes/by-figure/*.json 两份产物里口径不一致 (双口径).
#
# 清洗规则 (可复现, 逐条机械判定, 无人工干预, 不引入外部数据):
#   1. 取原始值并 strip; 空值 -> 直接回落分类标签;
#   2. 只保留首个 "/" 之前的片段 ("道德哲学/心学" -> "道德哲学",
#      "Moral Philosophy / Mind Studies" -> "Moral Philosophy");
#   3. 若该片段仍是散文 (长度 > MAX_DOMAIN_LEN=30 字符, 或含句读标点:
#      中文 。，、；：！？…, 英文 .,;:!?)
#      -> 整体丢弃, 回落 m["category"] (源数据里恒非空, 共 18 个 2~5 字短标签;
#      英文用脚本内固定的 CATEGORY_EN 映射, 保证中英同源, 可在 diff 中审阅);
#   4. 结果必然非空且 <= MAX_DOMAIN_LEN 字符, run() 末尾有回归断言兜底.
# 清洗后的字段同时供摘要索引 (modes/index-*.json) 与人物分片
# (modes/by-figure/*.json) 使用 —— 两份产物从此同源同口径.
MAX_DOMAIN_LEN = 30
DOMAIN_PUNCT_ZH = re.compile("[。，、；：！？…\n]")
DOMAIN_PUNCT_EN = re.compile("[.,;:!?\n]")

CATEGORY_EN = {
    "伦理修养": "Ethics & Self-Cultivation",
    "军事战略": "Military Strategy",
    "医学养生": "Medicine & Wellness",
    "史学文献": "History & Texts",
    "哲学形而上": "Philosophy & Metaphysics",
    "宗教修行": "Religious Practice",
    "工程技术": "Engineering & Technology",
    "心理洞察": "Psychological Insight",
    "战略决策": "Strategic Decision",
    "探险发现": "Exploration & Discovery",
    "政治治理": "Politics & Governance",
    "教育传承": "Education & Transmission",
    "文艺审美": "Arts & Aesthetics",
    "方法论通用": "General Methodology",
    "科学方法": "Scientific Method",
    "组织领导": "Organizational Leadership",
    "经济商业": "Economics & Business",
    "认识论逻辑": "Epistemology & Logic",
}


def _is_prose_domain(s, punct):
    return len(s) > MAX_DOMAIN_LEN or bool(punct.search(s))


def pick_domain(value, fallback, punct):
    """按上述规则把 domain 原始值压成短标签; 压不出来就回落 fallback."""
    s = "" if value is None else str(value).strip()
    if not s:
        return fallback
    head = s.split("/", 1)[0].strip()
    if head and not _is_prose_domain(head, punct):
        return head
    return fallback


def normalize_domain_fields(modes):
    """就地清洗 domain_zh / domain_en, 返回被改写的模式条数 (日志与断言语料用)."""
    changed = 0
    for m in modes:
        cat = "" if m.get("category") is None else str(m.get("category")).strip()
        zh = pick_domain(m.get("domain_zh"), cat, DOMAIN_PUNCT_ZH)
        en = pick_domain(m.get("domain_en"), CATEGORY_EN.get(cat, cat), DOMAIN_PUNCT_EN)
        if zh != m.get("domain_zh") or en != m.get("domain_en"):
            changed += 1
        m["domain_zh"] = zh
        m["domain_en"] = en
    return changed


LINKS_PATH = REPO_ROOT / "data" / "source_links.json"
CITATION_RE = re.compile(r"《([^》]{1,60})》")
VERIFICATION_STATUSES = ("verified", "pending", "suspect", "unverifiable")


def source_text(value) -> str:
    """source_chapter 少数条目是 list (实测 30 条): 拼成文本, 与 source_link_index 同口径."""
    if isinstance(value, list):
        return " ".join(str(x) for x in value)
    if value is None:
        return ""
    return str(value)


def inject_citation_links(modes: list, index: dict) -> dict:
    """构建期把 source_chapter 里的书名/事件匹配到 source_links.json, 写进站点数据.

    产物 (只在模式对象上加两个新字段, 不改任何既有字段):
      source_refs   每条**引文**的机读匹配结果 [citation, key, url, status, match_rule] (去重级)
      source_parts  出处文本的分段: 纯文本段 {text} + 可点段 {text, url, key} (出现级 / 渲染用)
    铁律 (承接 credibility_framework.md 第 2 节): 匹配不到就不给 url, **不伪造**;
    未解析的引文原样留在纯文本段里, 前端渲染成纯文本.
    自洽: 分段文本拼回去必须与 source_chapter 逐字相等, 不等就 exit 1 (不静默降级).
    计数口径要说清 (两个层级, 别混):
      citations_*  = **去重级**: 一条模式内同一引文出现多次只算 1 条 (与 source_link_index
                     --coverage 的 extract_refs 同口径, 也是 Y1 覆盖率报告的口径);
      segments_*   = **出现级**: 出处文本里每个书名号跨度都算 1 段 (渲染层真实处理的对象).
                    同一本书在同一段出处里被引两次 -> 2 段 / 1 条引文.
    """
    stats = {"modes_with_citations": 0, "modes_with_link": 0, "parts": 0,
             "citations": 0, "citations_linked": 0,
             "citations_registered_unlinkable": 0, "citations_unresolved": 0,
             "segments": 0, "segments_linked": 0, "segments_registered_unlinkable": 0,
             "segments_unresolved": 0}
    for m in modes:
        text = source_text(m.get("source_chapter"))
        if not text:
            continue
        refs = resolve_source_chapter(m.get("source_chapter"), index)
        if not refs:
            continue
        by_citation = {}
        for r in refs:
            by_citation.setdefault(r["citation"], r)
            stats["citations"] += 1
            if r["status"] == "linked":
                stats["citations_linked"] += 1
            elif r["status"] == "unresolved":
                stats["citations_unresolved"] += 1
            else:
                stats["citations_registered_unlinkable"] += 1
        parts = []
        pos = 0
        for match in CITATION_RE.finditer(text):
            inner = match.group(1).strip()
            res = by_citation.get(inner)
            if res is None:
                continue
            if match.start() > pos:
                parts.append({"text": text[pos:match.start()]})
            seg = {"text": match.group(0)}
            stats["segments"] += 1
            if res["status"] == "linked":
                seg["url"] = res["url"]
                seg["key"] = res["key"]
                stats["segments_linked"] += 1
            elif res["status"] == "unresolved":
                stats["segments_unresolved"] += 1
            else:
                stats["segments_registered_unlinkable"] += 1
            parts.append(seg)
            pos = match.end()
        if pos < len(text):
            parts.append({"text": text[pos:]})
        if "".join(p["text"] for p in parts) != text:
            raise SystemExit("source_parts 与 source_chapter 不相等 (mode_code=%s)" % m.get("mode_code"))
        compact_refs = [{"citation": r["citation"], "key": r["key"], "url": r["url"],
                         "status": r["status"], "match_rule": r["match_rule"]} for r in refs]
        m["source_refs"] = compact_refs
        m["source_parts"] = parts
        stats["modes_with_citations"] += 1
        if any(r["status"] == "linked" for r in refs):
            stats["modes_with_link"] += 1
    # 自洽: 两个层级各自四态求和必须等于各自总数
    if stats["citations"] != (stats["citations_linked"]
                              + stats["citations_registered_unlinkable"]
                              + stats["citations_unresolved"]):
        raise SystemExit("去重级计数不自洽: %s" % stats)
    if stats["segments"] != (stats["segments_linked"]
                             + stats["segments_registered_unlinkable"]
                             + stats["segments_unresolved"]):
        raise SystemExit("出现级计数不自洽: %s" % stats)
    return stats


def verification_counts(modes: list) -> dict:
    """四态计数 (credibility_framework.md 第 3 节): 只认四个状态, 其他值当场报错."""
    out = {s: 0 for s in VERIFICATION_STATUSES}
    unknown = {}
    for m in modes:
        v = m.get("verification")
        status = v.get("status") if isinstance(v, dict) else None
        if status in out:
            out[status] += 1
        else:
            unknown[str(status)] = unknown.get(str(status), 0) + 1
    if unknown:
        raise SystemExit("verification.status 出现四态之外的值: %s" % unknown)
    out["total"] = sum(out[s] for s in VERIFICATION_STATUSES)
    return out


def log(*a):
    print(*a, flush=True)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_quarantine_leaks(out_dir: Path, dropped_mode_codes) -> list:
    """产物自检: 隔离名单里的 figure_code / mode_code 不得出现在任何落盘 JSON 制品里。

    与 tools/build_graph_data.py 输入自检同源同义(那边命中隔离项直接非零退出);
    这里把「隔离名单是否真的在所有产出路径上生效」变成可执行的断言, 而不是靠人眼
    去 grep 八个分片看漏没漏。名单只有一份(见 tools/_quarantine.py)。
    """
    codes = [str(c) for c in QUARANTINE]
    mode_codes = [str(m) for m in dropped_mode_codes if str(m)]
    leaks = []
    for path in sorted(out_dir.rglob("*.json")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        rel = path.relative_to(out_dir)
        for code in codes:
            if code in text:
                leaks.append("%s: 含隔离 figure_code %s" % (rel, code))
        for mc in mode_codes:
            if '"%s"' % mc in text:
                leaks.append("%s: 含隔离 mode_code %s" % (rel, mc))
    return leaks


def dump_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def gzip_len(data: bytes) -> int:
    return len(gzip.compress(data, GZIP_LEVEL, mtime=0))


def write_product(path: Path, obj) -> dict:
    data = dump_bytes(obj)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {"raw_bytes": len(data), "gzip_bytes": gzip_len(data), "sha256": sha256_bytes(data)}


def aggregate_sha(items) -> str:
    h = hashlib.sha256()
    for rel, dig in sorted(items):
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(dig.encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()


def human(n: int) -> str:
    if n >= 1024 * 1024:
        return f"{n / 1024 / 1024:.2f} MB"
    if n >= 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n} B"


def shard_of(mode_code: str) -> int:
    return int(hashlib.md5(mode_code.encode("utf-8")).hexdigest(), 16) % N_SHARDS


# ---------------------------------------------------------------- 输入装载


def load_modes(src: Path):
    """复刻 api/load_v6.py 的去重规则：按 mode_code 首现保留，丢掉空 code 与重复。"""
    if not src.is_file():
        raise SystemExit(f"[FAIL] 缺少源文件 {src}")
    raw = json.loads(src.read_text(encoding="utf-8"))
    modes = raw.get("modes")
    if not isinstance(modes, list):
        raise SystemExit(f"[FAIL] {src} 中 raw['modes'] 不是列表")

    seen = set()
    kept = []
    dropped_dup = 0
    dropped_nocode = 0
    for m in modes:
        mc = m.get("mode_code")
        mc = "" if mc is None else str(mc)
        if not mc:
            dropped_nocode += 1
            continue
        if mc in seen:
            dropped_dup += 1
            continue
        seen.add(mc)
        kept.append(m)

    log(f"  modes_data.json : raw modes = {len(modes)}，去重后 = {len(kept)}"
        f"（丢重复 mode_code {dropped_dup}，丢空 code {dropped_nocode}）")
    return raw, kept, {"raw": len(modes), "kept": len(kept),
                       "dropped_dup": dropped_dup, "dropped_nocode": dropped_nocode}


def load_figures(db: Path):
    if not db.is_file():
        raise SystemExit(f"[FAIL] 缺少数据库 {db}")
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("SELECT * FROM figures ORDER BY id").fetchall()
    finally:
        conn.close()

    out = []
    for r in rows:
        d = {}
        for col in r.keys():
            if col == "id":
                continue
            v = r[col]
            if col in FIGURE_JSON_COLS:
                arr = []
                if isinstance(v, str) and v.strip():
                    try:
                        parsed = json.loads(v)
                    except json.JSONDecodeError:
                        parsed = []
                    if isinstance(parsed, list):
                        arr = parsed
                d[col] = arr
            else:
                d[col] = v
        d["n_modes"] = len(d.get("modes") or [])
        out.append(d)
    log(f"  protreptic.db   : figures = {len(out)} 行")
    return out


def prepare_out(out: Path) -> None:
    """清空并重建输出目录——脚本可重复运行，不留孤儿文件。

    安全阀：仅当目录为空、不存在、或带有本脚本的 SENTINEL 标记时才允许删除，
    避免 --out 写错路径时误删用户数据。
    """
    if out.exists():
        if not out.is_dir():
            raise SystemExit(f"[FAIL] --out 指向的不是目录：{out}")
        entries = list(out.iterdir())
        if entries and not (out / SENTINEL).exists():
            raise SystemExit(
                f"[FAIL] 拒绝覆盖非本脚本产出的目录：{out}\n"
                f"       （该目录非空且没有 {SENTINEL} 归属标记，请手工确认后清理）"
            )
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / SENTINEL).write_text(
        "generated by tools/export_static_site.py — 该目录整体由脚本重建，勿手工编辑\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------- 主流程


def run(out_dir: Path, assert_counts: bool = True) -> int:
    t0 = datetime.now(timezone.utc)

    log("== 读取源数据 ==")
    raw_doc, modes, mode_stats = load_modes(MODES_JSON)
    raw_modes_total = mode_stats["raw"]
    name_fixed = normalize_name_fields(modes)
    log(f"  名称字段折平          {name_fixed} 条（name_zh/name_en 历史三元组 -> 标量）")
    domain_fixed = normalize_domain_fields(modes)
    long_domain = sum(1 for m in modes if len(str(m.get("domain_zh") or "")) > MAX_DOMAIN_LEN)
    log(f"  domain 字段清洗       {domain_fixed} 条（散文/长值 -> 首个 '/' 片段或 category 短标签）"
        f"，清洗后 len(domain_zh) > {MAX_DOMAIN_LEN} 的条数 = {long_domain}")

    # ---------- 隔离名单（Phase32-F1）：公开产出层统一剔除 ----------
    # 名单只在 tools/_quarantine.py 里定义一处，此处用共享助手一次算出
    # 「隔离人物的全部模式」并清掉保留模式 related_modes 里指向它们的引用；
    # index 与 by-figure 共用这一份模式列表（不各写一份名单、不各判一次）。
    public_modes, dropped_modes = drop_quarantined_modes(modes)
    log(f"  [隔离] 剔除 {len(dropped_modes)} 条隔离人物的模式"
        f"（{', '.join(sorted(dropped_modes))}）：公开模式 {len(modes)} -> {len(public_modes)}"
        f"；名单见 tools/_quarantine.py：{', '.join(sorted(QUARANTINE))}")

    # ---------- 1.0 出处链接注入 (Phase38-Y2): 出处 -> 可点引用 ----------
    # 匹配规则唯一实现在 tools/source_link_index.py (R0-R3), 本步骤只做注入 + 自洽断言;
    # 匹配不到的引文保持纯文本、不给 url (不伪造). 新字段: source_refs / source_parts.
    link_index = load_index(LINKS_PATH)
    link_stats = inject_citation_links(public_modes, link_index)
    log(f"  [出处] 注入可点引用: {link_stats['modes_with_citations']} 条模式带引文, "
        f"{link_stats['modes_with_link']} 条有至少 1 个可点链接")
    log(f"         去重级引文 {link_stats['citations']} 条 (linked {link_stats['citations_linked']} / "
        f"registered-unlinkable {link_stats['citations_registered_unlinkable']} / "
        f"unresolved {link_stats['citations_unresolved']}); "
        f"出现级书名号段 {link_stats['segments']} 段 (linked {link_stats['segments_linked']})")
    src_counts = {"published": verification_counts(public_modes), "all": verification_counts(modes)}

    figures = load_figures(DB_PATH)

    # ---------- 1. figures 索引 + 详情分片 ----------
    log("")
    log("== 生成 figures ==")
    prepare_out(out_dir)

    index_rows = []
    detail_stats = []
    detail_items = []
    for f in figures:
        index_rows.append({
            "code": f["code"],
            "name_zh": f.get("name_zh"),
            "name_en": f.get("name_en"),
            "era": f.get("era"),
            "domains": f.get("domains") or [],
            "historical_domains": f.get("historical_domains") or [],
            "gender": f.get("gender"),
            "ethnicity": f.get("ethnicity"),
            "n_modes": f.get("n_modes", 0),
        })

    idx_stat = write_product(out_dir / "figures.index.json", index_rows)

    for f in figures:
        rel = f"figures/{f['code']}.json"
        st = write_product(out_dir / rel, f)
        detail_stats.append(st)
        detail_items.append((rel, st["sha256"]))

    detail_raw = sum(s["raw_bytes"] for s in detail_stats)
    detail_gz = sum(s["gzip_bytes"] for s in detail_stats)
    detail_med = sorted(s["raw_bytes"] for s in detail_stats)[len(detail_stats) // 2]
    log(f"  figures.index.json      {len(index_rows):>4} 条  "
        f"raw {human(idx_stat['raw_bytes'])} / gzip {human(idx_stat['gzip_bytes'])} "
        f"(上限 {human(LIMIT_INDEX_GZIP)})")
    log(f"  figures/                {len(detail_stats):>4} 片  "
        f"raw {human(detail_raw)} / gzip {human(detail_gz)} "
        f"(单片中位 raw {human(detail_med)})")

    # ---------- 2. modes 摘要索引（md5 % 8）+ by-figure 分片 ----------
    log("")
    log("== 生成 modes ==")
    shards = {i: [] for i in range(N_SHARDS)}
    by_figure = {}
    no_code_modes = 0

    for m in public_modes:
        fc = m.get("figure_code")
        if fc is None or str(fc).strip() == "":
            no_code_modes += 1
            continue
        by_figure.setdefault(str(fc), []).append(m)

    for m in sorted(public_modes, key=lambda x: str(x.get("mode_code"))):
        mc = str(m.get("mode_code"))
        shards[shard_of(mc)].append({k: m.get(k) for k in SUMMARY_FIELDS})

    shard_stats = []
    shard_items = []
    for i in range(N_SHARDS):
        rows = shards[i]
        rel = f"modes/index-{i}.json"
        st = write_product(out_dir / rel, rows)
        st["count"] = len(rows)
        shard_stats.append(st)
        shard_items.append((rel, st["sha256"]))
        flag = "   <== 超限!" if st["gzip_bytes"] > LIMIT_MODE_SHARD_GZIP else ""
        log(f"  modes/index-{i}.json       {len(rows):>4} 条  "
            f"raw {human(st['raw_bytes'])} / gzip {human(st['gzip_bytes'])}{flag}")
    log(f"  modes/ 合计             {sum(s['count'] for s in shard_stats):>4} 条  "
        f"raw {human(sum(s['raw_bytes'] for s in shard_stats))} / "
        f"gzip {human(sum(s['gzip_bytes'] for s in shard_stats))}")

    fig_stats = []
    fig_items = []
    unsafe_names = []
    quarantined_shards = 0
    for fc in sorted(by_figure):
        if is_quarantined(fc):
            quarantined_shards += 1
            continue
        rows = sorted(by_figure[fc], key=lambda x: str(x.get("mode_code")))
        if not SAFE_NAME.fullmatch(fc):
            unsafe_names.append(fc)
        rel = f"modes/by-figure/{fc}.json"
        st = write_product(out_dir / rel, {
            "figure_code": fc,
            "figure_name": next((r.get("figure_name") for r in rows if r.get("figure_name")), None),
            "count": len(rows),
            "modes": rows,
        })
        st["count"] = len(rows)
        fig_stats.append(st)
        fig_items.append((rel, st["sha256"]))

    fig_raw = sum(s["raw_bytes"] for s in fig_stats)
    fig_gz = sum(s["gzip_bytes"] for s in fig_stats)
    med = sorted(s["raw_bytes"] for s in fig_stats)[len(fig_stats) // 2]
    med_gz = sorted(s["gzip_bytes"] for s in fig_stats)[len(fig_stats) // 2]
    log(f"  modes/by-figure/        {len(fig_stats):>4} 片  "
        f"raw {human(fig_raw)} / gzip {human(fig_gz)} "
        f"(单片中位 raw {human(med)} / gzip {human(med_gz)})")
    if quarantined_shards:
        log(f"  [隔离] 跳过 {quarantined_shards} 个隔离人物的分片 (见 tools/_quarantine.py)")
    if unsafe_names:
        log(f"  [注意] {len(unsafe_names)} 个 figure_code 含文件名特殊字符（按原值落盘，"
            f"前端 fetch 需 encodeURIComponent）：{unsafe_names}")
    if no_code_modes:
        log(f"  [注意] {no_code_modes} 条模式无 figure_code，未进入 by-figure 分片")

    # ---------- 3. meta.json ----------
    log("")
    log("== 写 meta.json ==")
    counts = {
        "figures": len(figures),
        "figure_shards": len(detail_stats),
        # mode_summaries = 源去重口径 (3152)，与 pages_preflight.EXPECT_MODES / ci_data_check
        # 同一口径（数据完整性门）。站点文案与分享图用的是**发布口径**，见
        # mode_summaries_published（= 3152 - 隔离 60 条，也就是 modes/index-*.json 的合计）。
        "mode_summaries": len(modes),
        "mode_summaries_published": sum(s["count"] for s in shard_stats),
        "modes_quarantined": len(dropped_modes),
        "mode_index_shards": N_SHARDS,
        "mode_by_figure_shards": len(fig_stats),
        "modes_raw": raw_modes_total,
        "modes_deduped": len(modes),
        "modes_duplicates_dropped": mode_stats["dropped_dup"],
        "modes_empty_mode_code_dropped": mode_stats["dropped_nocode"],
        "modes_without_figure_code": no_code_modes,
        "verification": {
            # 四态计数 (credibility_framework.md 第 3 节). 两个口径都给:
            # published = 站上真正打得开的模式 (modes/index-*.json 合计);
            # all = 源库全量 (含被隔离人物的模式, 它们不进任何公开产物).
            "published": {k: src_counts["published"][k] for k in VERIFICATION_STATUSES},
            "published_total": src_counts["published"]["total"],
            "all": {k: src_counts["all"][k] for k in VERIFICATION_STATUSES},
            "all_total": src_counts["all"]["total"],
            "quarantined_total": src_counts["all"]["total"] - src_counts["published"]["total"],
        },
        # 出处 -> 可点引用 的注入统计 (事实源仍是每个模式的 source_refs / source_parts).
        # 两个层级都写在键名里: citations_* 去重级 (与 source_link_index --coverage 同口径),
        # segments_* 出现级 (渲染层真实处理的书名号跨度数).
        "citation_links": {
            "modes_with_citations": link_stats["modes_with_citations"],
            "modes_with_link": link_stats["modes_with_link"],
            "citations": link_stats["citations"],
            "citations_linked": link_stats["citations_linked"],
            "citations_registered_unlinkable": link_stats["citations_registered_unlinkable"],
            "citations_unresolved": link_stats["citations_unresolved"],
            "segments": link_stats["segments"],
            "segments_linked": link_stats["segments_linked"],
        },
    }


    # 自洽: 四态计数 (公开口径) 必须等于 modes/index-*.json 的合计, 否则 meta.json 在说谎.
    if src_counts["published"]["total"] != counts["mode_summaries_published"]:
        raise SystemExit("四态计数 published=%d 与 mode_summaries_published=%d 不等"
                         % (src_counts["published"]["total"], counts["mode_summaries_published"]))
    log("  [核验] verification 四态 (公开口径): "
        + " / ".join("%s=%d" % (s, src_counts["published"][s]) for s in VERIFICATION_STATUSES)
        + " / total=%d" % src_counts["published"]["total"])

    products = {
        "figures.index.json": {
            "count": len(index_rows),
            "raw_bytes": idx_stat["raw_bytes"],
            "gzip_bytes": idx_stat["gzip_bytes"],
            "sha256": idx_stat["sha256"],
        },
        "figures/": {
            "count": len(detail_stats),
            "raw_bytes": detail_raw,
            "gzip_bytes": detail_gz,
            "sha256": aggregate_sha(detail_items),
        },
        "modes/index-{0..%d}.json" % (N_SHARDS - 1): {
            "count": sum(s["count"] for s in shard_stats),
            "raw_bytes": sum(s["raw_bytes"] for s in shard_stats),
            "gzip_bytes": sum(s["gzip_bytes"] for s in shard_stats),
            "sha256": aggregate_sha(shard_items),
            "shards": [
                {
                    "file": f"modes/index-{i}.json",
                    "count": shard_stats[i]["count"],
                    "raw_bytes": shard_stats[i]["raw_bytes"],
                    "gzip_bytes": shard_stats[i]["gzip_bytes"],
                    "sha256": shard_stats[i]["sha256"],
                }
                for i in range(N_SHARDS)
            ],
        },
        "modes/by-figure/": {
            "count": len(fig_stats),
            "raw_bytes": fig_raw,
            "gzip_bytes": fig_gz,
            "sha256": aggregate_sha(fig_items),
        },
    }

    meta = {
        "schema": "protreptic.static_data/v1",
        "generator": "tools/export_static_site.py",
        "generated_at": t0.astimezone(timezone.utc).isoformat(timespec="seconds"),
        "generated_at_local": t0.astimezone().isoformat(timespec="seconds"),
        "counts": counts,
        "sources": {
            "data/modes_data.json": {
                "sha256": sha256_file(MODES_JSON),
                "bytes": MODES_JSON.stat().st_size,
            },
            "api/protreptic.db": {
                "sha256": sha256_file(DB_PATH),
                "bytes": DB_PATH.stat().st_size,
            },
        },
        "products": products,
        "limits": {
            "figures.index.json.gzip_bytes": LIMIT_INDEX_GZIP,
            "modes/index-*.json.gzip_bytes": LIMIT_MODE_SHARD_GZIP,
        },
        "notes": {
            "shard_rule": "by-figure 按 figure_code 原值分组（禁用 H- 前缀分片）；摘引用 md5(mode_code)%8",
            "filename_unsafe_figure_codes": unsafe_names,
            "no_full_modes_file": "不生成单个全量模式文件（18.92 MB raw 不可接受）",
            "domain_cleaning": ("domain_zh/domain_en 先取首个 '/' 前片段；仍 > %d 字符或含句读标点则"
                                "回落 category（英文用 CATEGORY_EN）；index 与 by-figure 共用同一份清洗结果"
                                % MAX_DOMAIN_LEN),
        },
    }
    write_product(out_dir / "meta.json", meta)
    log(f"  meta.json               counts={json.dumps(counts, ensure_ascii=False)}")

    # ---------- 3.5 隔离名单零泄漏自检 ----------
    leaks = scan_quarantine_leaks(out_dir, dropped_modes)
    if leaks:
        log("  [FAIL] 隔离项泄漏 %d 处" % len(leaks))
    else:
        log("  [OK] 隔离名单零泄漏 (名单 %s; 被剔模式 %d 条)"
            % (", ".join(sorted(QUARANTINE)), len(dropped_modes)))

    # ---------- 4. 数据治理清单 ----------
    try:
        out_rel = str(out_dir.relative_to(REPO_ROOT))
    except ValueError:
        out_rel = str(out_dir)
    manifest = {
        "schema": "protreptic.static_data_manifest/v1",
        "generated_by": "tools/export_static_site.py",
        "generated_at": meta["generated_at"],
        "out_dir": out_rel,
        "counts": counts,
        "sources": meta["sources"],
        "products": products,
        "assertions": [
            {"rule": "figures 条数 == %d" % EXPECT_FIGURES, "actual": counts["figures"]},
            {"rule": "modes 去重条数 == %d（load_v6.py 口径）" % EXPECT_MODES,
             "actual": counts["modes_deduped"]},
            {"rule": "by-figure 分片数 == %d" % EXPECT_BY_FIGURE,
             "actual": counts["mode_by_figure_shards"]},
            {"rule": "发布摘要条数 == 去重条数 - 隔离名单条数",
             "actual": counts["mode_summaries_published"],
             "modes_deduped": counts["modes_deduped"],
             "modes_quarantined": counts["modes_quarantined"]},
            {"rule": "隔离名单 (tools/_quarantine.py) 零泄漏: 制品里不得出现隔离 figure_code / mode_code",
             "actual_leaks": len(leaks)},
            {"rule": "清洗后 domain_zh 长度 <= %d（by-figure 与 index 同源同口径）" % MAX_DOMAIN_LEN,
             "actual_max_len": max(len(str(m.get("domain_zh") or "")) for m in modes),
             "normalized_modes": domain_fixed},
            {"rule": "figures.index.json gzip <= 80 KB",
             "actual_gzip_bytes": idx_stat["gzip_bytes"]},
            {"rule": "modes/index-*.json 单片 gzip <= 200 KB",
             "actual_max_gzip_bytes": max(s["gzip_bytes"] for s in shard_stats)},
        ],
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_bytes(dump_bytes(manifest) + b"\n")
    log(f"  {MANIFEST_PATH.relative_to(REPO_ROOT)} 已更新")

    # ---------- 5. 断言 ----------
    log("")
    log("== 验收断言 ==")
    failures = []

    if assert_counts:
        if counts["figures"] != EXPECT_FIGURES:
            failures.append(f"figures 条数 {counts['figures']} != {EXPECT_FIGURES}")
        if counts["modes_deduped"] != EXPECT_MODES:
            failures.append(f"模式去重条数 {counts['modes_deduped']} != {EXPECT_MODES}")
        if counts["mode_by_figure_shards"] != EXPECT_BY_FIGURE:
            failures.append(f"by-figure 分片数 {counts['mode_by_figure_shards']} != {EXPECT_BY_FIGURE}")
        if counts["figure_shards"] != counts["figures"]:
            failures.append("figures 详情分片数与索引条数不一致")
        if counts["mode_summaries"] != counts["modes_deduped"]:
            failures.append("meta 的 mode_summaries 与源去重条数不一致 (站内口径应为源去重数)")
        published = counts["mode_summaries_published"]
        if published != counts["mode_summaries"] - counts["modes_quarantined"]:
            failures.append("发布摘要条数 %d != 去重 %d - 隔离 %d"
                            % (published, counts["mode_summaries"], counts["modes_quarantined"]))
        if published != sum(s["count"] for s in shard_stats):
            failures.append("发布摘要条数 %d != 八个分片实际条数之和" % published)

    if long_domain:
        failures.append(f"清洗后仍有 {long_domain} 条 domain_zh 超过 {MAX_DOMAIN_LEN} 字符")
    empty_domain = sum(1 for m in modes if not str(m.get("domain_zh") or "").strip())
    if empty_domain:
        failures.append(f"清洗后有 {empty_domain} 条 domain_zh 为空")

    if idx_stat["gzip_bytes"] > LIMIT_INDEX_GZIP:
        failures.append(f"figures.index.json gzip {idx_stat['gzip_bytes']} > {LIMIT_INDEX_GZIP}")
    over = [s for s in shard_stats if s["gzip_bytes"] > LIMIT_MODE_SHARD_GZIP]
    if over:
        failures.append(f"{len(over)} 个 modes/index-*.json 分片 gzip 超 {LIMIT_MODE_SHARD_GZIP}")

    if leaks:
        for line in leaks[:10]:
            failures.append("隔离项泄漏: " + line)

    meta_on_disk = json.loads((out_dir / "meta.json").read_text(encoding="utf-8"))
    if meta_on_disk["counts"]["modes_deduped"] != counts["modes_deduped"]:
        failures.append("meta.json 条数与实际不符")

    total_files = 1 + counts["figure_shards"] + N_SHARDS + counts["mode_by_figure_shards"] + 1
    if failures:
        for f in failures:
            log(f"  [FAIL] {f}")
        return 1

    log(f"  [OK] 产物 {total_files} 个文件"
        f"（索引 1 + figures {counts['figure_shards']} + modes 索引 {N_SHARDS}"
        f" + by-figure {counts['mode_by_figure_shards']} + meta 1）")
    log(f"  [OK] figures={counts['figures']} modes(源)={counts['modes_deduped']}"
        f" modes(发布)={counts['mode_summaries_published']}"
        f" 隔离剔除={counts['modes_quarantined']}"
        f" by-figure={counts['mode_by_figure_shards']}")
    log(f"  [OK] 体积上限：index gzip {human(idx_stat['gzip_bytes'])} <= {human(LIMIT_INDEX_GZIP)}；"
        f"最大模式分片 gzip {human(max(s['gzip_bytes'] for s in shard_stats))}"
        f" <= {human(LIMIT_MODE_SHARD_GZIP)}")
    log("")
    log(f"输出目录：{out_dir}")
    return 0


# ---------------------------------------------------------------- CLI


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="把 Protreptic 数据导出为前端可 fetch 的静态 JSON 分片")
    ap.add_argument("--out", default=str(DEFAULT_OUT),
                    help=f"输出目录（默认 {DEFAULT_OUT}；相对路径按仓库根解析）")
    ap.add_argument("--no-assert-counts", action="store_true",
                    help="跳过硬编码条数断言（数据基线变化时使用）")
    args = ap.parse_args(argv)

    out = Path(args.out)
    if not out.is_absolute():
        out = (REPO_ROOT / out).resolve()
    out = out.resolve()

    if len(out.parts) < 3:
        raise SystemExit(f"[FAIL] 拒绝把 --out 指到这么浅的路径：{out}")

    log(f"仓库根 : {REPO_ROOT}")
    log(f"输出   : {out}")
    rc = run(out, assert_counts=not args.no_assert_counts)
    log("")
    log("完成 OK" if rc == 0 else "失败 FAILED")
    return rc


if __name__ == "__main__":
    sys.exit(main())
