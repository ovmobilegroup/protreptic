#!/usr/bin/env python3
"""Credibility Gate (D1–D6 hard gates + D4/D5 warnings).

Implements the defect taxonomy from credibility_framework.md:
- D1 伪人物      → 硬 FAIL
- D2 伪造出处    → 硬 FAIL
- D3 出处污染    → 硬 FAIL (正则扫描 source_chapter)
                  豁免：已隔离(D1) figure 的记录不扫（见 §D3 豁免条款，名单取自 _quarantine.py）
- D6 悬空引用    → 硬 FAIL
- D4 引文不符    → WARN
- D5 时间线矛盾  → WARN

Interface compatible with existing preflight (exit 0 = pass, 1 = fail).
Includes negative test mode (--negative-test) that injects a D3 sample and verifies exit 1.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = REPO_ROOT / "data" / "modes_data.json"
DEFAULT_BASELINE_PATH = REPO_ROOT / "data" / "audit" / "credibility_baseline.json"
QUARANTINE_PATH = REPO_ROOT / "tools" / "_quarantine.py"

# D3 污染模式（工程痕迹正则）
D3_PATTERNS = [
    r"sha256",
    r"[0-9a-f]{8,}",           # commit 哈希
    r"双镜像",
    r"qa_postmerge",
    r"入库复检",
    r"工作树",
    r"提交链",
    r"修复提交",
    r"脚本名",
    r"pipeline",
    r"ci/cd",
    r"github actions",
]

# D2 伪造出处：已知不存在的书名（可扩展）
KNOWN_FAKE_SOURCES = {
    "《苏咸子》",
    "《苏咸子·权变篇》",
    "《苏咸子·言术篇》",
    "《苏咸子·虚实篇》",
    "《苏咸子·利益篇》",
    "《苏咸子·情报篇》",
    "《苏咸子·主动篇》",
    "《苏咸子·合纵篇》",
    "《苏咸子·纵横篇》",
}

# D1 伪人物代码（隔离名单）
def load_quarantine(root: Path | None = None) -> set[str]:
    """Load quarantine list from _quarantine.py.

    Phase37-X3：白名单要跟着「被判的数据」走。--data-path 指向另一仓的数据文件时，
    调用方传那一仓的根（resolve_repo_root），避免出现「用 A 仓的白名单判 B 仓的数据」
    ——那正是「两份数据得到同一结论」这一类参数失效的根源。
    """
    import importlib.util

    base = Path(root) if root else REPO_ROOT
    for candidate in (base / "tools" / "_quarantine.py", REPO_ROOT / "tools" / "_quarantine.py"):
        if candidate.is_file():
            try:
                spec = importlib.util.spec_from_file_location("_quarantine_for_data", candidate)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return set(getattr(mod, "QUARANTINE", {}) or {})
            except Exception:
                return set()
    return set()


def resolve_repo_root(data_path: Path) -> Path:
    """从数据文件反推仓库根：<root>/data/modes_data.json -> <root>。

    `--data-path` 的完整语义：数据、白名单（tools/_quarantine.py）、默认基线
    （data/audit/credibility_baseline.json）三者都取自同一个仓。
    """
    p = Path(data_path).resolve()
    if p.parent.name == "data" and (p.parent.parent / "tools").is_dir():
        return p.parent.parent
    return REPO_ROOT


def load_baseline_module():
    """延迟导入 tools/credibility_baseline.py（两档模式内核）。

    延迟导入的原因：tools/test_credibility_gate.py 会把本脚本复制进临时目录当夹具跑，
    夹具目录里没有该模块；只有真正用到两档模式时才需要它。
    """
    import importlib.util

    for candidate in (TOOLS_DIR / "credibility_baseline.py",
                      REPO_ROOT / "tools" / "credibility_baseline.py"):
        if candidate.is_file():
            try:
                spec = importlib.util.spec_from_file_location("credibility_baseline", candidate)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod
            except Exception:
                return None
    return None


def run_baseline_mode(args, failures, warnings, exempted, baseline_path, data_path) -> int:
    """Phase37-X3 两档模式 + 基线冻结的实现。

    legacy-report -> exit 0（只报告不阻断）
    hard-fail     -> 基线外任何一条硬失败 exit 1；否则 exit 0
    write-baseline-> 用当前硬失败重新冻结基线（改基线必须显式跑，报告里说明）
    """
    cbase = load_baseline_module()
    if cbase is None:
        print("[FAIL] 无法导入 tools/credibility_baseline.py（两档模式内核缺失）", file=sys.stderr)
        return 2
    if args.write_baseline:
        bl = cbase.build_baseline(failures, data_path)
        cbase.save_baseline(bl, Path(baseline_path))
        print("=== CREDIBILITY GATE · 基线冻结 ===")
        print(f"data path:     {data_path}")
        print(f"data sha256:   {bl['data_sha256']}")
        print(f"baseline path: {baseline_path}")
        print(f"frozen counts: {json.dumps(bl['counts'], ensure_ascii=False)}")
        print("[OK] 基线已写入；此后 --hard-fail 只拦基线外的硬失败")
        return 0
    mode = "legacy-report" if args.legacy_report else "hard-fail"
    return cbase.run_mode(
        mode=mode,
        failures=failures,
        warnings=warnings,
        exempted=sorted(exempted),
        baseline_path=Path(baseline_path),
        data_path=Path(data_path),
    )


def load_modes_data(data_path: Path | None = None) -> dict:
    """Load modes_data.json."""
    path = data_path or DEFAULT_DATA_PATH
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_all_modes(data: dict) -> list[dict]:
    """Extract all mode objects from data."""
    modes = []

    # Top-level modes array
    if "modes" in data and isinstance(data["modes"], list):
        modes.extend([m for m in data["modes"] if isinstance(m, dict)])

    # Figure modes arrays
    for key, value in data.items():
        if isinstance(value, dict) and "modes" in value and isinstance(value["modes"], list):
            modes.extend([m for m in value["modes"] if isinstance(m, dict)])

    return modes


def check_d1_fake_figure(mode: dict, quarantine: set[str]) -> list[str]:
    """D1: 伪人物 - figure_code in quarantine."""
    figure_code = mode.get("figure_code", "")
    if figure_code in quarantine:
        return [f"D1 伪人物: figure_code={figure_code} 在隔离名单中"]
    return []


def check_d2_fake_source(mode: dict) -> list[str]:
    """D2: 伪造出处 - source_chapter matches known fake sources."""
    source = mode.get("source_chapter", "")
    if isinstance(source, list):
        sources = source
    elif isinstance(source, str):
        sources = [source]
    else:
        sources = []

    errors = []
    for src in sources:
        src_str = str(src).strip()
        for fake in KNOWN_FAKE_SOURCES:
            if fake in src_str:
                errors.append(f"D2 伪造出处: source_chapter 包含已知伪造书名 '{fake}' -> {src_str}")
    return errors


def is_d3_exempt(mode: dict, quarantine: set[str]) -> bool:
    """D3 豁免判定：模式所属 figure 是否已在 D1 隔离名单里。

    依据 docs/planning/credibility_framework.md：
      §1 D3 行「豁免条款」+ §4 「豁免逻辑」——
      **D1 已隔离记录允许保留源库工程痕迹，以导出期过滤为准。**
    隔离名单的唯一事实来源是 tools/_quarantine.py 的 QUARANTINE，
    本文件不复制名单副本（改名单只改那一处）。
    """
    figure_code = str(mode.get("figure_code", "") or "").strip()
    return bool(figure_code) and figure_code in quarantine


def check_d3_pollution(
    mode: dict,
    quarantine: set[str] | None = None,
    apply_exemption: bool = True,
) -> list[str]:
    """D3: 出处污染 - source_chapter contains engineering traces.

    apply_exemption=True（默认）时跳过已隔离 figure 的记录（豁免条款）；
    传 apply_exemption=False 可做严格扫描（审计/回看用，无豁免）。
    """
    if apply_exemption and quarantine and is_d3_exempt(mode, quarantine):
        return []

    source = mode.get("source_chapter", "")
    if isinstance(source, list):
        sources = source
    elif isinstance(source, str):
        sources = [source]
    else:
        sources = []

    errors = []
    for src in sources:
        src_str = str(src)
        for pattern in D3_PATTERNS:
            if re.search(pattern, src_str, re.IGNORECASE):
                errors.append(f"D3 出处污染: source_chapter 匹配污染模式 '{pattern}' -> {src_str}")
                break  # One match per source is enough
    return errors


# --------------------------------------------------------------------------
# Phase40-Z2: D4 引文不符（真子串核验）/ D5 时间线矛盾（生卒年 × 文本年份）
#
# 这两个检查在文档里长期被写成「已实现」，实际是空壳：D4 只判「有引文但出处为空」，
# D5 直接 `return []`（船长独立核验，2026-09-20）。下面的实现是真检查，并把
# 「不可核 / 不可判定」的部分**逐条计入统计**（禁止静默放过）。口径与局限见
# docs/planning/credibility_framework.md §1 的 D4/D5 行与 §10。
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Phase41-Z3: D4/D5 统一取文本 —— 修「字段类型盲区」
#
# 船长 2026-09-21 独立核验发现：Phase40-Z2 的 d4_scan/d5_scan 用
#     text = mode.get(field); if not isinstance(text, str): continue
# 直接跳过非字符串字段，而真实数据里**年份最集中的两个字段就是数组**：
#   process_zh               list 2808 / str 20 / None 60
#   representative_cases_zh  list 2546 / str 102 / None 240
#   source_chapter           str 2808 / list 30 / None 50
#   key_quote_zh             str 2816 / list 17 / None 55
# 结果：全库 2888 条模式里 2376 条（82.3%）D5 tokens=0、conflict 恒为 0 —— 检查形同虚设。
#
# 下面这组函数是 D4/D5 **唯一**的取文本口径（不许在别处再写一遍 isinstance 判断）：
#   str            -> 原样
#   list/tuple/set -> 逐层展开（嵌套也支持）后按行 join；None 元素变空串被丢掉
#   None / 缺字段   -> ""
#   bool           -> ""（True/False 不是年份文本，不参与扫描）
#   其它标量        -> str()（如 number -> "1270"，仍然参与年份扫描）
# --------------------------------------------------------------------------

D45_TEXT_FIELDS = ("definition_zh", "process_zh", "representative_cases_zh",
                   "source_chapter", "key_quote_zh")

def _text_atoms(value) -> list:
    """任意 JSON 值 -> 原子文本列表（不按类型整段跳过）。

    str -> [str]；list/tuple/set -> 逐层展开成各元素（嵌套也支持，set 按 str 排序保稳定）；
    None / 缺字段 / bool -> []（True/False 不是年份文本）；其它标量 -> [str(value)]。
    """
    if value is None or isinstance(value, bool):
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, (list, tuple)):
        out = []
        for v in value:
            out.extend(_text_atoms(v))
        return out
    if isinstance(value, (set, frozenset)):
        out = []
        for v in sorted(value, key=str):
            out.extend(_text_atoms(v))
        return out
    return [str(value)]


def _text_of(value) -> str:
    """任意 JSON 值 -> 单块文本（原子之间按行拼接）。"""
    return "\n".join(_text_atoms(value))


def field_text_atoms(mode: dict, field: str) -> list:
    """取模式字段的原子文本列表（list 字段 = 各元素，str 字段 = 单元素）。"""
    if not isinstance(mode, dict):
        return []
    return _text_atoms(mode.get(field))


def field_text(mode: dict, field: str) -> str:
    """取模式字段的单块文本（D4 的引文与出处、报告与统计用）。缺字段或空值 -> 空串。"""
    return "\n".join(field_text_atoms(mode, field))


def iter_field_text(mode: dict, fields) -> list:
    """逐个原子文本产出 field 与 atom 之对，这是 D5 的取文本口径。

    为什么不按拼接后的大字符串扫描（Phase41-Z3 自测 M1 实测暴露）：
    D5 的上下文窗口是正负 D5_NAME_RADIUS 字；若把列表各元素拼成一块再扫，窗口会跨元素，
    前一条元素里的背景与史料类标记会污染后一条元素里真矛盾的判定，
    反过来后一条元素里的人名也会替前一条元素里的年份背书。
    按原子扫描后窗口不越元素边界，列表与字符串两种载荷判定一致。
    """
    out = []
    for f in fields:
        for atom in field_text_atoms(mode, f):
            if atom:
                out.append((f, atom))
    return out


D5_YEAR_RE = re.compile(r"(?<!\d)(1\d{3}|20\d{2})(?!\d)")
# 只有「本人叙述字段」里的年份才可能构成「本人时间线矛盾」：
#   * source_chapter 记的是**所引文献**，文献晚于本人生年是常态；
#   * key_quote_zh 常带「（据 1456 年复审证词）」这类史料/来源标注。
# 两者都不作为矛盾来源，而是进「不可判定」桶并给理由（d5_scan 的 reason 分类）。
D5_CLAIM_FIELDS = ("definition_zh", "process_zh", "representative_cases_zh")
D5_SCAN_FIELDS = D5_CLAIM_FIELDS + ("source_chapter", "key_quote_zh")
D5_WINDOW_BEFORE = 40   # 早于生年多少年以内仍算「本人时间线附近的年份」
D5_WINDOW_AFTER = 30    # 晚于卒年多少年以内仍算「本人时间线附近的年份」
D5_NAME_RADIUS = 20     # 「年份与人物名同现」的上下文窗口（正负各 N 字）
D5_EXCLUDE_AFTER = ("身后", "卒后", "死后", "逝后", "之后", "以后", "后来", "后世",
                    "后人", "继任", "其子", "其女", "女儿", "其孙", "学生", "门人",
                    "遗", "追", "平反", "封圣", "纪念", "史实", "证明", "回归")
D5_EXCLUDE_SOURCE = ("《", "》", "(", ")", "（", "）", "版", "出版", "刊", "手稿",
                     "证词", "诏书", "论文")
D5_EXCLUDE_BACKGROUND = ("年代", "年间", "期间", "前后", "侵扰", "自", "起", "背景", "世纪")


def parse_year_value(value) -> int | None:
    """生卒年字段 -> int（公元前为负）；解析不了返回 None（不猜）。"""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        m = re.fullmatch(r"约?\s*前\s*(\d{1,4})", text)
        if m:
            return -int(m.group(1))
        m = re.fullmatch(r"约?\s*(-?\d{1,4})", text)
        if m:
            return int(m.group(1))
    return None


def load_figure_lifespans(root: Path | None = None) -> dict:
    """读 data/figures/*.json 的生卒年 -> {figure_code: {...}}。

    年份字段实测三种形态：int（114 个 figure）/ 纯数字字符串（141 个）/
    「约前287」「-356」式纪年（公元前后混用）。解析不了的**不猜**：该人物整体计为
    「无生卒年」，D5 对它的模式一律 undetermined 并如实计数。
    """
    base = Path(root) if root else REPO_ROOT
    figures_dir = base / "data" / "figures"
    out: dict = {}
    if not figures_dir.is_dir():
        return out
    for path in sorted(figures_dir.glob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        code = doc.get("figure_code") or doc.get("code") or doc.get("id")
        if not code:
            continue
        birth = parse_year_value(doc.get("birth_year"))
        death = parse_year_value(doc.get("death_year"))
        if birth is None or death is None or birth > death:
            continue
        out[str(code)] = {
            "birth_year": birth,
            "death_year": death,
            "figure_name": (doc.get("figure_name") or doc.get("name_zh") or "").strip() or None,
            "era": doc.get("era"),
            "provenance": "data/figures/%s.json:birth_year/death_year" % path.stem,
        }
    return out


def d5_scan(mode: dict, lifespans: dict) -> dict:
    """D5 单条模式 -> 结构化结果（含全部「不可判定」分类，不静默放过）。"""
    code = str(mode.get("figure_code") or "")
    life = lifespans.get(code)
    if not life:
        return {"status": "undetermined", "reason": "no-lifespan-for-figure",
                "conflicts": [], "undetermined": [], "tokens": 0}
    birth, death = life["birth_year"], life["death_year"]
    name = str(mode.get("figure_name") or mode.get("figure_name_zh") or "").strip()
    if not name:
        # Phase41-Z3：模式缺 figure_name（实测 30 条）时回退到 data/figures 的名字，
        # 否则这些模式的年份会因「名字为空」被一律降级为不可判定（假盲区）。
        name = str(life.get("figure_name") or "").strip()
    lo, hi = birth - D5_WINDOW_BEFORE, death + D5_WINDOW_AFTER

    conflicts, undetermined = [], []
    tokens = 0
    # Phase41-Z3：统一走 iter_field_text —— list/str/None 三种载荷一致对待，
    # 且按**原子文本**扫描，上下文窗口不跨 list 元素边界。
    for field, text in iter_field_text(mode, D5_SCAN_FIELDS):
        for m in D5_YEAR_RE.finditer(text):
            year = int(m.group(1))
            tokens += 1
            if birth <= year <= death:
                continue
            ctx = text[max(0, m.start() - D5_NAME_RADIUS): m.end() + D5_NAME_RADIUS]
            item = {"field": field, "year": year, "context": ctx}
            if not (lo <= year <= hi):
                item["reason"] = "out-of-window: 离生卒年过远（对照 / 现代 / 史料年代），不可判定"
                undetermined.append(item)
                continue
            if field not in D5_CLAIM_FIELDS:
                item["reason"] = "field-not-claim: %s 记的是所引文献 / 史料标注，不是本人行事" % field
                undetermined.append(item)
                continue
            if not name or len(name) < 2 or name not in ctx:
                item["reason"] = "name-not-in-context: 年份不与人物名同现（背景 / 他人事件）"
                undetermined.append(item)
                continue
            hit_src = [k for k in D5_EXCLUDE_SOURCE if k in ctx]
            hit_after = [k for k in D5_EXCLUDE_AFTER if k in ctx]
            hit_bg = [k for k in D5_EXCLUDE_BACKGROUND if k in ctx]
            if hit_src:
                item["reason"] = "source-marker: 上下文含文献 / 出版形态标记 %s" % ",".join(hit_src[:3])
                undetermined.append(item)
                continue
            if hit_after:
                item["reason"] = "afterlife-marker: 上下文含卒后余波 / 后人事件标记 %s" % ",".join(hit_after[:3])
                undetermined.append(item)
                continue
            if hit_bg:
                item["reason"] = "background-marker: 上下文含背景 / 年代区间标记 %s" % ",".join(hit_bg[:3])
                undetermined.append(item)
                continue
            conflicts.append(item)

    if conflicts:
        return {"status": "conflict", "reason": "year-outside-lifespan", "conflicts": conflicts,
                "undetermined": undetermined, "tokens": tokens}
    if tokens:
        return {"status": "clean", "reason": "no-conflicting-year", "conflicts": [],
                "undetermined": undetermined, "tokens": tokens}
    return {"status": "undetermined", "reason": "no-four-digit-year-in-text", "conflicts": [],
            "undetermined": undetermined, "tokens": 0}


def d5_message(item: dict) -> str:
    return ("D5 时间线矛盾(警告): %s=%d 落在人物生卒年之外 (context: %s)"
            % (item["field"], item["year"], item["context"].replace("\n", " ")))


def check_d5_timeline_conflict(mode: dict, lifespans: dict | None = None,
                               root: Path | None = None) -> list[str]:
    """D5: 时间线矛盾（本人叙述字段里的年份落在生卒年之外）-> 警告（非阻断）。

    只报「通过全部过滤」的强信号；被降级为不可判定的年份由 d5_scan 逐条给出理由，
    统计在 gate 报告与 findings.json 的 audit_meta.d5 里（不静默放过）。
    """
    if lifespans is None:
        lifespans = load_figure_lifespans(root)
    return [d5_message(c) for c in d5_scan(mode, lifespans)["conflicts"]]


def load_source_cache(root: Path | None = None):
    """延迟导入 tools/source_text_cache.py（夹具目录里没有它时降级为「无缓存」）。"""
    import importlib.util
    base = Path(root) if root else REPO_ROOT
    for candidate in (base / "tools" / "source_text_cache.py",
                      TOOLS_DIR / "source_text_cache.py"):
        if candidate.is_file():
            try:
                spec = importlib.util.spec_from_file_location("source_text_cache_gate", candidate)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod
            except Exception:
                return None
    return None


def load_link_index():
    """延迟导入 tools/source_link_index.py（出处 -> 引文/链接 的唯一匹配实现）。"""
    import importlib.util
    candidate = TOOLS_DIR / "source_link_index.py"
    if candidate.is_file():
        try:
            spec = importlib.util.spec_from_file_location("source_link_index_gate", candidate)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        except Exception:
            return None
    return None


class _EmptyCache:
    """缓存模块缺失时的替身：任何 key 都不可用（语义 = 全部 unchecked）。"""

    def __init__(self):
        self.index_path = REPO_ROOT / "data" / "audit" / "source_texts.json"
        self.entries = {}
        self.present = False
        self._module = None

    def status_of(self, key):
        return "cache-module-missing"

    def text_for(self, key):
        return None


def make_cache(root: Path | None = None):
    """构造原文缓存对象；模块缺失时返回空缓存替身（不假装有文本）。"""
    mod = load_source_cache(root)
    if mod is None:
        return _EmptyCache()
    cache = mod.load_cache()
    cache._module = mod
    return cache


def d4_scan(mode: dict, cache, link_index) -> dict:
    """D4 单条模式 -> {status: matched|mismatch|unchecked|quote-too-short, reason, key}。

    可核条件（三者同时满足）：出处里有书名号引文 / 引文解析到**原文类**链接
    (wikisource|gutenberg|ctext) / 该 key 的缓存状态为 ok。其余一律 unchecked 并给理由。
    """
    # Phase41-Z3：list/str/None 混载一致取文本（key_quote_zh 有 17 条是 list、
    # source_chapter 有 30 条是 list，旧写法会整段跳过 / 传给 extract_refs 的类型不确定）。
    quote = field_text(mode, "key_quote_zh") or field_text(mode, "key_quote")
    source = field_text(mode, "source_chapter")
    if not (isinstance(quote, str) and quote.strip()):
        return {"status": "unchecked", "reason": "no-quote", "key": None}
    if cache is None or link_index is None or getattr(cache, "_module", None) is None:
        return {"status": "unchecked", "reason": "cache-or-link-index-missing", "key": None}
    mod = cache._module
    links_path = Path(cache.index_path).parent.parent / "data" / "source_links.json"
    if not links_path.is_file():
        links_path = REPO_ROOT / "data" / "source_links.json"
    try:
        index = link_index.load_index(links_path)
    except Exception:
        return {"status": "unchecked", "reason": "source-links-unreadable", "key": None}
    refs = [link_index.resolve_citation(inner, index)
            for inner in link_index.extract_refs(source)]
    if not refs:
        return {"status": "unchecked", "reason": "no-citation: 出处里没有书名号引文", "key": None}
    status, key, reason = mod.cache_status_for_citations(refs, cache)
    if status != "checkable":
        return {"status": "unchecked", "reason": reason, "key": key}
    text = cache.text_for(key)
    if not text:
        return {"status": "unchecked", "reason": "cache-file-missing:%s" % key, "key": key}
    result, detail = mod.check_quote(quote, text)
    if result == "matched":
        return {"status": "matched", "reason": "substring-found", "key": key, "detail": detail}
    if result == "quote-too-short":
        return {"status": "quote-too-short",
                "reason": "all-fragments-shorter-than-min(%d)" % mod.MIN_FRAGMENT, "key": key}
    if result == "script-mismatch":
        # N5 繁简守卫：缓存原文是繁体、引文是简体 —— 字面比对无意义，标不可核（不判不符）
        return {"status": "unchecked",
                "reason": "script-mismatch(原文繁体 vs 引文简体: 字面比对无意义)", "key": key}
    return {"status": "mismatch", "reason": "substring-not-found", "key": key, "detail": detail}


def d4_message(res: dict) -> str:
    return ("D4 引文不符(警告): 出处 %s 的原文里找不到 key_quote_zh 的字面片段"
            " (最长片段: %s)" % (res.get("key"), str(res.get("detail"))[:40]))


def check_d4_quote_mismatch(mode: dict, cache=None, link_index=None) -> list[str]:
    """D4: 引文不符 —— key_quote_zh 的字面片段**不出现**于所标出处的原文（警告，非阻断）。

    与旧空壳的区别：真去比对原文（缓存文本的子串）。可核前提见 d4_scan；
    取不到原文的条目标 unchecked 并计入统计，**不假装核过**。
    """
    if cache is None:
        cache = make_cache()
    if link_index is None:
        link_index = load_link_index()
    res = d4_scan(mode, cache, link_index)
    if res["status"] == "mismatch":
        return [d4_message(res)]
    return []


def check_d6_dangling_ref(mode: dict, all_mode_codes: set[str]) -> list[str]:
    """D6: 悬空引用 - cross_references/related_modes point to non-existent mode_code."""
    errors = []

    for field in ("cross_references", "related_modes"):
        refs = mode.get(field, [])
        if isinstance(refs, list):
            for ref in refs:
                if ref and ref not in all_mode_codes:
                    errors.append(f"D6 悬空引用: {field} 指向不存在的 mode_code={ref}")

    return errors


def empty_d45_stats() -> dict:
    """D4/D5 报告用的累加器（Phase40-Z2）。"""
    return {"d4": {}, "d4_reasons": {}, "d4_mismatches": [],
            "d5": {}, "d5_reasons": {}, "d5_undetermined_reasons": {},
            "d5_tokens": 0, "d5_conflicts": [], "d5_undetermined": [],
            "life_figures": 0, "modes_with_lifespan": 0, "cache_keys": 0, "cache_present": False}


def run_gate(
    data: dict,
    negative_test: bool = False,
    injected_d3_mode: dict | None = None,
    apply_d3_exemption: bool = True,
    quarantine: set[str] | None = None,
    lifespans: dict | None = None,
    cache=None,
    link_index=None,
    root: Path | None = None,
    stats: dict | None = None,
) -> tuple[list[str], list[str], list[str]]:
    """Run credibility gate.

    Returns (hard_failures, warnings, d3_exempted_mode_codes)——
    第三个返回值是「按豁免条款跳过 D3 扫描」的 mode_code 列表（已排序），
    用于如实报告豁免面，避免「静默跳过」被当成「零缺陷」。
    """
    quarantine = load_quarantine() if quarantine is None else quarantine
    all_modes = get_all_modes(data)

    # Phase40-Z2: D4/D5 的真实依赖（生卒年 / 原文缓存 / 出处索引），都做延迟加载：
    # 夹具目录里没有这些文件时降级为「不可核 / 不可判定」，绝不假装核过。
    life = lifespans if lifespans is not None else load_figure_lifespans(root)
    cache_obj = cache if cache is not None else make_cache(root)
    link_idx = link_index if link_index is not None else load_link_index()
    if stats is not None:
        stats["life_figures"] = len(life)
        stats["cache_keys"] = len(getattr(cache_obj, "usable_keys", lambda: [])())
        stats["cache_present"] = bool(getattr(cache_obj, "present", False))
    all_mode_codes = {m.get("mode_code", "") for m in all_modes if isinstance(m, dict) and m.get("mode_code")}

    # Add injected mode for negative test
    if negative_test and injected_d3_mode:
        all_modes = [injected_d3_mode] + all_modes

    hard_failures = []
    warnings = []
    d3_exempted: list[str] = []

    for mode in all_modes:
        if not isinstance(mode, dict):
            continue

        mode_code = mode.get("mode_code", "UNKNOWN")

        # D3 豁免登记（已隔离 figure）——判定依据见 is_d3_exempt()
        src_text = field_text(mode, "source_chapter")
        has_source = bool(src_text.strip())
        if apply_d3_exemption and quarantine and has_source and is_d3_exempt(mode, quarantine):
            d3_exempted.append(str(mode_code))

        # Hard gates (D1, D2, D3, D6)
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d1_fake_figure(mode, quarantine)])
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d2_fake_source(mode)])
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d3_pollution(mode, quarantine, apply_d3_exemption)])
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d6_dangling_ref(mode, all_mode_codes)])

        # Warnings (D4, D5) —— Phase40-Z2 起是真检查（旧版 D4 是结构 stub、D5 直接 return []）
        d4 = d4_scan(mode, cache_obj, link_idx)
        d5 = d5_scan(mode, life)
        if d4["status"] == "mismatch":
            warnings.append(f"[{mode_code}] {d4_message(d4)}")
        for item in d5["conflicts"]:
            warnings.append(f"[{mode_code}] {d5_message(item)}")
        if stats is not None:
            stats["d4"][d4["status"]] = stats["d4"].get(d4["status"], 0) + 1
            stats["d4_reasons"][d4["reason"]] = stats["d4_reasons"].get(d4["reason"], 0) + 1
            if d4["status"] == "mismatch":
                stats["d4_mismatches"].append({"mode_code": mode_code, "key": d4.get("key"),
                                               "field": "key_quote_zh", "reason": d4["reason"],
                                               "detail": str(d4.get("detail"))[:60]})
            stats["d5"][d5["status"]] = stats["d5"].get(d5["status"], 0) + 1
            if d5["status"] != "undetermined":
                stats["d5_reasons"][d5["reason"]] = stats["d5_reasons"].get(d5["reason"], 0) + 1
            stats["d5_tokens"] += d5["tokens"]
            if str(mode.get("figure_code") or "") in life:
                stats["modes_with_lifespan"] += 1
            if d5["conflicts"]:
                for item in d5["conflicts"]:
                    stats["d5_conflicts"].append({"mode_code": mode_code,
                                                  "figure_code": mode.get("figure_code"),
                                                  **item})
            for item in d5["undetermined"]:
                stats["d5_undetermined"].append({"mode_code": mode_code,
                                                 "figure_code": mode.get("figure_code"), **item})

    return hard_failures, warnings, sorted(set(d3_exempted))


def print_d45_report(stats: dict, limit: int = 12) -> None:
    """如实打印 D4/D5 的覆盖 / 命中 / 不可核（不可判定）面 —— 不许静默放过。"""
    print("")
    print("--- D4 引文不符（真子串核验，Phase40-Z2）---")
    d4 = stats.get("d4", {})
    order = ("matched", "mismatch", "quote-too-short", "unchecked")
    total = sum(d4.values())
    print("  可核面: 缓存 key 可用 %d 个 (index present=%s)；参与判定的模式 %d 条"
          % (stats.get("cache_keys", 0), stats.get("cache_present"), total))
    for k in order:
        if d4.get(k):
            print("  %-16s %5d" % (k, d4[k]))
    for k, v in sorted(d4.items()):
        if k not in order:
            print("  %-16s %5d" % (k, v))
    print("  不可核理由分布（unchecked/quote-too-short 逐类计数）:")
    for r, n in sorted(stats.get("d4_reasons", {}).items(), key=lambda kv: -kv[1])[:limit]:
        print("    %-56s %5d" % (r[:56], n))
    if stats.get("d4_mismatches"):
        print("  D4 命中（字面片段在原文里找不到）样例:")
        for e in stats["d4_mismatches"][:limit]:
            print("    %s  key=%s  最长片段=%s" % (e["mode_code"], e.get("key"), e.get("detail")))
    print("  说明: 只对「出处有书名号引文 + 引文解析到原文类链接 + 缓存状态 ok」的模式可核；"
          "其余一律 unchecked 并计入上面的理由分布 —— **不假装核过**。"
          "命中只代表「字面不符」，不等于伪造（繁简/异体/意译都不命中，处置为复核）。")

    print("")
    print("--- D5 时间线矛盾（生卒年 × 文本年份，Phase40-Z2）---")
    d5 = stats.get("d5", {})
    print("  生卒年可用人物: %d 个（data/figures/*.json，含字符串/公元前纪年解析）" % stats.get("life_figures", 0))
    print("  可判定模式: %d 条（figure 有生卒年）" % stats.get("modes_with_lifespan", 0))
    print("  扫描到的 4 位年份 token: %d 个" % stats.get("d5_tokens", 0))
    for k in ("conflict", "clean", "undetermined"):
        if d5.get(k):
            print("  %-16s %5d" % (k, d5[k]))
    for k, v in sorted(d5.items()):
        if k not in ("conflict", "clean", "undetermined"):
            print("  %-16s %5d" % (k, v))
    print("  不可判定（逐类计数，禁止当成「零缺陷」）:")
    for r, n in sorted(stats.get("d5_undetermined_reasons", {}).items(), key=lambda kv: -kv[1])[:limit]:
        print("    %-56s %5d" % (r[:56], n))
    if stats.get("d5_conflicts"):
        print("  D5 命中（本人叙述字段里的年份落在生卒年之外）:")
        for e in stats["d5_conflicts"][:limit]:
            print("    %s  %s=%s  %s" % (e["mode_code"], e["field"], e["year"],
                                         e["context"].replace("\n", " ")[:70]))
    else:
        print("  D5 命中: 0 条（本次全库扫描无「通过全部过滤」的矛盾）")
    print("  说明: 判定顺序 = 生卒年可用 -> 4 位年份 -> 生涯带 [生年-%d, 卒年+%d] -> 字段为本人叙述字段"
          " -> 年份与人物名同现(±%d 字) -> 无文献/余波/背景标记。任一环不满足即进「不可判定」并给出理由。"
          % (D5_WINDOW_BEFORE, D5_WINDOW_AFTER, D5_NAME_RADIUS))


def main() -> int:
    parser = argparse.ArgumentParser(description="Credibility Gate for Protreptic modes")
    parser.add_argument("--negative-test", action="store_true",
                        help="Inject a D3 sample and verify gate catches it (exit 1)")
    parser.add_argument("--data-path", type=str, default=str(DEFAULT_DATA_PATH),
                        help="Path to modes_data.json")
    parser.add_argument("--no-d3-exemption", action="store_true",
                        help="关闭 D3 豁免（严格模式）：连已隔离 figure 的 source_chapter 一起扫。"
                             "默认开启豁免，依据 credibility_framework.md §1 D3 豁免条款")
    parser.add_argument("--legacy-report", action="store_true",
                        help="存量/新增两档之「只报告」：基线内与基线外都逐条列出，一律 exit 0（不阻断）")
    parser.add_argument("--hard-fail", action="store_true",
                        help="存量/新增两档之「新增即拦」：基线内（data/audit/credibility_baseline.json）"
                             "的存量只报告，基线外的任何硬失败 exit 1")
    parser.add_argument("--baseline", type=str, default=None,
                        help=f"基线文件路径；缺省随 --data-path 所在仓推导（{DEFAULT_BASELINE_PATH}）")
    parser.add_argument("--write-baseline", action="store_true",
                        help="用当前硬失败重新冻结基线（改基线必须显式跑这一步并在报告里说明）")
    args = parser.parse_args()

    apply_d3_exemption = not args.no_d3_exemption

    # Phase37-X3：--data-path 的完整语义 —— 数据 / 白名单 / 基线三者同仓
    data_path = Path(args.data_path) if args.data_path else DEFAULT_DATA_PATH
    repo_root = resolve_repo_root(data_path)
    quarantine = load_quarantine(repo_root)
    baseline_path = (Path(args.baseline) if args.baseline
                     else repo_root / "data" / "audit" / "credibility_baseline.json")

    data = load_modes_data(data_path)

    if args.negative_test:
        # Inject a D3 sample: source_chapter with "sha256" pollution
        injected = {
            "mode_code": "M-NEGATIVE-TEST-D3",
            "figure_code": "H-TEST-001",
            "name_zh": "负对照测试模式",
            "name_en": "Negative Test Mode",
            "source_chapter": "Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4...）",
            "key_quote_zh": "测试引文",
        }
        failures, warnings, exempted = run_gate(
            data, negative_test=True, injected_d3_mode=injected,
            apply_d3_exemption=apply_d3_exemption, quarantine=quarantine)

        print("=== NEGATIVE TEST MODE ===")
        print(f"D3 exemption: {'on' if apply_d3_exemption else 'off (--no-d3-exemption)'}")
        print(f"Injected D3 sample: {injected['source_chapter']}")
        print(f"Hard failures: {len(failures)}")
        print(f"Warnings: {len(warnings)}")
        print(f"D3-exempted modes (quarantined figures, not scanned): {len(exempted)}")
        for f in failures:
            print(f"  FAIL: {f}")
        for w in warnings:
            print(f"  WARN: {w}")

        # Negative test MUST fail (exit 1) if D3 is caught
        if any("D3 出处污染" in f for f in failures):
            print("\n[OK] Negative test PASSED: D3 pollution correctly caught -> exit 1")
            return 1
        else:
            print("\n[FAIL] Negative test FAILED: D3 pollution NOT caught -> exit 0 (should be 1)")
            return 0

    # Normal gate run（Phase40-Z2 起带 D4/D5 统计）
    stats = empty_d45_stats()
    failures, warnings, exempted = run_gate(data, apply_d3_exemption=apply_d3_exemption,
                                            quarantine=quarantine, root=repo_root,
                                            stats=stats)
    for item in stats["d5_undetermined"]:
        stats["d5_undetermined_reasons"][item["reason"].split(":")[0]] = \
            stats["d5_undetermined_reasons"].get(item["reason"].split(":")[0], 0) + 1

    # Phase37-X3 两档模式 / 基线冻结：存量只报告，新增即拦
    if args.write_baseline or args.legacy_report or args.hard_fail:
        rc = run_baseline_mode(args, failures, warnings, exempted,
                               baseline_path=baseline_path, data_path=data_path)
        if args.legacy_report or args.hard_fail:
            print_d45_report(stats)
        return rc

    d3_failures = [f for f in failures if "D3 出处污染" in f]

    print("=== CREDIBILITY GATE ===")
    print(f"resolved data path: {data_path}")
    print(f"Total modes checked: {len(get_all_modes(data))}")
    print(f"Hard failures (D1/D2/D3/D6): {len(failures)}")
    print(f"  of which D3 出处污染: {len(d3_failures)}")
    print(f"Warnings (D4/D5): {len(warnings)}")
    print_d45_report(stats)
    print(f"D3 exemption: {'on' if apply_d3_exemption else 'off (--no-d3-exemption)'}")

    # 豁免面如实公布（避免「静默跳过」被读成「零缺陷」）
    if apply_d3_exemption and exempted:
        figs = {}
        for m in get_all_modes(data):
            if not isinstance(m, dict):
                continue
            if str(m.get("mode_code", "")) in exempted:
                fc = str(m.get("figure_code", "") or "")
                figs[fc] = figs.get(fc, 0) + 1
        print(f"D3-exempted modes (D1 quarantined figures, not scanned): {len(exempted)}")
        print(f"  exempted mode_codes: {', '.join(exempted)}")
        print(f"  by figure: {', '.join(f'{k}={v}' for k, v in sorted(figs.items()))}")
        print(f"  whitelist source: tools/_quarantine.py QUARANTINE = {sorted(quarantine)}")
        print("  basis: credibility_framework.md §1 D3 豁免条款 / §4 豁免逻辑"
              "（D1 已隔离记录允许保留源库工程痕迹，以导出期过滤为准）")
    elif apply_d3_exemption:
        print("D3-exempted modes (D1 quarantined figures, not scanned): 0")

    if failures:
        print("\n--- HARD FAILURES (blocking) ---")
        for f in failures[:20]:  # Limit output
            print(f"  ::error::{f}")
        if len(failures) > 20:
            print(f"  ... and {len(failures) - 20} more")

    if warnings:
        print("\n--- WARNINGS (non-blocking) ---")
        for w in warnings[:20]:
            print(f"  ::warning::{w}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more")

    if failures:
        print(f"\n[FAIL] Gate failed with {len(failures)} hard failures")
        return 1
    else:
        print("\n[OK] Gate passed (no hard failures)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
