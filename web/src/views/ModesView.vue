<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useI18n } from '../composables/useI18n'
import { useRouter } from 'vue-router'
import { loadModeIndex } from '../api/modeIndex'
import { searchFullText, MIN_QUERY_CHARS } from '../api/fulltextSearch'

const { t, locale } = useI18n()
const router = useRouter()

const DATA_MODE = import.meta.env.VITE_DATA_MODE ?? 'api'
/** 查询防抖（ms）：与 docs/architecture/web_p0_architecture.md §4.4 一致 */
const FTS_DEBOUNCE_MS = 150

interface ModeItem {
  /** 静态模式下 = modes/index-0..7.json 拼接下标，与全文索引的 doc_id 同源 */
  docId?: number
  id: string
  name_zh: string
  name_en: string
  domain_zh: string
  domain_en: string
  category?: string
  figure_code?: string
  figure_name?: string
  description_zh?: string
  description_en?: string
  formula_zh?: string
  formula_en?: string
  level?: string | number
  /** 全文检索命中的权重和（仅静态模式、有查询时） */
  score?: number
}

const modes = ref<ModeItem[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const visibleCount = ref(120)
const query = ref('')
const activeCategory = ref('')

type FtsState = 'idle' | 'loading' | 'ready' | 'empty' | 'degraded'
const ftsState = ref<FtsState>('idle')
/** doc_id -> 权重和 */
const ftsHits = ref<Map<number, number>>(new Map())
const ftsShards = ref<number[]>([])
let ftsTimer: ReturnType<typeof setTimeout> | undefined
let ftsSeq = 0

/** 静态模式：8 个模式索引分片（api/modeIndex.ts 共享缓存，/figures 检索用同一份） */
const fetchStaticModes = async (): Promise<ModeItem[]> => {
  const entries = await loadModeIndex()
  return entries.map((e) => ({
    docId: e.docId,
    id: e.modeCode,
    name_zh: e.nameZh, name_en: e.nameEn,
    domain_zh: e.domainZh, domain_en: e.domainEn,
    category: e.category, figure_code: e.figureCode, figure_name: e.figureName,
    level: '',
  }))
}

const fetchApiModes = async (): Promise<ModeItem[]> => {
  const r = await fetch('/api/v1/modes')
  if (!r.ok) throw new Error(`/api/v1/modes HTTP ${r.status}`)
  const d = await r.json()
  return (d.data || []).map((m: any) => ({
    id: String(m.id ?? ''), name_zh: m.name ?? '', name_en: m.name_en ?? '',
    domain_zh: m.domain ?? '', domain_en: m.domain_en ?? '',
    description_zh: m.description ?? '', description_en: m.description_en ?? '',
    formula_zh: m.formula ?? '', formula_en: m.formula_en ?? '',
  }))
}

const fetchModes = async () => {
  loading.value = true; error.value = null
  try {
    modes.value = DATA_MODE === 'static' ? await fetchStaticModes() : await fetchApiModes()
    visibleCount.value = 120
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to fetch modes'
  } finally { loading.value = false }
}

const figureCount = computed(() => new Set(modes.value.map((m) => m.figure_code).filter(Boolean)).size)

// 分类聚合
const categories = computed(() => {
  const c: Record<string, number> = {}
  for (const m of modes.value) if (m.category) c[m.category] = (c[m.category] || 0) + 1
  return Object.entries(c).sort((a, b) => b[1] - a[1])
})

/** 现有子串匹配：保留为降级路径（索引不可用）与兜底（编号、拉丁前缀等索引外字段） */
const matchesSubstring = (m: ModeItem, q: string): boolean =>
  [m.id, m.name_zh, m.name_en, m.domain_zh, m.figure_name, m.category]
    .some((v) => String(v || '').toLowerCase().includes(q))

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  const base = activeCategory.value ? modes.value.filter((m) => m.category === activeCategory.value) : modes.value
  if (!q) return base

  const hits = ftsState.value === 'ready' ? ftsHits.value : null
  if (!hits || hits.size === 0) return base.filter((m) => matchesSubstring(m, q))

  // 倒排命中按相关度（权重和）排序，索引覆盖不到的（编号 / 拉丁前缀）用子串兜底追加在后
  const ranked: ModeItem[] = []
  const rest: ModeItem[] = []
  for (const m of base) {
    const score = m.docId === undefined ? undefined : hits.get(m.docId)
    if (score !== undefined) ranked.push({ ...m, score })
    else if (matchesSubstring(m, q)) rest.push(m)
  }
  ranked.sort((a, b) => (b.score || 0) - (a.score || 0) || (a.docId || 0) - (b.docId || 0))
  return [...ranked, ...rest]
})

const visibleModes = computed(() => filtered.value.slice(0, visibleCount.value))

const ftsRankedCount = computed(() => filtered.value.filter((m) => m.score !== undefined).length)
const ftsFallbackCount = computed(() => filtered.value.length - ftsRankedCount.value)

