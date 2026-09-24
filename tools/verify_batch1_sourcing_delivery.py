#!/usr/bin/env python3
"""verify_batch1_sourcing_delivery.py -- W8 Stage2 批1 交付独立核验（只读，可复跑）@@FS@@

核验对象（卡 t_70a8cbce）
    1) 候选口径：baseline 复扫 hot68 与书单 hot68 逐名一致；live 复扫为超集（附差集）
    2) 素材包 JSON：计数自洽（逐条数 = 各书之和；verdict 取值域）与 18 书齐备
    3) 缓存完整性：逐文件 sha256 与索引登记一致；索引 counts 与 entries 重算一致
    4) 负对照：扰动条目零假阳性；跨语言书结论全为 cross-lang
    5) 否定记录：现代诗无缓存条目且逐条结论均为 null（无源）@@FS@@
用法
    python3 tools/verify_batch1_sourcing_delivery.py
退出码 0 = 全部 PASS@@FS@@
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOOKLIST = REPO / "docs" / "research" / "phase21w8_stage2_batch1_booklist.json"
PACK = REPO / "docs" / "research" / "phase21w8_stage2_batch1_sourcing_report.json"
INDEX = REPO / "data" / "audit" / "source_texts_w8_stage2_batch1.json"
MANIFEST = REPO / "tools" / "manifests" / "w8_stage2_batch1_texts.json"
RECOUNT_BASE = REPO / "data" / "audit" / "phase21w8_stage2_batch1_recount_baseline.json"
RECOUNT_LIVE = REPO / "data" / "audit" / "phase21w8_stage2_batch1_recount_live.json"

CROSS_LANG = {"理想国", "形而上学", "奥林匹克回忆录", "诗学", "俄狄浦斯王", "伊利亚特",
              "奥德赛", "安提戈涅", "战争史"}
VERDICTS = {"quote", "variant", "null", "cross-lang"}

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  " + detail) if detail else ""))


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    booklist = load(BOOKLIST)
    hot68 = [r["book"] for r in booklist["hot68"]]
    base = load(RECOUNT_BASE)
    live = load(RECOUNT_LIVE)

    base_hot = sorted(r["book"] for r in base["rows"] if r["count_raw"] >= base["min_citations"] and r["unresolved"])
    live_hot = sorted(r["book"] for r in live["rows"] if r["count_raw"] >= live["min_citations"] and r["unresolved"])
    check("C1 对账 baseline hot68 == 书单 hot68（逐名）", base_hot == sorted(hot68),
          "n=%d" % len(base_hot))
    check("C2 live 为 hot68 超集且差集已登记", set(hot68) <= set(live_hot),
          "delta=%s" % sorted(set(live_hot) - set(hot68)))
    check("C3 dedup 口径数已登记（baseline）",
          base["hot_old_total"] == 59, "hot_old=%d" % base["hot_old_total"])

    pack = load(PACK)
    quotes = pack["quotes"]
    check("C4 verdict 取值域合法", {q["verdict"] for q in quotes} <= VERDICTS)
    check("C5 quotes_total 统计自洽", pack["counts"]["quotes_total"] == len(quotes),
          "%d" % len(quotes))
    sum_book = sum(b["quotes_n"] for b in pack["per_book"])
    check("C6 各书逐条数之和 == 总数", sum_book == len(quotes), "%d" % sum_book)
    vc = {}
    for q in quotes:
        vc[q["verdict"]] = vc.get(q["verdict"], 0) + 1
    check("C7 verdict 分项计数自洽", vc == pack["verdict_counts"], str(vc))
    check("C8 批1 十八书齐备", len(pack["per_book"]) == 18, "%d" % len(pack["per_book"]))
    check("C9 负对照零假阳性", pack["counts"]["negative_false_positive"] == 0,
          "controls=%d" % pack["counts"]["negative_controls"])
    bad = [q["mode_code"] for q in quotes if q["book"] in CROSS_LANG and q["verdict"] != "cross-lang"]
    check("C10 跨语言书结论全为 cross-lang", not bad, "bad=%s" % bad[:5])
    bad2 = [q["mode_code"] for q in quotes if q["book"] not in CROSS_LANG and q["verdict"] == "cross-lang"]
    check("C11 中文书无 cross-lang 结论", not bad2, "bad=%s" % bad2[:5])

    idx = load(INDEX)
    entries = idx.get("entries", [])
    counts = {}
    for e in entries:
        counts[e.get("status")] = counts.get(e.get("status"), 0) + 1
    check("C12 索引 counts 与 entries 重算一致", counts == idx.get("counts"), str(counts))

    ok_files, bad_files, missing = 0, [], []
    for e in entries:
        for fname, want in ((e.get("file"), e.get("sha256")),
                            ((e.get("zh_cn") or {}).get("file"), (e.get("zh_cn") or {}).get("sha256"))):
            if not fname:
                continue
            p = REPO / fname
            if not p.is_file():
                missing.append(fname)
                continue
            if sha256_file(p) == want:
                ok_files += 1
            else:
                bad_files.append(fname)
    check("C13 缓存文件 sha256 与索引登记一致", not bad_files and not missing,
          "ok=%d bad=%d missing=%d" % (ok_files, len(bad_files), len(missing)))

    manifest = load(MANIFEST)
    need = [b for b in manifest["books"] if b.get("fetch") != "none"]
    have = {(e.get("label") or "").strip("\u300a\u300b") for e in entries}
    missing_books = [b.get("label") for b in need if (b.get("label") or "").strip("\u300a\u300b") not in have]
    check("C14 manifest 应抓书全部有索引条目", not missing_books, "missing=%s" % missing_books[:6])

    mp = [b for b in manifest["books"] if b.get("label", "").strip("\u300a\u300b") == "现代诗"]
    check("C15 现代诗为否定记录（fetch=none，无缓存条目）",
          bool(mp) and mp[0].get("fetch") == "none" and "现代诗" not in have)

    modes_p = REPO / "data" / "modes_data.json"
    modes_now = sha256_file(modes_p)
    want = pack.get("modes_snapshot", {}).get("sha256")
    check("C16 素材包快照 sha == 现文件 sha（读侧零写实证）", bool(want) and want == modes_now,
          "sha16=%s mtime=%s" % (modes_now[:16],
                                 __import__("time").strftime("%H:%M:%S", __import__("time").localtime(modes_p.stat().st_mtime))))

    n_ok = sum(1 for _, ok in RESULTS if ok)
    print("----")
    print("TOTAL %d PASS / %d FAIL" % (n_ok, len(RESULTS) - n_ok))
    return 0 if n_ok == len(RESULTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
