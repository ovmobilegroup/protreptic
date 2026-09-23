#!/usr/bin/env python3
"""fetch_source_texts.py -- 把 source_links.json 里可达的原文链接抓成本地文本缓存（供 D4 子串核验）。

为什么有它
    docs/planning/credibility_framework.md 第 1 节的 D4（引文不符：key_quote_zh 不出现在所标出处
    的原文里）此前是空壳：check_d4_quote_mismatch 只判「有引文但出处为空」，真正的子串核验需要原文。
    本脚本负责取原文这一步，产出本地缓存：

        data/audit/source_texts/<sha1(key)[:16]>.txt    纯文本原文
        data/audit/source_texts.json                    机读索引（key / url / 状态 / 覆盖度 / 指纹）

    缓存入库（两仓同步）后，tools/credibility_gate.py 的 D4 在离线环境也能做子串核验：
    CI 不联网、不重新抓取；取不到文本或只取到部分篇章的条目一律标 unchecked 并计入统计。

抓取口径（诚实标注优先）
    * 只抓 source_type 属于原文类的条目（wikisource / gutenberg / ctext）；
      wikipedia（条目页）与 unverifiable（口述/信札）不抓 -- 前者不是原文，后者本质不可链接。
    * wikisource 走 action=raw（wikitext）拿正文；页面若只是目录（如《传习录》卷上/卷中/卷下），
      **顺着子页链接把分卷一并抓下来**，并如实记录 coverage：
          single-page  单页即全文
          complete     目录 + 全部子页（缓存覆盖整部作品）
          partial      目录 + 前 N 个子页（**未覆盖全部篇章** -> D4 对该 key 视为不可核）
    * gutenberg 的 /ebooks/<id> 落地页换成 /cache/epub/<id>/pg<id>.txt（真全文）。
    * ctext 有 Cloudflare 挑战页，curl 拿不到正文 -> 如实记 http-error，不伪造。
    * 每个 key 逐条记录 status：ok / partial / index-page / fetch-failed / http-error。
      抓不到就是抓不到：不伪造、不用二手转述补位（框架第 6 节铁律 2）。

用法
    python3 tools/fetch_source_texts.py --dry-run
    python3 tools/fetch_source_texts.py --limit 20
    python3 tools/fetch_source_texts.py --force --max-subpages 12
退出码：0 成功（逐条状态如实入库）/ 1 索引写入失败 / 2 输入缺失。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LINKS = REPO_ROOT / "data" / "source_links.json"
DEFAULT_INDEX = REPO_ROOT / "data" / "audit" / "source_texts.json"
DEFAULT_TEXT_DIR = REPO_ROOT / "data" / "audit" / "source_texts"
UA = "Mozilla/5.0 (compatible; protreptic-credibility/1.0)"
SCHEMA = "protreptic.source_texts/v1"
FULLTEXT_TYPES = ("wikisource", "gutenberg", "ctext")
MIN_CHARS = 800
MAX_BYTES_DEFAULT = 500_000
DEFAULT_MAX_CHARS = 120000
DEFAULT_MAX_SUBPAGES = 12

# Phase21-W5 pilot: 繁简双轨缓存（raw + zh-cn 转换副本）
CONVERT_API = "https://zh.wikipedia.org/w/api.php"
CONVERT_VARIANT = "zh-cn"
CONVERT_CHUNK_CHARS = 8000
CONVERT_RETRIES = 5
CONVERT_BACKOFF_SECONDS = 2
CONVERT_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


class _Strip(HTMLParser):
    """极简 HTML 转文本（丢掉 script/style，保留正文）。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        elif tag in ("p", "br", "div", "li", "tr", "h1", "h2", "h3", "td"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data:
            self.parts.append(data)


def html_to_text(html):
    start = html.find("mw-parser-output")
    if start > 0:
        html = html[start:]
    end = html.find("printfooter")
    if end > 0:
        html = html[:end]
    p = _Strip()
    try:
        p.feed(html)
    except Exception:
        pass
    text = "".join(p.parts)
    text = re.sub(r"[ \t\u00a0]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def raw_to_text(wikitext):
    """wikitext 转纯文本（去掉模板/链接语法，保留字面文字）。"""
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", wikitext, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\{\{[^{}]*\}\}", "", text)
    text = re.sub(r"\{\{[^{}]*\}\}", "", text)
    text = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]*)\]\]", r"\1", text)
    text = re.sub(r"''+", "", text)
    text = re.sub(r"^[=]+(.*?)[=]+$", r"\1", text, flags=re.M)
    text = re.sub(r"[ \t\u00a0]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def slug(key):
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]


