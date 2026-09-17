#!/usr/bin/env python3
"""export_static_site.py — Phase 29-2 数据静态化。

把两套核心资产导出为前端可直接 fetch 的静态 JSON 分片（GitHub Pages 无后端）：

    源 1  data/modes_data.json   -> modes 列表（2868 -> 按 mode_code 首现去重 2858）
    源 2  api/protreptic.db      -> figures 表（501 行）

产物（默认落在 web/public/data/，Vite 会原样复制进 dist/）：

    figures.index.json          501 条轻量索引     目标 gzip <= 50 KB
    figures/{code}.json         501 个详情分片
    modes/index-{0..7}.json     2858 条摘要，md5(mode_code)%8 均分   单片 gzip <= 200 KB
    modes/by-figure/{fc}.json   284 个「某人的 10 条模式」分片（按 figure_code 原值分组）
    meta.json                   构建时间戳 + 各产物条数 + sha256

同时输出 docs/architecture/static_data_manifest.json 供数据治理卡引用。

踩坑规则（依据 docs/architecture/web_pages_migration_assessment.md §3.2，必须遵守）：
  x 不要按 H- 前缀分片 —— 2858 条里有 1670 条的 figure_code 是旧式三字母 slug
    （HCM / SUK / AlGhazali …），按前缀会把它们全挤进一个 1.78 MB 的分片。
  v 按 figure_code 原值分组 -> 恰好 284 片。
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

# ---------------------------------------------------------------- 常量

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "web" / "public" / "data"
MODES_JSON = REPO_ROOT / "data" / "modes_data.json"
DB_PATH = REPO_ROOT / "api" / "protreptic.db"
MANIFEST_PATH = REPO_ROOT / "docs" / "architecture" / "static_data_manifest.json"

SENTINEL = ".static_site_export"
N_SHARDS = 8
GZIP_LEVEL = 9

EXPECT_FIGURES = 1058
EXPECT_MODES = 2858
EXPECT_BY_FIGURE = 284

LIMIT_INDEX_GZIP = 50 * 1024
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

    for m in modes:
        fc = m.get("figure_code")
        if fc is None or str(fc).strip() == "":
            no_code_modes += 1
            continue
        by_figure.setdefault(str(fc), []).append(m)

    for m in sorted(modes, key=lambda x: str(x.get("mode_code"))):
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
    for fc in sorted(by_figure):
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
        "mode_summaries": sum(s["count"] for s in shard_stats),
        "mode_index_shards": N_SHARDS,
        "mode_by_figure_shards": len(fig_stats),
        "modes_raw": raw_modes_total,
        "modes_deduped": len(modes),
        "modes_duplicates_dropped": mode_stats["dropped_dup"],
        "modes_empty_mode_code_dropped": mode_stats["dropped_nocode"],
        "modes_without_figure_code": no_code_modes,
    }

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
        },
    }
    write_product(out_dir / "meta.json", meta)
    log(f"  meta.json               counts={json.dumps(counts, ensure_ascii=False)}")

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
            {"rule": "figures.index.json gzip <= 50 KB",
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
            failures.append("模式摘要总数与去重条数不一致")

    if idx_stat["gzip_bytes"] > LIMIT_INDEX_GZIP:
        failures.append(f"figures.index.json gzip {idx_stat['gzip_bytes']} > {LIMIT_INDEX_GZIP}")
    over = [s for s in shard_stats if s["gzip_bytes"] > LIMIT_MODE_SHARD_GZIP]
    if over:
        failures.append(f"{len(over)} 个 modes/index-*.json 分片 gzip 超 {LIMIT_MODE_SHARD_GZIP}")

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
    log(f"  [OK] figures={counts['figures']} modes={counts['modes_deduped']}"
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
