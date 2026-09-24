#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_w9_fclass_archive.py - Phase21-W9 F类回填·链级档案独立验收（第二实现；卡 t_9cb09b90）

体例先例: verify_w8_stage2_batch1_archive.py / verify_w4_names_fix_archive.py。
不 import 生成器（build_w9_fclass_archive.py）；全部事实独立重算（git 对象 / 文件字节 / DB 行读 / 工具现跑）。

段目:
  A 档案结构（九节 + 关键 token + 计数恒等式 + 卡号引用）
  B 镜像面（本档 3 件 byte-exact + pb 三笔提交级 blob 对照 + 执行链镜像缺失登记）
  C 提交链（ws 4 笔 / pb 3 笔逐条 git 实测；短号->全号->日期；锚点与卡链）
  D 链数据面（8 件 sha16 双仓 + 5 件三段 pin + W9 备份 + W7 前像 1303 子集 + 删除面对账 + 547 台账含 400/104 分层）
  E 记录面（QA 指纹 + 未闭合项照登 + 回执区自洽与 v1 提交件集）
  F 反向注入自检（6 类突变，逐类必被捕获）

用法:
  python3 verify_w9_fclass_archive.py                      # 验收 + 写证据（含 --receipts-pending / --mirror-pending 过渡轮）
  python3 verify_w9_fclass_archive.py --with-live          # 额外采集 parity / ls-remote 快照（不进证据稳定性面时慎用）
退出码: 0 全绿；1 存在 FAIL。
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys

WS_DEFAULT = "/opt/data/workspace/Protreptic"
PB_DEFAULT = "/opt/data/release/Protreptic-publish"
REPORT_REL = "docs/research/phase21w9_fclass_archive_report.md"
EVIDENCE_REL = "docs/research/phase21w9_fclass_archive_evidence.json"
GEN_REL = "build_w9_fclass_archive.py"
VER_REL = "verify_w9_fclass_archive.py"
QA_REPORT = "docs/research/phase21w9_fclass_qa_report_espinosa.md"
QA_EVIDENCE = "docs/research/phase21w9_fclass_qa_evidence_espinosa.json"
QA_VER = "verify_w9_fclass_qa_espinosa.py"
RECON_MD = "docs/research/phase21r8_w4_names_recon.md"
RECON_JSON = "docs/research/phase21r8_w4_names_recon.json"
W7_CLASS = "data/audit/phase21w7_classification.json"
ZH_JSON = "tools/json/scenarios_zh.json"
DB_REL = "api/protreptic.db"
IDX_REL = "web/public/data/figures.index.json"
UNI_REL = "web/public/data/index.unified.json"
MAN_REL = "docs/architecture/static_data_manifest.json"
W9_BACKUP = "api/protreptic.db.backup_phase21w9_20260924_140928"
W7_BACKUP_DIR = "data/backup_phase21w7_clean_20260924"

AT = "e5ddd13f"
PARENT = "ee08f5b5"
RECON = "8adbdabd"
WS_COMMITS = ["e5ddd13f", "c6d626c6", "1e6f14eb", "4975cd26"]
PB_COMMITS = ["6b50893", "ad27e1a", "3129539"]
PB_ALIGN = {"6b50893": "c6d626c6", "ad27e1a": "1e6f14eb", "3129539": "4975cd26"}
ANCHORS = ["e5ddd13f", "ee08f5b5", "8adbdabd", "c6d626c6", "1e6f14eb", "4975cd26", "6b50893", "ad27e1a", "3129539",
           "39e3eb21", "b44ba0a3", "0683505", "e32cb3b"]
TEN = ["BW-KHA-001", "NA-NUJ-001", "SZ-MSW-001", "ZW-MUG-001", "ZA-ZUM-001",
       "BW-MAS-001", "LS-MOS-001", "MG-RAV-001", "NA-GEO-001", "ZW-CHA-001"]

