<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import { useI18n } from '../composables/useI18n'
import { SEO_ORIGIN, buildJsonLd, setSeo, truncateSeo } from '../composables/useSeo'

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

// 摘要取正文首个非空段落（跳过标题/列表/表格/引用/代码围栏行）。
const firstParagraph = (text: string): string => {
  for (const line of text.split('\n')) {
    const stripped = line.trim().replace(/^>\s*/, '')
    if (!stripped) continue
    if (stripped.startsWith('#') || stripped.startsWith('|') || stripped.startsWith('```')) continue
    if (stripped.startsWith('- ') || stripped.startsWith('* ')) continue
    return stripped.replace(/[*`]/g, '').replace(/\[([^\]]+)\]\([^)]*\)/g, '$1').trim()
  }
  return ''
}

// 模板页 head：标题取 markdown 的第一个 H1，摘要取首个正文段落（与预渲染 Article 同口径）。
const applySeo = () => {
  const id = String(route.params.id || '')
  const name = title.value
  const description = truncateSeo(firstParagraph(body.value) || `${name}：历史经典案例复盘模板。`)
  setSeo({
    title: name,
    description,
    path: `templates/${id}`,
    jsonLd: buildJsonLd('template', { name, description, path: `templates/${id}` }),
  })
}

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
  if (!notFound.value) applySeo()
}

onMounted(load)
watch(() => route.params.id, load)

/* ---------------- Phase30-B5：导出（Markdown 下载 / 打印 PDF） ---------------- */

// 下载的就是服务端那份 `templates/{id}.md` 原文（fetch 到 raw 后原样落盘），
// 不做任何再序列化 —— 否则"下载文件"和仓库里的文件会悄悄分叉。
const byteLength = computed(() => new TextEncoder().encode(raw.value).length)
const sizeLabel = computed(() => `${(byteLength.value / 1024).toFixed(1)} KB`)

const downloadMarkdown = () => {
  const id = String(route.params.id || '')
  if (!raw.value) return
  const blob = new Blob([raw.value], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${id}.md`
  a.rel = 'noopener'
  document.body.appendChild(a)
  a.click()
  a.remove()
  window.setTimeout(() => URL.revokeObjectURL(url), 5000)
}

// 浏览器打印：样式全部走 style.css 的 @media print（隐藏导航/页脚，白底黑字，表格留框，
// 标题不落单、行不被切断），这里不注入任何行内样式，保证打印预览和导出 PDF 同一套规则。
const printTemplate = () => window.print()

// 纸上页脚：纸质件脱离站点后仍能回溯到线上原文
const printUrl = computed(() => {
  const id = String(route.params.id || '')
  return `${SEO_ORIGIN}${import.meta.env.BASE_URL}templates/${id}/`
})
</script>

<template>
  <div class="pt-container pb-20 pt-8">
    <button @click="router.push({ name: 'templates' })"
            class="pt-print-hide mb-6 inline-flex items-center gap-2 text-sm text-parchment/50 transition-colors hover:text-gold-300">
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

        <div class="pt-print-hide relative mt-6 flex flex-wrap items-center gap-3">
          <button type="button" class="pt-btn-gold" @click="printTemplate">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M6 9V3h12v6M6 18H4v-6h16v6h-2M8 14h8v7H8z" />
            </svg>
            {{ t('打印 / 导出 PDF', 'Print / Export PDF') }}
          </button>
          <button type="button" class="pt-btn-ghost" @click="downloadMarkdown">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 3v12m0 0l-4-4m4 4l4-4M4 20h16" />
            </svg>
            {{ t('下载 Markdown', 'Download Markdown') }}
            <span class="pt-code ml-1">{{ sizeLabel }}</span>
          </button>
          <span class="text-xs leading-relaxed text-parchment/40">
            {{ t('导出 PDF 走浏览器打印：目标选“另存为 PDF”，勾选“页眉和页脚”即可带页码。',
                 'PDF export uses the browser print dialog: choose “Save as PDF”; enable headers & footers for page numbers.') }}
          </span>
        </div>
      </header>

      <div class="pt-print-only border-b border-white/[0.08] px-7 pb-3 pt-5 text-xs text-parchment/60 sm:px-10">
        Protreptic · {{ t('复盘模板', 'Review template') }} {{ String(route.params.id || '').toUpperCase() }} · {{ printUrl }}
      </div>
      <div class="pt-prose px-7 py-8 sm:px-10 sm:py-10" v-html="html"></div>
    </article>
  </div>
</template>
