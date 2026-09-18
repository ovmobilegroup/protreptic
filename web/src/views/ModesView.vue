<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from '../composables/useI18n'

const { t, locale } = useI18n()

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
const visibleCount = ref(120)
const query = ref('')
const activeCategory = ref('')

const fetchStaticModes = async (): Promise<ModeItem[]> => {
  const shards = await Promise.all(
    Array.from({ length: MODE_INDEX_SHARDS }, async (_, i) => {
      const r = await fetch(`${import.meta.env.BASE_URL}data/modes/index-${i}.json`)
      if (!r.ok) throw new Error(`data/modes/index-${i}.json HTTP ${r.status}`)
      const d = await r.json()
      if (!Array.isArray(d)) throw new Error(`data/modes/index-${i}.json 结构异常`)
      return d
    })
  )
  return shards.flat().map((m: any) => ({
    id: String(m.mode_code ?? ''),
    name_zh: m.name_zh ?? '', name_en: m.name_en ?? '',
    domain_zh: m.domain_zh ?? '', domain_en: m.domain_en ?? '',
    category: m.category ?? '', figure_code: m.figure_code ?? '', figure_name: m.figure_name ?? '',
  }))
}

const fetchApiModes = async (): Promise<ModeItem[]> => {
  const r = await fetch('/api/v1/modes')
  if (!r.ok) throw new Error(`/api/v1/modes HTTP ${r.status}`)
  const d = await r.json()
  return (d.data || []).map((m: any) => ({
    id: String(m.id ?? ''), name_zh: m.name ?? '', name_en: m.name_en ?? '',
    domain_zh: m.domain ?? '', domain_en: m.domain_en ?? '',
    description_zh: m.description ?? '', description_en: m.description_en ?? '',
    formula_zh: m.formula ?? '', formula_en: m.formula_en ?? '',
  }))
}

const fetchModes = async () => {
  loading.value = true; error.value = null
  try {
    modes.value = DATA_MODE === 'static' ? await fetchStaticModes() : await fetchApiModes()
    visibleCount.value = 120
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to fetch modes'
  } finally { loading.value = false }
}

const figureCount = computed(() => new Set(modes.value.map((m) => m.figure_code).filter(Boolean)).size)

// 分类聚合
const categories = computed(() => {
  const c: Record<string, number> = {}
  for (const m of modes.value) if (m.category) c[m.category] = (c[m.category] || 0) + 1
  return Object.entries(c).sort((a, b) => b[1] - a[1])
})

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  return modes.value.filter((m) => {
    if (activeCategory.value && m.category !== activeCategory.value) return false
    if (!q) return true
    return [m.id, m.name_zh, m.name_en, m.domain_zh, m.figure_name, m.category]
      .some((v) => String(v || '').toLowerCase().includes(q))
  })
})
const visibleModes = computed(() => filtered.value.slice(0, visibleCount.value))

onMounted(fetchModes)
</script>

