<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import { useI18n } from '../composables/useI18n'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const raw = ref('')
const loading = ref(true)
const notFound = ref(false)

const stripFrontmatter = (s: string) => {
  if (s.startsWith('---')) {
    const end = s.indexOf('\n---', 3)
    if (end !== -1) return s.slice(s.indexOf('\n', end + 1) + 1)
  }
  return s
}

const body = computed(() => stripFrontmatter(raw.value))
const title = computed(() => {
  const m = raw.value.match(/^#\s+(.+)$/m)
  return m ? m[1].trim() : String(route.params.id || '')
})
const html = computed(() => {
  if (!body.value) return ''
  // 去掉与页面标题重复的首个 H1
  const noH1 = body.value.replace(/^#\s+.+\n?/, '')
  return marked.parse(noH1, { gfm: true, breaks: false }) as string
})

const load = async () => {
  const id = String(route.params.id || '')
  loading.value = true
  notFound.value = false
  try {
    const res = await fetch(`${import.meta.env.BASE_URL}templates/${encodeURIComponent(id)}.md`)
    if (!res.ok) {
      notFound.value = true
      raw.value = ''
    } else {
      raw.value = await res.text()
    }
  } catch {
    notFound.value = true
    raw.value = ''
  }
  loading.value = false
}

onMounted(load)
watch(() => route.params.id, load)
</script>

<template>
  <div class="pt-container pb-20 pt-8">
    <button @click="router.push({ name: 'templates' })"
            class="mb-6 inline-flex items-center gap-2 text-sm text-parchment/50 transition-colors hover:text-gold-300">
      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      {{ t('返回模板库', 'Back to templates') }}
    </button>

    <div v-if="loading" class="flex min-h-[40vh] items-center justify-center">
      <div class="h-10 w-10 animate-spin rounded-full border-2 border-gold-500/25 border-t-gold-400"></div>
    </div>

    <div v-else-if="notFound" class="pt-panel mx-auto mt-16 max-w-lg px-8 py-14 text-center">
      <div class="mb-3 text-4xl opacity-70">🗂️</div>
      <h1 class="pt-h3 mb-2 text-parchment/90">{{ t('未找到该模板', 'Template not found') }}</h1>
      <p class="mb-5 font-mono text-xs text-parchment/40">{{ route.params.id }}</p>
      <button @click="router.push({ name: 'templates' })" class="pt-btn-ghost">{{ t('返回模板库', 'Back') }}</button>
    </div>

    <article v-else class="pt-panel overflow-hidden">
      <header class="relative overflow-hidden border-b border-white/[0.08] px-7 py-8 sm:px-10 sm:py-10">
        <div aria-hidden="true"
             class="pointer-events-none absolute -top-24 right-0 h-64 w-64 rounded-full bg-gold-500/10 blur-3xl"></div>
        <div class="relative mb-3 flex flex-wrap items-center gap-2">
          <span class="pt-code">{{ String(route.params.id || '').toUpperCase() }}</span>
          <span class="pt-chip-gold">{{ t('复盘模板', 'Review template') }}</span>
        </div>
        <h1 class="pt-h1 !text-3xl sm:!text-4xl">{{ title }}</h1>
      </header>
      <div class="pt-prose px-7 py-8 sm:px-10 sm:py-10" v-html="html"></div>
    </article>
  </div>
</template>
