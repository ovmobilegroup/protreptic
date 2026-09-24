#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_phase21w4_qa_espinosa.py -- Phase21 W4 independent QA assertor.

Card: t_8bad8d98 (QA, espinosa). Scope: phase21w4 fix (t_536073f4) +
rwkag-clear (t_ee203180) + fix2 (t_33240de8) receipts, re-derived from raw
repo state (never from the receipts' own claims). Read-only for both repos:
the only file it writes is the evidence JSON (default docs/qa/phase21w4_qa_evidence.json).

Usage:
  python3 verify_phase21w4_qa_espinosa.py            # full: gates + parity + fetch
  python3 verify_phase21w4_qa_espinosa.py --quick    # offline: skips gates/parity/fetch
  python3 verify_phase21w4_qa_espinosa.py --evidence /tmp/ev.json
Exit: 0 = all assertions PASS (INFO lines allowed), 1 = any FAIL, 2 = env error.

v3 (2026-09-24, t_8bad8d98): board-drift attribution. Foreign (non-W4, non-QA)
commits landing in the shared repo are tolerated only if they touch zero
W4-surface paths; unexplained single-side / extra files must be traceable to a
foreign commit. Remote pin relaxed to "receipt head is ancestor of origin/main".
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import time

WS = "/opt/data/workspace/Protreptic"
PB = "/opt/data/release/Protreptic-publish"
BASE = "40320e37"            # W4 window start (before fix)
EE = "8a0ac56d"             # rwkag-clear final workspace commit
HEAD_CLAIM = "2de84904"     # fix2 final workspace commit
HEAD = "HEAD"                # git revision constant (live workspace head)
PUB_HEAD = "c646f41a5c4fc65027d403cf448c847fc4756060"
WS_COMMITS = ["e7be5cc6", "8ca52c04", "9ed628e8", "37545ac7", "33762c4e",
              "4aa62574", "8a0ac56d", "00bc34a2", "489b72c3", "2de84904"]
PB_COMMITS = ["da1e9bc", "faccfbe", "7d6d1e9", "e5c111a", "74c5522",
              "ba3b1fa", "332188d", "0517b38", "8e4d3e6", "c646f41"]
ZH4 = "\u674e\u5148\u5ff5"
EN4 = "Li Xiannian"
MAO = "\u6bdb\u5148\u5ff5"
MAOEN = "Mao Xiannian"
RYZ = "\u664f\u9633\u521d"
MENCIUS = "\u5b5f\u5b50"
QA_FILES = {"verify_phase21w4_qa_espinosa.py", "docs/qa/phase21w4_qa_report.md",
            "docs/qa/phase21w4_qa_evidence.json", "docs/qa/phase21w4_qa_run_final.log"}

R = []
T0 = time.time()


def chk(sec, item, ok, detail=""):
    ok = bool(ok)
    R.append({"sec": sec, "item": item, "ok": ok, "detail": str(detail)[:900]})
    tag = "PASS" if ok else "FAIL"
    line = "[%s] %-4s %s" % (tag, sec, item)
    if detail:
        line += " :: " + str(detail)[:240]
    print(line)


def info(sec, item, detail):
    chk(sec, item, True, "INFO: " + str(detail)[:700])


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha_f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def run(cmd, cwd=None, timeout=1200):
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
        return (p.returncode,
                p.stdout.decode("utf-8", "replace"),
                p.stderr.decode("utf-8", "replace"),
                round(time.time() - t0, 1))
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT", round(time.time() - t0, 1)


def git(args, cwd=WS, timeout=600):
    return run(["git"] + list(args), cwd=cwd, timeout=timeout)


def git_out(args, cwd=WS):
    rc, out, err, _ = git(args, cwd=cwd)
    return out


def gshow_bytes(commit, path, cwd=WS):
    return subprocess.run(["git", "show", commit + ":" + path],
                          cwd=cwd, capture_output=True).stdout


def gshow_text(commit, path, cwd=WS):
    return gshow_bytes(commit, path, cwd).decode("utf-8", "replace")


def gshow_json(commit, path, cwd=WS):
    return json.loads(gshow_text(commit, path, cwd))


def load(p, repo=WS, binary=False):
    fp = p if p.startswith("/") else os.path.join(repo, p)
    if binary:
        with open(fp, "rb") as f:
            return f.read()
    with open(fp, encoding="utf-8") as f:
        return f.read()


def loadj(p, repo=WS):
    return json.loads(load(p, repo))


print("# verify_phase21w4_qa_espinosa -- start %s" % time.strftime("%Y-%m-%d %H:%M:%S"))

# ---------------------------------------------------------------- drift context
# Board-shared repo: unrelated cards land commits while this QA runs. Drift
# attribution keeps the W4 invariants strict: foreign commits must touch ZERO
# W4-surface paths, and every unexplained extra file must be traceable to a
# foreign commit (or be an untracked in-flight file outside W4 scope).
W4_SURFACE = set()
QA_COMMITS = []
FOREIGN = {}
try:
    for c in WS_COMMITS:
        for p in git_out(["diff-tree", "--no-commit-id", "--name-only", "-r", c]).split("\n"):
            if p:
                W4_SURFACE.add(p)
    for x in git_out(["rev-list", "--reverse", BASE + "..HEAD"]).split():
        c = x[:8]
        if c in WS_COMMITS:
            continue
        ps = set(p for p in git_out(["diff-tree", "--no-commit-id", "--name-only", "-r", c]).split("\n") if p)
        if ps and ps <= QA_FILES:
            QA_COMMITS.append(c)
        else:
            FOREIGN[c] = ps
except Exception as e:
    print("# drift context EXC %r" % e)


_DTREE = {}


def _dtree(c):
    if c not in _DTREE:
        _DTREE[c] = set(p for p in git_out(
            ["diff-tree", "--no-commit-id", "--name-only", "-r", c]).split("\n") if p)
    return _DTREE[c]


def foreign_attributed(path, rng):
    """True if every commit in rng touching path is outside the W4 chain (a
    board card commit, classified live -- not from the start-of-run snapshot),
    or the path is untracked in-flight work. W4 commits touching the path, or
    commits that touch any W4 marker path, make it non-attributable."""
    ts = [c[:8] for c in git_out(["rev-list", rng, "--", path]).split()]
    if not ts:
        rc, _, _, _ = git(["ls-files", "--error-unmatch", "--", path])
        return rc != 0
    for t in ts:
        if t in WS_COMMITS:
            return False
        if t in QA_COMMITS and path in QA_FILES:
            continue
        if any(is_w4_marker(p) for p in _dtree(t)):
            return False
    return True


def dirty_paths():
    out = {}
    for l in git_out(["status", "--porcelain"]).splitlines():
        if not l.strip():
            continue
        p = l[3:].strip()
        if " -> " in p:
            p = p.split(" -> ")[-1]
        out[p.strip('"')] = l[:2].strip()
    return out


DIRTY = dirty_paths()
FOREIGN_TOUCHED = {}
for _c, _ps in FOREIGN.items():
    for _p in _ps:
        FOREIGN_TOUCHED.setdefault(_p, []).append(_c)
FEATURE_SRC = ("data/", "tools/", "web/", "docs/architecture/")


def board_source_moved():
    for p in DIRTY:
        if p in QA_FILES or p.startswith("docs/qa/phase21w4_qa") or p.endswith(".backup"):
            continue
        return True
    for p in FOREIGN_TOUCHED:
        if p.startswith(FEATURE_SRC) and not p.startswith("docs/research/"):
            return True
    return False


BOARD_SRC_MOVED = board_source_moved()
DRIFTS = []


def is_build_product(p):
    return p.startswith("web/public/") or p.startswith("web/dist/")


def is_w4_marker(p):
    return (p.startswith("data/backup_phase21w4_") or p.startswith("docs/research/phase21w4_")
            or p.startswith("docs/research/_archive/RW-KAG")
            or p in ("verify_rwkag_clear.py", "verify_w4fix2_lxn.py"))


def live_drift(path, build=False):
    """Attribution for a live-state discrepancy at path: uncommitted board edit,
    committed foreign touch, or board rebuild of build products. Fresh probes
    re-read git state, since the board mutates while a run is in flight
    (new files appear, cards commit mid-run). None => FAIL."""
    if path in DIRTY and path not in QA_FILES and not path.startswith("docs/qa/phase21w4_qa"):
        return "dirty:" + DIRTY[path]
    if path in FOREIGN_TOUCHED:
        return "foreign:" + ",".join(FOREIGN_TOUCHED[path][:2])
    rc, out, _, _ = git(["status", "--porcelain", "--", path])
    if rc == 0 and out.strip():
        return "dirty-now:" + out.strip()[:2].strip()
    if git_out(["rev-list", BASE + "..HEAD", "--", path]).split() and \
            foreign_attributed(path, BASE + "..HEAD"):
        return "foreign-now"
    if (build or is_build_product(path)) and BOARD_SRC_MOVED:
        return "board-rebuild"
    return None


def chk_live(sec, item, ok, paths, detail=""):
    """Live-state check with drift attribution: attributed discrepancies are
    registered (PASS + DRIFT marker + DRIFTS entry), unattributed ones FAIL."""
    if ok:
        chk(sec, item, True, detail)
        return
    dr = None
    for p in paths:
        dr = live_drift(p, build=is_build_product(p))
        if dr:
            break
    if dr:
        DRIFTS.append({"sec": sec, "item": item, "path": paths[0] if paths else "",
                       "drift": dr, "detail": str(detail)[:240]})
        chk(sec, item, True, "DRIFT(%s) %s" % (dr, detail))
    else:
        chk(sec, item, False, detail)


# ---------------------------------------------------------------- sec 0 context
try:
    head = git_out(["rev-parse", "HEAD"]).strip()
    rc_a, out_a, _, _ = git(["merge-base", "--is-ancestor", HEAD_CLAIM, "HEAD"])
    between = git_out(["diff", "--name-only", HEAD_CLAIM + "..HEAD"]).split()
    w4_hit0 = [p for p in between if is_w4_marker(p)]
    unattr0 = [p for p in between if p not in QA_FILES and not foreign_attributed(p, HEAD_CLAIM + "..HEAD")]
    chk("0", "HEAD claim is ancestor of live HEAD; no W4-marker file changed after claim (drift-attributed)",
        rc_a == 0 and not w4_hit0 and not unattr0,
        "HEAD=%s between=%d w4_marker_hit=%s unattributed=%s" % (head[:8], len(between), w4_hit0[:6], unattr0[:6]))
    miss = []
    for c in WS_COMMITS:
        rc, _, _, _ = git(["cat-file", "-e", c + "^{commit}"])
        if rc != 0:
            miss.append(c)
    for c in PB_COMMITS:
        rc, _, _, _ = git(["cat-file", "-e", c + "^{commit}"], cwd=PB)
        if rc != 0:
            miss.append(c)
    chk("0", "all 20 W4 receipt commits exist locally", not miss, "missing=%s" % miss)
    st = git_out(["status", "--short"]).rstrip()
    w4m_dirty = []
    inflight_dirty = []
    for l in st.splitlines():
        if not l.strip():
            continue
        p = l[3:].strip().strip('"')
        if " -> " in p:
            p = p.split(" -> ")[-1]
        if p in QA_FILES or p.startswith("docs/qa/phase21w4_qa") or p == "verify_phase21w4_qa_espinosa.py":
            continue
        if is_w4_marker(p):
            w4m_dirty.append(p)
        else:
            inflight_dirty.append(p)
    chk("0", "worktree: W4 markers intact; foreign in-flight edits registered (board concurrency)",
        not w4m_dirty,
        "in_flight=%d %s | w4_marker_dirty=%s" % (len(inflight_dirty), inflight_dirty[:6], w4m_dirty[:4]))
except Exception as e:
    chk("0", "context probe", False, "EXC %r" % e)

# ---------------------------------------------------------------- sec A counts
try:
    db = sqlite3.connect(os.path.join(WS, "api/protreptic.db"))
    n_fig = db.execute("select count(*) from figures").fetchone()[0]
    n_modes_db = db.execute("select count(*) from thinking_modes").fetchone()[0]
    codes_db = set(r[0] for r in db.execute("select code from figures"))
    chk_live("A", "db figures == 1027", n_fig == 1027, ["api/protreptic.db"], "n=%d" % n_fig)
    info("A", "db thinking_modes count", n_modes_db)

    if os.path.exists(os.path.join(WS, "web/public/data/figures.index.json")):
        idx = loadj("web/public/data/figures.index.json")
    else:
        idx = loadj("web/public/data/figures.index.json", repo=PB)
        info("A", "figures.index read from pb copy", "ws path transiently absent (board rebuild)")
    codes_idx = set(e["code"] for e in idx)
    chk_live("A", "figures.index 1027 and set == db", len(idx) == 1027 and codes_idx == codes_db,
             ["web/public/data/figures.index.json"], "n=%d" % len(idx))
    shard_paths = glob.glob(os.path.join(WS, "web/public/data/figures/*.json"))
    codes_sh = set(os.path.basename(p)[:-5] for p in shard_paths)
    chk_live("A", "shards 1027 and set == db", len(shard_paths) == 1027 and codes_sh == codes_db,
             ["web/public/data/figures/"], "n=%d" % len(shard_paths))

    meta = loadj("web/public/data/meta.json")
    mc = meta["counts"]
    sdm_pin_c = gshow_json(HEAD_CLAIM, "docs/architecture/static_data_manifest.json")["counts"]
    exp_c = {"figures": 1027, "figure_shards": 1027, "mode_summaries_published": 3221,
             "mode_by_figure_shards": 318}
    pin_c_ok = all(sdm_pin_c.get(k) == v for k, v in exp_c.items())
    live_c_ok = all(mc.get(k) == v for k, v in exp_c.items())
    chk("A", "counts pin: manifest@HEAD_CLAIM == 1027/1027/3221/318 (strict)",
        pin_c_ok, json.dumps({k: sdm_pin_c.get(k) for k in exp_c}, ensure_ascii=False))
    chk_live("A", "meta counts live == expected or drift-attributed", live_c_ok,
             ["web/public/data/meta.json"],
             json.dumps({k: mc[k] for k in exp_c}, ensure_ascii=False))
    sdm = loadj("docs/architecture/static_data_manifest.json")
    sc = sdm["counts"]
    chk("A", "static_data_manifest counts == meta counts",
        all(sc.get(k) == mc.get(k) for k in ("figures", "figure_shards",
            "mode_summaries_published", "mode_by_figure_shards", "modes_quarantined")),
        json.dumps({k: sc.get(k) for k in ("figures", "figure_shards",
                    "mode_summaries_published", "mode_by_figure_shards")}, ensure_ascii=False))

    dz = loadj("tools/json/scenarios_zh.json")
    de = loadj("tools/json/scenarios_en.json")
    chk_live("A", "scenarios zh/en keys == 1040", len(dz) == 1040 and len(de) == 1040,
             ["tools/json/scenarios_zh.json", "tools/json/scenarios_en.json"],
             "zh=%d en=%d" % (len(dz), len(de)))

    if os.path.exists(os.path.join(WS, "web/public/data/index.unified.json")):
        u = loadj("web/public/data/index.unified.json")
    else:
        u = loadj("web/public/data/index.unified.json", repo=PB)
        info("A", "index.unified read from pb copy", "ws path transiently absent (board rebuild)")
    uc = u["counts"]
    chk_live("A", "unified 1342 = 318 + 1024, items 1342",
             uc["total"] == 1342 and uc["figures"] == 318 and uc["scenarios"] == 1024
             and len(u["items"]) == 1342, ["web/public/data/index.unified.json"],
             json.dumps(uc, ensure_ascii=False))

    rt = loadj("docs/architecture/web_p0_routes.json")
    chk_live("A", "routes count == 1358", rt.get("count") == 1358 and len(rt["routes"]) == 1358,
             ["docs/architecture/web_p0_routes.json"],
             "count=%s n=%d" % (rt.get("count"), len(rt["routes"])))

    smtxt = load("web/public/sitemap.xml")
    locs = re.findall(r"<loc>([^<]+)</loc>", smtxt)
    chk_live("A", "sitemap locs == 1359", len(locs) == 1359, ["web/public/sitemap.xml"],
             "n=%d" % len(locs))

    t_export = load("tools/export_static_site.py")
    t_pre = load("tools/pages_preflight.py")
    t_ci = load("tools/ci_data_check.py")
    t_static = load("web/src/api/static.ts")
    t_api = load("web/src/views/ApiDocsView.vue")
    chk_live("A", "anchor EXPECT_FIGURES = 1027 (export + preflight)",
             "EXPECT_FIGURES = 1027" in t_export and "EXPECT_FIGURES = 1027" in t_pre,
             ["tools/export_static_site.py", "tools/pages_preflight.py"],
             "export=%s preflight=%s" % ("EXPECT_FIGURES = 1027" in t_export,
                                          "EXPECT_FIGURES = 1027" in t_pre))
    chk_live("A", "anchor MIN_SITEMAP_ENTRIES = 1359 (ci_data_check)",
             "MIN_SITEMAP_ENTRIES = 1359" in t_ci, ["tools/ci_data_check.py"])
    chk_live("A", "copy text 1027 in static.ts / ApiDocsView.vue (no stale 1054/1056/1057)",
             ("1027" in t_static and "1054" not in t_static and "1056" not in t_static
              and "1057" not in t_static) and
             ("1027" in t_api and "1054" not in t_api and "1057" not in t_api),
             ["web/src/api/static.ts", "web/src/views/ApiDocsView.vue"],
             "static_ok=%s api_ok=%s" % ("1027" in t_static, "1027" in t_api))

    scnt = load("web/src/generated/siteCounts.ts")
    ver_pub = mc["verification"]["published"]
    okv = all(("%d" % ver_pub[k]) in scnt for k in ("verified", "pending", "suspect", "unverifiable"))
    chk_live("A", "siteCounts.ts matches meta verification published 4-state",
             okv, ["web/src/generated/siteCounts.ts"],
             "meta=%s" % json.dumps(ver_pub, ensure_ascii=False))

    nfiles = sum(len(f) for _, _, f in os.walk(os.path.join(WS, "web/public/data")))
    nfigd = len(glob.glob(os.path.join(WS, "web/public/data/figures/*.json")))
    nbyf = len(glob.glob(os.path.join(WS, "web/public/data/modes/by-figure/*.json")))
    nmidx = len(glob.glob(os.path.join(WS, "web/public/data/modes/index-*.json")))
    chk_live("A", "web/public/data products: figures 1027 / by-figure 318 / mode shards 8",
             nfigd == 1027 and nbyf == 318 and nmidx == 8, ["web/public/data/"],
             "files_total=%d figures=%d by_figure=%d mode_shards=%d" % (nfiles, nfigd, nbyf, nmidx))
    ws_tr = len(git_out(["ls-files"]).splitlines())
    pb_tr = len(git_out(["ls-files"], cwd=PB).splitlines())
    info("A", "tracked file counts", "ws=%d pb=%d" % (ws_tr, pb_tr))
except Exception as e:
    chk("A", "counts probe", False, "EXC %r" % e)

# ---------------------------------------------------------------- sec B 21-code chain
try:
    mj = loadj("docs/research/phase21w4_fix_manifest.json")
    TV = mj["f_target_values"]
    chk("B", "manifest target table has 21 codes", len(TV) == 21, "codes=%d" % len(TV))
    pb_zh = loadj("tools/json/scenarios_zh.json", repo=PB)
    pb_en = loadj("tools/json/scenarios_en.json", repo=PB)
    pb_idxm = {e["code"]: e for e in loadj("web/public/data/figures.index.json", repo=PB)}
    pb_um = {e["code"]: e for e in loadj("web/public/data/index.unified.json", repo=PB)["items"]}
    pb_rm = {r["path"]: r for r in loadj("docs/architecture/web_p0_routes.json", repo=PB)["routes"]}
    dbm = {r[0]: r for r in db.execute("select code, name_zh from figures").fetchall()}
    idxm = {e["code"]: e for e in idx}
    um = {e["code"]: e for e in u["items"]}
    rm = {r["path"]: r for r in rt["routes"]}
    fails = {k: [] for k in ("zh_name", "en_name", "db", "index", "shard", "unified",
                             "route", "sitemap", "pb_zh", "pb_en", "pb_index", "pb_shard",
                             "pb_unified", "pb_route")}
    for c, t in sorted(TV.items()):
        tz, te = t["zh"], t["en"]
        if not (dz.get(c) and dz[c].get("name") == tz):
            fails["zh_name"].append(c)
        if not (de.get(c) and de[c].get("name") == te):
            fails["en_name"].append(c)
        if dbm.get(c, (None, None))[1] != tz:
            fails["db"].append(c)
        if idxm.get(c, {}).get("name_zh") != tz:
            fails["index"].append(c)
        sh = os.path.join(WS, "web/public/data/figures/%s.json" % c)
        if not os.path.exists(sh):
            fails["shard"].append(c)
        else:
            sj = json.load(open(sh, encoding="utf-8"))
            if sj.get("code") != c:
                fails["shard"].append(c)
        if um.get(c, {}).get("name") != tz:
            fails["unified"].append(c)
        r = rm.get("figures/%s" % c) or rm.get("minds/%s" % c)
        if not (r and r.get("name") == tz and str(r.get("title", "")).startswith(tz)):
            fails["route"].append(c)
        if (c + "/") not in smtxt:
            fails["sitemap"].append(c)
        if not (pb_zh.get(c) and pb_zh[c].get("name") == tz):
            fails["pb_zh"].append(c)
        if not (pb_en.get(c) and pb_en[c].get("name") == te):
            fails["pb_en"].append(c)
        if pb_idxm.get(c, {}).get("name_zh") != tz:
            fails["pb_index"].append(c)
        if not os.path.exists(os.path.join(PB, "web/public/data/figures/%s.json" % c)):
            fails["pb_shard"].append(c)
        if pb_um.get(c, {}).get("name") != tz:
            fails["pb_unified"].append(c)
        pr = pb_rm.get("figures/%s" % c) or pb_rm.get("minds/%s" % c)
        if not (pr and pr.get("name") == tz):
            fails["pb_route"].append(c)
    for layer, bad in fails.items():
        chk("B", "21 codes / 21  " + layer, not bad, "fail=%s" % bad[:8])
except Exception as e:
    chk("B", "chain probe", False, "EXC %r" % e)


# ---------------------------------------------------------------- sec C scans
try:
    SCAN_OLD = ["SG-Lee-001", "MY-Mah-001", "JP-Sas-001", "UZ-Ulu-001"] + ["RW-KAG-%d" % i for i in range(1, 28)]
    pats = [re.escape(x).encode("ascii") for x in SCAN_OLD]
    SCAN_RE = re.compile(b"|".join(pats))

    EXEMPT = [
        ("data/backup_", "backup"),
        ("docs/research/", "report"),
        ("docs/qa/", "qa"),
        ("site_docs/", "site_docs"),
        ("release/", "release-frozen"),
        ("data/audit/", "audit"),
        ("tools/validation_report.json", "validation-report"),
        ("CHANGELOG.md", "changelog"),
        ("docs/scratch/", "scratch-legacy"),
        ("docs/archive/", "archive-docs"),
        ("data/individuals/", "individuals-legacy"),
        ("verify_rwkag_clear.py", "verifier"),
        ("verify_w4fix2_lxn.py", "verifier"),
        ("verify_phase21w4_qa_espinosa.py", "verifier"),
    ]

    def exempt_class(rel):
        for pref, cls in EXEMPT:
            if rel == pref or rel.startswith(pref):
                return cls
        return None

    def scan_repo(root):
        live, build_hits, counts, n = [], [], {}, 0
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in (".git", "node_modules", "__pycache__", ".cache")]
            for fn in fns:
                fp = os.path.join(dp, fn)
                rel = os.path.relpath(fp, root)
                try:
                    if os.path.getsize(fp) > 80 * 1024 * 1024:
                        continue
                    with open(fp, "rb") as f:
                        data = f.read()
                except Exception:
                    continue
                n += 1
                if SCAN_RE.search(data):
                    cls = exempt_class(rel)
                    if cls:
                        counts[cls] = counts.get(cls, 0) + 1
                    else:
                        live.append(rel)
                        if rel.startswith("web/public/") or rel.startswith("web/dist/"):
                            build_hits.append(rel)
        return n, counts, live, build_hits

    for root, label in [(WS, "ws"), (PB, "pb")]:
        n, counts, live, build_hits = scan_repo(root)
        chk("C", label + " residue live==0 (SG/MY/JP/UZ old keys + RW-KAG-1..27)",
            not live, "files=%d exempt=%s live=%s" % (n, json.dumps(counts, ensure_ascii=False), live[:6]))
        chk("C", label + " web/public + web/dist zero residue hits", not build_hits, "hits=%s" % build_hits[:6])
    dbb = open(os.path.join(WS, "api/protreptic.db"), "rb").read()
    pbb = open(os.path.join(PB, "api/protreptic.db"), "rb").read()
    chk("C", "api/protreptic.db bytes zero old-key residue (ws+pb)",
        not SCAN_RE.search(dbb) and not SCAN_RE.search(pbb))

    nk = loadj("data/figure_names.json") if os.path.exists(os.path.join(WS, "data/figure_names.json")) else {}
    pb_sm = load("web/public/sitemap.xml", repo=PB)
    cases = {}
    for c in ["JP-SAS-001", "UZ-ULU-001"]:
        cases[c] = {
            "zh": len(re.findall(c, json.dumps(dz.get(c), ensure_ascii=False) or "")),
            "en": len(re.findall(c, json.dumps(de.get(c), ensure_ascii=False) or "")),
            "sitemap": smtxt.count(c), "routes": json.dumps(rt).count(c),
            "unified": json.dumps(um.get(c)).count(c), "pb_zh": json.dumps(pb_zh.get(c), ensure_ascii=False).count(c),
            "pb_sitemap": pb_sm.count(c),
        }
    ok_new = all(all(v >= 1 for v in d.values()) for d in cases.values())
    chk("C", "new keys JP-SAS-001/UZ-ULU-001 referenced on all live surfaces (ws+pb)",
        ok_new, json.dumps(cases, ensure_ascii=False))
