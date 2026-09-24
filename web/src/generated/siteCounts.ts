/**
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
  modes: 3241,
  /** 人物数 (meta.json counts.mode_by_figure_shards, 与 /figures 名录一致) */
  figures: 320,
  /** 首页 description (与 site_counts.description_text 同值) */
  description: "3241 条思维模式 × 320 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。",
  /** og:description / 页脚文案 (与 site_counts.og_description_text 同值) */
  ogDescription: "3241 条思维模式 × 320 位历史人物 · 中英双语",
  /**
   * 可信度四态 (meta.json counts.verification) —— Phase38-Y3 统计页 /credibility 与卡片徽章
   * CredibilityBadge.vue 的唯一取数入口. 别在任何组件里手写这四个数字.
   *   published = 站上打得开的模式摘要口径 (counts.verification.published)
   *   all       = 源库口径 (含隔离记录), 只用于如实交代两者差别, 不冒充发布数据
   */
  verification: {
    published: { verified: 1019, pending: 1845, suspect: 37, unverifiable: 340 },
    publishedTotal: 3241,
    all: { verified: 1019, pending: 1877, suspect: 54, unverifiable: 351 },
    allTotal: 3301,
    quarantinedTotal: 60,
    /** 源库去重后的模式记录数 (counts.mode_summaries); 抽查不到时为 null, 不编数字 */
    sourceTotal: 3301,
  },
  /**
   * 可点链接覆盖率 (meta.json counts.citation_links) —— 统计页照实公布, 不声称全链.
   * citations* 是去重级 (同一本书只算一次), segments* 是出现级 (每条出处里的每个分段).
   */
  citationLinks: {
    modesWithCitations: 2509,
    modesWithLink: 1046,
    citations: 4504,
    citationsLinked: 1301,
    citationsRegisteredUnlinkable: 941,
    citationsUnresolved: 2262,
    segments: 4566,
    segmentsLinked: 1320,
  },
} as const

export type SiteCounts = typeof SITE_COUNTS