def curl(url, timeout):
    """返回 (http_code, body)。连接层失败返回 (0, b'')。"""
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout), "-A", UA, "-w", "\n%{http_code}", url],
            capture_output=True, timeout=timeout + 10,
        )
    except Exception:
        return 0, b""
    out = r.stdout or b""
    if b"\n" not in out:
        return 0, out
    body, _, code = out.rpartition(b"\n")
    try:
        return int(code.strip() or b"0"), body
    except ValueError:
        return 0, body


def convert_to_zh_cn(text, timeout):
    """繁 -> 简转换，走 zh.wikipedia action=parse&contentmodel=wikitext&variant=zh-cn 接口。

    Phase21-W5 pilot 扩能：分块 POST（CONVERT_CHUNK_CHARS），单块失败重试 CONVERT_RETRIES 次；
    重试仍失败的块保留繁体原文（不静默丢块、不伪造转换），并在元数据里如实记录失败块数；
    D4 对 failed_chunks>0（complete=False）的转换副本不予采用——
    宁可退回 script-mismatch 守卫，也不拿不完整的转换当全文比对。
    返回 (converted_text, meta)。
    """
    chunks = [text[i:i + CONVERT_CHUNK_CHARS] for i in range(0, len(text), CONVERT_CHUNK_CHARS)] or [""]
    parts = []
    failed = 0
    for ch in chunks:
        ok = False
        for attempt in range(CONVERT_RETRIES):
            if attempt:
                time.sleep(CONVERT_BACKOFF_SECONDS * attempt)
            try:
                r = subprocess.run(
                    ["curl", "-s", "--max-time", str(timeout), "-A", CONVERT_UA,
                     "--data-urlencode", "text@-", "-w", "\n%{http_code}",
                     CONVERT_API + "?action=parse&contentmodel=wikitext&variant=" + CONVERT_VARIANT + "&format=json&formatversion=2&prop=text"],
                    input=ch.encode("utf-8"), capture_output=True, timeout=timeout + 10)
            except Exception:
                continue
            out = r.stdout or b""
            if b"\n" not in out:
                continue
            body, _, code = out.rpartition(b"\n")
            try:
                if int(code.strip() or b"0") != 200:
                    continue
            except ValueError:
                time.sleep(CONVERT_BACKOFF_SECONDS)
                continue
            try:
                doc = json.loads(body.decode("utf-8", "replace"))
                html = re.sub(r"<!--.*?-->", "", doc["parse"]["text"], flags=re.S)
                sp = _Strip()
                sp.feed(html)
                parts.append("".join(sp.parts))
                ok = True
                break
            except Exception:
                continue
        if not ok:
            failed += 1
            parts.append(ch)
    meta = {"api": CONVERT_API, "variant": CONVERT_VARIANT,
            "method": "action=parse&contentmodel=wikitext&variant=zh-cn (POST text)",
            "chunk_chars": CONVERT_CHUNK_CHARS, "chunks": len(chunks),
            "retries": CONVERT_RETRIES, "failed_chunks": failed,
            "complete": failed == 0,
            "converted_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    return "".join(parts), meta


LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]")


def wikisource_parts(url):
    """wikisource 链接 -> (host, title)。非 wikisource 返回 (None, None)。"""
    m = re.match(r"^https?://([a-z.]*wikisource\.org)/wiki/(.+?)(?:#.*)?$", url)
    if not m:
        return None, None
    return m.group(1), unquote(m.group(2))


def raw_url(host, title):
    return "".join(["https://", host, "/w/index.php?title=", quote(title, safe="/"),
                    "&action=raw"])


def subpages_of(wikitext, title):
    """目录页里的子页名（[[/卷上|卷上]] 或 [[傳習錄/卷上|…]]），保序去重。"""
    subs = []
    for m in LINK_RE.finditer(wikitext):
        target = m.group(1).strip()
        if target.startswith("/"):
            name = target[1:]
        elif target.startswith(title + "/"):
            name = target[len(title) + 1:]
        else:
            continue
        if name and "/" not in name and name not in subs:
            subs.append(name)
    return subs


def gutenberg_text_url(url):
    m = re.match(r"^https?://(?:www\.)?gutenberg\.org/(?:ebooks|etext)/(\d+)$", url)
    if not m:
        return None
    i = m.group(1)
    return "https://www.gutenberg.org/cache/epub/" + i + "/pg" + i + ".txt"


