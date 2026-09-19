#!/usr/bin/env python3
"""verify_findings.py - self-check for data/audit/findings.json.

Checks (A-E):
  A structure      findings is a non-empty list; each entry has mode_code/figure_code/defect/evidence/anchor
  B code existence every mode_code exists in the source library; every figure_code exists as a figure there
  C locatable      every anchor is verbatim locatable in the library raw text AND, by defect rule, inside
                   the referenced record itself (evidence must contain the anchor too)
  D self-consist.  summary counts == number of findings entries per defect; total == len(findings)
  E library counts recomputed D1/D2/D3/D4/D6/D7 match the findings enumeration
                   (disable with --no-check-counts)

Exit code: 0 = all checks pass, 1 = at least one failure.
Annotations printed as ::error:: lines (GitHub Actions compatible).

Usage:
  python3 tools/verify_findings.py
  python3 tools/verify_findings.py --findings /tmp/copy/findings_bad.json   # negative test
  python3 tools/verify_findings.py --data-path data/modes_data.json --no-check-counts
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FINDINGS = REPO_ROOT / "data" / "audit" / "findings.json"
DEFAULT_DATA_PATH = REPO_ROOT / "data" / "modes_data.json"

REQUIRED_FIELDS = ("mode_code", "figure_code", "defect", "evidence", "anchor")
SUMMARY_KEYS = {
    "D1_pseudo_figure": "D1_pseudo_figure",
    "D2_fabricated_source": "D2_fabricated_source",
    "D3_source_contamination": "D3_source_contamination",
    "D4_empty_quote": "D4_quote_without_source",
    "D6_orphan_reference": "D6_orphan_reference",
    "D7_duplicate_definition": "D7_duplicate_definition",
}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _as_text(value) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return json.dumps(value, ensure_ascii=False)


def verify(findings_path: Path, data_path: Path, check_counts: bool = True):
    errors = []
    warnings = []

    if not findings_path.exists():
        return (["findings file not found: %s" % findings_path], [], {})
    try:
        payload = json.loads(findings_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return (["findings file is not valid JSON: %s" % exc], [], {})

    raw = data_path.read_text(encoding="utf-8")
    library = json.loads(raw)
    gate = _load_module("credibility_gate_verify", REPO_ROOT / "tools" / "credibility_gate.py")
    modes = gate.get_all_modes(library)
    mode_by_code = {}
    dup_codes = set()
    for m in modes:
        if not isinstance(m, dict) or not m.get("mode_code"):
            continue
        code = str(m.get("mode_code"))
        if code in mode_by_code:
            dup_codes.add(code)
        mode_by_code[code] = m
    figures = {m.get("figure_code") for m in modes if isinstance(m, dict) and m.get("figure_code")}
    all_codes = set(mode_by_code)

    findings = payload.get("findings")
    summary = payload.get("summary", {})
    audit_meta = payload.get("audit_meta", {})

    # A
    if not isinstance(findings, list) or not findings:
        errors.append("A: findings must be a non-empty list")
        return errors, warnings, {}
    for i, f in enumerate(findings):
        if not isinstance(f, dict):
            errors.append("A: findings[%d] is not an object" % i)
            continue
        for field in REQUIRED_FIELDS:
            if field not in f:
                errors.append("A: findings[%d] (%s) missing field '%s'" % (i, f.get("mode_code") or f.get("figure_code") or "?", field))

    # B / C
    for f in findings:
        if not isinstance(f, dict):
            continue
        code = f.get("mode_code")
        label = str(code) if code else "figure:%s" % f.get("figure_code")
        defect = f.get("defect")
        anchor = _as_text(f.get("anchor"))
        evidence = _as_text(f.get("evidence"))

        mode = None
        if code:
            mode = mode_by_code.get(str(code))
            if mode is None:
                errors.append("B: [%s] mode_code '%s' does not exist in the source library (%s)" % (label, code, data_path))
        fc = f.get("figure_code")
        if fc and str(fc) not in figures:
            errors.append("B: [%s] figure_code '%s' does not exist in the source library" % (label, fc))

        if not anchor:
            errors.append("C: [%s] empty anchor" % label)
            continue
        if anchor not in raw:
            errors.append("C: [%s] anchor not found verbatim in %s: %r" % (label, data_path.name, anchor[:60]))
        if anchor not in evidence:
            errors.append("C: [%s] anchor is not quoted inside evidence: %r" % (label, anchor[:60]))

        if mode is not None:
            if defect == "D1_pseudo_figure":
                if str(mode.get("figure_code")) != anchor:
                    errors.append("C: [%s] D1 anchor must equal the record figure_code (%r)" % (label, mode.get("figure_code")))
            elif defect in ("D2_fabricated_source", "D3_source_contamination"):
                src = _as_text(mode.get("source_chapter"))
                if anchor not in src:
                    errors.append("C: [%s] %s anchor %r not inside record source_chapter" % (label, defect, anchor[:60]))
            elif defect == "D4_quote_without_source":
                quote = _as_text(mode.get("key_quote_zh"))
                if anchor != quote:
                    errors.append("C: [%s] D4 anchor must equal the record key_quote_zh" % label)
                if _as_text(mode.get("source_chapter")).strip():
                    errors.append("C: [%s] D4 record has a non-empty source_chapter" % label)
            elif defect == "D6_orphan_reference":
                refs = []
                for field in ("cross_references", "related_modes"):
                    value = mode.get(field) or []
                    if isinstance(value, list):
                        refs.extend([str(r) for r in value])
                if anchor not in refs:
                    errors.append("C: [%s] D6 anchor %r is not one of the record references" % (label, anchor))
                if anchor in all_codes:
                    errors.append("C: [%s] D6 anchor %r actually exists in the library (not dangling)" % (label, anchor))

    # D
    counting = Counter(f.get("defect") for f in findings if isinstance(f, dict))
    for key, defect in SUMMARY_KEYS.items():
        expected = counting.get(defect, 0)
        actual = summary.get(key)
        if actual != expected:
            errors.append("D: summary.%s = %r but the findings list holds %d entries" % (key, actual, expected))
    if summary.get("total") != len(findings):
        errors.append("D: summary.total = %r but len(findings) = %d" % (summary.get("total"), len(findings)))

    # E
    recomputed = {}
    if check_counts:
        builder = _load_module("build_audit_findings_verify", REPO_ROOT / "tools" / "build_audit_findings.py")
        fresh = builder.scan_library(data_path)
        recomputed = fresh["summary"]
        for key in SUMMARY_KEYS:
            old = summary.get(key)
            new = recomputed.get(key)
            if old != new:
                errors.append("E: summary.%s = %r but a fresh scan of %s yields %r (counts are stale)" % (key, old, data_path.name, new))
        if summary.get("total") != recomputed.get("total"):
            errors.append("E: summary.total = %r but a fresh scan yields %r" % (summary.get("total"), recomputed.get("total")))
        if audit_meta.get("modes_file_sha256") != fresh.get("audit_meta", {}).get("modes_file_sha256"):
            warnings.append("E: audit_meta.modes_file_sha256 differs from the current library hash; refresh with build_audit_findings.py --write")

    if dup_codes:
        warnings.append("E: these mode codes are harvested twice by get_all_modes (present both in the top-level modes array and inside a figure node): %s" % sorted(dup_codes)[:10])

    return errors, warnings, {"entries": len(findings), "summary": summary, "recomputed": recomputed}


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify data/audit/findings.json against the source library")
    parser.add_argument("--findings", default=str(DEFAULT_FINDINGS))
    parser.add_argument("--data-path", default=str(DEFAULT_DATA_PATH))
    parser.add_argument("--no-check-counts", action="store_true", help="skip check E")
    args = parser.parse_args()

    errors, warnings, info = verify(Path(args.findings), Path(args.data_path), check_counts=not args.no_check_counts)

    print("=== VERIFY FINDINGS ===")
    print("findings file: %s" % args.findings)
    print("source library: %s" % args.data_path)
    print("entries: %s" % info.get("entries"))
    print("hard failures: %d" % len(errors))
    print("warnings: %d" % len(warnings))
    for e in errors:
        print("  ::error::%s" % e)
    for w in warnings:
        print("  ::warning::%s" % w)
    if errors:
        print("[FAIL] verify_findings: %d problem(s)" % len(errors))
        return 1
    print("[OK] verify_findings: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
