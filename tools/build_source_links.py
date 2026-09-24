#!/usr/bin/env python3
"""构建 `data/source_links.json`（**按书名/事件名索引**）——Phase38-Y1。

做什么
    1. 从 `data/modes_data.json` 统计被引书名（《…》内文）：扫**全部原始跨度**（不做
       条目内去重）并按中点「·」首段**归并为书级**，把**书级被引 >=3 次**的书名
       作为扩面候选（口径修复见 count_citations；卡 t_70a8cbce）；另外把**现索引里
       每一条 key 的书级名**也纳入候选（给旧 key 一次换成「正文可回读」源的机会）。
    2. 逐名到权威源解析，解析结果**逐条 curl 实测**：HTTP 200 且页面内容含源站标题才算数：
         * 中文公版书 -> zh.wikisource（MediaWiki API，canonical title 精确匹配 + 消歧义剔除）
         * 西文公版书 -> gutendex(Project Gutenberg) / Internet Archive
         * 著作条目   -> zh/en Wikipedia + **Wikidata P31 校验**（条目的实例类型必须是
                         「书/著作/文学作品」，否则不算命中，避免把书名挂到无关条目）
         * 事件·档案 -> zh/en Wikipedia（非消歧义即可）
    3. 解析不到的登记为 `unverifiable` + 理由，**绝不塞假 URL**。
    4. 写出索引 + 机读覆盖报告；可重复跑（幂等）。

为何优先 zh.wikisource 而非 ctext
    实测（Phase38-Y1）：`ctext.org` 章节深链在本环境**只返回 Cloudflare 挑战页**
    （HTTP 200，正文是 "Checking the security of your connection..."，浏览器同结果），
    正文无法回读。故只在**没有其它可回读源**时保留 ctext 存量链，并加 `note` 标注。

用法
    python3 tools/build_source_links.py --dry-run --review   # 只解析+核验+打印，不写文件
    python3 tools/build_source_links.py                      # 写索引 + 覆盖报告
    python3 tools/build_source_links.py --bookcount-report --bookcount-json /tmp/bookcount.json
        # 只看候选口径对账（不联网、不写盘；见 count_citations / bookcount_report）
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MODES_PATH = REPO_ROOT / "data" / "modes_data.json"
LINKS_PATH = REPO_ROOT / "data" / "source_links.json"
REPORT_PATH = REPO_ROOT / "data" / "audit" / "source_link_coverage.json"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
TODAY = date.today().isoformat()
CTEXT_NOTE = "ctext 章节深链：本环境 curl 得 200，但正文为 Cloudflare 挑战页，正文未回读"

sys.path.insert(0, str(REPO_ROOT))
from tools.source_link_index import extract_refs, extract_refs_raw  # noqa: E402

EVENT_MARKERS = ("事变", "之乱", "之变", "改革", "条约", "战争", "会议", "运动",
                 "起义", "废太子", "革命", "协定", "宣言", "法典", "考试", "事件")
GENERIC = {"自传", "历史", "南极", "巴黎评论", "评注", "通论", "音注", "书信",
           "词论", "秘史", "战史", "探路", "历史"}
# Wikipedia 条目必须是「著作」类（Wikidata P31），否则不认
BOOK_CLASSES = {
    "Q571",        # book
    "Q47461344",   # written work
    "Q7725634",    # literary work
    "Q8261",       # novel
    "Q25379",      # play
    "Q13136",      # reference work
    "Q3331189",    # version, edition or translation
    "Q732577",     # publication
    "Q17537576",   # creative work
    "Q11424",      # film (screenplay citations)
    "Q2352616",    # classical text? (unused fallback)
}
SPECIAL_REASONS = {
    "苏咸子": "D2 伪造出处：《苏咸子》不存在于任何权威目录（与 data/audit/findings.json 一致）",
    "卓特思维模式考辨": "自指书名，非公开出版物，无可核验源",
}


# 人工复核确认的「同标题≠同著作」命中：跳过该源（附理由，可复核）
REJECT_HITS = {
    "野鸭": "zh.wikisource 同标题页实为唐·李群玉《野鴨》诗（分类：李群玉/唐诗/五言絕句），非易卜生同名剧作",
    "忏悔录": "zh.wikisource 同标题页实为黄远生 1915 年散文《懺悔錄》（分类：黃遠生/1915年），非奥古斯丁《忏悔录》",
}
DISAMBIG_MARKS = ("消歧義", "消歧义", "disambiguation", "消歧义页")


def is_disambig_title(title: str) -> bool:
    t = (title or "").lower()
    return any(m.lower() in t for m in DISAMBIG_MARKS)


def curl(url: str, timeout: int = 25) -> str:
    try:
        r = subprocess.run(["curl", "-s", "-L", "--max-time", str(timeout), "-A", UA, url],
                           capture_output=True, text=True, timeout=timeout + 5)
        return r.stdout or ""
    except Exception:
        return ""


def curl_status(url: str, timeout: int = 20) -> int:
    if not url:
        return 0
    for _ in range(2):
        try:
            r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                                "-L", "--max-time", str(timeout), "-A", UA, url],
                               capture_output=True, text=True, timeout=timeout + 5)
            raw = (r.stdout or "").strip()
            code = int(raw) if raw.isdigit() else 0
            if code:
                return code
        except Exception:
            pass
        time.sleep(1.5)
    return 0


def api_json(url: str, attempts: int = 4):
    for k in range(attempts):
        raw = curl(url)
        if raw.strip().startswith("{") or raw.strip().startswith("["):
            try:
                return json.loads(raw)
            except Exception:
                pass
        time.sleep(1.5 + 2 * k)
    return None


# ---------------------------------------------------------------- MediaWiki helpers
def mw_chain(name, q):
    conv = {e["from"]: e["to"] for e in q.get("converted", [])}
    red = {e["from"]: e["to"] for e in q.get("redirects", [])}
    norm = {e["from"]: e["to"] for e in q.get("normalized", [])}
    t = name
    for _ in range(3):
        t = norm.get(t, t)
        t = conv.get(t, t)
        t = red.get(t, t)
    return t


def wikisource_resolve(names, lang="zh", batch_size=25, sleep=1.2):
    """批量：canonical title 精确命中 + 剔除消歧义页。"""
    out = {}
    for i in range(0, len(names), batch_size):
        batch = names[i:i + batch_size]
        url = ("https://%s.wikisource.org/w/api.php?action=query&format=json"
               "&redirects=1&converttitles=1&prop=info|pageprops&titles=%s"
               % (lang, urllib.parse.quote("|".join(batch))))
        j = api_json(url)
        if not j:
            for n in batch:
                out[n] = {"error": "api-failed"}
            continue
        q = j.get("query", {})
        pages = {pg.get("title"): pg for pg in q.get("pages", {}).values()}
        for n in batch:
            t = mw_chain(n, q)
            pg = pages.get(t)
            if not pg or int(pg.get("pageid", 0)) <= 0:
                out[n] = None
                continue
            pp = pg.get("pageprops", {}) or {}
            if "disambiguation" in pp or is_disambig_title(pg["title"]):
                out[n] = {"error": "disambiguation"}
                continue
            out[n] = {"title": pg["title"], "length": pg.get("length", 0),
                      "wikibase_item": pp.get("wikibase_item")}
        time.sleep(sleep)
    return out


def wikipedia_batch(names, lang="zh", batch_size=25, sleep=1.2):
    """批量：条目存在（非消歧义）+ pageprops.wikibase_item。"""
    out = {}
    names = list(names)
    for i in range(0, len(names), batch_size):
        batch = names[i:i + batch_size]
        url = ("https://%s.wikipedia.org/w/api.php?action=query&format=json"
               "&redirects=1&converttitles=1&prop=info|pageprops&titles=%s"
               % (lang, urllib.parse.quote("|".join(batch))))
        j = api_json(url)
        if not j:
            for n in batch:
                out[n] = None
            continue
        q = j.get("query", {})
        pages = {pg.get("title"): pg for pg in q.get("pages", {}).values()}
        for n in batch:
            t = mw_chain(n, q)
            pg = pages.get(t)
            if not pg or int(pg.get("pageid", 0)) <= 0:
                out[n] = None
                continue
            pp = pg.get("pageprops", {}) or {}
            if "disambiguation" in pp or is_disambig_title(pg["title"]):
                out[n] = None
                continue
            out[n] = {"title": pg["title"], "length": pg.get("length", 0),
                      "wikibase_item": pp.get("wikibase_item"), "lang": lang}
        time.sleep(sleep)
    return out


def wikidata_p31_batch(qids, batch_size=40, sleep=0.8):
    """批量查 P31：{qid: [class ids]}。"""
    out = {}
    qids = [q for q in dict.fromkeys(qids) if q]
    for i in range(0, len(qids), batch_size):
        batch = qids[i:i + batch_size]
        j = api_json("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json"
                     "&props=claims&ids=%s" % "|".join(batch), attempts=3)
        ent = (j or {}).get("entities", {})
        for qid in batch:
            claims = (ent.get(qid) or {}).get("claims", {})
            ids = []
            for st in claims.get("P31", []):
                try:
                    ids.append(st["mainsnak"]["datavalue"]["value"]["id"])
                except Exception:
                    pass
            out[qid] = ids
        time.sleep(sleep)
    return out


# ---------------------------------------------------------------- other providers
def gutendex_search(name: str, limit: int = 5):
    j = api_json("https://gutendex.com/books?search=" + urllib.parse.quote(name), attempts=2)
    if not j:
        return []
    return [{"id": b.get("id"), "title": b.get("title", "")} for b in j.get("results", [])[:limit]]


def archive_search(name: str, limit: int = 5):
    q = urllib.parse.quote('title:("%s")' % name)
    j = api_json("https://archive.org/advancedsearch.php?q=%s&fl%%5B%%5D=identifier"
                 "&fl%%5B%%5D=title&rows=%d&output=json" % (q, limit), attempts=2)
    if not j:
        return []
    return [{"identifier": d.get("identifier"), "title": d.get("title", "")}
            for d in j.get("response", {}).get("docs", [])]


def ws_url(title, lang="zh"):
    return "https://%s.wikisource.org/wiki/%s" % (lang, urllib.parse.quote(title.replace(" ", "_")))


def wp_url(title, lang="zh"):
    return "https://%s.wikipedia.org/wiki/%s" % (lang, urllib.parse.quote(title.replace(" ", "_")))


def verify(url, needle):
    """200 + 正文含 needle 才算通过。"""
    status = curl_status(url)
    if status != 200:
        return {"ok": False, "status": status, "reason": "http-%s" % status}
    if needle and needle not in curl(url, timeout=30):
        return {"ok": False, "status": status, "reason": "content-mismatch"}
    return {"ok": True, "status": status}


# ---------------------------------------------------------------- main
def bookcount_report(modes, index, args):
    """候选口径对账（卡 t_70a8cbce）：新口径（书级归并 raw 跨度）对旧口径（条目内去重）。

    只算计数、不联网、不写主索引；两个口径各列出「>=min 且未解析」的书单与差集，
    逐书计数行随 --bookcount-json 落盘。供 W8 Stage2 批1 工具卡对账使用。
    """
    from tools.source_link_index import candidate_keys

    def base_of(name):
        return name.split("\u00b7")[0].strip()

    span_counts, counts = count_citations(modes)
    dedup_books = {}
    for m in modes:
        for name in extract_refs(m.get("source_chapter")):
            name = (name or "").strip()
            if not name:
                continue
            b = base_of(name)
            if b:
                dedup_books[b] = dedup_books.get(b, 0) + 1

    def unresolved(name):
        return not any(k in index for k in candidate_keys(name))

    rows = []
    for name, c in counts.items():
        spans = {k: v for k, v in sorted(span_counts.items()) if base_of(k) == name}
        rows.append({"book": name, "count_raw": c, "count_dedup": dedup_books.get(name, 0),
                     "unresolved": unresolved(name), "spans": spans})
    rows.sort(key=lambda r: (-r["count_raw"], r["book"]))
    hot_new = [r for r in rows if r["count_raw"] >= args.min_citations and r["unresolved"]]
    hot_old = [r for r in rows if r["count_dedup"] >= args.min_citations and r["unresolved"]]
    new_only = sorted({r["book"] for r in hot_new} - {r["book"] for r in hot_old})
    old_only = sorted({r["book"] for r in hot_old} - {r["book"] for r in hot_new})
    print("== 候选口径对账（书级归并 raw 跨度 vs 条目内去重）==")
    print("modes=%d；跨度名 %d；书级名 %d；min_citations=%d"
          % (len(modes), len(span_counts), len(counts), args.min_citations))
    print("新口径（>=min 未解析）：%d 本；旧口径：%d 本" % (len(hot_new), len(hot_old)))
    print("新有旧无（旧口径漏收）：%d 本 %s" % (len(new_only), new_only[:20]))
    print("旧有新无：%d 本 %s" % (len(old_only), old_only[:20]))
    for r in hot_new[:15]:
        print("  %3d  %s  (dedup %d)" % (r["count_raw"], r["book"], r["count_dedup"]))
    if args.bookcount_json:
        payload = {
            "schema": "protreptic.book_count_scope_report/v1",
            "generated_at": TODAY,
            "generated_by": "tools/build_source_links.py --bookcount-report",
            "modes_total": len(modes),
            "modes_source": args.modes_spec or "worktree:data/modes_data.json",
            "min_citations": args.min_citations,
            "scope_new": "raw spans, no per-mode dedupe, merged at book level (first segment before U+00B7)",
            "scope_old": "extract_refs per-mode dedupe, merged at book level",
            "span_names_total": len(span_counts),
            "book_names_total": len(counts),
            "hot_new_total": len(hot_new),
            "hot_old_total": len(hot_old),
            "new_only": new_only,
            "old_only": old_only,
            "rows": rows,
        }
        with open(args.bookcount_json, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("[OK] 写出 %s" % args.bookcount_json)
    return 0


def count_citations(modes):
    """候选计数（书级归并口径；卡 t_70a8cbce 修复）。

    旧口径（根因）：每条目内去重后的「跨度名」计数，不按中点「·」归并书级 ——
    书级被引 >= min 而篇章跨度各自 < min 的书（如《论衡》）从未成为候选、从未探源；
    解析侧本支持章节到书级回落，不对称只在候选生成侧（pilot 报告 §2.1 根因条）。
    新口径（与 pilot 复扫一致）：
      1) 扫全部书名号原始跨度（不做条目内去重，同一 mode 内重复出现都计数）；
      2) 按中点 U+00B7 首段归并为书级名；
      3) 书级计数 >= min_citations 即入候选。
    返回 (span_counts, book_counts)。
    """
    span_counts, book_counts = {}, {}
    for m in modes:
        for name in extract_refs_raw(m.get("source_chapter")):
            name = (name or "").strip()
            if not name:
                continue
            span_counts[name] = span_counts.get(name, 0) + 1
            base = name.split("\u00b7")[0].strip()
            if base:
                book_counts[base] = book_counts.get(base, 0) + 1
    return span_counts, book_counts


def main() -> int:
    ap = argparse.ArgumentParser(description="构建按书名索引的 source_links.json")
    ap.add_argument("--modes-path", default=str(MODES_PATH))
    ap.add_argument("--links-path", default=str(LINKS_PATH))
    ap.add_argument("--report-path", default=str(REPORT_PATH))
    ap.add_argument("--min-citations", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--review", action="store_true")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--bookcount-report", action="store_true",
                    help="候选口径对账：书级归并口径重扫计数（不联网、不写主索引）")
    ap.add_argument("--bookcount-json", default=None,
                    help="--bookcount-report 的逐书计数 JSON 输出路径")
    ap.add_argument("--modes-spec", default=None,
                    help="git 版本态 modes：<rev>:data/modes_data.json（复扫对账用；默认读工作区）")
    args = ap.parse_args()

    if args.modes_spec:
        _rc = subprocess.run(["git", "-C", str(REPO_ROOT), "show", args.modes_spec],
                             capture_output=True, check=True)
        modes = json.loads(_rc.stdout.decode("utf-8"))["modes"]
    else:
        with open(args.modes_path, encoding="utf-8") as f:
            modes = json.load(f)["modes"]
    with open(args.links_path, encoding="utf-8") as f:
        index = json.load(f)
    if not isinstance(index, dict):
        raise SystemExit("source_links.json 不是 dict（旧裸列表 schema），先修 schema 再扩面")

    if args.bookcount_report:
        return bookcount_report(modes, index, args)

    span_counts, counts = count_citations(modes)

    def count_of(name):
        return counts.get(name) or span_counts.get(name) or 0

    candidates = sorted([n for n, c in counts.items() if c >= args.min_citations],
                        key=lambda n: (-counts[n], n))
    print("被引书级名 %d 种（跨度名 %d 种）；书级被引 >=%d 次者 %d 种"
          % (len(counts), len(span_counts), args.min_citations, len(candidates)))

    # A. 现有索引：逐条实测，200 的保留
    kept, stale = {}, []
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        st = list(ex.map(lambda kv: (kv[0], curl_status((kv[1].get("url") or "").strip())),
                         list(index.items())))
    stale_urls = {}
    for key, code in st:
        info = index[key]
        if code == 200:
            kept[key] = dict(info)
        else:
            stale.append(key)
            stale_urls[key] = {"url": (info.get("url") or "").strip(), "status": code}
    print("现索引 %d 条：实测 200 保留 %d；异常 %d %s"
          % (len(index), len(kept), len(stale),
             json.dumps({k: v["status"] for k, v in stale_urls.items()}, ensure_ascii=False)))

    # B. 候选名：被引 >=3 的 + 现索引 key 的书级名（含异常项）
    cand, seen = [], set()

    def push(n):
        n = (n or "").strip()
        if n and n not in seen:
            seen.add(n)
            cand.append(n)

    for n in candidates:
        push(n)
    for key in {"《%s》" % n for n in candidates} | set(index.keys()):
        if key.startswith("《") and key.endswith("》"):
            inner = key[1:-1]
            push(inner)
            if "·" in inner:
                push(inner.split("·")[0])
    print("待解析名 %d 个" % len(cand))

    resolved = {}
    pending = []
    for n in cand:
        if n in GENERIC or len(n) <= 1:
            resolved[n] = {"status": "unverifiable", "reason": "泛指表述，无唯一书名可指"}
        elif n.split("·")[0] in SPECIAL_REASONS:
            resolved[n] = {"status": "unverifiable",
                           "reason": SPECIAL_REASONS[n.split("·")[0]]}
        else:
            pending.append(n)

    # C1/C2 zh.wikisource：全名 + 书级名
    full = wikisource_resolve(pending)
    bases = []
    for n in pending:
        if "·" in n:
            b = n.split("·")[0]
            if b not in bases:
                bases.append(b)
    base_res = wikisource_resolve([b for b in bases if not full.get(b)])
    print("zh.wikisource：全名命中 %d/%d；书级名命中 %d/%d"
          % (sum(1 for v in full.values() if v and not v.get("error")), len(pending),
             sum(1 for v in base_res.values() if v and not v.get("error")),
             len([b for b in bases if not full.get(b)])))

    for n in pending:
        hit, key_name = None, n
        v = full.get(n)
        if v and not v.get("error"):
            hit = v
        elif "·" in n:
            b = n.split("·")[0]
            v = full.get(b) if (full.get(b) and not full.get(b).get("error")) else base_res.get(b)
            if v and not v.get("error"):
                hit, key_name = v, b
        if hit and n in REJECT_HITS:
            resolved[n] = {"status": "unverifiable", "reason": REJECT_HITS[n]}
            hit = None
        if hit:
            resolved[n] = {
                "status": "resolved", "key_name": key_name,
                "url": ws_url(hit["title"]), "source_type": "wikisource",
                "confidence": 0.9 if key_name == n else 0.8,
                "canonical_title": hit["title"], "provider": "zh.wikisource",
                "page_length": hit.get("length", 0), "wikibase_item": hit.get("wikibase_item"),
            }
        else:
            resolved[n] = None

    # C3 西文：Gutenberg / Internet Archive（仅纯 ASCII 名）
    ascii_names = [n for n in pending if resolved.get(n) is None
                   and all(ord(c) < 128 for c in n)]

    def guten(name):
        for b in gutendex_search(name, 3):
            if name.lower() in (b["title"] or "").lower():
                return {"url": "https://www.gutenberg.org/ebooks/%s" % b["id"],
                        "source_type": "gutenberg", "confidence": 0.85,
                        "canonical_title": b["title"], "provider": "Project Gutenberg"}
        return None

    def archive(name):
        for d in archive_search(name, 3):
            if name.lower() in (d["title"] or "").lower():
                return {"url": "https://archive.org/details/%s" % d["identifier"],
                        "source_type": "archive", "confidence": 0.7,
                        "canonical_title": d["title"], "provider": "Internet Archive"}
        return None

    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        gres = dict(ex.map(lambda n: (n, guten(n)), ascii_names))
        ares = dict(ex.map(lambda n: (n, archive(n)), ascii_names))
    for n, r in list(gres.items()) + list(ares.items()):
        if r and resolved.get(n) is None:
            r = dict(r)
            r.update({"status": "resolved", "key_name": n})
            resolved[n] = r

    # C4 著作条目：Wikipedia(+Wikidata P31) 批量；C5 事件条目
    todo = [n for n in pending if resolved.get(n) is None]
    base_todo = [n.split("·")[0] for n in todo if "·" in n]
    arts = {}
    zh = wikipedia_batch(todo + base_todo, "zh")
    for n, v in zh.items():
        arts[n] = v
    rest = [n for n in todo if not arts.get(n)]
    en = wikipedia_batch(rest, "en")
    for n, v in en.items():
        if v:
            arts[n] = v
    p31 = wikidata_p31_batch([a["wikibase_item"] for a in arts.values() if a and a.get("wikibase_item")])

    def pick(n):
        """全名优先，其次书级名；返回 (key_name, art)。"""
        if arts.get(n):
            return n, arts[n]
        if "·" in n and arts.get(n.split("·")[0]):
            return n.split("·")[0], arts[n.split("·")[0]]
        return None, None

    for n in todo:
        key_name, art = pick(n)
        if not art:
            continue
        qid = art.get("wikibase_item")
        classes = p31.get(qid) or []
        if qid and (set(classes) & BOOK_CLASSES):
            resolved[n] = {"status": "resolved", "key_name": key_name,
                           "url": wp_url(art["title"], art["lang"]),
                           "source_type": "wikipedia", "confidence": 0.6,
                           "canonical_title": art["title"],
                           "provider": "%s.wikipedia (wikidata P31)" % art["lang"],
                           "note": "条目级（书目级）链接：该条目在 Wikidata 上被认定为著作/作品"}
    ev = [n for n in todo if resolved.get(n) is None and any(k in n for k in EVENT_MARKERS)]
    for n in ev:
        art = arts.get(n) or (arts.get(n.split("·")[0]) if "·" in n else None)
        if art:
            resolved[n] = {"status": "resolved", "key_name": n,
                           "url": wp_url(art["title"], art["lang"]),
                           "source_type": "wikipedia", "confidence": 0.6,
                           "canonical_title": art["title"],
                           "provider": "%s.wikipedia" % art["lang"],
                           "note": "事件/档案条目链接"}
    print("Wikipedia 批量查询 %d 名（zh 命中 %d）" % (len(todo), sum(1 for v in zh.values() if v)))

    # D. 逐条实测（200 + 正文含标题）
    def check(item):
        n, r = item
        if not r or r.get("status") != "resolved":
            return n, r
        v = verify(r["url"], r.get("canonical_title") or n)
        if v["ok"]:
            r = dict(r)
            r["verified"] = {"status": 200, "checked_at": TODAY, "method": "curl+content"}
            return n, r
        r = dict(r)
        r["status"] = "verify-failed"
        r["reason"] = v["reason"]
        return n, r

    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for n, r in ex.map(check, list(resolved.items())):
            resolved[n] = r

    # E. 组装索引
    new_index = {}
    coverage = []
    linked_names = set()
    for n in sorted(resolved, key=lambda x: (-count_of(x), x)):
        r = resolved[n]
        c = count_of(n)
        if r and r.get("status") == "resolved":
            key = "《%s》" % r["key_name"]
            entry = {"url": r["url"], "source_type": r["source_type"],
                     "confidence": r["confidence"], "canonical_title": r["canonical_title"],
                     "provider": r["provider"], "checked_at": TODAY}
            if r.get("note"):
                entry["note"] = r["note"]
            if key in new_index and new_index[key].get("source_type") != "wikipedia":
                pass                      # 已有更强的源，不降级
            else:
                new_index[key] = entry
            linked_names.add(n)
            coverage.append({"name": n, "key": key, "status": "linked",
                             "citations": c, "url": r["url"],
                             "source_type": r["source_type"], "provider": r["provider"]})
        else:
            reason = (r or {}).get("reason") or "权威源未检索到匹配条目（书名不规范或无数字化版本）"
            if (r or {}).get("status") == "verify-failed":
                reason = "核验失败（%s），已剔除" % reason
            key = "《%s》" % n
            new_index.setdefault(key, {"url": "", "source_type": "unverifiable",
                                       "confidence": 0.0, "reason": reason,
                                       "checked_at": TODAY})
            coverage.append({"name": n, "key": key, "status": "unverifiable",
                             "citations": c, "reason": reason})

    # E2. 存量保留：200 的旧 key；若其书级名已换到可回读源，则丢弃旧的章节级链
    dropped = []
    for key, info in kept.items():
        inner = key[1:-1]
        br = {}
        if "·" in inner:
            br = resolved.get(inner.split("·")[0]) or {}
        if br and br.get("status") == "resolved" and br.get("key_name") != inner:
            dropped.append({"dropped_key": key, "reason": "书级名已换到可回读源 %s" % br.get("provider"),
                            "replaced_by": "《%s》" % br["key_name"]})
            continue
        if key in new_index:
            occ = new_index[key]
            if not (occ.get("url") or "").strip() and (info.get("url") or "").strip():
                # 占位的是「未解析」，而存量有实测 200 的链接 -> 存量胜出
                entry = dict(info)
                if entry.get("source_type") == "ctext" and not entry.get("note"):
                    entry["note"] = CTEXT_NOTE
                new_index[key] = entry
                coverage.append({"name": inner, "key": key, "status": "linked",
                                 "citations": count_of(inner), "url": entry.get("url"),
                                 "source_type": entry.get("source_type"),
                                 "provider": "存量保留（覆盖未解析占位）"})
                continue
            dropped.append({"dropped_key": key,
                            "reason": "同 key 已由本轮解析出的可回读源占用",
                            "replaced_by": key})
            continue
        entry = dict(info)
        if entry.get("source_type") == "ctext" and not entry.get("note"):
            entry["note"] = CTEXT_NOTE
        new_index[key] = entry
        coverage.append({"name": inner, "key": key, "status": "linked",
                         "citations": count_of(inner), "url": entry.get("url"),
                         "source_type": entry.get("source_type"), "provider": "存量保留"})

    # F. 覆盖指标（按 source_link_index 的真实匹配口径）
    sys.path.insert(0, str(REPO_ROOT))
    from tools.source_link_index import resolve_source_chapter
    modes_linked = sum(1 for m in modes
                       if any(x["status"] == "linked"
                              for x in resolve_source_chapter(m.get("source_chapter"), new_index)))
    modes_with_cit = sum(1 for m in modes if extract_refs(m.get("source_chapter")))
    cit_total = cit_linked = 0
    for m in modes:
        for x in resolve_source_chapter(m.get("source_chapter"), new_index):
            cit_total += 1
            if x["status"] == "linked":
                cit_linked += 1

    linked = [x for x in coverage if x["status"] == "linked"]
    unver = [x for x in coverage if x["status"] != "linked"]
    report = {
        "schema": "protreptic.source_link_coverage/v1",
        "generated_at": TODAY,
        "generated_by": "tools/build_source_links.py",
        "modes_total": len(modes),
        "modes_with_citations": modes_with_cit,
        "distinct_cited_names": len(span_counts),
        "distinct_book_level_names": len(counts),
        "candidate_scope": "book-level merged raw spans (卡 t_70a8cbce 口径修复)",
        "candidates_min3": len(candidates),
        "index_keys_total": len(new_index),
        "index_keys_linked": sum(1 for v in new_index.values() if (v.get("url") or "").strip()),
        "index_keys_unverifiable": sum(1 for v in new_index.values() if not (v.get("url") or "").strip()),
        "candidates": {"total": len(coverage), "linked": len(linked), "unverifiable": len(unver)},
        "provider_distribution": {},
        "citation_coverage": {"citations_total": cit_total, "citations_linked": cit_linked,
                              "modes_with_citations": modes_with_cit,
                              "modes_with_at_least_one_linked_citation": modes_linked},
        "stale_entries_reprobed": stale_urls,
        "dropped_chapter_keys": dropped,
        "entries": coverage,
        "unverifiable_reasons": {},
    }
    for x in linked:
        report["provider_distribution"][x["source_type"]] = \
            report["provider_distribution"].get(x["source_type"], 0) + 1
    for x in unver:
        r = x.get("reason", "?")
        report["unverifiable_reasons"][r] = report["unverifiable_reasons"].get(r, 0) + 1

    print()
    print("来源分布：%s" % json.dumps(report["provider_distribution"], ensure_ascii=False))
    print("索引 key：%d（有 url %d / unverifiable %d）"
          % (len(new_index), report["index_keys_linked"], report["index_keys_unverifiable"]))
    print("引文覆盖：%d/%d 条引文可点 = %.1f%%；%d/%d 条模式至少一条引文可点 = %.1f%%"
          % (cit_linked, cit_total, 100.0 * cit_linked / max(1, cit_total),
             modes_linked, modes_with_cit, 100.0 * modes_linked / max(1, modes_with_cit)))
    print("存量章节级链被书级可回读源替换：%d 条" % len(dropped))
    if args.review:
        print()
        print("--- 已链接（名 -> url）---")
        for x in sorted(linked, key=lambda y: (-y["citations"], y["name"])):
            print("%3d  %-26s %s" % (x["citations"], x["name"], x["url"]))
        print()
        print("--- 不可链接（按被引次数）---")
        for x in sorted(unver, key=lambda y: (-y["citations"], y["name"]))[:120]:
            print("%3d  %-26s %s" % (x["citations"], x["name"], x.get("reason", "")[:60]))

    if args.dry_run:
        print("[dry-run] 未写文件")
        return 0
    with open(args.links_path, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(new_index.items())), f, ensure_ascii=False, indent=2)
        f.write("\n")
    Path(args.report_path).parent.mkdir(parents=True, exist_ok=True)
    with open(args.report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("[OK] 写入 %s（%d keys）" % (args.links_path, len(new_index)))
    print("[OK] 写入 %s" % args.report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
