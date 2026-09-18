<script setup lang="ts">
/**
 * CompareView.vue — Phase30-B3: /compare 跨人物/跨模式并排对照。
 *
 * 组成（全部来自既有静态分片，见 api/compareData.ts）：
 *   1) 选择面板：人物 + 模式的字符级检索（不是语义检索），或从人物档案页「加入对比」一键带入
 *   2) 总览对照表：类型 / 时代 / 模式数 / 领域数 / 出处数 / 概念数
 *   3) 领域分布对比：每项的 domain 分布条 + 「领域 × 项」矩阵表
 *   4) 思维模式并排对照表：按序号对齐（第 N 行 = 每项自己的第 N 条模式，非语义对齐）
 *   5) 共同概念：出现在 >=2 项的关键概念
 *
 * 状态与分享：选中集合由 composables/useCompare 单例持有，URL 的 ?items=code1,code2 是分享真相，
 * 站内改动用 router.replace 回写 query（不污染历史栈）；带 ?items= 直连时以 URL 覆盖本地记忆。
 */
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { setSeo } from '../composables/useSeo'
import { useCompare } from '../composables/useCompare'
import {
  MAX_COMPARE_ITEMS,
  loadCompareItems,
  loadRegistry,
  searchRegistry,
  buildDomainMatrix,
  buildSharedConcepts,
  type CompareItem,
  type CompareMode,
} from '../api/compareData'

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()
const { codes, add, remove, clear, set: setCodes } = useCompare()

const items = ref<CompareItem[]>([])
const missing = ref<string[]>([])
const loading = ref(false)
const registry = ref<Awaited<ReturnType<typeof loadRegistry>>>([])
const query = ref('')
/** 提示语存「键」而不是成品字符串：切换中英文时不会残留另一种语言的旧文案 */
type NoticeKey = '' | 'full' | 'duplicate' | 'copyfail'
const notice = ref<NoticeKey>('')
const noticeText = computed(() => {
  switch (notice.value) {
    case 'full': return t(`最多同时对比 ${MAX_COMPARE_ITEMS} 项，请先移除一项`, `At most ${MAX_COMPARE_ITEMS} items — remove one first`)
    case 'duplicate': return t('该项已在对比列表中', 'Already in the list')
    case 'copyfail': return t('复制失败，请直接复制地址栏链接', 'Copy failed — copy the address bar URL instead')
    default: return ''
  }
})
const copied = ref(false)

/** 请求序号：快速连点时只接受最后一次解析结果，避免旧结果覆盖新选中 */
let seq = 0

const resolveItems = async () => {
  const wanted = codes.value.slice()
  if (!wanted.length) {
    items.value = []
    missing.value = []
    return
  }
  const my = ++seq
  loading.value = true
  const res = await loadCompareItems(wanted)
  if (my !== seq) return
  items.value = res.items
  missing.value = res.missing
  loading.value = false
}

const suggestions = computed(() => searchRegistry(registry.value, query.value))
const selectedSet = computed(() => new Set(codes.value))
const maxModes = computed(() => items.value.reduce((n, i) => Math.max(n, i.modes.length), 0))
const domains = computed(() => buildDomainMatrix(items.value))
const shared = computed(() => buildSharedConcepts(items.value, 2))
const ready = computed(() => items.value.length >= 2)

const shareUrl = computed(() => {
  const base = import.meta.env.BASE_URL || '/'
  const q = codes.value.map((c) => encodeURIComponent(c)).join(',')
  const origin = typeof location !== 'undefined' ? location.origin : 'https://ovmobilegroup.github.io'
  return `${origin}${base}compare/?items=${q}`
})

/** 分布条的调色板：类名必须是源码里的字面量，Tailwind 才能在构建期扫到 */
const BAR_CLASSES = ['bg-gold-400/70', 'bg-jade-400/70', 'bg-gold-600/70', 'bg-jade-600/70', 'bg-parchment/40']
const DOT_CLASSES = ['bg-gold-400', 'bg-jade-400', 'bg-gold-600', 'bg-jade-600', 'bg-parchment/40']
const barClass = (i: number) => BAR_CLASSES[i % BAR_CLASSES.length]
const dotClass = (i: number) => DOT_CLASSES[i % DOT_CLASSES.length]

