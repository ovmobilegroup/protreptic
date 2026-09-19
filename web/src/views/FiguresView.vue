<template>
  <div class="pt-container pb-16 pt-10">
    <!-- Hero -->
    <section class="relative mb-10">
      <div class="mb-3 flex items-center gap-3">
        <span class="pt-hairline w-10"></span>
        <span class="pt-code">{{ t('思想名录 · 人物 × 场景', 'REGISTER · MINDS × SCENARIOS') }}</span>
      </div>

      <h1 class="pt-h1">
        <span class="pt-gradient-text">{{ t('以人为鉴，明得失', 'Learn from minds of history') }}</span>
      </h1>
      <p class="mt-4 max-w-2xl text-base leading-relaxed text-parchment/70">
        {{ t(
          `${counts.figures} 位历史人物的思维方法，与 ${counts.scenarios} 个现代处境场景，汇成同一份可检索的名录，每条都有出处与操作步骤，中英双语。`,
          `Thinking methods from ${counts.figures} historical figures and ${counts.scenarios} modern scenarios, in one searchable register, each with source and steps.`
        ) }}
      </p>

      <div class="mt-6 flex flex-wrap items-center gap-2">
        <span class="pt-chip-gold">{{ t(`人物 ${counts.figures}`, `${counts.figures} figures`) }}</span>
        <span class="pt-chip-jade">{{ t(`场景 ${counts.scenarios}`, `${counts.scenarios} scenarios`) }}</span>
        <span class="pt-chip-mute">{{ t(`${counts.with_modes} 条含模式`, `${counts.with_modes} with modes`) }}</span>
      </div>
    </section>

    <!-- Phase30-B4: 今日一模式（确定性选取，见 api/dailyMode.ts）-->
    <section class="mb-8">
      <div v-if="dailyState === 'loading'" class="pt-panel p-6">
        <div class="pt-skeleton mb-3 h-6 w-1/2"></div>
        <div class="pt-skeleton h-20 w-full"></div>
      </div>
      <DailyModeCard v-else-if="dailyPick" :pick="dailyPick" />
      <p v-else class="text-xs leading-relaxed text-parchment/40">
        {{ t('今日一模式数据未就绪（data/daily/index.json 未加载）：本模块不猜、不随机，宁可空着。',
             'Daily-mode data unavailable (data/daily/index.json not loaded) — no guessing, no random fallback.') }}
      </p>
    </section>

    <!-- 检索区 -->
    <section class="pt-panel relative mb-8 p-4 sm:p-5">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-center">
        <!-- 类型切换 -->
        <div class="flex shrink-0 rounded-xl border border-white/10 bg-ink-950/50 p-1">
          <button v-for="tb in typeTabs" :key="tb.key"
                  @click="setType(tb.key as any)"
                  class="rounded-lg px-4 py-2 text-sm font-medium transition-all duration-300 ease-silk"
                  :class="type === tb.key
                    ? 'bg-gradient-to-b from-gold-400/90 to-gold-600 text-obsidian shadow-glow'
                    : 'text-parchment/55 hover:text-parchment'">
            {{ t(tb.zh, tb.en) }}
          </button>
        </div>

        <!-- 输入 -->
        <div class="relative flex-1">
          <svg class="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-parchment/35"
               fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
          </svg>
          <input v-model="query" type="text"
                 :placeholder="t('检索人名、编号、领域、概念、正文出处…', 'Search name, code, domain, concept, source…')"
                 class="pt-input pl-11" />
          <button v-if="query" @click="query = ''"
                  class="absolute right-3 top-1/2 -translate-y-1/2 rounded-md p-1 text-parchment/35
                         transition-colors hover:text-parchment/70">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- 筛选 -->
        <div class="shrink-0">
          <FilterPanel :filters="filters" :tag-labels="tagLabels"
                       @filter-change="onFilterChange" @clear-filters="clearFilters" />
        </div>
      </div>

      <p v-if="searchHint" class="mt-4 text-xs leading-relaxed text-parchment/40"
         :class="ftsState === 'degraded' ? 'text-amber-200/60' : ''">
        {{ searchHint }}
      </p>
    </section>

    <!-- 结果区 -->
    <section>
      <div v-if="activeFiltersCount > 0"
           class="mb-5 flex items-center justify-between rounded-xl border border-gold-500/20 bg-gold-500/[.06] px-4 py-2.5">
        <span class="text-sm text-gold-200/85">
          {{ t(`已应用 ${activeFiltersCount} 个筛选条件`, `${activeFiltersCount} filter(s) applied`) }}
        </span>
        <button @click="clearFilters"
                class="rounded-lg px-2.5 py-1 text-xs font-medium text-gold-300 transition-colors hover:bg-gold-500/15">
          {{ t('清除全部', 'Clear all') }}
        </button>
      </div>

      <div v-if="!loading" class="mb-5 flex items-baseline gap-3">
        <h2 class="pt-h2">{{ t('名录', 'Register') }}</h2>
        <span class="font-mono text-sm text-gold-300/80">{{ filtered.length }}</span>
        <span class="text-sm text-parchment/40">{{ t('条', 'entries') }}</span>
      </div>

      <div v-if="loading" class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <FigureCardSkeleton v-for="i in 12" :key="i" />
      </div>

      <div v-else-if="paged.length > 0" class="pt-stagger grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <EntryCard v-for="e in paged" :key="e.type + '-' + e.code" :entry="e" :match-score="e.matchScore" />
      </div>

      <div v-else class="pt-panel flex flex-col items-center gap-3 px-6 py-20 text-center">
        <span class="text-4xl opacity-60">🕳️</span>
        <h3 class="pt-h3 text-parchment/85">{{ t('暂无结果', 'No results') }}</h3>
        <p class="text-sm text-parchment/45">{{ t('试试调整关键词或筛选条件', 'Try adjusting the keyword or filters') }}</p>
        <button @click="clearFilters" class="pt-btn-ghost mt-2">{{ t('重置条件', 'Reset') }}</button>
      </div>

      <Pagination v-if="totalPages > 1" class="mt-10"
                  :current-page="page" :total-pages="totalPages"
                  @page-change="goPage" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { fetchUnifiedIndex, type UnifiedEntry } from '../api/static'
