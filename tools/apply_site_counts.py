#!/usr/bin/env python3
"""apply_site_counts.py -- 首页 head 的"条数 × 人物数"口径收口（Phase32-F2）。

问题（真实事故，别重犯）
    web/index.html 把计数写死在 <meta name="description"> 与 <meta property="og:description"> 里。
    R8R9 清了 web/src 的硬编码，漏了 index.html；而首页不在 tools/prerender_routes.py 的
    STATIC_ROUTES 里（首页就是 dist/index.html 本身，没有 <route>/index.html），
    prerender 也不会覆写它 —— 线上首页的 head 因此一直写着 2868 条 / 284 位（实测）。

做法
    单一来源 = dist/data/meta.json（tools/export_static_site.py 的产物）：
        条数    counts.mode_summaries         （与站内文案 / useSeo.ts 同口径：源去重后的条数）
        人物数  counts.mode_by_figure_shards  （by-figure 分片数 = 人物数）
    文案模板与 web/src/composables/useSeo.ts 的 SEO_DEFAULT_DESCRIPTION 同构 ——
    同一个 URL 的静态 head 与 SPA 运行时 head 必须是同一句话，否则就是两份内容打架。

运行时机
    必须在 prerender_routes.py 与 apply_og_meta.py 之后（这两步会重写 dist 里的 head）。

自检（任一不过非 0 退出）
    1) dist/data/meta.json 存在且 counts 齐全
    2) dist/index.html 里两条 meta 各恰好一份，写完回读必须等于目标串
    3) 目标串必须能在 dist/assets/*.js 里找到（SPA 运行时用的是同一句，
       用计数的字符串做交叉校验；找不到说明两边文案已经分叉）
    4) --dist 指向的页面里不允许残留旧口径的 meta（"…× 284 位历史人物"）
    5) 若页面里还有别的「N 条思维模式」（如 og:image:alt —— 由 tools/og_image.py 用
       modes_raw=2868 生成，与站点文案的 2858 口径不同）只提示不拦，见 Phase32-F2 遗留项

用法
    python3 tools/apply_site_counts.py                    # 默认 web/dist
    python3 tools/apply_site_counts.py --dist /tmp/dist    # 私有副本，验证用
    python3 tools/apply_site_counts.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# 与 prerender_routes.py 的 DESC_RE / OGD_RE 同形：网页里这两条 meta 可能跨行
DESC_RE = re.compile(r'<meta name="description"\s*\n?\s*content="[^"]*"\s*/>')
OGD_RE = re.compile(r'<meta property="og:description" content="[^"]*"\s*/>')

# 旧 meta 的原样文本：命中即说明这两条 meta 没被覆写干净（2868=源原始条数，284=隔离前的分片数）
STALE_META_MARKERS = (
    "2868 条思维模式 × 284 位历史人物",
    "2858 条思维模式 × 284 位历史人物",
)
# 页面里任何「N 条思维模式」：站点文案口径之外的值只提示（og:image:alt 走 modes_raw）
MODES_RE = re.compile(r"(\d{3,5}) 条思维模式")


def desc_text(modes: int, figures: int) -> str:
    return "%d 条思维模式 × %d 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。" % (modes, figures)


def og_desc_text(modes: int, figures: int) -> str:
    return "%d 条思维模式 × %d 位历史人物 · 中英双语" % (modes, figures)


def fail(msg: str) -> None:
    print("[counts] %s" % msg)
    raise SystemExit(1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(REPO / "web" / "dist"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    dist = Path(args.dist)
    meta_path = dist / "data" / "meta.json"
    index_path = dist / "index.html"
    if not meta_path.is_file():
        fail("缺少 %s：先跑 tools/export_static_site.py" % meta_path)
    if not index_path.is_file():
        fail("缺少 %s：先跑 cd web && VITE_DATA_MODE=static npm run build" % index_path)

    counts = json.loads(meta_path.read_text(encoding="utf-8")).get("counts") or {}
    for key in ("mode_summaries", "mode_by_figure_shards"):
        if not isinstance(counts.get(key), int):
            fail("meta.json 的 counts.%s 不是整数: %r" % (key, counts.get(key)))
    modes, figures = counts["mode_summaries"], counts["mode_by_figure_shards"]

    want_desc = desc_text(modes, figures)
    want_ogd = og_desc_text(modes, figures)

    html = index_path.read_text(encoding="utf-8")
    for label, rx in (("description", DESC_RE), ("og:description", OGD_RE)):
        n = len(rx.findall(html))
        if n != 1:
            fail("dist/index.html 里 %s 有 %d 份（应为 1）" % (label, n))

    out = DESC_RE.sub(lambda _: '<meta name="description" content="%s" />' % want_desc, html, count=1)
    out = OGD_RE.sub(lambda _: '<meta property="og:description" content="%s" />' % want_ogd, out, count=1)

    if args.dry_run:
        print("[counts] dry-run: 目标 description=%s" % want_desc)
        print("[counts] dry-run: 目标 og:description=%s" % want_ogd)
        return 0

    if out != html:
        index_path.write_text(out, encoding="utf-8")

    # 回读自检：两条 meta 必须等于目标串
    back = index_path.read_text(encoding="utf-8")
    for label, want, rx in (("description", want_desc, DESC_RE), ("og:description", want_ogd, OGD_RE)):
        got = rx.findall(back)
        if len(got) != 1 or want not in got[0]:
            fail("回读失败 %s: %s" % (label, got[:1]))

    # 交叉校验：SPA 运行时（打包后的 JS）里必须有同一句话
    assets = sorted((dist / "assets").glob("*.js")) if (dist / "assets").is_dir() else []
    if not assets:
        fail("dist/assets 里没有 *.js —— 构建产物不完整")
    bundle = "".join(a.read_text(encoding="utf-8", errors="ignore") for a in assets)
    for label, want in (("description", want_desc), ("og:description", want_ogd)):
        if want not in bundle:
            fail("dist/assets/*.js 里找不到 %s 目标串 %r：静态 head 与 SPA 运行时文案已分叉"
                 "（见 web/src/composables/useSeo.ts）" % (label, want))

    stale = [m for m in STALE_META_MARKERS if m in back]
    if stale:
        fail("dist/index.html 的 meta 仍残留旧口径: %s" % stale)

    # 软提示：页面里别的计数口径（og:image:alt 来自 tools/og_image.py 的 modes_raw）
    other_modes = sorted({m for m in MODES_RE.findall(back) if m != str(modes)})
    if other_modes:
        print("[counts] 提示: dist/index.html 里还有其它口径的条数 %s（站点文案口径 %d，"
              "og:image:alt 由 tools/og_image.py 取 meta.json 的 modes_raw 生成）"
              % (other_modes, modes))

    print("[counts] 首页计数已收口: %d 条模式 × %d 位人物 (来源 %s)" % (modes, figures, meta_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
