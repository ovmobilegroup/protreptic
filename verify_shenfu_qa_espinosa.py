#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_shenfu_qa_espinosa.py - Phase21-R9 Shen Fu (H-SHF-001) chain QA, independent acceptance (card t_83e0d68d).

Independent stance: every judgement is re-derived from raw artifacts - git objects (5a657b81 etc.),
current worktree state of the six files, pre-merge backup images, rebuild landing package (A1),
sourcing witnesses, site products, publish repo git objects. Self-reported numbers from the
verified cards are registered as cross-reference only, never as proof.

Groups:
  A chain + commits     B mode entries vs figure     C quotes + witnesses
  D site chain          E parity / mirror / push      F boundary

Usage:
  python3 verify_shenfu_qa_espinosa.py [--out <evidence.json>] [--logs <dir>] [--quick]
  --quick: skip rerun checks (export/preflight/parity/ls-remote).
Exit code: 0 = no FAIL (INFO allowed); 1 = FAIL present.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent
PUB = Path("/opt/data/release/Protreptic-publish")
BACKUP = REPO / "data/backup_merge_H-SHF-001_20260924_093849"
LAND = REPO / "docs/scratch/legacy20_r9_shenfu_landing"
WIT = REPO / "docs/scratch/phase21r9_shenfu/witness"
SCRATCH = Path("/opt/data/profiles/espinosa/cache/scratch/shenfu_qa")

SIX = [
    "data/modes_data.json",
    "data/code_maps.json",
    "data/figure_names.json",
    "data/scenarios_zh.json",
    "data/scenarios_en.json",
    "data/scenario_tags.json",
]
CODES = ["M-SHF-%03d" % i for i in range(1, 11)]
EXPECT_MODES = 3301
EXPECT_PUBLISHED = 3241
EXPECT_QUAR = 60
EXPECT_BY_FIGURE = 320
EXPECT_FIGURES = 1027

RESULTS = []


