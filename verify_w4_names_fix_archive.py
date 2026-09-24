#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_w4_names_fix_archive.py - Phase21-W4 九节档案独立验收（第二实现；卡 t_616e4991）

第二实现: 不导入 build_w4_names_fix_archive.py；独立读取 报告 + 两仓字节 + git 对象 + 上游数据。
段目:
  A 档案结构（九节/终表 48 码/R1-R12/镜像清单）
  B 镜像面（R-a 6 + QA 2 + 根见证器 + 本档三件：两仓 byte-exact）
  C 提交链（报告登记逐条 git 实测可解 + 全号一致）
  D 数据逐字核对（16 H-* + 5 码族 vs scenarios 双源；清档 0 残留；错名 0 命中；计数与备份复核）
  E 记录面（R-a/R-b/R-c/R-d、船长收口、回执节）
  F 反向注入自检（--inject-test：突变注入 -> 断言被捕获）

用法:
  python3 verify_w4_names_fix_archive.py                 # 全量（写证据 JSON）
  python3 verify_w4_names_fix_archive.py --no-evidence
  python3 verify_w4_names_fix_archive.py --inject-test
  python3 verify_w4_names_fix_archive.py --workspace DIR --publish DIR
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile

WS_DEFAULT = "/opt/data/workspace/Protreptic"
PB_DEFAULT = "/opt/data/release/Protreptic-publish"
REPORT_REL = "docs/research/phase21w4_names_fix_archive_report.md"
EVIDENCE_REL = "docs/research/phase21w4_names_fix_archive_evidence.json"

MIRROR_RELS = [
    "docs/research/phase21r8_w4_names_recon.md",
    "docs/research/phase21r8_w4_names_recon.json",
    "docs/research/phase21w4_fix_manifest.md",
    "docs/research/phase21w4_fix_manifest.json",
    "docs/research/phase21w6_marker_scan.md",
    "docs/research/phase21w6_marker_scan.json",
    "docs/qa/phase21w4_qa_report.md",
    "docs/qa/phase21w4_qa_evidence.json",
    "verify_phase21w4_qa_espinosa.py",
]
OWN_RELS = [
    REPORT_REL,
    "verify_w4_names_fix_archive.py",
]
DISP16 = {
    "H-HYP-145": ("黄炎培", "Huang Yanpei"),
    "H-WYX-146": ("吴有训", "Wu Youxun"),
    "H-WX-147": ("王选", "Wang Xuan"),
    "H-YLP-148": ("袁隆平", "Yuan Longping"),
    "H-SY-149": ("粟裕", "Su Yu"),
    "H-XMQ-151": ("薛暮桥", "Xue Muqiao"),
    "H-CY-159": ("陈毅", "Chen Yi"),
    "H-LXN-347": ("李先念", "Li Xiannian"),
    "H-LXN-001": ("李先念", "Li Xiannian"),
    "H-IKD-160": ("伊本·赫勒敦", "Ibn Khaldun"),
    "H-ISC-362": ("阿维森纳（伊本·西那）", "Avicenna (Ibn Sina)"),
    "H-GHZ-163": ("安萨里", "Al-Ghazali"),
    "H-SUF-364": ("鲁米（贾拉勒丁·鲁米）", "Rumi (Jalal al-Din Rumi)"),
    "H-ZEL-001": ("周恩来", "Zhou Enlai"),
    "H-HLG-001": ("华罗庚", "Hua Luogeng"),
    "H-MZ-001": ("晏阳初", "Y. C. James Yen"),
}
DISP5 = {
    "SG-LEE-001": ("李光耀", "Lee Kuan Yew"),
    "MY-MAH-001": ("马哈蒂尔", "Mahathir Mohamad"),
    "JP-SAS-001": ("西乡隆盛", "Saigō Takamori"),
    "UZ-ULU-001": ("乌鲁格别克", "Ulugh Beg"),
    "RW-KAG-001": ("卡加梅", "Paul Kagame"),
}
CLEARED = ["SG-Lee-001", "MY-Mah-001", "JP-Sas-001", "UZ-Ulu-001"] + ["RW-KAG-%d" % i for i in range(1, 28)]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_A(text):
    fails = []
    heads = ["## 一、概述", "## 二、背景", "## 三、方法", "## 四、执行（登记链）", "## 五、证据",
             "## 六、核验", "## 七、残留与账务登记", "## 八、下一步", "## 九、附链（全号索引与复跑）"]
    for h in heads:
        if h not in text:
            fails.append("missing section: %s" % h)
    n_sec = len(re.findall(r"^## ", text, re.M))
    if n_sec != 9:
        fails.append("section count != 9: %d" % n_sec)
    for sub in ["### 4.1", "### 4.4", "#### 4.4.1", "#### 4.4.2", "#### 4.4.3", "### 4.5", "### 4.7"]:
        if sub not in text:
            fails.append("missing subsection: %s" % sub)
    for code in DISP16:
        if not re.search(r"^\| %s \| " % re.escape(code), text, re.M):
            fails.append("16-table row missing: %s" % code)
    for i in range(1, 28):
        if ("| RW-KAG-%d |" % i) not in text:
            fails.append("RW row missing: RW-KAG-%d" % i)
    for fam in ["SG-LEE-001", "MY-MAH-001", "JP-SAS-001", "UZ-ULU-001", "RW-KAG-001"]:
        if fam not in text:
            fails.append("family token missing: %s" % fam)
    for i in range(1, 13):
        if not re.search(r"^\| R%d \| " % i, text, re.M):
            fails.append("ruling row missing: R%d" % i)
    for token in ["4 字段补正", "t_33240de8", "t_def07a84", "t_8bad8d98", "t_ee203180", "t_536073f4",
                  "t_24b92f58", "t_10a42b2a", "t_616e4991"]:
        if token not in text:
            fails.append("token missing: %s" % token)
    for rel in MIRROR_RELS:
        if rel not in text:
            fails.append("mirror rel missing: %s" % rel)
    return fails


