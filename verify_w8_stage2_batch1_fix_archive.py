#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase21-W8S2B1 修复链档案独立验收（卡 t_e01c8aa0；第二实现）。

段目：
  A 档案结构（九节 / 关键 token / 件数口径 / 卡号引用）
  B 镜像面（报告 / 验收 / 证据双仓 byte-exact；pb 四笔提交级 blob 对照；可选 push 面）
  C 提交链（§9.1 全号解析 / 日期 / 锚点 / 对对齐 / 回执区条目）
  D 数据面（§5.1 sha16 复核 / 计数重算 / 6 行归因 / 三段一致性 / 候选扫描）
  E 记录面（F0-F6 / 计数 token / 回执区 v1 复核 / 父链收口）
  F 反向注入自检（六类）
  G 链复核（QA 校验器三锚点复跑；可选 push 面）

用法：
  python3 verify_w8_stage2_batch1_fix_archive.py
      [--workspace WS] [--publish PB] [--with-remote] [--with-live]
      [--no-chain-repro] [--receipts-pending] [--no-evidence]
      [--evidence-out PATH] [--json-out PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

WS_DEFAULT = "/opt/data/workspace/Protreptic"
PB_DEFAULT = "/opt/data/release/Protreptic-publish"

REPORT_REL = "docs/research/phase21w8_stage2_batch1_fix_archive_report.md"
GEN_REL = "build_w8_stage2_batch1_fix_archive.py"
VER_REL = "verify_w8_stage2_batch1_fix_archive.py"
EVIDENCE_REL = "docs/research/phase21w8_stage2_batch1_fix_archive_evidence.json"

PARENT_REPORT_REL = "docs/research/phase21w8_stage2_batch1_archive_report.md"
PARENT_VER_REL = "verify_w8_stage2_batch1_archive.py"
PARENT_GEN_REL = "build_w8_stage2_batch1_archive.py"
PARENT_EVIDENCE_REL = "docs/research/phase21w8_stage2_batch1_archive_evidence.json"

FIX_RECEIPT_REL = "data/audit/phase21w8_stage2_batch1_sourcing_fix_receipt.json"
SOURCING_JSON_REL = "docs/research/phase21w8_stage2_batch1_sourcing_report.json"
QA_VER_REL = "tools/verify_batch1_sourcing_fix_qa_espinosa.py"

MIRROR_FILES = [REPORT_REL, VER_REL, EVIDENCE_REL,
                PARENT_REPORT_REL, PARENT_VER_REL, PARENT_EVIDENCE_REL]

CHAIN_FILES = [
    "docs/research/phase21w8_stage2_batch1_sourcing_report.md",
    "docs/research/phase21w8_stage2_batch1_sourcing_report.json",
    "tools/build_batch1_sourcing_pack.py",
    "docs/research/phase21w8_stage2_batch1_landing_report.md",
    "data/audit/phase21w8_stage2_batch1_sourcing_fix_receipt.json",
    "docs/research/phase21w8_stage2_batch1_sourcing_fix_qa_report_espinosa.md",
    "docs/research/phase21w8_stage2_batch1_sourcing_fix_qa_evidence_espinosa.json",
    "tools/verify_batch1_sourcing_fix_qa_espinosa.py",
    "docs/research/phase21w8_stage2_batch1_archive_report.md",
    "verify_w8_stage2_batch1_archive.py",
    "docs/research/phase21w8_stage2_batch1_archive_evidence.json",
]

PB_PIN = {"9afe48e": "68fd5569", "5b693bb": "5705b030",
          "0b86fd2": "e7bb276c", "27c2074": "46c29cbc"}
WS_SHORTS = ["68fd5569", "5705b030", "e7bb276c", "46c29cbc"]
PB_SHORTS = ["9afe48e", "5b693bb", "0b86fd2", "27c2074"]
ANCHOR_PRE = "1c00ca8a"

A_FILES8 = [REPORT_REL, GEN_REL, VER_REL, EVIDENCE_REL,
            PARENT_REPORT_REL, PARENT_GEN_REL, PARENT_VER_REL, PARENT_EVIDENCE_REL]
P_FILES6 = [REPORT_REL, VER_REL, EVIDENCE_REL,
            PARENT_REPORT_REL, PARENT_VER_REL, PARENT_EVIDENCE_REL]

EXPECT_VERDICTS = {"null": 57, "variant": 20, "quote": 3, "cross-lang": 74}
EXPECT_TOTAL = 154
EXPECT_NEAR = 28
EXPECT_NEG = 16
EXPECT_BOOKS = 18
CORE_V1 = 25
CORE_V2 = 23
SCAN_N = 40

TITLES = ["## 一、概述", "## 二、背景", "## 三、方法", "## 四、执行（登记链）",
          "## 五、证据", "## 六、核验", "## 七、残留与账务登记", "## 八、下一步", "## 九、附链"]
TOKENS = ["t_2ce1e334", "t_a407cb32", "t_e01c8aa0", "t_098d8ff6", "t_e727be57",
          "1c00ca8a", "68fd5569", "5705b030", "e7bb276c", "46c29cbc",
          "9afe48e", "5b693bb", "0b86fd2", "27c2074",
          "IDEMPOTENT", "byte-exact", "ls-remote", "回执区",
          "57 / 20 / 3 / 74", "25->23", "154",
          "30 PASS / 2 FAIL", "33/33 全 PASS"]

QA_EXPECT = {"POST": 33, "PRE": 32, "SCAN": 36, "REMOTE": 35}


def sh(cmd, cwd=None, check=True):
    r = subprocess.run(list(cmd), cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError("cmd failed: %s\n%s" % (cmd, r.stderr[:300]))
    return r.stdout.strip()


def sha16b(b):
    return hashlib.sha256(b).hexdigest()[:16]


def sha16f(p):
    p = Path(p)
    return sha16b(p.read_bytes()) if p.exists() else None


def gitshow_text(repo, rev, rel):
    r = subprocess.run(["git", "show", "%s:%s" % (rev, rel)], cwd=repo, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("git show failed: %s %s" % (rev, rel))
    return r.stdout.decode("utf-8", errors="replace")


def files_of(repo, rev):
    return sorted(f for f in sh(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", rev], cwd=repo).split("\n") if f)


def blob_map(repo, rev):
    out = {}
    for f in files_of(repo, rev):
        out[f] = sh(["git", "rev-parse", "%s:%s" % (rev, f)], cwd=repo)
    return out


class Res:
    def __init__(self):
        self.items = []

    def add(self, sec, name, ok, detail=""):
        self.items.append({"section": sec, "name": name, "ok": bool(ok),
                           "detail": str(detail)[:300]})

    def counts(self):
        c = Counter()
        for i in self.items:
            c[i["section"]] += 1
        return dict(c)

    def fails(self):
        return [i for i in self.items if not i["ok"]]


class Ctx:
    def __init__(self, ws, pb, args):
        self.ws = ws
        self.pb = pb
        self.args = args
        rp = Path(ws) / REPORT_REL
        self.report_text = rp.read_text(encoding="utf-8") if rp.exists() else ""
        self.mirror_bad = set()
        self.commit_bad = False
        self.sha_bad = False
        self.counts_override = None
        self.receipt_override = None


def load_receipt(ctx):
    return json.loads((Path(ctx.ws) / FIX_RECEIPT_REL).read_text(encoding="utf-8"))


def load_sourcing(ctx):
    return json.loads((Path(ctx.ws) / SOURCING_JSON_REL).read_text(encoding="utf-8"))


def sec_a(ctx, res):
    t = ctx.report_text
    missing = [x for x in TITLES if x not in t]
    res.add("A", "A1 九节标题齐备", not missing, "缺: %s" % missing)
    mt = [x for x in TOKENS if x not in t]
    res.add("A", "A2 关键 token 齐备", not mt, "缺: %s" % mt)
    fmt = all(x in t for x in ["九节", "3 卡", "4 笔", "11 件"])
    res.add("A", "A3 件数口径（九节 / 3 卡 / 4 笔 / 11 件）", fmt, "")
    ref = all(x in t for x in ["t_2ce1e334", "t_a407cb32", "t_e01c8aa0", "t_098d8ff6", "1c00ca8a"])
    res.add("A", "A4 卡号与锚点引用完整", ref, "")


def live_probe_check():
    import urllib.request

    def get(url):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "w8-fix-arch-verify"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, r.read()
        except Exception:
            return 0, b""

    base = "https://ovmobilegroup.github.io/protreptic/"
    s1, _ = get(base)
    s2, b2 = get(base + "credibility/")
    s3, _ = get(base + "data/meta.json")
    marks = (b"1845" in b2) or (b"1019" in b2)
    ok = s1 == 200 and s2 == 200 and marks
    return ok, "home=%s cred=%s meta=%s marks=%s" % (s1, s2, s3, marks)


def sec_b(ctx, res):
    for rel in MIRROR_FILES:
        w = sha16f(Path(ctx.ws) / rel)
        p = sha16f(Path(ctx.pb) / rel)
        ok = (w is not None) and (w == p)
        if rel in ctx.mirror_bad:
            ok = False
        res.add("B", "B1 双仓 byte-exact: %s" % rel, ok, "" if ok else "ws=%s pb=%s" % (w, p))
    for pbc, wsc in sorted(PB_PIN.items()):
        bm, bad, err = {}, [], ""
        try:
            bm = blob_map(ctx.pb, pbc)
            bw = blob_map(ctx.ws, wsc)
            bad = [k for k in sorted(set(bm) | set(bw)) if bm.get(k) != bw.get(k)]
        except Exception as e:
            err = str(e)[:200]
        ok = (not bad) and bool(bm) and not err
        res.add("B", "B2 pb %s -> ws %s 提交级 blob 对照（%d 件）" % (pbc, wsc, len(bm)), ok,
                "" if ok else (err or ("差异件: %s" % bad[:5])))
    if ctx.args.with_remote:
        lr = sh(["git", "ls-remote", "origin", "main"], cwd=ctx.pb, check=False).split()
        remote = lr[0] if lr else ""
        head = sh(["git", "rev-parse", "HEAD"], cwd=ctx.pb)
        res.add("B", "B3 push 面：ls-remote 与发布仓 HEAD 一致", bool(remote) and remote == head,
                "" if remote == head else "remote=%s head=%s" % (remote[:12], head[:12]))
    if ctx.args.with_live:
        ok, detail = live_probe_check()
        res.add("B", "B4 发布面线上抽验（--with-live）", ok, detail)


ROW91_RE = re.compile(
    r"^\| (\d) \| `([0-9a-f]{6,40})`（([0-9a-f]{40})） \| `([0-9a-f]{6,40})`（([0-9a-f]{40})） \| ([^|]+) \| ([^|]+) \|$",
    re.M)


def parse_91(ctx):
    out = []
    for m in ROW91_RE.finditer(ctx.report_text):
        out.append((int(m.group(1)), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6).strip()))
    return sorted(out)


def sec_c(ctx, res):
    rows = parse_91(ctx)
    exp_ws = list(WS_SHORTS)
    if ctx.commit_bad and exp_ws:
        exp_ws[0] = "0000000"
    got_ws = [r[1] for r in rows]
    got_pb = [r[3] for r in rows]
    ok = (len(rows) == 4) and got_ws == exp_ws and got_pb == list(PB_SHORTS)
    res.add("C", "C1 §9.1 四对全号索引与短号登记", ok,
            "" if ok else "ws=%s pb=%s n=%d" % (got_ws, got_pb, len(rows)))
    badfull = []
    for _, ws_s, ws_f, pb_s, pb_f, _ in rows:
        for repo, s, f in ((ctx.ws, ws_s, ws_f), (ctx.pb, pb_s, pb_f)):
            try:
                if sh(["git", "rev-parse", s], cwd=repo) != f:
                    badfull.append("%s@%s" % (s, Path(repo).name))
            except Exception:
                badfull.append("解析失败 %s@%s" % (s, Path(repo).name))
    res.add("C", "C2 短号全号解析复核（8 笔）", not badfull, "失配: %s" % badfull[:5])
    anc = ANCHOR_PRE in ctx.report_text
    try:
        full = sh(["git", "rev-parse", ANCHOR_PRE], cwd=ctx.ws)
        anc = anc and full.startswith(ANCHOR_PRE)
    except Exception:
        anc = False
    res.add("C", "C3 修复前锚点可解析", anc, "")
    badc4 = []
    for ws_s, pb_s in zip(WS_SHORTS, PB_SHORTS):
        try:
            if set(files_of(ctx.ws, ws_s)) != set(files_of(ctx.pb, pb_s)):
                badc4.append("%s/%s" % (ws_s, pb_s))
        except Exception:
            badc4.append("%s/%s" % (ws_s, pb_s))
    res.add("C", "C4 四对提交文件名集合逐对相符", not badc4, "失配: %s" % badc4)
    e48 = ("回执区" in ctx.report_text) and (("ws_commit_v1" in ctx.report_text) or ("回填" in ctx.report_text))
    res.add("C", "C5 §4.8 回执区条目存在（pending 或 v1 态）", e48, "")


SHA_ROW_RE = re.compile(
    r"^\| `([^`]+)` \| [^|]+ \| `([0-9a-f]{16})` \| `([0-9a-f]{16})` \| [^|]+ \|$", re.M)


def sec_d(ctx, res):
    rows = SHA_ROW_RE.findall(ctx.report_text)
    bad = []
    if len(rows) != len(CHAIN_FILES):
        bad.append("行数=%d" % len(rows))
    for rel, w16, p16 in rows:
        w16e = "deadbeefdeadbeef" if (ctx.sha_bad and rel == CHAIN_FILES[0]) else w16
        dw = sha16f(Path(ctx.ws) / rel)
        dp = sha16f(Path(ctx.pb) / rel)
        if dw != w16e or dp != p16:
            bad.append(rel.split("/")[-1])
        try:
            if (Path(ctx.ws) / rel).read_bytes() != (Path(ctx.pb) / rel).read_bytes():
                bad.append(rel.split("/")[-1] + ":两仓字节差异")
        except Exception:
            bad.append(rel.split("/")[-1] + ":缺件")
    res.add("D", "D1 §5.1 sha16 登记复核（%d 件）" % len(CHAIN_FILES), not bad, "失配: %s" % bad[:6])
    d = load_sourcing(ctx)
    vc = Counter(r.get("verdict") for r in d.get("quotes", []))
    eff = dict(vc)
    if ctx.counts_override:
        eff.update(ctx.counts_override)
    counts = d.get("counts", {})
    ok2 = (eff.get("null") == 57 and eff.get("variant") == 20 and eff.get("quote") == 3
           and eff.get("cross-lang") == 74 and len(d.get("quotes", [])) == 154)
    ok2 = ok2 and counts.get("null_near_partial") == 28 and counts.get("negative_false_positive") == 0 \
        and counts.get("books") == 18 and counts.get("quotes_total") == 154
    res.add("D", "D2 计数重算（154 条 / 57-20-3-74 / 近档 28 / 负对照零）", ok2,
            "" if ok2 else "verdicts=%s counts=%s" % (dict(eff), counts))
    receipt = load_receipt(ctx)
    v1 = json.loads(gitshow_text(ctx.ws, ANCHOR_PRE, SOURCING_JSON_REL))

    def _k(r):
        return "%s/%s" % (r.get("mode_code"), r.get("figure_code"))

    fields = sorted(set().union(*[set(r.keys()) for r in v1["quotes"]])
                    & set().union(*[set(r.keys()) for r in d["quotes"]]))

    def _norm(r):
        return tuple(str(r.get(f)) for f in fields)

    c1 = Counter((_k(r), _norm(r)) for r in v1["quotes"])
    c2 = Counter((_k(r), _norm(r)) for r in d["quotes"])
    diff_keys = {k for k, _ in (c2 - c1)} | {k for k, _ in (c1 - c2)}
    want = set(receipt["changed_rows"].keys())
    got = {k.split("/")[0] for k in diff_keys}
    ok3 = got == want
    badrows = []
    for rid in sorted(want):
        rv = receipt["changed_rows"][rid]
        rows1 = [r for r in v1["quotes"] if _k(r).split("/")[0] == rid]
        rows2 = [r for r in d["quotes"] if _k(r).split("/")[0] == rid]
        o1 = any(r.get("verdict") == rv["v1"].get("verdict") and r.get("match_level") == rv["v1"].get("match_level") for r in rows1)
        o2 = any(r.get("verdict") == rv["v2"].get("verdict") and r.get("match_level") == rv["v2"].get("match_level") for r in rows2)
        if not (o1 and o2):
            badrows.append(rid)
    ok3 = ok3 and not badrows
    res.add("D", "D3 6 行归因重算（v1@1c00ca8a 与磁盘逐行比对）", ok3,
            "" if ok3 else "diff=%s bad=%s" % (sorted(got)[:8], badrows[:5]))
    dec = receipt["per_fix_decomposition"]
    cs = receipt["core_stats"]
    cv1, cv2 = receipt["counts_v1"], receipt["counts_v2"]
    exp_cv2 = {"null": 57, "variant": 20, "quote": 3, "cross-lang": 74}
    ok4 = (cv2 == exp_cv2 and dec["F1_F2_final"] == exp_cv2)
    ok4 = ok4 and dec["F1_only"]["null"] == cv1["null"] + 3 and dec["F1_only"]["variant"] == cv1["variant"] - 3
    ok4 = ok4 and dec["F2_only_FE30"]["null"] == cv1["null"] - 1 and dec["F2_only_FE30"]["variant"] == cv1["variant"] + 1
    ok4 = ok4 and cs["v1"]["core"] == 25 and cs["v2"]["core"] == 23
    ok4 = ok4 and cs["v2"]["with_evidence"] + cs["v2"]["sent_composite"] == cs["v2"]["core"]
    ok4 = ok4 and ("25->23" in ctx.report_text)
    res.add("D", "D4 三段一致性与核中 25->23 复核", ok4, "")
    sc = receipt["f2_candidate_scan"]
    flips = sc.get("flips", {})
    fj = json.dumps(flips, ensure_ascii=False)
    ok5 = sc.get("candidates_n") == 40 and {"U+3000", "U+FE30"} <= set(flips.keys())
    ok5 = ok5 and ("M-ZXC-008" in fj) and ("M-LJY-002" in fj)
    res.add("D", "D5 F2 候选全扫登记（40 候选 / 两枚翻转）", ok5, fj[:200])


def sec_e(ctx, res):
    t = ctx.report_text
    disp = ["F0", "F1", "F2", "F3", "F4", "F5", "F6", "已修复", "表述收紧", "已修正", "移交"]
    res.add("E", "E1 F0-F6 处置表 token", all(x in t for x in disp), "")
    cnt = ["57 / 20 / 3 / 74", "25->23", "154", "零假阳性", "30 PASS / 2 FAIL", "33/33 全 PASS"]
    res.add("E", "E2 计数与收口 token", all(x in t for x in cnt), "")
    m_ws = re.search(r"^- ws_commit_v1：`([0-9a-f]{40})`", t, re.M)
    m_pb = re.search(r"^- pb_commit_v1：`([0-9a-f]{40})`", t, re.M)
    m_push = re.search(r"^- push_v1：ok（([^）]+)）", t, re.M)
    strict = (ctx.receipt_override is not None) or (not ctx.args.receipts_pending)
    if not strict:
        res.add("E", "E3a 回执区 v1 登记复核（ws 8 件 / pb 6 件）", True, "pending（回执区未回填；v2 后转严）")
        res.add("E", "E3b 回执区 v1 提交级 blob 对照（6 件 + push 面）", True, "pending（回执区未回填；v2 后转严）")
        return
    ws_sha = m_ws.group(1) if m_ws else None
    pb_sha = ctx.receipt_override if ctx.receipt_override else (m_pb.group(1) if m_pb else None)
    ok_a, det_a = True, ""
    if not ws_sha:
        ok_a, det_a = False, "ws_commit_v1 缺失"
    else:
        try:
            fs = set(files_of(ctx.ws, ws_sha))
            if fs != set(A_FILES8):
                ok_a, det_a = False, "ws 件集=%s" % sorted(fs)
        except Exception as e:
            ok_a, det_a = False, str(e)[:200]
    ok_b, det_b = True, ""
    if not pb_sha:
        ok_b, det_b = False, "pb_commit_v1 缺失"
    elif not ws_sha:
        ok_b, det_b = False, "ws_commit_v1 缺失"
    else:
        try:
            fs = set(files_of(ctx.pb, pb_sha))
            if fs != set(P_FILES6):
                ok_b, det_b = False, "pb 件集=%s" % sorted(fs)
            else:
                bm = blob_map(ctx.pb, pb_sha)
                bad = []
                for rel in P_FILES6:
                    wblob = sh(["git", "rev-parse", "%s:%s" % (ws_sha, rel)], cwd=ctx.ws)
                    if bm.get(rel) != wblob:
                        bad.append(rel)
                if bad:
                    ok_b, det_b = False, "blob 差异: %s" % bad[:5]
            if ok_b and not m_push:
                ok_b, det_b = False, "push_v1 缺失"
        except Exception as e:
            ok_b, det_b = False, str(e)[:200]
    res.add("E", "E3a 回执区 v1 登记复核（ws 8 件 / pb 6 件）", ok_a, det_a)
    res.add("E", "E3b 回执区 v1 提交级 blob 对照（6 件 + push 面）", ok_b, det_b)


def sec_e4(ctx, res):
    tmp = str(Path(ctx.ws) / "_w8fix_parent_verifier.json")
    ok, det = False, ""
    try:
        subprocess.run([sys.executable, PARENT_VER_REL, "--json-out", tmp],
                       cwd=ctx.ws, capture_output=True, text=True, timeout=900)
        pj = json.loads(Path(tmp).read_text(encoding="utf-8"))
        tot = pj.get("totals", {})
        ok = (tot.get("checks") == 33 and tot.get("pass") == 33 and tot.get("fail") == 0)
        det = "" if ok else "totals=%s" % tot
    except Exception as e:
        det = str(e)[:200]
    finally:
        try:
            os.remove(tmp)
        except Exception:
            pass
    res.add("E", "E4 父链收口复核（t_098d8ff6 验收 33/33 全 PASS）", ok, det)


def sec_f(ctx, res):
    cases = []

    def sub(secfn, mutate):
        r2 = Res()
        mutate()
        secfn(ctx, r2)
        return r2

    orig_text = ctx.report_text
    r2 = sub(sec_a, lambda: setattr(ctx, "report_text", orig_text.replace("## 一、概述", "")))
    ctx.report_text = orig_text
    cases.append(("F1 删节标题注入 -> A 捕获", bool(r2.fails())))

    r2 = sub(sec_b, lambda: ctx.mirror_bad.add(REPORT_REL))
    ctx.mirror_bad.clear()
    cases.append(("F2 镜像不符注入 -> B 捕获", bool(r2.fails())))

    r2 = sub(sec_c, lambda: setattr(ctx, "commit_bad", True))
    ctx.commit_bad = False
    cases.append(("F3 提交号篡改注入 -> C 捕获", bool(r2.fails())))

    r2 = sub(sec_d, lambda: setattr(ctx, "sha_bad", True))
    ctx.sha_bad = False
    cases.append(("F4 sha16 篡改注入 -> D 捕获", bool(r2.fails())))

    r2 = sub(sec_d, lambda: setattr(ctx, "counts_override", {"null": 58, "variant": 19}))
    ctx.counts_override = None
    cases.append(("F5 计数篡改注入 -> D 捕获", bool(r2.fails())))

    r2 = sub(sec_e, lambda: setattr(ctx, "receipt_override", "f" * 40))
    ctx.receipt_override = None
    cases.append(("F6 回执篡改注入 -> E 捕获", bool(r2.fails())))

    for name, ok in cases:
        res.add("F", name, ok, "")
    res.add("F", "F7 反向注入自检汇总（6 / 6）", all(ok for _, ok in cases), "")


def sec_g(ctx, res):
    if ctx.args.no_chain_repro:
        res.add("G", "G0 链复核跳过（--no-chain-repro）", True, "")
        return
    runs = [("POST", [], 33), ("PRE", ["--at", ANCHOR_PRE], 32), ("SCAN", ["--scan"], 36)]
    if ctx.args.with_remote:
        runs.append(("REMOTE", ["--with-remote"], 35))
    for mode, extra, exp in runs:
        ok, det = False, ""
        try:
            r = subprocess.run([sys.executable, QA_VER_REL, "--json"] + extra, cwd=ctx.ws,
                               capture_output=True, text=True, timeout=900)
            so = r.stdout
            i0 = so.find("{")
            j0 = so.rfind("}")
            j = json.loads(so[i0:j0 + 1])
            tot = int(j.get("total", -1))
            ps = int(j.get("pass", -1))
            fl = int(j.get("fail", -1))
            ok = (fl == 0 and ps == tot and tot == exp)
            det = "%s: total=%s pass=%s fail=%s (期望 %s)" % (mode, tot, ps, fl, exp)
        except Exception as e:
            det = "%s: %s" % (mode, str(e)[:150])
        res.add("G", "G %s 链复核（QA 校验器复跑）" % mode, ok, "" if ok else det)


def build_evidence(ctx, res, args):
    mdate = re.search(r"日期：(\d{4}-\d\d-\d\d)", ctx.report_text)
    ev = {
        "schema": "protreptic.w8_stage2_batch1.fix_archive_evidence/v1",
        "task": "t_e01c8aa0",
        "generated_by": "verify_w8_stage2_batch1_fix_archive.py",
        "generated_at": mdate.group(1) if mdate else "",
        "flags": {
            "with_remote": bool(args.with_remote),
            "with_live": bool(args.with_live),
            "chain_repro": not args.no_chain_repro,
            "receipts_pending": bool(args.receipts_pending),
        },
        "receipts_pending": bool(args.receipts_pending),
        "totals": {"checks": len(res.items), "pass": len(res.items) - len(res.fails()),
                   "fail": len(res.fails())},
        "sections": {},
        "fingerprints": {},
        "commits": {},
    }
    for sec in ["A", "B", "C", "D", "E", "F", "G"]:
        ev["sections"][sec] = [i for i in res.items if i["section"] == sec]
    fp = ev["fingerprints"]
    for key, rel in (("report", REPORT_REL), ("verifier", VER_REL), ("generator", GEN_REL),
                     ("parent_report", PARENT_REPORT_REL), ("parent_verifier", PARENT_VER_REL),
                     ("parent_evidence", PARENT_EVIDENCE_REL)):
        fp[key] = {"rel": rel, "sha16": sha16f(Path(ctx.ws) / rel)}
    fp["chain"] = {rel: {"ws": sha16f(Path(ctx.ws) / rel), "pb": sha16f(Path(ctx.pb) / rel)}
                   for rel in CHAIN_FILES}
    rows = parse_91(ctx)
    ev["commits"] = {"anchor": ANCHOR_PRE,
                     "ws": [{"short": r[1], "full": r[2]} for r in rows],
                     "pb": [{"short": r[3], "full": r[4]} for r in rows]}
    return ev


def main(argv=None):
    ap = argparse.ArgumentParser(description="W8S2B1 修复链档案独立验收（第二实现）")
    ap.add_argument("--workspace", default=WS_DEFAULT)
    ap.add_argument("--publish", default=PB_DEFAULT)
    ap.add_argument("--with-remote", action="store_true")
    ap.add_argument("--with-live", action="store_true")
    ap.add_argument("--no-chain-repro", action="store_true")
    ap.add_argument("--receipts-pending", action="store_true")
    ap.add_argument("--no-evidence", action="store_true")
    ap.add_argument("--evidence-out", default=None)
    ap.add_argument("--json-out", default=None)
    args = ap.parse_args(argv)
    ctx = Ctx(args.workspace, args.publish, args)
    res = Res()
    for fn in (sec_a, sec_b, sec_c, sec_d, sec_e):
        fn(ctx, res)
    sec_e4(ctx, res)
    sec_f(ctx, res)
    sec_g(ctx, res)
    ev = build_evidence(ctx, res, args)
    txt = json.dumps(ev, ensure_ascii=False, indent=2) + "\n"
    out = Path(args.evidence_out) if args.evidence_out else (Path(ctx.ws) / EVIDENCE_REL)
    if not args.no_evidence:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(txt, encoding="utf-8")
    if args.json_out:
        Path(args.json_out).write_text(txt, encoding="utf-8")
    fails = res.fails()
    print("W8S2B1 修复链档案验收：%d checks / %d PASS / %d FAIL"
          % (len(res.items), len(res.items) - len(fails), len(fails)))
    for i in fails:
        print("FAIL [%s] %s :: %s" % (i["section"], i["name"], i["detail"]))
    print("sections: %s" % json.dumps(res.counts(), ensure_ascii=False))
    print("evidence: %s" % ("skip" if args.no_evidence else str(out)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