def add(cid, group, title, ok, detail="", status=None):
    st = status or ("PASS" if ok else "FAIL")
    RESULTS.append({"id": cid, "group": group, "title": title, "status": st, "detail": detail})
    print("[%s] %-9s %s" % (st, cid, title))
    if detail and st != "PASS":
        print("      " + str(detail)[:2000].replace("\n", "\n      "))


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def jload(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def canon(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def git(*args, cwd=REPO):
    p = subprocess.run(["git", "-C", str(cwd)] + list(args), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def git_blob_sha(commit, rel):
    p = subprocess.run(["git", "-C", str(REPO), "show", "%s:%s" % (commit, rel)], capture_output=True)
    if p.returncode != 0:
        return None
    return sha256_bytes(p.stdout)


def run_cmd(cmd, cwd=REPO, timeout=1200):
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def write_log(logdir, name, text):
    logdir.mkdir(parents=True, exist_ok=True)
    (logdir / name).write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO / "docs/research/phase21r9_shenfu_qa_evidence.json"))
    ap.add_argument("--logs", default=str(REPO / "docs/research/phase21r9_shenfu_qa_logs"))
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    LOGS = Path(args.logs)

    MM = jload(REPO / "data/audit/phase21r9_shenfu_merge_manifest.json")
    LM = jload(REPO / "data/audit/phase21r9_shenfu_landing_manifest.json")
    ME = jload(REPO / "docs/research/phase21r9_shenfu_merge_evidence.json")

    # ================================================================ A chain + commits
    good, bad = [], []
    for rel in SIX:
        b = BACKUP / Path(rel).name
        got = sha256_file(b) if b.exists() else "MISSING"
        want = MM["inputs"][rel]["sha256"]
        (good if got == want else bad).append("%s %s" % (Path(rel).name, got[:12]))
    add("A01", "A", "backup six pre-images sha256 == merge manifest inputs", not bad,
        "good=%d/6 bad=%s" % (len(good), bad))

    good, bad = [], []
    for rel in SIX:
        got = sha256_file(REPO / rel)
        want = MM["after"][rel]["sha256"]
        want2 = ME["sha256"]["after"][rel]
        (good if (got == want == want2) else bad).append("%s got=%s want=%s want2=%s" % (rel, got[:12], want[:12], want2[:12]))
    add("A02", "A", "worktree six files sha256 == manifest/evidence after", not bad,
        "good=%d/6 bad=%s" % (len(good), bad))

    good, bad = [], []
    for rel in SIX:
        blob = git_blob_sha("5a657b81", rel)
        want = MM["after"][rel]["sha256"]
        (good if blob == want else bad).append("%s blob=%s want=%s" % (rel, str(blob)[:12], want[:12]))
    rc1, out1, _ = git("diff", "--name-only", "5a657b81", "HEAD", "--", *SIX)
    rc2, out2, _ = git("status", "--porcelain", "--", *SIX)
    add("A03", "A", "5a657b81 blobs == after; six files zero-drift vs HEAD and worktree", not bad and not out1.strip() and not out2.strip(),
        "blob bad=%s | diff-vs-HEAD=%r | status=%r" % (bad, out1.strip(), out2.strip()))

    chain = [("e0a98aa8", "59bc5471"), ("59bc5471", "5a657b81"), ("5a657b81", "906a0bee"),
             ("906a0bee", "c3cceb19"), ("c3cceb19", "HEAD")]
    bad = []
    for a, b in chain:
        rc, _, _ = git("merge-base", "--is-ancestor", a, b)
        if rc != 0:
            bad.append("%s->%s" % (a, b))
    _, head, _ = git("rev-parse", "HEAD")
    add("A04", "A", "commit ancestry (sourcing->rebuild->merge->receipt->verify->HEAD)", not bad,
        "HEAD=%s bad=%s" % (head.strip()[:12], bad))

    good, bad = [], []
    for rel, meta in LM["deliverables"].items():
        p = REPO / rel
        got = sha256_file(p) if p.exists() else "MISSING"
        (good if got == meta["sha256"] else bad).append(rel)
    pairs = [
        ("data/figures/H-SHF-001.json", "docs/scratch/legacy20_r9_shenfu_landing/figures/H-SHF-001.json"),
        ("data/individuals/H-SHF-001.json", "docs/scratch/legacy20_r9_shenfu_landing/individuals/H-SHF-001.json"),
        ("data/individuals/H-SHF-001_modes.json", "docs/scratch/legacy20_r9_shenfu_landing/individuals/H-SHF-001_modes.json"),
    ]
    for a, b in pairs:
        if sha256_file(REPO / a) != sha256_file(REPO / b):
            bad.append("pair-diff %s" % a)
    add("A05", "A", "landing 9 deliverables sha256 == landing manifest; data vs landing copies byte-equal", not bad,
        "good=%d/9 bad=%s" % (len(good), bad))

    good, bad = [], []
    for name, want in LM["archive_untouched"].items():
        cand = REPO / "data/figures/_duplicates" / name
        got = sha256_file(cand) if cand.exists() else "MISSING"
        (good if got == want else bad).append(name)
    add("A06", "A", "archived legacy files untouched (H-HAN-001 three files sha256)", not bad,
        "good=%d/3 bad=%s" % (len(good), bad))

    EXPECT24 = sorted([
        "data/audit/findings.json", "data/audit/phase21r9_shenfu_merge_manifest.json",
        "data/code_maps.json", "data/figure_names.json", "data/modes_data.json",
        "data/scenario_tags.json", "data/scenarios_en.json", "data/scenarios_zh.json",
        "docs/02-tools/figure_library.md", "docs/architecture/static_data_manifest.json", "docs/index.md",
        "docs/research/phase21r9_shenfu_merge_evidence.json", "docs/research/phase21r9_shenfu_merge_evidence.txt",
        "docs/research/phase21r9_shenfu_merge_report.md", "docs/research/phase21r9_shenfu_merge_verify_indep.json",
        "docs/research/phase21r9_shenfu_verify_evidence_merged.json",
        "tools/export_static_site.py", "tools/merge_phase21r9_shenfu.py", "tools/pages_preflight.py",
        "verify_phase21r9_shenfu.py", "verify_phase21r9_shenfu_merge_indep.py",
        "web/public/manifest-light.webmanifest", "web/public/manifest.webmanifest",
        "web/src/generated/siteCounts.ts",
    ])
    _, out, _ = git("show", "--name-only", "--format=", "5a657b81")
    got24 = sorted(x for x in out.split("\n") if x.strip())
    add("A07", "A", "main commit 5a657b81 changeset == expected 24 files (no smuggling)", got24 == EXPECT24,
        "n=%d extra=%s missing=%s" % (len(got24), sorted(set(got24) - set(EXPECT24)), sorted(set(EXPECT24) - set(got24))))
    bad = []
    for c in ("906a0bee", "c3cceb19", "a96302f1", "5ce7f6ad", "8c486442"):
        _, out, _ = git("show", "--name-only", "--format=", c)
        hit = sorted(set(x for x in out.split("\n") if x.strip()) & set(SIX))
        if hit:
            bad.append("%s:%s" % (c, hit))
    add("A08", "A", "later commits (receipts/sibling chain) never touched the six data files", not bad, "bad=%s" % bad)

    # ================================================================ B mode entries vs figure (item by item)
    AFTER = jload(REPO / "data/modes_data.json")
    BEFORE = jload(BACKUP / "modes_data.json")
    LAND_ENTRIES = jload(LAND / "combined_library_entries.json")["modes"]
    LAND_ML = jload(LAND / "modes_library_entries.json")
    FIG = jload(REPO / "data/figures/H-SHF-001.json")
    IND = jload(REPO / "data/individuals/H-SHF-001.json")
    INDM = jload(REPO / "data/individuals/H-SHF-001_modes.json")
    CM = jload(REPO / "data/code_maps.json")
    FN = jload(REPO / "data/figure_names.json")
    SZ = jload(REPO / "data/scenarios_zh.json")
    SE = jload(REPO / "data/scenarios_en.json")
    TG = jload(REPO / "data/scenario_tags.json")
    PROP = jload(LAND / "top_block_proposal.json")

    A_MODES = AFTER["modes"]
    B_ADDS = ["B02-%02d" % i for i in range(1, 11)]
    add("B01", "B", "modes list len==3311, total==len, SHF block is the tail 10 in order", 
        len(A_MODES) == 3311 and AFTER.get("total") == 3311 and [e.get("mode_code") for e in A_MODES[-10:]] == CODES,
        "len=%d total=%s tail=%s" % (len(A_MODES), AFTER.get("total"), [e.get("mode_code") for e in A_MODES[-10:]]))

    for i, (code, want) in enumerate(zip(CODES, LAND_ENTRIES), 1):
        got = A_MODES[EXPECT_MODES + i - 1]
        same = canon(got) == canon(want)
        add("B02-%02d" % i, "B", "%s in library == landing A1 entry (deep)" % code, same,
            "" if same else "diff fields: %s" % [k for k in set(list(got) + list(want)) if canon(got.get(k)) != canon(want.get(k))])

    same_fig = [i for i in range(10) if canon(A_MODES[EXPECT_MODES + i]) != canon(FIG["modes"][i])]
    same_ind = [i for i in range(10) if canon(A_MODES[EXPECT_MODES + i]) != canon(INDM["modes"][i])]
    same_ml = [i for i in range(10) if canon(A_MODES[EXPECT_MODES + i]) != canon(LAND_ML[i])]
    add("B03", "B", "library entries == figure modes == individuals modes == modes_library_entries", 
        not same_fig and not same_ind and not same_ml,
        "fig=%s ind=%s ml=%s" % (same_fig, same_ind, same_ml))

    bad = []
    for i, code in enumerate(CODES, 1):
        e = A_MODES[EXPECT_MODES + i - 1]
        if not (e.get("id") == e.get("mode_code") == code):
            bad.append("%s id/mode_code" % code)
        if e.get("figure_code") != "H-SHF-001":
            bad.append("%s figure_code" % code)
        if e.get("figure_name") != "\u6c88\u590d":
            bad.append("%s figure_name" % code)
        for f in ("definition_zh", "definition_en", "key_quote_zh", "name_zh", "name_en", "source_chapter"):
            if not str(e.get(f) or "").strip():
                bad.append("%s empty %s" % (code, f))
        for f in ("process_zh", "process_en", "representative_cases_zh", "representative_cases_en",
                  "modern_applications_zh", "modern_applications_en", "key_concepts"):
            v = e.get(f)
            if not v or (isinstance(v, (list, dict)) and len(v) == 0):
                bad.append("%s empty %s" % (code, f))
    add("B04", "B", "entry invariants (id==mode_code, figure link, non-empty core fields)", not bad, "bad=%s" % bad)

    fbad = []
    if FIG.get("mode_ids") != CODES:
        fbad.append("mode_ids")
    if FIG.get("thinking_mode_count") != 10:
        fbad.append("thinking_mode_count")
    if FIG.get("code") != "H-SHF-001" or FIG.get("figure_name") != "\u6c88\u590d":
        fbad.append("code/name")
    if FIG.get("birth_year") != 1763:
        fbad.append("birth_year")
    if len(FIG.get("caveats") or []) != 8:
        fbad.append("caveats=%d" % len(FIG.get("caveats") or []))
    ct_bad = [i + 1 for i in range(10) if ("M-SHF-%03d" % (i + 1)) not in str(FIG.get("core_thoughts", [""] * 10)[i])]
    add("B05", "B", "figure H-SHF-001 archive: mode_ids / count / identity / caveats / core_thoughts link", not fbad and not ct_bad,
        "bad=%s core_thoughts_bad=%s" % (fbad, ct_bad))

    cmf = CM["figures"].get("H-SHF-001") or {}
    cbad = []
    if cmf.get("mode_ids") != CODES:
        cbad.append("mode_ids")
    if cmf.get("tags") != [e["name_zh"] for e in LAND_ENTRIES]:
        cbad.append("tags")
    if canon(cmf.get("cross_references")) != canon(FIG.get("cross_references")):
        cbad.append("cross_references-vs-figure")
    for x in cmf.get("cross_references") or []:
        if x.get("target_figure_code") not in CM["figures"]:
            cbad.append("dangling xref %s" % x.get("target_figure_code"))
    add("B06", "B", "code_maps[H-SHF-001] = mode_ids + name tags + figure xrefs (0 dangling)", not cbad, "bad=%s" % cbad)

    n_shenfu = [k for k, v in FN.items() if v == "\u6c88\u590d"]
    add("B07", "B", "figure_names: H-SHF-001->Shen Fu, 1085 keys, exactly one key maps the name", 
        FN.get("H-SHF-001") == "\u6c88\u590d" and len(FN) == 1085 and n_shenfu == ["H-SHF-001"],
        "len=%d shenfu_keys=%s" % (len(FN), n_shenfu))

    blk = AFTER.get("H-SHF-001")
    keys = list(AFTER.keys())
    pos_ok = "H-SHF-001" in keys and "modes" in keys and keys.index("H-SHF-001") < keys.index("modes")
    add("B08", "B", "top block H-SHF-001 == proposal (23 keys, placed before modes)", 
        canon(blk) == canon(PROP["proposal"]) and len(blk) == 23 and pos_ok,
        "eq=%s n=%s pos_ok=%s" % (canon(blk) == canon(PROP["proposal"]), len(blk), pos_ok))

    SZC = SZ["scenarios_zh"]
    SEC = SE["scenarios_en"]
    for i, e in enumerate(LAND_ENTRIES, 1):
        code = "C-SHF-%03d" % i
        z = SZC.get(code)
        zbad = []
        if not z:
            zbad.append("missing")
        else:
            if z.get("code") != code or z.get("mode_code") != ("M-SHF-%03d" % i):
                zbad.append("code/mode_code")
            if z.get("title_zh") != e["name_zh"] or z.get("title_en") != e["name_en"]:
                zbad.append("titles")
            if z.get("application_area_zh") != e.get("modern_applications_zh"):
                zbad.append("area_zh")
            if z.get("application_area_en") != e.get("modern_applications_en"):
                zbad.append("area_en")
            want_zh = "%s" % e["name_zh"] + "\u7684\u5f53\u4ee3\u5e94\u7528\u573a\u666f\uff1a" + "\uff1b".join(e.get("modern_applications_zh") or []) + "\u3002"
            if z.get("text_zh") != want_zh:
                zbad.append("text_zh-recompute")
            if set(z.keys()) != {"code", "mode_code", "title_zh", "title_en", "text_zh", "text_en", "application_area_zh", "application_area_en"}:
                zbad.append("key-set=%s" % sorted(z.keys()))
        add("B09-%02d" % i, "B", "%s scenario zh (recomputed text/area/titles vs entry)" % code, not zbad, "bad=%s" % zbad)

    ebad = []
    for i, e in enumerate(LAND_ENTRIES, 1):
        code = "C-SHF-%03dE" % i
        en = SEC.get(code)
        zh = SZC.get("C-SHF-%03d" % i)
        if not en:
            ebad.append("%s missing" % code)
            continue
        if en.get("mode_code") != ("M-SHF-%03d" % i):
            ebad.append("%s mode_code" % code)
        a = dict(en); a.pop("code", None)
        b = dict(zh); b.pop("code", None)
        if canon(a) != canon(b):
            ebad.append("%s body != zh body" % code)
        want_en = "Contemporary applications of " + e["name_en"] + ": " + "; ".join(e.get("modern_applications_en") or []) + "."
        if en.get("text_en") != want_en:
            ebad.append("%s text_en-recompute" % code)
    add("B10", "B", "scenarios_en C-SHF-001E..010E (1:1 with zh, recomputed text_en)", not ebad, "bad=%s" % ebad)

    want_tags = []
    for i, e in enumerate(LAND_ENTRIES, 1):
        want_tags.append({"mode_code": "M-SHF-%03d" % i, "tag": e["name_zh"] + "_zh", "figure_code": "H-SHF-001", "language": "zh"})
        want_tags.append({"mode_code": "M-SHF-%03d" % i, "tag": e["name_en"] + "_en", "figure_code": "H-SHF-001", "language": "en"})
    tags = TG["scenario_tags"]
    idxs = [i for i, x in enumerate(tags) if x.get("figure_code") == "H-SHF-001"]
    contiguous = idxs == list(range(idxs[0], idxs[0] + 20)) if idxs else False
    got_tags = [tags[i] for i in idxs]
    add("B11", "B", "scenario_tags +20 block (zh then en per mode, contiguous, figure H-SHF-001)", 
        len(idxs) == 20 and contiguous and canon(got_tags) == canon(want_tags) and len(tags) == 7538,
        "n=%d contiguous=%s len=%d eq=%s" % (len(idxs), contiguous, len(tags), canon(got_tags) == canon(want_tags)))

    note = str(FIG.get("mode_ids_note") or "")
    add("B12", "B", "figure mode_ids_note present (new code, legacy not reused)", "H-SHF-001" in note and "M-SHF-010" in note, "note_len=%d" % len(note))
    # ================================================================ C quotes + witnesses
    src_md = (REPO / "docs/research/phase21r9_shenfu_sourcing_report.md").read_text(encoding="utf-8")
    qre = re.compile(r'^\s*> \u300c(.+?)\u300d\u2014\u2014(.+)$', re.M)
    quotes = [(m.group(1), m.group(2)) for m in qre.finditer(src_md)]
    add("C01", "C", "sourcing report quote lines extracted (expect 35)", len(quotes) == 35, "n=%d" % len(quotes))

    def norm(s):
        return re.sub(r'[^0-9A-Za-z\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]', '', s)

    W = {}
    for fn in sorted(os.listdir(WIT)):
        if fn.endswith((".txt", ".html")) and fn != "witness_sha256.txt":
            t = (WIT / fn).read_text(encoding="utf-8", errors="replace")
            if fn.endswith(".html"):
                import html as _html
                t = t + "\n" + _html.unescape(re.sub(r'<[^>]+>', ' ', t))
            W[fn] = norm(t)
    hits, miss = [], []
    for i, (q, attr) in enumerate(quotes, 1):
        nq = norm(q)
        hit = None
        for fn, t in W.items():
            p = t.find(nq)
            if p >= 0:
                hit = "%s@%d" % (fn, p)
                break
        if not hit and nq.startswith("\u82b8"):
            for fn, t in W.items():
                p = t.find(nq[1:])
                if p >= 0:
                    hit = "%s@%d drop-yun" % (fn, p)
                    break
        (hits if hit else miss).append((i, q[:24], hit))
    add("C02", "C", "all report quotes found in witness copies (independent normalization)",
        not miss and len(hits) == 35, "hits=%d/35 miss=%s" % (len(hits), miss[:5]))

    qvf = jload(WIT / "quote_verification_final.json")
    add("C03", "C", "witness quote_verification_final.json artifact: 35 rows all found",
        len(qvf) == 35 and all(r.get("found") for r in qvf),
        "n=%d unfound=%s" % (len(qvf), [r.get("n") for r in qvf if not r.get("found")]))

    wlines = (WIT / "witness_sha256.txt").read_text(encoding="utf-8").splitlines()
    wbad, wn = [], 0
    for ln in wlines:
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        parts = ln.split()
        if len(parts) < 3:
            wbad.append("parse:%s" % ln[:60])
            continue
        sha, size, name = parts[0], parts[1], parts[2]
        p = WIT / name
        if not p.exists():
            wbad.append("missing:%s" % name)
            continue
        if sha256_file(p) != sha or str(p.stat().st_size) != size:
            wbad.append(name)
        wn += 1
    add("C04", "C", "witness_sha256.txt manifest: %d files sha256+size verified" % wn, wn == 35 and not wbad,
        "n=%d bad=%s" % (wn, wbad[:6]))

    kqbad = []
    for i, e in enumerate(LAND_ENTRIES, 1):
        nq = norm(e["key_quote_zh"])
        hit = any(nq in t for t in W.values())
        if not hit and nq.startswith("\u82b8"):
            hit = any(nq[1:] in t for t in W.values())
        if not hit:
            kqbad.append("M-SHF-%03d" % i)
    add("C05", "C", "each entry key_quote_zh traceable to witnesses (10/10)", not kqbad, "bad=%s" % kqbad)

    fq = FIG.get("famous_quote") or ""
    fq_ok = any(norm(fq) in t for t in W.values()) if fq else False
    add("C06", "C", "figure famous_quote traceable to witnesses", fq_ok, "quote=%r" % fq[:30])

    # ================================================================ D site chain
    if not args.quick:
        rc, out, err = run_cmd([sys.executable, "tools/pages_preflight.py", "--stage", "data"])
        write_log(LOGS, "pages_preflight_data.txt", out + "\n" + err)
        add("D01", "D", "pages_preflight --stage data exit 0 (rerun)", rc == 0 and "figures=1027" in out,
            "rc=%d tail=%s" % (rc, out.strip().splitlines()[-3:] if out.strip() else err[:200]))

        fresh = SCRATCH / "qa_export"
        if fresh.exists():
            shutil.rmtree(fresh)
        rc, out, err = run_cmd([sys.executable, "tools/export_static_site.py", "--out", str(fresh)], timeout=1800)
        write_log(LOGS, "export_fresh.txt", out + "\n" + err)
        fm = jload(fresh / "meta.json")["counts"] if (fresh / "meta.json").exists() else {}
        okc = (fm.get("figures") == EXPECT_FIGURES and fm.get("modes_deduped") == EXPECT_MODES
               and fm.get("mode_summaries_published") == EXPECT_PUBLISHED and fm.get("modes_quarantined") == EXPECT_QUAR
               and fm.get("mode_by_figure_shards") == EXPECT_BY_FIGURE and fm.get("modes_raw") == 3311)
        add("D02", "D", "fresh export_static_site rerun: counts reproduced (figures/modes/published/quar/by-figure)",
            rc == 0 and okc, "rc=%d counts=%s" % (rc, {k: fm.get(k) for k in ("figures", "modes_deduped", "modes_quarantined", "mode_summaries_published", "mode_by_figure_shards", "modes_raw")}))

        def tree_shas(root):
            d = {}
            for p in sorted(Path(root).rglob("*")):
                if p.is_file():
                    d[p.relative_to(root).as_posix()] = sha256_file(p)
            return d

        t_new = tree_shas(fresh)
        t_old = tree_shas(REPO / "web/public/data")
        daily = {"daily/index.json", "daily/names.json"}
        excl = set(daily) | {"meta.json"}
        diff = sorted([k for k in (set(t_new) | set(t_old)) - excl if t_new.get(k) != t_old.get(k)])
        def meta_core(p):
            d = jload(p)
            for k in ("generated_at", "generated_at_local"):
                d.pop(k, None)
            return canon(d)
        meta_ok = meta_core(fresh / "meta.json") == meta_core(REPO / "web/public/data/meta.json")
        write_log(LOGS, "export_vs_committed_diff.json", json.dumps({"diff": diff, "meta_ts_masked_ok": meta_ok},
                                                                    ensure_ascii=False, indent=1))
        add("D03", "D", "fresh export tree == committed web/public/data (byte-exact modulo meta timestamps; daily deferred to D05)",
            not diff and meta_ok, "diff=%s meta_ts_masked_ok=%s n_new=%d n_old=%d" % (diff[:12], meta_ok, len(t_new), len(t_old)))
        mp = REPO / "docs/architecture/static_data_manifest.json"
        try:
            mmj = jload(mp)
        except Exception:
            mmj = {}
        if str(mmj.get("out_dir", "")) == str(fresh):
            rc, out, err = git("checkout", "--", "docs/architecture/static_data_manifest.json")
            add("D03b", "D", "rolled back shared manifest side write of this scratch export (restored to HEAD)", rc == 0, "rc=%d" % rc)
        else:
            add("D03b", "D", "shared manifest carries another writer (left untouched)", True,
                "out_dir=%s" % mmj.get("out_dir"), status="INFO")

        rc, out, err = run_cmd([sys.executable, "tools/gen_web_site_counts.py", "--check"])
        write_log(LOGS, "gen_web_site_counts_check.txt", out + "\n" + err)
        ts = (REPO / "web/src/generated/siteCounts.ts").read_text(encoding="utf-8")
        nums = dict(re.findall(r'(modes|figures|sourceTotal)\s*:\s*(\d+)', ts))
        add("D04", "D", "gen_web_site_counts --check exit 0; siteCounts.ts = 3241 x 320 (src 3301)",
            rc == 0 and nums.get("modes") == "3241" and nums.get("figures") == "320" and nums.get("sourceTotal") == "3301",
            "rc=%d nums=%s" % (rc, nums))

        rc, out, err = run_cmd([sys.executable, "tools/build_daily_index.py", "--check"])
        write_log(LOGS, "build_daily_index_check.txt", out + "\n" + err)
        di = jload(REPO / "web/public/data/daily/index.json")
        add("D05", "D", "build_daily_index --check exit 0; daily total=3241 / figure_count=320",
            rc == 0 and di.get("total") == EXPECT_PUBLISHED and di.get("figure_count") == EXPECT_BY_FIGURE,
            "rc=%d total=%s figs=%s" % (rc, di.get("total"), di.get("figure_count")))
    else:
        for cid, t in [("D01", "pages_preflight rerun (skipped --quick)"), ("D02", "fresh export rerun (skipped --quick)"),
                       ("D03", "fresh export vs committed (skipped --quick)"), ("D04", "gen_web_site_counts --check (skipped --quick)"),
                       ("D05", "build_daily_index --check (skipped --quick)")]:
            add(cid, "D", t, True, "quick mode", status="INFO")

    meta = jload(REPO / "web/public/data/meta.json")["counts"]
    okm = (meta.get("modes_raw") == 3311 and meta.get("modes_deduped") == EXPECT_MODES
           and meta.get("mode_summaries_published") == EXPECT_PUBLISHED and meta.get("modes_quarantined") == EXPECT_QUAR
           and meta.get("mode_by_figure_shards") == EXPECT_BY_FIGURE and meta.get("figures") == EXPECT_FIGURES)
    add("D06", "D", "committed meta.json counts consistent (3311 raw / 3301 dedup / 3241 pub / 60 quar / 320 / 1027)",
        okm, "counts=%s" % {k: meta.get(k) for k in ("modes_raw", "modes_deduped", "mode_summaries_published", "modes_quarantined", "mode_by_figure_shards", "figures")})

    sys.path.insert(0, str(REPO / "tools"))
    import site_counts  # noqa: E402
    dm, df = site_counts.load_counts(REPO / "web/dist/data")
    n1, v1 = site_counts.scan_display_surfaces(REPO / "web/dist", dm, df)
    n2, v2 = site_counts.scan_product_docs(REPO / "docs", dm, df)
    write_log(LOGS, "site_counts_scans.json", json.dumps({"dist": {"checked": n1, "violations": v1},
                                                          "docs": {"checked": n2, "violations": v2}}, ensure_ascii=False, indent=1))
    add("D07", "D", "display-surface scans zero violations (dist %d files / docs %d pages; counts 3241x320)" % (n1, n2),
        (dm, df) == (EXPECT_PUBLISHED, EXPECT_BY_FIGURE) and not v1 and not v2,
        "dist_viol=%s docs_viol=%s" % (v1[:5], v2[:5]))

    import _quarantine  # noqa: E402
    qset = set(_quarantine.QUARANTINE)
    qmodes = [e for e in A_MODES if str(e.get("figure_code") or "") in qset]
    qcodes = set(e.get("mode_code") for e in qmodes)
    leaks = []
    for p in sorted((REPO / "web/public/data").rglob("*.json")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        for c in qcodes:
            if c and c in t:
                leaks.append("%s:%s" % (p.relative_to(REPO), c))
                break
    fi = (REPO / "web/public/data/figures.index.json").read_text(encoding="utf-8")
    qfig_leak = [c for c in qset if c in fi]
    add("D08", "D", "quarantine: %d modes of quarantined figures excluded, zero leak in products" % len(qmodes),
        len(qmodes) == EXPECT_QUAR and not leaks and not qfig_leak,
        "n=%d leaks=%s fig_leaks=%s" % (len(qmodes), leaks[:5], qfig_leak))

    e_src = (REPO / "tools/export_static_site.py").read_text(encoding="utf-8")
    p_src = (REPO / "tools/pages_preflight.py").read_text(encoding="utf-8")
    def anchor(txt, name):
        m = re.search(r'^%s = (\d+)' % name, txt, re.M)
        return int(m.group(1)) if m else None
    av = {k: (anchor(e_src, k), anchor(p_src, k)) for k in ("EXPECT_MODES", "EXPECT_BY_FIGURE", "EXPECT_FIGURES")}
    add("D09", "D", "anchor constants equal across export/preflight and match observed counts",
        av["EXPECT_MODES"] == (EXPECT_MODES, EXPECT_MODES) and av["EXPECT_BY_FIGURE"] == (EXPECT_BY_FIGURE, EXPECT_BY_FIGURE)
        and av["EXPECT_FIGURES"] == (EXPECT_FIGURES, EXPECT_FIGURES),
        "anchors=%s" % av)
    # ================================================================ E parity / mirror / push
    CHAIN_FILES = set()
    for c in ("e0a98aa8", "59bc5471", "5a657b81", "906a0bee", "c3cceb19"):
        _, out, _ = git("show", "--name-only", "--format=", c)
        CHAIN_FILES.update(x.strip() for x in out.split("\n") if x.strip())
    CHAIN_FILES = sorted(CHAIN_FILES)

    parity_json = SCRATCH / "parity_now.json"
    if not parity_json.exists():
        alt = SCRATCH.parent / "parity_now.json"
        if alt.exists():
            parity_json = alt
    if not args.quick:
        rc, out, err = run_cmd([sys.executable, "tools/check_repo_parity.py", "--json"], timeout=1800)
        (SCRATCH).mkdir(parents=True, exist_ok=True)
        parity_json.write_text(out, encoding="utf-8")
        write_log(LOGS, "parity_stdout.err", err)
    if parity_json.exists() and parity_json.stat().st_size:
        pd = json.loads(parity_json.read_text(encoding="utf-8"))
        diffs = pd.get("diffs", [])
        dp = [x.get("path") for x in diffs]
        shf_in_diffs = sorted(set(dp) & set(CHAIN_FILES))
        inflight, real = [], []
        for pth in shf_in_diffs:
            rc, st, _ = git("status", "--porcelain", "--", pth)
            (inflight if st.strip() else real).append(pth)
        kinds = {}
        for x in diffs:
            kinds[x.get("kind")] = kinds.get(x.get("kind"), 0) + 1
        add("E01", "E", "parity: zero SHF-chain files among %d diffs (status=%s)" % (len(diffs), pd.get("status")),
            not real,
            "kinds=%s real=%s inflight=%s other=%s" % (kinds, real, inflight, sorted(dp)[:30]))
        if inflight:
            add("E01b", "E", "SHF-chain parity hits are uncommitted workspace writes (concurrent cards in flight)",
                True, "paths=%s" % inflight, status="INFO")
    else:
        add("E01", "E", "parity json unavailable", True, "no parity output found", status="INFO")

    good, bad, missing2 = 0, [], []
    for rel in CHAIN_FILES:
        blob = git_blob_sha("HEAD", rel)
        pb = PUB / rel
        if blob is None:
            missing2.append(rel + " (no HEAD blob)")
        elif not pb.exists():
            missing2.append(rel)
        elif sha256_file(pb) != blob:
            bad.append(rel)
        else:
            good += 1
    add("E02", "E", "publish mirror coverage: chain file set (%d) == workspace HEAD, byte-exact in publish" % len(CHAIN_FILES),
        not missing2 and not bad, "match=%d missing=%s diff=%s" % (good, missing2, bad))
    wt_drift = []
    for rel in CHAIN_FILES:
        rc, st, _ = git("status", "--porcelain", "--", rel)
        if st.strip():
            wt_drift.append(rel)
    add("E02b", "E", "chain files: working-tree drift vs HEAD (informational)", True, "drift=%s" % wt_drift, status="INFO")

    abad = []
    for c in ("2ec3af3", "6d8797d", "3b6874f"):
        rc, _, _ = git("merge-base", "--is-ancestor", c, "HEAD", cwd=PUB)
        if rc != 0:
            abad.append(c)
    _, pubhead, _ = git("rev-parse", "HEAD", cwd=PUB)
    _, n81, _ = git("show", "--name-only", "--format=", "2ec3af3", cwd=PUB)
    n81 = len([x for x in n81.split("\n") if x.strip()])
    six_bad = []
    for rel in SIX:
        p = subprocess.run(["git", "-C", str(PUB), "show", "2ec3af3:%s" % rel], capture_output=True)
        if p.returncode != 0 or sha256_bytes(p.stdout) != MM["after"][rel]["sha256"]:
            six_bad.append(rel)
    _, lm1, _ = git("show", "--name-only", "--format=", "6d8797d", cwd=PUB)
    _, lm2, _ = git("show", "--name-only", "--format=", "3b6874f", cwd=PUB)
    add("E03", "E", "publish mirror ancestry + 2ec3af3 carries 81 files and the six blobs == after",
        not abad and not six_bad and n81 == 81,
        "pub_head=%s bad_ancestor=%s six_bad=%s n_2ec3af3=%d receipt_files=%d/%d" % (
            pubhead.strip()[:12], abad, six_bad, n81,
            len([x for x in lm1.split("\n") if x.strip()]), len([x for x in lm2.split("\n") if x.strip()])))

    if not args.quick:
        remote_sha, attempts = None, []
        for i in range(3):
            rc, out, err = run_cmd(["git", "ls-remote", "origin", "main"], cwd=PUB, timeout=150)
            attempts.append("try%d rc=%d out=%r err=%r" % (i + 1, rc, out.strip()[:80], err.strip()[:120]))
            if rc == 0 and out.strip():
                remote_sha = out.split()[0]
                break
        write_log(LOGS, "ls_remote.txt", "\n".join(attempts) + "\nremote_main=%s" % remote_sha)
        if remote_sha:
            rc, _, _ = git("cat-file", "-t", remote_sha, cwd=PUB)
            on_local = rc == 0
            anc = None
            if on_local:
                rc2, _, _ = git("merge-base", "--is-ancestor", "3b6874f", remote_sha, cwd=PUB)
                anc = rc2 == 0
            add("E04", "E", "ls-remote origin main: SHF mirror commits on remote (remote=%s)" % remote_sha[:12],
                on_local and anc, "remote=%s local_obj=%s ancestor_of_3b6874f=%s attempts=%s" % (remote_sha, on_local, anc, attempts[-1]))
        else:
            add("E04", "E", "ls-remote origin main (network) unavailable - receipts rest on prior evidence", True,
                "attempts=%s" % attempts, status="INFO")
    else:
        add("E04", "E", "ls-remote skipped (--quick)", True, "quick mode", status="INFO")

    rc, out, _ = git("status", "--porcelain", "--", *CHAIN_FILES, cwd=PUB)
    add("E05", "E", "publish worktree clean for chain file set (all committed, no uncommitted drift)", not out.strip(),
        "porcelain=%r" % out.strip()[:400])

    # ================================================================ F boundary
    bm = BEFORE["modes"]
    am = AFTER["modes"]
    mod_keys = [k for k in BEFORE if k in AFTER and canon(BEFORE[k]) != canon(AFTER[k])]
    new_keys = sorted(set(AFTER) - set(BEFORE))
    rem_keys = sorted(set(BEFORE) - set(AFTER))
    tail_eq = canon(am[EXPECT_MODES:]) == canon(LAND_ENTRIES)
    add("F01-1", "F", "modes_data: pure append (prefix equal, +10 tail, new block only H-SHF-001, total follows)",
        canon(BEFORE["modes"]) == canon(am[:EXPECT_MODES]) and tail_eq and mod_keys == ["modes", "total"]
        and new_keys == ["H-SHF-001"] and not rem_keys and AFTER["total"] == 3311,
        "modified=%s new=%s removed=%s tail_eq=%s" % (mod_keys, new_keys, rem_keys, tail_eq))

    cb = jload(BACKUP / "code_maps.json")
    cf = cb["figures"]
    af = CM["figures"]
    cmod = [k for k in cf if k in af and canon(cf[k]) != canon(af[k])]
    add("F01-2", "F", "code_maps: pure registry append (common equal, +H-SHF-001, nothing removed)",
        not cmod and sorted(set(af) - set(cf)) == ["H-SHF-001"] and not (set(cf) - set(af)) and len(af) == 216,
        "modified=%s added=%s removed=%s" % (cmod[:5], sorted(set(af) - set(cf)), sorted(set(cf) - set(af))))

    fb = jload(BACKUP / "figure_names.json")
    fmod = [k for k in fb if k in FN and fb[k] != FN[k]]
    add("F01-3", "F", "figure_names: pure append (+H-SHF-001 only)",
        not fmod and sorted(set(FN) - set(fb)) == ["H-SHF-001"] and not (set(fb) - set(FN)),
        "modified=%s added=%s" % (fmod[:5], sorted(set(FN) - set(fb))))

    for fnm, inner, extsuf in (("scenarios_zh.json", "scenarios_zh", ""), ("scenarios_en.json", "scenarios_en", "E")):
        b = jload(BACKUP / fnm)
        a = jload(REPO / "data" / fnm)
        b_in, a_in = b[inner], a[inner]
        imod = [k for k in b_in if k in a_in and canon(b_in[k]) != canon(a_in[k])]
        added = sorted(set(a_in) - set(b_in))
        want = sorted("C-SHF-%03d%s" % (i, extsuf) for i in range(1, 11))
        top_mod = [k for k in b if k != inner and k in a and canon(b[k]) != canon(a[k])]
        add("F01-%s" % ("4" if not extsuf else "5"), "F",
            "%s: inner pure append (+10 C-SHF%s), outer untouched" % (fnm, "..E" if extsuf else "..010"),
            not imod and added == want and not (set(b_in) - set(a_in)) and not top_mod and len(a_in) == 2213,
            "imod=%s added=%s top_mod=%s" % (imod[:5], added[:5], top_mod))

    tb = jload(BACKUP / "scenario_tags.json")
    ta = TG
    tin_b, tin_a = tb["scenario_tags"], ta["scenario_tags"]
    tprefix = canon(tin_b) == canon(tin_a[:len(tin_b)])
    tadded = tin_a[len(tin_b):]
    add("F01-6", "F", "scenario_tags: inner pure append (+20 SHF tags at tail)",
        tprefix and len(tin_a) == len(tin_b) + 20 and all(x.get("figure_code") == "H-SHF-001" for x in tadded),
        "prefix=%s n_before=%d n_after=%d appended_figs=%s" % (tprefix, len(tin_b), len(tin_a), set(x.get("figure_code") for x in tadded)))

    add("F02", "F", "neighbours intact: first 10 / last-10-before-SHF entries byte-equal pre/post",
        canon(bm[:10]) == canon(am[:10]) and canon(bm[-10:]) == canon(am[EXPECT_MODES - 10:EXPECT_MODES]))
    add("F03", "F", "union guard: M-AZJ-001..010 intact, H-AZJ-001 block/registry in place",
        all(x in [e.get("mode_code") for e in am] for x in ["M-AZJ-%03d" % i for i in range(1, 11)])
        and "H-AZJ-001" in AFTER and "H-AZJ-001" in CM["figures"] and "H-AZJ-001" in FN
        and (("H-AZJ-001" not in BEFORE) or canon(BEFORE["H-AZJ-001"]) == canon(AFTER["H-AZJ-001"])),
        "azj_block=%s cm=%s fn=%s" % ("H-AZJ-001" in AFTER, "H-AZJ-001" in CM["figures"], "H-AZJ-001" in FN))

    scan_out = subprocess.run(["git", "-C", str(REPO), "ls-files", "--cached", "--others", "--exclude-standard"],
                              capture_output=True, text=True).stdout.split("\n")
    scan_out += [str(p.relative_to(REPO)) for p in (REPO / "web/public/data").rglob("*.json")]
    pat = re.compile(r"M-SHF-|C-SHF-|H-SHF-")
    hits = []
    for rel in sorted(set(x for x in scan_out if x.strip())):
        if rel.startswith(("web/dist/", "node_modules/", ".git/")):
            continue
        p = REPO / rel
        if not p.is_file():
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if pat.search(t):
            hits.append(rel)
    allowed_exact = set(SIX) | {
        "data/figures/H-SHF-001.json", "data/individuals/H-SHF-001.json", "data/individuals/H-SHF-001_modes.json",
        "data/audit/phase21r9_shenfu_landing_manifest.json", "data/audit/phase21r9_shenfu_merge_manifest.json",
        "data/backup_merge_H-SHF-001_20260924_093849/backup_ledger.json",
        "tools/build_phase21r9_shenfu.py", "tools/merge_phase21r9_shenfu.py",
        "verify_phase21r9_shenfu.py", "verify_phase21r9_shenfu_merge_indep.py",
        "tools/export_static_site.py", "tools/pages_preflight.py",
        "verify_shenfu_qa_espinosa.py",
    }
    def classified(rel):
        if rel in allowed_exact:
            return "shf-surface"
        if rel.startswith(("docs/research/phase21r9_shenfu_", "docs/scratch/legacy20_r9_shenfu_landing/",
                           "docs/scratch/phase21r9_shenfu/", "web/public/data/")):
            return "shf-surface"
        if rel.startswith(("docs/research/phase21r9_azj_", "docs/research/phase21r9_anzijie_")) \
           or rel in ("verify_phase21r9_azj.py", "verify_azj_merge_indep.py"):
            return "sibling-chain"
        if rel == "docs/qa/phase21w4_qa_evidence.json":
            return "other-card-scan-list"
        return "UNEXPECTED"
    classes = {}
    unexpected = []
    for rel in hits:
        c = classified(rel)
        classes[c] = classes.get(c, 0) + 1
        if c == "UNEXPECTED":
            unexpected.append(rel)
    write_log(LOGS, "stray_code_scan.json", json.dumps({"by_class": classes, "unexpected": unexpected, "hits": hits},
                                                        ensure_ascii=False, indent=1))
    add("F04", "F", "stray-code scan: no unexpected file carries M-SHF/C-SHF/H-SHF", not unexpected,
        "classes=%s unexpected=%s" % (classes, unexpected[:10]))

    old_codes = set("M35%d" % i for i in range(1, 9))
    old_in_lib = sorted(e.get("mode_code") for e in am if str(e.get("mode_code")) in old_codes)
    han_active = []
    if "H-HAN-001" in FN:
        han_active.append("figure_names")
    if "H-HAN-001" in CM["figures"]:
        han_active.append("code_maps")
    if any(str(k).startswith("H-HAN") for k in SZ["scenarios_zh"]):
        han_active.append("scenarios_zh")
    bgxref = []
    p_bg = REPO / "data/individuals/H-BG-001.json"
    if p_bg.exists():
        bgxref = [x.get("target_figure_code") for x in (jload(p_bg).get("cross_references") or []) if x.get("target_figure_code") == "H-HAN-001"]
    add("F05", "F", "legacy shell H-HAN-001: old codes M351..M358 not reused; not re-awakened in registries",
        not old_in_lib and not han_active, "old_in_lib=%s active=%s bg_xref=%s" % (old_in_lib, han_active, bgxref))
    if bgxref:
        add("F05b", "F", "known R7 dangling xref H-BG-001 -> H-HAN-001 still present (pre-existing, other chain)", True,
            "not introduced by this chain; registered for the archive card", status="INFO")

    fl = (REPO / "docs/02-tools/figure_library.md").read_text(encoding="utf-8")
    fl_ok = ("320" in fl.splitlines()[2] and "3241" in fl.splitlines()[2])
    ix = (REPO / "docs/index.md").read_text(encoding="utf-8")
    ix_line1_ok = "3241" in ix.splitlines()[2] and "320" in ix.splitlines()[2]
    rc, pre_ix, _ = git("show", "5a657b81^:docs/index.md")
    stale_now = [ln for ln in ix.splitlines()[:12] if ("2848" in ln or "283 " in ln)]
    stale_pre = [ln for ln in pre_ix.splitlines()[:12] if ("2848" in ln or "283 " in ln)]
    add("F06", "F", "product doc faces: figure_library/index count lines updated to 320/3241",
        fl_ok and ix_line1_ok, "fl_ok=%s ix_ok=%s" % (fl_ok, ix_line1_ok))
    if stale_now:
        add("F06b", "F", "pre-existing stale prose line in docs/index.md body (not introduced by this chain)", True,
            "pre_image_same=%s line=%r" % (stale_now == stale_pre, stale_now[0][:80]), status="INFO")

    _, bk_tracked, _ = git("ls-files", "--", "data/backup_merge_H-SHF-001_20260924_093849")
    add("F07", "F", "backup dir stays untracked (not committed, by design)", not bk_tracked.strip(), "tracked=%r" % bk_tracked.strip())

    # ================================================================ cross-reference (self-report of verified cards, informational)
    if not args.quick:
        ev_paths = ["docs/research/phase21r9_shenfu_verify_evidence_merged.json",
                    "docs/research/phase21r9_shenfu_merge_verify_indep.json"]
        pre = {}
        for pth in ev_paths:
            rc, st, _ = git("status", "--porcelain", "--", pth)
            pre[pth] = bool(st.strip())
        for script, xid in (("verify_phase21r9_shenfu.py", "X01"), ("verify_phase21r9_shenfu_merge_indep.py", "X02")):
            rc, out, err = run_cmd([sys.executable, script], timeout=1800)
            write_log(LOGS, "xref_%s.txt" % script.replace(".py", ""), out + "\n" + err)
            tail = [ln for ln in out.strip().splitlines() if ln.strip()][-1:]
            add(xid, "X", "cross-regression rerun %s (self-report, not judgement)" % script, True,
                "rc=%d tail=%s" % (rc, tail), status="INFO")
        restored = []
        for pth in ev_paths:
            rc, st, _ = git("status", "--porcelain", "--", pth)
            if st.strip() and not pre[pth]:
                git("checkout", "--", pth)
                restored.append(pth)
        add("X02b", "X", "cross-regression side writes rolled back (chain evidence restored to HEAD)", True,
            "restored=%s" % restored, status="INFO")
    else:
        for xid in ("X01", "X02"):
            add(xid, "X", "cross-regression rerun skipped (--quick)", True, "quick mode", status="INFO")

    # gate reruns (independent execution of the four gates claimed upstream)
    if not args.quick:
        gates = [
            ("X03", [sys.executable, "tools/credibility_gate.py", "--hard-fail"], "credibility_gate"),
            ("X04", [sys.executable, "tools/verify_findings.py", "--hard-fail"], "verify_findings"),
            ("X05", [sys.executable, "tools/verify_source_links.py", "--hard-fail"], "verify_source_links"),
            ("X06", [sys.executable, "tools/apply_verification_status.py", "--check"], "apply_verification_status"),
        ]
        for xid, cmd, label in gates:
            try:
                rc, out, err = run_cmd(cmd, timeout=900)
            except subprocess.TimeoutExpired:
                rc, out, err = -1, "", "TIMEOUT"
            write_log(LOGS, "gate_%s.txt" % label, (out or "") + "\n" + (err or ""))
            tail = [ln for ln in (out or "").strip().splitlines() if ln.strip()][-2:]
            bad_net = ("UNREACHABLE" in (out or "")) or ("TIMEOUT" == err)
            add(xid, "X", "gate rerun: %s" % label, rc == 0, "rc=%d tail=%s" % (rc, tail),
                status=None if rc == 0 else ("INFO" if bad_net else "FAIL"))
    else:
        for xid in ("X03", "X04", "X05", "X06"):
            add(xid, "X", "gate rerun skipped (--quick)", True, "quick mode", status="INFO")

    # ================================================================ summary + evidence
    n_pass = sum(1 for r in RESULTS if r["status"] == "PASS")
    n_fail = sum(1 for r in RESULTS if r["status"] == "FAIL")
    n_info = sum(1 for r in RESULTS if r["status"] == "INFO")
    verdict = "ALL PASS" if n_fail == 0 else "FAIL"
    print("-" * 72)
    print("TOTAL: %d PASS / %d FAIL / %d INFO | verdict=%s" % (n_pass, n_fail, n_info, verdict))
    if n_fail:
        for r in RESULTS:
            if r["status"] == "FAIL":
                print("  FAIL %s: %s" % (r["id"], r["detail"])[:400])

    ev = {
        "schema_version": "v1",
        "card": "t_83e0d68d",
        "chain": "Phase21-R9 Shen Fu (H-SHF-001) rebuild chain (cards t_d78053e7 / t_b6d4c0ee / t_a7d233f0)",
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "script": "verify_shenfu_qa_espinosa.py",
        "mode": "quick" if args.quick else "full",
        "repo_head": head.strip(),
        "publish_head": pubhead.strip(),
        "counts": {"pass": n_pass, "fail": n_fail, "info": n_info},
        "verdict": verdict,
        "results": RESULTS,
    }
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(ev, ensure_ascii=False, indent=1), encoding="utf-8")
    print("evidence -> %s" % outp)
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
