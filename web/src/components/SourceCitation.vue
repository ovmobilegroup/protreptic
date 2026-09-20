<script setup lang="ts">
/**
 * 出处渲染（Phase38-Y2）：有构建期注入的 source_parts 就按段渲染 —— 可点段给 <a target="_blank"> ，
 * 其余保持纯文本；没有 source_parts（旧分片 / 未注入）就退回纯文本 text 。
 *
 * 数据契约见 tools/export_static_site.py 的 inject_citation_links() ：
 *   source_parts = [{text} | {text, url, key}]，分段拼回去与 source_chapter 逐字等价（构建期已断言）
 *   verification = {status: verified|pending|suspect|unverifiable, method, evidence, checked_at, checker}
 * 铁律：只有构建期真的解析到链接的段才有 url ；本组件不猜、不补、不伪造。
 * 排版：全部段落渲染成行内元素，不新增块级盒子，因此不改变既有排版。
 */
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'

interface SourcePart { text: string; url?: string; key?: string }

const props = defineProps<{ parts?: unknown; text?: string; verification?: unknown }>()
const { t } = useI18n()

const segs = computed<SourcePart[]>(() => {
  const raw = props.parts
  if (!Array.isArray(raw)) return []
  return raw.filter((s): s is SourcePart =>
    !!s && typeof s === 'object' && typeof (s as SourcePart).text === 'string')
})

const fallback = computed(() => (typeof props.text === 'string' ? props.text : ''))

const status = computed(() => {
  const v = props.verification as string | { status?: unknown } | null | undefined
  if (typeof v === 'string') return v
  return v && typeof v === 'object' && typeof v.status === 'string' ? v.status : ''
})

const badge = computed(() => {
  if (status.value === 'verified') return t('已核验', 'Verified')
  if (status.value === 'suspect') return t('存疑', 'Suspect')
  if (status.value === 'unverifiable') return t('一手材料', 'Primary source')
  if (status.value === 'pending') return t('待核验', 'Pending')
  return ''
})
</script>

<template>
  <span><template v-for="(p, i) in segs" :key="i"><a v-if="p.url" :href="p.url" target="_blank" rel="noopener noreferrer" class="text-gold-300/90 underline decoration-gold-500/40 underline-offset-2 hover:text-gold-200">{{ p.text }}</a><template v-else>{{ p.text }}</template></template><template v-if="!segs.length">{{ fallback }}</template></span>
  <span v-if="badge" class="ml-2 shrink-0" :class="status === 'verified' ? 'pt-chip-jade' : 'pt-chip-mute'">{{ badge }}</span>
</template>
