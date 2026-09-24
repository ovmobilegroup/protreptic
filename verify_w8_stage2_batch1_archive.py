#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_w8_stage2_batch1_archive.py — Phase21-W8 Stage2 批1 全链档案·独立验收（第二实现）

卡: t_098d8ff6（pigafetta / W8 链尾·文档归档）。

本脚本不 import 生成器（build_w8_stage2_batch1_archive.py），独立读取：
  报告文件 / 两仓文件字节 / git 对象 / 链上数据（账本 / 缓存索引 / 备份 MANIFEST）。

段目:
  A 档案结构（九节 + 关键 token + 件数口径）
  B 镜像面（报告/验收/证据 双仓 byte-exact；pb 四笔提交级 blob 对照）
  C 提交链（8 ws + 4 pb 逐条 git 实测；锚点；§4.2/§4.3 登记面）
  D 链数据面（§5.1 26 件 sha16 复核；§5.4 三段 pin 复核；备份 5/5；缓存 txt 计数 20；
             四态两口径重算；翻面 69/3 重算；links_added 8 键；书级列键归一）
  E 记录面（§4.5 QA 指纹复核；残留 F1/F2/F4 登记；§4.7 回执区自洽）
  F 反向注入自检（6 类突变必被对应段捕获；--selftest）

用法:
  python3 verify_w8_stage2_batch1_archive.py [--workspace DIR] [--publish DIR]
      [--report PATH] [--receipts-pending] [--with-live] [--json-out PATH] [--selftest]
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
WS_DEFAULT = str(REPO_ROOT)
PB_DEFAULT = "/opt/data/release/Protreptic-publish"

REPORT_REL = "docs/research/phase21w8_stage2_batch1_archive_report.md"
GEN_REL = "build_w8_stage2_batch1_archive.py"
VER_REL = "verify_w8_stage2_batch1_archive.py"
EVIDENCE_REL = "docs/research/phase21w8_stage2_batch1_archive_evidence.json"

WS_COMMITS = ["20b13092", "ce1dc46b", "60d5d509", "58f34f88",
              "004332b4", "eda40f5b", "b5967043", "b0e2b0a8"]
PB_COMMITS = ["023a794", "c522897", "88cc86a", "384faae"]
PB_PIN = {"023a794": "004332b4", "c522897": "eda40f5b",
          "88cc86a": "b5967043", "384faae": "b0e2b0a8"}
ANCHORS = ["004332b4", "eda40f5b", "b5967043", "b0e2b0a8"]
SECTIONS = ["## 一、概述", "## 二、背景", "## 三、方法", "## 四、执行（登记链）",
            "## 五、证据", "## 六、核验", "## 七、残留与账务登记", "## 八、下一步",
            "## 九、附链（全号索引与复跑）"]
PIN_PATHS = ["data/modes_data.json", "data/source_links.json",
             "data/audit/source_texts.json", "data/audit/findings.json",
             "data/audit/verification_status.json",
             "web/src/generated/siteCounts.ts",
             "docs/architecture/static_data_manifest.json"]
BACKUP_DIR = "data/backup_merge_W8B1_20260924_113742"
LEDGER_REL = "data/audit/phase21w8_stage2_batch1_landing_ledger.json"
LIVE_BASE = "https://ovmobilegroup.github.io/protreptic/"


def sha16b(b):
    return hashlib.sha256(b).hexdigest()[:16]


