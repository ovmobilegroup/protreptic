<template>
  <div class="figures-view">
    <!-- Search Header -->
    <div class="search-header">
      <div class="search-container">
        <div class="search-modes">
          <button 
            :class="['mode-btn', { active: searchMode === 'keyword' }]"
            @click="handleModeChange('keyword')"
          >
            关键词搜索
          </button>
          <button 
            :class="['mode-btn', { active: searchMode === 'semantic' }]"
            @click="handleModeChange('semantic')"
          >
            语义搜索
          </button>
        </div>
        
        <div class="search-input-container">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索历史人物、思维模式..."
            @keyup.enter="handleSearch"
            class="search-input"
          />
          <button @click="handleSearch" class="search-btn">
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Sidebar -->
      <div class="sidebar">
        <FilterPanel 
          :filters="filters"
          @filter-change="handleFilterChange"
          @clear-filters="clearFilters"
        />
      </div>

      <!-- Content Area -->
      <div class="content">
        <!-- Active Filters -->
        <div v-if="activeFiltersCount > 0" class="active-filters">
          <span class="filter-count">已选择 {{ activeFiltersCount }} 个筛选条件</span>
          <button @click="clearFilters" class="clear-btn">清除所有</button>
        </div>

        <!-- Loading State -->
        <div v-if="figuresStore.loading" class="loading">
          <div class="skeleton-grid">
            <FigureCardSkeleton v-for="i in 12" :key="i" />
          </div>
        </div>

        <!-- Results -->
        <div v-else-if="figuresStore.figures.length > 0" class="results">
          <div class="results-header">
            <h2>搜索结果</h2>
            <span class="results-count">共 {{ figuresStore.total }} 条结果</span>
          </div>
          
          <div class="figures-grid">
            <FigureCard 
              v-for="figure in figuresStore.figures" 
              :key="figure.code"
              :figure="figure"
            />
          </div>

          <!-- Pagination -->
          <Pagination
            v-if="figuresStore.total > pageSize"
            :current-page="currentPage"
            :total-pages="Math.ceil(figuresStore.total / pageSize)"
            @page-change="currentPage = $event; fetchFigures()"
          />
        </div>

        <!-- No Results -->
        <div v-else class="no-results">
          <h3>暂无结果</h3>
          <p>请尝试调整搜索条件或筛选器</p>
        </div>
      </div>
    </div>
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
import { useApi } from '../api/client'

const route = useRoute()
const router = useRouter()
const figuresStore = useFiguresStore()
const { t, locale } = useI18n()
const api = useApi()

// Search mode: 'keyword' | 'semantic'
const searchMode = ref<'keyword' | 'semantic'>('keyword')

// Search state
const searchQuery = ref(route.query.q as string || '')
const currentPage = ref(Number(route.query.page) || 1)
const pageSize = 20

// Enhanced filter state (synced with URL)
const filters = ref({
  era: route.query.era as string || '',
  historical_domain: route.query.historical_domain as string || '',
  domain: route.query.domain as string || '',
  gender: route.query.gender as string || '',
  ethnicity: route.query.ethnicity as string || '',
  theme: route.query.theme as string || '',  // P4 theme: TECH/WOMEN/ETHNIC/MED/COMP
  // International filters
  nationality: route.query.nationality as string || '',
  civilization_sphere: route.query.civilization_sphere as string || '',
  time_period_standardized: route.query.time_period_standardized as string || '',
  wiki_id: route.query.wiki_id as string || '',
  primary_language: route.query.primary_language as string || '',
  intellectual_tradition: route.query.intellectual_tradition as string || '',
  cross_cultural_impact: route.query.cross_cultural_impact as string || '',
})

// Semantic search specific
const semanticResults = ref<any[]>([])
const semanticLoading = ref(false)
const semanticTotal = ref(0)
const semanticPage = ref(1)
const semanticPageSize = 20

// Watch for filter/search changes to update URL (only for keyword mode)
watch([searchQuery, filters, currentPage], () => {
  if (searchMode.value === 'keyword') {
    const query: Record<string, string> = {}
    if (searchQuery.value) query.q = searchQuery.value
    if (currentPage.value > 1) query.page = String(currentPage.value)
    Object.entries(filters.value).forEach(([key, value]) => {
      if (value) query[key] = value
    })
    router.replace({ query })
  }
}, { deep: true })

// Watch for semantic search query changes
watch([() => searchMode.value, searchQuery], async ([newMode]) => {
  if (newMode === 'semantic' && searchQuery.value) {
    await performSemanticSearch()
  }
})

// Fetch data for keyword search
const fetchFigures = async () => {
  await figuresStore.fetchFigures({
    page: currentPage.value,
    page_size: pageSize,
    search: searchQuery.value || undefined,
    lang: locale.value,
    ...filters.value,
  })
}

