#!/usr/bin/env python3
"""verify_batch1_sourcing_fix_qa_espinosa.py -- W8S2B1 素材包端修复（卡 t_2ce1e334）独立 QA 双锚点校验器。

（卡 t_a407cb32 / espinosa；只读：全部对象经 git show 读取，不写任何仓内文件）

用法
    python3 tools/verify_batch1_sourcing_fix_qa_espinosa.py                 # 默认 HEAD：修复后态全断言
    python3 tools/verify_batch1_sourcing_fix_qa_espinosa.py --at 1c00ca8a   # 修复前锚点：缺陷复现断言（必现）
    python3 tools/verify_batch1_sourcing_fix_qa_espinosa.py --json          # 机读摘要
    python3 tools/verify_batch1_sourcing_fix_qa_espinosa.py --scan          # 追加 F2 候选全扫（较慢）
    python3 tools/verify_batch1_sourcing_fix_qa_espinosa.py --with-remote   # 追加 push 面（ls-remote/fetch）

口径
    - 第二实现：本脚本内置独立实现（不 import 被审工具模块），按文档语义重算 154 行并逐字段对照产物。
    - 双锚点：1c00ca8a（修复前）复现两类缺陷（F1 分段仅首段命中 / F2 U+FE30 未归一）；
      HEAD（修复后）全 PASS。mode 由给定 ref 的工具版本自动判定。
    - 边界：t_2ce1e334 回执清单（工具 1 件 + 报告 2 件 + 落地报告 1 件 + 回执 1 件）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_REPO_DEFAULT = _HERE.parent.parent
REPO = _REPO_DEFAULT if (_REPO_DEFAULT / '.git').exists() else Path('/opt/data/workspace/Protreptic')
PB = Path('/opt/data/release/Protreptic-publish')

PRE_REF = '1c00ca8a821018cdb1ff28cd934112a387e844ad'
FIX_REF = '68fd5569dd18c57b2b21600fd7cb29186fef1867'
FIX_SUPP = '5705b030a486593982442ce2c94cae829c41e8df'
PB_REF = '9afe48e279ea492154cca7306b3ac0e05db9bf67'
PB_SUPP = '5b693bb'
RECEIPT = 'data/audit/phase21w8_stage2_batch1_sourcing_fix_receipt.json'
PRODUCT = 'docs/research/phase21w8_stage2_batch1_sourcing_report.json'
PRODUCT_MD = 'docs/research/phase21w8_stage2_batch1_sourcing_report.md'
LANDING_MD = 'docs/research/phase21w8_stage2_batch1_landing_report.md'
TOOL = 'tools/build_batch1_sourcing_pack.py'
LOG = 'data/audit/phase21w8_stage2_batch1_verify.log'
MODES = 'data/modes_data.json'
BOOKLIST = 'docs/research/phase21w8_stage2_batch1_booklist.json'
INDEX = 'data/audit/source_texts_w8_stage2_batch1.json'

OLD_CJK = "\u3001\u3002\uff0c\uff0e\uff1b\uff1a\uff1f\uff01\u201c\u201d\u2018\u2019\uff08\uff09\u3014\u3015\u3010\u3011\u3008\u3009\u300a\u300b\u2026\u2014\u00b7\u2500\uff5e~\u2550\uff0d"
EXTRA = "\ufe30\u3000"
ASCII_PUNCT = " \t\r\n.,;:?!\"'()[]{}<>|/\\_-+=*&^%$#@`"
CROSS_LANG = {"\u7406\u60f3\u56fd", "\u5f62\u800c\u4e0a\u5b66", "\u5965\u6797\u5339\u514b\u56de\u5fc6\u5f55", "\u8bd7\u5b66", "\u4fc4\u72c4\u6d66\u65af\u738b", "\u4f0a\u5229\u4e9a\u7279", "\u5965\u5fb7\u8d5b", "\u5b89\u63d0\u6208\u6d85", "\u6218\u4e89\u53f2"}
MIN_WEAK = 6
LEAD_RE = r"^\u300a[^\u300b]*\u300b[^\uff1a:]{0,16}[\uff1a:]\s*[\u2018\u201c\u300e\u300c]?(.*?)[\u2019\u201d\u300f\u300d]?\s*$"
V1_COUNTS = {"null": 55, "variant": 22, "quote": 3, "cross-lang": 74}
V2_COUNTS = {"null": 57, "variant": 20, "quote": 3, "cross-lang": 74}
COMBO_EXPECT = {"old_old": V1_COUNTS, "new_old": {"null": 58, "variant": 19, "quote": 3, "cross-lang": 74},
                "old_new": {"null": 54, "variant": 23, "quote": 3, "cross-lang": 74}, "new_new": V2_COUNTS}

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    if not ARGS.json:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  " + detail) if detail else ""))


def git_show(ref, path):
    r = subprocess.run(["git", "-C", str(REPO), "show", ref + ":" + path], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def sha16b(b):
    return hashlib.sha256(b).hexdigest()[:16]


def normer(extra=""):
    strip = set(OLD_CJK + ASCII_PUNCT + extra)

    def norm(text):
        return "".join(ch for ch in (text or "") if ch not in strip)
    return norm


def segments(quote, norm):
    parts = [p for p in re.split(r"\u2026+", quote or "") if norm(p)]
    return parts or [quote or ""]


def match_quote(segs, text, text_light, text_norm, norm, mode):
    """mode='old' 复现修复前语义（任一段标点归一命中即 early-return）；mode='new' 复现修复后语义（各段须全命中）。"""
    pos = 0
    punct_hit = None
    for s in segs:
        if not norm(s):
            continue
        sl = re.sub(r"\s+", "", s)
        i = text_light.find(sl)
        if i >= 0:
            pos = i
            continue
        sn = norm(s)
        j = text_norm.find(sn)
        if j < 0:
            return None
        if mode == "old":
            return "punct", j, text_norm[max(0, j - 24): j + len(sn) + 24]
        if punct_hit is None:
            punct_hit = (j, text_norm[max(0, j - 24): j + len(sn) + 24])
    if punct_hit is not None:
        return "punct", punct_hit[0], punct_hit[1]
    sl = re.sub(r"\s+", "", segs[0]) if segs else ""
    i = text_light.find(sl)
    snip = text_light[max(0, i - 24): i + len(sl) + 24] if i >= 0 else ""
    return "whitespace", pos, snip


ARGS = None


def load_cache(ref, extra):
    idx = json.loads(git_show(ref, INDEX).decode("utf-8"))
    norm = normer(extra)
    cache = {}
    for e in idx.get("entries", []):
        label = (e.get("label") or e.get("key") or "").strip("\u300a\u300b")
        item = {"entry": e}
        for slot, fname in (("raw", e.get("file")), ("zh", (e.get("zh_cn") or {}).get("file"))):
            if not fname:
                continue
            b = git_show(ref, fname)
            if b is None:
                continue
            text = b.decode("utf-8")
            item[slot] = text
            item[slot + "_light"] = re.sub(r"\s+", "", text)
            item[slot + "_norm"] = norm(text)
        cache[label] = item
    return cache


def classify(book, q, conv, cache, mode, norm):
    item = cache.get(book) or {}
    if book in CROSS_LANG:
        return {"verdict": "cross-lang", "match_level": None, "match_path": None}
    raw, zh = item.get("raw"), item.get("zh")
    R = item.get("raw_light") or ""
    RN = item.get("raw_norm") or ""
    Z = item.get("zh_light") or ""
    ZN = item.get("zh_norm") or ""
    RWF = (item.get("entry") or {}).get("file")
    ZWF = ((item.get("entry") or {}).get("zh_cn") or {}).get("file")
    segs = segments(q, norm)
    alts = [(q, segs, segments(conv, norm) if conv else None)]
    mm = re.match(LEAD_RE, q or "", flags=re.S)
    if mm and norm(mm.group(1)):
        q1 = mm.group(1)
        c1 = segments(conv, norm) if conv else None
        if conv:
            mm2 = re.match(LEAD_RE, conv, flags=re.S)
            if mm2 and norm(mm2.group(1)):
                c1 = segments(mm2.group(1), norm)
        alts.append((q1, segments(q1, norm), c1))
    for ai, (qq, sgs, csgs) in enumerate(alts):
        tail = "(\u53bb\u51a0\u540d\u540e)" if ai else ""
        hit = match_quote(sgs, raw, R, RN, norm, mode) if (raw and sgs) else None
        if hit:
            return {"verdict": "quote", "match_level": hit[0], "match_path": "raw",
                    "evidence": {"file": RWF, "snippet": hit[2]}, "tail": tail,
                    "quote_alt": alts[1][0] if len(alts) > 1 else None}
        hit = match_quote(csgs, raw, R, RN, norm, mode) if (raw and csgs) else None
        if hit:
            return {"verdict": "variant", "match_level": "zh-hant", "match_path": "raw",
                    "evidence": {"file": RWF, "snippet": hit[2]}, "tail": tail,
                    "quote_alt": alts[1][0] if len(alts) > 1 else None}
        hit = match_quote(sgs, zh, Z, ZN, norm, mode) if (zh and sgs) else None
        if hit:
            return {"verdict": "variant", "match_level": "zh-cn", "match_path": "zh-cn",
                    "evidence": {"file": ZWF, "snippet": hit[2]}, "tail": tail,
                    "quote_alt": alts[1][0] if len(alts) > 1 else None}
        hit = match_quote(csgs, zh, Z, ZN, norm, mode) if (zh and csgs) else None
        if hit:
            return {"verdict": "variant", "match_level": "zh-cn+hant", "match_path": "zh-cn",
                    "evidence": {"file": ZWF, "snippet": hit[2]}, "tail": tail,
                    "quote_alt": alts[1][0] if len(alts) > 1 else None}
    found = []
    sn = norm(q)
    for other, oitem in cache.items():
        if other == book:
            continue
        if (oitem.get("raw_norm") and sn and sn in oitem["raw_norm"]) or \
           (oitem.get("zh_norm") and sn and sn in oitem["zh_norm"]):
            found.append(other)
    rawn, zhn = RN, ZN
    shingle = None
    if sn and raw:
        wins = [sn[i:i + 3] for i in range(max(1, len(sn) - 2))]
        wh = sum(1 for x in wins if x in rawn or x in zhn)
        shingle = round(wh / len(wins), 3)
    sents = [s for s in re.split(r"[\u3002\uff1f\uff01]", q or "") if norm(s)]
    csents = [s for s in re.split(r"[\u3002\uff1f\uff01]", conv) if norm(s)] if conv else []
    sh = 0
    for i, s in enumerate(sents):
        s1 = norm(s)
        s2 = norm(csents[i]) if i < len(csents) else None
        if s1 in rawn or s1 in zhn or (s2 and (s2 in rawn or s2 in zhn)):
            sh += 1
    sent_hits = [sh, len(sents)] if sents else None
    if sents and sh == len(sents) and len(sents) >= 2 and all(len(norm(s)) >= 6 for s in sents):
        return {"verdict": "variant", "match_level": "sent-composite", "match_path": "raw|zh-cn",
                "sent_hits": sent_hits, "shingle": shingle, "quote_alt": alts[1][0] if len(alts) > 1 else None}
    near = False
    if sents and sh >= max(2, int(len(sents) * 0.5 + 0.999)):
        near = True
    if (shingle or 0) >= 0.8:
        near = True
    probes = [x for x in (sn, (norm(conv) if conv else "")) if x and len(x) >= 12]
    best3 = shingle or 0.0
    bestL = 0.0
    for probe in probes:
        w3 = [probe[i:i + 3] for i in range(max(1, len(probe) - 2))]
        r3 = sum(1 for x in w3 if x in rawn or x in zhn) / len(w3)
        run = 0
        for i in range(len(probe)):
            for L in range(len(probe) - i, run, -1):
                if probe[i:i + L] in rawn or probe[i:i + L] in zhn:
                    run = L
                    break
        best3 = max(best3, r3)
        bestL = max(bestL, run / len(probe))
    shingle2 = longest = None
    if raw:
        shingle2 = round(best3, 3)
        longest = round(bestL, 3)
    if best3 >= 0.8 or bestL >= 0.35:
        near = True
    return {"verdict": "null", "match_level": None, "match_path": None, "elsewhere": found[:6],
            "sent_hits": sent_hits, "shingle": shingle2 if raw else None,
            "longest": longest if raw else None,
            "near_partial": near if (raw and (shingle2 is not None or sents)) else None,
            "quote_alt": alts[1][0] if len(alts) > 1 else None}


def row_issues(r, c):
    issues = []
    if c["verdict"] != r["verdict"]:
        issues.append("verdict")
    if c.get("match_level") != r.get("match_level"):
        issues.append("match_level")
    if c.get("match_path") != r.get("match_path"):
        issues.append("match_path")
    if c.get("sent_hits") != r.get("sent_hits"):
        issues.append("sent_hits")
    if c.get("shingle") != r.get("shingle_ratio"):
        issues.append("shingle")
    if c.get("longest") != r.get("longest_ratio"):
        issues.append("longest")
    if c.get("near_partial") != r.get("near_partial"):
        issues.append("near_partial")
    if c.get("elsewhere") != r.get("elsewhere"):
        issues.append("elsewhere")
    if c.get("quote_alt") != r.get("quote_alt"):
        issues.append("quote_alt")
    ev_c = c.get("evidence") or {}
    ev_r = r.get("evidence") or {}
    if bool(ev_c) != bool(ev_r):
        issues.append("evidence-presence")
    elif ev_c:
        if ev_c.get("file") != ev_r.get("file"):
            issues.append("ev.file")
        if ev_c.get("snippet") != ev_r.get("snippet"):
            issues.append("ev.snippet")
    return issues


def recount(cache, mode, norm, rows):
    out = {}
    for r in rows:
        k = (r["book"], r["mode_code"], r["figure_code"])
        out[k] = classify(r["book"], r.get("quote") or "", r.get("quote_hant"), cache, mode, norm)
    return out


def derive_rows(ref, norm):
    modes = json.loads(git_show(ref, MODES).decode("utf-8"))["modes"]
    bl = json.loads(git_show(ref, BOOKLIST).decode("utf-8"))
    b1 = [e["book"] for e in bl["batch1"]]
    keys = set()
    span = 0
    for b in b1:
        for m in modes:
            sc = m.get("source_chapter")
            txt = sc if isinstance(sc, str) else "\u3001".join(str(x) for x in (sc or []))
            refs = [inner.split("\u00b7")[0].strip() for inner in re.findall(r"\u300a([^\u300b]{1,60})\u300b", txt)]
            if b in refs:
                keys.add((b, m.get("mode_code"), m.get("figure_code"), m.get("key_quote_zh") or ""))
            span += sum(1 for x in refs if x == b)
    return keys, span, len(b1)


def tally(cls):
    cnt = {}
    for c in cls.values():
        cnt[c["verdict"]] = cnt.get(c["verdict"], 0) + 1
    return cnt


def alts_of(q, conv, norm):
    segs = segments(q, norm)
    out = [(q, segs, segments(conv, norm) if conv else None)]
    mm = re.match(LEAD_RE, q or "", flags=re.S)
    if mm and norm(mm.group(1)):
        q1 = mm.group(1)
        c1 = segments(conv, norm) if conv else None
        if conv:
            mm2 = re.match(LEAD_RE, conv, flags=re.S)
            if mm2 and norm(mm2.group(1)):
                c1 = segments(mm2.group(1), norm)
        out.append((q1, segments(q1, norm), c1))
    return out


def norm_map(text, strip):
    buf = []
    idx = []
    for i, ch in enumerate(text):
        if ch not in strip:
            buf.append(ch)
            idx.append(i)
    return "".join(buf), idx


def main():
    global ARGS
    ap = argparse.ArgumentParser(description="W8S2B1 \u7d20\u6750\u5305\u7aef\u4fee\u590d\u72ec\u7acb QA \u53cc\u951a\u70b9\u6821\u9a8c\u5668\uff08\u53ea\u8bfb\uff09")
    ap.add_argument("--at", default=None, help="\u951a\u70b9 ref\uff08\u9ed8\u8ba4 HEAD\uff1b\u4fee\u590d\u524d=1c00ca8a\uff09")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--scan", action="store_true", help="\u8ffd\u52a0 F2 \u5019\u9009\u5168\u626b\uff08\u8f83\u6162\uff09")
    ap.add_argument("--with-remote", action="store_true")
    ARGS = ap.parse_args()
    ref = ARGS.at or "HEAD"
    tool_b = git_show(ref, TOOL)
    if tool_b is None:
        print("FAIL  cannot read %s at %s" % (TOOL, ref))
        return 2
    tool_txt = tool_b.decode("utf-8", "replace")
    needle = "\\" + "ufe30" + "\\" + "u3000"
    is_post = needle in tool_txt
    mlab = "POST" if is_post else "PRE"
    prod_b = git_show(ref, PRODUCT)
    if prod_b is None:
        print("FAIL  cannot read %s at %s" % (PRODUCT, ref))
        return 2
    prod = json.loads(prod_b.decode("utf-8"))
    rows = prod["quotes"]
    nnew = normer(EXTRA)
    nold = normer("")
    cache_new = load_cache(ref, EXTRA)
    cache_old = load_cache(ref, "")
    check("[%s] L0 ref=%s \u5de5\u5177\u7248\u672c\u5224\u5b9a" % (mlab, ref[:8]), True,
          "post-fix tool" if is_post else "pre-fix tool")
    # global: fix state exists in history
    fb = git_show("HEAD", TOOL)
    full = git_show(FIX_REF, TOOL)
    check("[G] \u4fee\u590d\u6001\u5b58\u5728\uff1a68fd5569 \u5de5\u5177 sha16 == 450d0e752732b9a2",
          full is not None and sha16b(full) == "450d0e752732b9a2", sha16b(full or b""))
    for path, want in ((TOOL, "450d0e752732b9a2"), (PRODUCT, "17265dd82fe6665a"),
                       (PRODUCT_MD, "72b1927c17a58a9e"), (LANDING_MD, "74e443cf3f5e6614")):
        b = git_show(FIX_REF, path)
        check("[G] 68fd5569 %s sha16 == %s" % (path.split("/")[-1], want), b is not None and sha16b(b) == want,
              sha16b(b or b""))
    rb = git_show(FIX_SUPP, RECEIPT)
    check("[G] 5705b030 \u56de\u6267 sha16 == 1a62e38355ca1eb9", rb is not None and sha16b(rb) == "1a62e38355ca1eb9",
          sha16b(rb or b""))
    rb0 = git_show(FIX_REF, RECEIPT)
    check("[G] 68fd5569 \u56de\u6267\uff08\u521d\u7248\uff09 sha16 == 47029aea07d221c1",
          rb0 is not None and sha16b(rb0) == "47029aea07d221c1", sha16b(rb0 or b""))
    logp = REPO / LOG
    if logp.is_file():
        check("[G] verify.log sha256 == 35a818a9c8dfee46\u2026",
              hashlib.sha256(logp.read_bytes()).hexdigest() == "35a818a9c8dfee4605d6de6a9afc556cf3c6303fac5030b47f80d013e6f976e2",
              "local ignored file")
    # row set derivation
    keys, span, nbooks = derive_rows(ref, nnew)
    prod_keys = set((r["book"], r["mode_code"], r["figure_code"], r.get("quote") or "") for r in rows)
    check("[%s] A1 \u884c\u96c6\u72ec\u7acb\u63a8\u5bfc == \u4ea7\u7269\uff0818 \u4e66 / %d \u884c / \u8de8\u5ea6 %d\uff09" % (mlab, len(keys), span),
          keys == prod_keys and len(keys) == 154 and span == 159, "n=%d span=%d books=%d" % (len(keys), span, nbooks))
    # recount
    if is_post:
        cls = recount(cache_new, "new", nnew, rows)
        mism = [(r["mode_code"], row_issues(r, cls[(r["book"], r["mode_code"], r["figure_code"])])) for r in rows]
        mism = [m for m in mism if m[1]]
        check("A2 154 \u884c\u7b2c\u4e8c\u5b9e\u73b0\u91cd\u7b97 vs \u4ea7\u7269\u9010\u5b57\u6bb5\uff080 \u5dee\uff09", not mism, "mismatch=%d %s" % (len(mism), mism[:3]))
        check("A3 \u4ea7\u7269\u8ba1\u6570 == 57/20/3/74", prod["verdict_counts"] == V2_COUNTS, json.dumps(prod["verdict_counts"]))
        combos = (("old_old", cache_old, "old", nold), ("new_old", cache_old, "new", nold),
                  ("old_new", cache_new, "old", nnew), ("new_new", cache_new, "new", nnew))
        for name, cache, mode, norm in combos:
            cnt = tally(recount(cache, mode, norm, rows))
            check("A4 combo %s == \u56de\u6267\u5206\u89e3 %s" % (name, json.dumps(COMBO_EXPECT[name])), cnt == COMBO_EXPECT[name], json.dumps(cnt))
    else:
        cls = recount(cache_old, "old", nold, rows)
        mism = [(r["mode_code"], row_issues(r, cls[(r["book"], r["mode_code"], r["figure_code"])])) for r in rows]
        mism = [m for m in mism if m[1]]
        check("D1 154 \u884c\u65e7\u8bed\u4e49/\u65e7\u5f52\u4e00\u96c6\u91cd\u7b97 == v1 \u4ea7\u7269\uff080 \u5dee\uff09", not mism,
              "mismatch=%d %s" % (len(mism), mism[:3]))
        check("D2 v1 \u8ba1\u6570 == 55/22/3/74", prod["verdict_counts"] == V1_COUNTS, json.dumps(prod["verdict_counts"]))
        check("D3 \u5de5\u5177\u786e\u4e3a\u4fee\u590d\u524d\u7248\uff08\u65e0 FE30/U3000 \u5f52\u4e00\uff09", needle not in tool_txt)
    by = {r["mode_code"]: r for r in rows}
    pr = "A" if is_post else "D"
    if is_post:
        vmap = {mc: by[mc]["verdict"] for mc in ("M-GX-007", "M-WB-010", "M-ZDY-005", "M-ZXC-008")}
        check("A5 \u56db\u884c\u6700\u7ec8\u5206\u6863 == null/null/null/variant",
              vmap == {"M-GX-007": "null", "M-WB-010": "null", "M-ZDY-005": "null", "M-ZXC-008": "variant"}, str(vmap))
        rev = (by["M-ZXC-008"].get("evidence") or {}).get("file", "")
        check("A6 M-ZXC-008 \u89c1\u8bc1\u6307\u5411 1c09d5d360d70a3d.txt", rev.endswith("1c09d5d360d70a3d.txt"), rev)
    else:
        vmap = {mc: by[mc]["verdict"] for mc in ("M-GX-007", "M-WB-010", "M-ZDY-005", "M-ZXC-008")}
        check("D4 v1 \u56db\u884c\u5206\u6863 == variant/variant/variant/null",
              vmap == {"M-GX-007": "variant", "M-WB-010": "variant", "M-ZDY-005": "variant", "M-ZXC-008": "null"}, str(vmap))

    def hit_any(mc, mode, cache, norm):
        r = by[mc]
        book, q, conv = r["book"], r.get("quote") or "", r.get("quote_hant")
        item = cache.get(book) or {}
        RR = item.get("raw_light") or ""
        RN = item.get("raw_norm") or ""
        for qq, sgs, csgs in alts_of(q, conv, norm):
            for segs in (sgs, csgs):
                if segs and match_quote(segs, item.get("raw"), RR, RN, norm, mode):
                    return True
        return False

    def tail_fails(mc):
        r = by[mc]
        conv = r.get("quote_hant") or ""
        item = cache_new.get(r["book"]) or {}
        RR = item.get("raw_light") or ""
        RN = item.get("raw_norm") or ""
        fails = []
        sets = [("h", segments(conv, nnew) if conv else [])]
        mm = re.match(LEAD_RE, conv, flags=re.S)
        if mm and nnew(mm.group(1)):
            sets.append(("h-alt", segments(mm.group(1), nnew)))
        for tag, segs in sets:
            for i, s in enumerate(segs):
                sl = re.sub(r"\s+", "", s)
                sn = nnew(s)
                if RR.find(sl) < 0 and RN.find(sn) < 0:
                    fails.append("%s%d" % (tag, i))
        return fails

    f1_ok = True
    f1_det = []
    for mc in ("M-GX-007", "M-WB-010", "M-ZDY-005"):
        oh = hit_any(mc, "old", cache_old, nold)
        nh = hit_any(mc, "new", cache_new, nnew)
        tf = tail_fails(mc)
        ok = oh and (not nh) and bool(tf)
        f1_ok &= ok
        f1_det.append("%s old=%s new=%s tail_fails=%s" % (mc, oh, nh, ",".join(tf[:3])))
    check("[%s] F1 \u4e09\u884c\uff1a\u65e7\u8bed\u4e49\u547d\u4e2d/**\u5c3e\u6bb5\u672a\u547d\u4e2d**\uff0c\u65b0\u8bed\u4e49\u672a\u547d\u4e2d" % pr, f1_ok, " | ".join(f1_det))

    def f2_facts(mc, ch):
        r = by[mc]
        book, conv = r["book"], r.get("quote_hant") or ""
        seg = segments(conv, nnew)[0]
        j_old = (cache_old.get(book, {}).get("raw_norm") or "").find(nold(seg))
        j_new = (cache_new.get(book, {}).get("raw_norm") or "").find(nnew(seg))
        raw = cache_new.get(book, {}).get("raw") or ""
        nt, idx = norm_map(raw, set(OLD_CJK + ASCII_PUNCT + EXTRA))
        span = raw[idx[j_new]: idx[j_new + len(nnew(seg)) - 1] + 1] if j_new >= 0 else ""
        return j_old < 0, j_new >= 0, span.count(ch)

    ok = True
    det = []
    for mc, ch, nm in (("M-ZXC-008", "\ufe30", "U+FE30"), ("M-LJY-002", "\u3000", "U+3000")):
        om, nh2, cnt = f2_facts(mc, ch)
        ok &= om and nh2 and cnt >= 2
        det.append("%s old_miss=%s new_hit=%s span_%s=%d" % (mc, om, nh2, nm, cnt))
    check("[%s] F2 \u4e24\u884c\uff1a\u65e7\u5f52\u4e00\u96c6\u672a\u547d\u4e2d / \u65b0\u5f52\u4e00\u96c6\u547d\u4e2d\uff0c\u539f\u6587\u7a97\u542b\u76f8\u5e94\u5b57" % pr, ok, " | ".join(det))

    # negative controls + rederivation
    nc = prod["negative_controls"]
    bad = []
    for c in nc:
        it = cache_new.get(c["book"]) or {}
        fp = (c["perturbed"] in (it.get("raw_norm") or "")) or (c["perturbed"] in (it.get("zh_norm") or ""))
        if fp or c.get("false_positive"):
            bad.append(c["book"] + ":" + c["mode_code"])
    check("[%s] B1 \u8d1f\u5bf9\u7167 %d \u6761\u590d\u8dd1\u96f6\u5047\u9633\u6027" % (mlab, len(nc)), len(nc) == 16 and not bad, "bad=%s" % bad[:3])
    rare = "\u9f98\u9fa0\u9fa5"
    der = []
    for book in sorted(set(r["book"] for r in rows)):
        it = cache_new.get(book) or {}
        if book in CROSS_LANG or not it.get("raw"):
            continue
        usable = [r for r in rows if r["book"] == book and len(nnew(r.get("quote") or "")) >= MIN_WEAK]
        for r in usable[:2]:
            qn = nnew(r.get("quote") or "")
            mid = len(qn) // 2
            cand = None
            for chx in rare:
                cc = qn[:mid] + chx + qn[mid + 1:]
                if cc != qn and cc not in (it.get("raw_norm") or "") and cc not in (it.get("zh_norm") or ""):
                    cand = cc
                    break
            if cand is None:
                continue
            hr = cand in (it.get("raw_norm") or "")
            hz = cand in (it.get("zh_norm") or "")
            der.append({"book": book, "mode_code": r["mode_code"], "perturbed": cand, "expected": "null",
                        "hit_raw": hr, "hit_zh": hz, "false_positive": bool(hr or hz)})
    check("[%s] B2 \u8d1f\u5bf9\u7167\u91cd\u63a8\u5bfc == \u5b58\u50a8\uff08\u540c 16 \u6761\uff09" % mlab, der == nc, "derived=%d" % len(der))

    # note derivation congruence
    CROSS_NOTE = "跨语言：中文引文对非中文原文本不适用逐字对读，留语义对照档"
    NOSRC_NOTE = "否定记录：无合法全文源（版权期内），逐条结论为 null（不伪造）"
    SENT_NOTE = "节引/拼合：全部短句逐字在源（各句单独命中），整段非连续"
    HANT_NOTE = "繁简差异：引文转繁体（zh-hant）后命中原文（引文侧繁简对读）"

    def hant_path(r, cache, norm):
        book, conv = r["book"], r.get("quote_hant")
        item = cache.get(book) or {}
        RR = item.get("raw_light") or ""
        RN = item.get("raw_norm") or ""

        def all_hit(segs):
            if not segs:
                return False
            for s in segs:
                sl = re.sub(r"\s+", "", s)
                sn = norm(s)
                if RR.find(sl) < 0 and RN.find(sn) < 0:
                    return False
            return True

        main = segments(conv, norm) if conv else []
        mm = re.match(LEAD_RE, conv or "", flags=re.S)
        alt = segments(mm.group(1), norm) if (mm and norm(mm.group(1))) else []
        return all_hit(main), all_hit(alt)

    cache_k = cache_new if is_post else cache_old
    norm_k = nnew if is_post else nold
    okn, nsfx, detn, sfxbad = True, 0, [], []
    for r in rows:
        v, lv, nt = r["verdict"], r.get("match_level"), (r.get("note") or "")
        if v == "cross-lang":
            exp = CROSS_NOTE
        elif v == "null":
            exp = NOSRC_NOTE if r["book"] == "现代诗" else ""
        elif v == "quote":
            exp = ""
        elif v == "variant" and lv == "sent-composite":
            exp = SENT_NOTE
        elif v == "variant" and lv == "zh-hant":
            sfx = nt.endswith("（去冠名后）")
            exp = HANT_NOTE + ("（去冠名后）" if sfx else "")
            if sfx:
                nsfx += 1
                mp, ap = hant_path(r, cache_k, norm_k)
                if is_post and (mp or not ap):
                    sfxbad.append(r["mode_code"])
                if (not is_post) and not (mp is False):
                    sfxbad.append(r["mode_code"])
        else:
            exp = nt
        if nt != exp:
            okn = False
            detn.append("%s:%s" % (r["mode_code"], nt[:18]))
    want_sfx = 2 if is_post else 3
    check("[%s] B3 note 字段全量派生一致（含去冠名后缀 %d 行）" % (mlab, nsfx),
          okn and nsfx == want_sfx and not sfxbad, "sfx=%d want=%d bad=%d sfxbad=%s" % (nsfx, want_sfx, len(detn), sfxbad[:3]))

    # zero main-lib write
    rr = subprocess.run(["git", "-C", str(REPO), "diff", "--name-only", PRE_REF, FIX_SUPP, "--", "data/"], capture_output=True)
    names = [x for x in rr.stdout.decode().splitlines() if x.strip()]
    check("[G] \u96f6\u4e3b\u5e93\u5199\uff1a1c00ca8a..5705b030 data/ \u53ea\u6709\u56de\u6267\u4e00\u4ef6", names == [RECEIPT], str(names[:4]))
    for cref, want in ((FIX_REF, {TOOL, PRODUCT, PRODUCT_MD, LANDING_MD, RECEIPT}), (FIX_SUPP, {RECEIPT})):
        q = subprocess.run(["git", "-C", str(REPO), "show", "--name-only", "--format=", cref], capture_output=True)
        got = set(x for x in q.stdout.decode().splitlines() if x.strip())
        check("[G] %s \u63d0\u4ea4\u767d\u540d\u5355\u4e00\u81f4" % cref[:8], got == want, "%d files" % len(got))
    rec = json.loads((git_show(ref, RECEIPT) or rb).decode("utf-8"))
    mo = git_show(FIX_SUPP, MODES)
    bo_ = git_show(FIX_SUPP, BOOKLIST)
    ix = git_show(FIX_SUPP, INDEX)
    pin_ok = (rec["zero_main_write"]["modes_data_untouched"] is True and
              rec["inputs_pinned"]["modes_data_sha256"] == hashlib.sha256(mo).hexdigest() and
              rec["inputs_pinned"]["booklist_sha16"] == sha16b(bo_) and
              rec["inputs_pinned"]["cache_index_sha16"] == sha16b(ix))
    if is_post:
        check("[G] 回执声明 + 输入 pin（modes/booklist/cache）与 5705b030 实文一致",
              pin_ok and prod["modes_snapshot"]["sha256"] == hashlib.sha256(mo).hexdigest() and
              prod["booklist"]["sha256"] == hashlib.sha256(bo_).hexdigest(),
              "modes=" + sha16b(mo))
    else:
        v2b = json.loads(git_show(FIX_REF, PRODUCT).decode("utf-8"))
        check("[G] 回执声明 + 输入 pin（modes/booklist/cache）与 5705b030 实文一致", pin_ok,
              "modes=" + sha16b(mo))
        check("[D] v1 快照 pin=6f3f4580…（生成时工作区态）/ v2 刷新=提交态 736aab3b",
              prod["modes_snapshot"]["sha256"] == "6f3f4580397614f5b79aaec4c3fb9aaaaa69957e94094120d8d7446949d6415f" and
              v2b["modes_snapshot"]["sha256"] == hashlib.sha256(mo).hexdigest(),
              prod["modes_snapshot"]["sha256"][:16] + "->" + sha16b(mo))
        check("[D] modes_data @1c00ca8a == @5705b030（修复窗口输入未动）",
              hashlib.sha256(git_show(ref, MODES)).hexdigest() == hashlib.sha256(mo).hexdigest())
        modes_ref = json.loads(git_show(ref, MODES).decode("utf-8"))["modes"]
        bymc = {}
        for m in modes_ref:
            bymc.setdefault(m.get("mode_code"), m)
        qd = [r["mode_code"] for r in rows if (r.get("quote") or "") != (bymc.get(r["mode_code"], {}).get("key_quote_zh") or "")]
        check("[D] v1 154 行引文 == modes@1c00ca8a 逐条", not qd, "diffs=%d %s" % (len(qd), qd[:3]))
    check("[G] modes_data @5705b030 sha16 == 736aab3b4164973d", sha16b(mo) == "736aab3b4164973d", sha16b(mo))

    # submission (ws/pb byte-exact)
    if PB.exists():
        for path, label in ((TOOL, "tool"), (PRODUCT, "report.json"), (PRODUCT_MD, "report.md"), (LANDING_MD, "landing.md")):
            a = git_show(FIX_REF, path)
            q = subprocess.run(["git", "-C", str(PB), "show", PB_REF + ":" + path], capture_output=True)
            b = q.stdout if q.returncode == 0 else None
            check("[%s] C1 %s ws68fd5569==pb9afe48e byte-exact" % (mlab, label), a is not None and a == b,
                  sha16b(a or b"") + "/" + sha16b(b or b""))
        a = git_show(FIX_SUPP, RECEIPT)
        q = subprocess.run(["git", "-C", str(PB), "show", PB_SUPP + ":" + RECEIPT], capture_output=True)
        check("[%s] C2 \u56de\u6267\u8865\u8bb0 ws5705b030==pb5b693bb byte-exact" % mlab, a == q.stdout, sha16b(a or b""))
    else:
        check("[%s] C1\u2013C2 pb \u4ed3\u53ef\u8bfb" % mlab, False, str(PB))

    # push face (optional)
    if ARGS.with_remote:
        r = subprocess.run(["git", "-C", str(PB), "ls-remote", "origin", "main"], capture_output=True, timeout=180)
        okr = r.returncode == 0
        remote = (r.stdout.decode().split() or [""])[0]
        check("[%s] C3 push \u9762 ls-remote \u53ef\u8fbe" % mlab, okr, (remote[:8] or r.stderr.decode()[:80]))
        if okr:
            fr = subprocess.run(["git", "-C", str(PB), "fetch", "origin", "main"], capture_output=True, timeout=180)
            anc = []
            if fr.returncode == 0:
                for c in (PB_REF, PB_SUPP):
                    q2 = subprocess.run(["git", "-C", str(PB), "merge-base", "--is-ancestor", c, "FETCH_HEAD"], capture_output=True)
                    anc.append(q2.returncode == 0)
            check("[%s] C4 \u4fee\u590d\u955c\u50cf\u4e24\u7b14\u5747\u5728 origin/main \u5386\u53f2" % mlab, anc == [True, True],
                  "remote=%s anc=%s" % (remote[:8], anc))

    # F2 candidate scan (optional, slow)
    if ARGS.scan:
        import unicodedata
        rec2 = json.loads((git_show(ref, RECEIPT) or rb).decode("utf-8"))
        rec_cp = [c["cp"] for c in rec2["f2_candidate_scan"]["candidates"]]

        def is_cjkx(ch):
            o = ord(ch)
            return (0x4E00 <= o <= 0x9FFF) or (0x3400 <= o <= 0x4DBF) or (0xF900 <= o <= 0xFAFF) or (0x20000 <= o <= 0x2FA1F)

        cands = set()
        for lb, it in cache_new.items():
            for t in (it.get("raw") or "", it.get("zh") or ""):
                for ch in t:
                    if ch in cands:
                        continue
                    if unicodedata.category(ch)[0] not in "PSZ" or ch.isalnum() or is_cjkx(ch) or ch in set(OLD_CJK + ASCII_PUNCT):
                        continue
                    cands.add(ch)
        mine_cp = sorted("U+%04X" % ord(c) for c in cands)
        check("[S1] \u5019\u9009\u96c6\u72ec\u7acb\u91cd\u7b97 == \u56de\u6267 40 \u5019\u9009", mine_cp == sorted(rec_cp), "n=%d" % len(cands))

        base_t = {}
        for r in rows:
            k = (r["book"], r["mode_code"], r["figure_code"])
            cx = classify(r["book"], r.get("quote") or "", r.get("quote_hant"), cache_old, "old", nold)
            base_t[k] = (cx["verdict"], cx.get("match_level"), cx.get("match_path"))
        flips = {}
        for x in rec_cp:
            c = chr(int(x[2:], 16))
            strip = set(OLD_CJK + ASCII_PUNCT + c)
            aff = [lb for lb, it in cache_old.items() if (it.get("raw") and c in it["raw"]) or (it.get("zh") and c in it["zh"])]
            cc2 = dict(cache_old)
            for lb in aff:
                it = dict(cache_old[lb])
                for slot in ("raw", "zh"):
                    t = it.get(slot)
                    if t:
                        it[slot + "_norm"] = "".join(ch for ch in t if ch not in strip)
                cc2[lb] = it
            nc_ = normer(c)
            hits = []
            for r in rows:
                book, q, conv = r["book"], r.get("quote") or "", r.get("quote_hant")
                if book not in aff and c not in q and not (conv and c in conv):
                    continue
                k = (book, r["mode_code"], r["figure_code"])
                cx = classify(book, q, conv, cc2, "old", nc_)
                if (cx["verdict"], cx.get("match_level"), cx.get("match_path")) != base_t[k]:
                    hits.append(r["mode_code"])
            flips[x] = hits
        nz = {k: v for k, v in flips.items() if v}
        check("[S2] \u4ec5 U+FE30/U+3000 \u4ea7\u751f\u7ffb\u8f6c\uff08old matcher + old set\uff09",
              nz == {"U+FE30": ["M-ZXC-008"], "U+3000": ["M-LJY-002"]}, json.dumps(nz, ensure_ascii=False))
        base_s = {}
        for r in rows:
            k = (r["book"], r["mode_code"], r["figure_code"])
            cx = classify(r["book"], r.get("quote") or "", r.get("quote_hant"), cache_new, "new", nnew)
            base_s[k] = (cx["verdict"], cx.get("match_level"), cx.get("match_path"))
        flips2 = {}
        for x in rec_cp:
            c = chr(int(x[2:], 16))
            strip2 = set(OLD_CJK + ASCII_PUNCT + EXTRA + c)
            aff = [lb for lb, it in cache_new.items() if (it.get("raw") and c in it["raw"]) or (it.get("zh") and c in it["zh"])]
            cc3 = dict(cache_new)
            for lb in aff:
                it = dict(cache_new[lb])
                for slot in ("raw", "zh"):
                    t = it.get(slot)
                    if t:
                        it[slot + "_norm"] = "".join(ch for ch in t if ch not in strip2)
                cc3[lb] = it
            nc2 = normer(EXTRA + c)
            hits = []
            for r in rows:
                book, q, conv = r["book"], r.get("quote") or "", r.get("quote_hant")
                if book not in aff and c not in q and not (conv and c in conv):
                    continue
                k = (book, r["mode_code"], r["figure_code"])
                cx = classify(book, q, conv, cc3, "new", nc2)
                if (cx["verdict"], cx.get("match_level"), cx.get("match_path")) != base_s[k]:
                    hits.append(r["mode_code"])
            flips2[x] = hits
        nz2 = {k: v for k, v in flips2.items() if v}
        check("[S3] \u65b0\u5f52\u4e00\u96c6\u518d\u52a0\u4efb\u4e00\u5019\u9009\uff1a\u540e\u7eed\u7ffb\u8f6c 0", nz2 == {}, json.dumps(nz2, ensure_ascii=False)[:200])

    n_ok = sum(1 for _, ok in RESULTS if ok)
    if ARGS.json:
        print(json.dumps({"mode": mlab, "ref": ref, "checks": [{"name": n, "ok": o} for n, o in RESULTS],
                          "total": len(RESULTS), "pass": n_ok, "fail": len(RESULTS) - n_ok},
                         ensure_ascii=False, indent=1))
    else:
        print("----")
        print("TOTAL %d PASS / %d FAIL" % (n_ok, len(RESULTS) - n_ok))
    return 0 if n_ok == len(RESULTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
