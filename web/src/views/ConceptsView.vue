<script setup lang="ts">
/**
 * /concepts 概念索引（Phase30-B2）。
 *
 * 数据源：B1 预计算的 data/graph/concept_graph.json（284 人物 / 13288 概念 / 13552 边）
 * 与 data/modes/by-figure/{code}.json（模式级 key_concepts，用来回答「这个概念在这些人物身上
 * 具体落在哪几条模式」）。人物名只取 data/index.unified.json 的真实字段，缺名就显示编号，
 * 不臆造人名。
 *
 * 事实边界（B1 实测）：13288 个概念里只有 218 个被 2 个及以上人物共享，最多共享 8 人；
 * 因此列表默认按「跨人物（≥2 人）」聚合，另给「全部概念」开关，不做无提示的截断。
 */
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { buildConceptUsage, loadConceptGraph, type ConceptGraphPayload, type ConceptUsage } from '../api/graphData'
import { fetchFigureModes, fetchUnifiedIndex, type UnifiedEntry } from '../api/static'
import { useI18n } from '../composables/useI18n'

interface ModeHit { code: string; name: string; definition: string }
interface FigureUsage { code: string; name: string; era: string; nMods: number; modes: ModeHit[] }

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()

const graph = ref<ConceptGraphPayload | null>(null)
const usage = ref<ConceptUsage[]>([])
const figureMeta = ref<Map<string, UnifiedEntry>>(new Map())
const state = ref<'loading' | 'ready' | 'unavailable'>('loading')

const query = ref('')
const activeQuery = ref('')
const scope = ref<'cross' | 'all'>('cross')
const shown = ref(60)

const selected = ref(String(route.query.c || ''))
const detail = ref<FigureUsage[]>([])
const detailState = ref<'idle' | 'loading' | 'ready' | 'unavailable'>('idle')

const crossCount = computed(() => usage.value.filter((u) => u.figures.length >= 2).length)

const filtered = computed(() => {
  const q = activeQuery.value.trim().toLowerCase()
  let list = scope.value === 'cross' ? usage.value.filter((u) => u.figures.length >= 2) : usage.value
  if (q) list = list.filter((u) => u.concept.toLowerCase().includes(q))
  return list
})

const visible = computed(() => filtered.value.slice(0, shown.value))

const nameOf = (code: string) => figureMeta.value.get(code)?.name || ''
const eraOf = (code: string) => figureMeta.value.get(code)?.era || ''

let searchTimer: number | undefined
const onSearch = (value: string) => {
  query.value = value
  window.clearTimeout(searchTimer)
  searchTimer = window.setTimeout(() => { activeQuery.value = value; shown.value = 60 }, 150)
}

const setScope = (next: 'cross' | 'all') => { scope.value = next; shown.value = 60 }

const shardCache = new Map<string, Promise<any>>()
const loadShard = (code: string) => {
  if (!shardCache.has(code)) {
    const p = fetchFigureModes(code)
    p.catch(() => shardCache.delete(code))
    shardCache.set(code, p)
  }
  return shardCache.get(code) as Promise<any>
}

const pickZh = (v: any): string => (Array.isArray(v) ? (v[0] ?? '') : (v ?? ''))

/** 概念 → 各人物身上携带该概念的模式（模式级证据，不是人物级猜测） */
const openConcept = async (concept: string) => {
  selected.value = concept
  router.replace({ name: 'concepts', query: concept ? { c: concept } : {} })
  detailState.value = 'loading'
  detail.value = []
  const hit = usage.value.find((u) => u.concept === concept)
  if (!hit) { detailState.value = 'ready'; return }
  const rows: FigureUsage[] = []
  for (const code of hit.figures) {
    const payload = await loadShard(code)
    const modes: ModeHit[] = ((payload?.modes) || [])
      .filter((m: any) => Array.isArray(m.key_concepts) && m.key_concepts.includes(concept))
      .map((m: any) => ({
        code: m.mode_code || '',
        name: locale.value === 'zh' ? pickZh(m.name_zh) : (pickZh(m.name_en) || pickZh(m.name_zh)),
        definition: locale.value === 'zh' ? (m.definition_zh || '') : (m.definition_en || m.definition_zh || ''),
      }))
    rows.push({
      code,
      name: nameOf(code),
      era: eraOf(code),
      nMods: payload?.count ?? (payload?.modes || []).length,
      modes,
    })
  }
  detail.value = rows
  detailState.value = 'ready'
}

