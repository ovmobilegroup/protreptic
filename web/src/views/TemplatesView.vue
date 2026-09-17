<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from '../composables/useI18n'
import { useRouter } from 'vue-router'

const { t, locale } = useI18n()
const router = useRouter()

const templates = ref<any[]>([])
const loading = ref(false)

const templateList = [
  { id: 'longzhong', title: { zh: '隆中对复盘', en: 'Longzhong Plan Review' }, figure: 'H-ZL-08', tags: ['战略规划', '创业定位', '年度规划'] },
  { id: 'baidi', title: { zh: '白帝托孤离职', en: 'Baidi Tuogu Succession' }, figure: 'H-LB-15', tags: ['CEO交接', '核心人才离职', '继任规划'] },
  { id: 'chibi', title: { zh: '赤壁之战复盘', en: 'Battle of Red Cliffs Review' }, figure: 'H-ZY-?', tags: ['联盟合作', '以弱胜强', '非对称竞争'] },
  { id: 'beifa', title: { zh: '北伐复盘', en: 'Northern Expeditions Review' }, figure: 'H-ZL-08', tags: ['长期项目', '技术攻关', '多阶段推进'] },
  { id: 'jieting', title: { zh: '街亭之战复盘', en: 'Battle of Jieting Review' }, figure: 'H-MS-?', tags: ['授权失败', '执行偏离', '问责闭环'] },
  { id: 'yiling', title: { zh: '夷陵之战复盘', en: 'Battle of Yiling Review' }, figure: 'H-LB-15', tags: ['情绪化决策', '战略失焦', '治理升级'] },
  { id: 'changban', title: { zh: '长坂坡复盘', en: 'Battle of Changban Review' }, figure: 'H-ZY-?', tags: ['极限生存', '核心资产护送', '承诺锚定'] },
]

const navigateToTemplate = (id: string) => {
  window.open(`/templates/${id}.md`, '_blank')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <h1 class="text-3xl font-bold text-gray-900">{{ t('复盘模板库', 'Review Templates Library') }}</h1>
        <p class="mt-1 text-gray-600">{{ t('7 个核心复盘模板，将历史经典案例转化为现代实战工具', '7 core review templates transforming historical cases into modern practical tools') }}</p>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <article
          v-for="template in templateList"
          :key="template.id"
          @click="navigateToTemplate(template.id)"
          class="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg hover:border-indigo-300 transition-all duration-200 cursor-pointer"
          tabindex="0"
          @keydown.enter="navigateToTemplate(template.id)"
        >
          <div class="flex items-start justify-between mb-4">
            <span class="text-xs font-mono font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
              {{ template.id.toUpperCase() }}
            </span>
          </div>

          <h3 class="text-lg font-semibold text-gray-900 mb-2">
            {{ locale === 'zh' ? template.title.zh : template.title.en }}
          </h3>

          <p class="text-sm text-gray-600 mb-4">
            关联人物: {{ template.figure }}
          </p>

          <div class="flex flex-wrap gap-1.5 mb-4">
            <span
              v-for="tag in template.tags"
              :key="tag"
              class="px-2 py-0.5 text-xs font-medium bg-indigo-50 text-indigo-700 rounded-full"
            >
              {{ tag }}
            </span>
          </div>

          <div class="pt-4 border-t border-gray-100">
            <button class="w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors">
              {{ locale === 'zh' ? '查看模板' : 'View Template' }}
              <svg class="inline w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </article>
      </div>
    </main>
  </div>
</template>