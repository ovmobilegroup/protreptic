<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useFiguresStore } from '../stores/figures'
import { useI18n } from '../composables/useI18n'

const route = useRoute()
const router = useRouter()
const figuresStore = useFiguresStore()
const { t, locale } = useI18n()
const DATA_MODE = import.meta.env.VITE_DATA_MODE ?? 'api'

const figure = ref<any>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const similarFigures = ref<any[]>([])
const similarLoading = ref(false)
const figureCode = ref(route.params.code as string)

const eraLabels: Record<string, { zh: string; en: string }> = {
  'Pre-Qin': { zh: '先秦', en: 'Pre-Qin' },
  'Qin-Han': { zh: '秦汉', en: 'Qin-Han' },
  'Three-Kingdoms-Jin': { zh: '三国两晋', en: 'Three Kingdoms & Jin' },
  'Northern-Southern': { zh: '南北朝', en: 'N. & S. Dynasties' },
  'Sui-Tang': { zh: '隋唐', en: 'Sui-Tang' },
  'Song-Yuan': { zh: '宋元', en: 'Song-Yuan' },
  'Ming-Qing': { zh: '明清', en: 'Ming-Qing' },
  'Modern-Early': { zh: '近代', en: 'Early Modern' },
  'Modern': { zh: '现代', en: 'Modern' },
}

const histDomainLabels: Record<string, { zh: string; en: string }> = {
  Military: { zh: '军事', en: 'Military' }, Philosophy: { zh: '哲学', en: 'Philosophy' },
  Governance: { zh: '治理', en: 'Governance' }, Science_Tech: { zh: '科技', en: 'Sci & Tech' },
  Historiography: { zh: '史学', en: 'History' }, Literature_Arts: { zh: '文艺', en: 'Arts' },
  Religion: { zh: '宗教', en: 'Religion' }, Education: { zh: '教育', en: 'Education' },
  Economics: { zh: '经济', en: 'Economics' }, Ethics: { zh: '伦理', en: 'Ethics' },
}

const DOMAINS = ['Strategic', 'Analytical', 'Collaborative', 'Operational', 'Systems', 'Creative', 'Personal']
const domainLabels: Record<string, { zh: string; en: string }> = {
  Strategic: { zh: '战略', en: 'Strategic' }, Analytical: { zh: '分析', en: 'Analytical' },
  Collaborative: { zh: '协作', en: 'Collaborative' }, Operational: { zh: '操作', en: 'Operational' },
  Systems: { zh: '系统', en: 'Systems' }, Creative: { zh: '创新', en: 'Creative' },
  Personal: { zh: '个人', en: 'Personal' },
}

const modeDomainMap: Record<number, string> = {
  1: 'Strategic', 2: 'Strategic', 3: 'Strategic', 4: 'Strategic',
  5: 'Analytical', 6: 'Collaborative', 7: 'Strategic', 8: 'Operational',
  9: 'Operational', 10: 'Collaborative', 11: 'Operational', 12: 'Systems',
  13: 'Strategic', 14: 'Strategic', 15: 'Strategic', 16: 'Strategic',
  17: 'Analytical', 18: 'Collaborative', 19: 'Analytical', 20: 'Analytical',
  21: 'Personal', 22: 'Systems', 23: 'Creative', 24: 'Analytical',
  25: 'Analytical', 26: 'Personal', 27: 'Systems', 28: 'Operational',
  29: 'Analytical', 30: 'Analytical', 31: 'Systems', 32: 'Systems',
  33: 'Strategic', 34: 'Operational', 35: 'Operational', 36: 'Personal',
  37: 'Personal', 38: 'Operational', 39: 'Strategic', 40: 'Operational',
  41: 'Operational', 42: 'Personal',
}
const domainToModeIds: Record<string, number[]> = {}
Object.entries(modeDomainMap).forEach(([modeId, domain]) => {
  ;(domainToModeIds[domain] ||= []).push(Number(modeId))
})