SHA16_EXPECT = {
    RECON_MD: (None, None), RECON_JSON: (None, None),
    QA_REPORT: ("a7235a94bd9e2aff", "a7235a94bd9e2aff"),
    QA_EVIDENCE: ("2deae7f546a10ff9", "2deae7f546a10ff9"),
    QA_VER: ("43220de86df64cfd", "43220de86df64cfd"),
    W7_CLASS: (None, None),
    IDX_REL: ("65a7cdc65ed930f3", "65a7cdc65ed930f3"),
    DB_REL: ("c4a89a2329b6690b", "c5eb126e93f88757"),
}
PINS_EXPECT = [
    (DB_REL, "c5eb126e93f88757", "c4a89a2329b6690b"),
    (MAN_REL, "abf786227c7757c6", "abf786227c7757c6"),
    (ZH_JSON, "e6777e7a556f26fc", "e6777e7a556f26fc"),
    (IDX_REL, None, "65a7cdc65ed930f3"),
    (UNI_REL, None, "27da3e7a7dfdfa8f"),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha16(path):
    return sha256_file(path)[:16]


def sh(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError("cmd failed: %s\n%s" % (" ".join(cmd), r.stderr.strip()[:300]))
    return r.stdout.strip()


def git_bytes(repo, spec):
    r = subprocess.run(["git", "-C", repo, "show", spec], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def resolve_commit(repo, short):
    full = sh(["git", "rev-parse", "--verify", short + "^{commit}"], cwd=repo)
    meta = sh(["git", "log", "-1", "--format=%ad|%s", "--date=format:%m-%d %H:%M", full], cwd=repo)
    date, subject = meta.split("|", 1)
    return dict(short=short, full=full, date=date, subject=subject)


def commit_files(repo, rev):
    out = sh(["git", "show", "--name-only", "--format=", "-M", rev], cwd=repo)
    return sorted([x for x in out.splitlines() if x.strip()])


def blob_sha1_at(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "rev-parse", "%s:%s" % (rev, path)], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def db_rows(path):
    con = sqlite3.connect("file:" + path + "?mode=ro", uri=True)
    cur = con.cursor()
    cur.execute("select code, coalesce(name_zh,''), coalesce(name_en,'') from figures order by id")
    rows = cur.fetchall()
    con.close()
    return rows


def db_rowhash(path):
    con = sqlite3.connect("file:" + path + "?mode=ro", uri=True)
    cur = con.cursor()
    cur.execute("select name from sqlite_master where type='table' order by name")
    out = {}
    for (t,) in cur.fetchall():
        cur.execute('select * from "%s"' % t)
        h = hashlib.sha256()
        for r in cur.fetchall():
            h.update(repr(r).encode("utf-8"))
            h.update(b"\n")
        out[t] = h.hexdigest()
    con.close()
    return out


def load_zh(ws):
    return json.load(open(os.path.join(ws, ZH_JSON), encoding="utf-8"))


def zh_name(doc, code):
    v = doc.get(code)
    return (v.get("name_zh") or "") if isinstance(v, dict) else ""


def load_idx(ws):
    return {it["code"]: (it.get("name_zh") or "") for it in json.load(open(os.path.join(ws, IDX_REL), encoding="utf-8"))}


def ledger_recompute(ws, recon_db, scratch):
    zh = load_zh(ws)
    rows_now = db_rows(os.path.join(ws, DB_REL))
    db_now = {c: (z, e) for c, z, e in rows_now}
    empty_nonh = sorted([c for c, z, e in rows_now if not z.strip() and not c.startswith("H-")])
    restorable = [c for c in empty_nonh if zh_name(zh, c).strip()]
    no_source = [c for c in empty_nonh if not zh_name(zh, c).strip()]
    rec_nonh = sorted([c for c, z, e in db_rows(recon_db) if not z.strip() and not c.startswith("H-")])
    resolved = sorted(set(rec_nonh) - set(empty_nonh))
    removed = [c for c in resolved if c not in db_now]
    named = [c for c in resolved if c in db_now and db_now[c][0].strip()]
    idx = load_idx(ws)
    items = []
    true_list, code_list = [], []
    for c in restorable:
        name = zh_name(zh, c)
        kind = "code_as_name" if name.strip() == c else "true_name"
        (code_list if kind == "code_as_name" else true_list).append(c)
        items.append(dict(code=c, cls="restorable", kind=kind, legacy_name_zh=name,
                          db_name_zh=db_now[c][0], db_name_en=db_now[c][1], site_name_zh=idx.get(c, "")))
    for c in no_source:
        items.append(dict(code=c, cls="no_source", kind=None, legacy_name_zh=None,
                          db_name_zh=db_now[c][0], db_name_en=db_now[c][1], site_name_zh=idx.get(c, "")))
    for c in removed:
        items.append(dict(code=c, cls="removed", kind=None, legacy_name_zh=None,
                          db_name_zh=None, db_name_en=None, site_name_zh=None))
    for c in named:
        items.append(dict(code=c, cls="named", kind=None, legacy_name_zh=None,
                          db_name_zh=db_now[c][0], db_name_en=db_now[c][1], site_name_zh=idx.get(c, "")))
    return dict(items=items, counts=dict(total=len(items), restorable=len(restorable), true_name=len(true_list),
                                        code_as_name=len(code_list), no_source=len(no_source),
                                        removed=len(removed), named=len(named), recon_nonh=len(rec_nonh)),
                restorable=restorable, no_source=no_source, removed=removed, named=named,
                true_list=true_list, code_list=code_list)


def it(id_, desc, ok, detail="", info=False):
    return dict(id=id_, desc=desc, status=("INFO" if info else ("PASS" if ok else "FAIL")), detail=detail)


def sec_A(text):
    out = []
    heads = ["## 一、概述", "## 二、背景", "## 三、方法", "## 四、执行（登记链）", "## 五、证据",
             "## 六、核验", "## 七、残留与账务登记", "## 八、下一步", "## 九、附链（全号索引与复跑）"]
    h2 = [l.strip() for l in text.splitlines() if l.strip().startswith("## ")]
    ok = (h2 == heads)
    out.append(it("A1", "九节标题齐备且有序（行级精确）", ok, "h2_count=%d match=%s" % (len(h2), ok)))
    toks = ["t_9cb09b90", "t_0b240eb7", "t_9ed2866a", "t_d7faccc5", "t_28a29244", "IDEMPOTENT",
            "byte-exact", "ls-remote", "FAIL", "0/504"]
    miss = [t for t in toks if t not in text]
    out.append(it("A2", "关键 token 齐备", not miss, "missing=%s" % miss))
    ids = ["514 = 400 + 104 + 10", "547 = 514 + 31 + 2", "1017 = 504 + 513", "1027 = 513 + 514",
           "400+104+10+31+2=547"]
    miss2 = [t for t in ids if t not in text]
    out.append(it("A3", "计数恒等式齐备（四口径 + 汇总）", not miss2, "missing=%s" % miss2))
    n = len(re.findall(r"t_[0-9a-f]{8}", text))
    out.append(it("A4", "卡号引用计数 >= 25", n >= 25, "count=%d" % n))
    return out


def sec_B(text, ws, pb, mirror_pending, mut_pb=None):
    out = []
    proot = mut_pb or pb
    bad = []
    pend = []
    for rel in [REPORT_REL, VER_REL, EVIDENCE_REL]:
        fp = os.path.join(ws, rel)
        pp = os.path.join(proot, rel)
        if not os.path.exists(fp):
            if mirror_pending and rel == EVIDENCE_REL:
                pend.append("ws 证据待生成（首次）")
            else:
                bad.append("ws 缺 %s" % rel)
            continue
        if not os.path.exists(pp):
            (pend if (mirror_pending and not mut_pb) else bad).append("pb 缺 %s" % rel)
            continue
        a = sha16(fp)
        b = sha16(pp)
        if a != b:
            (pend if (mirror_pending and not mut_pb) else bad).append("不等 %s（%s vs %s）" % (rel, a, b))
    if pend:
        out.append(it("B1", "本档 3 件 ws/pb byte-exact", True, "过渡轮（镜像待落地）：%s" % pend, info=True))
    else:
        out.append(it("B1", "本档 3 件 ws/pb byte-exact", not bad, "; ".join(bad) or "3/3 equal"))
    if mut_pb is not None:
        return out
    bad2 = []
    for pbs, wss in sorted(PB_ALIGN.items()):
        fpb = commit_files(pb, pbs)
        fws = commit_files(ws, wss)
        if fpb != fws:
            bad2.append("%s/%s 件集不等：%s vs %s" % (pbs, wss, fpb, fws))
            continue
        for f in fpb:
            a = blob_sha1_at(ws, wss, f)
            b = blob_sha1_at(pb, pbs, f)
            if a != b or a is None:
                bad2.append("%s:%s blob 不等" % (pbs, f))
    out.append(it("B2", "pb 三笔镜像提交逐件 blob 对照（3/2/3 件）", not bad2, "; ".join(bad2) or "P1=3 P2=2 P3=3 全等"))
    r1 = subprocess.run(["git", "-C", pb, "merge-base", "--is-ancestor", "e5ddd13f", "main"], capture_output=True)
    not_anc = (r1.returncode != 0)
    r2 = subprocess.run(["git", "-C", pb, "cat-file", "-e", "e5ddd13f^{commit}"], capture_output=True)
    exists = (r2.returncode == 0)
    refs = sorted(x for x in sh(["git", "-C", pb, "for-each-ref", "--contains", "e5ddd13f", "--format=%(refname)"], cwd=pb, check=False).split("\n") if x.strip())
    out.append(it("B3", "执行链未发布（非 origin/main 祖先）+ 对象在库登记", bool(not_anc and exists),
                  "not_anc_main=%s obj_in_pb=%s refs=%s" % (not_anc, exists, refs)))
    return out


def sec_C(text, ws, pb):
    out = []
    bad = []
    for c in WS_COMMITS:
        rc = resolve_commit(ws, c)
        if ("`%s` | `%s`" % (rc["short"], rc["full"])) not in text:
            bad.append("ws %s 行缺" % c)
        if ("`%s` | %s |" % (rc["full"], rc["date"])) not in text:
            bad.append("ws %s 日期缺" % c)
    out.append(it("C1", "ws 4 笔登记行（短号+全号+日期）", not bad, "; ".join(bad) or "4/4"))
    bad2 = []
    for c in PB_COMMITS:
        rc = resolve_commit(pb, c)
        if ("`%s` | `%s`" % (rc["short"], rc["full"])) not in text:
            bad2.append("pb %s 行缺" % c)
        if ("`%s` | %s |" % (rc["full"], rc["date"])) not in text:
            bad2.append("pb %s 日期缺" % c)
    out.append(it("C2", "pb 3 笔登记行（短号+全号+日期）", not bad2, "; ".join(bad2) or "3/3"))
    bad3 = []
    for a in ["e5ddd13f", "ee08f5b5", "8adbdabd", "c6d626c6", "1e6f14eb", "4975cd26",
              "f61f055d", "7714c9d1", "e7bb276c", "46c29cbc", "39e3eb21", "b44ba0a3",
              "0b480d9b", "97cc5b09"]:
        try:
            resolve_commit(ws, a)
        except Exception:
            bad3.append("ws " + a)
    for a in ["6b50893", "ad27e1a", "3129539", "c167cb5", "0b86fd2", "27c2074", "0683505", "e32cb3b", "fbb4844f"]:
        try:
            resolve_commit(pb, a)
        except Exception:
            bad3.append("pb " + a)
    out.append(it("C3", "锚点/窗口提交全部可解析", not bad3, "; ".join(bad3) or "20/20"))
    cards = ["t_0b240eb7", "t_9ed2866a", "t_9cb09b90", "t_d7faccc5", "t_28a29244"]
    miss = [c for c in cards if c not in text]
    out.append(it("C4", "五卡链登记齐备（含后置 QA）", not miss, "missing=%s" % miss))
    bad4 = []
    for c in ["ee08f5b5", "3dbf9d10", "f61f055d", "7714c9d1", "e7bb276c", "46c29cbc", "39e3eb21", "b44ba0a3", "0b480d9b", "97cc5b09"]:
        try:
            rc = resolve_commit(ws, c)
            if rc["short"] not in text:
                bad4.append("ws 窗口 %s 未登记" % c)
        except Exception:
            bad4.append("ws 窗口 %s 不可解析" % c)
    for c in ["c167cb5", "0b86fd2", "27c2074", "0683505", "e32cb3b", "fbb4844f"]:
        try:
            rc = resolve_commit(pb, c)
            if rc["short"] not in text:
                bad4.append("pb 窗口 %s 未登记" % c)
        except Exception:
            bad4.append("pb 窗口 %s 不可解析" % c)
    out.append(it("C5", "窗口邻居提交登记（ws 10 / pb 6）", not bad4, "; ".join(bad4) or "ok"))
    return out


def git_name_status(repo, rev):
    ns = subprocess.run(["git", "-C", repo, "show", "--name-status", "-z", "--format=", "-M", rev], capture_output=True)
    fields = ns.stdout.split(b"\0")
    D, A, M = [], [], []
    i = 0
    while i + 1 < len(fields):
        st = fields[i].decode()
        pat = fields[i + 1].decode("utf-8", "surrogateescape")
        if st.startswith("D"):
            D.append(pat)
        elif st.startswith("A"):
            A.append(pat)
        elif st.startswith("M"):
            M.append(pat)
        i += 2
    return D, A, M


def git_tree_map(repo, rev):
    outr = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-z", rev], capture_output=True)
    fields = outr.stdout.split(b"\0")
    m = {}
    for rec in fields:
        if not rec:
            continue
        meta, name = rec.split(b"\t", 1)
        m[name.decode("utf-8", "surrogateescape")] = meta.split()[2].decode()
    return m


def sec_D(text, ws, pb, recon_db, overrides=None):
    ov = overrides or {}
    out = []
    bad = []
    for rel, (ww, pw) in sorted(SHA16_EXPECT.items()):
        fp = os.path.join(ws, rel)
        pp = os.path.join(pb, rel)
        gs = sha16(fp)
        gp = sha16(pp)
        if pw is None:
            if gs != gp or (ww is not None and gs != ww):
                bad.append("注册面不符 %s" % rel)
            form = "| %s | `%s` | `%s` |" % (rel, gs, gp)
        else:
            if gs != ww or gp != pw:
                bad.append("注册面不符 %s（%s/%s）" % (rel, gs, gp))
            form = "| %s | `%s` | `%s` |" % (rel, gs, gp)
        if form not in text:
            bad.append("报告行缺/不符 %s" % rel)
    out.append(it("D1", "8 件 sha16 双仓复核（含 DB 不对称登记）", not bad, "; ".join(bad) or "8/8"))
    bad2 = []
    for rel, before, at in PINS_EXPECT:
        b = git_bytes(ws, "%s:%s" % (PARENT, rel))
        a = git_bytes(ws, "%s:%s" % (AT, rel))
        cur = sha16(os.path.join(ws, rel))
        bs = hashlib.sha256(b).hexdigest()[:16] if b is not None else None
        as_ = hashlib.sha256(a).hexdigest()[:16] if a is not None else None
        if before is None:
            if bs is not None:
                bad2.append("%s 预期前无" % rel)
            form = "| %s | （前无，随 e5ddd13f 强加入库） | `%s` | `%s` |" % (rel, as_, cur)
        else:
            if bs != before or as_ != at:
                bad2.append("%s 三段不符" % rel)
            form = "| %s | `%s` | `%s` | `%s` |" % (rel, bs, as_, cur)
        if form not in text:
            bad2.append("报告 pin 行缺/不符 %s" % rel)
    out.append(it("D2", "5 件三段 pin（before/at/现值）", not bad2, "; ".join(bad2) or "5/5"))
    fp = os.path.join(ws, W9_BACKUP)
    s = sha256_file(fp)
    par = git_bytes(ws, "%s:%s" % (PARENT, DB_REL))
    rh_eq = db_rowhash(fp) == db_rowhash(os.path.join(ws, DB_REL))
    ok3 = (s == hashlib.sha256(par).hexdigest()) and rh_eq and (s[:16] in text) and ("行级 rowhash" in text)
    out.append(it("D3", "W9 前像备份双核（blob == 父提交；rowhash eq）", ok3, "sha16=%s rowhash_eq=%s" % (s[:16], rh_eq)))
    D_, A_, M_ = git_name_status(ws, AT)
    tree = git_tree_map(ws, PARENT)
    bkroot = os.path.join(ws, W7_BACKUP_DIR, "ws")
    rels = ["%s/ws/%s" % (W7_BACKUP_DIR, p) for p in D_]
    proc = subprocess.run(["git", "hash-object", "--stdin-paths"], cwd=ws,
                          input=("\n".join(rels) + "\n").encode(), capture_output=True, timeout=600)
    ho = proc.stdout.decode().splitlines() if proc.returncode == 0 else []
    man_shas = set()
    for line in open(os.path.join(ws, W7_BACKUP_DIR, "MANIFEST.sha256"), encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if len(line) >= 64 and re.match(r"^[0-9a-f]{64}", line):
            man_shas.add(line[:64])
    okn = 0
    for p, g1 in zip(D_, ho):
        exp = tree.get(p)
        bf = os.path.join(bkroot, p)
        if exp and g1 == exp and os.path.exists(bf) and sha256_file(bf) in man_shas:
            okn += 1
    tok4 = "1303/1303 OK，0 mismatch"
    out.append(it("D4", "W7 前像 1303 件双锚复核", okn == len(D_) == 1303 and tok4 in text,
                  "ok=%d total=%d token=%s" % (okn, len(D_), tok4 in text)))
    cl = json.load(open(os.path.join(ws, W7_CLASS), encoding="utf-8"))
    wsv = {x["path"]: x.get("verdict") for x in cl["items"] if x.get("repo") == "workspace"}
    planned = {"archive_delete", "delete"}
    unpl = [x for x in D_ if wsv.get(x) not in planned]
    kh = [x for x in D_ if wsv.get(x) == "keep"]
    st = dict(D=len(D_), root=len([x for x in D_ if "/" not in x]),
              tools=len([x for x in D_ if x.startswith("tools/json/")]),
              A=len(A_), web=len([x for x in A_ if x.startswith("web/public/data")]), M=len(M_))
    ok5 = (st["D"] == 1303 and st["root"] == 633 and st["tools"] == 670 and st["A"] == 1359
           and st["web"] == 1359 and st["M"] == 1 and not unpl and not kh
           and "M=1 + A=1359 + D=1303" in text and "keep 面 0 命中" in text)
    out.append(it("D5", "删除面对账（1303 planned / 0 keep-hit；A 1359 web）", ok5, "%s unpl=%d keep=%d" % (st, len(unpl), len(kh))))
    led = ledger_recompute(ws, recon_db, None)
    if ov.get("drop_ledger_row"):
        led["items"] = led["items"][:-1]
        led["counts"]["total"] -= 1
    cnts = led["counts"]
    okc = (cnts["total"] == 547 and cnts["restorable"] == 504 and cnts["true_name"] == 400
           and cnts["code_as_name"] == 104 and cnts["no_source"] == 10 and cnts["removed"] == 31
           and cnts["named"] == 2 and cnts["recon_nonh"] == 547 and sorted(led["no_source"]) == sorted(TEN))
    qa = json.load(open(os.path.join(ws, QA_EVIDENCE), encoding="utf-8"))
    qt = {r["code"]: r["legacy_name_zh"] for r in qa["restorable_table"]}
    if set(qt) != set(led["restorable"]):
        okc = False
    for itm in led["items"]:
        if itm["cls"] == "restorable" and qt.get(itm["code"]) != itm["legacy_name_zh"]:
            okc = False
    bad6 = [] if okc else ["计数或集合不符"]
    def block(a, b):
        i0 = text.find(a)
        i1 = text.find(b) if b else len(text)
        return text[i0:i1] if i0 >= 0 else ""
    ba = block("#### 4.4.3a", "#### 4.4.3b")
    bb = block("#### 4.4.3b", "#### 4.4.4")
    rows_a = sorted((m.group(1), m.group(2)) for m in re.finditer(r"^\| ([A-Za-z0-9][A-Za-z0-9\-]*) \| (.+) \|$", ba, flags=re.M))
    rows_b = sorted((m.group(1), m.group(2)) for m in re.finditer(r"^\| ([A-Za-z0-9][A-Za-z0-9\-]*) \| (.+) \|$", bb, flags=re.M))
    exp_a = sorted((itm["code"], itm["legacy_name_zh"]) for itm in led["items"] if itm["cls"] == "restorable" and itm["kind"] == "true_name")
    exp_b = sorted((itm["code"], itm["legacy_name_zh"]) for itm in led["items"] if itm["cls"] == "restorable" and itm["kind"] == "code_as_name")
    blk_ns = block("#### 4.4.2", "#### 4.4.3a")
    ns_codes = sorted(set(m.group(1) for m in re.finditer(r"^\| ([A-Za-z0-9\-]+) \| 无 \|", blk_ns, flags=re.M)))
    blk_rm = block("#### 4.4.4", "#### 4.4.5")
    rm_codes = []
    for l in blk_rm.splitlines():
        l = l.strip()
        if l.startswith("- "):
            for x in l[2:].split("、"):
                x = x.strip()
                if x:
                    rm_codes.append(x)
    rm_codes = sorted(rm_codes)
    blk_nm = block("#### 4.4.5", "### 4.5")
    nm_codes = sorted(set(m.group(1) for m in re.finditer(r"^- ([A-Za-z0-9\-]+)（DB name_zh=", blk_nm, flags=re.M)))
    if rows_a != exp_a:
        bad6.append("4.4.3a 表不符（%d vs %d）" % (len(rows_a), len(exp_a)))
    if rows_b != exp_b:
        bad6.append("4.4.3b 表不符（%d vs %d）" % (len(rows_b), len(exp_b)))
    if ns_codes != sorted(led["no_source"]):
        bad6.append("4.4.2 表不符")
    if rm_codes != sorted(led["removed"]):
        bad6.append("4.4.4 列表不符（%d vs %d）" % (len(rm_codes), len(led["removed"])))
    if nm_codes != sorted(led["named"]):
        bad6.append("4.4.5 列表不符")
    if "400+104+10+31+2=547（重算一致）" not in text:
        bad6.append("汇总行缺")
    out.append(it("D6", "547 台账完整性 + 4.4 终表逐表核", not bad6, "; ".join(bad6) or "547=400+104+10+31+2 全对"))
    evp = os.path.join(ws, EVIDENCE_REL)
    if ov.get("skip_evidence_ledger") or not os.path.exists(evp) or ov.get("drop_ledger_row"):
        out.append(it("D6b", "证据台账对照（上轮）", True, "首次/过渡轮或注入模式跳过", info=True))
    else:
        try:
            ev = json.load(open(evp, encoding="utf-8"))
            evi = [(x.get("code"), x.get("cls"), x.get("kind")) for x in ev.get("ledger_547", {}).get("items", [])]
            cur = [(x["code"], x["cls"], x.get("kind")) for x in led["items"]]
            out.append(it("D6b", "证据台账对照（上轮）", evi == cur, "rows=%d" % len(evi)))
        except Exception as e:
            out.append(it("D6b", "证据台账对照（上轮）", False, str(e)[:120]))
    bad7 = []
    mg = re.search(r"生成器：build_w9_fclass_archive.py —— ws-only 面（sha16 `([0-9a-f]{16})`", text)
    mv = re.search(r"验收脚本：verify_w9_fclass_archive.py —— 随镜像（sha16 `([0-9a-f]{16})`", text)
    sg = sha16(os.path.join(ws, GEN_REL))
    sv = sha16(os.path.join(ws, VER_REL))
    if not mg or mg.group(1) != sg:
        bad7.append("生成器 sha16 行")
    if not mv or mv.group(1) != sv:
        bad7.append("验收脚本 sha16 行")
    out.append(it("D7", "5.2 本档件 sha16 自洽（生成器/验收脚本）", not bad7, "; ".join(bad7) or "2/2"))
    return out, led


def sec_E(text, pend, ws, pb):
    out = []
    bad = []
    for rel, want in [(QA_REPORT, "a7235a94bd9e2aff"), (QA_EVIDENCE, "2deae7f546a10ff9"), (QA_VER, "43220de86df64cfd")]:
        g = sha16(os.path.join(ws, rel))
        if g != want or g not in text:
            bad.append(rel)
    if "12 PASS / 3 FAIL / 2 INFO" not in text:
        bad.append("校验器现状计数")
    out.append(it("E1", "QA 产物指纹照登（现值一致）", not bad, "; ".join(bad) or "3/3 + 计数"))
    toks = ["QA-W9-F1", "QA-W9-F2", "QA-W9-F3", "QA-W9-F4", "QA-W9-F5", "QA-W9-F6",
            "0/504", "t_d7faccc5", "t_28a29244", "537 vs 504", "待核名"]
    miss = [t for t in toks if t not in text]
    out.append(it("E2", "未闭合项照登（F1..F6 + 去向）", not miss, "missing=%s" % miss))
    if pend:
        ok = ("回填区" in text) and ("stage：v1（回执待回填；v2 回执终版）" in text)
        out.append(it("E3", "回执区（过渡轮：占位）", ok, "回填区=%s" % ("回填区" in text)))
    else:
        m1 = re.search(r"ws_commit_v1：`([0-9a-f]{40})`", text)
        m2 = re.search(r"pb_commit_v1：`([0-9a-f]{40})`", text)
        bad3 = []
        if not m1:
            bad3.append("ws_commit_v1 缺")
        if not m2:
            bad3.append("pb_commit_v1 缺")
        if m1:
            try:
                f = commit_files(ws, m1.group(1))
                if f != sorted([REPORT_REL, GEN_REL, VER_REL, EVIDENCE_REL]):
                    bad3.append("ws v1 件集=%s" % f)
            except Exception:
                bad3.append("ws_commit_v1 不可解析")
        if m2:
            try:
                f = commit_files(pb, m2.group(1))
                if f != sorted([REPORT_REL, VER_REL, EVIDENCE_REL]):
                    bad3.append("pb v1 件集=%s" % f)
            except Exception:
                bad3.append("pb_commit_v1 不可解析")
        for tk in ["回执终版提交", "回执终版镜像", "证据终版提交", "证据终版镜像", "push_v1：ok", "push_v2：ok"]:
            if tk not in text:
                bad3.append("token 缺：%s" % tk)
        out.append(it("E3", "回执区自洽（v1 提交件集 + v2/v3 登记）", not bad3, "; ".join(bad3) or "v1 件集全对 + v2/v3 登记齐"))
    return out


def sec_F(text, ws, pb, recon_db, scratch, pend):
    out = []
    t1 = text.replace("## 三、方法", "## 三、方法X", 1)
    r1 = sec_A(t1)
    out.append(it("F1", "A 突变（去一节标题）必被捕获", any(x["status"] == "FAIL" for x in r1), ""))
    try:
        full = resolve_commit(ws, AT)["full"]
        t2 = text.replace(full, "0" * 40, 1)
        r2 = sec_C(t2, ws, pb)
        out.append(it("F2", "C 突变（全号篡改）必被捕获", any(x["status"] == "FAIL" for x in r2), ""))
    except Exception as e:
        out.append(it("F2", "C 突变（全号篡改）必被捕获", False, str(e)[:80]))
    t3 = text.replace("`a7235a94bd9e2aff`", "`0000000000000000`", 1)
    r3, _ = sec_D(t3, ws, pb, recon_db)
    out.append(it("F3", "D 突变（sha16 行篡改）必被捕获", any(x["status"] == "FAIL" for x in r3), ""))
    r4, _ = sec_D(text, ws, pb, recon_db, overrides={"drop_ledger_row": True})
    out.append(it("F4", "D 突变（台账丢行）必被捕获", any(x["status"] == "FAIL" for x in r4), ""))
    if pend:
        t5 = text.replace("回填区", "X填区")
    else:
        t5 = re.sub(r"ws_commit_v1：`[0-9a-f]{40}`", "ws_commit_v1：`" + "0" * 40 + "`", text, count=1)
    r5 = sec_E(t5, pend, ws, pb)
    out.append(it("F5", "E 突变（回执区篡改）必被捕获", any(x["status"] == "FAIL" for x in r5), ""))
    mutdir = os.path.join(scratch, "pb_mut")
    os.makedirs(mutdir, exist_ok=True)
    for rel in [REPORT_REL, VER_REL, EVIDENCE_REL]:
        src = os.path.join(pb, rel)
        dst = os.path.join(mutdir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            shutil.copyfile(src, dst)
    mrep = os.path.join(mutdir, REPORT_REL)
    if os.path.exists(mrep):
        with open(mrep, "a", encoding="utf-8") as f:
            f.write("X\n")
    r6 = sec_B(text, ws, mutdir, False, mut_pb=mutdir)
    out.append(it("F6", "B 突变（镜像件篡改）必被捕获", any(x["status"] == "FAIL" for x in r6), ""))
    return out


def build_evidence(args, sections, led, text, ws):
    tot = dict(pass_count=0, fail=0, info=0)
    secj = []
    for sid, items in sections:
        for x in items:
            if x["status"] == "PASS":
                tot["pass_count"] += 1
            elif x["status"] == "FAIL":
                tot["fail"] += 1
            else:
                tot["info"] += 1
        secj.append({"id": sid, "items": items})
    def rj(c):
        try:
            rc = resolve_commit(ws, c)
            return {"short": rc["short"], "full": rc["full"], "date": rc["date"]}
        except Exception:
            return {"short": c, "full": None, "date": None}
    chain = dict(
        ws_commits=[rj(c) for c in WS_COMMITS],
        pb_commits=[rj_pb(c) for c in PB_COMMITS],
        windows_ws=[rj(c) for c in ["ee08f5b5", "3dbf9d10", "f61f055d", "7714c9d1", "e7bb276c", "46c29cbc", "39e3eb21", "b44ba0a3", "0b480d9b", "97cc5b09"]],
        windows_pb=[rj_pb(c) for c in ["c167cb5", "0b86fd2", "27c2074", "0683505", "e32cb3b", "fbb4844f"]],
    )
    fp = dict(
        report_sha16=sha16(os.path.join(ws, REPORT_REL)) if os.path.exists(os.path.join(ws, REPORT_REL)) else None,
        gen_sha16=sha16(os.path.join(ws, GEN_REL)) if os.path.exists(os.path.join(ws, GEN_REL)) else None,
        verifier_sha16=sha16(os.path.join(ws, VER_REL)),
        qa_report_sha16=sha16(os.path.join(ws, QA_REPORT)),
        qa_evidence_sha16=sha16(os.path.join(ws, QA_EVIDENCE)),
        qa_ver_sha16=sha16(os.path.join(ws, QA_VER)),
        evidence="自指归零（本件 sha16 见卡面完成 metadata）",
    )
    m1 = re.search(r"ws_commit_v1：`([0-9a-f]{40})`", text)
    m2 = re.search(r"pb_commit_v1：`([0-9a-f]{40})`", text)
    ev = dict(
        schema="protreptic.phase21w9_fclass_archive_evidence/v1",
        task="t_9cb09b90",
        generated_by="verify_w9_fclass_archive.py",
        generated_at="2026-09-24",
        flags=dict(receipts_pending=bool(args.receipts_pending), mirror_pending=bool(args.mirror_pending)),
        totals=dict(pass_count=tot["pass_count"], fail=tot["fail"], info=tot["info"]),
        sections=secj,
        ledger_547=dict(counts=led["counts"], items=led["items"],
                        order="by code（cls/kind 分层：restorable(true_name|code_as_name)/no_source/removed/named）"),
        chain=chain,
        fingerprints=fp,
        receipts=dict(ws_commit_v1=(m1.group(1) if m1 else None),
                      pb_commit_v1=(m2.group(1) if m2 else None),
                      note="v2/v3 全号随卡面完成 metadata（先例体例）"),
    )
    if getattr(args, "with_live", False):
        ev["live"] = collect_live(ws, args.publish)
    return ev


def rj_pb(c):
    return {"short": c, "full": None, "date": None}


def collect_live(ws, pb):
    out = {}
    try:
        raw = sh(["python3", os.path.join(ws, "tools/check_repo_parity.py"), "--json"], cwd=ws, check=False)
        j = json.loads(raw)
        out["parity_status"] = j.get("status")
        out["parity_counts"] = j.get("counts")
    except Exception as e:
        out["parity_error"] = str(e)[:120]
    try:
        r = subprocess.run(["git", "-C", pb, "ls-remote", "origin", "main"], capture_output=True, text=True, timeout=90)
        out["ls_remote"] = r.stdout.split()[0] if r.stdout else "EMPTY"
    except Exception as e:
        out["ls_remote_error"] = str(e)[:120]
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Phase21-W9 F-class chain archive independent verification (2nd impl)")
    ap.add_argument("--workspace", default=WS_DEFAULT)
    ap.add_argument("--publish", default=PB_DEFAULT)
    ap.add_argument("--report", default=None)
    ap.add_argument("--evidence", default=None)
    ap.add_argument("--scratch", default="/opt/data/profiles/pigafetta/cache/scratch/w9arch_verify")
    ap.add_argument("--receipts-pending", action="store_true")
    ap.add_argument("--mirror-pending", action="store_true")
    ap.add_argument("--with-live", action="store_true")
    ap.add_argument("--force-write", action="store_true")
    args = ap.parse_args(argv)
    ws = args.workspace
    report = args.report or os.path.join(ws, REPORT_REL)
    evp = args.evidence or os.path.join(ws, EVIDENCE_REL)
    if not os.path.exists(report):
        print("FAIL: report missing: %s" % report)
        return 1
    text = open(report, encoding="utf-8").read()
    os.makedirs(args.scratch, exist_ok=True)
    recon_db = os.path.join(args.scratch, "recon.db")
    b = git_bytes(ws, "%s:%s" % (RECON, DB_REL))
    if b is None:
        print("FAIL: recon blob missing")
        return 1
    open(recon_db, "wb").write(b)
    sections = []
    items = sec_A(text)
    sections.append(("A", items))
    print("A: " + ", ".join("%s=%s" % (x["id"], x["status"]) for x in items))
    items = sec_B(text, ws, args.publish, args.mirror_pending)
    sections.append(("B", items))
    print("B: " + ", ".join("%s=%s" % (x["id"], x["status"]) for x in items))
    items = sec_C(text, ws, args.publish)
    sections.append(("C", items))
    print("C: " + ", ".join("%s=%s" % (x["id"], x["status"]) for x in items))
    items, led = sec_D(text, ws, args.publish, recon_db)
    sections.append(("D", items))
    print("D: " + ", ".join("%s=%s" % (x["id"], x["status"]) for x in items))
    items = sec_E(text, args.receipts_pending, ws, args.publish)
    sections.append(("E", items))
    print("E: " + ", ".join("%s=%s" % (x["id"], x["status"]) for x in items))
    items = sec_F(text, ws, args.publish, recon_db, args.scratch, args.receipts_pending)
    sections.append(("F", items))
    print("F: " + ", ".join("%s=%s" % (x["id"], x["status"]) for x in items))
    ev = build_evidence(args, sections, led, text, ws)
    nfail = sum(1 for _, its in sections for x in its if x["status"] == "FAIL")
    npass = sum(1 for _, its in sections for x in its if x["status"] == "PASS")
    ninfo = sum(1 for _, its in sections for x in its if x["status"] == "INFO")
    new = (json.dumps(ev, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")
    gate_ok = True
    if os.path.exists(evp):
        old = open(evp, "rb").read()
        try:
            oflags = json.loads(old.decode("utf-8")).get("flags", {})
        except Exception:
            oflags = None
        if oflags == ev["flags"]:
            if old == new:
                print("E5: PASS（证据自稳定：复跑字节不变）")
            else:
                print("E5: FAIL（证据字节不稳定；不覆盖 %s）" % evp)
                gate_ok = False
        else:
            print("E5: INFO（过渡轮：flags 变化 %s -> %s）" % (oflags, ev["flags"]))
    else:
        print("E5: INFO（首次生成）")
    if gate_ok or args.force_write:
        tmp = evp + ".tmp"
        with open(tmp, "wb") as f:
            f.write(new)
        os.replace(tmp, evp)
        print("EVIDENCE WROTE %s (%d bytes)" % (evp, len(new)))
    else:
        print("EVIDENCE NOT WRITTEN (稳定性门未过)")
    print("W9 ARCHIVE VERIFY: PASS=%d FAIL=%d INFO=%d rc=%d" % (npass, nfail, ninfo, 1 if nfail else 0))
    if nfail:
        for sid, its in sections:
            for x in its:
                if x["status"] == "FAIL":
                    print("  FAIL %s %s: %s" % (sid, x["id"], x["detail"]))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