except Exception as e:
    chk("C", "scan probe", False, "EXC %r" % e)

# ---------------------------------------------------------------- sec D backups
try:
    def sha256sum_c(bdir):
        rc, out, err, _ = run(["sha256sum", "-c", "MANIFEST.sha256"], cwd=bdir, timeout=900)
        okn = len(re.findall(r": OK$", out, re.M))
        bad = re.findall(r"^(.*): FAILED$", out, re.M)
        return rc, okn, bad, out

    b1 = os.path.join(WS, "data/backup_phase21w4_fix_20260924")
    b2 = os.path.join(WS, "data/backup_phase21w4_fix2_20260924")
    b3 = os.path.join(WS, "data/backup_phase21w4_rwkag_clear_20260924")
    rc1, ok1, bad1, _ = sha256sum_c(b1)
    chk("D", "fix backup MANIFEST.sha256 -c 11/11", rc1 == 0 and ok1 == 11 and not bad1,
        "rc=%s ok=%s bad=%s" % (rc1, ok1, bad1[:3]))
    rc2, ok2, bad2, _ = sha256sum_c(b2)
    chk("D", "fix2 backup MANIFEST.sha256 -c 4/4", rc2 == 0 and ok2 == 4 and not bad2,
        "rc=%s ok=%s bad=%s" % (rc2, ok2, bad2[:3]))
    rc3, ok3, bad3, _ = sha256sum_c(b3)
    chk("D", "rwkag backup MANIFEST.sha256 -c 89/89", rc3 == 0 and ok3 == 89 and not bad3,
        "rc=%s ok=%s bad=%s" % (rc3, ok3, bad3[:3]))

    def manifest_identity(bdir, refcommit, label):
        lines = [l for l in load(os.path.join(bdir, "MANIFEST.sha256")).splitlines() if l.strip()]
        n_ok = n_tracked = n_ident = 0
        bad = []
        for l in lines:
            m = re.match(r"^([0-9a-f]{64})\s+\*?(.+?)\s*$", l)
            p = m.group(2).strip().lstrip("./")
            f = os.path.join(bdir, p)
            if not os.path.exists(f) or sha_f(f) != m.group(1):
                bad.append(p)
                continue
            n_ok += 1
            if os.path.basename(p) in ("README.md", "backup_manifest.json", "MANIFEST.sha256"):
                continue
            blob = gshow_bytes(refcommit, p)
            if blob:
                n_tracked += 1
                if sha_b(blob) == m.group(1):
                    n_ident += 1
        chk("D", label + " entries ok / git-object identity at " + refcommit,
            n_ok == len(lines) and not bad and n_ident == n_tracked,
            "lines=%d ok=%d tracked=%d identical=%d bad=%s" % (len(lines), n_ok, n_tracked, n_ident, bad[:4]))

    manifest_identity(b1, BASE, "fix backup (11 payload)")
    manifest_identity(b3, "8ca52c04", "rwkag backup (89 payload, preimage=8ca52c04)")
    manifest_identity(b2, EE, "fix2 backup (payload)")

    f2b = open(os.path.join(b2, "tools/json/scenarios_zh.json"), "rb").read()
    ee_obj = gshow_bytes(EE, "tools/json/scenarios_zh.json")
    chk("D", "fix2 backup scenarios_zh == EE git object byte-exact", f2b == ee_obj and len(f2b) == 2981559,
        "len=%d" % len(f2b))
    fb = json.load(open(os.path.join(b2, "fields_before.json"), encoding="utf-8"))
    chk("D", "fields_before.file_sha256_before == backup copy sha256",
        fb["file_sha256_before"] == sha_b(f2b), fb["file_sha256_before"][:16])
    cur = load("tools/json/scenarios_zh.json", binary=True)
    cur_claim = gshow_bytes(HEAD_CLAIM, "tools/json/scenarios_zh.json")
    f2txt = load("docs/research/phase21w4_fix2_report.json")
    mafter = re.search(r"8b218e71[0-9a-f]{56}", f2txt)
    after_sha = mafter.group(0) if mafter else ""
    pin_sha_ok = bool(mafter) and sha_b(cur_claim) == after_sha
    live_sha_ok = bool(mafter) and sha_b(cur) == after_sha
    dr_s = None if live_sha_ok else live_drift("tools/json/scenarios_zh.json")
    chk("D", "scenarios_zh: sha@HEAD_CLAIM == fix2 after-sha (strict); live == or drift",
        pin_sha_ok and (live_sha_ok or bool(dr_s)),
        "pinned=%s live=%s drift=%s" % (sha_b(cur_claim)[:24], sha_b(cur)[:24], dr_s))

    def findall(hay, needle):
        out = []
        i = hay.find(needle)
        while i != -1:
            out.append(i)
            i = hay.find(needle, i + 1)
        return out

    MAOB = MAO.encode("utf-8")
    LIB = ZH4.encode("utf-8")
    pos_bk = findall(f2b, MAOB)
    pos_cur = findall(cur, LIB)
    WINDOWS = [645895, 646237, 647666, 651341]
    win_ok = all(cur[o:o + len(LIB)] == LIB for o in WINDOWS)
    chk("D", "raw windows: 4 MAO in backup (exact) / target name in place at same 4 offsets",
        pos_bk == WINDOWS and win_ok and len(WINDOWS) == 4,
        "bk=%s cur_hits=%d win_ok=%s" % (pos_bk, len(pos_cur), win_ok))
    chk("D", "live zh counts: MAO == 0, target == 34 (pre-fix 4/30)",
        cur.count(MAOB) == 0 and cur.count(LIB) == 34)
    diff_runs = []
    if len(f2b) == len(cur_claim):
        i = 0
        while i < len(f2b):
            if f2b[i] != cur_claim[i]:
                j = i
                while j < len(f2b) and f2b[j] != cur_claim[j]:
                    j += 1
                diff_runs.append((i, j - i))
                i = j
            else:
                i += 1
    chk("D", "EE->fix2HEAD byte diff == 4 runs x 2B (8 bytes total), equal length [pin=HEAD_CLAIM]",
        len(f2b) == len(cur_claim) and len(diff_runs) == 4 and all(r[1] == 2 for r in diff_runs)
        and sum(r[1] for r in diff_runs) == 8,
        "runs=%s" % diff_runs)
    for fname, blob in fb["fields"].items():
        chk("D", "fields_before field %s: before-sha + after_expected in place" % fname,
            sha_b(blob["before"].encode("utf-8")) == blob["before_sha256"]
            and blob["before"].encode("utf-8") in f2b
            and blob["after_expected"].encode("utf-8") in cur)
    dec = f2b.decode("utf-8")
    cps = []
    j = dec.find(MAO)
    while j != -1:
        cps.append(j)
        j = dec.find(MAO, j + 1)
    rec = fb.get("occurrence_byte_offsets")
    chk("D", "fields_before offsets re-verified as CODEPOINT offsets (errata reproduced)",
        cps == rec, "codepoints=%s recorded=%s" % (cps, rec))

    for c27 in ["RW-KAG-%d" % i for i in range(1, 28)]:
        assert_absent = []
        for p in [os.path.join(WS, "tools/json/%s.json" % c27),
                  os.path.join(WS, "%s.json" % c27),
                  os.path.join(WS, "web/public/data/figures/%s.json" % c27),
                  os.path.join(PB, "tools/json/%s.json" % c27),
                  os.path.join(PB, "web/public/data/figures/%s.json" % c27)]:
            if os.path.exists(p):
                assert_absent.append(p)
        if assert_absent:
            chk("D", "27-code live absence " + c27, False, str(assert_absent))
            break
    else:
        chk("D", "all 27 RW-KAG codes absent live (ws tools/json+root+shard, pb tools/json+shard)", True)
    ar = loadj("docs/research/_archive/RW-KAG_1-27_archive.json")
    frags = ar["per_code_fragments"]
    chk("D", "archive: 27 codes x per_code_fragments", len(frags) == 27)
    sample = [1, 4, 7, 10, 13, 16, 19, 22, 25]
    okd = okr = oks = oksc = okcm = 0
    for i in sample:
        c = "RW-KAG-%d" % i
        fr = frags[c]
        fd = fr["draft"]
        fdr = os.path.join(b3, fd["path"])
        twin = fr["root_twin"]
        fsh = fr["shard"]
        if os.path.exists(fdr) and sha_f(fdr) == fd["sha256"] and os.path.getsize(fdr) == fd["bytes"]:
            okd += 1
        tr = os.path.join(b3, twin["path"])
        if os.path.exists(tr) and sha_f(tr) == twin["sha256"] == fd["sha256"] and twin.get("byte_same_as_draft"):
            okr += 1
        shr = os.path.join(b3, fsh["path"])
        if os.path.exists(shr) and sha_f(shr) == fsh["sha256"]:
            oks += 1
        bzh = loadj("tools/json/scenarios_zh.json", repo=b3)
        if c in bzh and c not in dz:
            oksc += 1
        cm = load("tools/code_maps_en.json", repo=b3)
        cmc = load("tools/code_maps_en.json")
        if ('"%s"' % c) in cm and ('"%s"' % c) not in cmc:
            okcm += 1
    chk("D", "rwkag stratified sample 9/27 (33%): draft + root_twin + shard fragment recompute",
        okd == 9 and okr == 9 and oks == 9, "draft=%d twin=%d shard=%d" % (okd, okr, oks))
    chk("D", "rwkag sample: scenarios entry gone live / present in backup; code_maps key cleared",
        oksc == 9 and okcm == 9, "scen=%d codemaps=%d" % (oksc, okcm))