const fetchFigure = async () => {
  loading.value = true; error.value = null
  try {
    const data = await figuresStore.fetchFigure(figureCode.value, locale.value)
    if (data) { figure.value = data; await fetchSimilarFigures() }
    else error.value = t('人物不存在', 'Figure not found')
  } catch (err) {
    error.value = err instanceof Error ? err.message : t('加载失败', 'Failed to load')
  } finally { loading.value = false }
}

const fetchSimilarFigures = async () => {
  similarLoading.value = true
  try { similarFigures.value = await figuresStore.getSimilar(figureCode.value, locale.value, 6) }
  catch (e) { console.error('similar failed', e) }
  finally { similarLoading.value = false }
}

const eraLabel = computed(() => {
  if (!figure.value?.era) return ''
  return eraLabels[figure.value.era]?.[locale.value] || figure.value.era
})

const distribution = computed(() => {
  const dist: Record<string, number> = {}
  ;(figure.value?.modes || []).forEach((id: number) => {
    const d = modeDomainMap[id] || 'Personal'
    dist[d] = (dist[d] || 0) + 1
  })
  return dist
})

const maxDist = computed(() => Math.max(1, ...Object.values(distribution.value)))

const hasModes = computed(() => (figure.value?.modes || []).length > 0)

const timelineEvents = computed(() => {
  if (!figure.value) return []
  const out: any[] = []
  if (figure.value.era) out.push({ label: t('历史时期', 'Era'), value: eraLabel.value, icon: '📜' })
  if (figure.value.modes?.length) {
    out.push({ label: t('核心思维模式', 'Core modes'), value: figure.value.modes.slice(0, 3).map((m: number) => `#${m}`).join(' · '), icon: '🧠' })
  }
  if (figure.value.historical_domains?.length) {
    out.push({ label: t('历史领域', 'Historical domains'), value: figure.value.historical_domains.slice(0, 3).join(' · '), icon: '🏛️' })
  }
  return out
})

const applicationScenarios = computed(() => {
  if (!figure.value) return []
  const all = [
    { title: { zh: '战略规划与决策', en: 'Strategic Planning' }, description: { zh: '长期战略制定、资源分配、竞争格局分析', en: 'Long-term strategy, resource allocation, competitive analysis' }, icon: '🎯', tags: ['Strategic', 'Analytical'] },
    { title: { zh: '危机管理与突围', en: 'Crisis & Breakthrough' }, description: { zh: '逆境生存、资源极限下的最优决策', en: 'Survival in adversity, decisions under constraints' }, icon: '⚔️', tags: ['Strategic', 'Operational'] },
    { title: { zh: '团队建设与组织变革', en: 'Team & Org Change' }, description: { zh: '跨部门协作、文化重塑、人才梯队', en: 'Collaboration, culture, talent pipeline' }, icon: '🤝', tags: ['Collaborative', 'Systems'] },
    { title: { zh: '创新突破与技术攻关', en: 'Innovation & R&D' }, description: { zh: '核心技术攻关、新范式探索、从 0 到 1', en: 'Core tech R&D, paradigm shifts, 0-to-1' }, icon: '💡', tags: ['Creative', 'Analytical'] },
    { title: { zh: '个人成长与决策升级', en: 'Personal Growth' }, description: { zh: '职业规划、人生重大选择、认知升级', en: 'Career planning, life choices, cognitive upgrade' }, icon: '📈', tags: ['Personal', 'Analytical'] },
    { title: { zh: '组织传承与继任', en: 'Succession & Legacy' }, description: { zh: '核心人才交接、知识沉淀、制度化传承', en: 'Talent transition, knowledge transfer' }, icon: '🏛️', tags: ['Systems', 'Collaborative'] },
  ]
  const ids = new Set(figure.value.modes || [])
  return all.filter((s) => s.tags.some((tg) => domainToModeIds[tg]?.some((id) => ids.has(id)))).slice(0, 4)
})

watch(locale, () => fetchFigure())
watch(() => route.params.code, (c) => { if (c && c !== figureCode.value) { figureCode.value = c as string; fetchFigure() } })
onMounted(fetchFigure)

const backToList = () => router.push({ name: 'figures' })
</script>

