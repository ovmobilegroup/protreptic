<script setup lang="ts">
/**
 * 可信度徽章（Phase38-Y3）—— credibility_framework.md §3 的四态在 UI 里的**唯一实现**。
 *
 * 四态（符号与文案固定，别处不许再写一套）：
 *   verified     ✓ 已核验（出处可点）    玉绿：出处可达，且已解析出可点链接
 *   pending      ○ 待核验                灰：schema 缺省态，尚未核验
 *   suspect      ⚠ 存疑                  琥珀：命中 D1–D5 之一，待复核（显眼、不美化）
 *   unverifiable — 一手材料              灰：口述/信札等本质不可链接，诚实标注而非硬造链接
 *
 * 数据形状（构建期写入 data/modes_data.json，tools/export_static_site.py 原样带进 by-figure 分片）：
 *   verification = { status, method, evidence, checked_at, checker }，也容忍直接传 status 字符串。
 *
 * 诚实约定（本组件不做的事）：
 *   * **字段缺失不猜状态**：verification 为空、或 status 不在四态内 → 不渲染任何徽章，
 *     不假装成 pending（少一个标记 ≠ 编一个状态）。
 *   * 悬浮说明只拼字段里**真实存在**的内容，缺失的字段写「未记录」，不补故事。
 */
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'

interface Verification {
  status?: unknown
  method?: unknown
  evidence?: unknown
  checked_at?: unknown
  checker?: unknown
}

const props = defineProps<{ verification?: unknown; class?: string }>()
const { t, locale } = useI18n()

const STATUSES = ['verified', 'pending', 'suspect', 'unverifiable'] as const
type Status = (typeof STATUSES)[number]

const info = computed<Verification | null>(() => {
  const v = props.verification
  if (!v) return null
  if (typeof v === 'string') return { status: v }
  return typeof v === 'object' ? (v as Verification) : null
})

const status = computed<Status | ''>(() => {
  const s = info.value?.status
  return typeof s === 'string' && (STATUSES as readonly string[]).includes(s) ? (s as Status) : ''
})

const MARK: Record<Status, string> = { verified: '✓', pending: '○', suspect: '⚠', unverifiable: '—' }

const label = computed(() => {
  switch (status.value) {
    case 'verified': return t('已核验', 'Verified')
    case 'pending': return t('待核验', 'Pending')
    case 'suspect': return t('存疑', 'Suspect')
    case 'unverifiable': return t('一手材料', 'Primary source')
    default: return ''
  }
})

/** 悬浮说明：状态含义 + 字段里真实存在的复核线索（缺失写「未记录」，不补故事） */
const tooltip = computed(() => {
  if (!status.value) return ''
  const head = {
    verified: t('可信度：已核验 —— 出处可达，且有可点链接', 'Credibility: verified — source reachable, link available'),
    pending: t('可信度：待核验 —— 尚未核验（schema 缺省态）', 'Credibility: pending — not yet checked (schema default)'),
    suspect: t('可信度：存疑 —— 命中缺陷规则，待复核', 'Credibility: suspect — matched a defect rule, pending review'),
    unverifiable: t('可信度：一手材料 —— 口述/信札等本质不可链接，诚实标注', 'Credibility: primary source — not linkable by nature, labelled honestly'),
  }[status.value]
  const field = (v: unknown, zh: string, en: string) => {
    const text = typeof v === 'string' && v.trim() ? v.trim() : t('未记录', 'not recorded')
    return t(zh, en) + ': ' + text
  }
  return [
    head,
    field(info.value?.method, '核验方式', 'method'),
    field(info.value?.evidence, '证据', 'evidence'),
    field(info.value?.checked_at, '核验时间', 'checked_at'),
    field(info.value?.checker, '核验人', 'checker'),
  ].join('\n')
})

const CHIP: Record<Status, string> = {
  verified: 'border-jade-400/45 bg-jade-400/10 text-jade-200',
  pending: 'border-white/15 bg-white/[.04] text-parchment/60',
  suspect: 'border-amber-400/70 bg-amber-400/15 text-amber-200',
  unverifiable: 'border-white/15 bg-white/[.04] text-parchment/60',
}
const chipClass = computed(() => (status.value ? CHIP[status.value] : ''))
</script>

<template>
  <span
    v-if="status"
    class="inline-flex shrink-0 items-center gap-1.5 whitespace-nowrap rounded-full border px-2.5 py-0.5 text-[11px] font-medium leading-5"
    :class="[chipClass, props.class]"
    :data-credibility="status"
    :data-credibility-mark="MARK[status]"
    :title="tooltip"
  >
    <span aria-hidden="true" class="font-mono">{{ MARK[status] }}</span>
    <span>{{ label }}</span>
  </span>
</template>
