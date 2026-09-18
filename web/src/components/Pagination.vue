<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'

const props = defineProps<{
  currentPage: number
  totalPages: number
}>()

const { t } = useI18n()
const emit = defineEmits<{ (e: 'page-change', page: number): void }>()

const pages = computed(() => {
  const out: (number | '...')[] = []
  const total = props.totalPages
  const current = props.currentPage
  if (total <= 7) {
    for (let i = 1; i <= total; i++) out.push(i)
  } else {
    out.push(1)
    if (current > 3) out.push('...')
    const start = Math.max(2, current - 1)
    const end = Math.min(total - 1, current + 1)
    for (let i = start; i <= end; i++) out.push(i)
    if (current < total - 2) out.push('...')
    out.push(total)
  }
  return out
})

const goToPage = (page: number | '...') => {
  if (page === '...') return
  emit('page-change', page)
}
</script>

<template>
  <nav class="flex items-center justify-center gap-1.5" aria-label="分页">
    <button
      @click="goToPage(props.currentPage - 1)"
      :disabled="props.currentPage === 1"
      class="grid h-10 w-10 place-items-center rounded-xl border border-white/10 bg-white/[.03]
             text-parchment/70 transition-all duration-300 ease-silk
             hover:border-gold-500/40 hover:text-gold-300
             disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-white/10 disabled:hover:text-parchment/70"
      :aria-label="t('上一页', 'Previous page')"
    >
      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>

    <template v-for="page in pages" :key="page">
      <button
        v-if="page !== '...'"
        @click="goToPage(page)"
        class="grid h-10 min-w-10 place-items-center rounded-xl px-3 text-sm font-medium transition-all duration-300 ease-silk"
        :class="page === props.currentPage
          ? 'bg-gradient-to-b from-gold-400/90 to-gold-600 text-ink-950 shadow-glow'
          : 'border border-white/10 bg-white/[.03] text-parchment/70 hover:border-gold-500/40 hover:text-gold-300'"
        :aria-current="page === props.currentPage ? 'page' : undefined"
      >
        {{ page }}
      </button>
      <span v-else class="px-1 text-parchment/30">…</span>
    </template>

    <button
      @click="goToPage(props.currentPage + 1)"
      :disabled="props.currentPage === props.totalPages"
      class="grid h-10 w-10 place-items-center rounded-xl border border-white/10 bg-white/[.03]
             text-parchment/70 transition-all duration-300 ease-silk
             hover:border-gold-500/40 hover:text-gold-300
             disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-white/10 disabled:hover:text-parchment/70"
      :aria-label="t('下一页', 'Next page')"
    >
      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </nav>
</template>
