#!/usr/bin/env python3
"""verify_findings.py - self-check for data/audit/findings.json.

Checks (A-D hard, E warning):
  A structure      findings is a non-empty list; each entry has mode_code/figure_code/defect/evidence/anchor
  B code existence every mode_code exists in the source library; every figure_code exists as a figure there
  C locatable      every anchor is verbatim locatable in the library raw text AND, by defect rule, inside
                   the referenced record itself (evidence must contain the anchor too)
  D self-consist.  summary counts == number of findings entries per defect; total == len(findings)
  （Phase40-Z2 起 summary 还含 D4_quote_mismatch / D5_timeline_conflict 两个真检查键；
    D5 anchor 必须落在本人叙述字段且含 4 位年份，D4 anchor 必须落在 key_quote_zh 里）
  E library counts a FRESH scan of the live library yields the same summary counts
                   -> **warning, never blocking** (see "口径" below); disable with --no-check-counts

口径（Phase37-X5，与 tools/credibility_gate.py 的两档同构）
  * 默认（无档位参数）        : 严格口径（A-D 任何硬失败 exit 1；E 只警告）
  * `--legacy-report`        : 存量与新增都列出，**一律 exit 0**（清单档）
  * `--hard-fail`            : 基线内（data/audit/findings_baseline.json）只报告，
                              **基线外的任何硬失败 exit 1**；基线缺失 exit 2（fail-closed）
  * `--write-baseline`       : 用当前硬失败重新冻结基线

为什么 E 类「计数过期」只算警告（Phase37-X5 决策，理由写进 credibility_framework.md §8）
  E 把 findings.json 的 summary 与**现算**库对照，而 data/modes_data.json 每次数据更新 sha256 都会变，
  于是「每次数据改动都红」并强迫每次无关数据提交都额外刷新 findings。E 的真身是**清单新鲜度**，
  不是坏数据：坏数据由 credibility_gate --hard-fail 拦。故 E 降级为 ::warning::，并在输出里给出
  刷新命令 `python3 tools/build_audit_findings.py --write`。

指纹（fingerprint）口径 —— 为什么不是「整条消息取哈希」
  与 gate 同一理由：整条消息取哈希会把「给存量 findings 改一句说明文字」误判成新增。
  本脚本的指纹规则：
      A 结构       key = 归一化后的消息（下标 + 字段名）
      B 不存在     key = mode_code=值 或 figure_code=值（值本身 = 一条新的失效引用）
      C 锚点       key = 归一化后的消息（**去掉引号内的值** = 改锚点文字不产生假新增）
      D 自洽       key = summary.字段名
  取不到已知格式的失败退化为「归一化整条消息」（保守：不进基线就会被拦）。

Exit code: 0 = pass (or nothing outside the baseline), 1 = hard failure, 2 = fail-closed
           (baseline missing in a two-tier mode).
Annotations printed as ::error:: / ::warning:: / ::notice:: lines (GitHub Actions compatible).

Usage:
  python3 tools/verify_findings.py                                    # strict self-check
  python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json   # CI 口径
  python3 tools/verify_findings.py --legacy-report                    # 只报告
  python3 tools/verify_findings.py --write-baseline                    # 重新冻结基线
  python3 tools/verify_findings.py --findings /tmp/copy/findings_bad.json   # negative test
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FINDINGS = REPO_ROOT / "data" / "audit" / "findings.json"
DEFAULT_DATA_PATH = REPO_ROOT / "data" / "modes_data.json"
DEFAULT_BASELINE_NAME = Path("data") / "audit" / "findings_baseline.json"

REQUIRED_FIELDS = ("mode_code", "figure_code", "defect", "evidence", "anchor")
SUMMARY_KEYS = {
    "D1_pseudo_figure": "D1_pseudo_figure",
    "D2_fabricated_source": "D2_fabricated_source",
    "D3_source_contamination": "D3_source_contamination",
    "D4_empty_quote": "D4_quote_without_source",
    "D4_quote_mismatch": "D4_quote_mismatch",
    "D5_timeline_conflict": "D5_timeline_conflict",
    "D6_orphan_reference": "D6_orphan_reference",
    "D7_duplicate_definition": "D7_duplicate_definition",
}

# 计数过期（E 类）的警告前缀：两档打印时按它分节，不参与「存量/新增」判定
STALE_PREFIX = "计数过期(E)"
STALE_HINT = "刷新：python3 tools/build_audit_findings.py --write"

SCHEMA = "protreptic.findings_baseline/v1"
POLICY = ("存量冻结、新增即拦：本文件登记的 findings 硬失败只报告不阻断（exit 0）；"
          "任何未登记的硬失败在 --hard-fail 下 exit 1；计数过期（E 类）只算警告，不进本文件")

# ---- 指纹 ------------------------------------------------------------------
RE_FAIL = re.compile(r"^([A-E]):\s*(.*)$", re.DOTALL)
RE_B = re.compile(r"^\[(.*?)\]\s*(mode_code|figure_code)\s*'(.*?)'")
RE_D = re.compile(r"^summary\.(\S+)\s*=")
RE_QUOTED = re.compile(r"'[^']*'")


def fingerprint(failure: str) -> str:
    """一条硬失败 -> 稳定指纹（改存量条目的说明文字不产生假新增）。"""
    m = RE_FAIL.match(failure or "")
    if not m:
        return "UNPARSED|%s" % (failure or "")
    rule, rest = m.group(1), m.group(2)
    if rule == "B":
        b = RE_B.match(rest)
        if b:
            return "B|%s|%s=%s" % (b.group(1), b.group(2), b.group(3))
    if rule == "D":
        d = RE_D.match(rest)
        if d:
            return "D|summary|%s" % d.group(1)
    key = RE_QUOTED.sub("\u00ab\u00bb", rest)
    key = re.sub(r"\s+", " ", key).strip()
    return "%s|%s" % (rule, key[:160])


def rule_of(fid: str) -> str:
    return fid.split("|", 1)[0] if "|" in fid else "??"


def key_of(fid: str) -> str:
    return fid.split("|", 1)[1] if "|" in fid else fid


# ---- 基线 ------------------------------------------------------------------


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_repo_root(data_path: Path) -> Path:
    """从数据文件反推仓库根：<root>/data/modes_data.json -> <root>。

    与 credibility_gate.resolve_repo_root 同语义：`--data-path` 指向哪一仓的数据，
    默认基线就取那一仓的 data/audit/findings_baseline.json，避免「用 A 仓基线判 B 仓 findings」。
    """
    p = Path(data_path).resolve()
    if p.parent.name == "data" and (p.parent.parent / "tools").is_dir():
        return p.parent.parent
    return REPO_ROOT


def load_baseline(path: Path):
    if not path.is_file():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _rel(path, root: Path) -> str | None:
    """基线里记录「仓内相对路径」——避免 dev/pub 两仓因绝对路径不同而无法字节一致。"""
    if path is None:
        return None
    p = Path(path)
    if not p.is_absolute():
        return str(p)
    try:
        return str(p.resolve().relative_to(root.resolve()))
    except Exception:  # noqa: BLE001
        return str(p)


def build_baseline(failures, data_path=None, findings_path=None,
                   warnings=(), stale_counts=(), repo_root: Path | None = None) -> dict:
    entries = {}
    for f in failures:
        fid = fingerprint(f)
        if fid in entries:
            continue
        entries[fid] = {
            "id": fid,
            "rule": rule_of(fid),
            "key": key_of(fid),
            "sample": f[:200],
        }
    counts = {"total": len(failures), "distinct_fingerprints": len(entries),
              "A": 0, "B": 0, "C": 0, "D": 0}
    for e in entries.values():
        counts[e["rule"]] = counts.get(e["rule"], 0) + 1
    root = repo_root or REPO_ROOT
    return {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generated_by": "tools/verify_findings.py --write-baseline",
        "policy": POLICY,
        "data_path": _rel(data_path, root),
        "data_sha256": sha256_file(data_path) if data_path and data_path.is_file() else None,
        "findings_path": _rel(findings_path, root),
        "findings_sha256": (sha256_file(findings_path)
                            if findings_path and findings_path.is_file() else None),
        "counts": counts,
        # 非阻断面如实登记（不参与判定，只为「冻结时到底什么状态」留证据）
        "non_blocking_at_freeze": {
            "warnings": len(list(warnings)),
            "stale_counts": len(list(stale_counts)),
            "note": "计数过期(E)与非 E 警告都不阻断；E 的刷新命令见 STALE_HINT",
        },
        "entries": [entries[k] for k in sorted(entries)],
    }


def save_baseline(baseline: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def classify(failures, baseline: dict) -> dict:
    known = {e["id"]: e for e in baseline.get("entries", [])}
    legacy, new = [], []
    seen = set()
    for f in failures:
        fid = fingerprint(f)
        seen.add(fid)
        (legacy if fid in known else new).append((fid, f))
    stale = [known[i] for i in known if i not in seen]
    by_rule = {"A": 0, "B": 0, "C": 0, "D": 0}
    for fid, _ in legacy:
        r = rule_of(fid)
        by_rule[r] = by_rule.get(r, 0) + 1
    return {"legacy": legacy, "new": new, "stale": stale, "legacy_by_rule": by_rule}


def split_warnings(warnings):
    stale = [w for w in warnings if w.startswith(STALE_PREFIX)]
    other = [w for w in warnings if not w.startswith(STALE_PREFIX)]
    return stale, other


def run_mode(mode, *, errors, warnings, baseline_path, findings_path, data_path, limit=1000) -> int:
    """`--legacy-report` / `--hard-fail` 的打印与退出码（与 gate 同构）。

    legacy-report -> 一律 exit 0（只报告不阻断）
    hard-fail     -> 基线外任何一条硬失败 exit 1；正常 exit 0
    基线缺失       -> exit 2（fail-closed：没有基线就谈不上存量冻结，宁可红）
    """
    stale_counts, other_warnings = split_warnings(warnings)
    baseline = load_baseline(baseline_path)
    print("=== VERIFY FINDINGS · 存量/新增两档 ===")
    print("mode: %s" % mode)
    print("resolved findings path: %s (exists=%s)" % (findings_path, findings_path.is_file()))
    print("resolved data path:     %s (exists=%s)" % (data_path, data_path.is_file()))
    print("resolved baseline path: %s (exists=%s)" % (baseline_path, baseline_path.is_file()))
    print("hard failures on this findings file: %d" % len(errors))
    if baseline is None:
        print("[FAIL] baseline file missing: %s" % baseline_path)
        print("       先冻结基线: python3 tools/verify_findings.py --write-baseline "
              "--data-path data/modes_data.json")
        return 2

    b = baseline.get("counts", {})
    print("baseline frozen at %s (total=%s, fingerprints=%s, A=%s B=%s C=%s D=%s)" % (
        baseline.get("generated_at"), b.get("total"), b.get("distinct_fingerprints"),
        b.get("A"), b.get("B"), b.get("C"), b.get("D")))
    print("baseline data_sha256:     %s" % baseline.get("data_sha256"))
    print("current  data_sha256:     %s" % (sha256_file(data_path) if data_path.is_file() else "N/A"))

    res = classify(errors, baseline)
    legacy, new, stale = res["legacy"], res["new"], res["stale"]
    lr = res["legacy_by_rule"]

    print("")
    print("--- 存量（基线内，冻结）: %d 条 [A=%d B=%d C=%d D=%d] ---" % (
        len(legacy), lr.get("A", 0), lr.get("B", 0), lr.get("C", 0), lr.get("D", 0)))
    for fid, f in legacy[:limit]:
        print("  ::notice::LEGACY %s | %s" % (fid, f))
    if len(legacy) > limit:
        print("  ... and %d more legacy findings" % (len(legacy) - limit))

    print("")
    print("--- 新增（基线外，必拦）: %d 条 ---" % len(new))
    if not new:
        print("  (none)")
    for fid, f in new[:limit]:
        print("  ::error::NEW %s | %s" % (fid, f))
    if len(new) > limit:
        print("  ... and %d more new findings" % (len(new) - limit))

    if stale:
        print("")
        print("--- 基线里已不再成立（可重新冻结）: %d 条 ---" % len(stale))
        for e in stale[:50]:
            print("  ::warning::STALE %s" % e["id"])
        if len(stale) > 50:
            print("  ... and %d more stale entries" % (len(stale) - 50))

    print("")
    print("--- 计数过期（警告，不阻断）: %d 条 ---" % len(stale_counts))
    if not stale_counts:
        print("  (none)")
    for w in stale_counts[:limit]:
        print("  ::warning::%s" % w)
    if len(stale_counts) > limit:
        print("  ... and %d more stale-count warnings" % (len(stale_counts) - limit))

    if other_warnings:
        print("")
        print("--- 其他警告（不阻断）: %d 条 ---" % len(other_warnings))
        for w in other_warnings[:limit]:
            print("  ::warning::%s" % w)

    print("")
    if mode == "legacy-report":
        print("[OK] legacy-report: 存量 %d 条 / 新增 %d 条 / 计数过期 %d 条 —— 只报告，不阻断 (exit 0)"
              % (len(legacy), len(new), len(stale_counts)))
        return 0
    if new:
        print("[FAIL] hard-fail: %d 条新增硬失败（基线外）-> exit 1（存量 %d 条已冻结）"
              % (len(new), len(legacy)))
        return 1
    print("[OK] hard-fail: 无新增硬失败（存量 %d 条已冻结）-> exit 0" % len(legacy))
    return 0


# ---- 检查本体 --------------------------------------------------------------


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
        return (["A: findings file not found: %s" % findings_path], [], {})
    try:
        payload = json.loads(findings_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return (["A: findings file is not valid JSON: %s" % exc], [], {})

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
            elif defect == "D4_quote_mismatch":
                quote = _as_text(mode.get("key_quote_zh"))
                if anchor not in quote:
                    errors.append("C: [%s] D4 引文不符的 anchor %r 不在记录 key_quote_zh 里"
                                  % (label, anchor[:60]))
            elif defect == "D5_timeline_conflict":
                fields = " ".join(_as_text(mode.get(f)) for f in
                                  ("definition_zh", "process_zh", "representative_cases_zh"))
                if anchor not in fields:
                    errors.append("C: [%s] D5 时间线矛盾的 anchor %r 不在记录的本人叙述字段里"
                                  % (label, anchor[:60]))
                if not re.search(r"(?<!\d)(1\d{3}|20\d{2})(?!\d)", anchor):
                    errors.append("C: [%s] D5 anchor %r 里没有 4 位年份" % (label, anchor[:60]))
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

    # E —— 计数过期：**警告**，不是硬失败（Phase37-X5 决策，理由见 credibility_framework.md §8）
    recomputed = {}
    stale_counts = []
    if check_counts:
        builder = _load_module("build_audit_findings_verify", REPO_ROOT / "tools" / "build_audit_findings.py")
        fresh = builder.scan_library(data_path)
        recomputed = fresh["summary"]
        for key in SUMMARY_KEYS:
            old = summary.get(key)
            new = recomputed.get(key)
            if old != new:
                stale_counts.append("%s summary.%s = %r 而现算 %s 得 %r —— %s"
                                    % (STALE_PREFIX, key, old, data_path.name, new, STALE_HINT))
        if summary.get("total") != recomputed.get("total"):
            stale_counts.append("%s summary.total = %r 而现算得 %r —— %s"
                                % (STALE_PREFIX, summary.get("total"), recomputed.get("total"),
                                   STALE_HINT))
        # 库 sha 变化是「计数可能过期」的信号；审计元数据里也如实记一条（不重复计过期）
        if audit_meta.get("modes_file_sha256") != fresh.get("audit_meta", {}).get("modes_file_sha256"):
            warnings.append("E: audit_meta.modes_file_sha256 differs from the current library hash; refresh with build_audit_findings.py --write")

    if dup_codes:
        warnings.append("E: these mode codes are harvested twice by get_all_modes (present both in the top-level modes array and inside a figure node): %s" % sorted(dup_codes)[:10])

    warnings = stale_counts + warnings
    return errors, warnings, {"entries": len(findings), "summary": summary,
                              "recomputed": recomputed, "stale_counts": stale_counts}


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify data/audit/findings.json against the source library")
    parser.add_argument("--findings", default=str(DEFAULT_FINDINGS))
    parser.add_argument("--data-path", default=str(DEFAULT_DATA_PATH))
    parser.add_argument("--no-check-counts", action="store_true", help="skip check E")
    parser.add_argument("--legacy-report", action="store_true",
                        help="存量/新增两档之「只报告」：基线内与基线外都逐条列出，一律 exit 0（不阻断）")
    parser.add_argument("--hard-fail", action="store_true",
                        help="存量/新增两档之「新增即拦」：基线内（data/audit/findings_baseline.json）"
                             "的存量只报告，基线外的任何硬失败 exit 1")
    parser.add_argument("--baseline", type=str, default=None,
                        help="基线文件路径；缺省随 --data-path 所在仓推导"
                             "（<root>/data/audit/findings_baseline.json）")
    parser.add_argument("--write-baseline", action="store_true",
                        help="用当前硬失败重新冻结基线（改基线必须显式跑这一步并在报告里说明）")
    args = parser.parse_args()

    findings_path = Path(args.findings)
    data_path = Path(args.data_path)
    repo_root = resolve_repo_root(data_path)
    baseline_path = (Path(args.baseline) if args.baseline
                     else repo_root / DEFAULT_BASELINE_NAME)

    errors, warnings, info = verify(findings_path, data_path, check_counts=not args.no_check_counts)
    stale_counts, _ = split_warnings(warnings)

    if args.write_baseline:
        bl = build_baseline(errors, data_path=data_path, findings_path=findings_path,
                            warnings=warnings, stale_counts=stale_counts, repo_root=repo_root)
        save_baseline(bl, baseline_path)
        print("=== VERIFY FINDINGS · 基线冻结 ===")
        print("findings path: %s" % findings_path)
        print("data path:     %s" % data_path)
        print("data sha256:   %s" % bl["data_sha256"])
        print("baseline path: %s" % baseline_path)
        print("frozen counts: %s" % json.dumps(bl["counts"], ensure_ascii=False))
        print("[OK] 基线已写入；此后 --hard-fail 只拦基线外的硬失败")
        return 0

    if args.legacy_report or args.hard_fail:
        mode = "legacy-report" if args.legacy_report else "hard-fail"
        return run_mode(mode, errors=errors, warnings=warnings, baseline_path=baseline_path,
                        findings_path=findings_path, data_path=data_path)

    print("=== VERIFY FINDINGS ===")
    print("findings file: %s" % findings_path)
    print("source library: %s" % data_path)
    print("entries: %s" % info.get("entries"))
    print("hard failures: %d" % len(errors))
    print("warnings: %d (计数过期 %d)" % (len(warnings), len(stale_counts)))
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
