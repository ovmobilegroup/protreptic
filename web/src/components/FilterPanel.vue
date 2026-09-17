<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from '../composables/useI18n'

interface Props {
  filters: {
    era: string
    historical_domain: string
    domain: string
    gender: string
    ethnicity: string
    theme: string   // P4 theme filtering: TECH/WOMEN/ETHNIC/MED/COMP
    // International filters
    nationality: string
    civilization_sphere: string
    time_period_standardized: string
    wiki_id: string
    primary_language: string
    intellectual_tradition: string
    cross_cultural_impact: string
  }
  tagLabels: Record<string, Record<string, string>>
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'update:filters', filters: typeof props.filters): void
}>()

const { t } = useI18n()

const isOpen = ref(false)
const activeTab = ref<'era' | 'historical_domain' | 'domain' | 'gender' | 'ethnicity' | 'theme' | 'nationality' | 'civilization_sphere' | 'time_period_standardized' | 'wiki_id' | 'primary_language' | 'intellectual_tradition' | 'cross_cultural_impact'>('era')

const tabs = [
  { key: 'era', label: '时代', icon: '📜' },
  { key: 'historical_domain', label: '历史领域', icon: '🏛️' },
  { key: 'domain', label: '思维领域', icon: '🧠' },
  { key: 'gender', label: '性别', icon: '👤' },
  { key: 'ethnicity', label: '民族', icon: '🌍' },
  { key: 'theme', label: '专题', icon: '🎯' },  // P4 theme: TECH/WOMEN/ETHNIC/MED/COMP
  // International filters
  { key: 'nationality', label: '国籍', icon: '🏳️' },
  { key: 'civilization_sphere', label: '文明圈', icon: '🌐' },
  { key: 'time_period_standardized', label: '标准年代', icon: '📅' },
  { key: 'wiki_id', label: 'Wiki ID', icon: '📖' },
  { key: 'primary_language', label: '主语言', icon: '🗣️' },
  { key: 'intellectual_tradition', label: '思想传统', icon: '📚' },
  { key: 'cross_cultural_impact', label: '跨文化影响', icon: '🔄' },
] as const

const filterOptions = computed(() => {
  const options: Record<string, { value: string; label: string }[]> = {}
  
  Object.entries((props.filters as any)).forEach(([category, labels]) => {
    if (typeof labels === 'object' && labels !== null) {
      options[category] = Object.entries(labels as any).map(([value, label]) => ({
        value,
        label: `${label}`,
      }))
    }
  })
  
  return options
})

const handleSelect = (category: keyof typeof props.filters, value: string) => {
  const newFilters = { ...props.filters, [category]: value }
  emit('update:filters', newFilters)
}

const clearCategory = (category: keyof typeof props.filters) => {
  const newFilters = { ...props.filters, [category]: '' }
  emit('update:filters', newFilters)
}

const categoryCount = (category: keyof typeof props.filters) => {
  return props.filters[category] ? 1 : 0
}

const activeCount = computed(() => {
  return Object.values(props.filters).filter(v => v).length
})
</script>

<template>
  <div class="relative">
    <!-- Filter Button -->
    <button
      @click="isOpen = !isOpen"
      class="flex items-center gap-2 px-4 py-3 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
      aria-haspopup="true"
      :aria-expanded="isOpen"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 18a9 9 0 000-18m8 0a9 9 0 000-18m-9 9a9 9 0 000-18m8 0a9 9 0 000-18" />
      </svg>
      <span>{{ t('筛选', 'Filters') }}</span>
      <span v-if="activeCount > 0" class="ml-1 px-2 py-0.5 text-xs bg-indigo-100 text-indigo-700 rounded-full">
        {{ activeCount }}
      </span>
      <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Dropdown Panel -->
    <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" leave-active-class="transition ease-in duration-75" leave-to-class="transform opacity-0 scale-95">
      <div v-if="isOpen" class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
        <!-- Tabs -->
        <div class="border-b border-gray-200 px-2">
          <nav class="flex gap-1 overflow-x-auto pb-2" role="tablist">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              @click="activeTab = tab.key"
              :class="[
                'px-3 py-2 text-sm font-medium rounded-lg transition-colors whitespace-nowrap',
                activeTab === tab.key
                  ? 'bg-indigo-50 text-indigo-700'
                  : 'text-gray-600 hover:bg-gray-50'
              ]"
              :aria-selected="activeTab === tab.key"
              role="tab"
            >
              <span class="flex items-center gap-1">
                <span>{{ tab.icon }}</span>
                <span>{{ t(tab.label, tab.label) }}</span>
                <span v-if="categoryCount(tab.key) > 0" class="ml-1 px-1.5 py-0.5 text-xs bg-indigo-100 text-indigo-700 rounded-full">
                  {{ categoryCount(tab.key) }}
                </span>
              </span>
            </button>
          </nav>
        </div>

        <!-- Content -->
        <div class="max-h-96 overflow-y-auto p-3">
          <div v-if="filterOptions[activeTab].length === 0" class="py-8 text-center text-gray-500">
            {{ t('暂无选项', 'No options available') }}
          </div>
          <div v-else class="space-y-1">
            <label
              v-for="option in filterOptions[activeTab]"
              :key="option.value"
              class="flex items-center gap-3 px-3 py-2 hover:bg-gray-50 rounded-lg cursor-pointer transition-colors"
            >
              <input
                type="radio"
                :name="activeTab"
                :value="option.value"
                :checked="props.filters[activeTab] === option.value"
                @change="() => handleSelect(activeTab, option.value)"
                class="w-4 h-4 text-indigo-600 border-gray-300 focus:ring-indigo-500"
              >
              <span class="text-sm text-gray-700 truncate">{{ option.label }}</span>
            </label>
            
            <!-- Clear option -->
            <label v-if="props.filters[activeTab]" class="flex items-center gap-3 px-3 py-2 hover:bg-red-50 rounded-lg cursor-pointer transition-colors text-red-600">
              <input
                type="radio"
                :name="activeTab"
                value=""
                :checked="!props.filters[activeTab]"
                @change="() => clearCategory(activeTab)"
                class="w-4 h-4 text-red-600 border-gray-300 focus:ring-red-500"
              >
              <span class="text-sm font-medium">{{ t('不限', 'All') }}</span>
            </label>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
/* Hide scrollbar for tabs */
::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}
</style>