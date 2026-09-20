<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { fetchFigureModes } from '../api/static'
import { buildJsonLd, setSeo, truncateSeo } from '../composables/useSeo'
import SimilarModeList from '../components/SimilarModeList.vue'
import SourceCitation from '../components/SourceCitation.vue'
import { useCompare } from '../composables/useCompare'
import { MAX_COMPARE_ITEMS } from '../api/compareData'

// Phase30-B3: 一键加入对比（选中集合由 useCompare 单例持有，/compare 读取同一份）
const { codes: compareCodes, add: addCompare } = useCompare()
const compareNotice = ref('')
const compareFull = computed(() => compareCodes.value.length >= MAX_COMPARE_ITEMS)

const addToCompare = (target: string) => {
  const result = addCompare(target)
  compareNotice.value =
    result === 'added' ? t('已加入对比', 'Added to compare')
      : result === 'duplicate' ? t('已在对比列表中', 'Already in compare')
        : t(`最多对比 ${MAX_COMPARE_ITEMS} 项，请先在对比页移除一项`, `At most ${MAX_COMPARE_ITEMS} items — remove one on /compare`)
}

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()

const payload = ref<any>(null)
const loading = ref(false)
const code = ref(String(route.params.code || ''))

// 路由 meta 只给了通用标题/描述；真实人名与模式数要等 by-figure 分片到位。
// 口径与 tools/prerender_routes.py 的 person 路由完全一致，直连与站内跳转看到的 head 相同。
const applySeo = () => {
  const data = payload.value
  if (!data) return
  const name = data.figure_name || code.value
  const count = data.count ?? (data.modes || []).length
  const firstDefinition = (data.modes || []).map((m: any) => m.definition_zh).find((d: any) => !!d)
  const description = truncateSeo(firstDefinition || `${name} 的 ${count} 条思维模式档案：定义、操作步骤、出处与原话。`)
  setSeo({
    title: `${name} - 思维模式档案 ${count} 条`,
    description,
    path: `minds/${code.value}`,
    jsonLd: buildJsonLd('person', { name, description, path: `minds/${code.value}`, code: code.value }),
  })
}

const load = async () => {
  loading.value = true
  payload.value = await fetchFigureModes(code.value)
  loading.value = false
  applySeo()
}

const pick = (v: any) => (Array.isArray(v) ? (v[0] ?? '') : (v ?? ''))

const modes = computed(() =>
  (payload.value?.modes || []).map((m: any) => ({
    code: m.mode_code || '',
    name: locale.value === 'zh' ? pick(m.name_zh) : (pick(m.name_en) || pick(m.name_zh)),
    category: m.category || '',
    domain: locale.value === 'zh' ? (m.domain_zh || '') : (m.domain_en || m.domain_zh || ''),
    definition: locale.value === 'zh' ? (m.definition_zh || '') : (m.definition_en || m.definition_zh || ''),
    process: (locale.value === 'zh' ? m.process_zh : (m.process_en || m.process_zh)) || [],
    concepts: Array.isArray(m.key_concepts) ? m.key_concepts : [],
    source: m.source_chapter || '',
    // Phase38-Y2：构建期注入的出处分段与核验状态（缺字段时退回上面的纯文本）
    sourceParts: Array.isArray(m.source_parts) ? m.source_parts : [],
    verification: m.verification || null,
    quote: locale.value === 'zh' ? (m.key_quote_zh || '') : (m.key_quote_en || m.key_quote_zh || ''),
    cases: (locale.value === 'zh' ? m.representative_cases_zh : (m.representative_cases_en || m.representative_cases_zh)) || [],
    apps: (locale.value === 'zh' ? m.modern_applications_zh : (m.modern_applications_en || m.modern_applications_zh)) || [],
  }))
)

watch(locale, load)
watch(() => route.params.code, (c) => { if (c) { code.value = String(c); load() } })
onMounted(load)
</script>

