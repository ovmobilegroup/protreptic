<script setup lang="ts">
/**
 * 「每日一模式」卡片 (Phase30-B4) —— 首页模块与 /daily 归档页共用。
 *
 * 数据来自两次请求：
 *   1) daily/index.json（父级已经加载好，这里只接收 pick）—— 定位「今天是哪一条」；
 *   2) modes/by-figure/{figure_code}.json —— 详情（定义 / 步骤 / 出处 / 原话），与 /minds/:code 同一份分片。
 * 详情分片拉不到时不清空卡片，只降级成「编号 + 人物 + 名称」并如实提示，不假装有内容。
 */
import { computed, ref, watch } from 'vue'
import { useI18n } from '../composables/useI18n'
import { fetchFigureModes } from '../api/static'
import SourceCitation from './SourceCitation.vue'
import { weekdayLabel, type DailyNameRow, type DailyPick } from '../api/dailyMode'
import { useCompare } from '../composables/useCompare'
import { MAX_COMPARE_ITEMS } from '../api/compareData'

const props = defineProps<{
  pick: DailyPick
  /** 归档页可顺带传入名称表里的一行；首页不传，名称从详情分片取 */
  name?: DailyNameRow | null
  /**
   * 隐藏「加入对比」按钮。用「隐藏」而不是「显示」开关是因为 Vue 会把缺席的 boolean prop
   * 统一转成 false —— 写成 showCompare?: boolean 时缺省值等于关掉按钮（实测渲染成 <!---->）。
   */
  hideCompare?: boolean
}>()

const { t, locale } = useI18n()
const { codes: compareCodes, add: addCompare } = useCompare()
const compareNotice = ref('')
const compareFull = computed(() => compareCodes.value.length >= MAX_COMPARE_ITEMS)

const payload = ref<Record<string, any> | null>(null)
const loading = ref(false)
const detailFailed = ref(false)

const pickText = (value: unknown): string =>
  Array.isArray(value) ? String(value[0] ?? '') : String(value ?? '')

const mode = computed(() => {
  const modes = (payload.value?.modes as Array<Record<string, any>>) || []
  return modes.find((m) => String(m.mode_code || m.id || '') === props.pick.modeCode) || null
})

const figureName = computed(
  () => String(payload.value?.figure_name || props.pick.figureName || props.pick.figureCode || '')
)

const modeName = computed(() => {
  const m = mode.value
  if (locale.value === 'en') {
    return pickText(m?.name_en) || props.name?.nameEn || pickText(m?.name_zh) || props.name?.nameZh || props.pick.modeCode
  }
  return pickText(m?.name_zh) || props.name?.nameZh || props.pick.modeCode
})

const modeNameAlt = computed(() => {
  const m = mode.value
  return locale.value === 'en' ? (pickText(m?.name_zh) || props.name?.nameZh) : (pickText(m?.name_en) || props.name?.nameEn)
})

const category = computed(() => String(mode.value?.category || props.name?.category || ''))

const definition = computed(() => {
  const m = mode.value
  if (!m) return ''
  return locale.value === 'en'
    ? (pickText(m.definition_en) || pickText(m.definition_zh))
    : (pickText(m.definition_zh) || pickText(m.definition_en))
})

const steps = computed(() => {
  const m = mode.value
  if (!m) return [] as string[]
  const raw = locale.value === 'en' ? (m.process_en || m.process_zh) : (m.process_zh || m.process_en)
  const list = Array.isArray(raw) ? raw : []
  return list.slice(0, 3).map((s: unknown) => pickText(s))
})

const source = computed(() => String(mode.value?.source_chapter || ''))

// Phase38-Y2：构建期注入的出处分段 + 核验状态（分片没有这两个字段时退回纯文本，行为与注入前一致）
const sourceParts = computed<unknown[]>(() => {
  const raw = mode.value?.source_parts
  return Array.isArray(raw) ? raw : []
})
const verification = computed(() => mode.value?.verification ?? null)

const quote = computed(() => {
  const m = mode.value
  if (!m) return ''
  return locale.value === 'en'
    ? (pickText(m.key_quote_en) || pickText(m.key_quote_zh))
    : (pickText(m.key_quote_zh) || pickText(m.key_quote_en))
})

const weekday = computed(() => weekdayLabel(props.pick.dateKey, locale.value))

const load = async () => {
  payload.value = null
  detailFailed.value = false
  if (!props.pick.figureCode) return
  loading.value = true
  const data = await fetchFigureModes(props.pick.figureCode)
  loading.value = false
  if (data) {
    payload.value = data as unknown as Record<string, any>
  } else {
    detailFailed.value = true
  }
}