/** 检索能力说明：必须与实现一致，不得宣称语义检索 */
const searchHint = computed(() => {
  if (DATA_MODE !== 'static') return ''
  if (query.value.trim().length < MIN_QUERY_CHARS) {
    return t(
      '全文检索：按倒排索引匹配人物名 / 模式名 / 分类 / 出处 / 概念 / 领域 / 定义摘要——不是语义向量检索；拉丁词不做前缀（decis ≠ decision），编号与案例正文需靠子串兜底。',
      'Full-text search: an inverted index over figure/mode names, category, source chapter, key concepts, domain and definition snippets — not vector semantic search; Latin words are not prefix-expanded, and codes/case bodies rely on substring fallback.'
    )
  }
  if (ftsState.value === 'loading') {
    return t(
      '检索中…（首次查询按 token 首字符拉取索引分片，之后常驻内存）',
      'Searching… (first query fetches only the shards matching token initials, then caches them)'
    )
  }
  if (ftsState.value === 'degraded') {
    return t(
      '已降级为关键词匹配（倒排索引分片不可用）。',
      'Degraded to keyword matching (inverted-index shards unavailable).'
    )
  }
  if (ftsState.value === 'empty') {
    return t(
      '倒排索引未命中（拉丁词不做前缀，编号与案例正文不在索引内），以下为编号 / 名称 / 领域子串匹配结果。',
      'No inverted-index match (Latin words are not prefix-expanded; codes and case bodies are not indexed). Showing substring matches on code / name / domain.'
    )
  }
  if (ftsState.value === 'ready') {
    const tail = ftsFallbackCount.value > 0
      ? t(`；另有 ${ftsFallbackCount.value} 条为编号 / 名称子串兜底`, `; ${ftsFallbackCount.value} more from substring fallback`)
      : ''
    return t(
      `倒排索引命中 ${ftsRankedCount.value} 条，按相关度（命中词权重和）排序——不是语义向量检索${tail}。`,
      `${ftsRankedCount.value} inverted-index hits, ordered by token-weight sum — not vector semantic search${tail}.`
    )
  }
  return ''
})

const resetFts = () => {
  ftsSeq += 1
  ftsState.value = 'idle'
  ftsHits.value = new Map()
  ftsShards.value = []
}

const runFts = async () => {
  const raw = query.value.trim()
  if (DATA_MODE !== 'static' || raw.length < MIN_QUERY_CHARS) { resetFts(); return }
  const seq = ++ftsSeq
  ftsState.value = 'loading'
  const outcome = await searchFullText(raw)
  if (seq !== ftsSeq) return
  if (!outcome) {
    ftsState.value = 'degraded'
    ftsHits.value = new Map()
    ftsShards.value = []
    return
  }
  const hits = new Map<number, number>()
  for (const hit of outcome.hits) hits.set(hit.docId, hit.score)
  ftsHits.value = hits
  ftsShards.value = outcome.shards
  ftsState.value = outcome.note === 'ok' ? 'ready' : 'empty'
}

watch(query, () => {
  if (DATA_MODE !== 'static') return
  clearTimeout(ftsTimer)
  if (query.value.trim().length < MIN_QUERY_CHARS) { resetFts(); return }
  ftsTimer = setTimeout(runFts, FTS_DEBOUNCE_MS)
})

onMounted(fetchModes)
</script>

