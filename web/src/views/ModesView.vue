<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from '../composables/useI18n'

const { t, locale } = useI18n()

const modes = ref<any[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const fetchModes = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await fetch('/api/v1/modes')
    const data = await response.json()
    modes.value = data.data || []
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

onMounted(async () => {
  await fetchModes()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <h1 class="text-3xl font-bold text-gray-900">{{ t('思维模式库', 'Thinking Modes Library') }}</h1>
        <p class="mt-1 text-gray-600">{{ t('42 种可执行的思维模式，源自 321 位历史人物的智慧', '42 executable thinking modes from the wisdom of 321 historical figures') }}</p>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <ModeCardSkeleton v-for="i in 10" :key="i" />
      </div>

      <div v-else-if="error" class="text-center py-16">
        <p class="text-red-600">{{ error }}</p>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div v-for="mode in modes" :key="mode.id" class="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-shadow">
          <div class="flex items-start justify-between mb-4">
            <span class="text-xs font-mono font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
              #{{ mode.id }}
            </span>
            <span :class="modeDomainColors[mode.domain] || 'bg-gray-100 text-gray-700'" class="px-2 py-0.5 text-xs font-medium rounded-full">
              {{ locale === 'zh' ? mode.domain : mode.domain_en }}
            </span>
          </div>
          
          <h3 class="text-lg font-semibold text-gray-900 mb-2">
            {{ locale === 'zh' ? mode.name : mode.name_en }}
          </h3>
          
          <p class="text-sm text-gray-600 mb-4 line-clamp-3">
            {{ locale === 'zh' ? mode.description : mode.description_en }}
          </p>
          
          <p class="text-xs text-gray-500 mb-4">
            <strong>{{ t('公式', 'Formula') }}:</strong> {{ locale === 'zh' ? mode.formula : mode.formula_en }}
          </p>
          
          <div class="flex flex-wrap gap-1">
            <span v-for="figureId in []" :key="figureId" class="px-2 py-0.5 text-xs bg-gray-100 text-gray-700 rounded">
              关联人物
            </span>
          </div>
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