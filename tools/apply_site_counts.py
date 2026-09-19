#!/usr/bin/env python3
"""apply_site_counts.py -- 站点门面计数收口（Phase32-F2 / Phase33-L1 / Phase34-L1B）。

问题（真实事故，别重犯）
    「N 条思维模式 × M 位历史人物」这句话被多个表面复用，每个表面各自写死 / 各自读
    meta.json，于是每加一个表面就漏一次：
      * web/index.html 的 <meta>：R8R9 清了 web/src，漏了这里（首页 head 一直在说谎）；
      * web/public/manifest*.webmanifest：Phase33-L1 漏了 web/public/**（Vite 原样拷进 dist，
        线上 /manifest.webmanifest 可直取，QA3 终审实测仍是 2858 → L1 FAIL）；
      * docs/02-tools/figure_library.md：docs 站产品页，L1 只扫了 web/src + docs/index.md。

做法
    取数一律走共享模块 **tools/site_counts.py**（唯一来源 = 部署产物 data/meta.json 的
    counts.mode_summaries_published / counts.mode_by_figure_shards）。本脚本只负责
    「按顺序调用它 + 自检」，自己不拼文案、不读 meta.json 的键：
      1) dist/index.html 的 description / og:description 覆写为站点口径；
      2) 两份 PWA manifest 的 description 收口 —— **源（web/public）+ 产物（dist）一起改**，
         这样哪怕只跑 npm run build 也不会把旧口径带上线；
      3) 全量扫描 dist/**（部署产物，不是源码枚举）：任何「N 条思维模式」「N 位历史人物」
         必须等于本站口径；html/manifest/txt/xml/svg 里不允许出现旧口径裸数字；
      4) docs 站产品门面页（docs/index.md + docs/02-tools/**）同一把尺 —— 其余 docs 是
         历时报告/研究记录，允许保留当时的实测数字（QA3 已认可该处置）。

    口径纪律（Phase33-L1）
        条数 = counts.mode_summaries_published（真正发布出去、站上打得开的模式摘要条数）；
        不是 modes_raw 的源记录数，也不是含 10 条隔离伪造模式（H-SX-001 M393-M402）的
        mode_summaries。哪里再写死这两个旧数字都是回归。

运行时机
    必须在 prerender_routes.py 与 apply_og_meta.py 之后（这两步会重写 dist 里的 head），
    在 build_sw.py 之前（sw.js 的预缓存清单里含两份 manifest）。

自检（任一不过非 0 退出）
    1) dist/data/meta.json 存在且 counts 齐全（由 site_counts.load_counts 校验）
    2) dist/index.html 里两条 meta 各恰好一份，写完回读必须等于目标串
    3) 目标串必须能在 dist/assets/*.js 里找到（SPA 运行时用的是同一句）
    4) 两份 manifest 写完回读 = 目标串，且 description 以外的键一个字节都没动
    5) dist/** 全量扫描零违规（条数 / 人物数 / 旧口径裸数字）
    6) docs 产品门面页零违规

用法
    python3 tools/apply_site_counts.py                    # 默认 web/dist + web/public
    python3 tools/apply_site_counts.py --dist /tmp/dist    # 私有副本，验证用
    python3 tools/apply_site_counts.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:  # 仓库根在 sys.path 时（import 场景）
    from tools import site_counts
except ImportError:  # python3 tools/apply_site_counts.py：sys.path[0] = tools/
    import site_counts

REPO = Path(__file__).resolve().parent.parent

# 与 prerender_routes.py 的 DESC_RE / OGD_RE 同形：网页里这两条 meta 可能跨行
DESC_RE = re.compile(r'<meta name="description"\s*\n?\s*content="[^"]*"\s*/>')
OGD_RE = re.compile(r'<meta property="og:description" content="[^"]*"\s*/>')


def fail(msg: str) -> None:
    site_counts.fail(msg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(REPO / "web" / "dist"))
    ap.add_argument("--public", default=str(REPO / "web" / "public"))
    ap.add_argument("--docs", default=str(REPO / "docs"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    dist = Path(args.dist)
    index_path = dist / "index.html"
    if not index_path.is_file():
        fail("缺少 %s：先跑 cd web && VITE_DATA_MODE=static npm run build" % index_path)

    # 唯一取数入口：共享模块读 dist/data/meta.json
    modes, figures = site_counts.load_counts(dist / "data")
    want_desc = site_counts.description_text(modes, figures)
    want_ogd = site_counts.og_description_text(modes, figures)

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
        print("[counts] dry-run: manifest description=%s" % site_counts.manifest_description_text(modes, figures))
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

    # 两份 PWA manifest：源 + 产物一起收口（走的还是共享模块）
    for p, changed, old, new in site_counts.sync_manifests(dist, args.public, modes, figures):
        print("[counts] manifest %s: %s -> %s" % ("更新" if changed else "已一致", p, new))

    # 硬门 1：部署产物全量扫描（dist/**，不是源码枚举）
    checked, violations = site_counts.scan_display_surfaces(dist, modes, figures)
    if violations:
        for rel, kind, hit in violations:
            print("    [%s] %s -> %s" % (kind, rel, hit))
        fail("dist 全量扫描发现 %d 条第二种口径（口径 %d 条 × %d 位，扫描 %d 个文件）"
             % (len(violations), modes, figures, checked))

    # 硬门 2：docs 站产品门面页（历史报告页不在此列，允许保留当时实测数字）
    n_docs, doc_violations = site_counts.scan_product_docs(args.docs, modes, figures)
    if doc_violations:
        for rel, kind, hit in doc_violations:
            print("    [docs:%s] %s -> %s" % (kind, rel, hit))
        fail("docs 产品门面页出现第二种口径: %d 条" % len(doc_violations))

    print("[counts] 收口完成: %d 条模式 × %d 位人物 (来源 %s)" % (modes, figures, dist / "data" / "meta.json"))
    print("[counts] dist 扫描 %d 个文件零违规；docs 产品门面页 %d 个零违规" % (checked, n_docs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