CONN_CLOSE = re.compile(r"^\|\s*(\d+)\s*\|\s*([0-9a-f]{8})\s*\|\s*([0-9a-f]{40})\s*\|\s*(\d\d-\d\d \d\d:\d\d)\s*\|\s*(t_[0-9a-z]+|—|船长)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", re.M)


def check_C(text, ws, pb):
    fails = []
    pairs = re.findall(r"\| (ws|pb) \| `([0-9a-f]{7,8})` \| `([0-9a-f]{40})` \|", text)
    n_ws = sum(1 for p in pairs if p[0] == "ws")
    n_pb = sum(1 for p in pairs if p[0] == "pb")
    if n_ws < 19:
        fails.append("ws commit rows < 19: %d" % n_ws)
    if n_pb < 13:
        fails.append("pb commit rows < 13: %d" % n_pb)
    for kind, short, full in pairs:
        repo = ws if kind == "ws" else pb
        rc, out, _ = git(repo, "rev-parse", "--verify", full + "^{commit}")
        if rc != 0:
            fails.append("unresolvable commit: %s %s" % (kind, full))
        elif out != full:
            fails.append("commit mismatch: %s %s -> %s" % (kind, full, out))
        elif out[:len(short)] != short:
            fails.append("short/full prefix mismatch: %s %s" % (short, full))
    anchors = [("ws", "40320e37"), ("ws", "8a0ac56d"), ("ws", "2de84904"), ("ws", "bf177cda"), ("pb", "06c0637")]
    for kind, short in anchors:
        if short not in text:
            fails.append("anchor missing from text: %s %s" % (kind, short))
        repo = ws if kind == "ws" else pb
        rc, out, _ = git(repo, "rev-parse", "--verify", short + "^{commit}")
        if rc != 0:
            fails.append("anchor unresolvable: %s %s" % (kind, short))
    return fails


def check_B(ws, pb):
    fails = []
    rows = []
    rels = list(MIRROR_RELS) + list(OWN_RELS)
    if os.path.exists(os.path.join(ws, EVIDENCE_REL)):
        rels.append(EVIDENCE_REL)
    for rel in rels:
        wpath = os.path.join(ws, rel)
        ppath = os.path.join(pb, rel)
        row = dict(rel=rel, ws_exists=os.path.exists(wpath), pb_exists=os.path.exists(ppath))
        if not row["ws_exists"]:
            fails.append("workspace file missing: %s" % rel)
        if not row["pb_exists"]:
            fails.append("publish file missing: %s" % rel)
        if row["ws_exists"] and row["pb_exists"]:
            hw = sha256_file(wpath)
            hp = sha256_file(ppath)
            row["ws_sha256"] = hw
            row["pb_sha256"] = hp
            row["equal"] = (hw == hp)
            if not row["equal"]:
                fails.append("byte mismatch: %s" % rel)
        rows.append(row)
    return fails, rows