/** 名录里的 era 字段实测有整段传记（如麦哲伦），表格里只展示前 60 字，全文放 title */
const CLIP_LIMIT = 60
const clip = (value: string, limit = CLIP_LIMIT) => (value && value.length > limit ? `${value.slice(0, limit - 1)}…` : value)

const domainTotal = (item: CompareItem) => item.modes.length || 1
const percent = (n: number, total: number) => Math.round((n / Math.max(total, 1)) * 100)

const modeName = (m: CompareMode) => (locale.value === 'zh' ? m.name : (m.nameEn || m.name))
const modeDomain = (m: CompareMode) => (locale.value === 'zh' ? m.domain : (m.domainEn || m.domain))
const modeDefinition = (m: CompareMode) => (locale.value === 'zh' ? m.definition : (m.definitionEn || m.definition))
const modeSteps = (m: CompareMode) => (locale.value === 'zh' ? m.stepsZh : (m.stepsEn.length ? m.stepsEn : m.stepsZh))

const overviewRows = computed(() => {
  const rows: Array<{ label: string; values: string[]; titles?: string[] }> = [
    {
      label: t('类型', 'Type'),
      values: items.value.map((i) => (i.kind === 'figure' ? t('人物（全部模式）', 'Person (all modes)') : t('单条模式', 'Single mode'))),
    },
    { label: t('编号', 'Code'), values: items.value.map((i) => i.code) },
    { label: t('时代', 'Era'), values: items.value.map((i) => clip(i.era)), titles: items.value.map((i) => i.era) },
    { label: t('所属人物', 'Figure'), values: items.value.map((i) => `${i.figureName}（${i.figureCode}）`) },
    { label: t('模式数', 'Modes'), values: items.value.map((i) => String(i.modes.length)) },
    { label: t('领域数', 'Domains'), values: items.value.map((i) => String(i.domainCounts.length)) },
    { label: t('出处数', 'Sources'), values: items.value.map((i) => String(i.sources.length)) },
    { label: t('核心概念数', 'Concepts'), values: items.value.map((i) => String(i.concepts.length)) },
    {
      label: t('主要领域', 'Top domains'),
      values: items.value.map((i) => i.domainCounts.slice(0, 3).map((d) => `${d.domain} ×${d.count}`).join(' · ')),
    },
  ]
  return rows
})

const tryAdd = (code: string) => {
  const result = add(code)
  notice.value = ''
  if (result === 'full') notice.value = 'full'
  else if (result === 'duplicate') notice.value = 'duplicate'
  if (result === 'added') query.value = ''
}

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(shareUrl.value)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2200)
  } catch {
    notice.value = 'copyfail'
  }
}

/** 选中集合 -> URL query（分享链接的唯一真相） */
const syncQuery = () => {
  const want = codes.value.join(',')
  const have = String(route.query.items ?? '')
  if (want === have) return
  const next: Record<string, string> = {}
  for (const [k, v] of Object.entries(route.query)) if (k !== 'items' && typeof v === 'string') next[k] = v
  if (want) next.items = want
  router.replace({ query: next })
}

watch(codes, () => { resolveItems(); syncQuery() })

/** 直链/浏览器前进后退：URL 变了就整体替换选中集合 */
watch(() => route.query.items, (raw) => {
  const list = String(raw ?? '').split(',').map((s) => s.trim()).filter(Boolean)
  if (list.join(',') !== codes.value.join(',')) setCodes(list)
})

onMounted(async () => {
  const raw = String(route.query.items ?? '')
  if (raw) setCodes(raw.split(',').map((s) => s.trim()).filter(Boolean))
  await resolveItems()
  syncQuery()
  registry.value = await loadRegistry()
  setSeo({
    title: '跨人物对比 - 思维模式并排对照',
    description: '选 2-4 位历史人物或思维模式，并排对照定义、操作步骤、出处与领域分布；链接带选中项，可直接分享。',
    path: 'compare',
  })
})
</script>

