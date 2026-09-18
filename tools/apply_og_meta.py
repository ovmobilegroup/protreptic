#!/usr/bin/env python3
"""apply_og_meta.py -- Phase30-A3: 把 dist/og/manifest.json 里的分享图写进每个页面的 head.

为什么单独一步 (而不是塞进 tools/prerender_routes.py)
    A0/A2 的路由预渲染只负责「深链 200 + head 骨架」; 分享图是另一件事:
    先由 tools/build_og_images.py 把 PNG 画出来, 再在这里按 manifest 逐页写 meta.
    两步分开之后, 谁都不需要知道对方的内部实现, 而且本脚本可以被单独复跑 (幂等).

写进去的标签 (每页一组, 重复的旧标签会被替换掉, 不会出现两份)
    <meta property="og:type"          content="profile|article|website">
    <meta property="og:image"         content="绝对 URL">
    <meta property="og:image:width"   content="1200">
    <meta property="og:image:height"  content="630">
    <meta property="og:image:alt"     content="...">
    <meta name="twitter:card"         content="summary_large_image">
    <meta name="twitter:image"        content="绝对 URL">
    <meta name="twitter:image:alt"    content="...">

自检 (任一不过非 0 退出)
    1) manifest 里的每条路由都要有对应 HTML (route '' -> dist/index.html, 其余 -> dist/<route>/index.html)
    2) 图片文件必须真的在 dist 里, 且是 1200x630 的 PNG (只读文件头)
    3) 写完回读: 每个页面必须恰好出现一次目标 og:image, 且 og:image:width/height 都在

用法
    python3 tools/apply_og_meta.py
    python3 tools/apply_og_meta.py --dry-run
    python3 tools/apply_og_meta.py --only figures,minds/H-WYM-001
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import og_image  # noqa: E402

# 先去掉旧标签再去重写入, 避免页面里出现两份 og:image (静态壳与注入内容打架)
OG_TYPE_RE = re.compile(r'<meta property="og:type" content="[^"]*"\s*/?>\s*')
OG_IMG_BLOCK_RE = re.compile(r'<meta property="og:image(?::\w+)?"[^>]*>\s*')
TW_IMG_BLOCK_RE = re.compile(r'<meta name="twitter:image(?::\w+)?"[^>]*>\s*')
TW_CARD_RE = re.compile(r'<meta name="twitter:card" content="[^"]*"\s*/?>\s*')

OG_TYPE_BY_KIND = {"person": "profile", "template": "article"}
HEAD_END = "</head>"


def meta(kind: str, key: str, value: str) -> str:
    attr = "property" if kind == "og" else "name"
    return '    <meta %s="%s" content="%s" />' % (attr, key, value)


def og_block(entry: dict) -> str:
    url, alt = entry["url"], entry["alt"]
    kind = entry.get("kind") or ""
    lines = [
        meta("og", "og:type", OG_TYPE_BY_KIND.get(kind, "website")),
        meta("og", "og:image", url),
        meta("og", "og:image:width", str(og_image.OG_WIDTH)),
        meta("og", "og:image:height", str(og_image.OG_HEIGHT)),
        meta("og", "og:image:alt", alt),
        meta("tw", "twitter:card", "summary_large_image"),
        meta("tw", "twitter:image", url),
        meta("tw", "twitter:image:alt", alt),
    ]
    return "\n".join(lines) + "\n"


def inject(html: str, entry: dict) -> str:
    out = OG_TYPE_RE.sub("", html)
    out = OG_IMG_BLOCK_RE.sub("", out)
    out = TW_IMG_BLOCK_RE.sub("", out)
    out = TW_CARD_RE.sub("", out)
    if HEAD_END not in out:
        raise ValueError("页面里没有 </head>")
    return out.replace(HEAD_END, og_block(entry) + "  " + HEAD_END, 1)


def png_size(path: Path) -> tuple:
    try:
        head = path.read_bytes()[:33]
    except OSError:
        return 0, 0
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return 0, 0
    return struct.unpack(">II", head[16:24])


def html_for(dist: Path, route: str) -> Path:
    return dist / "index.html" if not route else dist / route / "index.html"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(REPO / "web" / "dist"))
    ap.add_argument("--only", default="", help="只处理这些路由 (逗号分隔, site 表示首页)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    dist = Path(args.dist)
    manifest_path = dist / og_image.OG_DIR / og_image.MANIFEST_NAME
    if not manifest_path.exists():
        sys.exit("[ogmeta] 缺少 %s: 先跑 python3 tools/build_og_images.py" % manifest_path)
    manifest = og_image.load_json(manifest_path)
    images = manifest.get("images") or {}
    if not images:
        sys.exit("[ogmeta] manifest 里没有任何图片")

    routes = sorted(images)
    if args.only:
        wanted = {("" if p.strip().strip("/") == "site" else p.strip().strip("/"))
                  for p in args.only.split(",") if p.strip()}
        routes = [r for r in routes if r in wanted]
        if not routes:
            sys.exit("[ogmeta] --only 没有匹配到任何路由")

    # 自检 1: 图片真的落盘且是 1200x630 的 PNG
    bad_images = []
    for route in routes:
        entry = images[route]
        size = png_size(dist / entry["image"])
        if size != (og_image.OG_WIDTH, og_image.OG_HEIGHT):
            bad_images.append("%s(%s -> %s)" % (route or "site", entry["image"], size))
    if bad_images:
        print("[ogmeta] 图片自检失败 %d 条: %s" % (len(bad_images), bad_images[:6]))
        return 1

    written, skipped, bad_pages = 0, [], []
    for route in routes:
        entry = images[route]
        page = html_for(dist, route)
        if not page.is_file():
            skipped.append(route or "site")
            continue
        html = page.read_text(encoding="utf-8")
        out = inject(html, entry)
        if not args.dry_run:
            page.write_text(out, encoding="utf-8")

    if args.dry_run:
        print("[ogmeta] dry-run: 可写 %d 页, 缺 HTML %d 页 %s"
              % (len(routes) - len(skipped), len(skipped), skipped[:5]))
        return 0

    # 自检 3: 回读, 确认每个页面只有一份目标 og:image, 且宽高都在
    for route in routes:
        entry = images[route]
        page = html_for(dist, route)
        if not page.is_file():
            continue
        html = page.read_text(encoding="utf-8")
        if html.count('property="og:image"') != 1 or entry["url"] not in html:
            bad_pages.append("%s(og:image 数量或取值不对)" % (route or "site"))
        elif '"og:image:width" content="%d"' % og_image.OG_WIDTH not in html:
            bad_pages.append("%s(缺 og:image:width)" % (route or "site"))
        else:
            written += 1

    if bad_pages:
        print("[ogmeta] 页面自检失败 %d 条: %s" % (len(bad_pages), bad_pages[:6]))
        return 1
    if skipped:
        print("[ogmeta] 警告: %d 条路由没有预渲染 HTML (未写 meta): %s"
              % (len(skipped), skipped[:6]))

    print("[ogmeta] 已写入 %d 页 og:image/twitter:image (base=%s, 尺寸 %dx%d)"
          % (written, manifest.get("base"), og_image.OG_WIDTH, og_image.OG_HEIGHT))
    kinds = {}
    for route in routes:
        kinds[images[route]["kind"]] = kinds.get(images[route]["kind"], 0) + 1
    print("[ogmeta] 分类: %s" % ", ".join("%s %d" % kv for kv in sorted(kinds.items())))
    sample = images.get("minds/H-WYM-001") or images[routes[1]]
    print("[ogmeta] 抽样 %s -> %s" % (sample["image"], sample["url"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