def check_D(text, ws):
    fails = []
    z = load_json(os.path.join(ws, "tools/json/scenarios_zh.json"))
    e = load_json(os.path.join(ws, "tools/json/scenarios_en.json"))
    for code, (zh, en) in DISP16.items():
        m = re.search(r"^\| %s \| ([^|]+?) \| ([^|]+?) \| " % re.escape(code), text, re.M)
        if not m:
            fails.append("report row unparsable: %s" % code)
            continue
        rz, re_ = m.group(1).strip(), m.group(2).strip()
        if rz != zh or re_ != en:
            fails.append("report row value drift: %s (%s/%s)" % (code, rz, re_))
        if z.get(code, {}).get("name") != zh:
            fails.append("scen_zh name mismatch: %s" % code)
        if e.get(code, {}).get("name") != en:
            fails.append("scen_en name mismatch: %s" % code)
    for code, (zh, en) in DISP5.items():
        if z.get(code, {}).get("name") != zh:
            fails.append("scen_zh family name mismatch: %s" % code)
        if e.get(code, {}).get("name") != en:
            fails.append("scen_en family name mismatch: %s" % code)
        if code not in text:
            fails.append("family token missing in report: %s" % code)
    for c in CLEARED:
        if c in z:
            fails.append("cleared code present in scen_zh: %s" % c)
        if c in e:
            fails.append("cleared code present in scen_en: %s" % c)
    zraw = open(os.path.join(ws, "tools/json/scenarios_zh.json"), encoding="utf-8").read()
    eraw = open(os.path.join(ws, "tools/json/scenarios_en.json"), encoding="utf-8").read()
    for token in ("毛先念", "Mao Xiannian"):
        if token in zraw:
            fails.append("wrong-name residual in scen_zh: %s" % token)
        if token in eraw:
            fails.append("wrong-name residual in scen_en: %s" % token)
    con = sqlite3.connect(os.path.join(ws, "api/protreptic.db"))
    try:
        n_fig = con.execute("SELECT COUNT(*) FROM figures").fetchone()[0]
        row = con.execute("SELECT name_zh, name_en FROM figures WHERE code='H-LXN-001'").fetchone()
    finally:
        con.close()
    if n_fig != 1027:
        fails.append("DB figures != 1027: %s" % n_fig)
    if row != ("李先念", "Li Xiannian"):
        fails.append("DB H-LXN-001 row mismatch: %s" % (row,))
    with open(os.path.join(ws, "docs/architecture/web_p0_routes.json"), encoding="utf-8") as f:
        routes = len(load_json_fileobj(f)["routes"])
    sm = open(os.path.join(ws, "web/public/sitemap.xml"), encoding="utf-8").read().count("<url>")
    up = os.path.join(ws, "web/public/data/index.unified.json")
    unified = len(load_json(up)["items"]) if os.path.exists(up) else None
    live = {"figures": n_fig, "routes": routes, "sitemap": sm, "unified": unified}
    for key, pat in [("routes（web_p0_routes.json）", "routes"), ("sitemap（web/public/sitemap.xml <url>）", "sitemap"),
                     ("unified（index.unified.json items）", "unified"), ("figures（DB 行）", "figures")]:
        m = re.search(r"^\| %s \| (\d+) \| ([^|]+?) \|" % re.escape(key), text, re.M)
        if not m:
            fails.append("counts row unparsable: %s" % key)
            continue
        shown = m.group(2).strip()
        actual = live[pat]
        if actual is None:
            if shown != "（不重算）":
                fails.append("unified None but report shows: %s" % shown)
        elif str(actual) != shown:
            fails.append("counts drift %s: report=%s live=%s" % (key, shown, actual))
    return fails


def load_json_fileobj(f):
    return json.load(f)


def check_E(text):
    fails = []
    for token in ["R-a", "R-b", "R-c", "R-d", "船长已收口", "bf177cda", "06c0637", "W7", "Phase46-R",
                  "ws_commit_v1", "push_v1", "remote_main", "parity_final", "verify_result",
                  "site_docs", "candidates_v5_research.md"]:
        if token not in text:
            fails.append("token missing: %s" % token)
    return fails


