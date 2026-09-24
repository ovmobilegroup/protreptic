#!/usr/bin/env python3
"""fetch_batch1_texts.py -- W8 Stage2 批1 全文抓取（缓存，零主库写）。

背景
    Phase21-W8 Stage2 批1（卡 t_70a8cbce）：按书单抓取 16 部书的主源全文到本地缓存，
    供逐条引文对照（quote/异文/查无）使用。来源 URL 取自
    docs/research/phase21w8_stage2_batch1_booklist.json 的 batch1[].primary 字段，
    逐页抓取清单见 tools/manifests/w8_stage2_batch1_texts.json 。
    现代诗为否定记录（无源），manifest 中标 fetch=none，不抓。

体系（沿用 W5 pilot 口径）
    * 文本文件落 data/audit/source_texts/<sha1(key)[:16]>.txt（与 W5 共用缓存目录，只新增文件）。
    * 中文（繁体底本）另产 zh-cn 转换副本 <slug>.zh-cn.txt（复用 tools.fetch_source_texts.。
      convert_to_zh_cn；转换来源/时间/分块/失败重试元数据随条目入索引）。
    * 索引为独立文件 data/audit/source_texts_w8_stage2_batch1.json —— 不改动
      data/audit/source_texts.json（D4 链在用），留待链接入库卡合并 。
    * coverage: single-page（单页）/ complete（枚举页全抓到）/ partial（缺页）。
    * 抓取/转换失败如实登记（pages_failed / zh_cn.failed_chunks），不伪造文本。

用法
    python3 tools/fetch_batch1_texts.py --dry-run          # 只枚举子页，不抓正文
    python3 tools/fetch_batch1_texts.py                    # 抓取全部（增量：已 ok 跳过）
    python3 tools/fetch_batch1_texts.py --only 春秋繁露,老子注 --force
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.fetch_source_texts import (  # noqa: E402
    MIN_CHARS,
    convert_to_zh_cn,
    curl,
    html_to_text,
    raw_to_text,
    raw_url,
    slug,
    subpages_of,
)

SCHEMA = "protreptic.source_texts/v1"
DEFAULT_MANIFEST = REPO_ROOT / "tools" / "manifests" / "w8_stage2_batch1_texts.json"
DEFAULT_INDEX = REPO_ROOT / "data" / "audit" / "source_texts_w8_stage2_batch1.json"
DEFAULT_TEXT_DIR = REPO_ROOT / "data" / "audit" / "source_texts"
RETRIES = 3
SLEEP_SECONDS = 0.6
TIMEOUT_DEFAULT = 60
MAX_CHARS = 3_000_000

POLICY = (
    "缓存原文类链接（wikisource）的真实响应文本；目录页顺著子页抓并如实标 coverage"
    "（complete/partial/single-page）；抓不到或只有目录的标 index-page / fetch-failed，"
    "不伪造文本、不用二手转述补位；对 coverage=complete/single-page 的抓取结果另产 "
    "zh-cn 转换副本（zh.wikipedia action=parse 接口 variant=zh-cn），"
    "转换来源、时间、分块与失败重试元数据随条目入索引（zh_cn 字段）。"
    "本索引为 Phase21-W8 Stage2 批1 独立索引（source_texts.json 零改动）。"
)

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8,
         "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15,
         "XVI": 16, "XVII": 17, "XVIII": 18, "XIX": 19, "XX": 20, "XXI": 21,
         "XXII": 22, "XXIII": 23, "XXIV": 24, "XXV": 25}


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def api_json(site, params, timeout=TIMEOUT_DEFAULT):
    base = "https://" + site + "/w/api.php?"
    url = base + urllib.parse.urlencode(params)
    for attempt in range(RETRIES):
        code, body = curl(url, timeout)
        if code == 200 and body:
            try:
                return json.loads(body.decode("utf-8", "replace"))
            except Exception:
                pass
        time.sleep(1.0 + attempt * 1.5)
    return None


def sort_pages(names):
    """按自然序排序子页名（Book 10 / Chapitre XXV 等数字与罗马数字后缀）。"""
    def key(name):
        m = re.search(r"(\d+)$", name)
        if m:
            return (0, int(m.group(1)), name)
        m = re.search(r"([IVXL]+)$", name)
        if m and m.group(1) in ROMAN:
            return (1, ROMAN[m.group(1)], name)
        return (2, 0, name)
    return sorted(names, key=key)


def enumerate_subpages(entry, timeout):
    """子页枚举：list（manifest 显式） / links（目录页 wikitext 链接） / allpages（API 前缀）。"""
    mode = entry.get("enumerate")
    title = entry["index_title"]
    if mode == "list":
        return list(entry.get("subpages") or [])
    if mode == "links":
        code, body = 0, b""
        for attempt in range(RETRIES):
            code, body = curl(raw_url(entry["site"], title), timeout)
            if code == 200 and body:
                break
            time.sleep(1.0 + attempt * 1.5)
        if code != 200 or not body:
            raise RuntimeError("index raw fetch failed: http=%s title=%s" % (code, title))
        return subpages_of(body.decode("utf-8", "replace"), title)
    if mode == "allpages":
        prefix = title + "/"
        out, cont = [], None
        while True:
            params = {"action": "query", "list": "allpages", "apprefix": prefix,
                      "aplimit": "100", "format": "json", "formatversion": "2"}
            if cont:
                params["apcontinue"] = cont
            j = api_json(entry["site"], params, timeout)
            if not j:
                raise RuntimeError("allpages failed: %s" % prefix)
            out += [p["title"] for p in j.get("query", {}).get("allpages", [])]
            cont = (j.get("continue") or {}).get("apcontinue")
            if not cont:
                break
        subs = [t[len(prefix):] for t in out if t.startswith(prefix)]
        return sort_pages(subs)
    raise RuntimeError("unknown enumerate mode: %r" % mode)


def fetch_page(entry, title, timeout):
    """抓单页 -> (http_code, text)。 raw 走 action=raw；render 走 API action=parse。 失败给 (0, "")。"""
    if entry["fetch"] == "raw":
        code = 0
        for attempt in range(RETRIES):
            code, body = curl(raw_url(entry["site"], title), timeout)
            if code == 200 and body:
                return code, raw_to_text(body.decode("utf-8", "replace"))
            time.sleep(1.0 + attempt * 1.5)
        return code or 0, ""
    j = api_json(entry["site"], {"action": "parse", "prop": "text", "format": "json",
                                 "formatversion": "2", "disablelimitreport": "1",
                                 "disableeditsection": "1", "page": title}, timeout)
    if not j or "parse" not in j:
        return 0, ""
    return 200, html_to_text(j["parse"].get("text") or "")


def fetch_book(entry, manifest, args, text_dir):
    """抓一本书（索引页 + 子页），写缓存文件，返回索引条目。"""
    key = entry["key"]
    subpages = enumerate_subpages(entry, args.timeout)
    excl = set(entry.get("exclude_pages") or [])
    subpages = [s for s in subpages if s not in excl]
    titles = [entry["index_title"]] + [entry["index_title"] + "/" + s for s in subpages]
    parts, pages_meta, failed, pos = [], [], [], 0
    for pt in titles:
        code, text = fetch_page(entry, pt, args.timeout)
        time.sleep(args.sleep)
        if not text.strip():
            failed.append({"title": pt, "http_code": code})
            print("  [miss] %s http=%s" % (pt, code), flush=True)
            continue
        parts.append(text)
        pages_meta.append({"title": pt, "http_code": code, "chars": len(text),
                           "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                           "start": pos, "end": pos + len(text)})
        pos += len(text) + 1
    joined = "\n".join(parts)
    truncated = False
    if len(joined) > MAX_CHARS:
        joined = joined[:MAX_CHARS]
        truncated = True
    n_sub_ok = sum(1 for p in pages_meta if p["title"].startswith(entry["index_title"] + "/"))
    if not pages_meta:
        status, coverage = "fetch-failed", None
    elif len(joined) < MIN_CHARS:
        status, coverage = "index-page", None
    elif not subpages:
        status, coverage = "ok", "single-page"
    elif n_sub_ok == len(subpages):
        status, coverage = "ok", "complete"
    else:
        status, coverage = "partial", "partial"
    out = {
        "key": key, "label": entry.get("label"), "url": entry.get("url"),
        "source_type": "wikisource", "provider": entry.get("site"),
        "lang": entry.get("lang"), "script": entry.get("script"),
        "batch": manifest.get("batch"), "fetch_mode": entry.get("fetch"),
        "index_title": entry.get("index_title"), "pageid": entry.get("pageid"),
        "status": status, "coverage": coverage,
        "subpages": [n_sub_ok, len(subpages)],
        "http_code": 200 if pages_meta else 0,
        "method": "wikitext" if entry.get("fetch") == "raw" else "html-render",
        "chars": len(joined), "bytes": len(joined.encode("utf-8")),
        "sha256": hashlib.sha256(joined.encode("utf-8")).hexdigest(),
        "truncated": truncated, "fetched_at": now_iso(),
        "pages": pages_meta, "pages_failed": failed,
    }
    if joined.strip():
        fname = slug(key) + ".txt"
        (text_dir / fname).write_text(joined, encoding="utf-8")
        out["file"] = "data/audit/source_texts/" + fname
    if entry.get("convert_zh_cn") and joined.strip():
        conv, meta = convert_to_zh_cn(joined, args.timeout)
        cname = slug(key) + ".zh-cn.txt"
        (text_dir / cname).write_text(conv, encoding="utf-8")
        zh = {"file": "data/audit/source_texts/" + cname, "chars": len(conv),
              "sha256": hashlib.sha256(conv.encode("utf-8")).hexdigest()}
        zh.update(meta)
        out["zh_cn"] = zh
    return out


def load_index(path):
    if path.is_file():
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(doc, dict) and isinstance(doc.get("entries"), list):
                return doc
        except Exception:
            pass
    return {"schema": SCHEMA, "generated_by": "tools/fetch_batch1_texts.py",
            "generated_at": now_iso(), "policy": POLICY, "min_chars": MIN_CHARS,
            "max_subpages": 95, "entries": []}


def save_index(path, doc):
    doc["generated_at"] = now_iso()
    counts = {}
    for e in doc["entries"]:
        counts[e.get("status")] = counts.get(e.get("status"), 0) + 1
    doc["counts"] = counts
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def main():
    ap = argparse.ArgumentParser(description="W8 Stage2 批1 全文抓取（缓存）")
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    ap.add_argument("--index-path", default=str(DEFAULT_INDEX))
    ap.add_argument("--text-dir", default=str(DEFAULT_TEXT_DIR))
    ap.add_argument("--only", default=None, help="只抓这些 label（逗号分隔）")
    ap.add_argument("--force", action="store_true", help="重抓已 ok 的书")
    ap.add_argument("--dry-run", action="store_true", help="只枚举子页，不抓正文")
    ap.add_argument("--timeout", type=int, default=TIMEOUT_DEFAULT)
    ap.add_argument("--sleep", type=float, default=SLEEP_SECONDS)
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    index_path = Path(args.index_path)
    text_dir = Path(args.text_dir)
    text_dir.mkdir(parents=True, exist_ok=True)
    doc = load_index(index_path)
    by_key = {e["key"]: e for e in doc["entries"]}
    only = set(x.strip() for x in args.only.split(",")) if args.only else None

    for entry in manifest["books"]:
        key = entry["key"]
        label = entry.get("label") or key
        if only and label not in only and key not in only:
            continue
        if entry.get("fetch") == "none":
            print("[skip] %s：否定记录（无源，不抓）" % label)
            continue
        prev = by_key.get(key)
        if prev and prev.get("status") in ("ok", "ok-shared") and not args.force:
            print("[skip] %s：已有 %s（--force 可重抓）" % (label, prev.get("status")))
            continue
        if args.dry_run:
            subs = enumerate_subpages(entry, args.timeout)
            excl = set(entry.get("exclude_pages") or [])
            subs = [s for s in subs if s not in excl]
            print("[dry] %s: enumerate=%s -> %d 子页 %s" %
                  (label, entry.get("enumerate"), len(subs), subs[:6]))
            continue
        if entry.get("shared_from"):
            src = by_key.get(entry["shared_from"])
            if not src or not src.get("file"):
                print("[warn] %s：共源 %s 尚无缓存，跳过（先抓共源）" % (label, entry["shared_from"]))
                continue
            out = dict(src)
            out.update({"key": key, "label": label, "status": "ok-shared",
                        "shared_from": entry["shared_from"],
                        "note": "同一书二名：与 %s 共源（同 URL 同缓存文件）" % entry["shared_from"]})
            by_key[key] = out
            doc["entries"] = [by_key[k] for k in by_key]
            save_index(index_path, doc)
            print("[ok-shared] %s -> %s" % (label, src.get("file")))
            continue
        print("[fetch] %s ..." % label)
        try:
            out = fetch_book(entry, manifest, args, text_dir)
        except Exception as exc:
            print("[error] %s: %s" % (label, exc))
            continue
        by_key[key] = out
        doc["entries"] = [by_key[k] for k in by_key]
        save_index(index_path, doc)
        print("[done] %s: status=%s coverage=%s pages=%s chars=%s zh_cn=%s" %
              (label, out["status"], out["coverage"], out["subpages"], out["chars"],
               "yes" if out.get("zh_cn") else "no"))
    if not args.dry_run:
        save_index(index_path, doc)
        print("[OK] index: %s (%d entries)" % (index_path, len(doc["entries"])))


if __name__ == "__main__":
    raise SystemExit(main())
