<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'
import { useRouter } from 'vue-router'

interface Props {
  figure: {
    code: string
    name: string
    description: string
    modes: number[]
    reason: string
    steps: string[]
    expected: string
    case: string
    era: string | null
    historical_domains: string[]
    domains: string[]
    gender: string | null
    ethnicity: string | null
  }
  lang: 'zh' | 'en'
}

const props = defineProps<Props>()
const router = useRouter()
const { t } = useI18n()

// Domain color mapping
const domainColors: Record<string, string> = {
  Strategic: 'bg-red-100 text-red-700',
  Analytical: 'bg-blue-100 text-blue-700',
  Collaborative: 'bg-green-100 text-green-700',
  Operational: 'bg-yellow-100 text-yellow-700',
  Systems: 'bg-purple-100 text-purple-700',
  Creative: 'bg-pink-100 text-pink-700',
  Personal: 'bg-indigo-100 text-indigo-700',
}

// Historical domain color mapping
const histDomainColors: Record<string, string> = {
  Military: 'bg-red-100 text-red-700',
  Philosophy: 'bg-blue-100 text-blue-700',
  Governance: 'bg-green-100 text-green-700',
  Science_Tech: 'bg-yellow-100 text-yellow-700',
  Historiography: 'bg-purple-100 text-purple-700',
  Literature_Arts: 'bg-pink-100 text-pink-700',
  Religion: 'bg-indigo-100 text-indigo-700',
  Education: 'bg-teal-100 text-teal-700',
  Economics: 'bg-orange-100 text-orange-700',
  Ethics: 'bg-gray-100 text-gray-700',
}

// Era labels
const eraLabels: Record<string, { zh: string; en: string }> = {
  'Pre-Qin': { zh: '先秦', en: 'Pre-Qin' },
  'Qin-Han': { zh: '秦汉', en: 'Qin-Han' },
  'Three-Kingdoms-Jin': { zh: '三国两晋', en: 'Three Kingdoms & Jin' },
  'Northern-Southern': { zh: '南北朝', en: 'Northern & Southern Dynasties' },
  'Sui-Tang': { zh: '隋唐', en: 'Sui-Tang' },
  'Song-Yuan': { zh: '宋元', en: 'Song-Yuan' },
  'Ming-Qing': { zh: '明清', en: 'Ming-Qing' },
  'Modern-Early': { zh: '近代', en: 'Early Modern' },
  'Modern': { zh: '现代', en: 'Modern' },
}

const navigateToDetail = () => {
  router.push({ name: 'figure-detail', params: { code: props.figure.code } })
}

const getEraLabel = () => {
  if (!props.figure.era) return ''
  return eraLabels[props.figure.era]?.[props.lang] || props.figure.era
}

const getDomainLabel = (domain: string) => {
  return domain // Keep English for domain tags for consistency
}

const getModeLabel = (modeId: number) => {
  return modeId.toString()
}

const getHistDomainLabel = (domain: string) => {
  return domain
}
</script>

<template>
  <article
    @click="navigateToDetail"
    class="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-lg hover:border-indigo-300 transition-all duration-200 cursor-pointer group"
    tabindex="0"
    @keydown.enter="navigateToDetail"
    @keydown.space.prevent="navigateToDetail"
  >
    <!-- Header with Code and Era -->
    <div class="px-5 py-4 border-b border-gray-100 flex items-start justify-between">
      <div class="flex items-center gap-2">
        <span class="text-xs font-mono font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
          {{ props.figure.code }}
        </span>
        <span v-if="props.figure.era" class="text-xs text-gray-500 bg-gray-50 px-2 py-0.5 rounded">
          {{ getEraLabel() }}
        </span>
      </div>
    </div>

    <!-- Content -->
    <div class="p-5">
      <!-- Name -->
      <h3 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-indigo-600 transition-colors">
        {{ props.figure.name }}
      </h3>

      <!-- Description -->
      <p v-if="props.figure.description" class="text-sm text-gray-600 mb-4 line-clamp-3">
        {{ props.figure.description }}
      </p>

      <!-- Thinking Modes -->
      <div v-if="props.figure.modes && props.figure.modes.length > 0" class="mb-4">
        <div class="flex flex-wrap gap-1.5">
          <span
            v-for="modeId in props.figure.modes.slice(0, 4)"
            :key="modeId"
            class="px-2 py-0.5 text-xs font-medium rounded-full"
            :class="domainColors[getModeLabel(modeId)] || 'bg-gray-100 text-gray-700'"
          >
            #{{ modeId }}
          </span>
          <span v-if="props.figure.modes.length > 4" class="px-2 py-0.5 text-xs text-gray-500 bg-gray-100 rounded-full">
            +{{ props.figure.modes.length - 4 }}
          </span>
        </div>
      </div>

      <!-- Tags Row -->
      <div class="flex flex-wrap gap-1.5 mb-4">
        <!-- Historical Domains -->
        <span
          v-for="domain in props.figure.historical_domains.slice(0, 2)"
          :key="domain"
          class="px-2 py-0.5 text-xs font-medium rounded"
          :class="histDomainColors[domain] || 'bg-gray-100 text-gray-700'"
        >
          {{ getHistDomainLabel(domain) }}
        </span>
        <span v-if="props.figure.historical_domains.length > 2" class="px-2 py-0.5 text-xs text-gray-500 bg-gray-100 rounded">
          +{{ props.figure.historical_domains.length - 2 }}
        </span>

        <!-- Era badge (if not shown in header) -->
        <span v-if="props.figure.era" class="px-2 py-0.5 text-xs text-gray-500 bg-gray-100 rounded">
          {{ eraLabels[props.figure.era]?.[props.lang] || props.figure.era }}
        </span>
      </div>

      <!-- Gender/Ethnicity -->
      <div class="flex items-center gap-2 text-xs text-gray-400">
        <span v-if="props.figure.gender" class="flex items-center gap-1">
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" />
          </svg>
          {{ props.figure.gender }}
        </span>
        <span v-if="props.figure.ethnicity" class="flex items-center gap-1">
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l3 3a1 1 0 001.414 0l3-3a1 1 0 00.293-.707V6z" clip-rule="evenodd" />
          </svg>
          {{ props.figure.ethnicity }}
        </span>
      </div>
    </div>

    <!-- Hover Action Hint -->
    <div class="px-5 pb-4 pt-2 border-t border-gray-50 opacity-0 group-hover:opacity-100 transition-opacity">
      <button
        @click.stop="navigateToDetail"
        class="w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors"
      >
        {{ props.lang === 'zh' ? '查看详情' : 'View Details' }}
        <svg class="inline w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  </article>
</template>

<style scoped>
/* Line clamp utilities */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>