<template>
  <div class="pt-container pb-16 pt-10">
    <!-- Hero -->
    <section class="mb-8">
      <div class="mb-3 flex items-center gap-3">
        <span class="pt-hairline w-10"></span>
        <span class="pt-code">{{ t('思维模式 · 可执行方法', 'THINKING MODES · EXECUTABLE METHODS') }}</span>
      </div>
      <h1 class="pt-h1"><span class="pt-gradient-text">{{ t('思维模式库', 'Thinking Modes') }}</span></h1>
      <p class="mt-4 max-w-2xl text-base leading-relaxed text-parchment/70">
        <template v-if="DATA_MODE === 'static'">
          {{ t(
            `${modes.length} 条思维模式实例，源自 ${figureCount} 位历史人物——每条都出自具体人物与具体文本。`,
            `${modes.length} mode instances from ${figureCount} historical figures.`
          ) }}
        </template>
        <template v-else>
          {{ t(`${modes.length} 种可执行的思维模式`, `${modes.length} executable thinking modes`) }}
        </template>
      </p>
    </section>

    <!-- 检索 + 分类 -->
    <section class="pt-panel mb-8 p-4">
      <div class="relative mb-4">
        <svg class="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-parchment/35"
             fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
        </svg>
        <input v-model="query" type="text"
               :placeholder="t('检索模式名、人物、领域、概念、出处…', 'Search mode, figure, domain, concept, source…')"
               class="pt-input pl-11" />
      </div>

      <p v-if="searchHint" class="mb-4 text-xs leading-relaxed text-parchment/40"
         :class="ftsState === 'degraded' ? 'text-amber-200/60' : ''">
        {{ searchHint }}
        <span v-if="ftsState === 'ready' && ftsShards.length" class="text-parchment/30">
          · {{ t(`本次索引分片 ${ftsShards.length} 片`, `${ftsShards.length} index shard(s)`) }}
        </span>
      </p>

      <div v-if="categories.length" class="flex flex-wrap gap-2">
        <button @click="activeCategory = ''"
                class="pt-chip" :class="!activeCategory ? 'border-gold-500/50 bg-gold-500/15 text-gold-200' : 'border-white/10 bg-white/[.04] text-parchment/60 hover:text-parchment'">
          {{ t('全部', 'All') }} · {{ modes.length }}
        </button>
        <button v-for="[cat, n] in categories" :key="cat" @click="activeCategory = cat"
                class="pt-chip"
                :class="activeCategory === cat ? 'border-gold-500/50 bg-gold-500/15 text-gold-200' : 'border-white/10 bg-white/[.04] text-parchment/60 hover:text-parchment'">
          {{ cat }} · {{ n }}
        </button>
      </div>
    </section>

    <!-- 结果 -->
    <div v-if="loading" class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div v-for="i in 8" :key="i" class="rounded-2xl border border-white/10 bg-white/[.03] p-5">
        <div class="pt-skeleton mb-3 h-4 w-20"></div>
        <div class="pt-skeleton mb-2 h-6 w-2/3"></div>
        <div class="pt-skeleton h-3.5 w-full"></div>
      </div>
    </div>

    <div v-else-if="error" class="pt-panel px-6 py-12 text-center text-red-300/85">
      {{ error }}
    </div>

    <template v-else>
      <div class="pt-stagger grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <article v-for="m in visibleModes" :key="m.id + '-' + (m.figure_code || '')"
                 @click="m.figure_code && router.push({ name: 'mind', params: { code: m.figure_code } })"
                 :class="m.figure_code ? 'cursor-pointer' : ''"
                 class="group relative flex flex-col overflow-hidden rounded-2xl border border-white/10 bg-white/[.03] p-5
                        transition-all duration-500 ease-silk hover:-translate-y-1 hover:border-jade-400/40 hover:bg-white/[.055]">
          <div class="mb-3 flex items-center justify-between gap-2">
            <span class="pt-code shrink-0">{{ m.id }}</span>
            <span v-if="m.category" class="pt-chip-mute max-w-[9rem] truncate">{{ m.category }}</span>
          </div>
          <h3 class="font-display text-base font-bold leading-snug text-parchment transition-colors group-hover:text-gold-200">
            {{ locale === 'zh' ? m.name_zh : (m.name_en || m.name_zh) }}
          </h3>
          <p v-if="(locale === 'zh' ? m.description_zh : m.description_en)"
             class="mt-2 text-sm leading-relaxed text-parchment/70 line-clamp-3">
            {{ locale === 'zh' ? m.description_zh : m.description_en }}
          </p>
          <p v-else-if="m.figure_name" class="mt-2 text-sm text-parchment/50">
            {{ t('代表人物', 'Figure') }} · <span class="text-gold-300/85">{{ m.figure_name }}</span>
          </p>
          <p v-if="m.domain_zh" class="mt-2 text-xs leading-relaxed text-jade-300/60 line-clamp-1">
            {{ locale === 'zh' ? m.domain_zh : (m.domain_en || m.domain_zh) }}
          </p>
          <div class="mt-auto flex flex-wrap items-center gap-1.5 pt-4">
            <span v-if="m.figure_name" class="pt-chip-mute max-w-full truncate">{{ m.figure_name }}</span>
            <span v-if="m.level" class="pt-chip-mute">{{ t('梯度', 'Tier') }}{{ m.level }}</span>
            <span v-if="m.score !== undefined" class="pt-chip-gold" :title="t('命中词权重和（4 人名/模式名 · 2 分类/出处/概念/领域 · 1 定义摘要）', 'Sum of matched token weights (4 name · 2 category/source/concept/domain · 1 definition snippet)')">
              {{ t('相关度', 'relevance') }} {{ m.score }}
            </span>
          </div>
        </article>
      </div>

      <div v-if="visibleCount < filtered.length" class="mt-10 text-center">
        <button @click="visibleCount += 240" class="pt-btn-ghost">
          {{ t(`显示更多（剩余 ${filtered.length - visibleCount} 条）`, `Show more (${filtered.length - visibleCount} left)`) }}
        </button>
      </div>
      <div v-else-if="!filtered.length" class="pt-panel px-6 py-16 text-center text-parchment/50">
        {{ t('没有匹配的模式', 'No matching modes') }}
      </div>
    </template>
  </div>
</template>