<template>
  <div class="pt-container pb-20 pt-8">
    <header class="pt-panel relative mb-8 overflow-hidden p-7">
      <div aria-hidden="true"
           class="pointer-events-none absolute -top-24 right-0 h-64 w-64 rounded-full bg-gold-500/10 blur-3xl"></div>
      <div class="relative">
        <div class="mb-3 flex flex-wrap items-center gap-2">
          <span class="pt-code">/compare</span>
          <span class="pt-chip-gold">{{ t(`已选 ${codes.length} / ${MAX_COMPARE_ITEMS} 项`, `${codes.length} of ${MAX_COMPARE_ITEMS} selected`) }}</span>
          <span v-if="loading" class="pt-chip-mute">{{ t('载入中…', 'Loading…') }}</span>
        </div>
        <h1 class="pt-h1 !text-4xl sm:!text-5xl">{{ t('跨人物对比', 'Compare Minds') }}</h1>
        <p class="mt-3 max-w-3xl text-sm leading-relaxed text-parchment/55">
          {{ t('选 2-4 位历史人物或思维模式，并排对照其定义、操作步骤、出处与领域分布。地址栏带选中项（?items=…），复制即分享。',
               'Pick 2-4 persons or thinking modes and compare definitions, steps, sources and domain distribution side by side. The URL carries the selection — copy it to share.') }}
        </p>
        <div class="mt-5 flex flex-wrap items-center gap-3">
          <button class="pt-btn-ghost" :disabled="!codes.length" @click="copyLink">
            {{ t('复制分享链接', 'Copy share link') }}
          </button>
          <button v-if="codes.length" class="pt-btn-ghost" @click="clear()">
            {{ t('清空选择', 'Clear') }}
          </button>
          <span v-if="copied" class="text-xs text-jade-300">{{ t('链接已复制到剪贴板', 'Link copied') }}</span>
          <span v-else-if="noticeText" class="text-xs text-gold-300/80">{{ noticeText }}</span>
        </div>
      </div>
    </header>

    <section class="pt-panel mb-8 p-5">
      <h2 class="pt-h3 mb-3 text-parchment/90">{{ t('选择对比项', 'Pick items') }}</h2>
      <input
        v-model="query"
        type="search"
        class="w-full rounded-xl border border-white/10 bg-white/[.03] px-4 py-2.5 text-sm text-parchment
               placeholder:text-parchment/35 focus:border-gold-500/50 focus:outline-none"
        :placeholder="t('搜索人物名、模式名或编号（如 王阳明 / 致良知 / M381）', 'Search a person, mode or code')"
      />
      <div v-if="query.trim()" class="mt-3 max-h-72 overflow-y-auto">
        <button
          v-for="e in suggestions"
          :key="e.kind + ':' + e.code"
          class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-left text-sm transition-colors hover:bg-gold-500/10"
          :class="selectedSet.has(e.code) ? 'opacity-40' : ''"
          @click="tryAdd(e.code)"
        >
          <span class="pt-chip shrink-0" :class="e.kind === 'figure' ? 'pt-chip-jade' : 'pt-chip-gold'">
            {{ e.kind === 'figure' ? t('人物', 'Figure') : t('模式', 'Mode') }}
          </span>
          <span class="min-w-0 flex-1 truncate text-parchment/85">{{ e.name }}</span>
          <span class="hidden min-w-0 shrink-0 truncate text-xs text-parchment/40 sm:block">{{ e.sub }}</span>
          <span class="shrink-0 font-mono text-xs text-parchment/35">{{ e.code }}</span>
        </button>
        <p v-if="!suggestions.length" class="px-3 py-4 text-sm text-parchment/45">
          {{ t('没有匹配项：只支持人物与模式（场景条目没有模式档案，无法并排对照）。', 'No match — figures and modes only.') }}
        </p>
      </div>
      <div v-if="codes.length" class="mt-4 flex flex-wrap gap-2">
        <span v-for="c in codes" :key="c" class="pt-chip-gold gap-2">
          <span class="font-mono">{{ c }}</span>
          <button class="text-gold-200/70 transition-colors hover:text-gold-100" :aria-label="t('移除', 'Remove')"
                  @click="remove(c)">✕</button>
        </span>
      </div>
      <p class="mt-3 text-xs text-parchment/40">
        {{ t('也可以从人物档案页点「加入对比」一键带入；同一浏览器里的选择会被记住。', 'Or use “Add to compare” on a person archive page.') }}
      </p>
      <p v-if="missing.length" class="mt-2 text-xs text-red-300/80">
        {{ t('无法解析（编号不存在或为场景条目）：', 'Unresolved (unknown code or scenario entry): ') }}{{ missing.join('、') }}
      </p>
    </section>

    <section v-if="!ready && !loading" class="pt-panel px-6 py-14 text-center">
      <div class="mb-3 text-4xl opacity-70">⚖️</div>
      <h2 class="pt-h3 mb-2 text-parchment/90">
        {{ codes.length ? t('再选 1 项即可开始对照', 'Pick one more to compare') : t('还没有选择对比项', 'Nothing selected yet') }}
      </h2>
      <p class="text-sm text-parchment/50">
        {{ t('支持 2-4 项：人物（含其全部模式）或单条模式。', '2-4 items: a person (all their modes) or a single mode.') }}
      </p>
    </section>

    <template v-if="items.length">
      <section class="mb-8">
        <h2 class="pt-h2 mb-4">{{ t('总览对照', 'Overview') }}</h2>
        <div class="pt-panel overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full min-w-[640px] text-sm">
              <thead>
                <tr class="border-b border-white/10 text-left text-xs uppercase tracking-wider text-parchment/40">
                  <th class="px-4 py-3 font-medium">{{ t('维度', 'Field') }}</th>
                  <th v-for="it in items" :key="it.code" class="px-4 py-3 font-medium text-parchment/70">
                    {{ it.name }}
                    <span class="ml-1 font-mono text-[10px] text-parchment/35">{{ it.code }}</span>
                  </th>
                </tr>
              </thead>
              <tbody class="text-parchment/70">
                <tr v-for="row in overviewRows" :key="row.label" class="border-b border-white/5 last:border-0">
                  <th class="px-4 py-3 text-left font-normal text-parchment/45">{{ row.label }}</th>
                  <td v-for="(v, i) in row.values" :key="i" class="px-4 py-3 align-top break-words"
                      :title="row.titles ? row.titles[i] : undefined">{{ v || '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section class="mb-8">
        <h2 class="pt-h2 mb-1">{{ t('领域分布对比', 'Domain distribution') }}</h2>
        <p class="mb-4 text-xs text-parchment/40">
          {{ t('按每条模式自身的领域字段归类：人物项 = 其全部模式，模式项 = 该模式 1 条。', 'Grouped by each mode’s own domain field.') }}
        </p>
        <div class="grid gap-4 lg:grid-cols-2">
          <div v-for="it in items" :key="it.code" class="pt-panel p-5">
            <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
              <h3 class="text-sm font-medium text-parchment/85">{{ it.name }}</h3>
              <span class="pt-chip-mute">{{ it.modes.length }} {{ t('条模式', 'modes') }}</span>
            </div>
            <div class="mb-3 flex h-2.5 overflow-hidden rounded-full bg-white/[.06]">
              <span v-for="(d, i) in it.domainCounts" :key="d.domain"
                    :class="barClass(i)" :style="{ width: percent(d.count, domainTotal(it)) + '%' }"
                    :title="`${d.domain} ×${d.count}`"></span>
            </div>
            <ul class="space-y-1.5 text-sm text-parchment/65">
              <li v-for="(d, i) in it.domainCounts" :key="d.domain" class="flex items-center gap-2">
                <span class="h-2 w-2 shrink-0 rounded-full" :class="dotClass(i)"></span>
                <span class="min-w-0 flex-1 break-words">{{ d.domain }}</span>
                <span class="shrink-0 font-mono text-xs text-parchment/45">{{ d.count }} · {{ percent(d.count, domainTotal(it)) }}%</span>
              </li>
            </ul>
          </div>
        </div>
        <div class="pt-panel mt-4 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full min-w-[560px] text-sm">
              <thead>
                <tr class="border-b border-white/10 text-left text-xs uppercase tracking-wider text-parchment/40">
                  <th class="px-4 py-3 font-medium">{{ t('领域 × 项', 'Domain × item') }}</th>
                  <th v-for="it in items" :key="it.code" class="px-4 py-3 text-right font-medium text-parchment/70">{{ it.name }}</th>
                  <th class="px-4 py-3 text-right font-medium">{{ t('合计', 'Total') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in domains" :key="row.domain" class="border-b border-white/5 last:border-0">
                  <th class="px-4 py-2.5 text-left font-normal text-parchment/70">{{ row.domain }}</th>
                  <td v-for="(n, i) in row.counts" :key="i" class="px-4 py-2.5 text-right font-mono"
                      :class="n ? 'text-gold-300' : 'text-parchment/25'">{{ n || '—' }}</td>
                  <td class="px-4 py-2.5 text-right font-mono text-parchment/45">{{ row.total }}</td>
                </tr>
                <tr v-if="!domains.length">
                  <td :colspan="items.length + 2" class="px-4 py-6 text-center text-parchment/45">
                    {{ t('这些项的领域字段为空，无法做分布对比。', 'No domain data for these items.') }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section class="mb-8">
        <h2 class="pt-h2 mb-1">{{ t('思维模式并排对照', 'Modes side by side') }}</h2>
        <p class="mb-4 text-xs text-parchment/40">
          {{ t('按序号对齐，不是语义对齐：第 N 行 = 每项自己的第 N 条模式。', 'Aligned by ordinal, not by meaning: row N = each item’s Nth mode.') }}
        </p>
        <div class="pt-panel overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full min-w-[820px] text-sm">
              <thead>
                <tr class="border-b border-white/10 text-left text-xs uppercase tracking-wider text-parchment/40">
                  <th class="w-12 px-4 py-3 font-medium">#</th>
                  <th v-for="it in items" :key="it.code" class="px-4 py-3 font-medium text-parchment/70">{{ it.name }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="i in maxModes" :key="i" class="border-b border-white/5 align-top last:border-0">
                  <td class="px-4 py-4 font-mono text-xs text-gold-400/70">{{ i }}</td>
                  <td v-for="it in items" :key="it.code" class="px-4 py-4 align-top">
                    <template v-if="it.modes[i - 1]">
                      <div class="mb-2 flex flex-wrap items-center gap-2">
                        <span class="pt-code">{{ it.modes[i - 1].code }}</span>
                        <span class="font-medium text-parchment/90">{{ modeName(it.modes[i - 1]) }}</span>
                      </div>
                      <div class="mb-2 flex flex-wrap gap-1.5">
                        <span class="pt-chip-jade">{{ modeDomain(it.modes[i - 1]) }}</span>
                        <span v-if="it.modes[i - 1].category" class="pt-chip-mute">{{ it.modes[i - 1].category }}</span>
                      </div>
                      <p class="mb-2 text-xs leading-relaxed text-parchment/65">{{ modeDefinition(it.modes[i - 1]) }}</p>
                      <ol v-if="modeSteps(it.modes[i - 1]).length" class="mb-2 space-y-1 text-xs text-parchment/55">
                        <li v-for="(s, j) in modeSteps(it.modes[i - 1])" :key="j" class="flex gap-2">
                          <span class="shrink-0 font-mono text-gold-400/60">{{ j + 1 }}.</span><span>{{ s }}</span>
                        </li>
                      </ol>
                      <div class="text-xs text-parchment/45">{{ t('出处', 'Source') }}：{{ it.modes[i - 1].source || '—' }}</div>
                      <blockquote v-if="it.modes[i - 1].quote"
                                  class="mt-2 border-l-2 border-gold-500/40 pl-3 font-display text-xs leading-relaxed text-parchment/70">
                        {{ it.modes[i - 1].quote }}
                      </blockquote>
                      <div v-if="it.modes[i - 1].concepts.length" class="mt-2 flex flex-wrap gap-1.5">
                        <span v-for="c in it.modes[i - 1].concepts.slice(0, 5)" :key="c" class="pt-chip-mute">{{ c }}</span>
                      </div>
                    </template>
                    <span v-else class="text-parchment/25">—</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section v-if="items.length >= 2" class="mb-8">
        <h2 class="pt-h2 mb-1">{{ t('共同概念', 'Shared concepts') }}</h2>
        <p class="mb-4 text-xs text-parchment/40">
          {{ t(`出现在 2 项及以上的关键概念（共 ${shared.length} 个）。`, `${shared.length} key concepts appearing in 2+ items.`) }}
        </p>
        <div v-if="shared.length" class="flex flex-wrap gap-2">
          <span v-for="s in shared" :key="s.concept" class="pt-chip-gold" :title="s.codes.join('、')">
            {{ s.concept }} · {{ s.codes.length }}
          </span>
        </div>
        <p v-else class="pt-panel px-5 py-6 text-sm text-parchment/50">
          {{ t('没有共同关键概念：这些项的 key_concepts 完全不重叠。', 'No overlap in key_concepts.') }}
        </p>
      </section>
    </template>
  </div>
</template>