import { loadFigureCodeByDoc } from '../api/modeIndex'
import { searchFullText, MIN_QUERY_CHARS } from '../api/fulltextSearch'
import { useFiguresStore } from '../stores/figures'
import EntryCard from '../components/EntryCard.vue'
import FilterPanel from '../components/FilterPanel.vue'
import Pagination from '../components/Pagination.vue'
import FigureCardSkeleton from '../components/FigureCardSkeleton.vue'
import DailyModeCard from '../components/DailyModeCard.vue'
import { pickToday, type DailyPick } from '../api/dailyMode'

const route = useRoute()
const router = useRouter()
const store = useFiguresStore()
const { t, locale } = useI18n()

// ---- 今日一模式（Phase30-B4）----
// 定位索引只有 12 KB gzip，首屏拉它没问题；详情由 DailyModeCard 再拉一次人物分片。
const dailyState = ref<'loading' | 'ready' | 'empty'>('loading')
const dailyPick = ref<DailyPick | null>(null)

const items = ref<UnifiedEntry[]>([])
const counts = ref({ total: 0, figures: 0, scenarios: 0, with_modes: 0 })
const loading = ref(true)

const type = ref<'all' | 'figure' | 'scenario'>((route.query.type as any) || 'all')
const query = ref((route.query.q as string) || '')
const page = ref(Number(route.query.page) || 1)
const PAGE_SIZE = 24

const filters = ref<Record<string, string>>({
  era: (route.query.era as string) || '',
  historical_domain: (route.query.historical_domain as string) || '',
  domain: (route.query.domain as string) || '',
  gender: (route.query.gender as string) || '',
  ethnicity: (route.query.ethnicity as string) || '',
})

const typeTabs = [
  { key: 'all', zh: '全部', en: 'All' },
  { key: 'figure', zh: '人物', en: 'Figures' },
  { key: 'scenario', zh: '场景', en: 'Scenarios' },
]

// ---- 全文检索（Phase30-A6）：复用 A5 的倒排索引分片 ----
// 索引的 doc_id 指向 modes/index-0..7.json 的拼接下标，靠 api/modeIndex.ts 的共享缓存
// 还原成 figure_code（因此 /figures 首次检索会懒加载模式索引分片，不在首屏加载）。
const DATA_MODE = import.meta.env.VITE_DATA_MODE ?? 'api'
const FTS_DEBOUNCE_MS = 150
type FtsState = 'idle' | 'loading' | 'ready' | 'empty' | 'degraded'
const ftsState = ref<FtsState>('idle')
/** figure_code -> 命中词权重和（同一个人物取最高的一条模式） */
const ftsFigures = ref<Map<string, number>>(new Map())
/** 参与过检索的人物数（用于说明文案） */
const ftsShards = ref<number[]>([])
let ftsTimer: ReturnType<typeof setTimeout> | undefined
let ftsSeq = 0
let figureCodeByDoc: string[] | null = null