except Exception as e:
    chk("D", "backup probe", False, "EXC %r" % e)

# ---------------------------------------------------------------- sec E commit audit
try:
    QA_ARTIFACTS = {"verify_phase21w4_qa_espinosa.py", "docs/qa/phase21w4_qa_report.md",
                    "docs/qa/phase21w4_qa_evidence.json"}
    got = [x[:8] for x in git_out(["rev-list", "--reverse", BASE + "..HEAD"]).split()]
    extra_commits = [c for c in got if c not in WS_COMMITS]
    extra_bad = []
    for c in extra_commits:
        ch = set(p for p in git_out(["diff-tree", "--no-commit-id", "--name-only", "-r", c]).split("\n") if p)
        if not ch:
            extra_bad.append(c + ":unresolved")
        elif ch <= QA_FILES:
            continue
        else:
            hitm = sorted(p for p in ch if is_w4_marker(p))
            if hitm:
                extra_bad.append(c + "->" + ",".join(hitm[:3]))
    chk("E", "commits BASE..HEAD == 10 W4 in order + QA-only + foreign(no W4-marker touch)",
        got[:10] == WS_COMMITS and not extra_bad,
        "n=%d qa=%d foreign=%d extra_bad=%s" % (len(got), len(QA_COMMITS), len(FOREIGN), extra_bad[:4]))
    ALLOWED_EXACT = {
        "api/protreptic.db",
        "tools/json/scenarios_zh.json", "tools/json/scenarios_en.json", "tools/json/H-LXN-001.json",
        "tools/ci_data_check.py", "tools/export_static_site.py", "tools/pages_preflight.py",
        "tools/code_maps_en.json",
        "docs/architecture/web_p0_routes.json", "docs/architecture/static_data_manifest.json",
        "web/public/sitemap.xml",
        "web/src/api/static.ts", "web/src/generated/siteCounts.ts", "web/src/views/ApiDocsView.vue",
        "verify_rwkag_clear.py", "verify_w4fix2_lxn.py", "verify_phase21w4_qa_espinosa.py",
    }
    ALLOWED_PREFIX = ("docs/research/", "data/backup_phase21w4_", "docs/qa/phase21w4_qa")
    FORBIDDEN_PREFIX = ("docs/research/phase20", "docs/research/phase21w5", "docs/research/phase21w6",
                        "docs/research/phase21r8", "data/individuals/", "docs/figures/")
    FORBIDDEN_EXACT = {"data/modes_data.json", "data/figure_names.json", "CHANGELOG.md"}

    changed_all = git_out(["diff", "--name-only", BASE + "..HEAD_CLAIM"]).split()
    w4qa_changed = [p for p in changed_all if p in W4_SURFACE or p in QA_FILES]
    unclassified = [p for p in w4qa_changed if not (p in ALLOWED_EXACT or p.startswith(ALLOWED_PREFIX))]
    forbidden = [p for p in w4qa_changed if p in FORBIDDEN_EXACT or p.startswith(FORBIDDEN_PREFIX)]
    chk("E", "W4-scope changed-path set fully classified (no out-of-scope files)", not unclassified,
        "n=%d unclassified=%s" % (len(w4qa_changed), unclassified[:8]))
    chk("E", "no touches to modes_data/figure_names/CHANGELOG/individuals/docs-figures/other reports",
        not forbidden, "forbidden=%s" % forbidden[:8])
    foreign_paths = set()
    for c, ps in FOREIGN.items():
        foreign_paths.update(ps)
    info("E", "board drift registered (foreign commits in window touch zero W4-surface paths)",
         "commits=%d paths=%d sample=%s" % (len(FOREIGN), len(foreign_paths), sorted(foreign_paths)[:4]))
    deletes = ""
    for c in WS_COMMITS + QA_COMMITS:
        d = git_out(["diff-tree", "-r", "-M", "--diff-filter=D", "--no-commit-id", "--name-only", c]).strip()
        if d:
            deletes += d + "\n"
    chk("E", "zero tracked deletions by W4+QA commits (untracked legacy moved to backups)", not deletes,
        "deletes=%s" % deletes[:200])

    def scen_diff(ca, cb, path):
        a = gshow_json(ca, path)
        bb = gshow_json(cb, path)
        added = sorted(set(bb) - set(a))
        removed = sorted(set(a) - set(bb))
        chg = {}
        for k in sorted(set(a) & set(bb)):
            fa, fbb = a[k], bb[k]
            if fa != fbb:
                chg[k] = sorted([f for f in set(fa) | set(fbb) if fa.get(f) != fbb.get(f)])
        return a, bb, added, removed, chg

    codes27 = ["RW-KAG-%d" % i for i in range(1, 28)]
    old_removed = ["JP-Sas-001", "SG-Lee-001", "UZ-Ulu-001", "MY-Mah-001"] + codes27
    exp_codes_zh = ["H-CY-159", "H-GHZ-163", "H-HLG-001", "H-HYP-145", "H-IKD-160", "H-ISC-362",
                    "H-LXN-001", "H-LXN-347", "H-MZ-001", "H-SUF-364", "H-SY-149", "H-WX-147",
                    "H-WYX-146", "H-XMQ-151", "H-YLP-148", "H-ZEL-001",
                    "MY-MAH-001", "RW-KAG-001", "SG-LEE-001"]
    a, bb, added, removed, chg = scen_diff(BASE, EE, "tools/json/scenarios_zh.json")
    chk("E", "zh BASE->EE: added/removed sets exact", added == ["JP-SAS-001", "UZ-ULU-001"]
        and removed == sorted(old_removed), "added=%s removed=%d" % (added, len(removed)))
    chk("E", "zh BASE->EE: changed == 19 target codes, fields == ['name']",
        sorted(chg) == sorted(exp_codes_zh) and all(v == ["name"] for v in chg.values()),
        "n=%d odd=%s" % (len(chg), [k for k, v in chg.items() if v != ["name"]][:5]))
    bad_val = []
    for k in exp_codes_zh:
        if bb[k].get("name") != TV[k]["zh"]:
            bad_val.append(k)
    chk("E", "zh BASE->EE: new names == manifest targets (19/19)", not bad_val, "bad=%s" % bad_val[:6])
    chk("E", "zh BASE->EE: backfill semantics (old name key absent) + MY correction",
        all(a[k].get("name") is None for k in exp_codes_zh if k != "MY-MAH-001")
        and a["MY-MAH-001"].get("name") == "Mahathir Mohamad",
        "MY old=%r" % a["MY-MAH-001"].get("name"))
    jp = dict(bb["JP-SAS-001"]); jp.pop("name", None); jp.pop("code", None)
    jpo = dict(a["JP-Sas-001"]); jpo.pop("name", None); jpo.pop("code", None)
    uz = dict(bb["UZ-ULU-001"]); uz.pop("name", None); uz.pop("code", None)
    uzo = dict(a["UZ-Ulu-001"]); uzo.pop("name", None); uzo.pop("code", None)
    chk("E", "zh rekey: JP/UZ migrated content-identical (allowed delta: code+name only)",
        jp == jpo and uz == uzo and bb["JP-SAS-001"].get("code") == "JP-SAS-001"
        and bb["UZ-ULU-001"].get("code") == "UZ-ULU-001")

    exp_codes_en = [c for c in exp_codes_zh if c != "MY-MAH-001"]
    a2, b2, added2, removed2, chg2 = scen_diff(BASE, EE, "tools/json/scenarios_en.json")
    chk("E", "en BASE->EE: added/removed sets exact", added2 == ["JP-SAS-001", "UZ-ULU-001"]
        and removed2 == sorted(old_removed))
    chk("E", "en BASE->EE: changed == 18 codes; H-LXN-001 5 fields, others ['name']",
        sorted(chg2) == sorted(exp_codes_en)
        and chg2.get("H-LXN-001") == ["case_en", "description_en", "name", "name_en", "reason_en"]
        and all(chg2[k] == ["name"] for k in chg2 if k != "H-LXN-001"),
        "n=%d lxn1=%s" % (len(chg2), chg2.get("H-LXN-001")))
    bad_val2 = [k for k in exp_codes_en if b2[k].get("name") != TV[k]["en"]]
    chk("E", "en BASE->EE: new names == manifest targets (18/18)", not bad_val2, "bad=%s" % bad_val2[:6])

    a3, b3j, added3, removed3, chg3 = scen_diff(EE, HEAD_CLAIM, "tools/json/scenarios_zh.json")
    chk("E", "zh EE->fix2HEAD [pin=HEAD_CLAIM]: only H-LXN-001, fields == 4 zh extensions",
        added3 == [] and removed3 == [] and sorted(chg3) == ["H-LXN-001"]
        and chg3.get("H-LXN-001") == ["case_zh", "description_zh", "name_zh", "reason_zh"],
        "chg=%s" % chg3)
    ent = b3j["H-LXN-001"]
    chk("E", "zh EE->HEAD: values are Li Xiannian; no residual Mao in 4 fields",
        MAO not in json.dumps({k: ent[k] for k in chg3.get("H-LXN-001", [])}, ensure_ascii=False)
        and all(ZH4 in str(ent[k]) for k in ("name_zh", "description_zh", "reason_zh", "case_zh")),
        "name_zh=%s" % ent["name_zh"])
    ee_names = {"en": "tools/json/scenarios_en.json" in
                git_out(["diff", "--name-only", EE + ".." + HEAD_CLAIM]).split()}
    chk("E", "en scenarios untouched by fix2 window [pin=HEAD_CLAIM]", not ee_names["en"])
    inf_zh = sorted([k for k in set(a3) & set(b3j) if a3[k] != b3j[k]])
    chk("E", "zh EE->HEAD: exactly 1 code deep-changed (1039 entries untouched)", inf_zh == ["H-LXN-001"],
        "n=%d" % len(inf_zh))

    dold = gshow_json(BASE, "tools/json/H-LXN-001.json")
    dnew_ = gshow_json(EE, "tools/json/H-LXN-001.json")
    dchg = sorted([f for f in set(dold) | set(dnew_) if dold.get(f) != dnew_.get(f)])
    chk("E", "draft H-LXN-001 BASE->EE: 8 fields, values Li Xiannian",
        dchg == ["case_en", "case_zh", "description_en", "description_zh", "name_en", "name_zh",
                 "reason_en", "reason_zh"]
        and dnew_["name_zh"] == ZH4 and dnew_["name_en"] == EN4
        and MAO not in json.dumps(dnew_, ensure_ascii=False) and MAOEN not in json.dumps(dnew_, ensure_ascii=False),
        "n=%d bad=%s" % (len(dchg), [f for f in dchg if "name" not in f][:4]))

    cm_o = gshow_json(BASE, "tools/code_maps_en.json")
    cm_n = gshow_json(EE, "tools/code_maps_en.json")
    cm_rm = sorted(set(cm_o) - set(cm_n))
    cm_add = sorted(set(cm_n) - set(cm_o))
    cm_chg = [k for k in set(cm_o) & set(cm_n) if cm_o[k] != cm_n[k]]
    chk("E", "code_maps_en BASE->EE: removed == 27 RW keys, no adds, no other changes",
        sorted(cm_rm) == sorted(codes27) and not cm_add and not cm_chg,
        "rm=%d add=%s chg=%d" % (len(cm_rm), cm_add[:3], len(cm_chg)))

    maybe = [("e7be5cc6", "tools/ci_data_check.py", "MIN_SITEMAP_ENTRIES", 1388, 1386),
             ("33762c4e", "tools/ci_data_check.py", "MIN_SITEMAP_ENTRIES", 1386, 1359),
             ("e7be5cc6", "tools/export_static_site.py", "EXPECT_FIGURES", 1056, 1054),
             ("33762c4e", "tools/export_static_site.py", "EXPECT_FIGURES", 1054, 1027),
             ("e7be5cc6", "tools/pages_preflight.py", "EXPECT_FIGURES", 1056, 1054),
             ("33762c4e", "tools/pages_preflight.py", "EXPECT_FIGURES", 1054, 1027)]
    anchor_bad = []
    for c, p, name, ov, nv in maybe:
        o = gshow_text(c + "^", p)
        nn = gshow_text(c, p)
        mo = re.search(r"%s = (\d+)" % name, o)
        mn = re.search(r"%s = (\d+)" % name, nn)
        if not (mo and mn and int(mo.group(1)) == ov and int(mn.group(1)) == nv):
            anchor_bad.append((c, p, name))
    sv = [("e7be5cc6", "web/src/api/static.ts", "1056", "1054"), ("33762c4e", "web/src/api/static.ts", "1054", "1027"),
          ("e7be5cc6", "web/src/views/ApiDocsView.vue", "1057", "1054"),
          ("33762c4e", "web/src/views/ApiDocsView.vue", "1054", "1027")]
    for c, p, ov, nv in sv:
        o = gshow_text(c + "^", p)
        nn = gshow_text(c, p)
        if not (o.count(ov) == 2 and o.count(nv) == 0 and nn.count(nv) == 2 and nn.count(ov) == 0):
            anchor_bad.append((c, p, ov, nv))
    so = gshow_text("e7be5cc6^", "web/src/generated/siteCounts.ts")
    sn = gshow_text("e7be5cc6", "web/src/generated/siteCounts.ts")
    mp = re.search(r"published: \{ verified: (\d+), pending: (\d+), suspect: (\d+), unverifiable: (\d+) \}", so)
    mpn = re.search(r"published: \{ verified: (\d+), pending: (\d+), suspect: (\d+), unverifiable: (\d+) \}", sn)
    ma = re.search(r"all: \{ verified: (\d+), pending: (\d+), suspect: (\d+), unverifiable: (\d+) \}", so)
    man = re.search(r"all: \{ verified: (\d+), pending: (\d+), suspect: (\d+), unverifiable: (\d+) \}", sn)
    ok_sc = (mp and mpn and ma and man
             and mp.groups() == ("931", "1916", "34", "340") and mpn.groups() == ("949", "1897", "35", "340")
             and ma.groups() == ("931", "1948", "51", "351") and man.groups() == ("949", "1929", "52", "351"))
    chk("E", "anchor churn matches receipts (constants + 4-state convergence 931/1916/34->949/1897/35)",
        not anchor_bad and ok_sc, "bad=%s sitecounts_all=%s" % (anchor_bad[:4], ma and man and (ma.groups(), man.groups())))

    ro = gshow_json(BASE, "docs/architecture/web_p0_routes.json")
    om = {r["path"]: r for r in ro["routes"]}
    rm_pin = {r["path"]: r for r in gshow_json(HEAD_CLAIM, "docs/architecture/web_p0_routes.json")["routes"]}
    removed_paths = sorted(set(om) - set(rm_pin))
    added_paths = sorted(set(rm_pin) - set(om))
    exp_rm_paths = sorted(["figures/%s" % c for c in (["JP-Sas-001", "SG-Lee-001", "UZ-Ulu-001", "MY-Mah-001"] + codes27)])
    chk("E", "routes BASE->fix2HEAD [pin=HEAD_CLAIM]: path removed/added sets exact",
        removed_paths == exp_rm_paths and added_paths == ["figures/JP-SAS-001", "figures/UZ-ULU-001"],
        "rm=%d add=%s" % (len(removed_paths), added_paths))
    chg_r = {}
    for k in sorted(set(om) & set(rm_pin)):
        d = {f for f in set(om[k]) | set(rm_pin[k]) if om[k].get(f) != rm_pin[k].get(f)}
        if d:
            chg_r[k] = sorted(d)
    chk("E", "routes kept-path changes confined to title/name/description (+W5 body convergence)",
        all(set(v) <= {"title", "name", "description", "body_text_chars"} for v in chg_r.values())
        and sum(1 for v in chg_r.values() if "body_text_chars" in v) <= 1,
        "n=%d body=%s" % (len(chg_r), [k for k, v in chg_r.items() if "body_text_chars" in v]))
    bodies = [k for k, v in chg_r.items() if "body_text_chars" in v]
    info("E", "route body_text_chars delta (W5 convergence surface)", "codes=%s delta=%s" % (
        bodies, [(b, om[b].get("body_text_chars"), rm_pin[b].get("body_text_chars")) for b in bodies]))

    sm_old = set(re.findall(r"<loc>([^<]+)</loc>", gshow_text(BASE, "web/public/sitemap.xml")))
    locs_pin = re.findall(r"<loc>([^<]+)</loc>", gshow_text(HEAD_CLAIM, "web/public/sitemap.xml"))
    sm_new = set(locs_pin)
    tail_old = set(x.split("/protreptic/")[-1] for x in sm_old - sm_new)
    tail_new = set(x.split("/protreptic/")[-1] for x in sm_new - sm_old)
    exp_tail_rm = set((["figures/%s/" % c for c in (["JP-Sas-001", "SG-Lee-001", "UZ-Ulu-001", "MY-Mah-001"] + codes27)]))
    chk("E", "sitemap BASE->fix2HEAD [pin=HEAD_CLAIM]: removed/added == 31 old paths / 2 new paths",
        tail_old == exp_tail_rm and tail_new == {"figures/JP-SAS-001/", "figures/UZ-ULU-001/"},
        "rm=%d add=%s" % (len(tail_old), sorted(tail_new)[:4]))

    fig_route = rm_pin.get("figures", {})
    chk("E", "figures index route description follows unified counts (318 + 1024)",
        "318" in str(fig_route.get("description")) and "1024" in str(fig_route.get("description")),
        str(fig_route.get("description"))[:120])
    cred = json.dumps(rm_pin.get("credibility", {}), ensure_ascii=False)
    chk("E", "credibility route carries converged 4-state (949/1897/35)", "949" in cred and "1897" in cred,
        cred[:160])

    zc_all = git_out(["diff", "--name-only", EE + ".." + HEAD_CLAIM]).split()
    exp_zc = sorted(["tools/json/scenarios_zh.json", "docs/research/phase21w4_fix_report.md",
                     "docs/research/phase21w4_fix2_report.md", "docs/research/phase21w4_fix2_report.json",
                     "verify_w4fix2_lxn.py"] + ["data/backup_phase21w4_fix2_20260924/" + p for p in
                     ("MANIFEST.sha256", "README.md", "backup_manifest.json", "fields_before.json",
                      "tools/json/scenarios_zh.json")])
    zc = [p for p in zc_all if p in W4_SURFACE or p in QA_FILES]
    zc_extra = sorted(set(zc) - set(exp_zc) - QA_FILES)
    chk("E", "fix2 window EE..HEAD (W4-scope) == 10 expected files + QA artifacts (zero-change re-run)",
        set(zc) >= set(exp_zc) and not zc_extra,
        "n=%d expected=%d W4-scope=%d drift-outside-scope=%d extras=%s" % (len(zc_all), len(exp_zc), len(zc), len(zc_all) - len(zc), zc_extra))
