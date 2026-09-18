#!/usr/bin/env python3
"""build_sitemap.py -- Phase30-A1: 产出 sitemap.xml (robots.txt 在 web/public/, 静态).

为什么是两个数据源 (取并集, 按 URL 去重):

  * docs/architecture/web_p0_routes.json —— tools/prerender_routes.py 的产物, 记录
    **真实被预渲染成 <route>/index.html 的页面** (带尾斜杠的 canonical 绝对地址).
    这是"可索引页面"的事实清单, 因此是首选源, 直接遍历 routes[].canonical, 不自行拼 URL.
  * web/public/data/index.unified.json —— 公开名录 (人物 + 场景). 当路由清单缺失, 或
    比名录旧 (例如只跑本脚本, 没跑 prerender) 时, 用它补齐 /minds/{code}/ 与 /figures/{code}/.

  另外补两类清单里没有单列、但确实存在的页面:
  * 站点首页 <origin><base> = https://ovmobilegroup.github.io/protreptic/ (dist/index.html)
  * 模板 /templates/{id}/ —— 优先取路由清单, 清单缺失时发现 web/public/templates/*.md

产物 (两个都写, 保证 CI 与本地一致):
  web/public/sitemap.xml   提交进仓; npm run build 时 Vite 把 public/ 复制成 dist/sitemap.xml
  web/dist/sitemap.xml     若 dist 目录存在则再直接写一份. CI 在 prerender 之后调用本脚本,
                           因此 dist 里那一份用的是**刚生成的最新路由清单**.

lastmod 的取值是真实时间戳, 不编造: 优先取 web/public/data/meta.json 的 generated_at
(静态数据重生成时间, 全站内容均由该数据派生), 缺失则整个 sitemap 省略 lastmod.

自检 (任一失败 exit 1, 不放行):
  * 每个 URL 都以 <origin><base> 开头且带尾斜杠 (线上 /protreptic/figures 会 301 到 .../figures/)
  * 无重复 URL; 条目数 >= --min-entries (默认 1300)
  * 内存条目数 == 产出 XML 的 <url> 数, 且 XML 能被 xml.etree 解析
  * 写盘后逐个文件重新读回校验 (文件不存在 / 解析失败 / 条数不符 -> 失败)

用法:
    python3 tools/build_sitemap.py
    python3 tools/build_sitemap.py --dist web/dist --min-entries 1300
    python3 tools/build_sitemap.py --no-public          # 只更新 dist 那一份

退出码: 0 成功; 1 自检失败 / 输入缺失.
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

REPO = Path(__file__).resolve().parent.parent
SITE_ORIGIN = "https://ovmobilegroup.github.io"
DEFAULT_BASE = "/protreptic/"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

DEFAULT_ROUTES = REPO / "docs" / "architecture" / "web_p0_routes.json"
DEFAULT_UNIFIED = REPO / "web" / "public" / "data" / "index.unified.json"
DEFAULT_META = REPO / "web" / "public" / "data" / "meta.json"
PUBLIC_OUT = REPO / "web" / "public" / "sitemap.xml"
DIST_DIR = REPO / "web" / "dist"

# 首页与四个入口页 (路由清单缺失时的兜底; 清单存在时以其为准)
FALLBACK_STATIC = ["", "figures", "modes", "templates", "api"]

PRIORITY = {
    "root": "1.0",
    "static": "0.8",
    "person": "0.7",
    "template": "0.6",
    "scenario": "0.5",
}
API_PRIORITY = "0.3"


def truncate(text: str, limit: int = 200) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def norm_base(base: str) -> str:
    return base if base.endswith("/") else base + "/"


class Entry:
    __slots__ = ("url", "kind", "priority")

    def __init__(self, url: str, kind: str, priority: str) -> None:
        self.url = url
        self.kind = kind
        self.priority = priority


def load_manifest(path: Path, base: str, origin: str):
    """路由清单 -> [(url, type)]. 返回 (entries, note)."""
    if not path.is_file():
        return [], "路由清单不存在: %s" % path
    doc = json.loads(path.read_text(encoding="utf-8"))
    routes = doc.get("routes") or []
    out = []
    for r in routes:
        url = r.get("canonical")
        if not url:
            url = "%s%s%s/" % (origin, base, r.get("path", ""))
        out.append((url, r.get("type") or "static", r.get("path") or ""))
    note = "路由清单 %s: count=%s, counts_by_type=%s" % (
        path.relative_to(REPO), doc.get("count"), doc.get("counts_by_type"))
    return out, note


def load_unified(path: Path, base: str, origin: str):
    """公开名录 -> [(url, type, path)]. 命名固定, 不使用文件里的 href (它是死的 hash 字段)."""
    if not path.is_file():
        return [], "统一名录不存在: %s" % path
    doc = json.loads(path.read_text(encoding="utf-8"))
    items = doc.get("items") or []
    out = []
    for it in items:
        code = it.get("code")
        if not code:
            continue
        kind = "person" if it.get("type") == "figure" else "scenario"
        route_path = ("minds/%s" if kind == "person" else "figures/%s") % code
        out.append(("%s%s%s/" % (origin, base, route_path), kind, route_path))
    return out, "统一名录 %s: items=%d" % (path.relative_to(REPO), len(items))


def load_templates(fallback_dir: Path):
    ids = sorted(p.stem for p in fallback_dir.glob("*.md")) if fallback_dir.is_dir() else []
    return ids


def build_entries(args, base: str) -> tuple[list[Entry], list[str]]:
    origin = SITE_ORIGIN
    notes: list[str] = []
    by_url: dict[str, Entry] = {}

    def add(url: str, kind: str, path: str = "") -> None:
        if url in by_url:
            return
        prio = API_PRIORITY if path == "api" else PRIORITY.get(kind, "0.5")
        by_url[url] = Entry(url, kind, prio)

    # 1) 首页: dist/index.html 直接提供
    add("%s%s" % (origin, base), "root", "")

    # 2) 路由清单 (首选源, 直接消费 canonical)
    manifest, note = load_manifest(Path(args.routes), base, origin)
    notes.append(note)
    if manifest:
        for url, kind, path in manifest:
            add(url, kind, path)
    else:
        for slug in FALLBACK_STATIC:
            add("%s%s%s/" % (origin, base, slug), "static", slug)
        for tid in load_templates(REPO / "web" / "public" / "templates"):
            add("%s%stemplates/%s/" % (origin, base, tid), "template", "templates/" + tid)

    # 3) 统一名录 (并集补齐: 名录里新增、但清单还没重跑的人物/场景)
    unified, note = load_unified(Path(args.unified), base, origin)
    notes.append(note)
    for url, kind, path in unified:
        add(url, kind, path)

    # 4) 模板兜底 (清单里已经有的话会在上面被去重掉)
    for tid in load_templates(REPO / "web" / "public" / "templates"):
        add("%s%stemplates/%s/" % (origin, base, tid), "template", "templates/" + tid)

    entries = sorted(by_url.values(), key=lambda e: e.url)
    return entries, notes


def read_lastmod(meta_path: Path) -> str | None:
    if not meta_path.is_file():
        return None
    try:
        doc = json.loads(meta_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    stamp = doc.get("generated_at") or ""
    return stamp[:10] if len(stamp) >= 10 else None


def render_xml(entries: list[Entry], lastmod: str | None, base: str) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="%s">' % SITEMAP_NS]
    for e in entries:
        lines.append("  <url>")
        lines.append("    <loc>%s</loc>" % escape(e.url))
        if lastmod:
            lines.append("    <lastmod>%s</lastmod>" % lastmod)
        if e.url == "%s%s" % (SITE_ORIGIN, base):
            lines.append("    <changefreq>daily</changefreq>")
        lines.append("    <priority>%s</priority>" % e.priority)
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def write_and_verify(path: Path, xml: str, expect: int) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(xml, encoding="utf-8")
    if not path.is_file():
        print("::error::写盘后文件不存在: %s" % path)
        return 1
    back = path.read_text(encoding="utf-8")
    try:
        root = ET.fromstring(back)
    except ET.ParseError as exc:
        print("::error::%s 不是合法 XML: %s" % (path, exc))
        return 1
    got = len(root.findall("{%s}url" % SITEMAP_NS))
    if got != expect:
        print("::error::%s 条目数 %d != 期望 %d" % (path, got, expect))
        return 1
    print("[sitemap] %s  (%d 条, %.1f KB)" % (path, got, len(back.encode("utf-8")) / 1024))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Phase30-A1 sitemap.xml 生成器")
    ap.add_argument("--routes", default=str(DEFAULT_ROUTES), help="预渲染路由清单 JSON")
    ap.add_argument("--unified", default=str(DEFAULT_UNIFIED), help="统一名录 JSON")
    ap.add_argument("--meta", default=str(DEFAULT_META), help="静态数据 meta.json (取 lastmod)")
    ap.add_argument("--dist", default=str(DIST_DIR), help="SPA 产物目录 (存在则写 dist/sitemap.xml)")
    ap.add_argument("--public-out", default=str(PUBLIC_OUT))
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--min-entries", type=int, default=1300)
    ap.add_argument("--no-public", action="store_true", help="不写 web/public/sitemap.xml")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    base = norm_base(args.base)
    entries, notes = build_entries(args, base)
    for n in notes:
        print("[sitemap] %s" % n)
    print("[sitemap] entries=%d (root=1)" % len(entries))

    # 自检 1: URL 前缀与尾斜杠
    bad = [e.url for e in entries if not e.url.startswith(SITE_ORIGIN + base) or not e.url.endswith("/")]
    if bad:
        print("::error::%d 条 URL 前缀或尾斜杠不合法, 例: %s" % (len(bad), bad[:3]))
        return 1
    kinds: dict[str, int] = {}
    for e in entries:
        kinds[e.kind] = kinds.get(e.kind, 0) + 1
    print("[sitemap] by kind: %s" % json.dumps(kinds, ensure_ascii=False, sort_keys=True))

    # 自检 2: 条目数下限 (发布仓基线 1350; 工作区本地数据较旧, 但并集仍应 >= 1300)
    if len(entries) < args.min_entries:
        print("::error::条目数 %d < 下限 %d (--min-entries)" % (len(entries), args.min_entries))
        return 1

    lastmod = read_lastmod(Path(args.meta))
    if lastmod is None:
        print("[sitemap] 无 meta.json generated_at, 省略 lastmod")
    xml = render_xml(entries, lastmod, base)

    if args.dry_run:
        print("[sitemap] dry-run, 未写盘")
        return 0

    rc = 0
    if not args.no_public:
        rc |= write_and_verify(Path(args.public_out), xml, len(entries))
    dist = Path(args.dist)
    if dist.is_dir():
        rc |= write_and_verify(dist / "sitemap.xml", xml, len(entries))
    else:
        print("[sitemap] dist 目录不存在 (%s), 跳过; npm run build 会从 public/ 复制" % dist)
    if rc:
        return 1
    print("[sitemap] OK: %d 条, robots.txt -> %srobots.txt" % (len(entries), SITE_ORIGIN + base))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
