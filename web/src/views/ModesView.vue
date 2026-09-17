<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from '../composables/useI18n'

const { t, locale } = useI18n()

// 数据源开关：VITE_DATA_MODE=static → 读 public/data/modes/index-*.json（无后端）；
// 否则沿用后端 /api/v1/modes（42 条模式定义）。
const DATA_MODE = import.meta.env.VITE_DATA_MODE ?? 'api'
const MODE_INDEX_SHARDS = 8

interface ModeItem {
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
}

const modes = ref<ModeItem[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
// 2858 条一次性渲染会拖慢移动端：分批显示
const visibleCount = ref(120)

/** 静态模式：8 个摘要分片（md5(mode_code)%8）合并为 2858 条模式实例 */
const fetchStaticModes = async (): Promise<ModeItem[]> => {
  const shards = await Promise.all(
    Array.from({ length: MODE_INDEX_SHARDS }, async (_, i) => {
      const response = await fetch(`${import.meta.env.BASE_URL}data/modes/index-${i}.json`)
      if (!response.ok) throw new Error(`data/modes/index-${i}.json HTTP ${response.status}`)
      const data = await response.json()
      if (!Array.isArray(data)) throw new Error(`data/modes/index-${i}.json 结构异常`)
      return data
    })
  )
  return shards.flat().map((mode: any) => ({
    id: String(mode.mode_code ?? ''),
    name_zh: mode.name_zh ?? '',
    name_en: mode.name_en ?? '',
    domain_zh: mode.domain_zh ?? '',
    domain_en: mode.domain_en ?? '',
    category: mode.category ?? '',
    figure_code: mode.figure_code ?? '',
    figure_name: mode.figure_name ?? '',
  }))
}

/** api 模式：后端 /api/v1/modes 的 42 条模式定义，归一化成同一形状 */
const fetchApiModes = async (): Promise<ModeItem[]> => {
  const response = await fetch('/api/v1/modes')
  if (!response.ok) throw new Error(`/api/v1/modes HTTP ${response.status}`)
  const data = await response.json()
  return (data.data || []).map((mode: any) => ({
    id: String(mode.id ?? ''),
    name_zh: mode.name ?? '',
    name_en: mode.name_en ?? '',
    domain_zh: mode.domain ?? '',
    domain_en: mode.domain_en ?? '',
    description_zh: mode.description ?? '',
    description_en: mode.description_en ?? '',
    formula_zh: mode.formula ?? '',
    formula_en: mode.formula_en ?? '',
  }))
}

const fetchModes = async () => {
  loading.value = true
  error.value = null
  try {
    modes.value = DATA_MODE === 'static' ? await fetchStaticModes() : await fetchApiModes()
    visibleCount.value = 120
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to fetch modes'
  } finally {
    loading.value = false
  }
}

const modeDomainColors: Record<string, string> = {
  '战略': 'bg-red-100 text-red-700',
  '分析': 'bg-blue-100 text-blue-700',
  '协作': 'bg-green-100 text-green-700',
  '操作': 'bg-yellow-100 text-yellow-700',
  '系统': 'bg-purple-100 text-purple-700',
  '创新': 'bg-pink-100 text-pink-700',
  '个人': 'bg-indigo-100 text-indigo-700',
}

const domainColors: Record<string, string> = {
  'Strategic': 'bg-red-100 text-red-700',
  'Analytical': 'bg-blue-100 text-blue-700',
  'Collaborative': 'bg-green-100 text-green-700',
  'Operational': 'bg-yellow-100 text-yellow-700',
  'Systems': 'bg-purple-100 text-purple-700',
  'Creative': 'bg-pink-100 text-pink-700',
  'Personal': 'bg-indigo-100 text-indigo-700',
}

const visibleModes = computed(() => modes.value.slice(0, visibleCount.value))
const figureCount = computed(() => new Set(modes.value.map(m => m.figure_code).filter(Boolean)).size)
const summary = computed(() => {
  if (!modes.value.length) return ''
  if (DATA_MODE === 'static') {
    return t(
      `${modes.value.length} 条思维模式实例，源自 ${figureCount.value} 位历史人物`,
      `${modes.value.length} thinking-mode instances from ${figureCount.value} historical figures`
    )
  }
  return t(`${modes.value.length} 种可执行的思维模式`, `${modes.value.length} executable thinking modes`)
})

onMounted(async () => {
  await fetchModes()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <h1 class="text-3xl font-bold text-gray-900">{{ t('思维模式库', 'Thinking Modes Library') }}</h1>
        <p class="mt-1 text-gray-600">{{ summary }}</p>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <ModeCardSkeleton v-for="i in 10" :key="i" />
      </div>

      <div v-else-if="error" class="text-center py-16">
        <p class="text-red-600">{{ error }}</p>
      </div>

      <div v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div v-for="mode in visibleModes" :key="mode.id + '-' + (mode.figure_code || '')" class="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-4">
              <span class="text-xs font-mono font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
                #{{ mode.id }}
              </span>
              <span :class="modeDomainColors[mode.domain_zh] || 'bg-gray-100 text-gray-700'" class="px-2 py-0.5 text-xs font-medium rounded-full">
                {{ locale === 'zh' ? mode.domain_zh : mode.domain_en }}
              </span>
            </div>

            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              {{ locale === 'zh' ? mode.name_zh : mode.name_en }}
            </h3>

            <p v-if="(locale === 'zh' ? mode.description_zh : mode.description_en)" class="text-sm text-gray-600 mb-4 line-clamp-3">
              {{ locale === 'zh' ? mode.description_zh : mode.description_en }}
            </p>
            <p v-else-if="mode.figure_name" class="text-sm text-gray-600 mb-4">
              {{ t('代表人物', 'Figure') }}：{{ mode.figure_name }}
            </p>

            <p v-if="(locale === 'zh' ? mode.formula_zh : mode.formula_en)" class="text-xs text-gray-500 mb-4">
              <strong>{{ t('公式', 'Formula') }}:</strong> {{ locale === 'zh' ? mode.formula_zh : mode.formula_en }}
            </p>
            <p v-else-if="mode.category" class="text-xs text-gray-500 mb-4">
              <strong>{{ t('分类', 'Category') }}:</strong> {{ mode.category }}
            </p>

            <div class="flex flex-wrap gap-1">
              <span v-if="mode.figure_name" class="px-2 py-0.5 text-xs bg-gray-100 text-gray-700 rounded">
                {{ mode.figure_name }}
              </span>
              <span v-if="mode.category" class="px-2 py-0.5 text-xs bg-gray-50 text-gray-500 rounded">
                {{ mode.category }}
              </span>
            </div>
          </div>
        </div>

        <div v-if="visibleCount < modes.length" class="text-center mt-8">
          <button
            @click="visibleCount += 240"
            class="px-6 py-3 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 rounded-lg hover:bg-indigo-50 transition-colors"
          >
            {{ t(`显示更多（剩余 ${modes.length - visibleCount} 条）`, `Show more (${modes.length - visibleCount} left)`) }}
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