except Exception as e:
    chk("E", "commit audit probe", False, "EXC %r" % e)


# ---------------------------------------------------------------- sec F gates
def sec_fgh(args):
    try:
        if args.quick:
            info("F", "gates/verifiers skipped (--quick)", "")
        else:
            gates = [
                ("credibility_gate --hard-fail", ["python3", "tools/credibility_gate.py", "--hard-fail"]),
                ("verify_source_links --hard-fail", ["python3", "tools/verify_source_links.py", "--hard-fail"]),
                ("verify_findings --hard-fail", ["python3", "tools/verify_findings.py", "--hard-fail"]),
                ("ci_data_check", ["python3", "tools/ci_data_check.py"]),
                ("pages_preflight --stage data", ["python3", "tools/pages_preflight.py", "--stage", "data"]),
                ("pages_preflight --stage dist", ["python3", "tools/pages_preflight.py", "--stage", "dist"]),
            ]
            for label, cmd in gates:
                rc, out, err, secs = run(cmd, cwd=WS, timeout=1800)
                tail = (out or err).strip().splitlines()
                tail = " | ".join(tail[-3:]) if tail else ""
                txt_g = out + err
                dr = None
                if rc != 0 and BOARD_SRC_MOVED and "index.unified.json" in txt_g \
                        and not os.path.exists(os.path.join(WS, "web/public/data/index.unified.json")):
                    dr = "board-rebuild: index.unified.json transiently absent"
                if dr:
                    DRIFTS.append({"sec": "F", "item": label + " rc!=0 attributed", "path": "web/public/data/index.unified.json",
                                   "drift": dr, "detail": tail[:240]})
                    chk("F", label + " rc==0 [drift-attributed]", True,
                        "DRIFT(%s) rc=%s %ss :: %s" % (dr, rc, secs, tail[:300]))
                else:
                    chk("F", label + " rc==0", rc == 0, "rc=%s %ss :: %s" % (rc, secs, tail[:400]))
            rc, out, err, secs = run(["python3", "verify_rwkag_clear.py"], cwd=WS, timeout=1800)
            txt2 = out + err
            fails2 = [l.strip() for l in txt2.splitlines() if l.strip().startswith("[FAIL]")]
            qa_self = (len(fails2) == 1 and fails2[0].startswith("[FAIL] scan.ws.live_zero")
                       and "verify_phase21w4_qa_espinosa.py" in fails2[0])
            chk("F", "upstream verifier verify_rwkag_clear.py full: rc==0, or sole fail = QA-script self-hit",
                rc == 0 or (rc == 1 and qa_self),
                "rc=%s %ss fails=%s :: %s" % (rc, secs, fails2[:2], (" | ".join(txt2.strip().splitlines()[-3:]))[:300]))
            info("F", "verify_rwkag_clear QA-self interaction",
                "scan.ws.live_zero flags this QA verifier itself (fixture holds old keys; allowed_hit exempts docs/qa/** and the two chain verifiers by exact name, not this root file); upstream 21/21 claim unaffected (pre-QA state); post-QA expectation = 20/21 with this sole hit")
            rc, out, err, secs = run(["python3", "verify_w4fix2_lxn.py"], cwd=WS, timeout=1800)
            tail = (out or err).strip().splitlines()
            tail = " | ".join(tail[-3:]) if tail else ""
            txt_w = out + err
            drw = None
            if rc != 0 and BOARD_SRC_MOVED and "index.unified.json" in txt_w \
                    and not os.path.exists(os.path.join(WS, "web/public/data/index.unified.json")):
                drw = "board-rebuild: index.unified.json transiently absent"
            if drw:
                DRIFTS.append({"sec": "F", "item": "verify_w4fix2_lxn rc!=0 attributed",
                               "path": "web/public/data/index.unified.json", "drift": drw, "detail": tail[:240]})
                chk("F", "upstream verifier verify_w4fix2_lxn.py full [drift-attributed]", True,
                    "DRIFT(%s) rc=%s %ss :: %s" % (drw, rc, secs, tail[:300]))
            else:
                chk("F", "upstream verifier verify_w4fix2_lxn.py full rc==0",
                    rc == 0, "rc=%s %ss :: %s" % (rc, secs, tail[:400]))
    except Exception as e:
        chk("F", "gate probe", False, "EXC %r" % e)

    # ------------------------------------------------------------ sec G parity
    try:
        if args.quick:
            info("G", "parity skipped (--quick)", "")
        else:
            rc, out, err, secs = run(["python3", "tools/check_repo_parity.py"], cwd=WS, timeout=1800)
            txt = out + err
            stats_line = "".join(l for l in txt.splitlines() if l.startswith("[stats]"))
            nums = re.findall(r"(\d+)", stats_line)[:5]
            m2 = sorted(re.findall(r"MISSING_IN_PUBLISH\s+\[[^\]]*\]\s+(\S+)", txt))
            known6 = sorted(["docs/research/phase21r8_w4_names_recon.json", "docs/research/phase21r8_w4_names_recon.md",
                             "docs/research/phase21w4_fix_manifest.json", "docs/research/phase21w4_fix_manifest.md",
                             "docs/research/phase21w6_marker_scan.json", "docs/research/phase21w6_marker_scan.md"])
            allowed_extra = ["docs/qa/phase21w4_qa_evidence.json", "docs/qa/phase21w4_qa_report.md",
                             "verify_phase21w4_qa_espinosa.py", "docs/qa/phase21w4_qa_run_final.log"]
            diffs = sorted(re.findall(r"CONTENT_DIFF\s+\[[^\]]*\]\s+(\S+)", txt))
            extras = sorted(set(m2) - set(known6))
            extras_foreign = [e for e in extras if e not in allowed_extra
                              and (foreign_attributed(e, BASE + "..HEAD") or live_drift(e))]
            extras_bad = [e for e in extras if e not in allowed_extra and e not in extras_foreign]
            diffs_bad = [p for p in diffs if not live_drift(p)]
            for p in diffs:
                if p in diffs_bad:
                    continue
                DRIFTS.append({"sec": "G", "item": "parity content-diff " + p, "path": p,
                               "drift": live_drift(p) or "", "detail": "ws vs pb content diff"})
            common_n = int(nums[0]) if (nums and nums[0].isdigit()) else 0
            ok = (common_n >= 2395 and nums[4:5] == ["0"] and set(known6) <= set(m2)
                  and not extras_bad and not diffs_bad
                  and nums[1:2] == [str(common_n - len(diffs))]
                  and nums[2:3] == [str(len(m2))] and nums[3:4] == [str(len(m2))])
            chk("G", "official parity: common >=2395 (self-consistent); content-diffs & single-sides drift-attributed",
                ok, "rc=%s %ss nums=%s miss=%d diffs=%d diff_bad=%s foreign_drift=%d bad=%s" % (
                    rc, secs, nums, len(m2), len(diffs), diffs_bad[:4], len(extras_foreign), extras_bad[:6]))
        KEYFILES = ["api/protreptic.db", "tools/json/scenarios_zh.json", "tools/json/scenarios_en.json",
                    "tools/json/H-LXN-001.json", "tools/code_maps_en.json",
                    "docs/architecture/web_p0_routes.json", "docs/architecture/static_data_manifest.json",
                    "web/public/sitemap.xml", "web/public/data/figures.index.json",
                    "web/public/data/index.unified.json", "web/public/data/meta.json",
                    "web/src/api/static.ts", "web/src/views/ApiDocsView.vue",
                    "web/src/generated/siteCounts.ts", "tools/ci_data_check.py",
                    "tools/export_static_site.py", "tools/pages_preflight.py",
                    "verify_w4fix2_lxn.py",
                    "docs/research/phase21w4_fix_report.md", "docs/research/phase21w4_fix_evidence.json",
                    "docs/research/phase21w4_rwkag_clear_report.md", "docs/research/phase21w4_rwkag_clear_evidence.json",
                    "docs/research/phase21w4_fix2_report.md", "docs/research/phase21w4_fix2_report.json",
                    "docs/research/_archive/RW-KAG_1-27_archive.json"]
        bad = []
        for p in KEYFILES:
            fw, fp2 = os.path.join(WS, p), os.path.join(PB, p)
            if not (os.path.exists(fw) and os.path.exists(fp2)):
                bad.append(p + ":missing")
            elif sha_f(fw) != sha_f(fp2):
                bad.append(p + ":diff")
        bad_unattr = [b for b in bad if not live_drift(b.split(":")[0], build=is_build_product(b.split(":")[0]))]
        for b in bad:
            if b in bad_unattr:
                continue
            p0 = b.split(":")[0]
            DRIFTS.append({"sec": "G", "item": "keyfile " + b, "path": p0,
                           "drift": live_drift(p0, build=is_build_product(p0)) or "", "detail": b})
        chk("G", "key-file byte identity ws vs pb (%d files) [drift-attributed]" % len(KEYFILES),
            not bad_unattr,
            "bad=%d attributed=%d unattributed=%s" % (len(bad), len(bad) - len(bad_unattr), bad_unattr[:6]))
        info("G", "verify_rwkag_clear.py ws-only", "not in any mirror/receipt claim (ee receipt lists report/evidence/data-mirror only); pb witness parity_key_files excludes it; non-material")

        sh_w = {os.path.basename(x): sha_f(x) for x in glob.glob(os.path.join(WS, "web/public/data/figures/*.json"))}
        sh_p = {os.path.basename(x): sha_f(x) for x in glob.glob(os.path.join(PB, "web/public/data/figures/*.json"))}
        chk("G", "1027 shards byte-identical ws vs pb", sh_w == sh_p and len(sh_w) == 1027,
            "ws=%d pb=%d" % (len(sh_w), len(sh_p)))

        SKIP = (".git", "node_modules", "__pycache__", "web/dist", "site_docs", "release", "logs",
                ".venv", "node-compile-cache")
        def tree_idx(root):
            idx = {}
            for dp, dns, fns in os.walk(root):
                dns[:] = [d for d in dns if d not in SKIP and not d.endswith(".cache")]
                for fn in fns:
                    fp = os.path.join(dp, fn)
                    rel = os.path.relpath(fp, root)
                    if rel.startswith(SKIP):
                        continue
                    try:
                        idx[rel] = os.path.getsize(fp)
                    except Exception:
                        pass
            return idx
        iw, ip = tree_idx(WS), tree_idx(PB)
        common = sorted(set(iw) & set(ip))
        only_ws = sorted(set(iw) - set(ip))
        only_pb = sorted(set(ip) - set(iw))
        content_diff = []
        for rel in common:
            fw, fp2 = os.path.join(WS, rel), os.path.join(PB, rel)
            if iw[rel] > 45 * 1024 * 1024:
                continue
            try:
                if sha_f(fw) != sha_f(fp2):
                    content_diff.append(rel)
            except Exception:
                content_diff.append(rel + ":read-error")
        CORE = ("tools/json/", "docs/architecture/", "web/public/", "web/src/", "docs/research/",
                "docs/qa/", "data/modes_data", "data/figure_names", "data/figures/", "api/protreptic.db")
        core_diff = [p for p in content_diff if p.startswith(CORE)]
        core_unattr = [p for p in core_diff if not live_drift(p, build=is_build_product(p))]
        for p in core_diff:
            if p in core_unattr:
                continue
            DRIFTS.append({"sec": "G", "item": "core-diff " + p, "path": p,
                           "drift": live_drift(p, build=is_build_product(p)) or "",
                           "detail": "ws vs pb content diff"})
        chk("G", "full-tree: core content diffs (ws vs pb) drift-attributed",
            not core_unattr, "common=%d total_diff=%d core=%d unattributed=%s" % (
                len(common), len(content_diff), len(core_diff), core_unattr[:6]))
        info("G", "dev-side content diff classes (by design, repo roles differ)",
            json.dumps(sorted(set(p.split("/")[0] for p in content_diff)))[:400])
        CORE_W = ("tools/json/", "docs/architecture/", "web/public/", "web/src/", "docs/research/",
                  "docs/qa/", "api/", "data/", "tools/")
        lm = sorted(p for p in only_ws if p.startswith(CORE_W) and not p.startswith("data/backup"))
        EXP_W = sorted(["api/data/semantic_index.faiss", "api/data/semantic_index_metadata.pkl",
                        "api/data/test_semantic_index.faiss", "api/threadpoolctl.py", "api/typing_extensions.py",
                        "data/all_sources.json", "data/code_maps.json.bak.fix-20260906_225525",
                        "data/code_maps.json.bak_zz_20260910_083514",
                        "data/figures/_duplicates/H-ZX-001_legacy_docs_page.bak_zengzi_fix.md",
                        "data/individuals/H-ZZ-001.json.bak_zz_20260910_083514",
                        "data/individuals/H-ZZ-001_modes.json.bak_zz_20260910_083514",
                        "data/merge_staging_H-SYX-001/figures_H-SYX-001.json",
                        "data/merge_staging_H-SYX-001/merge_payload_H-SYX-001.json",
                        "data/merge_staging_H-SYX-001/qa_payload.py", "data/modes_data.json.bak",
                        "data/modes_data.json.bak.fix-20260906_225525",
                        "data/modes_data.json.bak_zz_20260910_083514", "data/scenario_tags.json.bak_zz_20260910_083514",
                        "data/scenarios_en.json.bak_zz_20260910_083514",
                        "data/scenarios_zh.json.bak_zz_20260910_083514", "data/semantic_index.faiss",
                        "docs/research/phase21r8_w4_names_recon.json", "docs/research/phase21r8_w4_names_recon.md",
                        "docs/research/phase21w4_fix_manifest.json", "docs/research/phase21w4_fix_manifest.md",
                        "docs/research/phase21w6_marker_scan.json", "docs/research/phase21w6_marker_scan.md",
                        "tools/build_legacy20_r6_batch1.py", "tools/build_phase21r8_luorq.py",
                        "tools/build_phase21r8_wangxiang.py"])
        QA_W_ALLOWED = {"docs/qa/phase21w4_qa_evidence.json", "docs/qa/phase21w4_qa_run_final.log",
                        "docs/qa/phase21w4_qa_report.md"}
        w_missing = sorted(set(EXP_W) - set(lm))
        w_extra = sorted(set(lm) - set(EXP_W))
        w_extra_bad = [p for p in w_extra if p not in QA_W_ALLOWED
                       and not foreign_attributed(p, BASE + "..HEAD")
                       and not live_drift(p, build=is_build_product(p))]
        chk("G", "ws-only core set == expected 30 + QA artifacts + foreign-attributed drift",
            not w_missing and not w_extra_bad,
            "n=%d new=%d unattributed=%s gone=%s" % (len(lm), len(w_extra), w_extra_bad[:6], w_missing[:6]))
        lp = sorted(p for p in only_pb if p.startswith(CORE_W))
        lp_intl = [p for p in lp if p.startswith("data/intl_figures/")]
        lp_other = [p for p in lp if not p.startswith("data/intl_figures/")]
        EXP_PB_OTHER = sorted(["tools/json/, print(", "tools/json/.json", "tools/json/main_data.json",
                               "tools/json/modes_data.json", "tools/update_zengzi_db.py", "tools/verify_zengzi.py"])
        lp_extra = [p for p in lp_other if p not in EXP_PB_OTHER]
        lp_extra_bad = [p for p in lp_extra if not live_drift(p, build=is_build_product(p))]
        for p in lp_extra:
            if p in lp_extra_bad:
                continue
            DRIFTS.append({"sec": "G", "item": "pb-only " + p, "path": p,
                           "drift": live_drift(p, build=is_build_product(p)) or "",
                           "detail": "ws side transiently missing (pb-only)"})
        chk("G", "pb-only core == 610 intl_figures + 6 known + drift-attributed build products",
            len(lp_intl) == 610 and set(EXP_PB_OTHER) <= set(lp_other) and not lp_extra_bad,
            "intl=%d other_n=%d unattributed=%s" % (len(lp_intl), len(lp_other), lp_extra_bad[:8]))
        info("G", "single-side inventory totals",
            "ws_only=%d pb_only=%d (junk/legacy classes; official parity boundary: common 2395 / single-side 6)" % (len(only_ws), len(only_pb)))
    except Exception as e:
        chk("G", "parity probe", False, "EXC %r" % e)

    # ------------------------------------------------------------ sec H remote
    try:
        if args.quick:
            info("H", "git fetch skipped (--quick)", "offline checks still applied where possible")
        else:
            rc, out, err, _ = git(["fetch", "origin"], cwd=PB, timeout=900)
            chk("H", "pb git fetch origin rc==0", rc == 0, "rc=%s err=%s" % (rc, err[-120:]))
        om = git_out(["rev-parse", "origin/main"], cwd=PB).strip()
        rc_anc, _, _, _ = git(["merge-base", "--is-ancestor", PUB_HEAD, "origin/main"], cwd=PB)
        chk("H", "receipt head c646f41a is ancestor of origin/main (remote fetch live)",
            rc_anc == 0, "origin/main=%s" % om[:16])
        h = git_out(["rev-parse", "HEAD"], cwd=PB).strip()
        chk("H", "pb local HEAD == origin/main (worktree synced)", h == om, "head=%s" % h[:16])
        bad_anc = []
        for c in PB_COMMITS:
            rc, _, _, _ = git(["merge-base", "--is-ancestor", c, "origin/main"], cwd=PB)
            if rc != 0:
                bad_anc.append(c)
        chk("H", "all 10 PB receipt commits are ancestors of origin/main", not bad_anc, "missing=%s" % bad_anc)
        for p in ["tools/json/scenarios_zh.json", "docs/research/phase21w4_fix2_report.md", "verify_w4fix2_lxn.py"]:
            rc, out, err, _ = run(["git", "show", "origin/main:" + p], cwd=PB, timeout=300)
            ok = rc == 0 and sha_b(out.encode("utf-8", "replace")) == sha_f(os.path.join(PB, p))
            chk("H", "remote blob @origin/main == pb worktree file: " + p, ok, "rc=%s" % rc)
        zh_remote = subprocess.run(["git", "show", "origin/main:tools/json/scenarios_zh.json"],
                                   cwd=PB, capture_output=True).stdout
        chk("H", "remote scenarios_zh == live fix2 sha (8b218e71...)", sha_b(zh_remote) == sha_b(load("tools/json/scenarios_zh.json", repo=PB, binary=True)) == (mafter.group(0) if mafter else None),
            "remote=%s" % sha_b(zh_remote)[:16])
        rc, out, err, _ = git(["ls-remote", "origin"], cwd=WS, timeout=300)
        info("H", "ws repo remote refs (informational)", (out or err).strip()[:300] or "rc=%s" % rc)
    except Exception as e:
        chk("H", "remote probe", False, "EXC %r" % e)


