<script setup lang="ts">
/**
 * /daily —— 「每日一模式」归档页 (Phase30-B4)。
 *
 * 一页回答两件事：
 *   1) 某一天（默认今天，可用 ?date=YYYY-MM-DD 指定）选中了哪条模式，为什么是这一条；
 *   2) 往前每一历史日选中了哪条 —— 因为选取是「日期取模」，历史不需要另存一份记录，
 *      任何日期都能当场算出来（见 api/dailyMode.ts 的确定性契约）。
 * 数据：daily/index.json（定位，12 KB gzip）+ daily/names.json（历史每天的模式名，175 KB gzip）。
 * 详情：选中那一天的卡片再拉一次 modes/by-figure/{code}.json。
 */
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { SITE_COUNTS } from '../generated/siteCounts'
import DailyModeCard from '../components/DailyModeCard.vue'
import {
  DAILY_ARCHIVE_PAGE_SIZE,
  isDateKey,
  listDays,
  loadDailyIndex,
  loadDailyNames,
  nameFor,
  weekdayLabel,
  pickAt,
  shiftDateKey,
  todayKey,
  TZ_LABEL,
  type DailyIndex,
  type DailyNameRow,
  type DailyPick,
} from '../api/dailyMode'
import { setSeo, truncateSeo } from '../composables/useSeo'

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()

const index = ref<DailyIndex | null>(null)
const names = ref<DailyNameRow[] | null>(null)
const loading = ref(true)
const namesFailed = ref(false)
const archiveCount = ref(DAILY_ARCHIVE_PAGE_SIZE)

const today = todayKey()
const initial = String(route.query.date || '')
const dateKey = ref(isDateKey(initial) ? initial : today)


const selectedPick = computed<DailyPick | null>(() => (index.value ? pickAt(index.value, dateKey.value) : null))
const selectedName = computed<DailyNameRow | null>(() => (selectedPick.value ? nameFor(names.value, selectedPick.value.index) : null))

const archive = computed<DailyPick[]>(() => (index.value ? listDays(index.value, dateKey.value, archiveCount.value) : []))

const nameOf = (index_: number): DailyNameRow | null => nameFor(names.value, index_)

const displayName = (pick: DailyPick): string => {
  const row = nameOf(pick.index)
  if (!row) return pick.modeCode
  if (locale.value === 'en') return row.nameEn || row.nameZh || pick.modeCode
  return row.nameZh || pick.modeCode
}

const selectDate = (key: string) => {
  if (!isDateKey(key)) return
  dateKey.value = key
  router.replace({ query: { ...route.query, date: key } })
}

const step = (days: number) => selectDate(shiftDateKey(dateKey.value, days))
const backToToday = () => selectDate(today)
const isToday = computed(() => dateKey.value === today)
const canGoForward = computed(() => dateKey.value < today)

const loadMore = () => { archiveCount.value += DAILY_ARCHIVE_PAGE_SIZE }

const applySeo = () => {
  const pick = selectedPick.value
  const description = pick
    ? truncateSeo(
        `${pick.dateKey} 选中的思维模式：${displayName(pick)}（${pick.modeCode}，${pick.figureName || pick.figureCode}）。每日一模式按「日期对模式总数取模」选出，同一日重复打开结果一致；本页可回看任意历史日期。`,
      )
    : '每日一模式归档：按「日期对模式总数取模」选出当天的思维模式，同一日重复打开结果一致。'
  setSeo({ title: '每日一模式 - 今日与历史归档', description, path: 'daily' })
}

const load = async () => {
  loading.value = true
  const [idx, nm] = await Promise.all([loadDailyIndex(), loadDailyNames()])
  index.value = idx
  names.value = nm
  namesFailed.value = !nm
  loading.value = false
  applySeo()
}

onMounted(load)
</script>

