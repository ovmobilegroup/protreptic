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
          '284 位历史人物的思维方法，与 1058 个现代处境场景，汇成同一份可检索的名录——每条都有出处与操作步骤，中英双语。',
          'Thinking methods from 284 historical figures and 1058 modern scenarios, in one searchable register—each with source and steps.'
        ) }}
      </p>

      <div class="mt-6 flex flex-wrap items-center gap-2">
        <span class="pt-chip-gold">{{ t(`人物 ${counts.figures}`, `${counts.figures} figures`) }}</span>
        <span class="pt-chip-jade">{{ t(`场景 ${counts.scenarios}`, `${counts.scenarios} scenarios`) }}</span>
        <span class="pt-chip-mute">{{ t(`${counts.with_modes} 条含模式`, `${counts.with_modes} with modes`) }}</span>
      </div>
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
                 :placeholder="t('搜索人名、编号、领域、关键词…', 'Search name, code, domain…')"
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
        <EntryCard v-for="e in paged" :key="e.type + '-' + e.code" :entry="e" />
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
import { useFiguresStore } from '../stores/figures'
import EntryCard from '../components/EntryCard.vue'
import FilterPanel from '../components/FilterPanel.vue'
import Pagination from '../components/Pagination.vue'
import FigureCardSkeleton from '../components/FigureCardSkeleton.vue'

const route = useRoute()
const router = useRouter()
const store = useFiguresStore()
const { t, locale } = useI18n()

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

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  return items.value.filter((e) => {
    if (type.value !== 'all' && e.type !== type.value) return false
    if (filters.value.era && e.era !== filters.value.era) return false
    if (filters.value.historical_domain && !(e.historical_domains || []).includes(filters.value.historical_domain)) return false
    if (filters.value.domain && !(e.domains || []).includes(filters.value.domain)) return false
    if (filters.value.gender && e.gender !== filters.value.gender) return false
    if (filters.value.ethnicity && e.ethnicity !== filters.value.ethnicity) return false
    if (!q) return true
    return [e.code, e.name, e.description, e.era, ...(e.domains || []), ...(e.historical_domains || [])]
      .some((v) => String(v || '').toLowerCase().includes(q))
  })
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

onMounted(load)
watch(locale, load)
</script>
