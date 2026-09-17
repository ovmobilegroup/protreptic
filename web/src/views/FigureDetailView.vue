<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useFiguresStore } from '../stores/figures'
import { useI18n } from '../composables/useI18n'

const route = useRoute()
const router = useRouter()
const figuresStore = useFiguresStore()
const { t, locale } = useI18n()
// 数据源开关（与 stores/figures.ts 一致）：static 模式下相似人物按标签重叠度计算，不是向量语义相似度
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
  'Northern-Southern': { zh: '南北朝', en: 'Northern & Southern Dynasties' },
  'Sui-Tang': { zh: '隋唐', en: 'Sui-Tang' },
  'Song-Yuan': { zh: '宋元', en: 'Song-Yuan' },
  'Ming-Qing': { zh: '明清', en: 'Ming-Qing' },
  'Modern-Early': { zh: '近代', en: 'Early Modern' },
  'Modern': { zh: '现代', en: 'Modern' },
}

const domainColors: Record<string, string> = {
  'Strategic': 'bg-red-100 text-red-700',
  'Analytical': 'bg-blue-100 text-blue-700',
  'Collaborative': 'bg-green-100 text-green-700',
  'Operational': 'bg-yellow-100 text-yellow-700',
  'Systems': 'bg-purple-100 text-purple-700',
  'Creative': 'bg-pink-100 text-pink-700',
  'Personal': 'bg-indigo-100 text-indigo-700',
}

const histDomainColors: Record<string, string> = {
  'Military': 'bg-red-100 text-red-700',
  'Philosophy': 'bg-blue-100 text-blue-700',
  'Governance': 'bg-green-100 text-green-700',
  'Science_Tech': 'bg-yellow-100 text-yellow-700',
  'Historiography': 'bg-purple-100 text-purple-700',
  'Literature_Arts': 'bg-pink-100 text-pink-700',
  'Religion': 'bg-indigo-100 text-indigo-700',
  'Education': 'bg-teal-100 text-teal-700',
  'Economics': 'bg-orange-100 text-orange-700',
  'Ethics': 'bg-gray-100 text-gray-700',
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
  if (!domainToModeIds[domain]) domainToModeIds[domain] = []
  domainToModeIds[domain].push(Number(modeId))
})

const fetchFigure = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await figuresStore.fetchFigure(figureCode.value, locale.value)
    if (data) {
      figure.value = data
      await fetchSimilarFigures()
    } else {
      error.value = t('人物不存在', 'Figure not found')
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : t('加载失败', 'Failed to load')
  } finally {
    loading.value = false
  }
}

const fetchSimilarFigures = async () => {
  similarLoading.value = true
  try {
    const data = await figuresStore.getSimilar(figureCode.value, locale.value, 6)
    similarFigures.value = data
  } catch (err) {
    console.error('Failed to fetch similar figures:', err)
  } finally {
    similarLoading.value = false
  }
}

const getEraLabel = () => {
  if (!figure.value?.era) return ''
  return eraLabels[figure.value.era]?.[locale.value] || figure.value.era
}

const getModeDistribution = computed(() => {
  if (!figure.value?.modes) return {}
  const dist: Record<string, number> = {}
  figure.value.modes.forEach((modeId: number) => {
    const domain = modeDomainMap[modeId] || 'Personal'
    dist[domain] = (dist[domain] || 0) + 1
  })
  return dist
})

const getRadarData = computed(() => {
  const domains = ['Strategic', 'Analytical', 'Collaborative', 'Operational', 'Systems', 'Creative', 'Personal']
  const labels = {
    zh: ['战略', '分析', '协作', '操作', '系统', '创新', '个人'],
    en: ['Strategic', 'Analytical', 'Collaborative', 'Operational', 'Systems', 'Creative', 'Personal'],
  }
  const dist = getModeDistribution.value
  return {
    labels: labels[locale.value] || labels.en,
    datasets: [{
      label: locale.value === 'zh' ? '思维模式分布' : 'Thinking Mode Distribution',
      data: domains.map(d => dist[d] || 0),
      backgroundColor: 'rgba(99, 102, 241, 0.2)',
      borderColor: 'rgb(99, 102, 241)',
      pointBackgroundColor: 'rgb(99, 102, 241)',
      borderWidth: 2,
    }]
  }
})

