#!/usr/bin/env python3
"""prerender_routes.py -- Phase30-A0: SPA 路由预渲染, 静态路由壳 + 每路由 head.

问题, 实测:
    GitHub Pages 是纯静态托管. /protreptic/figures, /protreptic/minds/H-MO-001
    这类深链没有对应文件, Pages 只能回落到 404.html, 也就是 dist/index.html 的副本,
    于是页面能靠 JS 渲染出来, 但 HTTP 状态码是 404. 实测 2026-09-18:
        /protreptic/figures        -> 404
        /protreptic/modes          -> 404
        /protreptic/minds/H-MO-001 -> 404
        /protreptic/templates      -> 301 -> /protreptic/templates/ -> 404

方案:
    构建后为每个路由生成 <route>/index.html, 内容 = dist/index.html 加上该路由的
    title / description / canonical / og / JSON-LD. Pages 对目录请求会回落到目录下
    的 index.html, 因此深链由 404 变成 200; 未覆盖的路径仍然回落到 404.html 的
    SPA 外壳, 行为不变.

    本脚本负责 head (Phase30-A0); 关键路由的静态正文快照由 tools/prerender_body.py
    在 Phase30-A2 里补上, 见本文件 --body-persons / --no-body 参数. 快照写进
    <div id="app">, 无 JS 的 UA 也能读到正文; 有 JS 时由 web/src/main.ts 在挂载前
    清空容器, 因此不会出现两份正文并存, 也不需要 SSR / hydrate 那一套.

产物:
    web/dist/<route>/index.html            795 个路由目录, 默认
    docs/architecture/web_p0_routes.json   路由清单, 供 sitemap 生成器消费

用法:
    python3 tools/prerender_routes.py
    python3 tools/prerender_routes.py --base /
    python3 tools/prerender_routes.py --dry-run

退出码: 0 成功; 1 输入缺失 / 路由数为 0 / 写盘失败.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prerender_body import check_bodies, collect_bodies, inject_body, plain_text  # noqa: E402
DEFAULT_BASE = "/protreptic/"
SITE_ORIGIN = "https://ovmobilegroup.github.io"
SITE_NAME = "Protreptic 思想典藏"

TEMPLATE_IDS = ["longzhong", "baidi", "chibi", "beifa", "jieting", "yiling", "changban"]

STATIC_ROUTES = [
    ("daily", "每日一模式 - 今日与历史归档", "每天按「日期对模式总数取模」选出一条思维模式: 同一天重复打开结果一致, 可回看任意历史日期."),
    ("figures", "历史人物库 - 统一名录", "283 位历史人物 + 501 个现代场景, 统一检索入口."),
    ("modes", "思维模式库 - 2858 条可执行方法", "2858 条历史人物思维模式实例, 含定义, 操作步骤, 出处与原话."),
    ("templates", "复盘模板库 - 7 个历史案例工具", "把赤壁, 隆中对等 7 个历史经典案例转化为可直接套用的复盘模板."),
    ("concepts", "概念索引 - 跨人物思想连接", "按模式档案的 key_concepts 聚合: 概念出现在哪些历史人物身上, 落在哪几条模式里."),
    ("graph", "关系图谱 - 人物-模式-概念", "人物-模式-概念关系图谱: 本地力导向布局, 数据来自预计算图谱分片."),
    ("compare", "跨人物对比 - 思维模式并排对照", "选 2-4 位历史人物或思维模式, 并排对照定义, 步骤, 出处与领域分布; 地址栏带选中项, 可直接分享."),
    ("api", "API 文档", "Protreptic 静态数据与 API 说明."),
]

TITLE_RE = re.compile(r"<title>.*?</title>", re.S)
DESC_RE = re.compile(r'<meta name="description"\s*\n?\s*content="[^"]*"\s*/>', re.S)
OGT_RE = re.compile(r'<meta property="og:title" content="[^"]*"\s*/>')
OGD_RE = re.compile(r'<meta property="og:description" content="[^"]*"\s*/>')


def esc(text: str) -> str:
    return html.escape(text or "", quote=True)


def truncate(text: str, limit: int = 120) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[: limit - 1] + "..."


def md_title_desc(path: Path):
    """从模板 markdown 取标题, 首个 # 标题, 与描述, 其后首个非空段落."""
    title, desc = path.stem, ""
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("# "):
            title = s[2:].strip()
            for nxt in lines[i + 1:]:
                nxt = nxt.strip().strip(">").strip()
                if nxt and not nxt.startswith("#"):
                    desc = nxt
                    break
            break
    return title, truncate(desc)


