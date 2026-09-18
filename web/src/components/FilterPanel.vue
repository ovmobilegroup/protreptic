<script setup lang="ts">
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useI18n } from '../composables/useI18n'

interface Props {
  filters: Record<string, string>
  tagLabels: Record<string, Record<string, string>>
}
const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'filter-change', filters: Record<string, string>): void
  (e: 'clear-filters'): void
}>()
const { t } = useI18n()

const isOpen = ref(false)
const root = ref<HTMLElement | null>(null)

// 仅展示有选项的类目
const tabs = computed(() =>
  Object.entries(props.tagLabels)
    .filter(([, opts]) => opts && Object.keys(opts).length > 0)
    .map(([key, opts]) => ({
      key,
      label: {
        era: t('时代', 'Era'),
        historical_domain: t('历史领域', 'Domain'),
        domain: t('思维领域', 'Thinking'),
        gender: t('性别', 'Gender'),
        ethnicity: t('民族', 'Ethnicity'),
      }[key] || key,
      count: opts[props.filters[key]] ? 1 : 0,
    }))
)

const activeTab = ref<string>('')
const currentOptions = computed(() =>
  Object.entries(props.tagLabels[activeTab.value] || {}).map(([value, label]) => ({ value, label }))
)

const activeCount = computed(() => Object.values(props.filters).filter((v) => v).length)

const select = (value: string) => {
  emit('filter-change', { ...props.filters, [activeTab.value]: value })
  isOpen.value = false
}
const clearCategory = () => {
  emit('filter-change', { ...props.filters, [activeTab.value]: '' })
}

const toggle = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value && !activeTab.value) activeTab.value = tabs.value[0]?.key || ''
}

const onClickOutside = (e: MouseEvent) => {
  if (root.value && !root.value.contains(e.target as Node)) isOpen.value = false
}
onMounted(() => document.addEventListener('click', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <div ref="root" class="relative">
    <button
      @click.stop="toggle"
      class="pt-btn-ghost"
      aria-haspopup="true"
      :aria-expanded="isOpen"
    >
      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 5h18M7 12h10M10 19h4" />
      </svg>
      <span>{{ t('筛选', 'Filters') }}</span>
      <span v-if="activeCount > 0"
            class="grid h-5 min-w-[20px] place-items-center rounded-full bg-gold-500 px-1 text-[11px] font-bold text-ink-950">
        {{ activeCount }}
      </span>
    </button>

    <transition
      enter-active-class="transition duration-200 ease-silk"
      enter-from-class="opacity-0 -translate-y-1 scale-[.98]"
      leave-active-class="transition duration-150 ease-in"
      leave-to-class="opacity-0 scale-[.98]"
    >
      <div v-if="isOpen"
           class="pt-panel absolute right-0 z-50 mt-2 w-[22rem] overflow-hidden p-0 shadow-glow">
        <!-- 类目 -->
        <div class="flex gap-1 overflow-x-auto border-b border-white/10 p-2">
          <button
            v-for="tab in tabs" :key="tab.key"
            @click="activeTab = tab.key"
            class="relative whitespace-nowrap rounded-lg px-3 py-1.5 text-xs font-medium transition-colors"
            :class="activeTab === tab.key ? 'bg-gold-500/12 text-gold-300' : 'text-parchment/55 hover:text-parchment'"
          >
            {{ tab.label }}
            <span v-if="tab.count" class="ml-1 text-gold-400">•</span>
          </button>
        </div>

        <!-- 选项 -->
        <div class="max-h-80 overflow-y-auto p-2">
          <button
            v-if="props.filters[activeTab]"
            @click="clearCategory"
            class="mb-1 flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-sm
                   text-gold-300 transition-colors hover:bg-gold-500/10"
          >
            <span class="grid h-4 w-4 place-items-center rounded-full border border-gold-400/60">
              <span class="h-2 w-2 rounded-full bg-gold-400"></span>
            </span>
            {{ t('不限（清除）', 'Any (clear)') }}
          </button>

          <button
            v-for="opt in currentOptions" :key="opt.value"
            @click="select(opt.value)"
            class="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-sm transition-colors"
            :class="props.filters[activeTab] === opt.value
              ? 'bg-gold-500/10 text-gold-200'
              : 'text-parchment/70 hover:bg-white/5 hover:text-parchment'"
          >
            <span class="grid h-4 w-4 shrink-0 place-items-center rounded-full border"
                  :class="props.filters[activeTab] === opt.value ? 'border-gold-400' : 'border-white/20'">
              <span v-if="props.filters[activeTab] === opt.value" class="h-2 w-2 rounded-full bg-gold-400"></span>
            </span>
            <span class="truncate">{{ opt.label }}</span>
          </button>
        </div>

        <div class="flex items-center justify-between border-t border-white/10 px-3 py-2">
          <button @click="emit('clear-filters')"
                  class="text-xs text-parchment/45 transition-colors hover:text-gold-300">
            {{ t('清除全部', 'Clear all') }}
          </button>
          <button @click="isOpen = false" class="text-xs text-parchment/45 transition-colors hover:text-parchment">
            {{ t('关闭', 'Close') }}
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>
