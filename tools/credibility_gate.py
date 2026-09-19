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


def check_d4_quote_mismatch(mode: dict) -> list[str]:
    """D4: 引文不符 - key_quote_zh not found in source (warn only).

    This is a placeholder - full implementation requires fetching source text.
    """
    # For now, just check if key_quote_zh exists but source_chapter is empty/unverifiable
    quote = mode.get("key_quote_zh", "")
    source = mode.get("source_chapter", "")
    if quote and (not source or (isinstance(source, str) and not source.strip())):
        return [f"D4 引文不符(警告): 有引文但无出处 -> quote={quote[:50]}..."]
    return []


def check_d5_timeline_conflict(mode: dict) -> list[str]:
    """D5: 时间线矛盾 - quote date > figure death (warn only).

    Placeholder - requires figure birth/death dates and quote date extraction.
    """
    # Placeholder - would need figure metadata and quote date parsing
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


def run_gate(
    data: dict,
    negative_test: bool = False,
    injected_d3_mode: dict | None = None,
    apply_d3_exemption: bool = True,
    quarantine: set[str] | None = None,
) -> tuple[list[str], list[str], list[str]]:
    """Run credibility gate.

    Returns (hard_failures, warnings, d3_exempted_mode_codes)——
    第三个返回值是「按豁免条款跳过 D3 扫描」的 mode_code 列表（已排序），
    用于如实报告豁免面，避免「静默跳过」被当成「零缺陷」。
    """
    quarantine = load_quarantine() if quarantine is None else quarantine
    all_modes = get_all_modes(data)
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
        src_text = mode.get("source_chapter", "")
        has_source = bool(src_text.strip()) if isinstance(src_text, str) else bool(src_text)
        if apply_d3_exemption and quarantine and has_source and is_d3_exempt(mode, quarantine):
            d3_exempted.append(str(mode_code))

        # Hard gates (D1, D2, D3, D6)
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d1_fake_figure(mode, quarantine)])
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d2_fake_source(mode)])
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d3_pollution(mode, quarantine, apply_d3_exemption)])
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d6_dangling_ref(mode, all_mode_codes)])

        # Warnings (D4, D5)
        warnings.extend([f"[{mode_code}] {e}" for e in check_d4_quote_mismatch(mode)])
        warnings.extend([f"[{mode_code}] {e}" for e in check_d5_timeline_conflict(mode)])

    return hard_failures, warnings, sorted(set(d3_exempted))


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

    # Normal gate run
    failures, warnings, exempted = run_gate(data, apply_d3_exemption=apply_d3_exemption,
                                            quarantine=quarantine)

    # Phase37-X3 两档模式 / 基线冻结：存量只报告，新增即拦
    if args.write_baseline or args.legacy_report or args.hard_fail:
        return run_baseline_mode(args, failures, warnings, exempted,
                                 baseline_path=baseline_path, data_path=data_path)

    d3_failures = [f for f in failures if "D3 出处污染" in f]

    print("=== CREDIBILITY GATE ===")
    print(f"resolved data path: {data_path}")
    print(f"Total modes checked: {len(get_all_modes(data))}")
    print(f"Hard failures (D1/D2/D3/D6): {len(failures)}")
    print(f"  of which D3 出处污染: {len(d3_failures)}")
    print(f"Warnings (D4/D5): {len(warnings)}")
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
