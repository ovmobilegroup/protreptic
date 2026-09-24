#!/usr/bin/env python3
"""build_batch1_landing_ledger.py — Phase21-W8 Stage2 批1 · 处置逐条账本（卡 t_b85ae14a）。

产出 data/audit/phase21w8_stage2_batch1_landing_ledger.json。素材包（W8-2, 154 条）
逐条 → 处置类别 / 库内动作 / D4 判定 / 状态前→后 / 见证；外加书级 18 行、状态翻面、
四态前后、findings 增补、交叉自检。判定一律调用既有实现（credibility_gate.d4_scan），
本脚本不新增任何判定规则。

用法: python3 tools/build_batch1_landing_ledger.py [--write] [--backup-dir DIR]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import credibility_gate as gate  # noqa: E402  （D4 判定唯一实现）

PACK = REPO_ROOT / "docs/research/phase21w8_stage2_batch1_sourcing_report.json"
BOOKLIST = REPO_ROOT / "docs/research/phase21w8_stage2_batch1_booklist.json"
INDEX = REPO_ROOT / "data/audit/source_texts_w8_stage2_batch1.json"
LINKS = REPO_ROOT / "data/source_links.json"
SOURCES = REPO_ROOT / "data/audit/source_texts.json"
FINDINGS = REPO_ROOT / "data/audit/findings.json"
MODES = REPO_ROOT / "data/modes_data.json"
OUT = REPO_ROOT / "data/audit/phase21w8_stage2_batch1_landing_ledger.json"

# 书级备注（逐条处置的理由归并；来源 = 素材包 §七 per-book 诊断 + 本卡复核）
BOOK_NOTES = {
    "春秋繁露": "底本=繁露全文 73,419 字（coverage complete，wikitext）；查无主因：引文属《举贤良对策》（源在漢書卷056，非本底本）或改写/节引",
    "陆九渊集": "底本=象山先生全集 四部叢刊本 278,151 字（html-render 逐页）；查无主因：节引/改写（多入近似档）",
    "庄子注": "底本=荘子注 四庫全書本 render 全文 302,754 字（raw→render 已救回）；查无主因：四庫异体字/SKchar 洞 + 节引，逐字判定受字形限制",
    "老子注": "底本=道德經 王弼本 32,760 字（single-page）；查无主因：引文多出自《老子指略》《周易略例》《周易注》等王弼他著（源外），非本底本收录",
    "河南程氏遗书": "底本=二程遺書（wikisource；与《二程遗书》同源同文件 163,542 字）；查无主因：节引拼接/改写",
    "二程遗书": "与《河南程氏遗书》共用同一底本文件（wiki 重定向）；本批 3 条查无均属节引/改写",
    "文史通义": "底本=文史通义全文；4 条查无均入近似档（节引/改写），最长片段与底本可对上",
    "太极图说": "底本=太极图说全文（331 字符短篇；批1 索引标 index-page 系 MIN_CHARS 阈值误判，对照按全文做）；4 条查无均属撮述/改写",
    "现代诗": "无合法全文源（版权期内）→ 否定记录：不抓、不伪造，逐条结论 null",
}
CROSSLANG_NOTE = ("跨语言：中文引文对非中文原文（英/古希腊文/法文）不适用逐字对读；"
                  "本卡登记为待裁定并留语义对照档，不建链接、不改状态")
SOURCE_EXTERNAL = {
    "老子注": ("《老子指略》", "《周易略例》", "《周易略例·明彖》", "《周易·复卦注》", "《周易注》"),
}


def sha16(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def classify(item: dict, d4: dict | None) -> tuple[str, str]:
    """→ (处置类别, 说明)。类别字典固定，便于机读对账。"""
    kind = item.get("verdict")
    book = item.get("book")
    if kind == "quote":
        return ("核中·逐字（不改字）",
                "引文与底本逐字命中（match_level=%s，%s）；库内引文不需要改动" % (item.get("match_level"), item.get("match_path")))
    if kind == "variant":
        if item.get("match_level") == "zh-hant":
            return ("核中·繁简对读（不改字）",
                    "引文转繁后逐字命中；字面差异为繁简对读，库内引文不需要改动")
        return ("核中·节引/标点差（不改字）",
                "命中判据：%s；差异属节引/标点/撮合，逐字核验通过，库内引文不需要改动" % (item.get("match_level") or "?"))
    if kind == "cross-lang":
        return ("跨语言·语义对照（待裁定）", CROSSLANG_NOTE)
    # kind == null
    if book == "现代诗":
        return ("否定记录·无合法全文源（未抓，不伪造）", BOOK_NOTES["现代诗"])
    src = item.get("source_chapter") or ""
    q = item.get("quote") or ""
    for marker in SOURCE_EXTERNAL.get(book, ()):
        if q.startswith(marker) or marker in src:
            return ("查无·源外（王弼他著，非本底本）",
                    "引文出自%s，不在本批抓取的底本内；判定『源外』而非伪造，待后续按需另抓" % marker)
    if book == "春秋繁露" and ("举贤良对策" in src or "举贤良对策" in q):
        return ("查无·源外（对策类，源在漢書卷056）",
                "引文属《举贤良对策》一类，源在漢書卷056（非繁露底本）；待后续按需另抓，不伪造")
    if item.get("near_partial"):
        return ("查无·待核（近似档）",
                "底本内有近似段落但非逐字（shingle=%.2f / longest=%.2f / sent_hits=%s）：节引/改写/底本字形限制；按『待核』登记，不改引文"
                % (item.get("shingle_ratio", 0), item.get("longest_ratio", 0), item.get("sent_hits")))
    return ("查无·待核（无近似命中）",
            "底本内未命中逐字片段、亦无近似档（shingle=%.2f / longest=%.2f）：按『待核』登记，不改引文；书级限制见备注"
            % (item.get("shingle_ratio", 0), item.get("longest_ratio", 0)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--backup-dir", default=None)
    args = ap.parse_args()

    pack = load(PACK)
    booklist = load(BOOKLIST)
    index = load(INDEX)
    links = load(LINKS)
    sources = load(SOURCES)
    findings = load(FINDINGS)
    cur_modes = load(MODES)
    cur_status = {str(m.get("mode_code")): (m.get("verification") or {}).get("status")
                  for m in cur_modes["modes"] if isinstance(m, dict)}
    before_status = {}
    if args.backup_dir:
        bdoc = load(Path(args.backup_dir) / "data__modes_data.json")
        before_status = {str(m.get("mode_code")): (m.get("verification") or {}).get("status")
                         for m in bdoc["modes"] if isinstance(m, dict)}

    cache = gate.make_cache(REPO_ROOT)
    link_index = gate.load_link_index()
    d4_by_mode, d4_census = {}, Counter()
    mode_by_code = {str(m.get("mode_code")): m for m in cur_modes["modes"] if isinstance(m, dict)}
    for code in {str(i["mode_code"]) for i in pack["quotes"]}:
        res = gate.d4_scan(mode_by_code.get(code, {}), cache, link_index)
        d4_by_mode[code] = {"status": res["status"], "reason": res["reason"], "key": res.get("key")}
        d4_census[(res["status"], res["reason"].split(":")[0].split("(")[0].strip())] += 1

    items = []
    for n, it in enumerate(pack["quotes"], 1):
        code = str(it["mode_code"])
        cls, why = classify(it, d4_by_mode.get(code))
        row = {
            "n": n, "mode_code": code, "figure_code": it.get("figure_code"),
            "figure_name_zh": it.get("figure_name_zh"), "mode_name_zh": it.get("name_zh"),
            "book": it.get("book"), "kind": it.get("verdict"),
            "disposition": cls, "disposition_note": why,
            "library_action": "none（不改引文/不加旗标）",
            "match_level": it.get("match_level"), "near_partial": it.get("near_partial"),
            "shingle_ratio": it.get("shingle_ratio"), "longest_ratio": it.get("longest_ratio"),
            "sent_hits": it.get("sent_hits"),
            "d4": d4_by_mode.get(code),
            "status_before": before_status.get(code), "status_after": cur_status.get(code),
            "witness": it.get("evidence") or None,
            "source_chapter": it.get("source_chapter"), "quote": it.get("quote"),
        }
        items.append(row)

    # 书级行
    books = []
    cached = {e["key"]: e for e in index["entries"]}
    merged = {e["key"]: e for e in sources["entries"] if e["key"] in cached}
    for b in pack["per_book"]:
        key = b["book"]
        ce = cached.get(key) or {}
        books.append({
            "book": key, "rank": b.get("rank"), "heat_spans": b.get("heat_spans"),
            "fetch": b.get("fetch"), "primary_title": b.get("primary_title"),
            "index_status": b.get("index_status"), "coverage": b.get("coverage"),
            "chars": b.get("chars"), "method": b.get("method"), "file": b.get("file"),
            "quotes_n": b.get("quotes_n"), "verdict_counts": b.get("verdict_counts"),
            "link_in_source_links": key in links,
            "link_url": (links.get(key) or {}).get("url"),
            "cache_merged_into_source_texts": key in merged,
            "cache_sha256_matches": (merged.get(key) or {}).get("sha256") == ce.get("sha256") if ce else None,
            "note": BOOK_NOTES.get(key, ""),
        })

    # 状态翻面 / 四态
    flips = {"pending->verified": [], "pending->suspect": [], "other": []}
    for code, aft in cur_status.items():
        bef = before_status.get(code)
        if bef is None or bef == aft:
            continue
        if bef == "pending" and aft == "verified":
            flips["pending->verified"].append(code)
        elif bef == "pending" and aft == "suspect":
            flips["pending->suspect"].append(code)
        else:
            flips["other"].append("%s:%s->%s" % (code, bef, aft))
    for k in ("pending->verified", "pending->suspect"):
        flips[k] = sorted(flips[k])
    flips["other"] = sorted(flips["other"])

    fs = {}
    for tag, src_path in (("before", (Path(args.backup_dir) / "data__audit__verification_status.json") if args.backup_dir else None),
                          ("after", REPO_ROOT / "data/audit/verification_status.json")):
        if src_path is None or not Path(src_path).is_file():
            continue
        rep = load(Path(src_path))
        fs[tag] = {"counts": rep.get("counts"), "inputs": {k: v.get("sha256", "")[:16] for k, v in (rep.get("inputs") or {}).items()}}

    d4_new = [f for f in findings["findings"]
              if f.get("defect") == "D4_quote_mismatch" and str(f.get("mode_code")) in set(flips["pending->suspect"])]

    item_codes = {i["mode_code"] for i in items}
    checks = {
        "items_total": len(items),
        "items_expected": pack["counts"]["quotes_total"],
        "verdict_counts_from_items": dict(Counter(i["kind"] for i in items)),
        "verdict_counts_from_pack": pack.get("verdict_counts"),
        "disposition_counts": dict(Counter(i["disposition"] for i in items)),
        "unique_modes_in_items": len(item_codes),
        "all_flipped_codes_in_items": all(c in item_codes for c in flips["pending->verified"] + flips["pending->suspect"]),
        "side_effect_flips_outside_pack": [c for c in flips["pending->verified"] + flips["pending->suspect"] if c not in item_codes],
        "d4_census": {"%s|%s" % k: v for k, v in sorted(d4_census.items())},
        "new_d4_findings": [{"mode_code": f.get("mode_code"), "anchor": f.get("anchor"), "summary": f.get("summary")} for f in d4_new],
        "links_added": {k: v.get("url") for k, v in links.items() if k in {b["book"] for b in pack["per_book"]}},
        "cross_lang_linked": [b["book"] for b in pack["per_book"]
                              if b.get("verdict_counts", {}).get("cross-lang") and b["book"] in links],
        "cache_merged": sorted(merged),
    }
    ok = True
    if len(items) != pack["counts"]["quotes_total"]:
        print("[FAIL] 条目数 %d != 素材包 %d" % (len(items), pack["counts"]["quotes_total"]))
        ok = False
    if sorted(checks["verdict_counts_from_items"].items()) != sorted((pack.get("verdict_counts") or {}).items()):
        print("[FAIL] verdict 计数与素材包不一致: %s vs %s" % (checks["verdict_counts_from_items"], pack.get("verdict_counts")))
        ok = False
    if checks["side_effect_flips_outside_pack"]:
        print("[FAIL] 存在素材包外模式状态翻面: %s" % checks["side_effect_flips_outside_pack"])
        ok = False
    if len(d4_new) != len(flips["pending->suspect"]):
        print("[FAIL] 新增 D4 findings 数与 suspect 翻面数不一致: %d vs %d" % (len(d4_new), len(flips["pending->suspect"])))
        ok = False
    if checks["cross_lang_linked"]:
        print("[FAIL] 跨语言书被建链接（口径未裁定，不应发生）: %s" % checks["cross_lang_linked"])
        ok = False
    if len(merged) != len(cached):
        print("[FAIL] 缓存条目未全部并入 source_texts: %d/%d" % (len(merged), len(cached)))
        ok = False

    ledger = {
        "schema": "protreptic.w8_stage2_batch1.landing_ledger/v1",
        "task": "t_b85ae14a",
        "generated_at": date.today().isoformat(),
        "generated_by": "tools/build_batch1_landing_ledger.py",
        "inputs": {
            "sourcing_pack": {"path": str(PACK.relative_to(REPO_ROOT)), "sha16": sha16(PACK)},
            "booklist": {"path": str(BOOKLIST.relative_to(REPO_ROOT)), "sha16": sha16(BOOKLIST)},
            "batch1_cache_index": {"path": str(INDEX.relative_to(REPO_ROOT)), "sha16": sha16(INDEX)},
            "source_links": {"path": str(LINKS.relative_to(REPO_ROOT)), "sha16": sha16(LINKS)},
            "source_texts": {"path": str(SOURCES.relative_to(REPO_ROOT)), "sha16": sha16(SOURCES)},
            "findings": {"path": str(FINDINGS.relative_to(REPO_ROOT)), "sha16": sha16(FINDINGS)},
            "modes_data": {"path": str(MODES.relative_to(REPO_ROOT)), "sha16": sha16(MODES)},
        },
        "policy": ("批1 处置=①已核条目『不改字』入库（核验结论入账本+见证位）；②查无/源外/否定/跨语言"
                   "逐条登记不改引文；③真差异按既有 D4 流程登记（3 条）；④不新增判定规则、不动他卡条目"
                   "（20 条他卡印记已回填保护）。"),
        "dispositions_summary": dict(Counter(i["disposition"] for i in items)),
        "status_flips": flips,
        "four_state": fs,
        "books": books,
        "items": items,
        "cross_checks": checks,
        "verdict": "PASS" if ok else "FAIL",
    }
    text = json.dumps(ledger, ensure_ascii=False, indent=2) + "\n"
    print("[ledger] 条目 %d；处分类别: %s" % (len(items), json.dumps(ledger["dispositions_summary"], ensure_ascii=False)))
    print("[ledger] 翻面: pending->verified=%d pending->suspect=%d other=%d；D4 新增 findings=%d"
          % (len(flips["pending->verified"]), len(flips["pending->suspect"]), len(flips["other"]), len(d4_new)))
    print("[ledger] 包外翻面=%s；跨语言链接=%s；缓存并入=%d/%d"
          % (checks["side_effect_flips_outside_pack"], checks["cross_lang_linked"], len(merged), len(cached)))
    print("[ledger] verdict=%s" % ledger["verdict"])
    if args.write:
        if not ok:
            print("[FAIL] 自检未过，拒绝写盘")
            return 1
        OUT.write_text(text, encoding="utf-8")
        print("[OK] 已写 %s (%d bytes, sha16=%s)" % (OUT, len(text.encode('utf-8')), sha16(OUT)))
    else:
        print("[dry-run] 未写盘")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