const timelineEvents = computed(() => {
  if (!figure.value) return []
  const events: any[] = []
  if (figure.value.era) {
    events.push({
      type: 'era',
      label: locale.value === 'zh' ? '历史时期' : 'Historical Era',
      value: getEraLabel(),
      icon: '📜',
    })
  }
  if (figure.value.modes?.length) {
    const topModes = figure.value.modes.slice(0, 3)
    events.push({
      type: 'modes',
      label: locale.value === 'zh' ? '核心思维模式' : 'Core Thinking Modes',
      value: topModes.map((m: number) => `#${m}`).join(', '),
      icon: '🧠',
    })
  }
  if (figure.value.historical_domains?.length) {
    events.push({
      type: 'domains',
      label: locale.value === 'zh' ? '历史领域' : 'Historical Domains',
      value: figure.value.historical_domains.slice(0, 3).join(', '),
      icon: '🏛️',
    })
  }
  if (figure.value.domains?.length) {
    events.push({
      type: 'domains',
      label: locale.value === 'zh' ? '思维领域' : 'Thinking Domains',
      value: figure.value.domains.slice(0, 3).join(', '),
      icon: '🧭',
    })
  }
  return events
})

const applicationScenarios = computed(() => {
  if (!figure.value) return []
  const scenarios = [
    { title: { zh: '战略规划与决策', en: 'Strategic Planning & Decision Making' }, description: { zh: '适用于长期战略制定、资源分配、竞争格局分析', en: 'Long-term strategy, resource allocation, competitive analysis' }, icon: '🎯', tags: ['Strategic', 'Analytical'] },
    { title: { zh: '危机管理与突围', en: 'Crisis Management & Breakthrough' }, description: { zh: '适用于逆境生存、资源极限下的最优决策', en: 'Survival in adversity, optimal decisions under constraints' }, icon: '⚔️', tags: ['Strategic', 'Operational'] },
    { title: { zh: '团队建设与组织变革', en: 'Team Building & Org Change' }, description: { zh: '适用于跨部门协作、文化重塑、人才梯队建设', en: 'Cross-functional collaboration, culture building, talent pipeline' }, icon: '🤝', tags: ['Collaborative', 'Systems'] },
    { title: { zh: '创新突破与技术攻关', en: 'Innovation & Technical Breakthrough' }, description: { zh: '适用于核心技术攻关、新范式探索、从0到1创新', en: 'Core tech R&D, paradigm shifts, 0-to-1 innovation' }, icon: '💡', tags: ['Creative', 'Analytical'] },
    { title: { zh: '个人成长与决策升级', en: 'Personal Growth & Decision Upgrade' }, description: { zh: '适用于职业规划、人生重大选择、认知模型升级', en: 'Career planning, major life choices, cognitive upgrade' }, icon: '📈', tags: ['Personal', 'Analytical'] },
    { title: { zh: '组织传承与继任规划', en: 'Succession Planning & Legacy' }, description: { zh: '适用于核心人才交接、知识沉淀、制度化传承', en: 'Key talent transition, knowledge transfer, institutionalization' }, icon: '🏛️', tags: ['Systems', 'Collaborative'] },
  ]
  const modeIds = new Set(figure.value.modes || [])
  return scenarios.filter(s => s.tags.some(tag => domainToModeIds[tag]?.some(id => modeIds.has(id)))).slice(0, 4)
})

// 语言切换后重新取数（name/description/reason 等字段随 lang 变化）
watch(locale, () => { fetchFigure() })

const backToList = () => { router.push({ name: 'figures' }) }

onMounted(() => { fetchFigure() })