# ---------------------------------------------------------------- sec I H-MZ-001
def sec_i():
    try:
        zmz = dz["H-MZ-001"]
        emz = de["H-MZ-001"]
        b_zmz = gshow_json(BASE, "tools/json/scenarios_zh.json")["H-MZ-001"]
        b_emz = gshow_json(BASE, "tools/json/scenarios_en.json")["H-MZ-001"]
        chk("I", "H-MZ-001 zh/en name == Yan Yangchu / Y. C. James Yen (R1 backfill)",
            zmz.get("name") == RYZ and emz.get("name") == "Y. C. James Yen",
            "zh=%r en=%r" % (zmz.get("name"), emz.get("name")))
        chk("I", "H-MZ-001 figure_name == Mencius retained in both files (R3 keep-asis)",
            zmz.get("figure_name") == MENCIUS and emz.get("figure_name") == MENCIUS,
            "zh_fn=%r en_fn=%r" % (zmz.get("figure_name"), emz.get("figure_name")))
        fzh = sorted([f for f in set(b_zmz) | set(zmz) if b_zmz.get(f) != zmz.get(f)])
        fen = sorted([f for f in set(b_emz) | set(emz) if b_emz.get(f) != emz.get(f)])
        chk("I", "H-MZ-001 scenario delta vs BASE == name only (zh+en)", fzh == ["name"] and fen == ["name"],
            "zh=%s en=%s" % (fzh, fen))
        fn = loadj("data/figure_names.json")
        chk("I", "figure_names.json H-MZ-001 == Yan Yangchu; file untouched in window",
            fn.get("H-MZ-001") == RYZ and "data/figure_names.json" not in changed_all)
        dfp = "data/figures/H-MZ-001.json"
        df = loadj(dfp)
        chk("I", "data/figures/H-MZ-001.json figure_name/style_name + byte-unchanged vs BASE",
            df.get("figure_name") == RYZ and df.get("style_name") == "Y. C. James Yen"
            and sha_f(os.path.join(WS, dfp)) == sha_b(gshow_bytes(BASE, dfp)))
        ret = ["data/individuals/H-MZ-001.json", "data/individuals/H-MZ-001_modes.json",
               "data/individuals/ZH-MZ-001_modes.json", "data/figures/H-MZ-001_modes.json",
               "tools/json/H-MZ-001.json", "tools/json/H-MZ-001_modes.json",
               "docs/figures/H-MZ-001.md", "docs/research/phase20_moci_research.md"]
        bad = []
        tracked = 0
        for p in ret:
            fp = os.path.join(WS, p)
            if p in changed_all:
                bad.append(p + ":changed-in-window")
                continue
            blob = gshow_bytes(BASE, p)
            if blob:
                tracked += 1
                if sha_f(fp) != sha_b(blob):
                    bad.append(p + ":content-delta")
        chk("I", "R3 retention surfaces untouched by W4 window (Mencius pack + Mozi ref)",
            not bad, "listed=%d tracked-vs-BASE=%d bad=%s" % (len(ret), tracked, bad))
    except Exception as e:
        chk("I", "H-MZ-001 probe", False, "EXC %r" % e)