const addToCompare = () => {
  const result = addCompare(props.pick.modeCode)
  compareNotice.value =
    result === 'added' ? t('已加入对比', 'Added to compare')
      : result === 'duplicate' ? t('已在对比列表中', 'Already in compare')
        : t(`最多对比 ${MAX_COMPARE_ITEMS} 项，请先在对比页移除一项`, `At most ${MAX_COMPARE_ITEMS} items — remove one on /compare`)
}

watch(() => props.pick.modeCode, load, { immediate: true })
</script>

<template>
  <article class="pt-panel relative overflow-hidden p-6 sm:p-7">
    <div aria-hidden="true"
         class="pointer-events-none absolute -top-24 -right-16 h-56 w-56 rounded-full bg-gold-500/10 blur-3xl"></div>

    <div class="relative">
      <div class="mb-4 flex flex-wrap items-center gap-2">
        <span class="pt-code">{{ t('每日一模式 · DAILY MODE', 'DAILY MODE') }}</span>
        <span class="pt-chip-gold">{{ pick.dateKey }}</span>
        <span class="pt-chip-mute">{{ weekday }}</span>
        <RouterLink to="/daily"
                    class="ml-auto text-xs font-medium text-gold-300/80 transition-colors hover:text-gold-200">
          {{ t('查看归档 →', 'Archive →') }}
        </RouterLink>
      </div>

      <div v-if="loading" class="space-y-3">
        <div class="pt-skeleton h-7 w-2/3"></div>
        <div class="pt-skeleton h-4 w-1/3"></div>
        <div class="pt-skeleton h-16 w-full"></div>
      </div>

      <template v-else>
        <h3 class="font-display text-2xl font-bold leading-snug text-parchment sm:text-[26px]">
          {{ modeName }}
        </h3>
        <p v-if="modeNameAlt" class="mt-1 font-mono text-xs text-parchment/40">{{ modeNameAlt }}</p>

        <div class="mt-3 flex flex-wrap items-center gap-2">
          <span class="pt-chip-mute font-mono">{{ pick.modeCode }}</span>
          <span v-if="category" class="pt-chip-jade">{{ category }}</span>
          <RouterLink :to="`/minds/${pick.figureCode}`" class="pt-chip-gold hover:border-gold-400/60">
            {{ t(`人物 · ${figureName || pick.figureCode}`, `Figure · ${figureName || pick.figureCode}`) }}
          </RouterLink>
        </div>

        <p v-if="definition" class="mt-4 line-clamp-3 text-sm leading-relaxed text-parchment/75">
          {{ definition }}
        </p>

        <ol v-if="steps.length" class="mt-4 space-y-1.5 border-t border-white/[0.08] pt-4">
          <li v-for="(step, i) in steps" :key="i" class="flex gap-2.5 text-[13px] leading-relaxed text-parchment/65">
            <span class="mt-0.5 shrink-0 font-mono text-[11px] text-gold-400/80">{{ i + 1 }}</span>
            <span class="min-w-0">{{ step }}</span>
          </li>
        </ol>
        <p v-if="!steps.length && detailFailed" class="mt-4 border-t border-white/[0.08] pt-4 text-xs leading-relaxed text-amber-200/70">
          {{ t('详情分片暂不可用（离线或数据未就绪）：只显示编号与人物，不假装有内容。',
               'Detail shard unavailable (offline or data not ready) — showing code and figure only.') }}
        </p>

        <blockquote v-if="source || quote"
                    class="mt-4 border-l-2 border-gold-500/40 pl-4 text-[13px] leading-relaxed text-parchment/60">
          <p v-if="source" class="mb-1"><span class="text-gold-300/80">{{ t('出处', 'Source') }}</span> · <SourceCitation :parts="sourceParts" :text="source" :verification="verification" /></p>
          <p v-if="quote" class="text-jade-200/80">「{{ quote }}」</p>
        </blockquote>

        <div class="mt-5 flex flex-wrap items-center gap-3 border-t border-white/[0.08] pt-4">
          <RouterLink :to="`/minds/${pick.figureCode}`" class="pt-btn-ghost">
            {{ t(`看 ${figureName || pick.figureCode} 的完整档案`, `Open ${figureName || pick.figureCode}'s archive`) }}
          </RouterLink>
          <button v-if="!hideCompare" class="pt-btn-ghost" :disabled="compareFull" @click="addToCompare">
            {{ t('加入对比', 'Add to compare') }}
          </button>
          <span v-if="compareNotice" class="text-xs text-gold-200/70">{{ compareNotice }}</span>
        </div>
      </template>
    </div>
  </article>
</template>
