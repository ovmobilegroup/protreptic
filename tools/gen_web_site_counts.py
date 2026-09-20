#!/usr/bin/env python3
"""gen_web_site_counts.py - 把站点门面计数注入 SPA 源码 (Phase35-V1FIX).

为什么需要它 (真实事故, 别重犯)
    "N 条思维模式 x M 位历史人物" 这句话在站点上有两类表面:
      * 静态表面 (index.html 的 meta, 两份 PWA manifest) -- tools/apply_site_counts.py
        在**构建之后**覆写, 取数走 tools/site_counts.py, 本来就是同源;
      * SPA 运行时表面 (useSeo.ts 的 SEO_DEFAULT_DESCRIPTION, App.vue 页脚, ApiDocsView,
        FiguresView 等) -- 它们**编译进 dist/assets/*.js**, 构建之后改不了,
        于是各自写死了一个数字. 数据一变 (例: 隔离 5 个伪人物, 60 条模式) 静态表面跟着
        走, 运行时表面不动, apply_site_counts 的交叉校验 ("dist/assets/*.js 里必须能找到
        同一句 target") 就失败 -> Pages 构建失败 -> 部署跳过 -> **线上照旧**.
        V1 (d8c809c) 线上没生效, 根因就是这条.

做法 (根治: 让运行时表面也吃同一口数据)
    本脚本在 npm run build **之前**运行, 读部署产物的 data/meta.json (与
    tools/site_counts.py 同一个取数入口, 同一套文案模板), 生成
    web/src/generated/siteCounts.ts -- 一个只含**字面量**的 TS 模块:
        SITE_COUNTS.modes / figures / description / ogDescription
    SPA 侧只 import 它, 不许再写数字. 因为字符串是字面量, 打包后仍**原样**出现在
    dist/assets/*.js 里, apply_site_counts 的字面量交叉校验因此成立.

    Phase38-Y3 起同一个文件还带 **可信度四态** SITE_COUNTS.verification
    (meta.json counts.verification 的 published / all 两个口径 + quarantinedTotal),
    供 /credibility 统计页与 CredibilityBadge.vue 取数; 取数仍走 tools/site_counts.py 的
    load_verification() (缺 counts.verification 直接非 0 退出, 不静默生成一份假统计).

    生成物入库 (web/src/generated/siteCounts.ts 提交进仓库): 干净 checkout 里
    vue-tsc / Docker 构建 (无数据分片) 也拿得到类型与一份最近口径的兜底值. 真正的
    口径正确性由 apply_site_counts 在 Pages 流水线里对着 meta.json 逐字节卡住.

用法
    python3 tools/gen_web_site_counts.py                  # 读 web/public/data/meta.json
    python3 tools/gen_web_site_counts.py --data-dir web/dist/data
    python3 tools/gen_web_site_counts.py --check          # 只校验, 不写 (自检用)

退出码: 0 成功/已最新; 1 数据缺失或 --check 发现生成物过期.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:  # python3 tools/gen_web_site_counts.py: sys.path[0] = tools/
    import site_counts
except ImportError:  # 仓库根在 sys.path 时
    from tools import site_counts

REPO = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO / "web" / "src" / "generated" / "siteCounts.ts"

HEADER = """/**
 * siteCounts.ts - SPA 运行时侧的门面计数.
 *
 * 【生成物, 请勿手改】由 tools/gen_web_site_counts.py 在 npm run build 之前生成,
 * 取数与文案模板一律走 tools/site_counts.py (唯一来源 = 部署产物 data/meta.json 的
 * counts.mode_summaries_published / counts.mode_by_figure_shards).
 *
 * 为什么要有这个文件: SPA 的文案会被编译进 dist/assets/*.js, 构建之后改不了;
 * 谁在这里写死数字, 谁就会在下一次数据变更时和静态 head 分叉, 让 Pages 部署失败
 * (Phase35-V1FIX 的真实事故). 任何地方要显示站点规模, import 本模块, 别写字面数字.
 *
 * 重新生成: python3 tools/gen_web_site_counts.py
 */
export const SITE_COUNTS = {
  /** 站点发布口径的模式摘要条数 (meta.json counts.mode_summaries_published) */
  modes: %(modes)d,
  /** 人物数 (meta.json counts.mode_by_figure_shards, 与 /figures 名录一致) */
  figures: %(figures)d,
  /** 首页 description (与 site_counts.description_text 同值) */
  description: %(description)s,
  /** og:description / 页脚文案 (与 site_counts.og_description_text 同值) */
  ogDescription: %(ogDescription)s,
  /**
   * 可信度四态 (meta.json counts.verification) —— Phase38-Y3 统计页 /credibility 与卡片徽章
   * CredibilityBadge.vue 的唯一取数入口. 别在任何组件里手写这四个数字.
   *   published = 站上打得开的模式摘要口径 (counts.verification.published)
   *   all       = 源库口径 (含隔离记录), 只用于如实交代两者差别, 不冒充发布数据
   */
  verification: {
    published: { verified: %(v_verified)d, pending: %(v_pending)d, suspect: %(v_suspect)d, unverifiable: %(v_unverifiable)d },
    publishedTotal: %(v_published_total)d,
    all: { verified: %(a_verified)d, pending: %(a_pending)d, suspect: %(a_suspect)d, unverifiable: %(a_unverifiable)d },
    allTotal: %(a_total)d,
    quarantinedTotal: %(quarantined)d,
    /** 源库去重后的模式记录数 (counts.mode_summaries); 抽查不到时为 null, 不编数字 */
    sourceTotal: %(source_total)s,
  },
  /**
   * 可点链接覆盖率 (meta.json counts.citation_links) —— 统计页照实公布, 不声称全链.
   * citations* 是去重级 (同一本书只算一次), segments* 是出现级 (每条出处里的每个分段).
   */
  citationLinks: {
    modesWithCitations: %(cl_modes_with_citations)d,
    modesWithLink: %(cl_modes_with_link)d,
    citations: %(cl_citations)d,
    citationsLinked: %(cl_citations_linked)d,
    citationsRegisteredUnlinkable: %(cl_unlinkable)d,
    citationsUnresolved: %(cl_unresolved)d,
    segments: %(cl_segments)d,
    segmentsLinked: %(cl_segments_linked)d,
  },
} as const

