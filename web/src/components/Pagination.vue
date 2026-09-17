<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'

const props = defineProps<{
  currentPage: number
  totalPages: number
}>()

const router = useRouter()
const { t } = useI18n()

const pages = computed(() => {
  const pages: (number | '...')[] = []
  const total = props.totalPages
  const current = props.currentPage

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    const start = Math.max(2, current - 1)
    const end = Math.min(total - 1, current + 1)
    for (let i = start; i <= end; i++) pages.push(i)
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  return pages
})

const goToPage = (page: number | '...') => {
  if (page === '...') return
  router.push({ query: { ...router.currentRoute.value.query, page } })
}
</script>

<template>
  <nav class="flex items-center justify-center gap-2 py-6" aria-label="Pagination">
    <button
      @click="goToPage(props.currentPage - 1)"
      :disabled="props.currentPage === 1"
      class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      :aria-label="t('上一页', 'Previous page')"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>

    <div class="flex items-center gap-1">
      <template v-for="page in pages" :key="page">
        <button
          v-if="page !== '...'"
          @click="goToPage(page)"
          :class="[
            'w-10 h-10 text-sm font-medium rounded-lg transition-colors',
            page === props.currentPage
              ? 'bg-indigo-600 text-white'
              : 'text-gray-700 bg-white border border-gray-300 hover:bg-gray-50'
          ]"
          :aria-label="`${t('第', 'Page')} ${page} ${t('页', '')}`"
          :aria-current="page === props.currentPage ? 'page' : undefined"
        >
          {{ page }}
        </button>
        <span v-else class="px-2 text-gray-400">...</span>
      </template>
    </div>

    <button
      @click="goToPage(props.currentPage + 1)"
      :disabled="props.currentPage === props.totalPages"
      class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      :aria-label="t('下一页', 'Next page')"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </nav>
</template>