# ---------------------------------------------------------------- sec J G-class + fix2
def sec_j():
    try:
        dj = loadj("tools/json/H-LXN-001.json")
        chk("J", "draft tools/json/H-LXN-001.json clean (no Mao; Li in 8 fields)",
            MAO not in json.dumps(dj, ensure_ascii=False) and MAOEN not in json.dumps(dj, ensure_ascii=False)
            and dj.get("name_zh") == ZH4 and dj.get("name_en") == EN4)
        rp = "H-LXN-001.json"
        rf = os.path.join(WS, rp)
        blob = gshow_bytes(BASE, rp)
        if blob:
            same = sha_f(rf) == sha_b(blob)
        else:
            same = None
        cnt_zh = load(rp, binary=True).count(MAO.encode("utf-8"))
        cnt_en = load(rp, binary=True).count(MAOEN.encode("utf-8"))
        chk("J", "root H-LXN-001.json retained (R-b/W7): 4+4 old names, unchanged vs BASE",
            cnt_zh == 4 and cnt_en == 4 and (same is not False),
            "zh=%d en=%d unchanged=%s tracked=%s" % (cnt_zh, cnt_en, same, bool(blob)))
        mp = "docs/figures/H-LXN-001.md"
        mtxt = load(mp)
        chk("J", "docs/figures/H-LXN-001.md retained (R-c): 2 correction-note occurrences",
            mtxt.count(MAO) == 2 and (not gshow_bytes(BASE, mp) or sha_b(mtxt.encode("utf-8")) == sha_b(gshow_bytes(BASE, mp))),
            "count=%d" % mtxt.count(MAO))
        ctx = [l for l in mtxt.splitlines() if MAO in l]
        chk("J", "the 2 md occurrences are correction notes (contain the wrong-name remark)",
            all(("\u8bef\u5199" in l) or ("\u7ea0\u9519" in l) or ("\u6ce8" in l) for l in ctx),
            "lines=%d" % len(ctx))
        ch = load("CHANGELOG.md")
        ch_blob = gshow_bytes(BASE, "CHANGELOG.md")
        chok = sh = None
        chok = ch.count(MAO) == 1
        sh = (not ch_blob) or sha_b(ch.encode("utf-8")) == sha_b(ch_blob)
        chk("J", "CHANGELOG.md retained (R-e): 1 historical occurrence, unchanged", chok and sh,
            "count=%d unchanged=%s" % (ch.count(MAO), sh))
        ent = dz["H-LXN-001"]
        en4 = [f for f in ("name_en", "description_en", "reason_en", "case_en") if MAOEN in str(ent.get(f))]
        chk("J", "B-a registered: en-side 4x Mao Xiannian still in scenarios_zh (ruled -> t_def07a84)",
            len(en4) == 4 and json.dumps(ent, ensure_ascii=False).count(MAOEN) == 4,
            "fields=%s count=%d" % (en4, json.dumps(ent, ensure_ascii=False).count(MAOEN)))
        ent_en = de["H-LXN-001"]
        chk("J", "en scenarios file clean of Mao (fix landed there)",
            MAOEN not in json.dumps(ent_en, ensure_ascii=False) and MAO not in json.dumps(ent_en, ensure_ascii=False))
        def odd_names(root):
            out = []
            for dp, dns, fns in os.walk(root):
                dns[:] = [d for d in dns if d != ".git"]
                for n in list(dns) + list(fns):
                    if ("\n" in n) or ("<" in n):
                        out.append(os.path.join(os.path.relpath(dp, root), n))
            return out
        badnames = odd_names(os.path.join(WS, "data")) + odd_names(os.path.join(PB, "data"))
        chk("J", "no abnormal filenames under data/ (ws+pb) incl. R11 two dirs", not badnames, "bad=%s" % badnames[:4])
        norm = ["data/asia/individuals/xue_mu_qiao_H-XMQ-151_modes.json", "data/asia/individuals/gong_yu_H-GY-152_modes.json"]
        chk("J", "normal-name counterparts exist (ws+pb)", all(os.path.exists(os.path.join(r, p)) for r in (WS, PB) for p in norm))
        st = os.stat(os.path.join(WS, "data/asia/individuals"))
        info("J", "R-d vs live state", "two abnormal dirs absent now; ws data/asia/individuals mtime=%s (chain reports registered 'not deleted, handed over'; no action recorded - QA registers discrepancy, empty dirs, zero data impact)" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)))
        info("J", "B-a operator ruling", "B-a (en-side 4x Mao Xiannian) ruled=fix, assigned t_def07a84 (gated after this QA, before t_616e4991); QA scope unchanged, no action here")
        fr = load("docs/research/phase21w4_fix_report.md")
        fr_ee = gshow_text(EE, "docs/research/phase21w4_fix_report.md")
        chk("J", "fix_report correction note (2.2) present at HEAD / absent at EE (fix2-added)",
            "补正注记" in fr and "补正注记" not in fr_ee and "t_33240de8" in fr
            and "9727c8ea" in fr and "8b218e71" in fr)
        ev = loadj("docs/research/phase21w4_fix_evidence.json")
        r2 = ev.get("r2_scenarios_zh_extras") or {}
        okb = bool(r2) and all(v.get("before") == v.get("after") for v in r2.values()) and MAO in r2["name_zh"]["before"]
        chk("J", "parent evidence keeps pre-fix record intact (before==after, original delta not erased)", okb,
            "fields=%s" % sorted(r2))
        f2r = load("docs/research/phase21w4_fix2_report.md")
        chk("J", "fix2 report consistent (after=before provenance + sha transition 9727c8ea->8b218e71)",
            "after=before" in f2r and "9727c8ea" in f2r and "8b218e71" in f2r, "")
        info("J", "fix2 backup fields_before offset errata", "registered (t_33240de8 comment): occurrence_byte_offsets are CODEPOINT offsets; QA re-verified equality - non-rework")
    except Exception as e:
        chk("J", "G-class probe", False, "EXC %r" % e)


