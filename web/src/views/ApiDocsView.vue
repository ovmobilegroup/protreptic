<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from '../composables/useI18n'

const { t, locale } = useI18n()

const endpointList = [
  { method: 'GET', path: '/api/v1/scenarios', desc: { zh: '获取所有场景（分页/筛选/搜索）', en: 'List all scenarios (pagination/filter/search)' } },
  { method: 'GET', path: '/api/v1/scenarios/{code}', desc: { zh: '获取单个场景详情', en: 'Get single scenario detail' } },
  { method: 'GET', path: '/api/v1/scenarios/search', desc: { zh: '关键词搜索场景', en: 'Search scenarios by keyword' } },
  { method: 'GET', path: '/api/v1/scenarios/filter', desc: { zh: '标签筛选场景', en: 'Filter scenarios by tags' } },
  { method: 'GET', path: '/api/v1/modes', desc: { zh: '获取所有思维模式', en: 'List all thinking modes' } },
  { method: 'GET', path: '/api/v1/modes/{id}', desc: { zh: '获取单个思维模式详情', en: 'Get single thinking mode detail' } },
  { method: 'GET', path: '/api/v1/tags/stats', desc: { zh: '获取标签统计', en: 'Get tag statistics' } },
  { method: 'GET', path: '/api/v1/tags/values', desc: { zh: '获取可用标签值', en: 'Get available tag values' } },
  { method: 'GET', path: '/api/v1/export', desc: { zh: '导出数据 (JSON/Markdown)', en: 'Export data (JSON/Markdown)' } },
  { method: 'GET', path: '/api/v1/health', desc: { zh: '健康检查', en: 'Health check' } },
]

const methodColors: Record<string, string> = {
  GET: 'bg-green-100 text-green-700',
  POST: 'bg-blue-100 text-blue-700',
  PUT: 'bg-yellow-100 text-yellow-700',
  DELETE: 'bg-red-100 text-red-700',
  PATCH: 'bg-purple-100 text-purple-700',
}

const copyEndpoint = (path: string) => {
  navigator.clipboard.writeText(`http://localhost:8000${path}`)
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <h1 class="text-3xl font-bold text-gray-900">{{ t('API 文档', 'API Documentation') }}</h1>
        <p class="mt-1 text-gray-600">{{ t('Protreptic REST API v2.1.0 - 历史人物思维模式库接口', 'Protreptic REST API v2.1.0 - Historical Figures Thinking Modes Library API') }}</p>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8 bg-white rounded-xl border border-gray-200 p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">{{ t('基础信息', 'Base Information') }}</h2>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div class="bg-gray-50 rounded-lg p-4">
            <h3 class="font-medium text-gray-900 mb-2">{{ t('基础 URL', 'Base URL') }}</h3>
            <code class="text-sm bg-white px-3 py-2 rounded block">http://localhost:8000/api/v1</code>
          </div>
          <div class="bg-gray-50 rounded-lg p-4">
            <h3 class="font-medium text-gray-900 mb-2">{{ t('格式', 'Format') }}</h3>
            <p class="text-sm text-gray-600">JSON</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-4">
            <h3 class="font-medium text-gray-900 mb-2">{{ t('认证', 'Authentication') }}</h3>
            <p class="text-sm text-gray-600">{{ t('无需认证 (公开 API)', 'No auth required (public API)') }}</p>
          </div>
        </div>

        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="font-medium text-gray-900 mb-2">{{ t('交互式文档', 'Interactive Docs') }}</h3>
          <div class="flex gap-4">
            <a href="http://localhost:8000/docs" target="_blank" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
              Swagger UI
            </a>
            <a href="http://localhost:8000/redoc" target="_blank" class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors">
              ReDoc
            </a>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ t('方法', 'Method') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ t('路径', 'Path') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ t('描述', 'Description') }}</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">{{ t('操作', 'Action') }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="endpoint in endpointList" :key="endpoint.path">
                <td class="px-6 py-4">
                  <span :class="methodColors[endpoint.method]" class="px-2 py-0.5 text-xs font-medium rounded-full">
                    {{ endpoint.method }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <code class="text-sm font-mono text-gray-900">{{ endpoint.path }}</code>
                  <button @click="copyEndpoint(endpoint.path)" class="ml-2 text-gray-400 hover:text-indigo-600" :aria-label="t('复制路径', 'Copy path')">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 012-2h10a2 2 0 012 2v12a2 2 0 01-2 2h-2M8 5a2 2 0 00-2 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V7a2 2 0 012-2h2" />
                    </svg>
                  </button>
                </td>
                <td class="px-6 py-4">
                  <p class="text-sm text-gray-700">{{ endpoint.desc[locale] }}</p>
                </td>
                <td class="px-6 py-4 text-right">
                  <a :href="`http://localhost:8000${endpoint.path}`" target="_blank" class="text-sm text-indigo-600 hover:text-indigo-900">
                    {{ t('测试', 'Try') }}
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
table {
  border-collapse: collapse;
}
tr:hover {
  background-color: #f9fafb;
}
code {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 4px;
}
</style>