def build_routes(dist: Path, base: str):
    unified_path = dist / "data" / "index.unified.json"
    if not unified_path.exists():
        sys.exit("[prerender] missing %s, run export_static_site.py + build_unified_index.py first" % unified_path)

    unified = json.loads(unified_path.read_text(encoding="utf-8"))
    items = unified["items"]
    routes = []

    for slug, title, desc in STATIC_ROUTES:
        routes.append({"path": slug, "title": title, "description": desc, "type": "static"})

    for item in items:
        code, name = item["code"], item.get("name") or item["code"]
        n = item.get("n_modes") or 0
        desc = truncate(item.get("description") or "")
        if item["type"] == "figure":
            routes.append({
                "path": "minds/%s" % code,
                "title": "%s - 思维模式档案 %d 条" % (name, n),
                "description": desc or "%s 的 %d 条思维模式档案, 含定义, 步骤, 出处与原话." % (name, n),
                "type": "person", "name": name, "code": code, "n_modes": n,
            })
        else:
            routes.append({
                "path": "figures/%s" % code,
                "title": "%s - 场景档案 %d 条模式" % (name, n),
                "description": desc or "场景 %s %s 关联的 %d 条思维模式." % (name, code, n),
                "type": "scenario", "name": name, "code": code, "n_modes": n,
            })

    tmpl_dir = dist / "templates"
    for tid in TEMPLATE_IDS:
        md = tmpl_dir / ("%s.md" % tid)
        if not md.exists():
            sys.exit("[prerender] missing template markdown: %s" % md)
        title, desc = md_title_desc(md)
        routes.append({"path": "templates/%s" % tid, "title": title,
                       "description": desc, "type": "template", "name": title})

    seen = set()
    for r in routes:
        if r["path"] in seen:
            sys.exit("[prerender] duplicate route: %s" % r["path"])
        seen.add(r["path"])
    return routes


def excluded_figure_codes(dist, unified_codes):
    """by-figure 分片存在但不在公开名录里的人物编码.

    已知 H-SX-001 被 tools/_quarantine.py 的 QUARANTINE 隔离（名录/每日/图谱三层共用）, 但
    tools/export_static_site.py 仍会把它的 by-figure 分片写进 data/. 本脚本按
    公开名录预渲染, 因此不为它生成路由, 它继续走 404 外壳. 这里把它报出来,
    供 sitemap 生成器与数据治理卡对齐.
    """
    bf = dist / "data" / "modes" / "by-figure"
    if not bf.is_dir():
        return []
    codes = {q.stem for q in bf.glob("*.json")}
    return sorted(codes - set(unified_codes))


