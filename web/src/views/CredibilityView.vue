<script setup lang="ts">
/**
 * 可信度统计页（Phase38-Y3）—— /credibility
 *
 * 站点对外的核心承诺是「每条都有出处」。这一页把承诺变成**可核对的数字**：
 * 已核验 / 待核验 / 存疑 / 一手材料 四态如实公布，空态（0）也照实显示，不做美化。
 *
 * 取数纪律（唯一来源 = 部署产物 data/meta.json 的 counts.verification）：
 *   * SPA 侧读 web/src/generated/siteCounts.ts —— 由 tools/gen_web_site_counts.py 在
 *     npm run build **之前**从 meta.json 生成（生成物入库，构建后改不了）；
 *   * 静态 head（预渲染的 /credibility/index.html）由 tools/prerender_routes.py 用同一份
 *     meta.json 现算（tools/site_counts.py 的 credibility_*_text）；
 *   * 本组件**不 fetch、不写死**任何数字：想让这里显示别的数，只能改 meta.json 后重新构建。
 *
 * 诚实边界（写在页面里，不藏在报告里）：
 *   * 四态是**核验状态**，不是「引文已逐字比对原文」；D4 引文比对 / D5 时间线机检尚未接入；
 *   * 可点链接覆盖率远未到 100%，页面照实给出比例，不声称「全部可点」；
 *   * 源库口径（含隔离记录）与发布口径的差别一并列出，隔离记录不进公开产物。
 */
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'
import CredibilityBadge from '../components/CredibilityBadge.vue'
import { SITE_COUNTS } from '../generated/siteCounts'

const { t } = useI18n()

type FourStates = { verified: number; pending: number; suspect: number; unverifiable: number }
type VerificationCounts = {
  published: FourStates
  publishedTotal: number
  all: FourStates
  allTotal: number
  quarantinedTotal: number
  sourceTotal: number | null
}
type CitationLinkCounts = {
  modesWithCitations: number
  modesWithLink: number
  citations: number
  citationsLinked: number
  citationsRegisteredUnlinkable: number
  citationsUnresolved: number
  segments: number
  segmentsLinked: number
}

// siteCounts.ts 是 `as const` 的字面量类型：这里显式放宽成 number，才能对空态（0）做运行时判断
// —— 生成物里的数字随 meta.json 变，'911 === 0' 这类比较不能被类型系统提前判死。
const v = SITE_COUNTS.verification as VerificationCounts
const links = SITE_COUNTS.citationLinks as CitationLinkCounts

/** 四态卡片：文案与符号与 CredibilityBadge.vue 一致（徽章组件本身负责渲染标记） */
const cards = computed(() => [
  {
    status: 'verified',
    count: v.published.verified,
    zh: '出处可达，且构建期解析出可点链接',
    en: 'Source reachable, with a clickable link resolved at build time',
  },
  {
    status: 'pending',
    count: v.published.pending,
    zh: '尚未核验（schema 缺省态）',
    en: 'Not yet checked (schema default)',
  },
  {
    status: 'suspect',
    count: v.published.suspect,
    zh: '命中缺陷规则，待复核 —— 显眼标注，不美化',
    en: 'Matched a defect rule, pending review — flagged, never smoothed over',
  },
  {
    status: 'unverifiable',
    count: v.published.unverifiable,
    zh: '口述 / 信札等本质不可链接，诚实标注而非硬造链接',
    en: 'Not linkable by nature (oral accounts, letters) — labelled, never faked',
  },
])

const pct = (n: number) => (v.publishedTotal > 0 ? (n / v.publishedTotal) * 100 : 0)

const pctText = (n: number) => {
  const p = pct(n)
  return p > 0 && p < 0.1 ? '<0.1%' : p.toFixed(1) + '%'
}

const citePctText = computed(() =>
  links.citations > 0 ? ((links.citationsLinked / links.citations) * 100).toFixed(1) + '%' : '—'
)

const metaHref = `${import.meta.env.BASE_URL || '/'}data/meta.json`
</script>

