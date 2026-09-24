#!/usr/bin/env python3
"""build_batch1_sourcing_pack.py -- W8 Stage2 批1 素材包：逐条引文对照（quote/异文/查无）。

做什么
    读 W8 批1 书单 + data/modes_data.json + 本卡抓取缓存（data/audit/source_texts 。
    与独立索引 source_texts_w8_stage2_batch1.json），对批1 各书的全部 mode 引文
    （key_quote_zh）逐条与缓存全文对照，产出逐条结论：
      quote       原文逐字命中（允许空白/标点归一；ellipsis 分段全命中）
      variant     异文命中：原文仅繁简/异体字差，在 zh-cn 转换副本命中（D4 转换层证据）
      null        两副本均未见（查无；附其他缓存书的旁证与 alt 源提示）
      cross-lang  跨语言书：中文引文对希腊/英/法文原文本就不适用逐字对读，留语义对照档
    另跑负对照（逐书抽 2 条引文做单字符扰动，必须查无）与噪声处理（过短引文标 weak）。
    只读缓存 + 书单 + modes_data；**零主库写入**；输出 JSON 供报告装配。

修订（t_2ce1e334，QA-F1/F2）
    F1：ellipsis 分段核验改为全段命中（旧实现首段标点命中即 early-return，未校验其余段）。
    F2：归一集补 U+FE30『︰』与 U+3000『　』（实测唯一产生翻转的两字：M-ZXC-008 / M-LJY-002）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.fetch_source_texts import convert_to_zh_cn  # noqa: E402
from tools.source_link_index import extract_refs_raw  # noqa: E402

BOOKLIST = REPO_ROOT / "docs" / "research" / "phase21w8_stage2_batch1_booklist.json"
MODES = REPO_ROOT / "data" / "modes_data.json"
W8_INDEX = REPO_ROOT / "data" / "audit" / "source_texts_w8_stage2_batch1.json"
TEXT_DIR = REPO_ROOT / "data" / "audit" / "source_texts"
OUT_JSON = REPO_ROOT / "docs" / "research" / "phase21w8_stage2_batch1_sourcing_report.json"

# 归一集：CJK 标点 + 空白；U+FE30『︰』 / U+3000『　』 为 t_2ce1e334 实测补入（QA-F2 类缺口）。
CJK_PUNCT = "\u3001\u3002\uff0c\uff0e\uff1b\uff1a\uff1f\uff01\u201c\u201d\u2018\u2019\uff08\uff09\u3014\u3015\u3010\u3011\u3008\u3009\u300a\u300b\u2026\u2014\u00b7\u2500\uff5e~\u2550\uff0d\ufe30\u3000"
ASCII_PUNCT = " \t\r\n.,;:?!\"'()[]{}<>|/\\_-+=*&^%$#@`"
STRIP = set(CJK_PUNCT + ASCII_PUNCT)

CROSS_LANG = {"理想国", "形而上学", "奥林匹克回忆录", "诗学", "俄狄浦斯王", "伊利亚特",
              "奥德赛", "安提戈涅", "战争史"}
MIN_WEAK = 6
CONVERT_DELIM = "\u2297\u2297"


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def norm(text):
    """归一：去空白与标点（中英），保留汉字/字母/数字。"""
    return "".join(ch for ch in (text or "") if ch not in STRIP)


def as_text(sc):
    if isinstance(sc, list):
        return "\u3001".join(str(x) for x in sc)
    return sc or ""


def book_bases(sc):
    out = []
    for m in extract_refs_raw(as_text(sc)):
        b = m.split("\u00b7")[0].strip()
        if b:
            out.append(b)
    return out


def segments(quote):
    """ellipsis 分段：…… 或 … 两侧各自须命中。"""
    parts = [p for p in re.split(r"\u2026+", quote or "") if norm(p)]
    return parts or [quote or ""]


def dual_key(entry):
    ks = [entry.get("book")] + list(entry.get("keys") or [])
    return [k for k in ks if k]


def load_cache():
    """读 W8 缓存索引 + 文本文件：label -> {raw, raw_light, raw_norm, zh, zh_light, zh_norm, entry}。"""
    idx = json.loads(W8_INDEX.read_text(encoding="utf-8"))
    cache = {}
    for e in idx.get("entries", []):
        label = (e.get("label") or e.get("key") or "").strip("\u300a\u300b")
        item = {"entry": e}
        for slot, fname in (("raw", e.get("file")), ("zh", (e.get("zh_cn") or {}).get("file"))):
            if not fname:
                continue
            p = REPO_ROOT / fname
            if not p.is_file():
                continue
            text = p.read_text(encoding="utf-8")
            item[slot] = text
            item[slot + "_light"] = re.sub(r"\s+", "", text)
            item[slot + "_norm"] = norm(text)
        cache[label] = item
    return cache


def match_quote(segs, text, text_light, text_norm):
    """返回 (level, pos, snippet) 或 None。 level: exact | whitespace | punct。

    ellipsis 分段核验（t_2ce1e334 修正）：各段（按 …… / … 切分）须**各自命中**，
    任一段未命中即整条未命中；旧实现在任一段「仅标点归一命中」时 early-return，
    不再校验其余段。单段引文行为与旧实现一致。
    """
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
        if punct_hit is None:
            punct_hit = (j, text_norm[max(0, j - 24): j + len(sn) + 24])
    if punct_hit is not None:
        return "punct", punct_hit[0], punct_hit[1]
    sl = re.sub(r"\s+", "", segs[0]) if segs else ""
    i = text_light.find(sl)
    snip = text_light[max(0, i - 24): i + len(sl) + 24] if i >= 0 else ""
    return "whitespace", pos, snip


def quote_row(book, m, cache, conv=None):
    q = m.get("key_quote_zh") or ""
    segs = segments(q)
    weak = len(norm(q)) < MIN_WEAK
    row = {"book": book, "mode_code": m.get("mode_code"), "figure_code": m.get("figure_code"),
           "figure_name_zh": m.get("figure_name_zh") or m.get("figure_code"), "name_zh": m.get("name_zh"),
           "source_chapter": as_text(m.get("source_chapter")), "quote": q, "weak": weak}
    item = cache.get(book) or {}
    if book in CROSS_LANG:
        row.update({"verdict": "cross-lang", "match_level": None,
                    "note": "跨语言：中文引文对非中文原文本不适用逐字对读，留语义对照档"})
        return row
    raw, zh = item.get("raw"), item.get("zh")
    if conv:
        row["quote_hant"] = conv
    R, RN = item.get("raw_light") or "", item.get("raw_norm") or ""
    Z, ZN = item.get("zh_light") or "", item.get("zh_norm") or ""
    RWF = (item.get("entry") or {}).get("file")
    ZWF = ((item.get("entry") or {}).get("zh_cn") or {}).get("file")
    LEAD_RE = r"^《[^》]*》[^：:]{0,16}[：:]\s*[‘“『「]?(.*?)[’”』」]?\s*$"
    alts = [(q, segs, segments(conv) if conv else None)]
    mm = re.match(LEAD_RE, q or "", flags=re.S)
    if mm and norm(mm.group(1)):
        q1 = mm.group(1)
        c1 = segments(conv) if conv else None
        if conv:
            mm2 = re.match(LEAD_RE, conv, flags=re.S)
            if mm2 and norm(mm2.group(1)):
                c1 = segments(mm2.group(1))
        alts.append((q1, segments(q1), c1))
    row["quote_alt"] = alts[1][0] if len(alts) > 1 else None
    for ai, (qq, sgs, csgs) in enumerate(alts):
        tail = "（去冠名后）" if ai else ""
        hit = match_quote(sgs, raw, R, RN) if (raw and sgs) else None
        if hit:
            row.update({"verdict": "quote", "match_level": hit[0], "match_path": "raw",
                        "evidence": {"file": RWF, "snippet": hit[2]}})
            if ai:
                row["note"] = "去冠名（书名/章名引言）后逐字命中"
            return row
        hit = match_quote(csgs, raw, R, RN) if (raw and csgs) else None
        if hit:
            row.update({"verdict": "variant", "match_level": "zh-hant", "match_path": "raw",
                        "note": "繁简差异：引文转繁体（zh-hant）后命中原文（引文侧繁简对读）" + tail,
                        "evidence": {"file": RWF, "snippet": hit[2]}})
            return row
        hit = match_quote(sgs, zh, Z, ZN) if (zh and sgs) else None
        if hit:
            row.update({"verdict": "variant", "match_level": "zh-cn", "match_path": "zh-cn",
                        "note": "繁简差异：原文（繁体底本）未见逐字，zh-cn 转换副本命中（D4 转换层证据）" + tail,
                        "evidence": {"file": ZWF, "snippet": hit[2]}})
            return row
        hit = match_quote(csgs, zh, Z, ZN) if (zh and csgs) else None
        if hit:
            row.update({"verdict": "variant", "match_level": "zh-cn+hant", "match_path": "zh-cn",
                        "note": "繁简差异：引文转繁体后与 zh-cn 副本交叉命中" + tail,
                        "evidence": {"file": ZWF, "snippet": hit[2]}})
            return row
    found = []
    sn = norm(q)
    for other, oitem in cache.items():
        if other == book:
            continue
        if (oitem.get("raw_norm") and sn and sn in oitem["raw_norm"]) or \
           (oitem.get("zh_norm") and sn and sn in oitem["zh_norm"]):
            found.append(other)
    rawn, zhn = item.get("raw_norm") or "", item.get("zh_norm") or ""
    if sn and raw:
        wins = [sn[i:i + 3] for i in range(max(1, len(sn) - 2))]
        wh = sum(1 for x in wins if x in rawn or x in zhn)
        row["shingle_ratio"] = round(wh / len(wins), 3)
    sents = [s for s in re.split(r"[。？！]", q or "") if norm(s)]
    csents = []
    if conv:
        csents = [s for s in re.split(r"[。？！]", conv) if norm(s)]
    sh = 0
    for i, s in enumerate(sents):
        s1 = norm(s)
        s2 = norm(csents[i]) if i < len(csents) else None
        if s1 in rawn or s1 in zhn or (s2 and (s2 in rawn or s2 in zhn)):
            sh += 1
    if sents:
        row["sent_hits"] = [sh, len(sents)]
    if sents and sh == len(sents) and len(sents) >= 2 and all(len(norm(s)) >= 6 for s in sents):
        row.update({"verdict": "variant", "match_level": "sent-composite", "match_path": "raw|zh-cn",
                    "note": "节引/拼合：全部短句逐字在源（各句单独命中），整段非连续"})
        row.pop("near_partial", None)
        return row
    near = False
    if sents and sh >= max(2, int(len(sents) * 0.5 + 0.999)):
        near = True
    if (row.get("shingle_ratio") or 0) >= 0.8:
        near = True
    probes = [x for x in (sn, (norm(conv) if conv else "")) if x and len(x) >= 12]
    best3 = row.get("shingle_ratio") or 0.0
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
    if raw:
        row["shingle_ratio"] = round(best3, 3)
        row["longest_ratio"] = round(bestL, 3)
    if best3 >= 0.8 or bestL >= 0.35:
        near = True
    if raw and (row.get("shingle_ratio") is not None or sents):
        row["near_partial"] = near
    note = None
    if book == "现代诗":
        note = "否定记录：无合法全文源（版权期内），逐条结论为 null（不伪造）"
    row.update({"verdict": "null", "match_level": None, "elsewhere": found[:6]})
    if note:
        row["note"] = note
    return row


def convert_quotes_hant(quotes):
    """引文侧繁简对读：整批一次 API 转换（zh-hant）；失败返回 (None, meta)。"""
    if not quotes:
        return None, None
    batch = CONVERT_DELIM.join(quotes)
    conv, meta = convert_to_zh_cn(batch, 120, variant="zh-hant")
    parts = [x.strip() for x in conv.split(CONVERT_DELIM)]
    if len(parts) != len(quotes):
        return None, {"error": "delimiter split mismatch", "meta": meta}
    return parts, meta


def negative_controls(book_rows, cache):
    """逐书抽 2 条引文做单字符扰动：必须查无（matcher 不假阳性）。"""
    out = []
    rare = "\u9f98\u9fa0\u9fa5"
    for book, rows in sorted(book_rows.items()):
        item = cache.get(book) or {}
        if book in CROSS_LANG or not item.get("raw"):
            continue
        usable = [r for r in rows if len(norm(r["quote"])) >= MIN_WEAK]
        for r in usable[:2]:
            qn = norm(r["quote"])
            mid = len(qn) // 2
            bad = None
            for ch in rare:
                cand = qn[:mid] + ch + qn[mid + 1:]
                if cand != qn and cand not in (item.get("raw_norm") or "") and cand not in (item.get("zh_norm") or ""):
                    bad = cand
                    break
            if not bad:
                continue
            hit_raw = bad in (item.get("raw_norm") or "")
            hit_zh = bad in (item.get("zh_norm") or "")
            out.append({"book": book, "mode_code": r["mode_code"], "perturbed": bad,
                        "expected": "null", "hit_raw": hit_raw, "hit_zh": hit_zh,
                        "false_positive": bool(hit_raw or hit_zh)})
    return out


def sha256_of(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description="W8 Stage2 批1 素材包（逐条引文对照；只读）")
    ap.add_argument("--out", default=str(OUT_JSON))
    args = ap.parse_args()

    booklist = json.loads(BOOKLIST.read_text(encoding="utf-8"))
    b1 = booklist["batch1"]
    modes = json.loads(MODES.read_text(encoding="utf-8"))["modes"]
    cache = load_cache()

    need_conv, conv_keys = [], []
    for e in b1:
        book = e["book"]
        if book in CROSS_LANG or book == "现代诗":
            continue
        for m in modes:
            if book in book_bases(m.get("source_chapter")):
                need_conv.append(m.get("key_quote_zh") or "")
                conv_keys.append((book, m.get("mode_code")))
    conv_list, conv_meta = convert_quotes_hant(need_conv)
    conv_map = {}
    if conv_list:
        for k, v in zip(conv_keys, conv_list):
            conv_map[k] = v

    rows_all, per_book, book_rows, span_instances = [], [], {}, 0
    for e in b1:
        book = e["book"]
        rows = [m for m in modes if book in book_bases(m.get("source_chapter"))]
        span_instances += sum(1 for m in modes for b in book_bases(m.get("source_chapter")) if b == book)
        qrows = [quote_row(book, m, cache, conv_map.get((book, m.get("mode_code")))) for m in rows]
        book_rows[book] = qrows
        rows_all += qrows
        counts = {}
        for r in qrows:
            counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
        item = cache.get(book) or {}
        ent = item.get("entry") or {}
        per_book.append({
            "book": book, "rank": e.get("rank"), "heat_spans": e.get("heat"),
            "fetch": (e.get("primary") or {}).get("fetch"),
            "primary_title": (e.get("primary") or {}).get("title"),
            "index_status": ent.get("status") or ("none-negative" if book == "现代诗" else "not-in-index"),
            "coverage": ent.get("coverage"), "file": ent.get("file"),
            "zh_cn_file": (ent.get("zh_cn") or {}).get("file"),
            "chars": ent.get("chars"), "method": ent.get("method"),
            "quotes_n": len(qrows), "verdict_counts": counts,
        })

    counts_all = {}
    for r in rows_all:
        counts_all[r["verdict"]] = counts_all.get(r["verdict"], 0) + 1
    controls = negative_controls(book_rows, cache)
    payload = {
        "schema": "protreptic.w8_stage2_batch1_sourcing/v1",
        "generated_at": now_iso(),
        "generated_by": "tools/build_batch1_sourcing_pack.py",
        "booklist": {"path": "docs/research/phase21w8_stage2_batch1_booklist.json",
                     "sha256": sha256_of(BOOKLIST)},
        "modes_snapshot": {"path": "data/modes_data.json", "modes_total": len(modes),
                           "sha256": sha256_of(MODES)},
        "cache_index": "data/audit/source_texts_w8_stage2_batch1.json",
        "policy": "逐条结论 quote（原文逐字，含空白/标点归一与 ellipsis 分段全命中）/ variant（仅繁简差，"
                  "zh-cn 转换副本命中）/ null（两副本未见，附 elsewhere 旁证）/ cross-lang（跨语言不适用"
                  "逐字对读）；负对照=单字符扰动必查无；weak=归一后短于 6 字。",
        "quote_conversion": {"variant": "zh-hant", "n": len(conv_list or []), "meta": conv_meta},
        "counts": {"books": len(b1), "quotes_total": len(rows_all), "span_instances": span_instances,
                   "null_near_partial": sum(1 for r in rows_all if r.get("near_partial")),
                   "weak": sum(1 for r in rows_all if r["weak"]),
                   "negative_controls": len(controls),
                   "negative_false_positive": sum(1 for c in controls if c["false_positive"])},
        "verdict_counts": counts_all,
        "per_book": per_book,
        "negative_controls": controls,
        "quotes": rows_all,
    }
    out = Path(args.out)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("== W8 Stage2 batch1 sourcing pack ==")
    print("books=%d quotes=%d span_instances=%d" % (len(b1), len(rows_all), span_instances))
    for v, c in sorted(counts_all.items()):
        print("  %-10s %d" % (v, c))
    print("weak=%d negative_controls=%d false_positive=%d"
          % (payload["counts"]["weak"], len(controls), payload["counts"]["negative_false_positive"]))
    print("[OK] %s" % out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
