<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'
import { useRouter } from 'vue-router'

interface Entry {
  code: string
  name: string
  type: 'figure' | 'scenario'
  era?: string
  domains?: string[]
  historical_domains?: string[]
  n_modes?: number
  description?: string
}

const props = defineProps<{ entry: Entry }>()
const router = useRouter()
const { t, locale } = useI18n()

const eraLabels: Record<string, { zh: string; en: string }> = {
  'Pre-Qin': { zh: '先秦', en: 'Pre-Qin' }, 'Qin-Han': { zh: '秦汉', en: 'Qin-Han' },
  'Three-Kingdoms-Jin': { zh: '三国两晋', en: '3K & Jin' }, 'Northern-Southern': { zh: '南北朝', en: 'N.&S. Dyn.' },
  'Sui-Tang': { zh: '隋唐', en: 'Sui-Tang' }, 'Song-Yuan': { zh: '宋元', en: 'Song-Yuan' },
  'Ming-Qing': { zh: '明清', en: 'Ming-Qing' }, 'Modern-Early': { zh: '近代', en: 'Early Modern' },
  Modern: { zh: '现代', en: 'Modern' },
}
const histDoms: Record<string, { zh: string; en: string }> = {
  Military: { zh: '军事', en: 'Military' }, Philosophy: { zh: '哲学', en: 'Philosophy' },
  Governance: { zh: '治理', en: 'Governance' }, Science_Tech: { zh: '科技', en: 'Sci & Tech' },
  Historiography: { zh: '史学', en: 'History' }, Literature_Arts: { zh: '文艺', en: 'Arts' },
  Religion: { zh: '宗教', en: 'Religion' }, Education: { zh: '教育', en: 'Education' },
  Economics: { zh: '经济', en: 'Economics' }, Ethics: { zh: '伦理', en: 'Ethics' },
}

const isFigure = computed(() => props.entry.type === 'figure')
const eraLabel = computed(() => {
  const e = props.entry.era
  if (!e) return ''
  return eraLabels[e]?.[locale.value] || e
})
const tags = computed(() =>
  (props.entry.historical_domains || []).slice(0, 2).map((d) => histDoms[d]?.[locale.value] || d)
)
const open = () => {
  router.push(isFigure.value
    ? { name: 'mind', params: { code: props.entry.code } }
    : { name: 'figure-detail', params: { code: props.entry.code } })
}
</script>

<template>
  <article
    @click="open"
    tabindex="0"
    @keydown.enter="open"
    @keydown.space.prevent="open"
    class="group relative flex cursor-pointer flex-col overflow-hidden rounded-2xl border border-white/10
           bg-white/[.03] p-5 transition-all duration-500 ease-silk
           hover:-translate-y-1 hover:bg-white/[.055]"
    :class="isFigure ? 'hover:border-gold-500/45 hover:shadow-glow' : 'hover:border-jade-400/40'"
  >
    <div aria-hidden="true"
         class="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100"
         :style="isFigure
           ? 'background: radial-gradient(420px 180px at 50% 0%, rgba(212,162,76,.14), transparent 70%)'
           : 'background: radial-gradient(420px 180px at 50% 0%, rgba(94,234,212,.10), transparent 70%)'"></div>

    <!-- 顶部 -->
    <div class="relative mb-3 flex items-center justify-between gap-2">
      <span class="pt-code">{{ entry.code }}</span>
      <span :class="isFigure ? 'pt-chip-gold' : 'pt-chip-jade'">
        {{ isFigure ? t('人物', 'Figure') : t('场景', 'Scenario') }}
      </span>
    </div>

    <h3 class="relative font-display text-xl font-bold leading-snug text-parchment
               transition-colors duration-300 line-clamp-2"
        :class="isFigure ? 'group-hover:text-gold-200' : 'group-hover:text-jade-300'">
      {{ entry.name || entry.code }}
    </h3>

    <span v-if="!entry.name"
          class="relative mt-1.5 w-fit rounded-md border border-amber-400/25 bg-amber-400/[.07] px-2 py-0.5
                 text-[11px] text-amber-200/80">
      {{ t('档案待核名', 'Name pending review') }}
    </span>

    <p v-if="entry.description" class="relative mt-2.5 text-sm leading-relaxed text-parchment/70 line-clamp-3">
      {{ entry.description }}
    </p>

    <!-- 模式数 -->
    <div v-if="entry.n_modes" class="relative mt-4 flex flex-wrap items-center gap-2">
      <span class="pt-chip-mute">{{ t(`${entry.n_modes} 条模式`, `${entry.n_modes} modes`) }}</span>
      <span v-if="eraLabel" class="pt-chip-mute max-w-[14rem] truncate">{{ eraLabel }}</span>
    </div>

    <!-- 底部 -->
    <div class="relative mt-4 flex items-center justify-between gap-3 border-t border-white/[0.08] pt-3.5">
      <div class="flex flex-wrap gap-1.5">
        <span v-for="d in tags" :key="d" class="text-xs text-parchment/45">{{ d }}</span>
      </div>
      <span class="flex items-center gap-1 text-xs font-medium transition-all duration-300"
            :class="isFigure
              ? 'text-gold-400/0 group-hover:text-gold-300'
              : 'text-jade-400/0 group-hover:text-jade-300'">
        {{ isFigure ? t('看模式', 'Modes') : t('看详情', 'Detail') }}
        <svg class="h-3.5 w-3.5 transition-transform duration-300 group-hover:translate-x-0.5"
             fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </span>
    </div>
  </article>
</template>