const resetFts = () => {
  ftsSeq += 1
  ftsState.value = 'idle'
  ftsFigures.value = new Map()
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
    ftsFigures.value = new Map()
    return
  }
  if (outcome.note !== 'ok') {
    ftsState.value = 'empty'
    ftsFigures.value = new Map()
    ftsShards.value = outcome.shards
    return
  }
  try {
    if (!figureCodeByDoc) figureCodeByDoc = await loadFigureCodeByDoc()
  } catch (err) {
    console.warn('[figures] 模式索引不可用，无法把 doc_id 还原成人物，降级为关键词匹配：', err)
    if (seq !== ftsSeq) return
    ftsState.value = 'degraded'
    ftsFigures.value = new Map()
    return
  }
  if (seq !== ftsSeq) return
  const scores = new Map<string, number>()
  for (const hit of outcome.hits) {
    const code = figureCodeByDoc[hit.docId]
    if (!code) continue
    const prev = scores.get(code) ?? 0
    if (hit.score > prev) scores.set(code, hit.score)
  }
  ftsFigures.value = scores
  ftsShards.value = outcome.shards
  ftsState.value = scores.size ? 'ready' : 'empty'
}

watch(query, () => {
  if (DATA_MODE !== 'static') return
  clearTimeout(ftsTimer)
  if (query.value.trim().length < MIN_QUERY_CHARS) { resetFts(); return }
  ftsTimer = setTimeout(runFts, FTS_DEBOUNCE_MS)
})

const load = async () => {
  loading.value = true
  const idx = await fetchUnifiedIndex()
  if (idx && Array.isArray(idx.items) && idx.items.length) {
    items.value = idx.items
    counts.value = idx.counts
  } else {
    // 回退：老接口/接口模式
    const figs = (store.figures || []) as any[]
    items.value = figs.map((f) => ({
      code: f.code, name: f.name, type: 'scenario' as const,
      description: f.description, n_modes: (f.modes || []).length,
      era: f.era, domains: f.domains, historical_domains: f.historical_domains,
      gender: f.gender, ethnicity: f.ethnicity,
    }))
    counts.value = { total: items.value.length, figures: 0, scenarios: items.value.length, with_modes: items.value.length }
  }
  loading.value = false
}

type RankedEntry = UnifiedEntry & { matchScore?: number }

/** 现有子串匹配：保留为降级路径（索引不可用）与兜底（编号 / 拉丁前缀 / 场景条目） */
const matchesSubstring = (e: UnifiedEntry, q: string): boolean =>
  [e.code, e.name, e.description, e.era, ...(e.domains || []), ...(e.historical_domains || [])]
    .some((v) => String(v || '').toLowerCase().includes(q))

const passesFilters = (e: UnifiedEntry): boolean => {
  if (type.value !== 'all' && e.type !== type.value) return false
  if (filters.value.era && e.era !== filters.value.era) return false
  if (filters.value.historical_domain && !(e.historical_domains || []).includes(filters.value.historical_domain)) return false
  if (filters.value.domain && !(e.domains || []).includes(filters.value.domain)) return false
  if (filters.value.gender && e.gender !== filters.value.gender) return false
  if (filters.value.ethnicity && e.ethnicity !== filters.value.ethnicity) return false
  return true
}

const filtered = computed<RankedEntry[]>(() => {
  const q = query.value.trim().toLowerCase()
  const base = items.value.filter(passesFilters)
  if (!q) return base
  const scores = ftsFigures.value
  if (!scores.size) return base.filter((e) => matchesSubstring(e, q))

  // 倒排命中的（人物）按相关度排前，索引覆盖不到的（场景 / 编号 / 拉丁前缀）子串兜底在后
  const ranked: RankedEntry[] = []
  const rest: RankedEntry[] = []
  for (const e of base) {
    const score = e.type === 'figure' ? scores.get(e.code) : undefined
    if (score !== undefined) ranked.push({ ...e, matchScore: score })
    else if (matchesSubstring(e, q)) rest.push(e)
  }
  ranked.sort((a, b) => (b.matchScore || 0) - (a.matchScore || 0) || a.code.localeCompare(b.code))
  return [...ranked, ...rest]
})