def render_head(shell: str, route: dict, base: str) -> str:
    path = route["path"]
    url = "%s%s%s/" % (SITE_ORIGIN, base, path)
    full_title = "%s | %s" % (route["title"], SITE_NAME)
    desc = truncate(route.get("description") or "", 150)

    out = TITLE_RE.sub(lambda _: "<title>%s</title>" % esc(full_title), shell, count=1)
    out = DESC_RE.sub(lambda _: '<meta name="description" content="%s" />' % esc(desc), out, count=1)
    out = OGT_RE.sub(lambda _: '<meta property="og:title" content="%s" />' % esc(route["title"]), out, count=1)
    out = OGD_RE.sub(lambda _: '<meta property="og:description" content="%s" />' % esc(desc), out, count=1)

    ld = {
        "@context": "https://schema.org",
        "@type": "Person" if route["type"] == "person" else "CreativeWork",
        "name": route.get("name") or route["title"],
        "description": desc,
        "url": url,
        "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": "%s%s" % (SITE_ORIGIN, base)},
    }
    if route["type"] == "person":
        ld["identifier"] = route.get("code")
        ld["alternateName"] = route.get("code")
    elif route["type"] == "template":
        ld["@type"] = "Article"
        ld["headline"] = route.get("name") or route["title"]
    elif route["type"] == "scenario":
        ld["identifier"] = route.get("code")

    # 下面注入的 <script> 必须写成 <script ...></script>:
    # 自闭合 <script .../> 会被 HTML 解析器忽略 (script 是 raw text 元素), 它后面的标签
    # 全部被吞成脚本文本, 预渲染页面直接空白 —— web/index.html 上踩过一次 (Phase30-A3 修复).
    extra = (
            '\n    <link rel="canonical" href="%s" />' % esc(url)
            + '\n    <meta property="og:url" content="%s" />' % esc(url)
            + '\n    <script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False, separators=(",", ":"))
            + "\n  </head>"
        )
    if "</head>" not in out:
        sys.exit("[prerender] no </head> in index.html")
    return out.replace("</head>", extra, 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(REPO / "web" / "dist"))
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--routes-out", default=str(REPO / "docs" / "architecture" / "web_p0_routes.json"))
    ap.add_argument("--body-persons", default="40",
                    help="人物页正文快照覆盖数: N=模式数最多的前 N 名, all=全部人物页, 0=不生成")
    ap.add_argument("--body-max-modes", type=int, default=12,
                    help="人物页快照里最多列出的模式条数")
    ap.add_argument("--no-body", action="store_true",
                    help="只做 A0 的 head 预渲染, 不写正文快照")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    base = args.base if args.base.endswith("/") else args.base + "/"
    dist = Path(args.dist)
    shell_path = dist / "index.html"
    if not shell_path.exists():
        sys.exit("[prerender] missing %s, run npm run build first" % shell_path)
    shell = shell_path.read_text(encoding="utf-8")

    routes = build_routes(dist, base)
    if not routes:
        sys.exit("[prerender] zero routes, aborting")
    unified_codes = {r["code"] for r in routes if r["type"] == "person"}
    excluded = excluded_figure_codes(dist, unified_codes)
    bodies = {}
    if not args.no_body:
        persons = None if str(args.body_persons).strip().lower() == "all" else max(0, int(args.body_persons))
        bodies = collect_bodies(routes, dist, persons=persons, max_modes=args.body_max_modes)
    for route in routes:
        route["body"] = route["path"] in bodies
        route["body_text_chars"] = len(plain_text(bodies[route["path"]])) if route["body"] else 0
    print("[prerender] 正文快照 %d 条, 共 %.0f KB" % (len(bodies), sum(len(b.encode("utf-8")) for b in bodies.values()) / 1024))

    print("[prerender] base=%s routes=%d" % (base, len(routes)))
    if args.dry_run:
        print("[prerender] dry-run, nothing written")
        return 0

    total = 0
    for route in routes:
        body_html = bodies.get(route["path"])
        html_out = render_head(inject_body(shell, body_html) if body_html else shell, route, base)
        target = dist / route["path"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html_out, encoding="utf-8")
        total += len(html_out.encode("utf-8"))
        route["canonical"] = "%s%s%s/" % (SITE_ORIGIN, base, route["path"])

    shutil.copyfile(shell_path, dist / "404.html")

    by_type = {}
    for r in routes:
        by_type[r["type"]] = by_type.get(r["type"], 0) + 1

    out_path = Path(args.routes_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "schema": "protreptic.prerendered_routes/v1",
        "generated_by": "tools/prerender_routes.py",
        "base": base,
        "count": len(routes),
        "total_html_bytes": total,
        "counts_by_type": by_type,
        "body_count": len(bodies),
        "body_total_bytes": sum(len(b.encode("utf-8")) for b in bodies.values()),
        "body_routes": sorted(bodies),
        "excluded_figure_codes": excluded,
        "routes": sorted(routes, key=lambda r: r["path"]),
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    if excluded:
        print("[prerender] excluded figure codes (not in public register): %s" % ", ".join(excluded))
    # 写盘自检: 逐个路由确认 index.html 存在且带 canonical, 数量对得上才放行
    missing = []
    for route in routes:
        f = dist / route["path"] / "index.html"
        if not f.is_file() or 'rel="canonical"' not in f.read_text(encoding="utf-8"):
            missing.append(route["path"])
    if missing:
        sys.exit("[prerender] self-check failed for %d routes: %s" % (len(missing), missing[:5]))

    bad_body = check_bodies(dist, routes)
    if bad_body:
        sys.exit("[prerender] 正文快照自检失败 (%d): %s" % (len(bad_body), bad_body[:5]))

    print("[prerender] wrote %d index.html, total %.0f KB" % (len(routes), total / 1024))
    print("[prerender] route manifest -> %s" % out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