def selftest(text, ws, pb):
    """反向注入自检: 对档案文本做 5 类突变, 断言对应段必须捕获."""
    results = []
    t = text.replace("## 七、残留与账务登记", "# mutated-header")
    results.append(("inject:del-section7", len(check_A(t)) > 0))
    pairs = re.findall(r"\| (ws|pb) \| `([0-9a-f]{7,8})` \| `([0-9a-f]{40})` \|", text)
    if pairs:
        bad_full = pairs[-1][2][:-1] + ("0" if pairs[-1][2][-1] != "0" else "1")
        t = text.replace(pairs[-1][2], bad_full)
        results.append(("inject:bad-sha", len(check_C(t, ws, pb)) > 0))
    else:
        results.append(("inject:bad-sha", False))
    t = text.replace("| H-LXN-001 | 李先念 |", "| H-LXN-001 | 李先念X |")
    results.append(("inject:value-drift", len(check_D(t, ws)) > 0))
    t = text.replace("船长已收口", "船长未收口")
    results.append(("inject:caption-lost", len(check_E(t)) > 0))
    with tempfile.TemporaryDirectory() as td:
        fails, _ = check_B(ws, td)
        results.append(("inject:pb-missing", len(fails) > 0))
    return results


def run(ws, pb, write_evidence, inject, allow_pending_pb):
    report_path = os.path.join(ws, REPORT_REL)
    if not os.path.exists(report_path):
        print("REPORT MISSING: %s" % report_path)
        return 1
    text = open(report_path, encoding="utf-8").read()
    allf = {}
    allf["A"] = check_A(text)
    bfails, brows = check_B(ws, pb)
    allf["B"] = bfails
    allf["C"] = check_C(text, ws, pb)
    allf["D"] = check_D(text, ws)
    allf["E"] = check_E(text)
    st = None
    if inject:
        st = selftest(text, ws, pb)
        allf["F"] = [name for name, ok in st if not ok]
    hard = ["A", "C", "D", "E"] + (["F"] if inject else [])
    nfail = sum(len(allf[k]) for k in hard)
    soft_bfail = len(bfails) if allow_pending_pb else 0
    for k in ["A", "B", "C", "D", "E"] + (["F"] if inject else []):
        tag = "PASS" if not allf[k] else "FAIL"
        if k == "B" and allow_pending_pb:
            tag = "SOFT" if allf[k] else "PASS"
        print("sec %s: %s (%d)" % (k, tag, len(allf[k])))
        for m in allf[k][:8]:
            print("   - %s" % m)
    if st:
        for name, ok in st:
            print("selftest %s: %s" % ("PASS" if ok else "FAIL", name))
    nfail_total = nfail + (0 if allow_pending_pb else len(bfails))
    if write_evidence:
        ev = dict(card="t_616e4991", report_rel=REPORT_REL, report_sha256=sha256_file(report_path),
                  note="evidence.json 自身两仓 byte-exact 相等性由最终 no-write 复跑复核（结果记录于卡面完成 metadata）",
                  sections={k: allf[k] for k in allf}, mirror=brows, selftest=st,
                  ws_root=ws, pb_root=pb)
        with open(os.path.join(ws, EVIDENCE_REL), "w", encoding="utf-8") as f:
            json.dump(ev, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("EVIDENCE WRITTEN: %s" % EVIDENCE_REL)
    if nfail_total == 0:
        print("VERIFY: ALL PASS (0 FAIL%s)" % (", pending-pb tolerated" if soft_bfail else ""))
        return 0
    print("VERIFY: %d FAIL" % nfail_total)
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="W4 archive independent verifier (second implementation)")
    ap.add_argument("--workspace", default=WS_DEFAULT)
    ap.add_argument("--publish", default=PB_DEFAULT)
    ap.add_argument("--no-evidence", action="store_true")
    ap.add_argument("--inject-test", action="store_true")
    ap.add_argument("--allow-pending-pb", action="store_true")
    args = ap.parse_args(argv)
    return run(args.workspace, args.publish, not args.no_evidence, args.inject_test, args.allow_pending_pb)


if __name__ == "__main__":
    sys.exit(main())