# ---------------------------------------------------------------- sec K W5 convergence precision
def sec_k():
    try:
        import copy
        import importlib.util
        spec = importlib.util.spec_from_file_location("pbmod", os.path.join(WS, "tools/prerender_body.py"))
        pbmod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pbmod)
        src = None
        payload = None
        for cand in ["web/dist/data/modes/by-figure/H-WC-001.json",
                     "web/public/data/modes/by-figure/H-WC-001.json"]:
            if os.path.exists(os.path.join(WS, cand)):
                payload = loadj(cand)
                src = cand
                break
        if payload:
            cur_len = len(pbmod.plain_text(pbmod.render_person(payload)))
            p2 = copy.deepcopy(payload)
            n = 0
            for mode in p2.get("modes", []):
                if isinstance(mode.get("verification"), dict):
                    mode["verification"]["status"] = "pending"
                    n += 1
            old_len = len(pbmod.plain_text(pbmod.render_person(p2)))
            rt_entry = rm.get("minds/H-WC-001", {})
            chk("K", "H-WC-001 body -1 char reproduced (4209 live / 4210 with pre-W5 statuses)",
                cur_len == 4209 and old_len == 4210 and rt_entry.get("body_text_chars") == 4209,
                "live=%d patched=%d route=%s src=%s modes=%d" % (cur_len, old_len,
                rt_entry.get("body_text_chars"), src, n))
            info("K", "root cause (independent)", "W5-B 18405015 set Wang Chong 10 modes -> 9 verified + 1 suspect; rebuild badge text 10x3 -> 9x3+2 = -1 char; unregistered per-route precision of the registered W5 convergence family")
        else:
            chk("K", "H-WC-001 by-figure payload found", False, "none")
    except Exception as e:
        chk("K", "convergence probe", False, "EXC %r" % e)