export type SiteCounts = typeof SITE_COUNTS
"""


def resolve_data_dir(explicit):
    if explicit:
        d = Path(explicit)
        if not d.is_absolute():
            d = REPO / d
        return d
    for candidate in (REPO / "web" / "public" / "data", REPO / "web" / "dist" / "data"):
        if (candidate / "meta.json").is_file():
            return candidate
    return REPO / "web" / "public" / "data"


def render(modes, figures, verification, citation_links):
    v, a = verification["published"], verification["all"]
    return HEADER % {
        "modes": modes,
        "figures": figures,
        "v_verified": v["verified"],
        "v_pending": v["pending"],
        "v_suspect": v["suspect"],
        "v_unverifiable": v["unverifiable"],
        "v_published_total": verification["published_total"],
        "a_verified": a["verified"],
        "a_pending": a["pending"],
        "a_suspect": a["suspect"],
        "a_unverifiable": a["unverifiable"],
        "a_total": verification["all_total"],
        "quarantined": verification["quarantined_total"],
        "source_total": json.dumps(verification["mode_summaries"]) if verification.get("mode_summaries") is not None else "null",
        "cl_modes_with_citations": citation_links["modes_with_citations"],
        "cl_modes_with_link": citation_links["modes_with_link"],
        "cl_citations": citation_links["citations"],
        "cl_citations_linked": citation_links["citations_linked"],
        "cl_unlinkable": citation_links["citations_registered_unlinkable"],
        "cl_unresolved": citation_links["citations_unresolved"],
        "cl_segments": citation_links["segments"],
        "cl_segments_linked": citation_links["segments_linked"],
        # json.dumps 产出的双引号字面量与 TS 字符串语法一致, 且保证转义安全
        "description": json.dumps(site_counts.description_text(modes, figures), ensure_ascii=False),
        "ogDescription": json.dumps(site_counts.og_description_text(modes, figures), ensure_ascii=False),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="生成 SPA 侧门面计数模块 (唯一取数 = data/meta.json)")
    ap.add_argument("--data-dir", default=None, help="默认 web/public/data (回落 web/dist/data)")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--check", action="store_true", help="只校验生成物是否为当前口径")
    args = ap.parse_args(argv)

    data_dir = resolve_data_dir(args.data_dir)
    modes, figures = site_counts.load_counts(data_dir)  # 缺 meta.json 会非 0 退出
    verification = site_counts.load_verification(data_dir)  # 缺 counts.verification 同样非 0 退出
    citation_links = site_counts.load_citation_links(data_dir)  # 缺 counts.citation_links 亦然
    want = render(modes, figures, verification, citation_links)

    out = Path(args.out)
    if not out.is_absolute():
        out = REPO / out
    cur = out.read_text(encoding="utf-8") if out.is_file() else None

    if args.check:
        if cur != want:
            print("[counts] %s 与 %s/meta.json (%d x %d) 不一致: "
                  "跑 python3 tools/gen_web_site_counts.py 重新生成" % (out, data_dir, modes, figures))
            return 1
        print("[counts] %s 已是当前口径 (%d x %d)" % (out, modes, figures))
        return 0

    if cur == want:
        print("[counts] %s 已最新 (%d x %d), 未改动" % (out, modes, figures))
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(want, encoding="utf-8")
    back = out.read_text(encoding="utf-8")
    for needle in (site_counts.description_text(modes, figures),
                   site_counts.og_description_text(modes, figures)):
        if needle not in back:
            site_counts.fail("回读失败: 生成的 %s 里找不到 %r" % (out, needle))
    print("[counts] 已写 %s: %d 条模式 x %d 位人物 (来源 %s/meta.json)"
          % (out, modes, figures, data_dir))
    v = verification["published"]
    print("[counts] 可信度四态 (发布口径 %d): 已核验 %d / 待核验 %d / 存疑 %d / 一手材料 %d"
          % (verification["published_total"], v["verified"], v["pending"], v["suspect"], v["unverifiable"]))
    print("[counts] 可点链接覆盖率: 去重级 %d/%d, 出现级 %d/%d, 带引文模式 %d/%d 至少一个可点"
          % (citation_links["citations_linked"], citation_links["citations"],
             citation_links["segments_linked"], citation_links["segments"],
             citation_links["modes_with_link"], citation_links["modes_with_citations"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
