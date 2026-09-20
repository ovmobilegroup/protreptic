#!/usr/bin/env python3
"""build_audit_findings.py - generate data/audit/findings.json (re-runnable, counts from live library).

Defect taxonomy (aligned with docs/planning/credibility_framework.md section 1):
  D1 pseudo figure    figure_code listed in tools/_quarantine.py QUARANTINE
  D2 fabricated source source_chapter contains a fabricated book title (《苏咸子》 family)
  D3 source pollution  source_chapter matches credibility_gate.D3_PATTERNS (STRICT scan, no exemption)
  D4 quote w/o source  key_quote present but source_chapter empty (structural)
  D4 quote mismatch    key_quote_zh 的字面片段在所标出处的**缓存原文**里找不到
                       (Phase40-Z2; 只在缓存覆盖整部作品时可核 -> data/audit/source_texts.json)
  D5 timeline conflict 本人叙述字段里的年份落在人物生卒年之外
                       (Phase40-Z2; 生卒年取 data/figures/*.json，含字符串/公元前纪年)
  D6 orphan reference  bare mode_code in related_modes/cross_references missing from the library
  D7 duplicate/近重   duplicated mode_code, or duplicated definition_zh inside one figure

Conventions:
  * every finding carries "anchor" (a verbatim locatable string) checked by tools/verify_findings.py:
      D1 -> figure_code   D2/D3 -> mode.source_chapter   D4 -> mode.key_quote_zh   D6 -> dangling ref
      D4_quote_mismatch -> key_quote_zh 片段   D5_timeline_conflict -> 本人叙述字段里的年份上下文
  * summary counts == number of findings entries per defect (cross-checked by verify_findings.py)
  * annotated refs ('M-XXX-001(comment)' whose prefix code exists) are NOT D6; counted in audit_meta.notes

Usage:
  python3 tools/build_audit_findings.py            # dry run, print stats
  python3 tools/build_audit_findings.py --write    # write data/audit/findings.json
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = REPO_ROOT / "data" / "modes_data.json"
DEFAULT_OUT_PATH = REPO_ROOT / "data" / "audit" / "findings.json"

BARE_CODE_RE = re.compile(r"^M-[A-Z0-9]+-\d+$")
FAKE_SOURCE_RE = re.compile(r"《苏咸子")


def _load_gate():
    path = REPO_ROOT / "tools" / "credibility_gate.py"
    spec = importlib.util.spec_from_file_location("credibility_gate_local", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _as_text(value) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return json.dumps(value, ensure_ascii=False)


def _safe_anchor(text, maxlen: int = 40) -> str:
    """取一段「逐字可定位」的锚点：不含引号 / 反斜杠 / 换行的连续片段。

    verify_findings 的 C 类要求锚点在**库原文里逐字存在**、且出现在 evidence 里，
    所以锚点必须避开会被 JSON 转义的字符（" \\ 换行），只取干净片段。
    """
    if not isinstance(text, str):
        return ""
    cleaned = text.replace('"', " ").replace("\\", " ").replace("\n", " ").replace("\r", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:maxlen].strip()


def scan_d4_d5(modes) -> dict:
    """Phase40-Z2：D4（引文不符）/ D5（时间线矛盾）真检查的审计清单产出。

    规则不在本文件里另抄一份 —— 全部调 tools/credibility_gate.py 的实现：
        D4: d4_scan(mode, cache, link_index)  -> mismatch 才进清单
        D5: d5_scan(mode, lifespans)          -> conflicts 才进清单
    「不可核 / 不可判定」的面逐类计数进 report（audit_meta.d4_d5_report），不静默放过。
    """
    gate = _load_gate()
    lifespans = gate.load_figure_lifespans(REPO_ROOT)
    cache = gate.make_cache(REPO_ROOT)
    link_index = gate.load_link_index()

    findings = []
    d4_counts = Counter()
    d4_reasons = Counter()
    d5_counts = Counter()
    d5_reasons = Counter()
    d5_undetermined = Counter()
    d4_mismatches = []
    d5_conflicts = []

    ordered = sorted((m for m in modes if isinstance(m, dict)),
                     key=lambda m: str(m.get("mode_code")))
    for m in ordered:
        code = str(m.get("mode_code") or "")
        d4 = gate.d4_scan(m, cache, link_index)
        d4_counts[d4["status"]] += 1
        d4_reasons[d4["reason"].split(":")[0]] += 1
        if d4["status"] == "mismatch":
            quote = _as_text(m.get("key_quote_zh"))
            anchor = _safe_anchor(quote)
            evidence = ("key_quote_zh 的字面片段在所标出处的缓存原文里找不到"
                        "（出处 key=%s；缓存见 data/audit/source_texts.json；"
                        "最长未命中片段='%s'）" % (d4.get("key"), anchor))
            findings.append({
                "mode_code": m.get("mode_code"),
                "figure_code": m.get("figure_code"),
                "defect": "D4_quote_mismatch",
                "evidence": evidence,
                "anchor": anchor,
                "source_key": d4.get("key"),
                "suggested_action": "复核：确认引文是改写/意译还是伪造；不改写则补正出处",
            })
            d4_mismatches.append({"mode_code": code, "key": d4.get("key"),
                                  "anchor": anchor, "detail": str(d4.get("detail"))[:60]})

        d5 = gate.d5_scan(m, lifespans)
        d5_counts[d5["status"]] += 1
        if d5["status"] != "undetermined":
            d5_reasons[d5["reason"]] += 1
        for item in d5["undetermined"]:
            d5_undetermined[item["reason"].split(":")[0]] += 1
        for item in d5["conflicts"]:
            anchor = _safe_anchor(item["context"])
            life = lifespans.get(str(m.get("figure_code") or ""), {})
            evidence = ("%s=%d 落在该人物生卒年之外（%s-%s，来源 %s）：上下文 '%s'"
                        % (item["field"], item["year"], life.get("birth_year"),
                           life.get("death_year"), life.get("provenance"), anchor))
            findings.append({
                "mode_code": m.get("mode_code"),
                "figure_code": m.get("figure_code"),
                "defect": "D5_timeline_conflict",
                "evidence": evidence,
                "anchor": anchor,
                "year": item["year"],
                "suggested_action": "复核：该年份是否真指本人行事（改年份或改归属）",
            })
            d5_conflicts.append({"mode_code": code, "field": item["field"],
                                 "year": item["year"], "anchor": anchor})

    report = {
        "generated_by": "tools/build_audit_findings.py::scan_d4_d5 (Phase40-Z2)",
        "rules_source": "tools/credibility_gate.py::d4_scan / d5_scan（规则唯一实现）",
        "d4": {
            "cache_index": "data/audit/source_texts.json",
            "cache_present": bool(getattr(cache, "present", False)),
            "usable_keys": len(getattr(cache, "usable_keys", lambda: [])()),
            "statuses": dict(d4_counts),
            "unchecked_reasons": dict(d4_reasons),
            "mismatches": d4_mismatches,
            "note": ("只在「出处有书名号引文 + 引文解析到原文类链接 + 缓存覆盖整部作品"
                     "(single-page/complete)」时判 matched/mismatch；"
                     "coverage=partial 的缓存**不可核**（在部分文本里找不到引文不能证明引文不符）"),
        },
        "d5": {
            "figures_with_lifespan": len(lifespans),
            "statuses": dict(d5_counts),
            "reasons": dict(d5_reasons),
            "undetermined_reasons": dict(d5_undetermined),
            "conflicts": d5_conflicts,
            "note": ("只把「本人叙述字段(definition_zh/process_zh/representative_cases_zh) + 年份与人物名同现"
                     "+ 生在生涯带内 + 无文献/余波/背景标记」的年份判为矛盾；"
                     "其余逐类计数为不可判定"),
        },
        "findings_emitted": {"D4_quote_mismatch": sum(1 for f in findings if f["defect"] == "D4_quote_mismatch"),
                             "D5_timeline_conflict": sum(1 for f in findings if f["defect"] == "D5_timeline_conflict")},
    }
    return {"findings": findings, "report": report}


def scan_library(data_path: Path | None = None) -> dict:
    path = Path(data_path) if data_path else DEFAULT_DATA_PATH
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    gate = _load_gate()

    modes = gate.get_all_modes(data)
    quarantine = sorted(gate.load_quarantine())
    qset = set(quarantine)
    top_modes = data.get("modes", [])
    all_codes = {m.get("mode_code") for m in modes if isinstance(m, dict) and m.get("mode_code")}

    findings = []

    # D1
    d1_modes = sorted(
        (m for m in modes if isinstance(m, dict) and m.get("figure_code") in qset),
        key=lambda m: str(m.get("mode_code")),
    )
    for m in d1_modes:
        fc = str(m.get("figure_code"))
        findings.append({
            "mode_code": m.get("mode_code"),
            "figure_code": fc,
            "defect": "D1_pseudo_figure",
            "evidence": (
                "figure_code '%s' is listed in QUARANTINE (tools/_quarantine.py): "
                "pipeline-stage placeholder, not a real historical figure; "
                "its records are still present in the source library and are filtered at export time" % fc
            ),
            "anchor": fc,
            "suggested_action": "isolate + archive",
        })

    # D2
    d2_modes = sorted(
        (m for m in modes if isinstance(m, dict) and FAKE_SOURCE_RE.search(_as_text(m.get("source_chapter")))),
        key=lambda m: str(m.get("mode_code")),
    )
    for m in d2_modes:
        src = _as_text(m.get("source_chapter"))
        findings.append({
            "mode_code": m.get("mode_code"),
            "figure_code": m.get("figure_code"),
            "defect": "D2_fabricated_source",
            "evidence": "source_chapter='%s' -- 《苏咸子》 is a fabricated book title absent from any authoritative catalogue" % src,
            "anchor": src,
            "source_chapter": src,
            "suggested_action": "isolate + manual review",
        })

    # D3 (strict, exemption deliberately NOT applied: the audit must show the full pollution surface)
    for m in modes:
        if not isinstance(m, dict):
            continue
        src = _as_text(m.get("source_chapter"))
        if not src:
            continue
        hit = None
        for pattern in gate.D3_PATTERNS:
            match = re.search(pattern, src, re.IGNORECASE)
            if match:
                hit = (pattern, match.group(0))
                break
        if hit:
            pattern, matched = hit
            findings.append({
                "mode_code": m.get("mode_code"),
                "figure_code": m.get("figure_code"),
                "defect": "D3_source_contamination",
                "evidence": "source_chapter matches D3 engineering-trace regex '%s' (matched '%s') -> %s" % (pattern, matched, src[:160]),
                "anchor": matched,
                "source_chapter": src,
                "suggested_action": "rewrite or isolate",
            })

    # D4
    d4_modes = sorted(
        (
            m for m in modes
            if isinstance(m, dict)
            and _as_text(m.get("key_quote_zh")).strip()
            and not _as_text(m.get("source_chapter")).strip()
        ),
        key=lambda m: str(m.get("mode_code")),
    )
    for m in d4_modes:
        quote = _as_text(m.get("key_quote_zh"))
        findings.append({
            "mode_code": m.get("mode_code"),
            "figure_code": m.get("figure_code"),
            "defect": "D4_quote_without_source",
            "evidence": "key_quote_zh present but source_chapter empty -> quote='%s'" % quote[:80],
            "anchor": quote,
            "suggested_action": "add source or re-verify quote",
        })

    # D4b / D5 —— Phase40-Z2：真检查（引文子串核验 / 生卒年 × 文本年份）
    d45 = scan_d4_d5(modes)
    findings.extend(d45["findings"])

    # D6 (bare code only)
    d6_rows = []
    for m in modes:
        if not isinstance(m, dict):
            continue
        for field in ("cross_references", "related_modes"):
            refs = m.get(field) or []
            if not isinstance(refs, list):
                continue
            for ref in refs:
                if ref and isinstance(ref, str) and ref not in all_codes and BARE_CODE_RE.match(ref):
                    d6_rows.append((str(m.get("mode_code")), m.get("figure_code"), field, ref))
    d6_rows.sort()
    for mode_code, figure_code, field, ref in d6_rows:
        findings.append({
            "mode_code": mode_code,
            "figure_code": figure_code,
            "defect": "D6_orphan_reference",
            "evidence": "%s points to a mode_code that does not exist in the library: '%s'" % (field, ref),
            "anchor": ref,
            "dangling_ref": ref,
            "suggested_action": "auto-fix: repoint to a real code or drop the reference",
        })

    # D7
    d7_entries = []
    code_counter = Counter(m.get("mode_code") for m in top_modes if isinstance(m, dict) and m.get("mode_code"))
    for code, n in sorted(code_counter.items()):
        if n > 1:
            d7_entries.append((code, None, "mode_code duplicated %d times inside top-level modes" % n))
    by_figure = {}
    for m in modes:
        if isinstance(m, dict):
            by_figure.setdefault(str(m.get("figure_code")), []).append(_as_text(m.get("definition_zh")).strip())
    for figure_code, defs in sorted(by_figure.items()):
        dup = [d for d, n in Counter(x for x in defs if x).items() if n > 1]
        for d in dup:
            d7_entries.append((None, figure_code, "definition_zh duplicated inside one figure -> %s" % d[:60]))
    for code, figure_code, why in d7_entries:
        findings.append({
            "mode_code": code,
            "figure_code": figure_code,
            "defect": "D7_duplicate_definition",
            "evidence": why,
            "anchor": (code or figure_code or ""),
            "suggested_action": "merge/annotate",
        })

    by_defect = Counter(f["defect"] for f in findings)
    summary = {
        "D1_pseudo_figure": by_defect.get("D1_pseudo_figure", 0),
        "D2_fabricated_source": by_defect.get("D2_fabricated_source", 0),
        "D3_source_contamination": by_defect.get("D3_source_contamination", 0),
        "D4_empty_quote": by_defect.get("D4_quote_without_source", 0),
        "D4_quote_mismatch": by_defect.get("D4_quote_mismatch", 0),
        "D5_timeline_conflict": by_defect.get("D5_timeline_conflict", 0),
        "D6_orphan_reference": by_defect.get("D6_orphan_reference", 0),
        "D7_duplicate_definition": by_defect.get("D7_duplicate_definition", 0),
        "total": len(findings),
    }

    by_scope = {}
    for _defect in ("D1_pseudo_figure", "D2_fabricated_source", "D3_source_contamination",
                    "D4_quote_without_source", "D4_quote_mismatch", "D5_timeline_conflict",
                    "D6_orphan_reference"):
        _rows = [f for f in findings if f.get("defect") == _defect]
        _q = sum(1 for f in _rows if str(f.get("figure_code")) in qset)
        by_scope[_defect] = {"total": len(_rows), "quarantined_figure": _q, "public_figure": len(_rows) - _q}

    annotated = 0
    for m in modes:
        if not isinstance(m, dict):
            continue
        for field in ("cross_references", "related_modes"):
            refs = m.get(field) or []
            if not isinstance(refs, list):
                continue
            for ref in refs:
                if not isinstance(ref, str) or not ref or ref in all_codes:
                    continue
                if BARE_CODE_RE.match(ref):
                    continue
                prefix = ref.split("(")[0].split("（")[0].strip()
                if prefix in all_codes:
                    annotated += 1

    embedded_dupes = len(modes) - len(top_modes)
    empty_code = len([m for m in top_modes if isinstance(m, dict) and not m.get("mode_code")])

    audit_meta = {
        "scan_date": date.today().isoformat(),
        "modes_file": "data/modes_data.json",
        "modes_file_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "total_modes_count": len(modes),
        "top_level_modes_entries": len(top_modes),
        "distinct_mode_codes": len(all_codes),
        "modes_empty_mode_code": empty_code,
        "embedded_figure_mode_entries": embedded_dupes,
        "total_figures": len(set(m.get("figure_code") for m in modes if isinstance(m, dict) and m.get("figure_code"))),
        "quarantined_figures": quarantine,
        "by_scope": by_scope,
        "methodology": (
            "full regex/grep scan of data/modes_data.json; gate semantics shared with "
            "tools/credibility_gate.py; D1 list from tools/_quarantine.py; D3 is a strict scan (no exemption)"
        ),
        "d4_d5_report": d45["report"],
        "notes": [
            "annotated references ('M-XXX-001(comment)' with an existing prefix code): %d entries, "
            "not counted as D6 per library convention" % annotated,
            "get_all_modes total %d = top-level modes %d + embedded figure-node duplicates %d; "
            "distinct mode_code %d (plus %d entries with an empty mode_code, dropped at export)"
            % (len(modes), len(top_modes), embedded_dupes, len(all_codes), empty_code),
            "D4/D5 已由 Phase40-Z2 真实现（不再是占位）：D4 对『缓存覆盖整部作品』的出处做"
            " key_quote_zh 归一化子串核验（缓存见 data/audit/source_texts.json）；"
            "D5 用 data/figures/*.json 的生卒年 × 模式文本里的 4 位年份，"
            "不可核/不可判定的部分逐类计数在 audit_meta.d4_d5_report（禁止当成零缺陷）",
            "D1/D2/D3/D4/D6 的 by_scope 见 audit_meta.by_scope: quarantined_figure 指该条 mode 的 figure_code 在隔离名单中",
        ],
    }
    return {"findings": findings, "summary": summary, "audit_meta": audit_meta}


def main() -> int:
    parser = argparse.ArgumentParser(description="build data/audit/findings.json (re-runnable)")
    parser.add_argument("--data-path", default=str(DEFAULT_DATA_PATH))
    parser.add_argument("--out", default=str(DEFAULT_OUT_PATH))
    parser.add_argument("--write", action="store_true", help="actually write the file")
    args = parser.parse_args()

    result = scan_library(Path(args.data_path))
    print("=== findings scan ===")
    print("findings entries: %d" % len(result["findings"]))
    for k, v in result["summary"].items():
        print("  %s: %s" % (k, v))
    print("modes sha256: %s" % result["audit_meta"]["modes_file_sha256"])

    if args.write:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("[OK] wrote %s" % out)
    else:
        print("(dry-run; pass --write to write the file)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