<template>
  <div class="pt-container pb-20 pt-10">
    <section class="mb-8">
      <div class="mb-3 flex items-center gap-3">
        <span class="pt-hairline w-10"></span>
        <span class="pt-code">{{ t('每日一模式 · 归档', 'DAILY MODE · ARCHIVE') }}</span>
      </div>
      <h1 class="pt-h1"><span class="pt-gradient-text">{{ t('每日一模式', 'Daily Mode') }}</span></h1>
      <p class="mt-4 max-w-3xl text-base leading-relaxed text-parchment/55">
        {{ t(
          '每天从全部历史人物思维模式里选出一条：谁都不掷骰子，直接按「这一天是第几天」对模式总数取模。因此同一天无论何时打开、换哪台设备，看到的都是同一条；往前翻任意历史日期，也能当场算出那天是哪一条（当前条数见下方「为什么是这一条」）。',
          `One mode a day out of ${SITE_COUNTS.modes}: no dice — the day number modulo the mode count. The same day always yields the same mode, on any device; any past date can be recomputed on the spot.`
        ) }}
      </p>
    </section>

    <div v-if="loading" class="pt-panel mb-8 p-6">
      <div class="pt-skeleton mb-3 h-6 w-1/2"></div>
      <div class="pt-skeleton h-24 w-full"></div>
    </div>

    <div v-else-if="!index" class="pt-panel mb-8 px-6 py-14 text-center">
      <div class="mb-3 text-4xl opacity-70">🕳️</div>
      <h2 class="pt-h3 mb-2 text-parchment/90">{{ t('每日一模式数据未就绪', 'Daily data unavailable') }}</h2>
      <p class="text-sm leading-relaxed text-parchment/50">
        {{ t(
          '未能读取 data/daily/index.json（离线或构建产物缺失）。这里如实报错，不会退化成随机数——随机就不可复现了。',
          'Could not read data/daily/index.json (offline or missing build output). No random fallback: randomness would break reproducibility.'
        ) }}
      </p>
    </div>

    <template v-else>
      <!-- 选中日期的卡片 -->
      <section class="mb-6">
        <div class="mb-4 flex flex-wrap items-center gap-2">
          <button class="pt-btn-ghost" @click="step(-1)">{{ t('← 前一日', '← Previous') }}</button>
          <button class="pt-btn-ghost" :disabled="!canGoForward" @click="step(1)">{{ t('后一日 →', 'Next →') }}</button>
          <button v-if="!isToday" class="pt-btn-ghost" @click="backToToday">{{ t('回到今天', 'Today') }}</button>
          <label class="ml-auto flex items-center gap-2 text-xs text-parchment/50">
            {{ t('指定日期', 'Pick a date') }}
            <input type="date" class="pt-input w-40 py-1.5 text-xs" :value="dateKey" @change="selectDate(($event.target as HTMLInputElement).value)" />
          </label>
        </div>

        <DailyModeCard v-if="selectedPick" :pick="selectedPick" :name="selectedName" />
      </section>

      <!-- 算法说明：把算式摆出来，可核对 -->
      <section class="pt-panel mb-8 p-5 sm:p-6">
        <h2 class="pt-h3 mb-3">{{ t('为什么是这一条', 'Why this mode') }}</h2>
        <p class="font-mono text-sm leading-relaxed text-gold-200/85">
          {{ selectedPick ? `${selectedPick.dateKey} → 第 ${selectedPick.dayNumber} 天` : '' }}
          <span class="text-parchment/45"> mod </span>{{ index.total }}
          <span class="text-parchment/45"> = </span>{{ selectedPick?.index }}
          <span class="text-parchment/45"> → </span>{{ selectedPick?.modeCode }}
        </p>
        <ul class="mt-3 space-y-1.5 text-xs leading-relaxed text-parchment/50">
          <li>· {{ t(`时区固定 ${TZ_LABEL}（UTC+8）：每天 0 点换一条，与访问者所在时区无关。`, `Fixed timezone ${TZ_LABEL} (UTC+8): the mode changes at local midnight, regardless of visitor timezone.`) }}</li>
          <li>· {{ t(`索引口径：${index.total} 条模式 / ${index.figureCount} 位人物，已剔除确证虚构的人物（H-SX-001）。`, `Index: ${index.total} modes / ${index.figureCount} figures, excluding the debunked H-SX-001.`) }}</li>
          <li>· {{ t(`取模意味着"总天数"是唯一变量：同一天重复打开一定相同；但数据集新增人物/模式后，历史每天的选取会重排，这是确定性算法的固有限制，本页不假装长期不变。`, 'Modulo means the day count is the only variable: same day, same mode; adding new figures/modes will reshuffle past days — an inherent limit of this deterministic rule, stated rather than hidden.') }}</li>
          <li v-if="index.generatedAt">· {{ t('数据构建时间', 'Index built at') }}：{{ index.generatedAt }}</li>
        </ul>
      </section>

      <!-- 历史归档 -->
      <section>
        <div class="mb-4 flex items-baseline gap-3">
          <h2 class="pt-h2">{{ t('历史每日模式', 'Past daily modes') }}</h2>
          <span class="text-sm text-parchment/40">{{ t(`自 ${dateKey} 往前 ${archive.length} 天`, `${archive.length} days back from ${dateKey}`) }}</span>
        </div>
        <p v-if="namesFailed" class="mb-3 text-xs text-amber-200/70">
          {{ t('名称表（data/daily/names.json）未就绪：列表只显示模式编号与人物，不假装有名称。',
               'Names table (data/daily/names.json) unavailable — showing mode codes only.') }}
        </p>

        <ol class="pt-panel divide-y divide-white/[0.06] overflow-hidden">
          <li v-for="pick in archive" :key="pick.dateKey">
            <div class="flex flex-wrap items-center gap-x-4 gap-y-2 px-5 py-3.5 transition-colors hover:bg-white/[.03]">
              <button class="flex min-w-[7.5rem] shrink-0 items-baseline gap-2 text-left" @click="selectDate(pick.dateKey)">
                <span class="font-mono text-xs" :class="pick.dateKey === dateKey ? 'text-gold-300' : 'text-parchment/60'">{{ pick.dateKey }}</span>
                <span class="text-[11px] text-parchment/35">{{ weekdayLabel(pick.dateKey, locale) }}</span>
              </button>
              <span class="min-w-0 flex-1 truncate text-sm text-parchment/85" :title="displayName(pick)">
                {{ displayName(pick) }}
              </span>
              <span v-if="nameOf(pick.index)?.category" class="pt-chip-mute shrink-0">{{ nameOf(pick.index)?.category }}</span>
              <RouterLink :to="`/minds/${pick.figureCode}`"
                          class="shrink-0 text-xs text-gold-300/80 transition-colors hover:text-gold-200">
                {{ pick.figureName || pick.figureCode }} →
              </RouterLink>
            </div>
          </li>
        </ol>

        <div class="mt-6 flex justify-center">
          <button class="pt-btn-ghost" @click="loadMore">{{ t('加载更早 30 天', 'Load 30 more days') }}</button>
        </div>
      </section>
    </template>
  </div>
</template>