watch(() => route.params.code, (newCode) => { if (newCode !== figureCode.value) { figureCode.value = newCode as string; fetchFigure() } })
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div v-if="loading" class="min-h-screen flex items-center justify-center">
      <div class="text-center">
        <svg class="animate-spin h-12 w-12 text-indigo-600 mx-auto mb-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" /></svg>
        <p class="text-gray-600">{{ t('加载中...', 'Loading...') }}</p>
      </div>
    </div>
    <div v-else-if="error" class="min-h-screen flex items-center justify-center">
      <div class="text-center px-4">
        <svg class="mx-auto h-12 w-12 text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
        <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ error }}</h1>
        <button @click="backToList" class="mt-4 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">{{ t('返回列表', 'Back to List') }}</button>
      </div>
    </div>
    <div v-else-if="figure" class="min-h-screen bg-gray-50">
      <header class="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex items-center justify-between h-16">
            <div class="flex items-center gap-3">
              <button @click="backToList" class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg></button>
              <div>
                <h1 class="text-xl font-bold text-gray-900">{{ t('人物详情', 'Figure Detail') }}</h1>
                <p class="text-sm text-gray-500">{{ figure.code }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span v-if="figure.era" class="px-3 py-1 text-xs font-medium bg-gray-100 text-gray-700 rounded-full">{{ eraLabels[figure.era]?.[locale] || figure.era }}</span>
            </div>
          </div>
        </div>
      </header>
      <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid lg:grid-cols-3 gap-8">
          <div class="lg:col-span-2 space-y-8">
            <article class="bg-white rounded-xl border border-gray-200 p-6">
              <div class="flex items-start justify-between mb-6">
                <div>
                  <span class="text-xs font-mono font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded mb-2 inline-block">{{ figure.code }}</span>
                  <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ figure.name }}</h1>
                  <div v-if="figure.era" class="text-gray-500">
                    <span class="inline-flex items-center gap-1 px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                      {{ eraLabels[figure.era]?.[locale] || figure.era }}
                    </span>
                  </div>
                </div>
              </div>

              <div v-if="figure.description" class="prose prose-gray max-w-none mb-6">
                <p class="text-gray-700 leading-relaxed">{{ figure.description }}</p>
              </div>

              <section v-if="figure.modes && figure.modes.length > 0" class="mb-6">
                <h2 class="text-lg font-semibold text-gray-900 mb-3">{{ t('思维模式组合', 'Thinking Modes') }} ({{ figure.modes.length }})</h2>
                <div class="flex flex-wrap gap-2">
                  <span v-for="modeId in figure.modes" :key="modeId" class="px-3 py-1 text-sm font-medium rounded-full" :class="domainColors[modeDomainMap[modeId]] || 'bg-gray-100 text-gray-700'">#{{ modeId }}</span>
                </div>
              </section>

              <section class="mb-6">
                <h2 class="text-lg font-semibold text-gray-900 mb-3">{{ t('思维模式雷达图', 'Thinking Mode Radar') }}</h2>
                <div class="bg-gray-50 rounded-xl p-6">
                  <canvas id="modeRadar" width="400" height="300"></canvas>
                </div>
              </section>

              <section v-if="figure.reason" class="mb-6">
                <h2 class="text-lg font-semibold text-gray-900 mb-2">{{ t('推荐理由', 'Rationale') }}</h2>
                <div class="prose prose-gray max-w-none bg-gray-50 p-4 rounded-lg">
                  <p>{{ figure.reason }}</p>
                </div>
              </section>

              <section v-if="figure.steps && figure.steps.length > 0" class="mb-6">
                <h2 class="text-lg font-semibold text-gray-900 mb-3">{{ t('分步操作指南', 'Step-by-Step Guide') }}</h2>
                <ol class="space-y-3">
                  <li v-for="(step, index) in figure.steps" :key="index" class="flex gap-3">
                    <span class="flex-shrink-0 w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 text-sm font-bold flex items-center justify-center">{{ index + 1 }}</span>
                    <div class="prose prose-gray max-w-none pt-1"><p>{{ step }}</p></div>
                  </li>
                </ol>
              </section>

              <section v-if="figure.expected" class="mb-6">
                <h2 class="text-lg font-semibold text-gray-900 mb-2">{{ t('预期效果', 'Expected Outcome') }}</h2>
                <div class="prose prose-gray max-w-none bg-green-50 p-4 rounded-lg">
                  <p>{{ figure.expected }}</p>
                </div>
              </section>

              <section v-if="figure.case" class="mb-6">
                <h2 class="text-lg font-semibold text-gray-900 mb-2">{{ t('实战案例', 'Case Study') }}</h2>
                <div class="prose prose-gray max-w-none bg-gray-50 p-4 rounded-lg">
                  <p>{{ figure.case }}</p>
                </div>
              </section>

              <section v-if="timelineEvents.length > 0" class="mb-6">
                <h2 class="text-lg font-semibold text-gray-900 mb-3">{{ t('关键时间线', 'Key Timeline') }}</h2>
                <div class="relative pl-4 border-l-2 border-indigo-200">
                  <div v-for="(event, index) in timelineEvents" :key="index" class="relative pb-6 ml-4">
                    <div class="absolute left-[-10px] top-0 w-3 h-3 bg-indigo-500 rounded-full"></div>
                    <div class="bg-white p-4 rounded-lg border border-gray-100 shadow-sm">
                      <div class="flex items-center gap-2 mb-1">
                        <span class="text-lg">{{ event.icon }}</span>
                        <span class="text-sm font-medium text-gray-900">{{ event.label }}</span>
                      </div>
                      <p class="text-sm text-gray-600 ml-6">{{ event.value }}</p>
                    </div>
                    <div v-if="index < timelineEvents.length - 1" class="absolute left-[-4px] top-8 bottom-0 w-0.5 bg-indigo-100"></div>
                  </div>
                </div>
              </section>

              <section v-if="applicationScenarios.length > 0" class="mb-6">
                <h2 class="text-lg font-semibold text-gray-900 mb-3">{{ t('现代应用场景', 'Modern Application Scenarios') }}</h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <article v-for="scenario in applicationScenarios" :key="scenario.title.zh" class="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-lg hover:border-indigo-300 transition-all cursor-pointer">
                    <div class="flex items-start gap-3">
                      <span class="text-2xl">{{ scenario.icon }}</span>
                      <div class="flex-1">
                        <h4 class="font-semibold text-gray-900 mb-1">{{ locale === 'zh' ? scenario.title.zh : scenario.title.en }}</h4>
                        <p class="text-sm text-gray-600 mb-2">{{ locale === 'zh' ? scenario.description.zh : scenario.description.en }}</p>
                        <div class="flex flex-wrap gap-1">
                          <span v-for="tag in scenario.tags" :key="tag" class="px-2 py-0.5 text-xs font-medium rounded" :class="domainColors[tag] || 'bg-gray-100 text-gray-700'">{{ tag }}</span>
                        </div>
                      </div>
                    </div>
                  </article>
                </div>
              </section>

              <section v-if="similarFigures.length > 0" class="mb-6">
                <h2 class="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">{{ DATA_MODE === 'static' ? t('相似人物（标签重叠度）', 'Similar Figures (Tag Overlap)') : t('语义相似人物', 'Semantically Similar Figures') }}<svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.547a3.374 3.374 0 00-3.374-3.374l-.548-.547z" /></svg><span class="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded">{{ DATA_MODE === 'static' ? t('标签相似度', 'Tag Overlap') : t('语义搜索', 'Semantic Search') }}</span></h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  <article v-for="sim in similarFigures" :key="sim.code" @click="router.push({ name: 'figure-detail', params: { code: sim.code } })" class="bg-white border border-gray-200 rounded-xl p-4 hover:shadow-lg hover:border-indigo-300 transition-all cursor-pointer group">
                    <div class="flex items-start justify-between mb-3">
                      <span class="text-xs font-mono font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">{{ sim.code }}</span>
                      <span class="px-2 py-0.5 text-xs bg-green-50 text-green-700 rounded-full">{{ (sim.similarity_score * 100).toFixed(0) }}%</span>
                    </div>
                    <h4 class="font-semibold text-gray-900 mb-1 group-hover:text-indigo-600 transition-colors">{{ sim.name }}</h4>
                    <p class="text-sm text-gray-500 line-clamp-2">{{ sim.reason }}</p>
                    <div class="mt-2 flex flex-wrap gap-1">
                      <span v-for="modeId in sim.modes.slice(0, 3)" :key="modeId" class="px-2 py-0.5 text-xs font-medium rounded-full" :class="domainColors[modeDomainMap[modeId]] || 'bg-gray-100 text-gray-700'">#{{ modeId }}</span>
                    </div>
                  </article>
                </div>
              </section>
            </article>
          </div>
          <div class="space-y-6">
            <aside class="bg-white rounded-xl border border-gray-200 p-6 sticky top-24">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">{{ t('标签', 'Tags') }}</h3>
              <div class="space-y-4">
                <div v-if="figure.historical_domains && figure.historical_domains.length > 0">
                  <h4 class="text-sm font-medium text-gray-500 mb-2">{{ t('历史领域', 'Historical Domains') }}</h4>
                  <div class="flex flex-wrap gap-1.5">
                    <span v-for="domain in figure.historical_domains" :key="domain" class="px-2 py-1 text-xs font-medium rounded" :class="histDomainColors[domain] || 'bg-gray-100 text-gray-700'">{{ domain }}</span>
                  </div>
                </div>
                <div v-if="figure.domains && figure.domains.length > 0">
                  <h4 class="text-sm font-medium text-gray-500 mb-2">{{ t('思维领域', 'Thinking Domains') }}</h4>
                  <div class="flex flex-wrap gap-1.5">
                    <span v-for="domain in figure.domains" :key="domain" class="px-2 py-1 text-xs font-medium rounded" :class="domainColors[domain] || 'bg-gray-100 text-gray-700'">{{ domain }}</span>
                  </div>
                </div>
                <div v-if="figure.core_modes && figure.core_modes.length > 0">
                  <h4 class="text-sm font-medium text-gray-500 mb-2">{{ t('核心模式', 'Core Modes') }}</h4>
                  <div class="flex flex-wrap gap-1.5">
                    <span v-for="modeId in figure.core_modes" :key="modeId" class="px-2 py-1 text-xs font-medium bg-indigo-50 text-indigo-700 rounded-full">#{{ modeId }}</span>
                  </div>
                </div>
                <div v-if="figure.applications && figure.applications.length > 0">
                  <h4 class="text-sm font-medium text-gray-500 mb-2">{{ t('应用场景', 'Applications') }}</h4>
                  <div class="flex flex-wrap gap-1.5">
                    <span v-for="app in figure.applications" :key="app" class="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">{{ app }}</span>
                  </div>
                </div>
                <div class="pt-4 border-t border-gray-100">
                  <div v-if="figure.gender" class="flex items-center gap-2 text-sm text-gray-600 mb-2">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" /></svg>
                    {{ figure.gender }}
                  </div>
                  <div v-if="figure.ethnicity" class="flex items-center gap-2 text-sm text-gray-600">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l3 3a1 1 0 001.414 0l3-3a1 1 0 00.293-.707V6z" clip-rule="evenodd" /></svg>
                    {{ figure.ethnicity }}
                  </div>
                </div>
              </div>
            </aside>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
canvas { max-width: 100%; height: auto; }
.prose { font-size: 0.95rem; line-height: 1.7; }
.prose p { margin-bottom: 0.75rem; }
.relative.pl-4.border-l-2::before { content: ''; position: absolute; left: -4px; top: 8px; bottom: 0; width: 2px; background: #c7d2fe; }
.group:hover .group-hover\:text-indigo-600 { color: #4f46e5; }
.group:hover .group-hover\:border-indigo-300 { border-color: #c7d2fe; }
</style>