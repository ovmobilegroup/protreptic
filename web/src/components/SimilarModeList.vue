<script setup lang="ts">
/**
 * 「相似模式」区块：读 B1 预计算的 data/graph/similar_modes.json。
 *
 * 数据事实（B1 复核）：已发布的模式里只有 595 条有预计算邻居（1010 条边），
 * 邻居得分几乎都是 1（= 只共享 1 个 key_concepts），所以这里展示「共享概念」而不是分数；
 * 没有邻居是正常状态，必须显式告知，不能渲染成空区块。
 */
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { loadSimilarModes, type SimilarModeEntry } from '../api/graphData'
import { loadModeIndex, type ModeIndexEntry } from '../api/modeIndex'
import { useI18n } from '../composables/useI18n'

const props = withDefaults(defineProps<{ modeCode: string; limit?: number }>(), { limit: 5 })

const router = useRouter()
const { t, locale } = useI18n()

const entries = ref<SimilarModeEntry[]>([])
const index = ref<Map<string, ModeIndexEntry>>(new Map())
const state = ref<'loading' | 'ready' | 'unavailable'>('loading')

const describe = (e: SimilarModeEntry) => {
  const hit = index.value.get(e.modeCode)
  return {
    code: e.modeCode,
    name: hit ? (locale.value === 'zh' ? hit.nameZh : (hit.nameEn || hit.nameZh)) : e.modeCode,
    figure: hit?.figureName || hit?.figureCode || '',
    figureCode: hit?.figureCode || '',
    concepts: (e.sharedConcepts || []).slice(0, 3),
    sameDomain: e.sameDomain,
  }
}

const load = async () => {
  state.value = 'loading'
  const payload = await loadSimilarModes()
  if (!payload) {
    state.value = 'unavailable'
    entries.value = []
    return
  }
  const hit = payload.modes?.[props.modeCode]
  entries.value = Array.isArray(hit) ? hit.slice(0, props.limit) : []
  const idx = await loadModeIndex().catch(() => [])
  index.value = new Map(idx.map((m) => [m.modeCode, m]))
  state.value = 'ready'
}

watch(() => props.modeCode, load)
onMounted(load)
</script>

<template>
  <div class="mt-5 rounded-xl border border-white/10 bg-white/[.02] p-4">
    <div class="mb-2 flex flex-wrap items-center gap-2">
      <h3 class="text-xs uppercase tracking-wider text-parchment/40">{{ t('相似模式', 'Similar modes') }}</h3>
      <span class="pt-chip-mute !text-[10px]">{{ t('概念交集预计算', 'Concept-overlap precomputed') }}</span>
    </div>

    <p v-if="state === 'loading'" class="text-xs text-parchment/45">{{ t('加载相似模式…', 'Loading similar modes…') }}</p>

    <p v-else-if="state === 'unavailable'" class="text-xs text-parchment/45">
      {{ t('相似模式数据不可用（data/graph/similar_modes.json 未取到）', 'Similar-mode data unavailable (data/graph/similar_modes.json not fetched)') }}
    </p>

    <p v-else-if="!entries.length" class="text-xs text-parchment/45">
      {{ t('该模式没有预计算的相似模式（与其它模式无 key_concepts 交集）', 'No precomputed neighbour for this mode (no key_concepts overlap with other modes)') }}
    </p>

    <div v-else class="flex flex-wrap gap-2">
      <button
        v-for="e in entries" :key="e.modeCode"
        type="button"
        :disabled="!describe(e).figureCode"
        class="group max-w-full rounded-lg border border-white/10 bg-white/[.03] px-3 py-2 text-left
               transition-colors duration-300 hover:border-jade-400/40 hover:bg-white/[.06]
               disabled:cursor-default disabled:opacity-70"
        @click="describe(e).figureCode && router.push({ name: 'mind', params: { code: describe(e).figureCode } })"
      >
        <span class="flex flex-wrap items-baseline gap-x-2 gap-y-1">
          <span class="font-mono text-[10px] text-gold-400/70">{{ e.modeCode }}</span>
          <span class="text-sm text-parchment/85">{{ describe(e).name }}</span>
          <span v-if="describe(e).figure" class="text-xs text-parchment/45">{{ describe(e).figure }}</span>
          <span v-if="e.sameDomain" class="pt-chip-mute !text-[10px]">{{ t('同领域', 'same domain') }}</span>
        </span>
        <span v-if="describe(e).concepts.length" class="mt-1 flex flex-wrap gap-1">
          <span v-for="c in describe(e).concepts" :key="c" class="rounded bg-white/[.05] px-1.5 py-0.5 text-[10px] text-jade-200/70">
            {{ c }}
          </span>
        </span>
      </button>
    </div>
  </div>
</template>