<template>
  <div class="pt-container pb-20 pt-8">
    <div v-if="loading" class="flex min-h-[40vh] items-center justify-center">
      <div class="h-10 w-10 animate-spin rounded-full border-2 border-gold-500/25 border-t-gold-400"></div>
    </div>

    <div v-else-if="!payload" class="pt-panel mx-auto mt-20 max-w-lg px-8 py-14 text-center">
      <div class="mb-3 text-4xl opacity-70">🕳️</div>
      <h1 class="pt-h3 mb-2 text-parchment/90">{{ t('未找到该人物的模式档案', 'No mode archive for this figure') }}</h1>
      <p class="mb-5 font-mono text-xs text-parchment/40">{{ code }}</p>
      <button @click="router.push({ name: 'modes' })" class="pt-btn-ghost">{{ t('去模式库', 'Browse modes') }}</button>
    </div>

    <template v-else>
      <button @click="router.push({ name: 'modes' })"
              class="mb-6 inline-flex items-center gap-2 text-sm text-parchment/50 transition-colors hover:text-gold-300">
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        {{ t('返回模式库', 'Back to modes') }}
      </button>

      <header class="pt-panel relative mb-8 overflow-hidden p-7">
        <div aria-hidden="true"
             class="pointer-events-none absolute -top-24 right-0 h-64 w-64 rounded-full bg-jade-400/10 blur-3xl"></div>
        <div class="relative">
          <div class="mb-3 flex flex-wrap items-center gap-2">
            <span class="pt-code">{{ payload.figure_code }}</span>
            <span class="pt-chip-jade">{{ t(`${payload.count} 条模式`, `${payload.count} modes`) }}</span>
          </div>
          <h1 class="pt-h1 !text-4xl sm:!text-5xl">{{ payload.figure_name || payload.figure_code }}</h1>
          <p class="mt-3 text-sm text-parchment/55">
            {{ t('以下为该历史人物的全部思维模式，含定义、操作步骤、出处与原话。',
                 'All thinking modes of this figure, with definition, steps, source and quote.') }}
          </p>

          <!-- Phase30-B3: 一键加入对比 -->
          <div class="mt-5 flex flex-wrap items-center gap-3">
            <button class="pt-btn-ghost" :disabled="compareFull" @click="addToCompare(code)">
              {{ t('加入对比', 'Add to compare') }}
            </button>
            <RouterLink v-if="compareCodes.length" to="/compare" class="pt-btn-gold">
              {{ t(`开始对比（${compareCodes.length}/${MAX_COMPARE_ITEMS}）`, `Compare (${compareCodes.length}/${MAX_COMPARE_ITEMS})`) }}
            </RouterLink>
            <span v-if="compareNotice" class="text-xs text-gold-300/80">{{ compareNotice }}</span>
          </div>
        </div>
      </header>

      <div class="space-y-6">
        <article v-for="(m, i) in modes" :key="m.code"
                 class="pt-panel p-7 transition-colors duration-500 hover:border-gold-500/30">
          <div class="mb-4 flex flex-wrap items-center gap-2">
            <span class="grid h-7 w-7 place-items-center rounded-full border border-gold-500/40 bg-gold-500/10
                         font-mono text-xs font-bold text-gold-300">{{ i + 1 }}</span>
            <h2 class="pt-h3 text-parchment">{{ m.name }}</h2>
            <button class="pt-chip-mute transition-colors hover:border-gold-500/40 hover:text-gold-200"
                    @click="addToCompare(m.code)">
              {{ t('加入对比', 'Compare') }}
            </button>
            <span v-if="m.domain" class="pt-chip-jade ml-auto">{{ m.domain }}</span>
          </div>

          <p v-if="m.definition" class="leading-relaxed text-parchment/70">{{ m.definition }}</p>

          <div v-if="m.process?.length" class="mt-5">
            <h3 class="mb-2 text-xs uppercase tracking-wider text-parchment/40">{{ t('操作步骤', 'Steps') }}</h3>
            <ol class="space-y-2">
              <li v-for="(s, j) in m.process" :key="j" class="flex gap-3 text-sm text-parchment/65">
                <span class="font-mono text-gold-400/70">{{ j + 1 }}.</span><span>{{ s }}</span>
              </li>
            </ol>
          </div>

          <div v-if="m.concepts?.length" class="mt-5 flex flex-wrap gap-1.5">
            <span v-for="c in m.concepts" :key="c" class="pt-chip-mute">{{ c }}</span>
          </div>

          <div class="mt-5 grid gap-4 sm:grid-cols-2">
            <div v-if="m.source" class="rounded-xl border border-white/10 bg-white/[.02] p-4">
              <div class="mb-1 text-xs uppercase tracking-wider text-parchment/40">{{ t('出处', 'Source') }}</div>
              <div class="flex flex-wrap items-baseline text-sm text-parchment/70"><SourceCitation :parts="m.sourceParts" :text="m.source" :verification="m.verification" /></div>
            </div>
            <div v-if="m.quote" class="rounded-xl border border-gold-500/20 bg-gold-500/[.05] p-4">
              <div class="mb-1 text-xs uppercase tracking-wider text-gold-300/70">{{ t('原话', 'Quote') }}</div>
              <div class="font-display text-sm leading-relaxed text-parchment/80">{{ m.quote }}</div>
            </div>
          </div>

          <div v-if="m.cases?.length" class="mt-5">
            <h3 class="mb-2 text-xs uppercase tracking-wider text-parchment/40">{{ t('史实案例', 'Cases') }}</h3>
            <ul class="space-y-1.5 text-sm leading-relaxed text-parchment/65">
              <li v-for="(c, j) in m.cases" :key="j" class="flex gap-2"><span class="text-gold-400/60">◆</span><span>{{ c }}</span></li>
            </ul>
          </div>

          <div v-if="m.apps?.length" class="mt-5">
            <h3 class="mb-2 text-xs uppercase tracking-wider text-parchment/40">{{ t('现代应用', 'Applications') }}</h3>
            <ul class="space-y-1.5 text-sm leading-relaxed text-parchment/65">
              <li v-for="(a, j) in m.apps" :key="j" class="flex gap-2"><span class="text-jade-400/70">◆</span><span>{{ a }}</span></li>
            </ul>
          </div>

          <!-- Phase30-B2: 读 B1 预计算的相似模式（key_concepts 交集，非向量语义相似度） -->
          <SimilarModeList v-if="m.code" :mode-code="m.code" :limit="5" />
        </article>
      </div>
    </template>
  </div>
</template>