<template>
  <div class="pt-container pb-20 pt-8">
    <header class="pt-panel relative mb-8 overflow-hidden p-7">
      <div aria-hidden="true"
           class="pointer-events-none absolute -top-24 right-0 h-64 w-64 rounded-full bg-jade-400/10 blur-3xl"></div>
      <div class="relative">
        <div class="mb-3 flex flex-wrap items-center gap-2">
          <span class="pt-code">CREDIBILITY</span>
          <span class="pt-chip-mute">{{ t('统计页', 'Statistics') }}</span>
        </div>
        <h1 class="pt-h1 !text-4xl sm:!text-5xl">{{ t('可信度统计', 'Credibility') }}</h1>
        <p class="mt-3 max-w-3xl text-sm leading-relaxed text-parchment/60">
          {{ t('这一页如实公布每条模式的核验状态：已核验、待核验、存疑、一手材料。',
               'This page publishes, as it stands, the verification status of every mode: verified, pending, suspect and primary source.') }}
          <span class="text-parchment/80">{{ t('存疑比假装全对更可信。', 'Flagging doubts beats pretending everything is clean.') }}</span>
        </p>
        <p class="mt-2 max-w-3xl text-xs leading-relaxed text-parchment/45">
          {{ t(`发布口径合计 ${v.publishedTotal} 条模式摘要（站上打得开的那些）；源库口径 ${v.allTotal} 条，其中 ${v.quarantinedTotal} 条隔离记录不进公开产物，也不计入下列四态。`,
               `Published scope: ${v.publishedTotal} mode summaries (the ones reachable on the site). Source scope: ${v.allTotal}, of which ${v.quarantinedTotal} quarantined records never enter public output and are excluded from the four states below.`) }}
        </p>
      </div>
    </header>

    <!-- 四态 -->
    <section class="mb-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <article v-for="c in cards" :key="c.status"
               class="pt-panel p-6" :data-credibility-card="c.status">
        <div class="mb-3 flex items-center justify-between gap-2">
          <CredibilityBadge :verification="c.status" />
          <span class="pt-chip-mute font-mono text-[11px]">{{ pctText(c.count) }}</span>
        </div>
        <div class="font-display text-4xl font-bold tabular-nums text-parchment" :data-credibility-count="c.status">{{ c.count }}</div>
        <p class="mt-2 text-xs leading-relaxed text-parchment/55">{{ t(c.zh, c.en) }}</p>
      </article>
    </section>

    <!-- 空态如实说明 -->
    <section class="mb-8 space-y-3">
      <p v-if="v.published.suspect === 0"
         class="pt-panel p-5 text-sm leading-relaxed text-parchment/60">
        {{ t(`公开口径「存疑」当前为 0 条 —— 这是实测结果，不是省略：源库口径另有 ${v.all.suspect} 条存疑，全部落在隔离记录里，按 D3 豁免条款只服务复核与回滚，不进公开产物。`,
             `Public "suspect" currently equals 0 — that is a measurement, not an omission: the source scope holds ${v.all.suspect} more suspect records, all inside quarantined figures, excluded from public output.`) }}
      </p>
      <p v-if="v.published.verified === 0"
         class="pt-panel border-amber-400/50 p-5 text-sm leading-relaxed text-amber-200/80">
        {{ t('已核验为 0 条：页面照实显示 0，不寻找说法掩盖空态。',
             'Verified count is 0: shown as 0, with no wording invented to hide the empty state.') }}
      </p>
    </section>

    <!-- 可点链接覆盖率（诚实给出比例，不声称全部可点） -->
    <section class="pt-panel mb-8 p-7">
      <h2 class="pt-h3 mb-3 text-parchment">{{ t('可点链接覆盖率', 'Clickable-link coverage') }}</h2>
      <p class="text-sm leading-relaxed text-parchment/65">
        {{ t(`去重级引文 ${links.citationsLinked} / ${links.citations} 条有真实可达的链接（${citePctText}）；出现级引文段 ${links.segmentsLinked} / ${links.segments} 有链接；${links.modesWithLink} / ${links.modesWithCitations} 条带引文的模式至少有一个可点出处。`,
             `Distinct citations with a genuinely reachable link: ${links.citationsLinked} / ${links.citations} (${citePctText}); citation segments: ${links.segmentsLinked} / ${links.segments}; modes with at least one clickable source: ${links.modesWithLink} / ${links.modesWithCitations}.`) }}
      </p>
      <p class="mt-2 text-xs leading-relaxed text-parchment/45">
        {{ t('覆盖率远未到 100%：解析不到链接的出处保持纯文本，宁可不可点，也不伪造 URL。',
             'Coverage is far from 100%: sources without a resolved link stay plain text — better unclickable than faked.') }}
      </p>
    </section>

    <!-- 判定口径与数据来源 -->
    <section class="grid gap-4 lg:grid-cols-2">
      <article class="pt-panel p-7">
        <h2 class="pt-h3 mb-4 text-parchment">{{ t('四态怎么判', 'How the four states are decided') }}</h2>
        <ul class="space-y-3 text-sm leading-relaxed text-parchment/65">
          <li class="flex flex-wrap items-center gap-2"><CredibilityBadge verification="verified" /><span>{{ t('出处可达 + 构建期解析到可点链接', 'Source reachable + link resolved at build time') }}</span></li>
          <li class="flex flex-wrap items-center gap-2"><CredibilityBadge verification="pending" /><span>{{ t('尚未核验，schema 缺省态', 'Not yet checked — the schema default') }}</span></li>
          <li class="flex flex-wrap items-center gap-2"><CredibilityBadge verification="suspect" /><span>{{ t('命中 D1–D5 之一，待复核', 'Matched one of the D1–D5 defect rules, pending review') }}</span></li>
          <li class="flex flex-wrap items-center gap-2"><CredibilityBadge verification="unverifiable" /><span>{{ t('口述 / 信札 / 档案等本质不可链接', 'Oral accounts, letters, archives — not linkable by nature') }}</span></li>
        </ul>
        <p class="mt-4 text-xs leading-relaxed text-parchment/45">
          {{ t('判定规则与处置口径见仓库 docs/planning/credibility_framework.md §1 与 §3。',
               'Rules and dispositions: docs/planning/credibility_framework.md §1 and §3 in the repository.') }}
        </p>
      </article>

      <article class="pt-panel p-7">
        <h2 class="pt-h3 mb-4 text-parchment">{{ t('数字从哪来', 'Where the numbers come from') }}</h2>
        <ul class="space-y-3 text-sm leading-relaxed text-parchment/65">
          <li>{{ t('唯一来源：部署产物 data/meta.json 的 counts.verification。',
                 'Single source: counts.verification in the deployed data/meta.json.') }}
            <a :href="metaHref" class="ml-1 text-gold-300/90 underline decoration-gold-500/40 underline-offset-2 hover:text-gold-200" target="_blank" rel="noopener noreferrer">data/meta.json</a>
          </li>
          <li>{{ t('SPA 侧数字由 tools/gen_web_site_counts.py 在构建前注入（本页不写死、不 fetch 第二份）。',
                 'The SPA numbers are injected before the build by tools/gen_web_site_counts.py (this page hardcodes nothing and fetches no second copy).') }}</li>
          <li>{{ t('静态 head 的四态数字由 tools/prerender_routes.py 用同一份 meta.json 现算；两处不一致，构建立刻失败。',
                 'The prerendered head computes them from the same meta.json; any divergence fails the build.') }}</li>
        </ul>
        <h3 class="mt-6 text-xs uppercase tracking-wider text-parchment/40">{{ t('尚未做（如实列出）', 'Not done yet (listed honestly)') }}</h3>
        <ul class="mt-2 space-y-2 text-xs leading-relaxed text-parchment/45">
          <li>{{ t('D4 引文与原文逐字比对、D5 时间线机检仍缺输入，未接入流水线 —— 因此「已核验」只声称出处可达，不声称引文已逐字核对。',
               'D4 verbatim quote matching and D5 timeline checks still lack inputs and are not wired into the pipeline — so "verified" claims a reachable source, not a verbatim-checked quote.') }}</li>
          <li>{{ t('链接源覆盖面有限：被引书名绝大多数尚无链接源，覆盖率见上。',
               'Link sources are partial: most cited titles still have no link source — see the coverage above.') }}</li>
        </ul>
      </article>
    </section>
  </div>
</template>