// Semantic search - ENHANCED for batch H-322 to H-361
const performSemanticSearch = async () => {
  if (!searchQuery.value.trim()) return
  
  semanticLoading.value = true
  try {
    // Try enhanced semantic search first
    const response = await api.get('/api/v1/scenarios/batch/semantic-search', {
      params: {
        q: searchQuery.value,
        lang: locale.value,
        top_k: semanticPageSize,
      }
    })
    semanticResults.value = response.data?.data || []
    semanticTotal.value = response.data?.meta?.total || semanticResults.value.length || 0
  } catch (error) {
    console.error('Enhanced semantic search error (fallback to standard):', error)
    // Fallback to standard semantic search
    try {
      const response = await api.get('/api/v1/scenarios/semantic-search', {
        params: {
          q: searchQuery.value,
          lang: locale.value,
          top_k: semanticPageSize,
        }
      })
      semanticResults.value = response.data?.data || []
      semanticTotal.value = response.data?.meta?.total || semanticResults.value.length || 0
    } catch (fallbackError) {
      console.error('Standard semantic search also failed:', fallbackError)
      semanticResults.value = []
      semanticTotal.value = 0
    }
  } finally {
    semanticLoading.value = false
  }
}

// Search handler
const handleSearch = async () => {
  if (searchMode.value === 'keyword') {
    currentPage.value = 1
    await fetchFigures()
  } else {
    semanticPage.value = 1
    await performSemanticSearch()
  }
}

// Filter change handler
const handleFilterChange = async (newFilters: typeof filters.value) => {
  filters.value = newFilters
  if (searchMode.value === 'keyword') {
    currentPage.value = 1
    await fetchFigures()
  }
}

// Clear all filters
const clearFilters = async () => {
  filters.value = {
    era: '',
    historical_domain: '',
    domain: '',
    gender: '',
    ethnicity: '',
    theme: '',
    // International filters
    nationality: '',
    civilization_sphere: '',
    time_period_standardized: '',
    wiki_id: '',
    primary_language: '',
    intellectual_tradition: '',
    cross_cultural_impact: '',
  }
  if (searchMode.value === 'keyword') {
    currentPage.value = 1
    await fetchFigures()
  }
}

// Mode change handler
const handleModeChange = async (newMode: 'keyword' | 'semantic') => {
  searchMode.value = newMode
  if (newMode === 'semantic' && searchQuery.value) {
    await performSemanticSearch()
  }
}

// Initial load
onMounted(async () => {
  await fetchFigures()
})

// Tag labels for display
const tagLabels: Record<string, Record<string, string>> = {
  era: {
    'Pre-Qin': '先秦',
    'Qin-Han': '秦汉',
    'Three-Kingdoms-Jin': '三国两晋',
    'Northern-Southern': '南北朝',
    'Sui-Tang': '隋唐',
    'Song-Yuan': '宋元',
    'Ming-Qing': '明清',
    'Modern-Early': '近代',
    'Modern': '现代',
  },
  historical_domain: {
    'Military': '军事',
    'Philosophy': '哲学',
    'Governance': '治理',
    'Science_Tech': '科技',
    'Historiography': '史学',
    'Literature_Arts': '文学艺术',
    'Religion': '宗教',
    'Education': '教育',
    'Economics': '经济',
    'Ethics': '伦理',
  },
  domain: {
    'Strategic': '战略',
    'Analytical': '分析',
    'Collaborative': '协作',
    'Operational': '操作',
    'Systems': '系统',
    'Creative': '创新',
    'Personal': '个人',
  },
  gender: {
    'Male': '男性',
    'Female': '女性',
  },
  ethnicity: {
    'Han': '汉族',
    'Minority': '少数民族',
  },
}

const getTagLabel = (category: string, value: string) => {
  return tagLabels[category]?.[value] || value
}

const activeFiltersCount = computed(() => {
  return Object.values(filters.value).filter(v => v).length
})
</script>

<style scoped>
.figures-view {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.search-header {
  margin-bottom: 30px;
}

.search-container {
  display: flex;
  gap: 20px;
  align-items: center;
}

.search-modes {
  display: flex;
  gap: 10px;
}

.mode-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.mode-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.search-input-container {
  display: flex;
  gap: 10px;
  flex: 1;
}

.search-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.search-btn {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.main-content {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 30px;
}

.sidebar {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.content {
  min-height: 400px;
}

.active-filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.filter-count {
  color: #666;
  font-size: 14px;
}

.clear-btn {
  padding: 4px 12px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.loading {
  padding: 40px 0;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.results {
  min-height: 400px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.results-count {
  color: #666;
  font-size: 14px;
}

.figures-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.no-results {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.no-results h3 {
  margin-bottom: 10px;
  color: #333;
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    position: static;
  }
  
  .search-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-modes {
    justify-content: center;
  }
}
</style>