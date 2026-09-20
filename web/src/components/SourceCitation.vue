<script setup lang="ts">
/**
 * 出处渲染（Phase38-Y2）：有构建期注入的 source_parts 就按段渲染 —— 可点段给 <a target="_blank"> ，
 * 其余保持纯文本；没有 source_parts（旧分片 / 未注入）就退回纯文本 text 。
 *
 * 数据契约见 tools/export_static_site.py 的 inject_citation_links() ：
 *   source_parts = [{text} | {text, url, key}]，分段拼回去与 source_chapter 逐字等价（构建期已断言）
 * 铁律：只有构建期真的解析到链接的段才有 url ；本组件不猜、不补、不伪造。
 * 排版：全部段落渲染成行内元素，不新增块级盒子，因此不改变既有排版。
 *
 * Phase38-Y3：**核验状态徽章已从这里移出**，改由调用方在模式卡层级渲染 CredibilityBadge
 * —— 一条模式只显示一个徽章，且「出处为空」的模式也能显示状态。本组件因此是纯出处渲染器，
 * 不再接收 verification 字段。
 */
import { computed } from 'vue'

interface SourcePart { text: string; url?: string; key?: string }

const props = defineProps<{ parts?: unknown; text?: string }>()
const segs = computed<SourcePart[]>(() => {
  const raw = props.parts
  if (!Array.isArray(raw)) return []
  return raw.filter((s): s is SourcePart =>
    !!s && typeof s === 'object' && typeof (s as SourcePart).text === 'string')
})

const fallback = computed(() => (typeof props.text === 'string' ? props.text : ''))
</script>

<template>
  <span><template v-for="(p, i) in segs" :key="i"><a v-if="p.url" :href="p.url" target="_blank" rel="noopener noreferrer" class="text-gold-300/90 underline decoration-gold-500/40 underline-offset-2 hover:text-gold-200">{{ p.text }}</a><template v-else>{{ p.text }}</template></template><template v-if="!segs.length">{{ fallback }}</template></span>
</template>
