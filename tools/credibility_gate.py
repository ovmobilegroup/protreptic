#!/usr/bin/env python3
"""Credibility Gate (D1–D6 hard gates + D4/D5 warnings).

Implements the defect taxonomy from credibility_framework.md:
- D1 伪人物      → 硬 FAIL
- D2 伪造出处    → 硬 FAIL
- D3 出处污染    → 硬 FAIL (正则扫描 source_chapter)
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
DEFAULT_DATA_PATH = REPO_ROOT / "data" / "modes_data.json"
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
def load_quarantine() -> set[str]:
    """Load quarantine list from _quarantine.py."""
    try:
        sys.path.insert(0, str(REPO_ROOT / "tools"))
        from _quarantine import QUARANTINE
        return set(QUARANTINE)
    except Exception:
        return set()


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


def check_d3_pollution(mode: dict) -> list[str]:
    """D3: 出处污染 - source_chapter contains engineering traces."""
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
    injected_d3_mode: dict | None = None
) -> tuple[list[str], list[str]]:
    """Run credibility gate. Returns (hard_failures, warnings)."""
    quarantine = load_quarantine()
    all_modes = get_all_modes(data)
    all_mode_codes = {m.get("mode_code", "") for m in all_modes if isinstance(m, dict) and m.get("mode_code")}

    # Add injected mode for negative test
    if negative_test and injected_d3_mode:
        all_modes = [injected_d3_mode] + all_modes

    hard_failures = []
    warnings = []

    for mode in all_modes:
        if not isinstance(mode, dict):
            continue

        mode_code = mode.get("mode_code", "UNKNOWN")

        # Hard gates (D1, D2, D3, D6)
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d1_fake_figure(mode, quarantine)])
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d2_fake_source(mode)])
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d3_pollution(mode)])
        hard_failures.extend([f"[{mode_code}] {e}" for e in check_d6_dangling_ref(mode, all_mode_codes)])

        # Warnings (D4, D5)
        warnings.extend([f"[{mode_code}] {e}" for e in check_d4_quote_mismatch(mode)])
        warnings.extend([f"[{mode_code}] {e}" for e in check_d5_timeline_conflict(mode)])

    return hard_failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Credibility Gate for Protreptic modes")
    parser.add_argument("--negative-test", action="store_true",
                        help="Inject a D3 sample and verify gate catches it (exit 1)")
    parser.add_argument("--data-path", type=str, default=str(DEFAULT_DATA_PATH),
                        help="Path to modes_data.json")
    args = parser.parse_args()

    data = load_modes_data(Path(args.data_path) if args.data_path else None)

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
        failures, warnings = run_gate(data, negative_test=True, injected_d3_mode=injected)

        print("=== NEGATIVE TEST MODE ===")
        print(f"Injected D3 sample: {injected['source_chapter']}")
        print(f"Hard failures: {len(failures)}")
        print(f"Warnings: {len(warnings)}")
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
    failures, warnings = run_gate(data)

    print("=== CREDIBILITY GATE ===")
    print(f"Total modes checked: {len(get_all_modes(data))}")
    print(f"Hard failures (D1/D2/D3/D6): {len(failures)}")
    print(f"Warnings (D4/D5): {len(warnings)}")

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
