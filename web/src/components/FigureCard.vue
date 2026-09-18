<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'
import { useRouter } from 'vue-router'

interface Props {
  figure: {
    code: string
    name: string
    description: string
    modes: number[]
    reason: string
    steps: string[]
    expected: string
    case: string
    era: string | null
    historical_domains: string[]
    domains: string[]
    gender: string | null
    ethnicity: string | null
  }
  lang: 'zh' | 'en'
}

const props = defineProps<Props>()
const router = useRouter()
const { t } = useI18n()

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
  Military: { zh: '军事', en: 'Military' },
  Philosophy: { zh: '哲学', en: 'Philosophy' },
  Governance: { zh: '治理', en: 'Governance' },
  Science_Tech: { zh: '科技', en: 'Sci & Tech' },
  Historiography: { zh: '史学', en: 'History' },
  Literature_Arts: { zh: '文艺', en: 'Arts' },
  Religion: { zh: '宗教', en: 'Religion' },
  Education: { zh: '教育', en: 'Education' },
  Economics: { zh: '经济', en: 'Economics' },
  Ethics: { zh: '伦理', en: 'Ethics' },
}

const navigateToDetail = () => {
  router.push({ name: 'figure-detail', params: { code: props.figure.code } })
}

const eraLabel = computed(() => {
  if (!props.figure.era) return ''
  return eraLabels[props.figure.era]?.[props.lang] || props.figure.era
})

const histDoms = computed(() =>
  (props.figure.historical_domains || [])
    .slice(0, 2)
    .map((d) => histDomainLabels[d]?.[props.lang] || d)
)
</script>

<template>
  <article
    @click="navigateToDetail"
    tabindex="0"
    @keydown.enter="navigateToDetail"
    @keydown.space.prevent="navigateToDetail"
    class="group relative flex cursor-pointer flex-col overflow-hidden rounded-2xl border border-white/10
           bg-white/[.03] p-5 transition-all duration-500 ease-silk
           hover:-translate-y-1 hover:border-gold-500/45 hover:bg-white/[.055] hover:shadow-glow"
  >
    <!-- 悬停金晕 -->
    <div aria-hidden="true"
         class="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500
                group-hover:opacity-100"
         style="background: radial-gradient(420px 180px at 50% 0%, rgba(212,162,76,.14), transparent 70%)"></div>

    <!-- 顶部：编号 + 时代 -->
    <div class="relative mb-3 flex items-center justify-between gap-2">
      <span class="pt-code">{{ props.figure.code }}</span>
      <span v-if="eraLabel" class="pt-chip-mute">{{ eraLabel }}</span>
    </div>

    <!-- 名称 -->
    <h3 class="relative font-display text-xl font-bold leading-snug text-parchment
               transition-colors duration-300 group-hover:text-gold-200 line-clamp-2">
      {{ props.figure.name }}
    </h3>

    <!-- 描述 -->
    <p v-if="props.figure.description" class="relative mt-2.5 text-sm leading-relaxed text-parchment/55 line-clamp-3">
      {{ props.figure.description }}
    </p>

    <!-- 思维模式编号 -->
    <div v-if="props.figure.modes?.length" class="relative mt-4 flex flex-wrap gap-1.5">
      <span v-for="modeId in props.figure.modes.slice(0, 4)" :key="modeId" class="pt-chip-jade">
        #{{ modeId }}
      </span>
      <span v-if="props.figure.modes.length > 4" class="pt-chip-mute">
        +{{ props.figure.modes.length - 4 }}
      </span>
    </div>

    <!-- 底部：领域 + 箭头 -->
    <div class="relative mt-4 flex items-center justify-between gap-3 border-t border-white/[0.08] pt-3.5">
      <div class="flex flex-wrap gap-1.5">
        <span v-for="d in histDoms" :key="d" class="text-xs text-parchment/45">{{ d }}</span>
        <span v-if="!(histDoms.length)" class="text-xs text-parchment/30">—</span>
      </div>
      <span class="flex items-center gap-1 text-xs font-medium text-gold-400/0 transition-all duration-300
                   group-hover:text-gold-300">
        {{ t('查看', 'Open') }}
        <svg class="h-3.5 w-3.5 transition-transform duration-300 group-hover:translate-x-0.5"
             fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </span>
    </div>
  </article>
</template>