def file_bytes(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError:
        return None


def git(*args, cwd, text=True):
    r = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("git %s (cwd=%s): %s" % (" ".join(args), cwd,
                                                    r.stderr.decode("utf-8", "replace")[:200]))
    out = r.stdout.decode("utf-8", "replace")
    return out if text else r.stdout


def gbytes(commit, path, cwd):
    r = subprocess.run(["git", "show", "%s:%s" % (commit, path)], cwd=cwd, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def jload(b):
    return json.loads(b.decode("utf-8"))


def load_quarantine(ws):
    import importlib.util
    cand = Path(ws) / "tools" / "_quarantine.py"
    spec = importlib.util.spec_from_file_location("_q_arch_verify", str(cand))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set((getattr(mod, "QUARANTINE", {}) or {}).keys())


def parse_sha_rows(t):
    rows = []
    for m in re.finditer(r"^\| ([^|]+?) \| `([0-9a-f]{16})` \| `([0-9a-f]{16})` \| 等于（byte-exact） \|$", t, re.M):
        rows.append((m.group(1).strip(), m.group(2), m.group(3)))
    return rows


def parse_pin_rows(t):
    rows = []
    for m in re.finditer(r"^\| ([^|]+?) \| `([0-9a-f]{16})` \| `([0-9a-f]{16})` \| `[0-9a-f]{16}` \|", t, re.M):
        rows.append((m.group(1).strip(), m.group(2), m.group(3)))
    return rows


def parse_commit_index(t):
    ws, pb, cur = [], [], None
    for line in t.splitlines():
        if line.startswith("- 工作仓（W8 链"):
            cur = "ws"
            continue
        if line.startswith("- 发布仓（W8 链"):
            cur = "pb"
            continue
        if line.startswith("- 锚点"):
            cur = None
            continue
        m = re.match(r"^  - ([0-9a-f]{7,40})  ([0-9a-f]{40})  (\d\d-\d\d \d\d:\d\d)$", line)
        if m and cur:
            (ws if cur == "ws" else pb).append((m.group(1), m.group(2), m.group(3)))
    return ws, pb


class Res:
    def __init__(self):
        self.items = []

    def add(self, section, name, ok, detail=""):
        self.items.append({"section": section, "name": name, "ok": bool(ok),
                           "detail": "" if ok else str(detail)[:300]})

    def fails(self):
        return [i for i in self.items if not i["ok"]]


def sec_A(ctx, res):
    t = ctx["report_text"]
    res.add("A", "A1 九节标题齐备", all(s in t for s in SECTIONS),
            "缺失: %s" % [s for s in SECTIONS if s not in t])
    toks = ["t_098d8ff6", "t_6ed4fe0d", "t_70a8cbce", "t_b85ae14a", "t_e727be57",
            "IDEMPOTENT", "byte-exact", "ls-remote", "154", "1018", "回执区"]
    res.add("A", "A2 关键 token 齐备", all(x in t for x in toks),
            "缺失: %s" % [x for x in toks if x not in t])
    res.add("A", "A3 件数口径（26 链件 / 20 txt / 五卡 / 八笔 / 四笔）",
            ("26 件" in t and "20 件" in t and "（5 卡）" in t)
            and "8 笔" in t and "4 笔" in t, "口径 token 缺失")
    res.add("A", "A4 上/下游卡号引用完整", len(re.findall(r"t_[0-9a-f]{8}", t)) >= 20,
            "t_ 引用计数不足")


def sec_B(ctx, res):
    mut = ctx.get("mutations", {})
    for rel in [REPORT_REL, VER_REL, EVIDENCE_REL]:
        wb = file_bytes(str(Path(ctx["ws"]) / rel))
        pb = file_bytes(str(Path(ctx["pb"]) / rel))
        ok = wb is not None and pb is not None and wb == pb and len(wb) > 0
        if mut.get("B") == rel:
            ok = False
        res.add("B", "B1 双仓 byte-exact: %s" % rel, ok,
                "ws=%s pb=%s" % ("缺" if wb is None else len(wb),
                                 "缺" if pb is None else len(pb)))
    for pbc, wsc in sorted(PB_PIN.items()):
        files = git("diff-tree", "--no-commit-id", "--name-only", "-r", pbc, cwd=ctx["pb"]).split()
        bad = []
        for f in files:
            b1 = gbytes(pbc, f, ctx["pb"])
            b2 = gbytes(wsc, f, ctx["ws"])
            if b1 is None or b2 is None or b1 != b2:
                bad.append(f)
        res.add("B", "B2 pb %s -> ws %s 提交级 blob 对照（%d 件）" % (pbc, wsc, len(files)),
                bool(files) and not bad, "不符件: %s" % bad[:6])


def sec_C(ctx, res):
    t = ctx["report_text"]
    wsl, pbl = parse_commit_index(t)
    mutc = ctx.get("mutations", {}).get("C")
    if mutc:
        wsl = [(s, mutc if s == wsl[0][0] else f, d) for (s, f, d) in wsl]
    res.add("C", "C1 附链登记 8 ws / 4 pb 条目", len(wsl) == 8 and len(pbl) == 4,
            "ws=%d pb=%d" % (len(wsl), len(pbl)))
    bad = []
    for short, full, date in wsl + pbl:
        try:
            have = git("rev-parse", short, cwd=ctx["ws"] if short in WS_COMMITS else ctx["pb"]).strip()
        except RuntimeError as e:
            bad.append("%s: %s" % (short, e))
            continue
        if have != full:
            bad.append("%s->%s" % (short, have[:12]))
    res.add("C", "C2 短号解析全号 == 登记全号（ws+pb 12 笔）", not bad, "不符: %s" % bad[:6])
    bad2 = []
    for short, full, date in wsl:
        got = git("show", "-s", "--format=%cd", "--date=format:%m-%d %H:%M", short, cwd=ctx["ws"]).strip()
        if got != date:
            bad2.append("%s: %s != %s" % (short, got, date))
    res.add("C", "C3 ws 提交日期 == 登记日期", not bad2, "不符: %s" % bad2[:6])
    ok = True
    for a in ANCHORS:
        ok = ok and bool(git("rev-parse", a, cwd=ctx["ws"]).strip())
    res.add("C", "C4 锚点可解析（004332b4 / eda40f5b / b5967043 / b0e2b0a8）", ok)
    for s in WS_COMMITS[:8]:
        if s not in t:
            res.add("C", "C5 §4.2/§9.1 登记 ws 短号", False, "缺 %s" % s)
    for s in PB_COMMITS[:4]:
        if s not in t:
            res.add("C", "C5 §4.3/§9.1 登记 pb 短号", False, "缺 %s" % s)
    res.add("C", "C5 §4.2/§4.3 短号齐备", all(s in t for s in WS_COMMITS + PB_COMMITS))


def sec_D(ctx, res):
    t = ctx["report_text"]
    mutd = ctx.get("mutations", {}).get("D", {})
    # D1: §5.1 26 件 sha16 双仓复核
    rows = parse_sha_rows(t)
    bad = []
    if mutd.get("sha_row"):
        rows = [(rows[0][0], mutd["sha_row"], rows[0][2])] + rows[1:]
    for rel, a, b in rows:
        wb = file_bytes(str(Path(ctx["ws"]) / rel))
        pb = file_bytes(str(Path(ctx["pb"]) / rel))
        if wb is None or pb is None or sha16b(wb) != a or sha16b(pb) != b:
            bad.append(rel)
    res.add("D", "D1 §5.1 sha16 登记复核（%d 件，双仓）" % len(rows),
            len(rows) >= 26 and not bad, "行数=%d 不符=%s" % (len(rows), bad[:6]))
    # D2: §5.4 三段 pin（before=004332b4^ / after=eda40f5b）
    pins = parse_pin_rows(t)
    bad2 = []
    if mutd.get("pin_before"):
        pins = [(pins[0][0], mutd["pin_before"], pins[0][2])] + pins[1:]
    for rel, before, after in pins:
        bb = gbytes("004332b4^", rel, ctx["ws"])
        ab = gbytes("eda40f5b", rel, ctx["ws"])
        if bb is None or ab is None or sha16b(bb) != before or sha16b(ab) != after:
            bad2.append(rel)
    res.add("D", "D2 §5.4 三段 pin 复核（%d 件；before/after 为 git 对象实测）" % len(pins),
            sorted(p[0] for p in pins) == sorted(PIN_PATHS) and not bad2,
            "行数=%d 不符=%s" % (len(pins), bad2[:6]))
    # D3: 备份 MANIFEST 5/5
    mb = file_bytes(str(Path(ctx["ws"]) / BACKUP_DIR / "MANIFEST.json"))
    bad3 = []
    n = 0
    if mb is None:
        bad3.append("MANIFEST 缺")
    else:
        doc = jload(mb)
        for e in doc.get("files", []):
            n += 1
            bf = file_bytes(str(Path(ctx["ws"]) / BACKUP_DIR / e["backup_file"]))
            if bf is None or hashlib.sha256(bf).hexdigest() != e["sha256"]:
                bad3.append(e["path"])
    res.add("D", "D3 备份 MANIFEST 逐件 sha256 复核（%d 件）" % n, n == 5 and not bad3, "不符=%s" % bad3[:6])
    # D4: 缓存 txt 计数（ce1dc46b 新增 20 件，其中 zh-cn 4 件）
    dt = git("diff-tree", "-r", "--name-status", "--no-commit-id", "ce1dc46b", "--", "data/audit/source_texts", cwd=ctx["ws"])
    added = [ln.split("\t", 1)[1] for ln in dt.splitlines() if ln.startswith("A\t")]
    txts = [f for f in added if f.endswith(".txt")]
    zh = [f for f in txts if ".zh-cn" in f]
    res.add("D", "D4 缓存 txt 计数（新增 %d 件 / zh-cn %d 件）" % (len(txts), len(zh)),
            len(txts) == 20 and len(zh) == 4, "新增=%d zh=%d" % (len(txts), len(zh)))
    # D5: 四态两口径重算（after=eda40f5b 实测；before=备份态）
    mdb = gbytes("eda40f5b", "data/modes_data.json", ctx["ws"])
    mdf = file_bytes(str(Path(ctx["ws"]) / BACKUP_DIR / "data__modes_data.json"))
    ok5 = False
    detail5 = "数据缺"
    if mdb and mdf:
        md = jload(mdb)
        bmd = jload(mdf)
        qset = load_quarantine(ctx["ws"])
        cnt = Counter((m.get("verification") or {}).get("status") for m in md["modes"])
        pub = Counter((m.get("verification") or {}).get("status") for m in md["modes"]
                      if str(m.get("figure_code")) not in qset)
        bcnt = Counter((m.get("verification") or {}).get("status") for m in bmd["modes"])
        bpub = Counter((m.get("verification") or {}).get("status") for m in bmd["modes"]
                       if str(m.get("figure_code")) not in qset)
        ok5 = (cnt.get("verified") == 1018 and cnt.get("pending") == 1887
               and cnt.get("suspect") == 55 and cnt.get("unverifiable") == 351 and sum(cnt.values()) == 3311
               and pub.get("verified") == 1018 and pub.get("pending") == 1855
               and pub.get("suspect") == 38 and pub.get("unverifiable") == 340 and sum(pub.values()) == 3251
               and bcnt.get("verified") == 949 and bcnt.get("pending") == 1959
               and bcnt.get("suspect") == 52 and bcnt.get("unverifiable") == 351 and sum(bcnt.values()) == 3311
               and bpub.get("verified") == 949 and bpub.get("pending") == 1927
               and bpub.get("suspect") == 35 and bpub.get("unverifiable") == 340 and sum(bpub.values()) == 3251)
        detail5 = "after=%s pub=%s before=%s bpub=%s" % (dict(cnt), dict(pub), dict(bcnt), dict(bpub))
    res.add("D", "D5 四态两口径重算（after 1018/1887/55/351 与 1018/1855/38/340；before 949/1959/52/351 与 949/1927/35/340）",
            ok5, detail5)
    # D6: 翻面重算（多重集差 69 verified / 3 suspect；包内；包外零）
    ok6 = False
    detail6 = "数据缺"
    if mdb and mdf:
        bstat = Counter((m.get("mode_code"), (m.get("verification") or {}).get("status")) for m in bmd["modes"])
        astat = Counter((m.get("mode_code"), (m.get("verification") or {}).get("status")) for m in md["modes"])
        old_by, new_by = {}, {}
        for (c, s), n in (bstat - astat).items():
            old_by.setdefault(c, []).append((s, n))
        for (c, s), n in (astat - bstat).items():
            new_by.setdefault(c, []).append((s, n))
        trans = Counter()
        for c in set(old_by) | set(new_by):
            for s1, n1 in old_by.get(c, []):
                for s2, n2 in new_by.get(c, []):
                    trans[(s1, s2)] += min(n1, n2)
        led = jload(file_bytes(str(Path(ctx["ws"]) / LEDGER_REL)))
        item_codes = {str(i.get("mode_code")) for i in (led.get("items") or [])}
        flipped = set(old_by) | set(new_by)
        outside = (led.get("cross_checks") or {}).get("side_effect_flips_outside_pack")
        ok6 = (trans.get(("pending", "verified")) == 69 and trans.get(("pending", "suspect")) == 3
               and sum(trans.values()) == 72 and flipped <= item_codes and outside == [])
        detail6 = "trans=%s outside=%s" % (dict(trans), outside)
    res.add("D", "D6 翻面重算 69/3（72）＋全在包内＋包外零", ok6, detail6)


def sec_E(ctx, res):
    t = ctx["report_text"]
    # E1: §4.5 QA 指纹复核
    fps = {"84ff028da6bee8d4": LEDGER_REL,
           "886a7c90c560e727": "docs/research/phase21w8_stage2_batch1_landing_report.md",
           "0a6f5a5ae266281b": "docs/research/phase21w8_stage2_batch1_landing_evidence.json",
           "81d6329c92afe97c": "tools/build_batch1_landing_ledger.py",
           "4d55095b5776a82f": "tools/verify_batch1_qa_espinosa.py"}
    bad = []
    for fp, rel in fps.items():
        wb = file_bytes(str(Path(ctx["ws"]) / rel))
        if wb is None or sha16b(wb) != fp:
            bad.append(rel)
        if fp not in t:
            bad.append("报告缺 %s" % fp)
    res.add("E", "E1 §4.5 复核指纹（5 枚）与实测一致", not bad, "不符=%s" % bad[:8])
    res.add("E", "E2 未闭合项照登（QA-F1/F2/F4 及其判定）",
            all(x in t for x in ["QA-F1", "QA-F2", "QA-F4", "25->22", "55->54"]), "残留 token 缺失")
    # E3: §4.7 回执区自洽
    m = re.search(r"- ws_commit_v1：`([0-9a-f]{7,40})`", t)
    m2 = re.search(r"- pb_commit_v1：`([0-9a-f]{7,40})`", t)
    pending = ctx.get("receipts_pending", True)
    if pending:
        res.add("E", "E3 回执区（--receipts-pending 过渡面）", "回填区" in t,
                "过渡面应含回填区字样")
    else:
        ok = False
        detail = ""
        mutr = ctx.get("mutations", {}).get("E")
        if m and m2:
            wsc, pbc = m.group(1), m2.group(1)
            if mutr:
                wsc = mutr
            try:
                wfiles = set(git("diff-tree", "--no-commit-id", "--name-only", "-r", wsc, cwd=ctx["ws"]).split())
                pfiles = set(git("diff-tree", "--no-commit-id", "--name-only", "-r", pbc, cwd=ctx["pb"]).split())
                ok = (wfiles == {REPORT_REL, GEN_REL, VER_REL, EVIDENCE_REL}
                      and pfiles == {REPORT_REL, VER_REL, EVIDENCE_REL}
                      and "push_v1：ok" in t)
                detail = "ws=%s pb=%s" % (sorted(wfiles), sorted(pfiles))
            except RuntimeError as e:
                detail = str(e)[:200]
        else:
            detail = "回执行缺失"
        res.add("E", "E3 §4.7 回执区自洽（ws 4 件 / pb 3 件 / push ok）", ok, detail)


def sec_F(ctx, res):
    # F: 反向注入自检（6 类突变必被对应段捕获）
    muts = [
        ("A", "报告删节标题", lambda c: c.update(report_text=c["report_text"].replace("## 六、核验", "## 六、XX"))),
        ("B", "镜像不符注入", lambda c: c.setdefault("mutations", {}).update({"B": REPORT_REL})),
        ("C", "提交全号篡改", lambda c: c.setdefault("mutations", {}).update(
            {"C": "0" * 40})),
        ("D", "sha16 行篡改", lambda c: c.setdefault("mutations", {}).update(
            {"D": {"sha_row": "0" * 16}})),
        ("D", "pin before 篡改", lambda c: c.setdefault("mutations", {}).update(
            {"D": {"pin_before": "0" * 16}})),
        ("E", "回执 sha 篡改", lambda c: c.setdefault("mutations", {}).update(
            {"E": "ffffffffffffffffffffffffffffffffffffffff"})),
    ]
    fns = {"A": sec_A, "B": sec_B, "C": sec_C, "D": sec_D, "E": sec_E}
    n_ok = 0
    for sec, label, mut in muts:
        c2 = dict(ctx)
        c2["report_text"] = ctx["report_text"]
        c2["mutations"] = dict(ctx.get("mutations", {}))
        c2["receipts_pending"] = False
        mut(c2)
        r2 = Res()
        fns[sec](c2, r2)
        caught = bool(r2.fails())
        if caught:
            n_ok += 1
        res.add("F", "F 注入「%s」-> %s 段捕获" % (label, sec), caught,
                "未捕获（%s 段应 FAIL）" % sec)
    res.add("F", "F 自检合计 6/6", n_ok == 6, "捕获 %d/6" % n_ok)


def live_checks(ctx, res):
    def get(url):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "w8-arch-verify"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, r.read()
        except Exception as e:
            return 0, str(e).encode()
    st, body = get(LIVE_BASE)
    res.add("LIVE", "L1 首页 HTTP 200", st == 200, "status=%s" % st)
    st2, body2 = get(LIVE_BASE + "credibility/")
    res.add("LIVE", "L2 可信度页 HTTP 200 且含 1019/1845",
            st2 == 200 and b"1019" in body2 and b"1845" in body2, "status=%s" % st2)


def main(argv=None):
    ap = argparse.ArgumentParser(description="W8 Stage2 batch1 archive independent verifier")
    ap.add_argument("--workspace", default=WS_DEFAULT)
    ap.add_argument("--publish", default=PB_DEFAULT)
    ap.add_argument("--report", default=None)
    ap.add_argument("--receipts-pending", action="store_true")
    ap.add_argument("--with-live", action="store_true")
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    rep = args.report or str(Path(args.workspace) / REPORT_REL)
    rb = file_bytes(rep)
    if rb is None:
        print("FAIL: 报告不存在: %s" % rep)
        return 2
    ctx = {"ws": args.workspace, "pb": args.publish,
           "report_text": rb.decode("utf-8"), "receipts_pending": args.receipts_pending,
           "mutations": {}}
    res = Res()
    sec_A(ctx, res)
    sec_B(ctx, res)
    sec_C(ctx, res)
    sec_D(ctx, res)
    sec_E(ctx, res)
    if args.with_live:
        live_checks(ctx, res)
    sec_F(ctx, res)

    fails = res.fails()
    z = [i for i in res.items if not i["ok"]]
    for i in res.items:
        mark = "PASS" if i["ok"] else "FAIL"
        print("[%s] %s %s%s" % (mark, i["section"], i["name"],
                                "" if i["ok"] else (" <- " + i["detail"])))
    print()
    print("totals: %d checks, %d PASS, %d FAIL" % (len(res.items), len(res.items) - len(fails), len(fails)))

    if args.selftest:
        r2 = Res()
        sec_F(ctx, r2)
        print("selftest: %d/%d mutated-catches" % (
            len([i for i in r2.items if i["ok"] and "捕获" in i["name"]]),
            len([i for i in r2.items if "捕获" in i["name"] and i["name"].startswith("F 注入")])))

    rc = 1 if fails else 0
    if args.json_out or True:
        out = args.json_out or str(Path(args.workspace) / EVIDENCE_REL)
        ev = {
            "schema": "protreptic.w8_stage2_batch1.archive_evidence/v1",
            "task": "t_098d8ff6",
            "generated_by": "verify_w8_stage2_batch1_archive.py",
            "generated_at": "2026-09-24",
            "receipts_pending": bool(args.receipts_pending),
            "totals": {"checks": len(res.items), "pass": len(res.items) - len(fails), "fail": len(fails)},
            "sections": {},
            "fingerprints": {
                REPORT_REL: sha16b(rb),
                VER_REL: sha16b(file_bytes(str(Path(args.workspace) / VER_REL)) or b""),
                GEN_REL: sha16b(file_bytes(str(Path(args.workspace) / GEN_REL)) or b""),
                EVIDENCE_REL: None,
            },
        }
        for i in res.items:
            ev["sections"].setdefault(i["section"], []).append(
                {"name": i["name"], "ok": i["ok"], "detail": i["detail"]})
        ev["fingerprints"][EVIDENCE_REL] = "（本件；自指省略）"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(ev, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("evidence -> %s" % out)
    return rc


if __name__ == "__main__":
    sys.exit(main())