def fetch_one(url, timeout, max_bytes, max_subpages):
    """抓一条链接 -> {status, coverage, http_code, text, method, url_fetched, subpages}。"""
    out = {"status": "fetch-failed", "coverage": None, "http_code": 0, "text": "",
           "method": "html", "url_fetched": url, "subpages": [0, 0]}
    host, title = wikisource_parts(url)

    if host and title:
        code, body = curl(raw_url(host, title), timeout)
        if code == 200 and body:
            wikitext = body[:max_bytes].decode("utf-8", "replace")
            subs = subpages_of(wikitext, title)
            texts = [raw_to_text(wikitext)]
            if len(subs) > max_subpages:
                # 分卷数超过上限：**不去抓那 N 卷**（抓了也只是部分语料，D4 照样不可核），
                # 如实记 status=partial（缓存未能覆盖整部作品），省掉无意义的抓取。
                out.update({"text": texts[0], "method": "wikitext", "coverage": "partial",
                            "subpages": [0, len(subs)], "status": "partial", "http_code": 200})
                return out
            got = 0
            for name in subs:
                if got >= max_subpages:
                    break
                c2, b2 = curl(raw_url(host, title + "/" + name), timeout)
                if c2 == 200 and b2:
                    texts.append(raw_to_text(b2[:max_bytes].decode("utf-8", "replace")))
                    got += 1
            text = "\n".join(t for t in texts if t.strip())
            if len(text) >= MIN_CHARS:
                if not subs:
                    coverage = "single-page"
                elif got >= len(subs):
                    coverage = "complete"
                else:
                    coverage = "partial"
                out.update({"text": text, "method": "wikitext", "coverage": coverage,
                            "subpages": [got, len(subs)], "status": "ok"})
                out["http_code"] = 200
                return out
            # 目录页且子页也拿不到正文 -> 继续试 HTML
    elif url.endswith(".txt"):
        code, body = curl(url, timeout)
        if code == 200 and body:
            text = body[:max_bytes].decode("utf-8", "replace")
            if len(text) >= MIN_CHARS:
                out.update({"text": text, "method": "plain", "coverage": "single-page",
                            "status": "ok", "http_code": 200})
                return out

    gut = gutenberg_text_url(url)
    fetched_url = gut or url
    code, body = curl(fetched_url, timeout)
    if code and code != 200:
        out["http_code"] = code
        out["status"] = "http-error"
        return out
    if code != 200 or not body:
        return out
    decoded = body[:max_bytes].decode("utf-8", "replace")
    text = decoded if fetched_url.endswith(".txt") else html_to_text(decoded)
    out.update({"text": text, "method": "plain" if fetched_url.endswith(".txt") else "html",
                "url_fetched": fetched_url, "http_code": code})
    if not text:
        out["status"] = "fetch-failed"
        return out
    out["status"] = "ok" if len(text) >= MIN_CHARS else "index-page"
    out["coverage"] = "single-page" if out["status"] == "ok" else None
    return out