const closeConcept = () => {
  selected.value = ''
  detail.value = []
  detailState.value = 'idle'
  router.replace({ name: 'concepts' })
}

const load = async () => {
  const [g, idx] = await Promise.all([loadConceptGraph(), fetchUnifiedIndex()])
  if (!g) { state.value = 'unavailable'; return }
  graph.value = g
  usage.value = buildConceptUsage(g)
  figureMeta.value = new Map((idx?.items || []).filter((i) => i.type === 'figure').map((i) => [i.code, i]))
  state.value = 'ready'
  if (selected.value) openConcept(selected.value)
}

watch(locale, () => { if (selected.value) openConcept(selected.value) })
onMounted(load)
</script>

<template>
  <div class="pt-container pb-20 pt-10">
    <section class="mb-8">
      <div class="mb-3 flex flex-wrap items-center gap-3">
        <span class="pt-hairline w-10"></span>
        <span class="pt-code">{{ t('概念索引 · 跨人物连接', 'CONCEPT INDEX · CROSS-FIGURE LINKS') }}</span>
      </div>
      <h1 class="pt-h1 !text-4xl">概念索引</h1>
      <p class="pt-prose mt-3 max-w-3xl">
        按模式档案里的 key_concepts 聚合：同一个概念出现在哪些历史人物身上、又落在哪几条具体模式里。
        数据来自静态图谱分片，不需要后端。
      </p>
    </section>

    <div v-if="state === 'loading'" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="i in 6" :key="i" class="pt-skeleton h-36"></div>
    </div>

    <div v-else-if="state === 'unavailable'" class="pt-panel px-6 py-10 text-center">
      <p class="text-parchment/70">{{ t('概念图谱数据不可用', 'Concept graph data unavailable') }}</p>
      <p class="mt-2 font-mono text-xs text-parchment/40">data/graph/concept_graph.json</p>
    </div>

    <template v-else>
      <div class="pt-panel mb-6 flex flex-wrap items-center gap-x-6 gap-y-2 px-5 py-4 text-sm">
        <span class="text-parchment/70">{{ t('概念总数', 'Concepts') }} <b class="text-parchment">{{ usage.length.toLocaleString() }}</b></span>
        <span class="text-parchment/70">{{ t('跨人物概念（≥2 人）', 'Shared by ≥2 figures') }} <b class="text-gold-300">{{ crossCount }}</b></span>
        <span class="text-parchment/70">{{ t('人物', 'Figures') }} <b class="text-parchment">{{ graph?.stats.n_figures }}</b></span>
        <span class="text-parchment/70">{{ t('人物-概念边', 'Edges') }} <b class="text-parchment">{{ graph?.stats.n_edges }}</b></span>
      </div>

      <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center">
        <input
          :value="query"
          class="pt-input w-full sm:max-w-sm"
          type="search"
          :placeholder="t('搜索概念（如 良知 / 知行合一）', 'Search concepts')"
          @input="onSearch(($event.target as HTMLInputElement).value)"
        />
        <div class="flex flex-wrap gap-2">
          <button type="button" :class="scope === 'cross' ? 'pt-btn-gold' : 'pt-btn-ghost'" @click="setScope('cross')">
            {{ t(`跨人物 ${crossCount}`, `Shared ${crossCount}`) }}
          </button>
          <button type="button" :class="scope === 'all' ? 'pt-btn-gold' : 'pt-btn-ghost'" @click="setScope('all')">
            {{ t(`全部 ${usage.length.toLocaleString()}`, `All ${usage.length.toLocaleString()}`) }}
          </button>
        </div>
      </div>

      <p class="mb-4 text-xs text-parchment/45">
        {{ t(`显示 ${visible.length} / 命中 ${filtered.length} 条概念`, `Showing ${visible.length} of ${filtered.length} concepts`) }}
      </p>

      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <article
          v-for="u in visible" :key="u.concept"
          data-concept-card
          class="pt-panel flex min-w-0 flex-col p-5 transition-colors duration-300 hover:border-gold-500/30"
        >
          <div class="mb-2 flex items-start justify-between gap-3">
            <h2 class="min-w-0 break-words font-display text-lg text-parchment">{{ u.concept }}</h2>
            <span class="pt-chip-jade shrink-0">{{ t(`${u.figures.length} 人`, `${u.figures.length} fig.`) }}</span>
          </div>
          <div class="mb-3 flex flex-wrap gap-1.5">
            <span v-for="code in u.figures.slice(0, 4)" :key="code" class="pt-chip-mute max-w-full break-words">
              {{ nameOf(code) || code }}
            </span>
            <span v-if="u.figures.length > 4" class="pt-chip-mute">+{{ u.figures.length - 4 }}</span>
          </div>
          <button type="button" class="pt-btn-ghost mt-auto w-full" @click="openConcept(u.concept)">
            {{ t('查看跨人物用法', 'See cross-figure usage') }}
          </button>
        </article>
      </div>

      <div v-if="visible.length < filtered.length" class="mt-6 text-center">
        <button type="button" class="pt-btn-gold" @click="shown += 120">
          {{ t(`加载更多（还有 ${filtered.length - visible.length} 条）`, `Load more (${filtered.length - visible.length} left)`) }}
        </button>
      </div>

      <section v-if="selected" class="pt-panel mt-10 p-6">
        <div class="mb-4 flex flex-wrap items-center gap-3">
          <h2 class="min-w-0 break-words pt-h2 !text-2xl">{{ selected }}</h2>
          <span class="pt-chip-gold">{{ t('跨人物用法', 'Cross-figure usage') }}</span>
          <button type="button" class="pt-btn-ghost ml-auto" @click="closeConcept">{{ t('收起', 'Collapse') }}</button>
        </div>

        <p v-if="detailState === 'loading'" class="text-sm text-parchment/50">{{ t('加载各人物模式分片…', 'Loading figure mode shards…') }}</p>

        <p v-else-if="!detail.length" class="text-sm text-parchment/50">
          {{ t('该概念只出现在图谱边里，模式分片未命中（数据边界，不做推断）', 'No mode-level hit in the figure shards.') }}
        </p>

        <div v-else class="space-y-4">
          <article
            v-for="f in detail" :key="f.code"
            data-figure-card
            class="rounded-xl border border-white/10 bg-white/[.02] p-4"
          >
            <div class="mb-2 flex flex-wrap items-center gap-2">
              <RouterLink :to="{ name: 'mind', params: { code: f.code } }" class="pt-h3 text-gold-300 hover:text-gold-200">
                {{ f.name || f.code }}
              </RouterLink>
              <span v-if="!f.name" class="pt-chip-mute">{{ t('待核名', 'Name pending review') }}</span>
              <span v-if="f.era" class="pt-chip-mute max-w-full break-words">{{ f.era }}</span>
              <span class="pt-chip-jade">{{ t(`${f.nMods} 条模式`, `${f.nMods} modes`) }}</span>
            </div>
            <ul v-if="f.modes.length" class="space-y-2">
              <li v-for="m in f.modes" :key="m.code" class="text-sm text-parchment/70">
                <span class="font-mono text-[10px] text-gold-400/70">{{ m.code }}</span>
                <span class="ml-2 text-parchment/90">{{ m.name }}</span>
                <p v-if="m.definition" class="mt-1 text-xs leading-relaxed text-parchment/50 line-clamp-2">{{ m.definition }}</p>
              </li>
            </ul>
            <p v-else class="text-xs text-parchment/45">{{ t('该人物的模式分片里没有这条概念（图谱边来自其它口径）', 'Not found in this figure’s mode shard.') }}</p>
          </article>
        </div>
      </section>
    </template>
  </div>
</template>