<template>
  <div class="pt-container pb-16 pt-10">
    <!-- Hero -->
    <section class="mb-8">
      <div class="mb-3 flex items-center gap-3">
        <span class="pt-hairline w-10"></span>
        <span class="pt-code">{{ t('思维模式 · 可执行方法', 'THINKING MODES · EXECUTABLE METHODS') }}</span>
      </div>
      <h1 class="pt-h1"><span class="pt-gradient-text">{{ t('思维模式库', 'Thinking Modes') }}</span></h1>
      <p class="mt-4 max-w-2xl text-base leading-relaxed text-parchment/55">
        <template v-if="DATA_MODE === 'static'">
          {{ t(
            `${modes.length} 条思维模式实例，源自 ${figureCount} 位历史人物——每条都出自具体人物与具体文本。`,
            `${modes.length} mode instances from ${figureCount} historical figures.`
          ) }}
        </template>
        <template v-else>
          {{ t(`${modes.length} 种可执行的思维模式`, `${modes.length} executable thinking modes`) }}
        </template>
      </p>
    </section>

    <!-- 检索 + 分类 -->
    <section class="pt-panel mb-8 p-4">
      <div class="relative mb-4">
        <svg class="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-parchment/35"
             fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
        </svg>
        <input v-model="query" type="text"
               :placeholder="t('搜索模式名、人物、领域…', 'Search mode, figure, domain…')"
               class="pt-input pl-11" />
      </div>

      <div v-if="categories.length" class="flex flex-wrap gap-2">
        <button @click="activeCategory = ''"
                class="pt-chip" :class="!activeCategory ? 'border-gold-500/50 bg-gold-500/15 text-gold-200' : 'border-white/10 bg-white/[.04] text-parchment/60 hover:text-parchment'">
          {{ t('全部', 'All') }} · {{ modes.length }}
        </button>
        <button v-for="[cat, n] in categories" :key="cat" @click="activeCategory = cat"
                class="pt-chip"
                :class="activeCategory === cat ? 'border-gold-500/50 bg-gold-500/15 text-gold-200' : 'border-white/10 bg-white/[.04] text-parchment/60 hover:text-parchment'">
          {{ cat }} · {{ n }}
        </button>
      </div>
    </section>

    <!-- 结果 -->
    <div v-if="loading" class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div v-for="i in 8" :key="i" class="rounded-2xl border border-white/10 bg-white/[.03] p-5">
        <div class="pt-skeleton mb-3 h-4 w-20"></div>
        <div class="pt-skeleton mb-2 h-6 w-2/3"></div>
        <div class="pt-skeleton h-3.5 w-full"></div>
      </div>
    </div>

    <div v-else-if="error" class="pt-panel px-6 py-12 text-center text-red-300/85">
      {{ error }}
    </div>

    <template v-else>
      <div class="pt-stagger grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <article v-for="m in visibleModes" :key="m.id + '-' + (m.figure_code || '')"
                 class="group relative flex flex-col rounded-2xl border border-white/10 bg-white/[.03] p-5
                        transition-all duration-500 ease-silk hover:-translate-y-1 hover:border-jade-400/40 hover:bg-white/[.055]">
          <div class="mb-3 flex items-start justify-between gap-2">
            <span class="pt-code">{{ m.id }}</span>
            <span v-if="m.domain_zh" class="pt-chip-jade shrink-0">
              {{ locale === 'zh' ? m.domain_zh : (m.domain_en || m.domain_zh) }}
            </span>
          </div>
          <h3 class="font-display text-base font-bold leading-snug text-parchment transition-colors group-hover:text-gold-200">
            {{ locale === 'zh' ? m.name_zh : (m.name_en || m.name_zh) }}
          </h3>
          <p v-if="(locale === 'zh' ? m.description_zh : m.description_en)"
             class="mt-2 text-sm leading-relaxed text-parchment/50 line-clamp-3">
            {{ locale === 'zh' ? m.description_zh : m.description_en }}
          </p>
          <p v-else-if="m.figure_name" class="mt-2 text-sm text-parchment/50">
            {{ t('代表人物', 'Figure') }} · <span class="text-gold-300/85">{{ m.figure_name }}</span>
          </p>
          <div class="mt-auto flex flex-wrap items-center gap-1.5 pt-4">
            <span v-if="m.figure_name" class="pt-chip-mute">{{ m.figure_name }}</span>
            <span v-if="m.category" class="pt-chip-mute">{{ m.category }}</span>
          </div>
        </article>
      </div>

      <div v-if="visibleCount < filtered.length" class="mt-10 text-center">
        <button @click="visibleCount += 240" class="pt-btn-ghost">
          {{ t(`显示更多（剩余 ${filtered.length - visibleCount} 条）`, `Show more (${filtered.length - visibleCount} left)`) }}
        </button>
      </div>
      <div v-else-if="!filtered.length" class="pt-panel px-6 py-16 text-center text-parchment/50">
        {{ t('没有匹配的模式', 'No matching modes') }}
      </div>
    </template>
  </div>
</template>
