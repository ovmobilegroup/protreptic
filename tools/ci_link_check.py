#!/usr/bin/env python3
"""ci_link_check.py -- Phase30-C1 死链检测门 (站内链接 + sitemap URL 全部可达).

两个子命令, 同一套判定语义:

  dist  离站检测: 遍历 web/dist 下所有 HTML, 抽出每个 href/src 站内引用, 逐个解析到磁盘
        文件并断言存在; 同时校验 <link rel="canonical"> 与该页自身 URL 一致, 且 sitemap
        里的每个 URL 在 dist 里都能落到实际文件. 不需要网络, 可在部署前拦住断链.

  live  线上检测: 取 sitemap.xml 的 URL 全集中 + 路由清单的 canonical + 站内资源引用,
        逐个真实 HTTP 请求. 判定口径 (来自 Phase30-A0 实测, 写死在这里以免后人踩坑):
          * 301/302/307/308 允许, 但 **跟随重定向后的最终状态码必须是 200**;
            线上 /protreptic/figures 就是 301 -> /protrectic/figures/ -> 200,
            按「!= 200 即死链」判会把整站入口全部误报.
          * 最终 4xx/5xx 或网络失败 (重试耗尽) => 死链.
          * 5xx / 429 属于可重试, 重试仍失败才算死链.

自检注入: --break-link 往待检集合里塞入一个必然不存在的 URL/路径, 用来证明「本检测确实
会失败」而不是永远绿. CI 用 workflow_dispatch 的 break_link 输入触发这条路径.

用法:
  python3 tools/ci_link_check.py dist --dist web/dist
  python3 tools/ci_link_check.py live --base-url https://ovmobilegroup.github.io/protreptic
  python3 tools/ci_link_check.py live --assets-from web/dist --max-links 200
  python3 tools/ci_link_check.py live --break-link          # 自检: 应当 exit 1

退出码: 0 全部可达; 1 存在死链 / 自检注入被漏检; 2 用法或输入错误.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

SITE_ORIGIN = "https://ovmobilegroup.github.io"
DEFAULT_BASE = "/protreptic/"
DEFAULT_ROUTES = "docs/architecture/web_p0_routes.json"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
BREAK_TOKEN = "__quality_gate_self_test_dead_link__"

ATTR_RE = re.compile(r"""(?:href|src)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
CANONICAL_RE = re.compile(
    r"""<link[^>]+rel\s*=\s*["']canonical["'][^>]*>""", re.I
)
CANONICAL_HREF_RE = re.compile(r"""href\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)

SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:", "blob:", "about:")


class Report:
    def __init__(self, title: str) -> None:
        self.title = title
        self.failures: list[str] = []
        self.checked = 0
        self.notes: list[str] = []

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    def finish(self) -> int:
        for n in self.notes:
            print(f"  · {n}")
        print(f"{self.title}: 检查 {self.checked} 条, 失败 {len(self.failures)} 条")
        if self.failures:
            print(f"{self.title}: FAIL -- 死链/断言失败明细 (最多 40 条):")
            for f in self.failures[:40]:
                print(f"    - {f}")
            if len(self.failures) > 40:
                print(f"    ... 另有 {len(self.failures) - 40} 条未列出")
            return 1
        print(f"{self.title}: PASS")
        return 0


def encode_url(url: str) -> str:
    """把 URL 路径段做百分号转义 (裸空格/中文等), 已转义的部分保持不变.

    为什么需要: 公开名录里有 code 带空格的记录 (Sun Quan / code field), 路由清单的
    canonical 是裸空格 —— 裸空格不是合法 URL, urllib 会直接抛 InvalidURL, 而线上
    资源本身是好的 (%20 形式返回 200). 检测要对资源可达性负责, 所以先转义再请求,
    同时在报告里保留原始写法以免掩盖上游未转义的缺陷 (该缺陷由 ci_data_check 断言).
    """
    parts = urllib.parse.urlsplit(url)
    path = "/".join(urllib.parse.quote(seg, safe="%") for seg in parts.path.split("/"))
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))


def strip_query(url: str) -> str:
    return url.split("#", 1)[0].split("?", 1)[0]


def is_internal(url: str) -> bool:
    u = url.strip()
    if not u or u.startswith("#"):
        return False
    low = u.lower()
    if low.startswith(SKIP_SCHEMES):
        return False
    if low.startswith("//"):
        return False
    return not re.match(r"^[a-z][a-z0-9+.\-]*:", low)


def to_site_path(url: str, base: str) -> str | None:
    """把站内引用规整成 <base> 开头的站点绝对路径; 站外/无法规整返回 None."""
    u = strip_query(html.unescape(url.strip()))
    if not u:
        return None
    if is_internal(u):
        if u.startswith("/"):
            p = u
        else:
            return None  # 相对引用单独处理
        if not p.startswith(base):
            if p == base.rstrip("/"):
                return base
            return None  # 不在本站 base 下
        return p
    parsed = urllib.parse.urlparse(u)
    if parsed.netloc == urllib.parse.urlparse(SITE_ORIGIN).netloc:
        p = parsed.path
        return p if p.startswith(base) else None
    return None


def resolve_relative(url: str, page_path: str, base: str) -> str | None:
    """页面内相对引用 -> 站点绝对路径 (页面的 URL 目录作为基准)."""
    u = strip_query(html.unescape(url.strip()))
    if not u or u.startswith("#") or u.startswith("/"):
        return None
    if not is_internal(u):
        return None
    page_url = base + ("" if page_path in ("", "/") else page_path.strip("/") + "/")
    joined = urllib.parse.urljoin("https://x" + page_url, u)
    p = urllib.parse.urlparse(joined).path
    return p if p.startswith(base) else None


def path_to_file(dist: Path, site_path: str, base: str) -> Path:
    rel = site_path[len(base):].lstrip("/") if site_path != base else ""
    if not rel:
        return dist / "index.html"
    return dist / rel


def file_exists(dist: Path, target: Path) -> bool:
    if target.is_file():
        return True
    if target.is_dir() and (target / "index.html").is_file():
        return True
    return False


def load_routes(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def sitemap_urls(path: Path) -> list[str]:
    root = ET.parse(path).getroot()
    return [
        (el.text or "").strip()
        for el in root.iter(f"{{{SITEMAP_NS}}}loc")
        if (el.text or "").strip()
    ]


# --------------------------------------------------------------------------- dist
def run_dist(args: argparse.Namespace) -> int:
    dist = Path(args.dist).resolve()
    if not dist.is_dir():
        print(f"输入错误: dist 目录不存在: {dist}", file=sys.stderr)
        return 2
    base = args.base
    rep = Report(f"[dist] {dist}")

    html_files = sorted(dist.rglob("*.html"))
    if not html_files:
        rep.fail(f"{dist} 下没有任何 HTML 文件")
        return rep.finish()

    routes_path = Path(args.routes).resolve()
    route_pages: dict[str, str] = {}
    if routes_path.is_file():
        routes = load_routes(routes_path)
        base = routes.get("base", base)
        for r in routes.get("routes", []):
            route_pages[r["path"].strip("/")] = r.get("canonical", "")
    else:
        rep.fail(f"路由清单不存在: {routes_path}")
        return rep.finish()

    checked_links = 0
    dead: list[str] = []
    canonical_bad: list[str] = []
    off_base: list[str] = []
    pages_with_canonical = 0

    for f in html_files:
        rel = f.relative_to(dist).as_posix()
        page_path = "" if rel == "index.html" else rel[: -len("/index.html")]
        text = f.read_text(encoding="utf-8", errors="replace")

        for m in ATTR_RE.finditer(text):
            raw = m.group(1) or m.group(2) or ""
            cleaned = strip_query(html.unescape(raw.strip()))
            if cleaned.startswith("/") and not cleaned.startswith("//") \
                    and not cleaned.startswith(base) and cleaned != base.rstrip("/"):
                if len(off_base) < 40:
                    off_base.append(f"{rel} -> {raw} (根绝对路径未带 base {base})")
                continue
            site_path = to_site_path(raw, base)
            if site_path is None:
                site_path = resolve_relative(raw, page_path, base)
            if site_path is None:
                continue
            checked_links += 1
            target = path_to_file(dist, site_path, base)
            if not file_exists(dist, target):
                if len(dead) < 200:
                    dead.append(f"{rel} -> {raw} (缺 {target.relative_to(dist)})")

        canon_m = CANONICAL_RE.search(text)
        if canon_m:
            pages_with_canonical += 1
            href_m = CANONICAL_HREF_RE.search(canon_m.group(0))
            canon = html.unescape(href_m.group(1) or href_m.group(2) or "") if href_m else ""
            expected = f"{SITE_ORIGIN}{base}{page_path + '/' if page_path else ''}"
            if canon != expected:
                if len(canonical_bad) < 40:
                    canonical_bad.append(f"{rel}: canonical={canon!r} != {expected!r}")

    rep.checked = checked_links
    if dead:
        for d in dead:
            rep.fail(d)
    rep.note(f"HTML 页数 {len(html_files)}, 站内引用 {checked_links} 条, "
             f"带 canonical 的页面 {pages_with_canonical}")
    for c in canonical_bad:
        rep.fail(c)
    if off_base:
        rep.note(f"根绝对引用未带 base 的 {len(off_base)} 处")
    for o in off_base:
        rep.fail(o)

    # sitemap -> dist 文件
    if args.sitemap == "":
        rep.note("sitemap 检查被 --sitemap 空串跳过 (仅限本地排查, CI 不允许)")
        if args.break_link:
            fake = f"{base}{BREAK_TOKEN}/"
            rep.note(f"自检注入: {fake} (必然不存在, 期望 PASS 判定失败)")
            rep.checked += 1
            if file_exists(dist, path_to_file(dist, fake, base)):
                rep.fail(f"自检失效: 注入的 {fake} 竟然存在")
            else:
                rep.fail(f"[自检注入] 死链未被检出: {fake}")
        return rep.finish()
    sm = Path(args.sitemap).resolve()
    if sm.is_file():
        locs = sitemap_urls(sm)
        missing = []
        for loc in locs:
            site_path = to_site_path(loc, base)
            if site_path is None:
                missing.append(f"sitemap 条目不在本站 base 下: {loc}")
                continue
            if not file_exists(dist, path_to_file(dist, site_path, base)):
                missing.append(f"sitemap 条目无对应产物: {loc}")
        rep.checked += len(locs)
        rep.note(f"sitemap 条目 {len(locs)} 条, 其中 {len(missing)} 条与 dist 对不上")
        for m in missing[:40]:
            rep.fail(m)
    else:
        rep.fail(f"sitemap 不存在: {sm} (先跑 tools/build_sitemap.py)")

    if args.break_link:
        fake = f"{base}{BREAK_TOKEN}/"
        rep.note(f"自检注入: {fake} (必然不存在, 期望 PASS 判定失败)")
        rep.checked += 1
        if file_exists(dist, path_to_file(dist, fake, base)):
            rep.fail(f"自检失效: 注入的 {fake} 竟然存在")
        else:
            rep.fail(f"[自检注入] 死链未被检出: {fake}")

    return rep.finish()


# --------------------------------------------------------------------------- live
def http_probe(url: str, timeout: float, retries: int) -> tuple[str, int | str, str]:
    """返回 (url, final_status_or_error, final_url). 重定向由 urllib 自动跟随."""
    last_err = ""
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url,
            method="GET",
            headers={
                "User-Agent": "protreptic-quality-gate/1.0 (+ci)",
                "Accept": "*/*",
                "Cache-Control": "no-cache",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                resp.read(1024)
                return url, int(resp.status), resp.geturl()
        except urllib.error.HTTPError as exc:
            code = int(exc.code)
            if code >= 500 or code == 429:
                last_err = f"HTTP {code}"
                time.sleep(1.5 * (attempt + 1))
                continue
            return url, code, exc.geturl() if hasattr(exc, "geturl") else url
        except Exception as exc:  # noqa: BLE001 - 网络类异常统一按可重试处理
            last_err = f"{type(exc).__name__}: {exc}"
            time.sleep(1.5 * (attempt + 1))
    return url, last_err or "unreachable", url


def harvest_assets(dist: Path, base: str, limit: int) -> list[str]:
    """从本地 dist HTML 里收集站内资源引用 (assets/favicon), 用于线上可达性抽查."""
    urls: set[str] = set()
    for f in Path(dist).rglob("*.html"):
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in ATTR_RE.finditer(text):
            raw = m.group(1) or m.group(2) or ""
            cleaned = strip_query(html.unescape(raw.strip()))
            if cleaned.startswith("/") and not cleaned.startswith("//") \
                    and not cleaned.startswith(base) and cleaned != base.rstrip("/"):
                if len(off_base) < 40:
                    off_base.append(f"{rel} -> {raw} (根绝对路径未带 base {base})")
                continue
            site_path = to_site_path(raw, base)
            if site_path and not site_path.endswith("/"):
                urls.add(f"{SITE_ORIGIN}{site_path}")
        if len(urls) >= limit:
            break
    return sorted(urls)[:limit]


def crawl_internal_links(seed_urls: list[str], base: str, timeout: float) -> tuple[list[str], list[str]]:
    """抓种子页, 返回 (站内链接绝对 URL 集合, 错误列表).

    页面自报的 href/src 就是该页运行所需的站内资源 (assets/favicon/入口页), 直接拿线上
    HTML 抽取, 不依赖本地 dist —— 本地 dist 的 asset hash 只在与线上同一次构建时才对得上,
    拿本地清单去查线上会造出假死链 (实测 publish/web/dist 是旧构建, hash 与线上不一致).
    """
    found: set[str] = set()
    errors: list[str] = []
    for seed in seed_urls:
        try:
            req = urllib.request.Request(seed, headers={"User-Agent": "protreptic-quality-gate/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                html_text = resp.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{seed}: {type(exc).__name__}: {exc}")
            continue
        for m in ATTR_RE.finditer(html_text):
            raw = m.group(1) or m.group(2) or ""
            cleaned = html.unescape(raw.strip())
            if not is_internal(cleaned):
                continue
            if cleaned.startswith("/"):
                site_path = cleaned
            else:
                site_path = urllib.parse.urlparse(
                    urllib.parse.urljoin(seed, cleaned)
                ).path
            if site_path.startswith(base):
                found.add(f"{SITE_ORIGIN}{site_path}")
    return sorted(found), errors


def run_live(args: argparse.Namespace) -> int:
    base = args.base_url if args.base_url.endswith("/") else args.base_url + "/"
    parsed = urllib.parse.urlparse(base)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    path_base = parsed.path
    rep = Report(f"[live] {base}")

    routes_path = Path(args.routes).resolve()
    if not routes_path.is_file():
        print(f"输入错误: 路由清单不存在: {routes_path}", file=sys.stderr)
        return 2
    routes = load_routes(routes_path)

    urls: set[str] = set()
    for r in routes.get("routes", []):
        urls.add(r["canonical"])
    urls.add(base)

    # 线上 sitemap
    sm_url = args.sitemap_url or f"{base}sitemap.xml"
    try:
        req = urllib.request.Request(sm_url, headers={"User-Agent": "protreptic-quality-gate/1.0"})
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            xml = resp.read()
        root = ET.fromstring(xml)
        locs = [(el.text or "").strip() for el in root.iter(f"{{{SITEMAP_NS}}}loc")]
        rep.note(f"线上 sitemap: {sm_url} 读到 {len(locs)} 条 URL")
        urls.update(l for l in locs if l)
    except Exception as exc:  # noqa: BLE001
        rep.fail(f"sitemap 抓取/解析失败: {sm_url}: {type(exc).__name__}: {exc}")

    if args.crawl_sample:
        seeds = [base]
        for extra in ("figures/", "modes/", "templates/"):
            seeds.append(base + extra)
        rest = sorted(u for u in urls if u not in seeds and u.startswith(base))
        if rest:
            step = max(1, len(rest) // max(1, args.crawl_sample - len(seeds)))
            seeds.extend(rest[::step][: max(0, args.crawl_sample - len(seeds))])
        seeds = seeds[: args.crawl_sample]
        page_links, crawl_errors = crawl_internal_links(seeds, path_base, args.timeout)
        rep.note(f"页面内链接抽查: 抓 {len(seeds)} 页, 抽出站内引用 {len(page_links)} 条")
        for e in crawl_errors:
            rep.fail(f"种子页抓取失败: {e}")
        urls.update(page_links)

    if args.assets_from:
        assets = harvest_assets(Path(args.assets_from), path_base, args.max_links or 200)
        rep.note(f"站内静态资源抽查 {len(assets)} 条 (来自 {args.assets_from})")
        urls.update(assets)

    if args.break_link:
        fake = f"{base}{BREAK_TOKEN}/"
        rep.note(f"自检注入: {fake} (必然 404, 期望本检测 FAIL)")
        urls.add(fake)

    targets = sorted(urls)[: args.max_links] if args.max_links else sorted(urls)
    if args.max_links and len(urls) > args.max_links:
        rep.note(f"注意: 待检 {len(urls)} 条被 --max-links={args.max_links} 截断")

    unencoded = [u for u in targets if encode_url(u) != u]
    if unencoded:
        rep.note(f"待检集合里 {len(unencoded)} 条 URL 含未转义字符 (请求前已 %XX 转义, "
                 f"但上游仍应修): {unencoded[:3]}")
    probes = {encode_url(u): u for u in targets}

    dead: list[str] = []
    histogram: dict[str, int] = {}
    redirects = 0
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [pool.submit(http_probe, u, args.timeout, args.retries) for u in probes]
        for fut in concurrent.futures.as_completed(futures):
            probed, status, final = fut.result()
            url = probes.get(probed, probed)
            key = str(status)
            histogram[key] = histogram.get(key, 0) + 1
            if status != 200:
                dead.append(f"{status} <- {url}")
            elif encode_url(final) != probed:
                redirects += 1

    rep.checked = len(targets)
    rep.note(f"耗时 {time.time() - t0:.1f}s, 并发 {args.concurrency}, "
             f"状态码分布 {dict(sorted(histogram.items()))}, 重定向后 200 的 {redirects} 条")
    for d in dead:
        rep.fail(d)
    return rep.finish()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Phase30-C1 死链检测门")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("dist", help="对本地 dist 产物做静态断链检测")
    d.add_argument("--dist", default="web/dist")
    d.add_argument("--routes", default=DEFAULT_ROUTES)
    d.add_argument("--sitemap", default="web/dist/sitemap.xml")
    d.add_argument("--base", default=DEFAULT_BASE)
    d.add_argument("--break-link", action="store_true")
    d.set_defaults(func=run_dist)

    l = sub.add_parser("live", help="对线上站点做真实 HTTP 可达性检测")
    l.add_argument("--base-url", default=f"{SITE_ORIGIN}{DEFAULT_BASE}")
    l.add_argument("--routes", default=DEFAULT_ROUTES)
    l.add_argument("--sitemap-url", default=None)
    l.add_argument("--assets-from", default=None, help="本地 dist 目录, 用于抽取站内资源抽查")
    l.add_argument("--crawl-sample", type=int, default=6,
                   help="抓取线上页面并检查其自报的站内链接 (默认 6 页, 0=关闭)")
    l.add_argument("--max-links", type=int, default=0, help="0 = 不截断")
    l.add_argument("--concurrency", type=int, default=16)
    l.add_argument("--timeout", type=float, default=20.0)
    l.add_argument("--retries", type=int, default=2)
    l.add_argument("--break-link", action="store_true")
    l.set_defaults(func=run_live)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