def main():
    global MIN_CHARS
    ap = argparse.ArgumentParser(description="抓取原文类出处文本到本地缓存（供 D4 子串核验）")
    ap.add_argument("--links-path", default=str(DEFAULT_LINKS))
    ap.add_argument("--index-path", default=str(DEFAULT_INDEX))
    ap.add_argument("--text-dir", default=str(DEFAULT_TEXT_DIR))
    ap.add_argument("--types", default=",".join(FULLTEXT_TYPES), help="只抓这些 source_type（逗号分隔）")
    ap.add_argument("--keys", default=None, help="只抓这些 key（逗号分隔）")
    ap.add_argument("--limit", type=int, default=0, help="最多抓 N 条（0 = 不限）")
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--max-bytes", type=int, default=MAX_BYTES_DEFAULT)
    ap.add_argument("--min-chars", type=int, default=MIN_CHARS)
    ap.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS,
                    help="单条缓存文本的最大字符数（超出截断并标 truncated）")
    ap.add_argument("--max-subpages", type=int, default=DEFAULT_MAX_SUBPAGES,
                    help="目录页最多跟抓多少个子页；抓不满 -> coverage=partial（D4 视为不可核）")
    ap.add_argument("--force", action="store_true", help="已有 ok 缓存也重抓")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    MIN_CHARS = args.min_chars

    links_path = Path(args.links_path)
    if not links_path.is_file():
        print("[FAIL] 输入缺失: %s" % links_path, file=sys.stderr)
        return 2
    links = json.loads(links_path.read_text(encoding="utf-8"))
    types = set(t.strip() for t in args.types.split(",") if t.strip())
    keys = set(k.strip() for k in args.keys.split(",")) if args.keys else None

    index_path = Path(args.index_path)
    text_dir = Path(args.text_dir)
    old = {}
    if index_path.is_file():
        try:
            doc = json.loads(index_path.read_text(encoding="utf-8"))
            old = dict((e["key"], e) for e in doc.get("entries", []))
        except Exception:
            old = {}

    targets = []
    for key in sorted(links):
        info = links[key]
        if not isinstance(info, dict):
            continue
        if (info.get("source_type") or "") not in types:
            continue
        if not (info.get("url") or "").strip():
            continue
        if keys is not None and key not in keys:
            continue
        targets.append((key, info))
    if args.limit:
        targets = targets[: args.limit]

    print("source_links: %s (%d key)" % (links_path, len(links)))
    print("原文类待抓 (types=%s): %d 条" % (",".join(sorted(types)), len(targets)))
    if args.dry_run:
        for key, info in targets:
            print("  %s  [%s]  %s" % (key, info.get("source_type"), info.get("url")))
        return 0

    text_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    counts = {}
    by_url = {}
    by_url_zh = {}
    for key, info in targets:
        prev = old.get(key)
        if prev and prev.get("status") == "ok" and not args.force:
            entries.append(prev)
            counts["cached"] = counts.get("cached", 0) + 1
            print("  [cached] %s" % key)
            continue
        r = fetch_one((info.get("url") or "").strip(), args.timeout, args.max_bytes,
                      args.max_subpages)
        text = r["text"]
        truncated = len(text) > args.max_chars
        if truncated:
            text = text[: args.max_chars]
        file_rel = "data/audit/source_texts/%s.txt" % slug(key)
        if text and r["url_fetched"] in by_url:
            file_rel = by_url[r["url_fetched"]]
            r["status"] = "ok-shared"
        elif text:
            (REPO_ROOT / file_rel).write_text(text, encoding="utf-8")
            by_url[r["url_fetched"]] = file_rel
        zh_cn_meta = None
        if text and r["status"] in ("ok", "ok-shared") \
                and r.get("coverage") in ("single-page", "complete"):
            conv_text, conv_meta = convert_to_zh_cn(text, args.timeout)
            zrel = "data/audit/source_texts/%s.zh-cn.txt" % slug(key)
            if r["url_fetched"] in by_url_zh:
                zrel = by_url_zh[r["url_fetched"]]
            else:
                (REPO_ROOT / zrel).write_text(conv_text, encoding="utf-8")
                by_url_zh[r["url_fetched"]] = zrel
            conv_meta.update({"chars": len(conv_text),
                              "sha256": hashlib.sha256(conv_text.encode("utf-8")).hexdigest(),
                              "file": zrel})
            zh_cn_meta = conv_meta
            print("  [zh-cn] %s chunks=%s failed=%s complete=%s" %
                  (key[:40], conv_meta["chunks"], conv_meta["failed_chunks"],
                   conv_meta["complete"]))
        entry = {
            "key": key,
            "url": (info.get("url") or "").strip(),
            "url_fetched": r["url_fetched"],
            "source_type": info.get("source_type"),
            "status": r["status"],
            "coverage": r.get("coverage"),
            "subpages": r.get("subpages"),
            "http_code": r["http_code"],
            "method": r["method"],
            "chars": len(text),
            "bytes": len(text.encode("utf-8")),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest() if text else None,
            "file": file_rel if text else None,
            "truncated": truncated,
            "zh_cn": zh_cn_meta,
        }
        entries.append(entry)
        counts[r["status"]] = counts.get(r["status"], 0) + 1
        print("  [%s] http=%-5s chars=%-7d cov=%-11s subs=%s %s"
              % (r["status"], r["http_code"], len(text), str(r.get("coverage")),
                 r.get("subpages"), key[:50]))

    payload = {
        "schema": SCHEMA,
        "generated_by": "tools/fetch_source_texts.py",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "policy": ("只缓存原文类链接（wikisource/gutenberg/ctext）的真实响应文本；"
                   "目录页顺着子页抓并如实标 coverage（complete/partial/single-page）；"
                   "抓不到或只有目录的标 index-page / fetch-failed / http-error，"
                   "不伪造文本、不用二手转述补位（credibility_framework.md 第 6 节铁律 2）；"
                   "对 coverage=complete/single-page 的抓取结果另产 zh-cn 转换副本"
                   "（zh.wikipedia action=parse&contentmodel=wikitext&variant=zh-cn），"
                   "转换来源、时间、分块与失败重试元数据随条目入索引（zh_cn 字段）"),
        "min_chars": MIN_CHARS,
        "max_subpages": args.max_subpages,
        "counts": counts,
        "entries": entries,
    }
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print()
    print("索引写入 %s (%d 条; %s)" % (index_path, len(entries), json.dumps(counts, ensure_ascii=False)))
    print("文本目录 %s" % text_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