<template>
  <div class="pt-container pb-20 pt-8">
    <!-- 加载 -->
    <div v-if="loading" class="flex min-h-[50vh] items-center justify-center">
      <div class="flex flex-col items-center gap-4">
        <div class="h-10 w-10 animate-spin rounded-full border-2 border-gold-500/25 border-t-gold-400"></div>
        <p class="text-sm text-parchment/45">{{ t('加载中…', 'Loading…') }}</p>
      </div>
    </div>

    <!-- 错误 -->
    <div v-else-if="error" class="pt-panel mx-auto mt-20 max-w-lg px-8 py-14 text-center">
      <div class="mb-3 text-4xl opacity-70">🕳️</div>
      <h1 class="pt-h3 mb-2 text-parchment/90">{{ error }}</h1>
      <button @click="backToList" class="pt-btn-ghost mt-4">{{ t('返回列表', 'Back to list') }}</button>
    </div>

    <!-- 详情 -->
    <div v-else-if="figure">
      <!-- 返回 -->
      <button @click="backToList"
              class="mb-6 inline-flex items-center gap-2 text-sm text-parchment/50 transition-colors hover:text-gold-300">
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        {{ t('返回名录', 'Back to register') }}
      </button>

      <div class="grid gap-8 lg:grid-cols-3">
        <!-- 主列 -->
        <div class="space-y-8 lg:col-span-2">
          <!-- 标题卡 -->
          <header class="pt-panel relative overflow-hidden p-7">
            <div aria-hidden="true"
                 class="pointer-events-none absolute -top-24 right-0 h-64 w-64 rounded-full bg-gold-500/10 blur-3xl"></div>
            <div class="relative">
              <div class="mb-3 flex flex-wrap items-center gap-2">
                <span class="pt-code">{{ figure.code }}</span>
                <span v-if="eraLabel" class="pt-chip-mute">{{ eraLabel }}</span>
                <span v-if="figure.gender" class="pt-chip-mute">{{ figure.gender }}</span>
                <span v-if="figure.ethnicity" class="pt-chip-mute">{{ figure.ethnicity }}</span>
              </div>
              <h1 class="pt-h1 !text-4xl sm:!text-5xl">{{ figure.name }}</h1>
              <p v-if="figure.description" class="mt-4 max-w-2xl text-base leading-relaxed text-parchment/60">
                {{ figure.description }}
              </p>
              <div v-if="hasModes" class="mt-5 flex flex-wrap gap-1.5">
                <span v-for="modeId in figure.modes.slice(0, 10)" :key="modeId" class="pt-chip-jade">#{{ modeId }}</span>
              </div>
            </div>
          </header>

          <!-- 分布 -->
          <section v-if="hasModes" class="pt-panel p-7">
            <h2 class="pt-h3 mb-6 text-gold-200">{{ t('思维模式分布', 'Thinking-mode distribution') }}</h2>
            <div class="space-y-3">
              <div v-for="d in DOMAINS" :key="d" class="flex items-center gap-4">
                <span class="w-20 shrink-0 text-sm text-parchment/70">
                  {{ locale === 'zh' ? domainLabels[d].zh : domainLabels[d].en }}
                </span>
                <div class="h-2.5 flex-1 overflow-hidden rounded-full bg-white/[.08]">
                  <div class="h-full rounded-full bg-gradient-to-r from-gold-600 to-gold-300 transition-all duration-700 ease-silk"
                       :style="{ width: ((distribution[d] || 0) / maxDist) * 100 + '%' }"></div>
                </div>
                <span class="w-8 shrink-0 text-right font-mono text-sm"
                      :class="(distribution[d] || 0) > 0 ? 'text-gold-300' : 'text-parchment/25'">
                  {{ distribution[d] || 0 }}
                </span>
              </div>
            </div>
          </section>

          <!-- 推荐理由 -->
          <section v-if="figure.reason" class="pt-panel p-7">
            <h2 class="pt-h3 mb-3 text-gold-200">{{ t('推荐理由', 'Rationale') }}</h2>
            <p class="leading-relaxed text-parchment/65">{{ figure.reason }}</p>
          </section>

          <!-- 分步指南 -->
          <section v-if="figure.steps?.length" class="pt-panel p-7">
            <h2 class="pt-h3 mb-5 text-gold-200">{{ t('分步操作指南', 'Step-by-step guide') }}</h2>
            <ol class="space-y-4">
              <li v-for="(step, i) in figure.steps" :key="i" class="flex gap-4">
                <span class="grid h-7 w-7 shrink-0 place-items-center rounded-full border border-gold-500/40
                             bg-gold-500/10 font-mono text-xs font-bold text-gold-300">{{ i + 1 }}</span>
                <p class="pt-0.5 leading-relaxed text-parchment/70">{{ step }}</p>
              </li>
            </ol>
          </section>

          <!-- 预期效果 / 案例 -->
          <div class="grid gap-6 sm:grid-cols-2">
            <section v-if="figure.expected" class="pt-panel border-jade-400/20 p-6">
              <h2 class="mb-3 flex items-center gap-2 text-sm font-semibold text-jade-300">
                <span>◆</span>{{ t('预期效果', 'Expected outcome') }}
              </h2>
              <p class="text-sm leading-relaxed text-parchment/65">{{ figure.expected }}</p>
            </section>
            <section v-if="figure.case" class="pt-panel p-6">
              <h2 class="mb-3 flex items-center gap-2 text-sm font-semibold text-gold-300">
                <span>◆</span>{{ t('实战案例', 'Case study') }}
              </h2>
              <p class="text-sm leading-relaxed text-parchment/65">{{ figure.case }}</p>
            </section>
          </div>

          <!-- 时间线 -->
          <section v-if="timelineEvents.length" class="pt-panel p-7">
            <h2 class="pt-h3 mb-6 text-gold-200">{{ t('关键线索', 'Key threads') }}</h2>
            <div class="relative space-y-6 border-l border-white/10 pl-6">
              <div v-for="(ev, i) in timelineEvents" :key="i" class="relative">
                <span class="absolute -left-[31px] top-1.5 grid h-3 w-3 place-items-center rounded-full
                             bg-gold-500 ring-4 ring-gold-500/15"></span>
                <div class="text-xs uppercase tracking-wider text-parchment/40">{{ ev.label }}</div>
                <div class="mt-1 flex items-center gap-2 text-sm text-parchment/75">
                  <span>{{ ev.icon }}</span><span>{{ ev.value }}</span>
                </div>
              </div>
            </div>
          </section>

          <!-- 应用场景 -->
          <section v-if="applicationScenarios.length" class="pt-panel p-7">
            <h2 class="pt-h3 mb-5 text-gold-200">{{ t('现代应用场景', 'Modern applications') }}</h2>
            <div class="grid gap-4 sm:grid-cols-2">
              <article v-for="s in applicationScenarios" :key="s.title.zh"
                       class="rounded-xl border border-white/10 bg-white/[.02] p-5 transition-all duration-500 ease-silk
                              hover:-translate-y-0.5 hover:border-gold-500/35 hover:bg-white/[.045]">
                <div class="mb-2 text-2xl">{{ s.icon }}</div>
                <h4 class="font-display font-semibold text-parchment">{{ locale === 'zh' ? s.title.zh : s.title.en }}</h4>
                <p class="mt-1 text-sm leading-relaxed text-parchment/55">{{ locale === 'zh' ? s.description.zh : s.description.en }}</p>
              </article>
            </div>
          </section>

          <!-- 相似人物 -->
          <section v-if="similarFigures.length" class="pt-panel p-7">
            <div class="mb-5 flex flex-wrap items-center gap-3">
              <h2 class="pt-h3 text-gold-200">
                {{ DATA_MODE === 'static' ? t('相似人物', 'Similar figures') : t('语义相似人物', 'Semantically similar') }}
              </h2>
              <span class="pt-chip-mute">
                {{ DATA_MODE === 'static' ? t('按标签重叠度', 'by tag overlap') : t('语义检索', 'semantic') }}
              </span>
            </div>
            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              <article v-for="sim in similarFigures" :key="sim.code"
                       @click="router.push({ name: 'figure-detail', params: { code: sim.code } })"
                       class="group cursor-pointer rounded-xl border border-white/10 bg-white/[.02] p-4 transition-all duration-500 ease-silk
                              hover:-translate-y-1 hover:border-jade-400/40 hover:bg-white/[.05]">
                <div class="mb-2 flex items-center justify-between">
                  <span class="pt-code">{{ sim.code }}</span>
                  <span class="text-xs text-jade-300/80">{{ ((sim.similarity_score || 0) * 100).toFixed(0) }}%</span>
                </div>
                <h4 class="font-display font-semibold text-parchment transition-colors group-hover:text-gold-200">{{ sim.name }}</h4>
                <p class="mt-1 text-sm text-parchment/50 line-clamp-2">{{ sim.reason }}</p>
              </article>
            </div>
          </section>
        </div>

        <!-- 侧栏 -->
        <aside class="space-y-6 lg:sticky lg:top-24 lg:self-start">
          <!-- 档案信息（始终有内容） -->
          <div class="pt-panel p-6">
            <h3 class="pt-h3 mb-4 text-parchment/90">{{ t('档案', 'Profile') }}</h3>
            <dl class="space-y-3 text-sm">
              <div class="flex items-center justify-between gap-3">
                <dt class="text-parchment/45">{{ t('编号', 'Code') }}</dt>
                <dd class="pt-code">{{ figure.code }}</dd>
              </div>
              <div v-if="eraLabel" class="flex items-center justify-between gap-3">
                <dt class="text-parchment/45">{{ t('时代', 'Era') }}</dt>
                <dd class="text-parchment/80">{{ eraLabel }}</dd>
              </div>
              <div v-if="figure.gender" class="flex items-center justify-between gap-3">
                <dt class="text-parchment/45">{{ t('性别', 'Gender') }}</dt>
                <dd class="text-parchment/80">{{ figure.gender }}</dd>
              </div>
              <div v-if="figure.ethnicity" class="flex items-center justify-between gap-3">
                <dt class="text-parchment/45">{{ t('民族', 'Ethnicity') }}</dt>
                <dd class="text-parchment/80">{{ figure.ethnicity }}</dd>
              </div>
              <div class="flex items-center justify-between gap-3">
                <dt class="text-parchment/45">{{ t('模式数', 'Modes') }}</dt>
                <dd class="font-mono text-gold-300">{{ (figure.modes || []).length }}</dd>
              </div>
            </dl>
          </div>

          <div v-if="figure.historical_domains?.length || figure.domains?.length || figure.core_modes?.length"
               class="pt-panel p-6">
            <h3 class="pt-h3 mb-4 text-parchment/90">{{ t('标签', 'Tags') }}</h3>
            <div class="space-y-5">
              <div v-if="figure.historical_domains?.length">
                <h4 class="mb-2 text-xs uppercase tracking-wider text-parchment/40">{{ t('历史领域', 'Historical domains') }}</h4>
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="d in figure.historical_domains" :key="d" class="pt-chip-gold">
                    {{ histDomainLabels[d]?.[locale] || d }}
                  </span>
                </div>
              </div>
              <div v-if="figure.domains?.length">
                <h4 class="mb-2 text-xs uppercase tracking-wider text-parchment/40">{{ t('思维领域', 'Thinking domains') }}</h4>
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="d in figure.domains" :key="d" class="pt-chip-jade">
                    {{ domainLabels[d]?.[locale] || d }}
                  </span>
                </div>
              </div>
              <div v-if="figure.core_modes?.length">
                <h4 class="mb-2 text-xs uppercase tracking-wider text-parchment/40">{{ t('核心模式', 'Core modes') }}</h4>
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="m in figure.core_modes" :key="m" class="pt-chip-mute">#{{ m }}</span>
                </div>
              </div>
              <p v-if="!figure.historical_domains?.length && !figure.domains?.length && !figure.core_modes?.length"
                 class="text-sm text-parchment/35">
                {{ t('暂无标签', 'No tags') }}
              </p>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>
