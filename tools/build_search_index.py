#!/usr/bin/env python3
"""build_search_index.py — Phase30-A5 全文检索索引分片构建（替代前端子串匹配）。

现状: 前端搜索是 mode_code / 名称 / 领域的子串匹配（web/src/api/static.ts 的
matchesKeyword + ModesView.vue 的 filtered）。本脚本按 Phase30-A0 的实测规格
（docs/architecture/web_p0_architecture.md 第 4 节，推荐规格实测 741 KB gzip）
构建二进制倒排索引分片，让前端能对 name / category / source / concepts / domain /
definition 做真正的倒排检索。

输入
    web/public/data/modes/index-0..7.json   —— 决定 doc_id 顺序（export_static_site.py 产物）
    data/modes_data.json                    —— 正文字段来源（index 分片只有 8 个轻字段）

输出
    web/public/data/search/index-0.bin ... index-15.bin   16 个倒排分片
    web/public/data/search/meta.json                      条数 / 分片数 / 体积 / sha256 / 规格

doc_id 契约（A0 定的，不要改）
    doc_id = 该 mode 在 modes/index-0.json..index-7.json **按序拼接**后的下标（2848 条）。
    前端为 /modes 本来就要拉这 8 个分片并拼接，因此拿到 doc_id 可直接查表取
    mode_code / figure_code / figure_name / name / category / domain 用于展示，
    所以 **不需要下发词典文件**（单独一份 5 字段词典实测 194 KB gzip，会击穿预算）。

分片函数
    bucket = crc32(utf8(token 首字符)) % 16
    中文查询按 2-gram 切分，首字符决定唯一分片，因此一次查询只需拉「查询串里出现过的
    首字符」对应的那几片（典型 4 字中文查询 <= 3 片，最坏约 177 KB gzip）。
    不能用 crc32(整个 token)：那样每次查询都要拉全部 16 片。

文件格式（每个分片，见 meta.json 的 format 字段，前端解码以此为准）
    file   = varint(len(body)) + body + varint(len(weights)) + weights
    body   = token 记录序列（token 升序）：
                 varint(len(utf8(token))) + utf8(token) + varint(df) + varint(升序 doc_id 差值)
             doc_id 差值的第一个值 = 首个 doc_id 本身。（这一段与 A0 记录格式逐字节一致）
    weights = 每 token 1 字节，取值 0/1/2 = 权重 4/2/1，顺序与 body 里的 token 一致。
    权重表 = 按同一 token 升序，每 token 1 字节，取值 0/1/2 = 权重 4/2/1（追加在记录体之后）。
    权重是 token 级（该 token 在全部字段里出现的最高字段权重），不是 posting 级：
    逐 posting 存权重实测 866 KB gzip 超预算，token 级权重表只多约 20 KB。

预算口径（Phase43-R10，2026-09-21 改）
    有效预算 = min(1024 KB, max(800 KB, ceil(模式数 × 0.32 KB)))
    超有效预算 → 非 0 退出；使用率 >= 90% → 打印 WARN（不阻断，GitHub Actions 下额外发 ::warning)。
    --budget-kb 显式指定时以该值为准，不加地板/天花板（用于本地压测与负对照）。

用法
    python3 tools/build_search_index.py                     # 写 web/public/data/search
    python3 tools/build_search_index.py --budget-kb 700     # 显式覆盖有效预算（压测/负对照）
    python3 tools/build_search_index.py --out public/data/search
    python3 tools/build_search_index.py --no-assert-budget  # 数据涨了、临时放行
    python3 tools/build_search_index.py --quiet             # 不打印抽样查询
    python3 tools/build_search_index.py --self-test         # 只做解码回环自检

退出码: 0 成功；1 输入缺失 / 自检失败 / 体积超预算。
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import sys
import unicodedata
import zlib
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "web" / "public" / "data" / "search"
MODES_INDEX_DIR = REPO_ROOT / "web" / "public" / "data" / "modes"
MODES_JSON = REPO_ROOT / "data" / "modes_data.json"
MODES_INDEX_SHARDS = 8

SPEC_VERSION = "1.1-a5"
N_SHARDS = 16
GZIP_LEVEL = 9
# ---- 预算口径（Phase43-R10 收口，依据与推导见 docs/architecture/web_p0_architecture.md §4.10）----
# 硬失败不变：总 gzip > 有效预算 → 非 0 退出（CI 卡死发布）。
# 有效预算 = min(天花板, max(地板, ceil(模式数 × 每条系数)))，三段都有实测依据：
BUDGET_FLOOR_GZIP_KB = 800     # A5 卡原始约束；数据规模 <= 2500 条时它就是有效预算
BUDGET_PER_MODE_KB = 0.32      # 每条模式配额 = 实测均值 0.2711 KB/条 ÷ 0.85（相对预算口径留 15% 余量）
BUDGET_CEILING_GZIP_KB = 1024  # 绝对天花板：分片按需拉取 + SW cache-first，一次性离线预算上限
WARN_BUDGET_RATIO = 0.90       # 使用率达到有效预算的该比例 → WARN（只提示，不阻断）
MEASURED_MARGINAL_BYTES = 243  # 实测边际：2500→2798 条时 0.237 KB/条（仅用于 WARN 文案的换算）
WEIGHT_TIERS = (4, 2, 1)
# 权重表编码：1 字节/token，取值 0/1/2 对应权重 4/2/1（顺序即 WEIGHT_TIERS 下标）
WEIGHT_CODE = {w: i for i, w in enumerate(WEIGHT_TIERS)}
WEIGHT_BY_CODE = {i: w for i, w in enumerate(WEIGHT_TIERS)}

# (字段, 权重, 截断字符数[0 = 不截断], 是否逐条截断[列表字段])
# 这一张表就是 A0 第 4.3 节的推荐规格，改它就是改规格，必须同步 meta.json 与文档。
FIELDS = [
    ("figure_name", 4, 0, False),
    ("name_zh", 4, 0, False),
    ("name_en", 4, 0, False),
    ("category", 2, 0, False),
    ("source_chapter", 2, 40, False),
    ("key_concepts", 2, 60, True),
    ("domain_zh", 2, 30, False),
    ("definition_zh", 1, 30, False),
    ("definition_en", 1, 30, False),
]

SAMPLE_QUERIES = ["良知", "王阳明", "战略 决策", "幂势既同", "decision", "decis"]
TOKENIZE_SPEC = {
    "normalize": "NFKC",
    "cjk": "连续 CJK 串取全部 2-gram；长度 1 的串取该字本身",
    "cjk_ranges": ["U+3400-U+4DBF", "U+4E00-U+9FFF", "U+F900-U+FAFF"],
    "latin": "连续拉丁/数字串转小写，长度 >= 2 的词（不做前缀扩展）",
}


# ------------------------------------------------------------------ 工具

def varint(n: int) -> bytes:
    out = bytearray()
    while True:
        x = n & 0x7F
        n >>= 7
        if n:
            out.append(x | 0x80)
        else:
            out.append(x)
            return bytes(out)


def read_varint(buf: bytes, pos: int) -> tuple[int, int]:
    shift = 0
    val = 0
    while True:
        b = buf[pos]
        pos += 1
        val |= (b & 0x7F) << shift
        if not b & 0x80:
            return val, pos
        shift += 7


def is_cjk(ch: str) -> bool:
    o = ord(ch)
    return (0x3400 <= o <= 0x4DBF) or (0x4E00 <= o <= 0x9FFF) or (0xF900 <= o <= 0xFAFF)


def tokenize(text: str) -> list[str]:
    """A0 第 4.3 节分词规则；查询期必须用同一函数（前端有一份等价实现）。"""
    if not text:
        return []
    t = unicodedata.normalize("NFKC", str(text))
    out: list[str] = []
    i, n = 0, len(t)
    while i < n:
        ch = t[i]
        if is_cjk(ch):
            j = i
            while j < n and is_cjk(t[j]):
                j += 1
            run = t[i:j]
            if len(run) == 1:
                out.append(run)
            else:
                out.extend(run[k:k + 2] for k in range(len(run) - 1))
            i = j
        elif ch.isalnum():
            j = i
            while j < n and t[j].isalnum() and not is_cjk(t[j]):
                j += 1
            w = t[i:j].lower()
            if len(w) >= 2:
                out.append(w)
            i = j
        else:
            i += 1
    return out


def shard_of(token: str) -> int:
    """bucket = crc32(utf8(token 首字符)) % 16 —— 查询期可算，见 A0 4.3。"""
    return zlib.crc32(token[0].encode("utf-8")) % N_SHARDS


def prep_field(value, limit: int, per_item: bool) -> str:
    """取字段文本：列表字段拼空格；per_item=True 时逐条截断（key_concepts 的实测口径）。"""
    if value is None:
        return ""
    if isinstance(value, list):
        if per_item and limit:
            text = " ".join(str(x)[:limit] for x in value)
        else:
            text = " ".join(str(x) for x in value)
        text = unicodedata.normalize("NFKC", text)
    else:
        text = unicodedata.normalize("NFKC", str(value))
    text = text.strip()
    if limit and not per_item:
        text = text[:limit]
    return text


# ------------------------------------------------------------------ 输入

def load_docs(modes_dir: Path) -> list[dict]:
    """doc_id 顺序 = modes/index-0..7.json 按序拼接（A0 硬契约）。"""
    docs: list[dict] = []
    for i in range(MODES_INDEX_SHARDS):
        p = modes_dir / f"index-{i}.json"
        if not p.exists():
            raise SystemExit(
                f"[FATAL] 缺少 {p} —— 请先跑 python3 tools/export_static_site.py "
                f"（它会清空并重建 web/public/data/，本脚本必须排在它之后）"
            )
        data = json.loads(p.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else next(
            (v for v in data.values() if isinstance(v, list)), None
        )
        if items is None:
            raise SystemExit(f"[FATAL] {p} 结构无法识别（既不是 list 也没有 list 值）")
        docs.extend(items)
    if not docs:
        raise SystemExit("[FATAL] modes index 分片为空")
    return docs


def load_records(path: Path) -> dict[str, dict]:
    """data/modes_data.json -> mode_code -> 正文字段（同 code 取首次出现，与 export 口径一致）。"""
    if not path.exists():
        raise SystemExit(f"[FATAL] 缺少 {path}")
    md = json.loads(path.read_text(encoding="utf-8"))
    modes = md.get("modes", md) if isinstance(md, dict) else md
    out: dict[str, dict] = {}
    for m in modes:
        mc = m.get("mode_code")
        if mc and mc not in out:
            out[mc] = m
    return out


# ------------------------------------------------------------------ 建索引

def build_postings(docs, records):
    """返回 (postings, token_weight)；postings[token] = 升序 doc_id 列表。"""
    postings: dict[str, set] = defaultdict(set)
    token_weight: dict[str, int] = {}
    for did, doc in enumerate(docs):
        mc = doc.get("mode_code")
        rec = records.get(mc)
        if rec is None:
            raise SystemExit(f"[FATAL] doc_id={did} mode_code={mc} 在 data/modes_data.json 里找不到")
        for field, weight, limit, per_item in FIELDS:
            # index 分片里的 8 个轻字段与 modes_data 完全一致（已实测），统一从后者取
            for tk in set(tokenize(prep_field(rec.get(field), limit, per_item))):
                postings[tk].add(did)
                if token_weight.get(tk, 0) < weight:
                    token_weight[tk] = weight
    return {k: sorted(v) for k, v in postings.items()}, token_weight


def encode_shards(postings, token_weight):
    """每个分片 = 升序 token 记录体 + 追加的权重表（token 级权重，附加段，不改 A0 记录格式）。"""
    order = sorted(postings)
    bodies = [bytearray() for _ in range(N_SHARDS)]
    weights = [bytearray() for _ in range(N_SHARDS)]
    counts = [0] * N_SHARDS
    for tk in order:
        idx = shard_of(tk)
        ids = postings[tk]
        tb = tk.encode("utf-8")
        bodies[idx] += varint(len(tb)) + tb + varint(len(ids))
        prev = 0
        for k, did in enumerate(ids):
            bodies[idx] += varint(did if k == 0 else did - prev)
            prev = did
        weights[idx].append(WEIGHT_CODE[token_weight[tk]])
        counts[idx] += 1
    shards, stats = [], []
    for i in range(N_SHARDS):
        blob = varint(len(bodies[i])) + bytes(bodies[i]) + varint(len(weights[i])) + bytes(weights[i])
        shards.append(blob)
        stats.append({"tokens": counts[i], "postings": 0})
    for tk in order:
        stats[shard_of(tk)]["postings"] += len(postings[tk])
    return shards, stats


def decode_shard(blob: bytes):
    """解码器（自检 & 前端参考实现）：返回 [(token, weight, [doc_id,...]), ...]。"""
    body_len, pos = read_varint(blob, 0)
    body_end = pos + body_len
    out = []
    while pos < body_end:
        tlen, pos = read_varint(blob, pos)
        token = blob[pos:pos + tlen].decode("utf-8")
        pos += tlen
        df, pos = read_varint(blob, pos)
        ids = []
        prev = 0
        for k in range(df):
            d, pos = read_varint(blob, pos)
            did = d if k == 0 else prev + d
            ids.append(did)
            prev = did
        out.append([token, None, ids])
    if pos != body_end:
        raise SystemExit(f"[FATAL] 分片 token 记录体越界: 期望 {body_end}, 实际 {pos}")
    wlen, pos = read_varint(blob, pos)
    if pos + wlen != len(blob):
        raise SystemExit(f"[FATAL] 权重表长度不符: {wlen} + {pos} != {len(blob)}")
    wmap = blob[pos:pos + wlen]
    if len(wmap) != len(out):
        raise SystemExit(f"[FATAL] 权重表条数 {len(wmap)} != token 数 {len(out)}")
    for i, code in enumerate(wmap):
        out[i][1] = WEIGHT_BY_CODE.get(code)
        if out[i][1] is None:
            raise SystemExit(f"[FATAL] 权重表出现未知编码 {code}")
    return [(t, w, ids) for t, w, ids in out]


def self_test(shards, postings, token_weight):
    """解码回环：解出来的 (token, weight, doc_ids) 必须与内存里的完全一致。"""
    seen = 0
    bad = 0
    for idx, blob in enumerate(shards):
        for token, w, ids in decode_shard(blob):
            if shard_of(token) != idx:
                bad += 1
            if postings.get(token) != ids or token_weight.get(token) != w:
                bad += 1
            seen += 1
    if seen != len(postings):
        raise SystemExit(f"[FATAL] 解码回环 token 数不一致: 解出 {seen}, 内存 {len(postings)}")
    if bad:
        raise SystemExit(f"[FATAL] 解码回环有 {bad} 处不一致")
    return seen


def query(postings, token_weight, docs, q: str, limit: int = 5):
    """本地验证用查询（与前端同一分词 + 权重和打分，无 IDF/BM25）。"""
    scores: dict[int, int] = defaultdict(int)
    for tk in tokenize(q):
        for did in postings.get(tk, []):
            scores[did] += token_weight[tk]
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]
    return [(docs[d].get("mode_code"), docs[d].get("figure_name"), s) for d, s in ranked]


def effective_budget_kb(doc_count: int, override: int | None = None) -> tuple[int, str]:
    """有效 gzip 预算（KB）与来源标签。

    override（--budget-kb）显式给出时优先，且不加地板/天花板 —— 显式旋钮就该是显式语义。
    派生口径：min(天花板, max(地板, ceil(模式数 × 每条系数)))，见文档 §4.10。
    """
    if override is not None:
        return override, "cli-override"
    derived = math.ceil(doc_count * BUDGET_PER_MODE_KB)
    if derived > BUDGET_CEILING_GZIP_KB:
        return BUDGET_CEILING_GZIP_KB, "ceiling"
    if derived < BUDGET_FLOOR_GZIP_KB:
        return BUDGET_FLOOR_GZIP_KB, "floor"
    return derived, "per-mode"


# ------------------------------------------------------------------ 主流程

def main() -> int:
    ap = argparse.ArgumentParser(description="构建全文检索索引分片（Phase30-A5）")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="输出目录（相对仓库根或绝对路径）")
    ap.add_argument("--modes-dir", default=str(MODES_INDEX_DIR), help="modes index 分片目录")
    ap.add_argument("--modes-data", default=str(MODES_JSON), help="data/modes_data.json 路径")
    ap.add_argument("--budget-kb", type=int, default=None,
                    help="显式覆盖有效预算 KB（默认按模式数派生，见模块 docstring 与文档 §4.10）")
    ap.add_argument("--no-assert-budget", action="store_true", help="超预算不失败（临时放行）")
    ap.add_argument("--quiet", action="store_true", help="不打印抽样查询")
    ap.add_argument("--self-test", action="store_true", help="只做解码回环自检，不写盘")
    args = ap.parse_args()

    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = REPO_ROOT / out_dir
    modes_dir = Path(args.modes_dir)
    if not modes_dir.is_absolute():
        modes_dir = REPO_ROOT / modes_dir
    modes_json = Path(args.modes_data)
    if not modes_json.is_absolute():
        modes_json = REPO_ROOT / modes_json

    docs = load_docs(modes_dir)
    records = load_records(modes_json)
    extra = set(records) - {d.get("mode_code") for d in docs}
    postings, token_weight = build_postings(docs, records)
    shards, per_shard = encode_shards(postings, token_weight)
    tokens_seen = self_test(shards, postings, token_weight)

    gz = [gzip.compress(blob, GZIP_LEVEL) for blob in shards]
    total_raw = sum(len(b) for b in shards)
    total_gz = sum(len(b) for b in gz)

    budget_kb, budget_source = effective_budget_kb(len(docs), args.budget_kb)
    usage_ratio = total_gz / (budget_kb * 1024)

    print(f"[search-index] docs={len(docs)} tokens={len(postings)} "
          f"postings={sum(len(v) for v in postings.values())}")
    print(f"[search-index] raw={total_raw / 1024:.1f} KB gzip={total_gz / 1024:.1f} KB "
          f"(预算 {budget_kb} KB [{budget_source}]，使用率 {usage_ratio * 100:.1f}%，"
          f"余量 {(budget_kb * 1024 - total_gz) / 1024:.1f} KB) "
          f"max_shard={max(len(b) for b in gz) / 1024:.1f} KB "
          f"min_shard={min(len(b) for b in gz) / 1024:.1f} KB")
    print(f"[search-index] 解码回环自检通过：{tokens_seen} 个 token 全部一致")

    if not args.quiet:
        for q in SAMPLE_QUERIES:
            hits = query(postings, token_weight, docs, q)
            print(f"[search-index] {q} -> {hits}")

    if args.self_test:
        return 0

    if usage_ratio >= WARN_BUDGET_RATIO:
        headroom_kb = (budget_kb * 1024 - total_gz) / 1024
        if total_gz > budget_kb * 1024:
            tail = "已超有效预算（见下方 FATAL）"
        else:
            tail = (f"接近硬上限：按实测边际 {MEASURED_MARGINAL_BYTES} B/条折算，"
                    f"约剩 {max(budget_kb * 1024 - total_gz, 0) // MEASURED_MARGINAL_BYTES} 条模式的量")
        warn = (f"[search-index] WARN 预算使用率 {usage_ratio * 100:.1f}% >= "
                f"{WARN_BUDGET_RATIO * 100:.0f}%（{total_gz / 1024:.1f} / {budget_kb} KB "
                f"[{budget_source}]，余量 {headroom_kb:.1f} KB）—— {tail}；"
                f"字段加宽/新增字段会立刻击穿（见文档 §4.10）")
        print(warn)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(f"::warning title=search-index budget::{warn.split('] ', 1)[1]}")

    if total_gz > budget_kb * 1024 and not args.no_assert_budget:
        raise SystemExit(
            f"[FATAL] 索引总 gzip {total_gz / 1024:.1f} KB 超有效预算 {budget_kb} KB "
            f"[{budget_source}]（模式数 {len(docs)}）—— 请按 A0 第 4.2 节收缩字段/截断"
            f"（不要动 idx 契约），或显式用 --budget-kb 调整（文档 §4.10）"
        )

    # 幂等重跑：清掉本脚本自己的产物（不动 by-figure / index-*.json 等别人家的分片）
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("index-*.bin"):
        old.unlink()

    shard_meta = []
    for i, blob in enumerate(shards):
        p = out_dir / f"index-{i}.bin"
        p.write_bytes(blob)
        shard_meta.append({
            "file": p.name,
            "raw_bytes": len(blob),
            "gzip_bytes": len(gz[i]),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "tokens": per_shard[i]["tokens"],
            "postings": per_shard[i]["postings"],
        })

    idx_files = []
    h = hashlib.sha256()
    for i in range(MODES_INDEX_SHARDS):
        raw = (modes_dir / f"index-{i}.json").read_bytes()
        h.update(raw)
        idx_files.append({"file": f"index-{i}.json", "sha256": hashlib.sha256(raw).hexdigest()})

    meta = {
        "spec_version": SPEC_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "tools/build_search_index.py",
        "doc_count": len(docs),
        "shard_count": N_SHARDS,
        "token_count": len(postings),
        "token_count_by_weight": {str(w): sum(1 for t in token_weight if token_weight[t] == w)
                                  for w in WEIGHT_TIERS},
        "postings_count": sum(len(v) for v in postings.values()),
        "total_raw_bytes": total_raw,
        "total_gzip_bytes": total_gz,
        "total_gzip_kb": round(total_gz / 1024, 1),
        "budget_gzip_kb": budget_kb,
        "budget": {
            "effective_gzip_kb": budget_kb,
            "source": budget_source,
            "formula": "min(ceiling_gzip_kb, max(floor_gzip_kb, ceil(doc_count * per_mode_kb)))",
            "per_mode_kb": BUDGET_PER_MODE_KB,
            "floor_gzip_kb": BUDGET_FLOOR_GZIP_KB,
            "ceiling_gzip_kb": BUDGET_CEILING_GZIP_KB,
            "warn_ratio": WARN_BUDGET_RATIO,
            "usage_ratio": round(usage_ratio, 4),
            "headroom_gzip_kb": round((budget_kb * 1024 - total_gz) / 1024, 1),
            "warn_triggered": usage_ratio >= WARN_BUDGET_RATIO,
            "doc_count": len(docs),
            "measured_bytes_per_mode": round(total_gz / len(docs), 1),
        },
        "max_shard_gzip_kb": round(max(len(b) for b in gz) / 1024, 1),
        "min_shard_gzip_kb": round(min(len(b) for b in gz) / 1024, 1),
        "shards": shard_meta,
        "sources": {
            "modes_data": str(modes_json.relative_to(REPO_ROOT)),
            "modes_data_sha256": hashlib.sha256(modes_json.read_bytes()).hexdigest(),
            "modes_index_concat_sha256": h.hexdigest(),
            "modes_index_files": idx_files,
            "modes_index_extra_records_not_indexed": len(extra),
        },
        "format": {
            "file": "varint(len(body)) + body + varint(len(weights)) + weights",
            "body": "varint(len(utf8(token))) + utf8(token) + varint(df) + varint(doc_id 升序差值)",
            "first_delta": "第一个差值是首个 doc_id 本身",
            "weights": "每 token 1 字节，顺序与 body 一致；取值 0/1/2 = 权重 4/2/1",
            "weight_codes": {str(w): c for w, c in WEIGHT_CODE.items()},
            "compression": "gzip level 9，前端 fetch 时浏览器自动解压",
            "weight_semantics": "token 级：该 token 在全部字段中出现的最高字段权重；"
                                "不是 posting 级（逐 posting 存权重实测 866 KB gzip，超预算）",
        },
        "doc_id_contract": "该 mode 在 modes/index-0..7.json 按序拼接后的下标，共 %d 条" % len(docs),
        "shard_fn": "crc32(utf8(token[0])) %% %d" % N_SHARDS,
        "tokenize": TOKENIZE_SPEC,
        "fields": [{"field": f, "weight": w, "truncate_chars": lim, "per_item": pi}
                   for f, w, lim, pi in FIELDS],
        "known_gaps": [
            "拉丁词不做前缀扩展（decis 无结果、decision 有结果）",
            "相关性只是权重和，无 IDF / BM25 / 长度归一",
            "representative_cases / modern_applications / 完整 definition 不在索引里",
            "英文语料只有 name_en 与 definition_en 首 30 字符",
        ],
    }
    meta_path = out_dir / "meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[search-index] 写出 {N_SHARDS} 个分片 + meta.json -> {out_dir}")
    print(f"[search-index] meta: {meta_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
