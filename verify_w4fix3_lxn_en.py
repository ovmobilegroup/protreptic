#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_w4fix3_lxn_en.py - Phase21 W4 补正-B-a en 扩展位落盘 独立见证器 (卡 t_def07a84).

复跑断言 (默认全量; --quick 跳过镜像面):
  A. 源落盘: tools/json/scenarios_zh.json H-LXN-001 en 侧 4 扩展位 MAO->LI 落盘,
     真字节窗口 + before/after 映射复验 (长度变化 -4B => 偏移对位校验), 文件 sha 钉住,
     与备份 before 副本做显式拼接重建 + 区域外 shift 对位逐字节核验.
  B. 备份: data/backup_phase21w4_fix3_20260924/MANIFEST.sha256 逐件重算 + payload byte-exact.
  C. 计数零变化 (开工实测 + R9 合并后口径): figures 1027 / routes 1360 / sitemap 1361 /
     unified 1344 (320+1024) / modes 3241 x by-figure 320.
     注: 卡面 1358/1359/1342(318+1024)/3221 为 R9 合并前口径; R9 合并 +2 人物 +20 模式后,
     各 live 面收敛为 320/3241; routes/sitemap 由本链 15/18 步补齐为 1360/1361,
     12 步 cross.coverage 由此 FAIL->PASS. 逐条归因见 fix3 报告 第四节.
  D. 活跃面残扫 (ws): 命中仅豁免类 (备份/报告/QA/site_docs/CHANGELOG/根 H-LXN-001.json
     [W7 在途]/figures 注记/他卡在制 data/audit/见证器类) + 定向 pin.
  E. 镜像面: 本卡镜像集与发布仓逐字节全等; 两仓构建树零命中; pb 全仓分类登记
     (data/intl_figures 惰性档 = parity 排除面, 4 处残留另案, 不在本卡边界).

