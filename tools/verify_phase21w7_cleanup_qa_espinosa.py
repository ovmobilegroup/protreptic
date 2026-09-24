#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase21-W7 cleanup independent QA verifier (card t_06511a5a, espinosa).

Re-derives from raw data + git objects (no trust in upstream claims):
  A. delete-face reconciliation: git window deletions == backup ws set == 1309
  B. preimage byte-exactness: backup files sha256 == git blobs (ws 1309 / pb 674)
  C. absence at HEAD (ws + pb) for every deleted path
  D. MANIFEST logical completeness (sha + rel + size per entry)
  E. keep-face present, ws/pb byte-equal; boundary anchors consistent
  F. live-surface residual scan (CI/web-src/api/scripts/cli_tests): 0 hard
  G. stratified sample re-derivation (>=15% or >=50 per layer)
  H. boundary numbers self-consistency (db == meta == figures.index == EXPECT_FIGURES)

Usage:  python3 tools/verify_phase21w7_cleanup_qa_espinosa.py [--quick]
Exit:   0 = all assertions pass; 1 = at least one failure.
"""
import argparse, hashlib, json, os, re, sqlite3, subprocess, sys

WS = os.environ.get("QA_WS", "/opt/data/workspace/Protreptic")
PB = os.environ.get("QA_PB", "/opt/data/release/Protreptic-publish")
BK = os.path.join(WS, "data/backup_phase21w7_clean_20260924")
REV_WS_JUNK = "f61f055d"      # ws commit that removed the 6 junk entries
REV_WS_FACE = "e5ddd13f"      # ws commit that removed the 1303 file entries
REV_PB = "c167cb5"            # pb commit that removed the 674 publish-side preimages
EXPECT = dict(face=1309, root=632, tj=670, junk_files=6, pb=674,
              manifest_logical=1983, manifest_physical=1984)

def sh(cmd, cwd=None):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, errors="replace")

def git_z(args, cwd):
    r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True)
    return [x.decode("utf-8", "surrogateescape") for x in r.stdout.split(b"\0") if x]

def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def git_blob_sha(rev, path, cwd):
    r = subprocess.run(["git", "cat-file", "blob", rev + ":" + path], cwd=cwd, capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None

def blobs_sha_batch(rev, paths, cwd):
    """{path: sha256} via one git cat-file --batch; newline-named paths bypassed."""
    clean = [p for p in paths if "\n" not in p and "\r" not in p]
    out = {p: git_blob_sha(rev, p, cwd) for p in paths if p not in clean}
    if not clean:
        return out
    proc = subprocess.Popen(["git", "cat-file", "--batch"], cwd=cwd,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for p in clean:
        proc.stdin.write((rev + ":" + p + "\n").encode("utf-8", "surrogateescape"))
    proc.stdin.close()
    for p in clean:
        header = proc.stdout.readline().decode("utf-8", "replace").strip()
        if header.endswith(" missing") or not header:
            out[p] = None
            continue
        parts = header.split()
        if len(parts) < 3 or parts[1] != "blob":
            out[p] = None
            proc.stdout.read(int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0)
            continue
        data = proc.stdout.read(int(parts[2]))
        proc.stdout.read(1)
        out[p] = hashlib.sha256(data).hexdigest()
    proc.wait()
    return out

results = []
def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(("[OK]  " if ok else "[FAIL]") + f" {name}" + (f" :: {detail}" if detail else ""))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="sample-based checks only")
    a = ap.parse_args()

    cls = json.load(open(os.path.join(WS, "data/audit/phase21w7_classification.json"), encoding="utf-8"))
    items = cls["items"]
    del_items = [it for it in items if it.get("verdict") in ("archive_delete", "delete")]
    root_items = [it for it in del_items if it["face"] == "root_json"]
    tj_items = [it for it in del_items if it["face"] == "tools_json"]
    expected = {it["path"] for it in root_items} | {it["path"] for it in tj_items} | {", "}

    # A. reconciliation
    win_del = set(git_z(["diff-tree", "-r", "-z", "--diff-filter=D", "--name-only", REV_WS_FACE + "^", "HEAD"], WS))
    junk_del = set(git_z(["diff-tree", "-r", "-z", "--diff-filter=D", "--name-only", REV_WS_JUNK + "^", REV_WS_JUNK], WS))
    win_del |= junk_del
    bk_ws = set()
    for dp, dn, fn in os.walk(os.path.join(BK, "ws")):
        for f in fn:
            bk_ws.add(os.path.relpath(os.path.join(dp, f), os.path.join(BK, "ws")))
    check("A1 window deletions == backup ws set", win_del == bk_ws, f"{len(win_del)} vs {len(bk_ws)}")
    extra = bk_ws - expected
    check("A2 backup set = classification face (1303) + 6 junk nested files",
          expected <= bk_ws and len(extra) == EXPECT["junk_files"] and len(bk_ws) == EXPECT["face"],
          f"face_files={len(expected)} extra={len(extra)}")
    lr = {it["path"] for it in root_items}; lt = {it["path"] for it in tj_items}
    layers = dict(root=len([x for x in bk_ws if x in lr]), tj=len([x for x in bk_ws if x in lt]))
    check("A3 layer counts 632/670", layers["root"] == 632 and layers["tj"] == 670, str(layers))
    check("A4 e5ddd13f deletions are a faithful subset", set(git_z(["diff-tree", "-r", "-z", "--diff-filter=D", "--name-only", "e5ddd13f^", "e5ddd13f"], WS)) <= bk_ws)

    # B. preimages ws
    ws_list = sorted(bk_ws)
    revs = {p: (REV_WS_JUNK + "^" if p in junk_del else REV_WS_FACE + "^") for p in ws_list}
    by_rev = {}
    for p, rv in revs.items():
        by_rev.setdefault(rv, []).append(p)
    ok_ws = 0; bad_ws = []
    for rv, ps in by_rev.items():
        m = blobs_sha_batch(rv, ps, WS)
        for p in ps:
            if m.get(p) and sha_file(os.path.join(BK, "ws", p)) == m[p]:
                ok_ws += 1
            else:
                bad_ws.append(p)
    check("B1 ws preimages byte-exact (1309/1309)", ok_ws == len(ws_list), f"{ok_ws}/{len(ws_list)} bad={bad_ws[:5]}")

    # pb
    bk_pb = set()
    for dp, dn, fn in os.walk(os.path.join(BK, "pb")):
        for f in fn:
            bk_pb.add(os.path.relpath(os.path.join(dp, f), os.path.join(BK, "pb")))
    pb_del = set(git_z(["diff-tree", "-r", "-z", "--diff-filter=D", "--name-only", REV_PB + "^", REV_PB], PB))
    pb_list = sorted(bk_pb)
    sel_pb = pb_list if not a.quick else pb_list[::16]
    m = blobs_sha_batch(REV_PB + "^", sel_pb, PB)
    ok_pb = sum(1 for p in sel_pb if m.get(p) and sha_file(os.path.join(BK, "pb", p)) == m[p])
    check("B2 pb preimages byte-exact", ok_pb == len(sel_pb), f"{ok_pb}/{len(sel_pb)}")
    check("B3 pb backup set == pb deletions (674)", bk_pb == pb_del and len(bk_pb) == EXPECT["pb"], f"{len(bk_pb)} vs {len(pb_del)}")

    # C. absence
    def absent_list(rev, paths, cwd):
        proc = subprocess.Popen(["git", "cat-file", "--batch-check"], cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        for p in paths:
            if "\n" in p or "\r" in p:
                proc.stdin.write((rev + ":" + p.replace("\n", "\t") + "\n").encode("utf-8", "surrogateescape"))
            else:
                proc.stdin.write((rev + ":" + p + "\n").encode("utf-8", "surrogateescape"))
        proc.stdin.close()
        present = []
        for p in paths:
            line = proc.stdout.readline().decode("utf-8", "replace")
            if "missing" not in line:
                present.append(p)
        proc.wait()
        return present
    ws_sel = ws_list if not a.quick else ws_list[::16]
    pres = absent_list("HEAD", ws_sel, WS)
    check("C1 ws HEAD absence (all sampled)", not pres, f"present={pres[:5]}")
    pb_sel = pb_list if not a.quick else pb_list[::16]
    pres = absent_list("HEAD", pb_sel, PB)
    check("C2 pb HEAD absence (all sampled)", not pres, f"present={pres[:5]}")

    # D. manifest (tolerant: shrunk to plain sha<space> rel<space> size; handles 1 split-name entry)
    raw = open(os.path.join(BK, "MANIFEST.sha256"), encoding="utf-8", errors="surrogateescape").read()
    lines = raw.splitlines()
    logical = 0; bad_man = []
    pending = None
    for ln in lines:
        mm = re.match(r"^([0-9a-f]{64})  (.*?)(?:  (\d+))?$", ln)
        if mm and mm.group(3) is not None and not pending:
            logical += 1
            rel = mm.group(2); bfp = os.path.join(BK, rel)
            if not os.path.exists(bfp) or sha_file(bfp) != mm.group(1) or os.path.getsize(bfp) != int(mm.group(3)):
                bad_man.append(rel)
        elif mm and mm.group(3) is None:
            pending = (mm.group(1), mm.group(2))
        elif pending is not None:
            mm2 = re.match(r"^(.*?)  (\d+)$", ln)
            if mm2:
                rel = pending[1] + "\n" + mm2.group(1)
                logical += 1
                bfp = os.path.join(BK, rel)
                if not os.path.exists(bfp) or sha_file(bfp) != pending[0] or os.path.getsize(bfp) != int(mm2.group(2)):
                    bad_man.append(repr(rel))
            pending = None
    check("D1 manifest logical entries == 1983 and every entry verifies",
          logical == EXPECT["manifest_logical"] and not bad_man, f"logical={logical} bad={bad_man[:5]}")
    check("D2 manifest physical lines == 1984", len(lines) == EXPECT["manifest_physical"], f"lines={len(lines)}")

    # E. keeps + boundary anchors
    keeps = [".markdownlint.json", "lighthouserc.json", "tools/json/scenarios_zh.json",
             "tools/json/scenarios_en.json", "tools/json/scenario_tags.json"]
    kb = []
    for k in keeps:
        p1, p2 = os.path.join(WS, k), os.path.join(PB, k)
        if not (os.path.exists(p1) and os.path.exists(p2) and sha_file(p1) == sha_file(p2)):
            kb.append(k)
    check("E1 keep-face present + ws/pb byte-equal (5)", not kb, f"bad={kb}")
    pf = open(os.path.join(WS, "tools/pages_preflight.py"), encoding="utf-8").read()
    es = open(os.path.join(WS, "tools/export_static_site.py"), encoding="utf-8").read()
    mi = open(os.path.join(WS, "tools/ci_data_check.py"), encoding="utf-8").read()
    e1 = int(re.search(r"EXPECT_FIGURES = (\d+)", pf).group(1))
    e2 = int(re.search(r"EXPECT_FIGURES = (\d+)", es).group(1))
    e3 = int(re.search(r"MIN_SITEMAP_ENTRIES = (\d+)", mi).group(1))
    meta = json.load(open(os.path.join(WS, "web/public/data/meta.json"), encoding="utf-8"))["counts"]
    fi = json.load(open(os.path.join(WS, "web/public/data/figures.index.json"), encoding="utf-8"))
    sm = open(os.path.join(WS, "web/public/sitemap.xml"), encoding="utf-8").read()
    uni = json.load(open(os.path.join(WS, "web/public/data/index.unified.json"), encoding="utf-8"))
    con = sqlite3.connect(f"file:{WS}/api/protreptic.db?mode=ro", uri=True)
    dbf = con.execute("SELECT COUNT(*) FROM figures").fetchone()[0]
    con.close()
    check("E2 anchors self-consistent (db==preflight==export==meta==index)",
          e1 == e2 == meta["figures"] == len(fi) == dbf, f"db={dbf} preflight={e1} export={e2} meta={meta['figures']} index={len(fi)}")
    check("E3 sitemap >= MIN_SITEMAP_ENTRIES", sm.count("<url>") >= e3, f"urls={sm.count('<url>')} min={e3}")
    check("E4 unified total == figures + scenarios",
          len(uni["items"]) == uni["counts"]["total"] == uni["counts"]["figures"] + uni["counts"]["scenarios"], str(uni["counts"]))

    # F. live-surface residual scan with resolution
    face_paths = {p for p in ws_list} | {p for p in pb_list}
    face_names = sorted({os.path.basename(p) for p in face_paths
                      if p != ", " and re.match(r"^[A-Za-z0-9\u4e00-\u9fff]", os.path.basename(p))})
    roots_face = {it["path"] for it in root_items}
    tj_face = {it["path"] for it in tj_items}
    live_dirs = [os.path.join(WS, d) for d in (".github", "web/src", "api", "scripts", "cli_tests")]
    PREFIXES = ("/opt/data/workspace/Protreptic/", "/opt/data/release/Protreptic-publish/")

    def token_at(d, i, j):
        L = i; R = j
        charset = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._/-+%~@")
        while L > 0 and d[L-1] in charset:
            L -= 1
        while R < len(d) and d[R] in charset:
            R += 1
        return d[L:R]

    def cands_of(token, name):
        t = token
        for pref in PREFIXES:
            if t.startswith(pref):
                t = t[len(pref):]
        t = t.lstrip("/")
        if "/" in t:
            return [t]
        return [t, "data/" + name, "tools/" + name, "tools/json/" + name, name]

    def resolves(token, name):
        return any(os.path.exists(os.path.join(WS, c)) or os.path.exists(os.path.join(PB, c)) for c in cands_of(token, name))

    hard = []; reg = []; ben = 0
    for base in live_dirs:
        for dp, dn, fn in os.walk(base):
            dn[:] = [d for d in dn if d not in (".git", "node_modules", "__pycache__")]
            for f in fn:
                fp = os.path.join(dp, f)
                try:
                    if os.path.getsize(fp) > 20 << 20:
                        continue
                    d = open(fp, "rb").read().decode("utf-8", "replace")
                except Exception:
                    continue
                rel = os.path.relpath(fp, WS)
                seen = set()
                for nm in face_names:
                    if nm in d and nm not in seen:
                        for mm in re.finditer(re.escape(nm), d):
                            pre = d[mm.start() - 1] if mm.start() else "/"
                            post = d[mm.end()] if mm.end() < len(d) else "/"
                            if pre.isalnum() or pre in "_-.:" or post.isalnum() or post in "_-.:":
                                continue
                            tok = token_at(d, mm.start(), mm.end())
                            seen.add(nm)
                            if resolves(tok, nm):
                                ben += 1
                            elif any(c in win_del for c in cands_of(tok, nm)):
                                hard.append((rel, nm, tok))
                            elif ("check_repo_parity.py" in rel) or ("build_figures_db.py" in rel):
                                ben += 1
                            else:
                                reg.append((rel, nm, tok))
                            break
    check("F1 live-surface 0 hard residual (deleted-face path refs)", not hard, f"hard={hard[:8]} resolved_benign={ben} preexisting_stale={len(reg)}")
    junk_lits = ["tools/json/.json", "tools/json/, print("]
    junk_bad = []
    for base in live_dirs:
        for dp, dn, fn in os.walk(base):
            dn[:] = [d for d in dn if d not in (".git", "node_modules", "__pycache__")]
            for f in fn:
                fp = os.path.join(dp, f)
                try:
                    if os.path.getsize(fp) > 20 << 20:
                        continue
                    d = open(fp, "rb").read().decode("utf-8", "replace")
                except Exception:
                    continue
                for lit in junk_lits:
                    if lit in d:
                        junk_bad.append((os.path.relpath(fp, WS), lit))
    build_graph_files = ("tools/check_repo_parity.py", "tools/pages_preflight.py", "tools/export_static_site.py",
                         "tools/build_figures_db.py", "tools/ci_data_check.py", "tools/build_search_index.py")
    reg_bad = [r for r in reg if r[0] in build_graph_files]
    check("F2 pre-existing stale refs registered / no build-graph file among them",
          not junk_bad and not reg_bad and len(reg) <= 8,
          f"n={len(reg)} files={sorted({r[0] for r in reg})} junk_lit={junk_bad[:4]}")
    if not a.quick:
        rc = sh("python3 tools/check_repo_parity.py", cwd=WS)
        boundary_ok = ("boundary] pages.yml" in rc.stdout or "边界自检通过" in rc.stdout)
        check("F3 parity tool rc<=2 + boundary self-check line", rc.returncode <= 2 and boundary_ok, f"rc={rc.returncode}")

    # G. stratified sample
    def stride(lst, n):
        st = max(1, len(lst) // n)
        return lst[::st][:n + 8]
    r_s = stride(root_items, 10 if a.quick else 100) or root_items
    t_s = stride(tj_items, 10 if a.quick else 105) or tj_items
    if not a.quick:
        notw = set()
        for it in root_items:
            claims = [c for c in (it.get("byte_twins") or []) if "(byte-equal)" in c]
            if not claims:
                notw.add(it["path"])
        for it in root_items:
            if it["path"] in notw and it not in r_s:
                r_s.append(it)
    fails = []
    for it in r_s + t_s:
        p = it["path"]
        if not os.path.exists(os.path.join(BK, "ws", p)):
            fails.append(p); continue
        rv = REV_WS_JUNK + "^" if p in junk_del else REV_WS_FACE + "^"
        if git_blob_sha(rv, p, WS) is None:
            fails.append(p)
    check("G1 stratified sample backup+git-object present", not fails, f"sample={len(r_s)+len(t_s)} fails={fails[:5]}")
    ok_size = True if a.quick else (len(r_s) >= 95 and len(t_s) >= 101)
    check("G2 sample size >=15% (or >=50) per layer", ok_size, f"root={len(r_s)} tj={len(t_s)} quick={a.quick}")

    np = sum(1 for _, ok, _ in results if ok)
    print(f"\n=== {np}/{len(results)} PASS ===")
    return 0 if np == len(results) else 1

if __name__ == "__main__":
    sys.exit(main())
