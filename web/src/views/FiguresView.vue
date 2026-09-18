<template>
  <div class="pt-container pb-16 pt-10">
    <!-- Hero -->
    <section class="relative mb-10">
      <div class="mb-3 flex items-center gap-3">
        <span class="pt-hairline w-10"></span>
        <span class="pt-code">{{ t('历史人物 · 思维方法', 'HISTORICAL FIGURES · THINKING METHODS') }}</span>
      </div>

      <h1 class="pt-h1">
        <span class="pt-gradient-text">{{ t('以人为鉴，明得失', 'Learn from minds of history') }}</span>
      </h1>
      <p class="mt-4 max-w-2xl text-base leading-relaxed text-parchment/55">
        {{ t(
          '从 284 位历史人物身上提炼的可操作思维方法——每条都有出处、操作步骤与现代应用，供你在真实问题里取用。',
          'Actionable thinking methods distilled from 284 historical figures—each with source, steps and modern application.'
        ) }}
      </p>

      <div class="mt-6 flex flex-wrap items-center gap-2">
        <span class="pt-chip-gold">{{ t('共 1058 位人物', '1058 figures') }}</span>
        <span class="pt-chip-jade">{{ t('2858 条思维模式', '2858 modes') }}</span>
        <span class="pt-chip-mute">{{ t('中英双语', 'Bilingual') }}</span>
      </div>
    </section>

    <!-- 检索区 -->
    <section class="pt-panel relative mb-8 p-4 sm:p-5">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-center">
        <!-- 模式切换 -->
        <div class="flex shrink-0 rounded-xl border border-white/10 bg-ink-950/50 p-1">
          <button
            v-for="m in [
              { key: 'keyword', zh: '关键词', en: 'Keyword' },
              { key: 'smart', zh: '智能检索', en: 'Smart' },
            ]"
            :key="m.key"
            @click="handleModeChange(m.key as 'keyword' | 'smart')"
            class="rounded-lg px-4 py-2 text-sm font-medium transition-all duration-300 ease-silk"
            :class="searchMode === m.key
              ? 'bg-gradient-to-b from-gold-400/90 to-gold-600 text-ink-950 shadow-glow'
              : 'text-parchment/55 hover:text-parchment'"
          >
            {{ t(m.zh, m.en) }}
          </button>
        </div>

        <!-- 输入 -->
        <div class="flex flex-1 items-center gap-3">
          <div class="relative flex-1">
            <svg class="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-parchment/35"
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              :placeholder="t('搜索历史人物、思维模式、领域…', 'Search figures, modes, domains…')"
              @keyup.enter="handleSearch"
              class="pt-input pl-11"
            />
          </div>
          <button @click="handleSearch" class="pt-btn-gold shrink-0">
            {{ t('检索', 'Search') }}
          </button>
        </div>

        <!-- 筛选 -->
        <div class="shrink-0">
          <FilterPanel
            :filters="filters"
            :tag-labels="tagLabels"
            @filter-change="handleFilterChange"
            @clear-filters="clearFilters"
          />
        </div>
      </div>

      <p v-if="searchMode === 'smart'" class="mt-3 flex items-start gap-2 text-xs leading-relaxed text-parchment/40">
        <span class="mt-0.5 text-jade-400">◆</span>
        {{ t(
          '智能检索＝编号 / 名称 / 领域子串匹配（静态站点无向量语义检索）',
          'Smart search = substring match on code / name / domain (no vector search on a static site)'
        ) }}
      </p>
    </section>

    <!-- 结果区 -->
    <section>
      <!-- 已选筛选 -->
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

      <!-- 计数 -->
      <div v-if="!loading" class="mb-5 flex items-baseline gap-3">
        <h2 class="pt-h2">{{ t('思想名录', 'Register of Minds') }}</h2>
        <span class="font-mono text-sm text-gold-300/80">{{ displayedTotal }}</span>
        <span class="text-sm text-parchment/40">{{ t('条', 'entries') }}</span>
      </div>

      <!-- 加载骨架 -->
      <div v-if="loading" class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <FigureCardSkeleton v-for="i in 12" :key="i" />
      </div>

      <!-- 结果网格 -->
      <div v-else-if="displayedFigures.length > 0"
           class="pt-stagger grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <FigureCard v-for="figure in displayedFigures" :key="figure.code" :figure="figure" :lang="locale" />
      </div>

      <!-- 空状态 -->
      <div v-else class="pt-panel flex flex-col items-center gap-3 px-6 py-20 text-center">
        <span class="text-4xl opacity-60">🕳️</span>
        <h3 class="pt-h3 text-parchment/85">{{ t('暂无结果', 'No results') }}</h3>
        <p class="text-sm text-parchment/45">
          {{ t('试试调整关键词或筛选条件', 'Try adjusting the keyword or filters') }}
        </p>
        <button @click="clearFilters" class="pt-btn-ghost mt-2">{{ t('重置条件', 'Reset') }}</button>
      </div>

      <!-- 分页 -->
      <Pagination
        v-if="searchMode === 'keyword' && figuresStore.total > pageSize"
        class="mt-10"
        :current-page="currentPage"
        :total-pages="Math.ceil(figuresStore.total / pageSize)"
        @page-change="currentPage = $event; fetchFigures()"
      />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useFiguresStore } from '../stores/figures'