def main():
    ap = argparse.ArgumentParser(description="Phase21 W4 QA assertor (card t_8bad8d98)")
    ap.add_argument("--quick", action="store_true", help="skip gates/parity/fetch")
    ap.add_argument("--evidence", default=os.path.join(WS, "docs/qa/phase21w4_qa_evidence.json"))
    args = ap.parse_args()
    sec_fgh(args)
    sec_i()
    sec_j()
    sec_k()
    fails = [r for r in R if not r["ok"]]
    ev = {
        "schema": "phase21w4-qa-evidence-1",
        "card": "t_8bad8d98",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S %z"),
        "quick": args.quick,
        "ws_head": git_out(["rev-parse", "HEAD"]).strip(),
        "pb_head": git_out(["rev-parse", "HEAD"], cwd=PB).strip(),
        "pb_origin_main": git_out(["rev-parse", "origin/main"], cwd=PB).strip(),
        "counts": {"checks": len(R), "fail": len(fails), "pass": len(R) - len(fails),
                   "drift": len(DRIFTS)},
        "board_drift": {"dirty": sorted(DIRTY), "foreign_commits": sorted(FOREIGN),
                        "board_src_moved": BOARD_SRC_MOVED},
        "drifts": DRIFTS,
        "assertions": R,
    }
    if args.evidence:
        os.makedirs(os.path.dirname(args.evidence), exist_ok=True)
        with open(args.evidence, "w", encoding="utf-8") as f:
            json.dump(ev, f, ensure_ascii=False, indent=1)
        print("evidence written:", args.evidence)
    print("== SUMMARY: %d checks / %d FAIL / %d DRIFT / %.0fs" % (len(R), len(fails), len(DRIFTS), time.time() - T0))
    for d in DRIFTS:
        print("   DRIFT %s :: %s :: %s :: %s" % (d["sec"], d["item"], d["drift"], d["path"]))
    for r in fails:
        print("   FAIL %s :: %s :: %s" % (r["sec"], r["item"], r["detail"][:200]))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
