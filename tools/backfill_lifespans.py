#!/usr/bin/env python3
"""backfill_lifespans.py -- 生卒年「补数」清单（Phase42-Z4，可重入）。

背景（船长 2026-09-21 独立核验，可复现）
    Z3 修好字段类型盲区后，全库 tokens=0 仍有 2292 条（79.4%）。拆成因发现主因不是
    「文本里没有年份」，而是「该 figure 拿不到生卒年」——1736 条模式所属 figure 被
    `load_figure_lifespans()` 判为「无生卒年」，而其中 56 个 figure 的日期**就在
    `data/figures/*.json` 里**，只是旧取值口径取不到：

      * 旧口径 = `doc["figure_code"] or code or id` 的**第一个非空值**；而实测 347 个
        figure 文件里有一大批把 `figure_code` 写成**人物名**（'DaVinci' / 'Bach'）或
        **时代名**（'战国' / 'Modern'），于是有的键只有「代码写法」的模式看得到、
        有的键只有「人名写法」的模式看得到；
      * 13 个文件的 `figure_code` 都写 'Modern'、6 个都写 '战国' → 不同人物互相覆盖，
        胜者由遍历顺序决定；
      * '约公元前330' 这类写法旧正则解析失败（H-EUC-001）。

本脚本做什么
    1) 用 `tools/credibility_gate.py` 的**同一份**取值逻辑（`load_figure_lifespans()` /
       `figure_key_candidates()`）算出**现在**的生卒年取值面，逐条记录 provenance
       （哪个文件、哪个字段、原始值、解析值）；
    2) 用**旧口径的对照实现**（`legacy_key()`，只为对照，不参与判定）算出**修复前**的
       取值面，给出 before/after 与「因本次修复而新覆盖」的 figure 清单；
    3) 把「仍然没有日期」的 figure **明确列出**（`still_no_date`，带原因：无文件 /
       文件里没有 birth_year 或 death_year 字段 / 年份不可解析），不许算作「已覆盖」；
    4) 写 `data/audit/lifespan_backfill.json`（机读清单，两仓同字节）。

重入语义
    幂等：任何一次运行都从 `data/figures/*.json` 与 `data/modes_data.json` 现场重算，
    不依赖上一次的产物；`--check` 比对磁盘清单与现场重算结果，漂移即 exit 1。

用法
    python3 tools/backfill_lifespans.py            # 打印对照 + 写清单
    python3 tools/backfill_lifespans.py --check     # 只校验清单是否新鲜（exit 0/1）
    python3 tools/backfill_lifespans.py --json      # 打印清单 JSON（人读用）
退出码：0 = 正常 / 清单新鲜；1 = --check 发现漂移
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GATE_PATH = Path(__file__).resolve().parent / "credibility_gate.py"
MANIFEST_PATH = REPO_ROOT / "data" / "audit" / "lifespan_backfill.json"
SCHEMA = "protreptic.lifespan_backfill/v1"


def load_gate():
    spec = importlib.util.spec_from_file_location("gate_for_backfill", GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def legacy_key(doc: dict):
    """旧口径（对照用，**不参与判定**）：figure_code -> code -> id 的第一个非空值。"""
    for field in ("figure_code", "code", "id"):
        value = doc.get(field)
        if value:
            return str(value)
    return None


def legacy_surface(gate) -> dict:
    """旧口径能取到的生卒年（逐 figure），用于 before/after 对照。"""
    out = {}
    figures_dir = REPO_ROOT / "data" / "figures"
    for path in sorted(figures_dir.glob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(doc, dict):
            continue
        key = legacy_key(doc)
        if not key:
            continue
        birth = gate.parse_year_value(doc.get("birth_year"))
        death = gate.parse_year_value(doc.get("death_year"))
        if birth is None or death is None or birth > death:
            continue
        out[key] = {"birth_year": birth, "death_year": death,
                    "provenance": "data/figures/%s.json:birth_year/death_year" % path.stem}
    return out


def build_manifest(gate) -> dict:
    data_path = REPO_ROOT / "data" / "modes_data.json"
    modes = gate.get_all_modes(json.loads(data_path.read_text(encoding="utf-8")))
    life = gate.load_figure_lifespans(REPO_ROOT)
    diag = {k: (list(v) if isinstance(v, list) else v) for k, v in gate.LAST_LIFESPAN_LOAD.items()}
    legacy = legacy_surface(gate)

    mode_counts: dict = {}
    for mode in modes:
        code = str(mode.get("figure_code") or "")
        mode_counts[code] = mode_counts.get(code, 0) + 1

    figures_dir = REPO_ROOT / "data" / "figures"
    has_file = {p.stem: p for p in figures_dir.glob("*.json")}
    skipped_by_file = {}
    for item in diag.get("skipped", []):
        skipped_by_file[Path(item["file"]).stem] = item

    covered = sorted(c for c in mode_counts if c in life)
    still_no_date = []
    for code in sorted(c for c in mode_counts if c not in life):
        base = code[:-6] if code.endswith("_modes") else code
        path = has_file.get(code) or has_file.get(base)
        if path is None:
            reason, provenance = "no-figure-file", None
        else:
            item = skipped_by_file.get(path.stem)
            reason = item["reason"] if item else "file-has-years-but-no-key-matched-this-code"
            provenance = "data/figures/%s" % path.name
        still_no_date.append({"figure_code": code, "modes": mode_counts[code],
                              "reason": reason, "file": provenance})

    newly = sorted(c for c in covered if c not in legacy)
    return {
        "schema": SCHEMA,
        "generated_by": "tools/backfill_lifespans.py",
        "source": "data/figures/*.json × data/modes_data.json（现场重算，幂等）",
        "counting_rule": ("覆盖 = 该 figure_code 能在 load_figure_lifespans() 的取值面里"
                          "取到完整 birth_year+death_year；取不到的一律进 still_no_date，"
                          "不得算作已覆盖"),
        "figure_files_scanned": diag.get("files", 0),
        "keys_available": len(life),
        "keys_legacy": len(legacy),
        "key_collisions_dropped": diag.get("collisions", []),
        "files_without_usable_years": diag.get("skipped", []),
        "modes_total": len(modes),
        "mode_figures_total": len(mode_counts),
        "mode_figures_covered": len(covered),
        "modes_covered": sum(mode_counts[c] for c in covered),
        "mode_figures_covered_legacy": len([c for c in mode_counts if c in legacy]),
        "modes_covered_legacy": sum(mode_counts[c] for c in mode_counts if c in legacy),
        "newly_covered_figures": [
            {"figure_code": c, "modes": mode_counts[c],
             "birth_year": life[c]["birth_year"], "death_year": life[c]["death_year"],
             "provenance": life[c]["provenance"]} for c in newly
        ],
        "lifespans": {c: {"birth_year": life[c]["birth_year"], "death_year": life[c]["death_year"],
                          "provenance": life[c]["provenance"]} for c in covered},
        "still_no_date": still_no_date,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="生卒年补数清单（Phase42-Z4）")
    parser.add_argument("--check", action="store_true", help="只校验磁盘清单是否新鲜")
    parser.add_argument("--json", action="store_true", help="打印清单 JSON")
    args = parser.parse_args()

    gate = load_gate()
    manifest = build_manifest(gate)

    if args.check:
        if not MANIFEST_PATH.is_file():
            print("[FAIL] 清单不存在: %s" % MANIFEST_PATH)
            return 1
        on_disk = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        if on_disk != manifest:
            print("[FAIL] 清单过期：盘上 %d 个取值键 / 现场重算 %d 个 —— 请跑 "
                  "python3 tools/backfill_lifespans.py 刷新"
                  % (on_disk.get("keys_available", -1), manifest["keys_available"]))
            return 1
        print("[OK] 清单新鲜：%d 个取值键、%d 个 figure 有日期、%d 个无日期，逐字节一致"
              % (manifest["keys_available"], manifest["mode_figures_covered"],
                 len(manifest["still_no_date"])))
        return 0

    if args.json:
        print(json.dumps(manifest, ensure_ascii=False, indent=1))
        return 0

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
                             encoding="utf-8")
    print("=== 生卒年补数（Phase42-Z4）===")
    print("扫描: data/figures/*.json %d 个文件" % manifest["figure_files_scanned"])
    print("取值面: 旧口径 %d 个键 → 新口径 %d 个键（+%d）"
          % (manifest["keys_legacy"], manifest["keys_available"],
             manifest["keys_available"] - manifest["keys_legacy"]))
    print("键冲突丢弃: %d 个键" % len(manifest["key_collisions_dropped"]))
    for c in manifest["key_collisions_dropped"]:
        print("  丢 %-12s %s%s  vs  %s%s"
              % (c["key"], c["kept"], c["kept_years"], c["dropped"], c["dropped_years"]))
    print("有文件的年份不可用: %d 个文件（%s）"
          % (len(manifest["files_without_usable_years"]),
             ", ".join(sorted({i["reason"] for i in manifest["files_without_usable_years"]}))))
    print("模式侧覆盖: figure %d → %d 个 / 模式 %d → %d 条（全库 %d 条）"
          % (manifest["mode_figures_covered_legacy"], manifest["mode_figures_covered"],
             manifest["modes_covered_legacy"], manifest["modes_covered"], manifest["modes_total"]))
    print("本次修复新覆盖 figure: %d 个（逐条 provenance）" % len(manifest["newly_covered_figures"]))
    for item in manifest["newly_covered_figures"]:
        print("  %-14s n=%2d  %s-%s  <- %s"
              % (item["figure_code"], item["modes"], item["birth_year"], item["death_year"],
                 item["provenance"]))
    print("仍然无日期 figure: %d 个（模式 %d 条）—— 明确列出，不算已覆盖"
          % (len(manifest["still_no_date"]), sum(i["modes"] for i in manifest["still_no_date"])))
    by_reason: dict = {}
    for item in manifest["still_no_date"]:
        by_reason[item["reason"]] = by_reason.get(item["reason"], 0) + 1
    for reason, n in sorted(by_reason.items(), key=lambda kv: -kv[1]):
        print("  %-46s %3d 个 figure" % (reason, n))
    print("清单已写: data/audit/lifespan_backfill.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