const ftsRankedCount = computed(() => filtered.value.filter((e) => e.matchScore !== undefined).length)
const ftsFallbackCount = computed(() => filtered.value.length - ftsRankedCount.value)

/** 检索能力说明：必须与实现一致，不得宣称语义检索 */
const searchHint = computed(() => {
  if (DATA_MODE !== 'static') return ''
  if (query.value.trim().length < MIN_QUERY_CHARS) {
    return t(
      '全文检索：人物命中来自倒排索引（覆盖人物名 / 模式名 / 分类 / 出处 / 概念 / 领域 / 定义摘要）——不是语义向量检索；场景条目、编号与拉丁前缀仍走子串匹配，案例正文不在索引内。',
      'Full-text search: figure hits come from an inverted index (figure/mode names, category, source chapter, key concepts, domain, definition snippets) — not vector semantic search; scenarios, codes and Latin prefixes still use substring matching, and case bodies are not indexed.'
    )
  }
  if (ftsState.value === 'loading') {
    return t(
      '检索中…（首次检索按 token 首字符拉取索引分片，并把 doc_id 还原成人物）',
      'Searching… (first query loads the shards for the token initials, then resolves doc_ids to figures)'
    )
  }
  if (ftsState.value === 'degraded') {
    return t(
      '已降级为关键词匹配（倒排索引或模式索引分片不可用）。',
      'Degraded to keyword matching (inverted-index or mode-index shards unavailable).'
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
      ? t(`；另有 ${ftsFallbackCount.value} 条为子串兜底`, `; ${ftsFallbackCount.value} more from substring fallback`)
      : ''
    return t(
      `倒排索引命中 ${ftsRankedCount.value} 个人物，按相关度（命中词权重和）排序——不是语义向量检索${tail}。`,
      `${ftsRankedCount.value} figures matched by the inverted index, ordered by token-weight sum — not vector semantic search${tail}.`
    )
  }
  return ''
})

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / PAGE_SIZE)))
const paged = computed(() => filtered.value.slice((page.value - 1) * PAGE_SIZE, page.value * PAGE_SIZE))

const goPage = (p: number) => { page.value = p; window.scrollTo({ top: 180, behavior: 'smooth' }) }
const setType = (v: 'all' | 'figure' | 'scenario') => { type.value = v }
const onFilterChange = (f: Record<string, string>) => { filters.value = { ...filters.value, ...f } }
const clearFilters = () => {
  filters.value = { era: '', historical_domain: '', domain: '', gender: '', ethnicity: '' }
  if (type.value !== 'all') type.value = 'all'
}

// URL 同步
watch([query, type, page, filters], () => {
  const q: Record<string, string> = {}
  if (query.value) q.q = query.value
  if (type.value !== 'all') q.type = type.value
  if (page.value > 1) q.page = String(page.value)
  Object.entries(filters.value).forEach(([k, v]) => { if (v) q[k] = v })
  router.replace({ query: q })
}, { deep: true })

watch([query, type, filters], () => { page.value = 1 }, { deep: true })

const activeFiltersCount = computed(() => Object.values(filters.value).filter((v) => v).length)

const tagLabels: Record<string, Record<string, string>> = {
  era: {
    'Pre-Qin': '先秦', 'Qin-Han': '秦汉', 'Three-Kingdoms-Jin': '三国两晋',
    'Northern-Southern': '南北朝', 'Sui-Tang': '隋唐', 'Song-Yuan': '宋元',
    'Ming-Qing': '明清', 'Modern-Early': '近代', 'Modern': '现代',
  },
  historical_domain: {
    Military: '军事', Philosophy: '哲学', Governance: '治理', Science_Tech: '科技',
    Historiography: '史学', Literature_Arts: '文学艺术', Religion: '宗教',
    Education: '教育', Economics: '经济', Ethics: '伦理',
  },
  domain: {
    Strategic: '战略', Analytical: '分析', Collaborative: '协作', Operational: '操作',
    Systems: '系统', Creative: '创新', Personal: '个人',
  },
  gender: { Male: '男性', Female: '女性' },
  ethnicity: { Han: '汉族', Minority: '少数民族' },
}

const loadDaily = async () => {
  const pick = await pickToday()
  dailyPick.value = pick
  dailyState.value = pick ? 'ready' : 'empty'
}

onMounted(() => {
  load()
  loadDaily()
})
watch(locale, load)
</script>
