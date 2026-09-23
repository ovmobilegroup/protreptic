#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_w4fix2_lxn.py - Phase21 W4 补正·R2 zh 扩展位落盘 独立见证器 (卡 t_33240de8).

复跑断言 (默认全量; --quick 跳过镜像面):
  A. 源落盘: tools/json/scenarios_zh.json H-LXN-001 4 扩展位 MAO->LI 落盘,
     等长最小 diff (4x2B), 文件 sha 钉住, 与备份 before 副本逐字节 diff 结构核对.
  B. 备份: data/backup_phase21w4_fix2_20260924/MANIFEST.sha256 逐件重算.
  C. 计数零变化: figures 1027 / routes 1358 / sitemap 1359 / unified 1342(318+1024) / modes 3221.
  D. 活跃面残扫: 目标串 (MAO) 在 tools/ web/ api/ docs/architecture/ data/(非备份) = 0;
     余量仅豁免类 (备份/报告/CHANGELOG/根副本/figures 注记).
  E. 镜像面: web/public/data + web/dist 与发布仓逐字节全等 + 本卡镜像件全等.

用法: python3 verify_w4fix2_lxn.py [--quick] [--publish DIR]
说明: 目标串以 unicode 转义构造, 避免本文件孳生扫描噪音.
"""
import argparse, hashlib, json, os, sqlite3, sys

WS = os.path.dirname(os.path.abspath(__file__))
MAO = "\u6bdb\u5148\u5ff5"        # erroneous legacy given name (target of the fix)
LI = "\u674e\u5148\u5ff5"         # corrected given name
MAO_B = MAO.encode("utf-8")
LI_B = LI.encode("utf-8")
SRC_REL = "tools/json/scenarios_zh.json"
BK_REL = "data/backup_phase21w4_fix2_20260924"
FIELDS = ["name_zh", "description_zh", "reason_zh", "case_zh"]
SHA_AFTER = "8b218e717cdb8cb5490e4951632907dac0b3ee0cd366c9f9c81bd0ac11702ceb"
SHA_BEFORE = "9727c8eaaf96ab92899a26409f949ff4caf3c1bf10c363acc2b58b33da54e470"
BYTES = 2981559

results = []

def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))

def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--publish", default="/opt/data/release/Protreptic-publish")
    args = ap.parse_args()

    # ---------- A. 源落盘 ----------
    raw = open(os.path.join(WS, SRC_REL), "rb").read()
    text = raw.decode("utf-8")
    check("A1 file sha256", sha_file(os.path.join(WS, SRC_REL)) == SHA_AFTER, sha_file(os.path.join(WS, SRC_REL))[:16])
    check("A2 file bytes", len(raw) == BYTES, str(len(raw)))
    check("A3 occ MAO==0", text.count(MAO) == 0, str(text.count(MAO)))
    check("A4 occ LI==34", text.count(LI) == 34, str(text.count(LI)))
    d = json.loads(text)
    e = d["H-LXN-001"]
    check("A5 name", e.get("name") == LI, e.get("name"))
    bf = json.load(open(os.path.join(WS, BK_REL, "fields_before.json"), encoding="utf-8"))
    okf = True
    for k in FIELDS:
        exp = bf["fields"][k]["after_expected"]
        if e.get(k) != exp:
            okf = False
            check("A6.%s" % k, False, "current != after_expected")
    check("A6 4 fields == backup after_expected", okf)
    check("A7 backup before sha", hashlib.sha256(bf["fields"]["name_zh"]["before"].encode()).hexdigest()
          == bf["fields"]["name_zh"]["before_sha256"])
    # diff structure vs backup copy
    old = open(os.path.join(WS, BK_REL, SRC_REL), "rb").read()
    check("A8 backup copy sha==before pin", sha_file(os.path.join(WS, BK_REL, SRC_REL)) == SHA_BEFORE)
    win, i = [], 0
    while True:
        j = old.find(MAO_B, i)
        if j < 0:
            break
        win.append((j, j + len(MAO_B)))
        i = j + 1
    check("A9 before windows==4", len(win) == 4, str(win))
    runs, prev = [], None
    for k in range(min(len(old), len(raw))):
        if old[k] != raw[k]:
            if prev is not None and k == prev + 1:
                runs[-1][1] = k
            else:
                runs.append([k, k])
            prev = k
    check("A10 diff runs==4, width 2 each", len(runs) == 4 and all(r[1] - r[0] == 1 for r in runs), str(runs))
    inside = all(any(w[0] <= a and b < w[1] for w in win) for a, b in runs)
    check("A11 diff runs all inside windows", inside)
    check("A12 old/new same length", len(old) == len(raw))

    # ---------- B. 备份 MANIFEST ----------
    bk = os.path.join(WS, BK_REL)
    man = os.path.join(bk, "MANIFEST.sha256")
    if os.path.exists(man):
        n = ok = 0
        for line in open(man, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            s, rel = line.split("  ", 1)
            n += 1
            ok += (sha_file(os.path.join(bk, rel)) == s)
        check("B1 MANIFEST.sha256 %d/%d" % (ok, n), ok == n)
    else:
        check("B1 MANIFEST exists", False)

    # ---------- C. 计数零变化 ----------
    con = sqlite3.connect(os.path.join(WS, "api/protreptic.db"))
    nf = con.execute("SELECT COUNT(*) FROM figures").fetchone()[0]
    row = con.execute("SELECT name_zh FROM figures WHERE code='H-LXN-001'").fetchone()
    con.close()
    check("C1 figures==1027", nf == 1027, str(nf))
    check("C2 db H-LXN-001 name_zh==LI", row and row[0] == LI, str(row))
    r = json.load(open(os.path.join(WS, "docs/architecture/web_p0_routes.json"), encoding="utf-8"))
    check("C3 routes==1358", r.get("count") == 1358 and len(r.get("routes", [])) == 1358, str(r.get("count")))
    sm = open(os.path.join(WS, "web/public/sitemap.xml"), encoding="utf-8").read()
    check("C4 sitemap==1359", sm.count("<loc>") == 1359, str(sm.count("<loc>")))
    u = json.load(open(os.path.join(WS, "web/public/data/index.unified.json"), encoding="utf-8"))["counts"]
    check("C5 unified 1342=318+1024", u.get("total") == 1342 and u.get("figures") == 318 and u.get("scenarios") == 1024, json.dumps(u))
    m = json.load(open(os.path.join(WS, "web/public/data/meta.json"), encoding="utf-8"))["counts"]
    check("C6 modes 3221 / by-figure 318", m.get("mode_summaries_published") == 3221 and m.get("mode_by_figure_shards") == 318, "")

    # ---------- D. 活跃面残扫 ----------
    exempt_prefix = ("data/backup", "docs/research/", "docs/qa/", "site_docs/", "release/", ".git/")
    live_hits, exempt_hits = [], {}
    for dirpath, dirs, files in os.walk(WS):
        dirs[:] = [x for x in dirs if x not in (".git", "node_modules", ".pytest_cache", "__pycache__", ".ogvenv", ".mkdocsvenv")]
        for fn in files:
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, WS)
            try:
                b = open(fp, "rb").read()
            except Exception:
                continue
            cnt = b.count(MAO_B)
            if cnt == 0:
                continue
            if rel.startswith(exempt_prefix) or rel in ("CHANGELOG.md", "H-LXN-001.json", "docs/figures/H-LXN-001.md"):
                exempt_hits[rel] = cnt
            else:
                live_hits.append((rel, cnt))
    check("D1 live-face hits==0", not live_hits, str(live_hits[:5]))
    print("     exempt-face hits (%d files):" % len(exempt_hits))
    for k in sorted(exempt_hits):
        print("       %s : %d" % (k, exempt_hits[k]))
    # pinned expectations for key exempt files
    check("D2 root copy==4", exempt_hits.get("H-LXN-001.json") == 4, str(exempt_hits.get("H-LXN-001.json")))
    check("D3 CHANGELOG==1", exempt_hits.get("CHANGELOG.md") == 1, str(exempt_hits.get("CHANGELOG.md")))
    check("D4 figures md==2", exempt_hits.get("docs/figures/H-LXN-001.md") == 2, str(exempt_hits.get("docs/figures/H-LXN-001.md")))

    # ---------- E. 镜像面 ----------
    if args.quick:
        print("[SKIP] E mirror-face checks (--quick)")
    else:
        PB = args.publish
        if not os.path.isdir(PB):
            check("E0 publish dir", False, PB)
        else:
            for tree in ("web/public/data", "web/dist"):
                n = same = 0
                diffs = []
                for dirpath, dirs, files in os.walk(os.path.join(WS, tree)):
                    for fn in files:
                        wp = os.path.join(dirpath, fn)
                        rel = os.path.relpath(wp, WS)
                        pp = os.path.join(PB, rel)
                        n += 1
                        if os.path.exists(pp) and sha_file(wp) == sha_file(pp):
                            same += 1
                        else:
                            diffs.append(rel)
                check("E1 %s %d/%d byte-identical" % (tree, same, n), same == n, str(diffs[:5]))
            mirror_set = [SRC_REL, "verify_w4fix2_lxn.py", "docs/research/phase21w4_fix_report.md",
                          "docs/research/phase21w4_fix2_report.md", "docs/research/phase21w4_fix2_report.json",
                          BK_REL + "/MANIFEST.sha256", BK_REL + "/backup_manifest.json", BK_REL + "/fields_before.json",
                          BK_REL + "/README.md", BK_REL + "/" + SRC_REL]
            bad = [rel for rel in mirror_set if not (os.path.exists(os.path.join(PB, rel)) and sha_file(os.path.join(WS, rel)) == sha_file(os.path.join(PB, rel)))]
            check("E2 mirror set byte-exact", not bad, str(bad[:6]))

    npass = sum(1 for _, ok, _ in results if ok)
    nfail = len(results) - npass
    print("\n== %d PASS / %d FAIL ==" % (npass, nfail))
    return 1 if nfail else 0

if __name__ == "__main__":
    sys.exit(main())
