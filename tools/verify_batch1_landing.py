#!/usr/bin/env python3
"""verify_batch1_landing.py — Phase21-W8 Stage2 批1 落地独立核验（卡 t_b85ae14a）。

对**盘上终态**逐项核验（不看过程日志、只认文件），可选外加三道门禁复跑：
    python3 tools/verify_batch1_landing.py                  # 数据面 18 项
    python3 tools/verify_batch1_landing.py --with-gates     # 外加 credibility/verify_findings/links 复跑
退出码：0 全 PASS / 1 任一 FAIL。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import credibility_gate as gate  # noqa: E402

LEDGER = REPO_ROOT / "data/audit/phase21w8_stage2_batch1_landing_ledger.json"
PACK = REPO_ROOT / "docs/research/phase21w8_stage2_batch1_sourcing_report.json"
INDEX = REPO_ROOT / "data/audit/source_texts_w8_stage2_batch1.json"
LINKS = REPO_ROOT / "data/source_links.json"
SOURCES = REPO_ROOT / "data/audit/source_texts.json"
FINDINGS = REPO_ROOT / "data/audit/findings.json"
MODES = REPO_ROOT / "data/modes_data.json"
REPORT = REPO_ROOT / "data/audit/verification_status.json"

RESULTS = []


def check(name: str, cond: bool, detail: str = ""):
    RESULTS.append((name, bool(cond), detail))
    print("%s %s%s" % ("[PASS]" if cond else "[FAIL]", name, (" — " + detail) if detail else ""))


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-gates", action="store_true")
    args = ap.parse_args()

    ledger = load(LEDGER)
    pack = load(PACK)
    index = load(INDEX)
    links = load(LINKS)
    sources = load(SOURCES)
    findings = load(FINDINGS)
    modes = load(MODES)
    report = load(REPORT)
    items = ledger["items"]
    cur = {str(m.get("mode_code")): m for m in modes["modes"] if isinstance(m, dict)}
    cn_books = sorted({e["key"] for e in index["entries"] if e.get("lang") == "lzh"})
    cross_books = sorted({e["key"] for e in index["entries"] if e.get("lang") != "lzh"})

    check("①账本存在且自检 PASS", ledger.get("verdict") == "PASS", "verdict=%s" % ledger.get("verdict"))
    check("②账本条目 154 条、处分类别求和 154",
          len(items) == 154 and sum(ledger["dispositions_summary"].values()) == 154,
          "items=%d" % len(items))

    # ③ 链接：8 中文书入库（url/canonical_title/provider/checked_at 齐），9 跨语言书零链接
    missing = [b for b in cn_books if not (links.get(b) or {}).get("url")]
    fields_ok = all(all(k in (links.get(b) or {}) for k in ("url", "canonical_title", "provider", "checked_at", "source_type"))
                    for b in cn_books)
    check("③批1 中文书 8 部全部在 source_links（字段齐）", len(cn_books) == 8 and not missing and fields_ok,
          "cn=%d missing=%s fields=%s" % (len(cn_books), missing, fields_ok))
    check("④跨语言书 9 部零链接（口径待裁定，未越界）",
          len(cross_books) == 9 and not any(b in links for b in cross_books),
          "cross=%d linked=%s" % (len(cross_books), [b for b in cross_books if b in links]))

    # ⑤ 缓存：批1 索引 17 条全部并入，sha256/file 原样
    idx = {e["key"]: e for e in index["entries"]}
    st = {e["key"]: e for e in sources["entries"]}
    merged = [k for k in idx if k in st]
    same_sha = all(st[k].get("sha256") == idx[k].get("sha256") and st[k].get("file") == idx[k].get("file") for k in merged)
    check("⑤批1 缓存 17 条全部并入 source_texts（sha256/file 原样）",
          len(idx) == 17 and len(merged) == 17 and same_sha, "merged=%d sha_ok=%s" % (len(merged), same_sha))

    # ⑥ D4 判定与账本一致（逐 mode 复算，用 credibility_gate 唯一实现）
    cache = gate.make_cache(REPO_ROOT)
    link_index = gate.load_link_index()
    recomputed, mismatch_codes = {}, []
    for code in {i["mode_code"] for i in items}:
        res = gate.d4_scan(cur.get(code, {}), cache, link_index)
        recomputed[code] = res["status"] + "|" + res["reason"].split(":")[0].split("(")[0].strip()
        if res["status"] == "mismatch":
            mismatch_codes.append(code)
    ledger_d4 = {i["mode_code"]: "%s|%s" % (i["d4"]["status"], i["d4"]["reason"].split(":")[0].split("(")[0].strip())
                 for i in items}
    check("⑥D4 逐条复算与账本一致（%d 个 mode）" % len(recomputed),
          {k: recomputed[k] for k in recomputed} == {k: ledger_d4[k] for k in recomputed})
    check("⑦D4 mismatch 恰为 3 条且=账本 suspect 名单",
          sorted(mismatch_codes) == ["M-WB-003", "M-WB-004", "M-WB-008"],
          ",".join(sorted(mismatch_codes)))

    # ⑧ 状态：库中 status == 账本 status_after；翻面 69/3；包外 0
    st_ok = all((cur[i["mode_code"]].get("verification") or {}).get("status") == i["status_after"] for i in items)
    check("⑧库中状态与账本 status_after 逐条一致（154）", st_ok)
    flips = ledger["status_flips"]
    check("⑨状态翻面 = pending->verified 69 / pending->suspect 3 / 其他 0",
          len(flips["pending->verified"]) == 69 and len(flips["pending->suspect"]) == 3 and not flips["other"],
          "verified=%d suspect=%d other=%d" % (len(flips["pending->verified"]), len(flips["pending->suspect"]), len(flips["other"])))
    item_codes = {i["mode_code"] for i in items}
    check("⑩包外模式零翻面（单卡面）",
          not [c for c in flips["pending->verified"] + flips["pending->suspect"] if c not in item_codes])

    # ⑪ findings：168 条 / D4_quote_mismatch 27（+3）；3 条新增锚点可定位在 key_quote_zh
    summ = findings["summary"]
    new_d4 = [f for f in findings["findings"] if f.get("defect") == "D4_quote_mismatch"
              and str(f.get("mode_code")) in {"M-WB-003", "M-WB-004", "M-WB-008"}]
    anchors_ok = all((f.get("anchor") or "") in (cur[str(f["mode_code"])].get("key_quote_zh") or "") for f in new_d4)
    check("⑪findings=168 且 D4_quote_mismatch=27（+3）", summ["total"] == 168 and summ["D4_quote_mismatch"] == 27,
          "total=%d d4=%d" % (summ["total"], summ["D4_quote_mismatch"]))
    check("⑫3 条新增 D4 锚点在库引文内可逐字定位", len(new_d4) == 3 and anchors_ok, "n=%d anchors=%s" % (len(new_d4), anchors_ok))

    # ⑬ 四态自洽（全库 3311 / 公开 3251）+ 报告计数一致
    counts = Counter((m.get("verification") or {}).get("status") for m in modes["modes"] if isinstance(m, dict))
    rep_counts = report["counts"]
    check("⑬四态全库求和=3311 且与 verification_status.json 一致",
          sum(counts.values()) == 3311
          and all(counts.get(k) == rep_counts["all"][k] for k in rep_counts["all"]),
          json.dumps(dict(counts), ensure_ascii=False))
    check("⑭公开口径 3251 / 隔离 60 且与报告一致",
          rep_counts["published_total"] == 3251 and rep_counts["quarantined_total"] == 60
          and sum(rep_counts["published"].values()) + 60 == 3311)

    # ⑮ verify_findings 规则 C：全部 findings 锚点可在库文本定位（抽样全量都查：D4/D4b/D5）
    bad = []
    for f in findings["findings"]:
        anch = f.get("anchor")
        mc = str(f.get("mode_code") or "")
        if not anch or mc not in cur:
            continue
        blob = json.dumps(cur[mc], ensure_ascii=False)
        if anch not in blob:
            bad.append("%s:%s" % (f.get("defect"), mc))
    check("⑮findings 锚点全量可定位（%d 条）" % len(findings["findings"]), not bad, ",".join(bad[:5]))

    # ⑯ 备份目录 + sha 收据存在
    bk = sorted((REPO_ROOT / "data").glob("backup_merge_W8B1_*"))
    man_ok = False
    if bk:
        man = load(bk[-1] / "MANIFEST.json")
        man_ok = len(man.get("files", [])) == 5 and all(f.get("present") for f in man["files"])
    check("⑯先备份后落地：备份目录 5 件齐 + MANIFEST", bool(bk) and man_ok, bk[-1].name if bk else "missing")

    if args.with_gates:
        for name, cmd in (
            ("credibility_gate --hard-fail", [sys.executable, "tools/credibility_gate.py", "--hard-fail"]),
            ("verify_findings --hard-fail", [sys.executable, "tools/verify_findings.py", "--hard-fail"]),
            ("apply_verification_status --check", [sys.executable, "tools/apply_verification_status.py", "--check"]),
            ("pages_preflight --stage data", [sys.executable, "tools/pages_preflight.py", "--stage", "data"]),
        ):
            r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
            check("⑰门禁复跑 %s" % name, r.returncode == 0, "rc=%d" % r.returncode)

    nfail = len([1 for _, ok, _ in RESULTS if not ok])
    print("\n=== verify_batch1_landing: %d PASS / %d FAIL ===" % (len(RESULTS) - nfail, nfail))
    return 1 if nfail else 0


if __name__ == "__main__":
    raise SystemExit(main())
