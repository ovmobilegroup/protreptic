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
  modes: 2798,
  /** 人物数 (meta.json counts.mode_by_figure_shards, 与 /figures 名录一致) */
  figures: 278,
  /** 首页 description (与 site_counts.description_text 同值) */
  description: "2798 条思维模式 × 278 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。",
  /** og:description / 页脚文案 (与 site_counts.og_description_text 同值) */
  ogDescription: "2798 条思维模式 × 278 位历史人物 · 中英双语",
} as const

export type SiteCounts = typeof SITE_COUNTS