import { useI18n } from '../composables/useI18n'
import FigureCard from '../components/FigureCard.vue'
import FilterPanel from '../components/FilterPanel.vue'
import Pagination from '../components/Pagination.vue'
import FigureCardSkeleton from '../components/FigureCardSkeleton.vue'

const route = useRoute()
const router = useRouter()
const figuresStore = useFiguresStore()
const { t, locale } = useI18n()

const searchMode = ref<'keyword' | 'smart'>('keyword')
const searchQuery = ref((route.query.q as string) || '')
const currentPage = ref(Number(route.query.page) || 1)
const pageSize = 20

const filters = ref({
  era: (route.query.era as string) || '',
  historical_domain: (route.query.historical_domain as string) || '',
  domain: (route.query.domain as string) || '',
  gender: (route.query.gender as string) || '',
  ethnicity: (route.query.ethnicity as string) || '',
  theme: (route.query.theme as string) || '',
  nationality: (route.query.nationality as string) || '',
  civilization_sphere: (route.query.civilization_sphere as string) || '',
  time_period_standardized: (route.query.time_period_standardized as string) || '',
  wiki_id: (route.query.wiki_id as string) || '',
  primary_language: (route.query.primary_language as string) || '',
  intellectual_tradition: (route.query.intellectual_tradition as string) || '',
  cross_cultural_impact: (route.query.cross_cultural_impact as string) || '',
})

const smartResults = ref<any[]>([])
const smartLoading = ref(false)
const smartTotal = ref(0)
const smartPage = ref(1)
const smartPageSize = 20

const loading = computed(() => figuresStore.loading || smartLoading.value)

watch([searchQuery, filters, currentPage], () => {
  if (searchMode.value === 'keyword') {
    const query: Record<string, string> = {}
    if (searchQuery.value) query.q = searchQuery.value
    if (currentPage.value > 1) query.page = String(currentPage.value)
    Object.entries(filters.value).forEach(([key, value]) => { if (value) query[key] = value })
    router.replace({ query })
  }
}, { deep: true })

watch([() => searchMode.value, searchQuery], async ([newMode]) => {
  if (newMode === 'smart' && searchQuery.value) await performSmartSearch()
})

const fetchFigures = async () => {
  await figuresStore.fetchFigures({
    page: currentPage.value,
    page_size: pageSize,
    search: searchQuery.value || undefined,
    lang: locale.value,
    ...filters.value,
  })
}

watch(locale, async () => {
  if (searchMode.value === 'smart') await performSmartSearch()
  else await fetchFigures()
})

const normalizeResults = (items: any[]): any[] =>
  items.map((item) => ({
    code: '', name: '', description: '', reason: '', modes: [],
    era: null, historical_domains: [], domains: [], gender: null, ethnicity: null,
    ...item,
  }))

const performSmartSearch = async () => {
  if (!searchQuery.value.trim()) return
  smartLoading.value = true
  try {
    const data = await figuresStore.semanticSearch(searchQuery.value, locale.value, smartPageSize)
    smartResults.value = normalizeResults(data || [])
    smartTotal.value = smartResults.value.length
  } catch (error) {
    console.error('Smart search failed:', error)
    smartResults.value = []
    smartTotal.value = 0
  } finally {
    smartLoading.value = false
  }
}

const handleSearch = async () => {
  if (searchMode.value === 'keyword') { currentPage.value = 1; await fetchFigures() }
  else { smartPage.value = 1; await performSmartSearch() }
}

const handleFilterChange = async (newFilters: Record<string, string>) => {
  filters.value = { ...filters.value, ...newFilters }
  if (searchMode.value === 'keyword') { currentPage.value = 1; await fetchFigures() }
}

const clearFilters = async () => {
  filters.value = {
    era: '', historical_domain: '', domain: '', gender: '', ethnicity: '', theme: '',
    nationality: '', civilization_sphere: '', time_period_standardized: '', wiki_id: '',
    primary_language: '', intellectual_tradition: '', cross_cultural_impact: '',
  }
  if (searchMode.value === 'keyword') { currentPage.value = 1; await fetchFigures() }
}

const handleModeChange = async (newMode: 'keyword' | 'smart') => {
  searchMode.value = newMode
  if (newMode === 'smart' && searchQuery.value) await performSmartSearch()
}

onMounted(async () => { await fetchFigures() })

// 筛选项来源（中文标签）
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

const displayedFigures = computed(() => (searchMode.value === 'smart' ? smartResults.value : figuresStore.figures))
const displayedTotal = computed(() => (searchMode.value === 'smart' ? smartTotal.value : figuresStore.total))

const activeFiltersCount = computed(() => Object.values(filters.value).filter((v) => v).length)
</script>