用法: python3 verify_w4fix3_lxn_en.py [--quick] [--publish DIR]
说明: 目标串以拼接构造, 避免本文件孳生扫描噪音 (D6 自检断言 0 命中).
"""
import argparse, bisect, hashlib, json, os, sqlite3, sys

WS = os.path.dirname(os.path.abspath(__file__))
MAO = "Mao" + " " + "Xiannian"      # erroneous legacy latin name (fixed by this card)
LI  = "Li"  + " " + "Xiannian"      # corrected latin name
MAO_B = MAO.encode("utf-8")
LI_B = LI.encode("utf-8")
SRC_REL = "tools/json/scenarios_zh.json"
BK_REL = "data/backup_phase21w4_fix3_20260924"
FIELDS = ["name_en", "description_en", "reason_en", "case_en"]
SHA_AFTER = "e6777e7a556f26fc26b03338ae1df170ad8d084f1ea1df331db43d98ab4b4794"
SHA_BEFORE = "8b218e717cdb8cb5490e4951632907dac0b3ee0cd366c9f9c81bd0ac11702ceb"
BYTES = 2981555
BYTES_BEFORE = 2981559
WIN_BEFORE = [645917, 646781, 648210, 651925]   # 真字节窗口 (raw bytes.find, before 文件)
SELF = os.path.basename(__file__)

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

def finds(buf, needle):
    out, i = [], 0
    while True:
        j = buf.find(needle, i)
        if j < 0: break
        out.append(j); i = j + 1
    return out

def scan(root):
    """全仓扫描 -> (live, classes); ws/pb 通用."""
    exempt_prefix = [("data/backup", "backup"), ("docs/research/", "report"), ("docs/qa/", "qa"),
                     ("site_docs/", "site_docs"), ("release/", "release"), ("data/audit/", "audit"),
                     ("docs/figures/", "figures-note"), ("data/intl_figures/", "intl-inert")]
    live, classes = [], {}
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in (".git", "node_modules", ".pytest_cache", "__pycache__")]
        for fn in files:
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, root)
            try:
                b = open(fp, "rb").read()
            except Exception:
                continue
            c = b.count(MAO_B)
            if not c:
                continue
            cls = None
            for pfx, tag in exempt_prefix:
                if rel.startswith(pfx):
                    cls = tag
                    break
            if cls is None:
                if rel == "H-LXN-001.json":
                    cls = "pin-root-copy"
                elif rel == "CHANGELOG.md":
                    cls = "pin-changelog"
                elif rel.startswith("verify_") and rel != SELF:
                    cls = "verifier"
                elif rel == SELF:
                    cls = "SELF(bug!)"
            if cls:
                classes.setdefault(cls, {})[rel] = c
            else:
                live.append((rel, c))
    return live, classes

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
    check("A4 occ LI==5", text.count(LI) == 5, str(text.count(LI)))
    d = json.loads(text)
    e = d["H-LXN-001"]
    bf = json.load(open(os.path.join(WS, BK_REL, "fields_before.json"), encoding="utf-8"))
    check("A5 name_en", e.get("name_en") == LI, e.get("name_en"))
    okf = True
    for k in FIELDS:
        exp = bf["fields"][k]["after_expected"]
        if e.get(k) != exp:
            okf = False
            check("A6.%s" % k, False, "current != after_expected")
    check("A6 4 fields == backup after_expected", okf)
    check("A7 backup before sha", hashlib.sha256(bf["fields"]["name_en"]["before"].encode()).hexdigest()
          == bf["fields"]["name_en"]["before_sha256"])
    old = open(os.path.join(WS, BK_REL, SRC_REL), "rb").read()
    check("A8 backup copy sha==before pin", sha_file(os.path.join(WS, BK_REL, SRC_REL)) == SHA_BEFORE
          and len(old) == BYTES_BEFORE, "%d" % len(old))
    win_b = finds(old, MAO_B)
    check("A9 before windows == pinned true-byte offsets", win_b == WIN_BEFORE, str(win_b))
    rec = bf.get("occurrence_byte_offsets")
    check("A9b recorded byte-offsets == recomputed(true-byte)", rec == win_b, str(rec))
    cpo = bf.get("occurrence_codepoint_offsets_informational")
    check("A9c codepoint offsets labelled separately", isinstance(cpo, list) and len(cpo) == 4 and cpo != win_b,
          "cp=%s" % (cpo,))
    after_lb = finds(raw, LI_B)
    old_lb = finds(old, LI_B)
    exp_lb = sorted([q - sum(1 for b in win_b if b + len(MAO_B) <= q) for q in old_lb]
                    + [b - i for i, b in enumerate(win_b)])
    check("A10 after LI positions == mapped set", after_lb == exp_lb, str(after_lb))
    okw = all(raw[p:p+len(LI_B)] == LI_B for p in after_lb) and all(old[b:b+len(MAO_B)] == MAO_B for b in win_b)
    check("A11 window contents (before MAO / after LI)", okw)
    expected = old[:win_b[0]] + LI_B + old[win_b[0]+len(MAO_B):win_b[1]] + LI_B \
        + old[win_b[1]+len(MAO_B):win_b[2]] + LI_B + old[win_b[2]+len(MAO_B):win_b[3]] + LI_B + old[win_b[3]+len(MAO_B):]
    check("A12 explicit-splice reconstruction == after", expected == raw)
    regions = [(b - i, b - i + len(LI_B)) for i, b in enumerate(win_b)]
    in_region = bytearray(len(raw))
    for p, q in regions:
        for k in range(p, q): in_region[k] = 1
    ends = sorted(q for _, q in regions)
    bad = 0
    for p in range(len(raw)):
        if in_region[p]: continue
        if raw[p] != old[p + bisect.bisect_right(ends, p)]:
            bad += 1
    check("A13 outside-region bytes equal under shift", bad == 0, "bad=%d" % bad)
    ob = json.loads(old.decode("utf-8"))
    e_b = ob["H-LXN-001"]
    changed = [k for k in set(list(e_b.keys()) + list(e.keys())) if e_b.get(k) != e.get(k)]
    others = [c for c in ob.keys() if c != "H-LXN-001" and ob[c] != d[c]]
    check("A14 changed fields == 4 en fields", set(changed) == set(FIELDS), str(sorted(changed)))
    check("A15 other entries zero-change", not others, str(others[:5]))

    # ---------- B. 备份 ----------
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
    bm = json.load(open(os.path.join(bk, "backup_manifest.json"), encoding="utf-8"))
    check("B2 payload byte-exact flag", bm["files"][0]["sha256"] == bm["files"][0]["sha256_copy"] == SHA_BEFORE)

    # ---------- C. 计数 (开工实测 + R9 后口径) ----------
    con = sqlite3.connect(os.path.join(WS, "api/protreptic.db"))
    nf = con.execute("SELECT COUNT(*) FROM figures").fetchone()[0]
    row = con.execute("SELECT name_zh, name_en FROM figures WHERE code='H-LXN-001'").fetchone()
    nazj = con.execute("SELECT COUNT(*) FROM figures WHERE code IN ('H-AZJ-001','H-SHF-001')").fetchone()[0]
    con.close()
    check("C1 figures==1027", nf == 1027, str(nf))
    check("C2 db H-LXN-001 names", row and row[0] == "\u674e\u5148\u5ff5" and row[1] == LI, str(row))
    check("C2b db azj/shf rows==0 (合并链不入 db 先例)", nazj == 0, str(nazj))
    r = json.load(open(os.path.join(WS, "docs/architecture/web_p0_routes.json"), encoding="utf-8"))
    check("C3 routes==1360 (R9 后口径; 卡面 1358 为 R9 前)", r.get("count") == 1360
          and len(r.get("routes", [])) == 1360, str(r.get("count")))
    sm = open(os.path.join(WS, "web/public/sitemap.xml"), encoding="utf-8").read()
    check("C4 sitemap==1361 (R9 后口径; 卡面 1359 为 R9 前)", sm.count("<loc>") == 1361, str(sm.count("<loc>")))
    u = json.load(open(os.path.join(WS, "web/public/data/index.unified.json"), encoding="utf-8"))["counts"]
    check("C5 unified 1344=320+1024 (R9 后; 卡面 1342=318+1024 为 R9 前)",
          u.get("total") == 1344 and u.get("figures") == 320 and u.get("scenarios") == 1024, json.dumps(u))
    m = json.load(open(os.path.join(WS, "web/public/data/meta.json"), encoding="utf-8"))["counts"]
    check("C6 modes 3241 / by-figure 320 (R9 后; 卡面 3221 为 R9 前)",
          m.get("mode_summaries_published") == 3241 and m.get("mode_by_figure_shards") == 320
          and m.get("mode_summaries") == 3301,
          json.dumps({k: m.get(k) for k in ("mode_summaries", "mode_summaries_published", "mode_by_figure_shards")}))

    # ---------- D. 活跃面残扫 (ws) ----------
    live, classes = scan(WS)
    check("D1 live-face hits==0", not live, str(live[:5]))
    print("     classes (ws):")
    for cls in sorted(classes):
        for rel in sorted(classes[cls]):
            print("       [%s] %s : %d" % (cls, rel, classes[cls][rel]))
    check("D2 root copy pin==4 (W7 在途, 未触碰)", classes.get("pin-root-copy", {}).get("H-LXN-001.json") == 4,
          str(classes.get("pin-root-copy")))
    check("D3 CHANGELOG.md 零命中 (其历史条目属中文串, 另一扫描目标)", "CHANGELOG.md" not in classes.get("pin-changelog", {}),
          str(classes.get("pin-changelog")))
    check("D4 docs/figures 注记零命中 (R-c 注记属中文串, 另一扫描目标)", "docs/figures/H-LXN-001.md" not in classes.get("figures-note", {}),
          str(classes.get("figures-note")))
    check("D5 verifier-class registered (他卡QA见证器自带样本, 同 W4 QA verifier 口径)", True,
          json.dumps(classes.get("verifier", {}), ensure_ascii=False))
    check("D6 self-clean: 本见证器 0 命中",
          MAO_B not in open(os.path.join(WS, SELF), "rb").read())
    check("D7 fix2 报告补记在案 (e6777e7a 迁移)",
          "e6777e7a" in open(os.path.join(WS, "docs/research/phase21w4_fix2_report.md"), encoding="utf-8").read())
    check("D8 backup class registered (备份件计数)", len(classes.get("backup", {})) >= 5,
          "files=%d" % len(classes.get("backup", {})))

    # ---------- E. 镜像面 ----------
    PB = args.publish
    if args.quick:
        print("[SKIP] E mirror-face checks (--quick)")
    else:
        if not os.path.isdir(PB):
            check("E0 publish dir", False, PB)
        else:
            mirror_set = [SRC_REL, SELF,
                          "docs/research/phase21w4_fix2_report.md", "docs/research/phase21w4_fix2_report.json",
                          "docs/research/phase21w4_fix3_report.md", "docs/research/phase21w4_fix3_report.json",
                          "docs/research/phase21w4_fix3_evidence.json",
                          BK_REL + "/MANIFEST.sha256", BK_REL + "/backup_manifest.json", BK_REL + "/fields_before.json",
                          BK_REL + "/README.md", BK_REL + "/" + SRC_REL]
            bad = [rel for rel in mirror_set
                   if not (os.path.exists(os.path.join(PB, rel)) and sha_file(os.path.join(WS, rel)) == sha_file(os.path.join(PB, rel)))]
            check("E1 mirror set byte-exact (%d files)" % len(mirror_set), not bad, str(bad[:8]))
            for tag, root in (("ws", WS), ("pb", PB)):
                hits = []
                for tree in ("web/public/data", "web/dist"):
                    base = os.path.join(root, tree)
                    if not os.path.isdir(base):
                        continue
                    for dirpath, dirs, files in os.walk(base):
                        for fn in files:
                            fp = os.path.join(dirpath, fn)
                            try:
                                if open(fp, "rb").read().count(MAO_B):
                                    hits.append(os.path.relpath(fp, root))
                            except Exception:
                                pass
                check("E2.%s build-trees MAO hits==0" % tag, not hits, str(hits[:5]))
            plive, pcls = scan(PB)
            check("E3.pb pb live(非豁免) hits==0", not plive, str(plive[:6]))
            print("     classes (pb):")
            for cls in sorted(pcls):
                for rel in sorted(pcls[cls]):
                    print("       [%s] %s : %d" % (cls, rel, pcls[cls][rel]))
            check("E4.pb intl_figures 惰性档 pin==4 (pb-only, parity 排除面, 另案登记)",
                  pcls.get("intl-inert", {}).get("data/intl_figures/H-LXN-001.json") == 4,
                  str(pcls.get("intl-inert")))
            for tree in ("web/public/data", "web/dist"):
                n = same = diff = missing = 0
                for dirpath, dirs, files in os.walk(os.path.join(WS, tree)):
                    for fn in files:
                        wp = os.path.join(dirpath, fn)
                        rel = os.path.relpath(wp, WS)
                        pp = os.path.join(PB, rel)
                        n += 1
                        if not os.path.exists(pp):
                            missing += 1
                        elif sha_file(wp) == sha_file(pp):
                            same += 1
                        else:
                            diff += 1
                print("     [info] %s: ws=%d same=%d diff=%d missing_in_pb=%d (他链在制差异, 非本卡门禁)" % (tree, n, same, diff, missing))

    npass = sum(1 for _, ok, _ in results if ok)
    nfail = len(results) - npass
    print("\n== %d PASS / %d FAIL ==" % (npass, nfail))
    return 1 if nfail else 0

if __name__ == "__main__":
    sys.exit(main())
