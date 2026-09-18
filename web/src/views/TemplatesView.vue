<script setup lang="ts">
import { useI18n } from '../composables/useI18n'

const { t, locale } = useI18n()

const templateList = [
  { id: 'longzhong', title: { zh: '隆中对复盘', en: 'Longzhong Plan Review' }, figure: '诸葛亮', tags: ['战略规划', '创业定位', '年度规划'] },
  { id: 'baidi', title: { zh: '白帝托孤离职', en: 'Baidi Tuogu Succession' }, figure: '刘备', tags: ['CEO 交接', '核心人才离职', '继任规划'] },
  { id: 'chibi', title: { zh: '赤壁之战复盘', en: 'Battle of Red Cliffs Review' }, figure: '孙刘联盟', tags: ['联盟合作', '以弱胜强', '非对称竞争'] },
  { id: 'beifa', title: { zh: '北伐复盘', en: 'Northern Expeditions Review' }, figure: '诸葛亮', tags: ['长期项目', '技术攻关', '多阶段推进'] },
  { id: 'jieting', title: { zh: '街亭之战复盘', en: 'Battle of Jieting Review' }, figure: '马谡', tags: ['授权失败', '执行偏离', '问责闭环'] },
  { id: 'yiling', title: { zh: '夷陵之战复盘', en: 'Battle of Yiling Review' }, figure: '刘备', tags: ['情绪化决策', '战略失焦', '治理升级'] },
  { id: 'changban', title: { zh: '长坂坡复盘', en: 'Battle of Changban Review' }, figure: '赵云', tags: ['极限生存', '核心资产护送', '承诺锚定'] },
]

const openTemplate = (id: string) => {
  window.open(`${import.meta.env.BASE_URL}templates/${id}.md`, '_blank', 'noopener')
}
</script>

<template>
  <div class="pt-container pb-16 pt-10">
    <section class="mb-10">
      <div class="mb-3 flex items-center gap-3">
        <span class="pt-hairline w-10"></span>
        <span class="pt-code">{{ t('复盘模板 · 历史案例 → 现代工具', 'REVIEW TEMPLATES · HISTORY → PRACTICE') }}</span>
      </div>
      <h1 class="pt-h1"><span class="pt-gradient-text">{{ t('复盘模板库', 'Review Templates') }}</span></h1>
      <p class="mt-4 max-w-2xl text-base leading-relaxed text-parchment/55">
        {{ t(
          '7 个核心复盘模板，把历史经典案例转化为可直接套用的现代实战工具。',
          'Seven core review templates that turn classic historical cases into ready-to-use modern tools.'
        ) }}
      </p>
    </section>

    <div class="pt-stagger grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <article
        v-for="item in templateList" :key="item.id"
        @click="openTemplate(item.id)"
        tabindex="0"
        @keydown.enter="openTemplate(item.id)"
        class="group relative flex cursor-pointer flex-col overflow-hidden rounded-2xl border border-white/10
               bg-white/[.03] p-6 transition-all duration-500 ease-silk
               hover:-translate-y-1 hover:border-gold-500/45 hover:bg-white/[.055] hover:shadow-glow"
      >
        <div aria-hidden="true"
             class="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100"
             style="background: radial-gradient(420px 180px at 50% 0%, rgba(212,162,76,.14), transparent 70%)"></div>

        <div class="relative mb-4 flex items-center justify-between">
          <span class="pt-code">{{ item.id.toUpperCase() }}</span>
          <span class="text-2xl opacity-70 transition-transform duration-500 ease-silk group-hover:scale-110">🗂️</span>
        </div>

        <h3 class="relative font-display text-xl font-bold text-parchment transition-colors group-hover:text-gold-200">
          {{ locale === 'zh' ? item.title.zh : item.title.en }}
        </h3>

        <p class="relative mt-2 text-sm text-parchment/50">
          {{ t('关联人物', 'Figure') }} · <span class="text-gold-300/85">{{ item.figure }}</span>
        </p>

        <div class="relative mt-4 flex flex-wrap gap-1.5">
          <span v-for="tag in item.tags" :key="tag" class="pt-chip-mute">{{ tag }}</span>
        </div>

        <div class="relative mt-5 flex items-center gap-1 border-t border-white/[0.08] pt-4 text-xs font-medium
                    text-gold-400/0 transition-all duration-300 group-hover:text-gold-300">
          {{ t('查看模板', 'Open template') }}
          <svg class="h-3.5 w-3.5 transition-transform duration-300 group-hover:translate-x-0.5"
               fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </article>
    </div>
  </div>
</template>
