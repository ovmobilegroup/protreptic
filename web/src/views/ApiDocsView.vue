<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from '../composables/useI18n'

const { t, locale } = useI18n()

// 静态站点实际可用的数据接口（GitHub Pages 无后端）
const staticEndpoints = [
  { path: '/data/meta.json', desc: { zh: '数据清单：条数与 sha256 校验', en: 'Manifest: counts + sha256' } },
  { path: '/data/figures.index.json', desc: { zh: '全部人物轻量索引（1057 条）', en: 'Lightweight figure index (1057)' } },
  { path: '/data/figures/{code}.json', desc: { zh: '单个人物详情分片', en: 'Single figure detail shard' } },
  { path: '/data/modes/index-{0..7}.json', desc: { zh: '思维模式摘要（8 分片，共 2848 条）', en: 'Mode summaries (8 shards, 2848 total)' } },
  { path: '/data/modes/by-figure/{code}.json', desc: { zh: '某位人物的全部模式（283 片）', en: 'All modes of one figure (283 shards)' } },
]

// 可选：本地 FastAPI 服务（仓库自带，需自行启动）
const apiEndpoints = [
  { method: 'GET', path: '/api/v1/thinking-modes', desc: { zh: '列出/筛选思维模式', en: 'List / filter thinking modes' } },
  { method: 'GET', path: '/api/v1/thinking-modes/stats', desc: { zh: '库统计', en: 'Library statistics' } },
  { method: 'GET', path: '/api/v1/thinking-modes/{mode_code}', desc: { zh: '单条模式详情', en: 'Single mode detail' } },
  { method: 'GET', path: '/api/v1/figures/{code}/modes', desc: { zh: '某位人物的全部模式', en: 'All modes of a figure' } },
]

const copied = ref('')
const copy = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    copied.value = text
    setTimeout(() => { if (copied.value === text) copied.value = '' }, 1600)
  } catch { /* 剪贴板不可用 */ }
}

const origin = typeof window !== 'undefined' ? window.location.origin : ''
const baseUrl = `${origin}${import.meta.env.BASE_URL}`

const pySnippet = `# 克隆仓库后即可查询全部 2848 条模式
python3 tools/figure_library.py --stats
python3 tools/figure_library.py -f H-INM-001     # 稻盛和夫的 10 条模式
python3 tools/figure_library.py -s 矛盾           # 关键词搜索`
</script>

<template>
  <div class="pt-container pb-16 pt-10">
    <section class="mb-10">
      <div class="mb-3 flex items-center gap-3">
        <span class="pt-hairline w-10"></span>
        <span class="pt-code">{{ t('数据接口 · 静态与本地', 'DATA ACCESS · STATIC & LOCAL') }}</span>
      </div>
      <h1 class="pt-h1"><span class="pt-gradient-text">{{ t('数据与 API', 'Data & API') }}</span></h1>
      <p class="mt-4 max-w-2xl text-base leading-relaxed text-parchment/55">
        {{ t(
          '本站为纯静态站点，所有数据以 JSON 分片形式直接可取，无需认证。若需要带筛选能力的服务端接口，可本地启动仓库自带的 FastAPI 服务。',
          'This site is fully static: all data is available as JSON shards with no auth. For a server-side API with filtering, run the bundled FastAPI service locally.'
        ) }}
      </p>
    </section>

    <!-- 基础信息 -->
    <section class="pt-panel mb-8 p-6">
      <h2 class="pt-h3 mb-4 text-gold-200">{{ t('基础信息', 'Base information') }}</h2>
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div class="rounded-xl border border-white/10 bg-ink-900/50 p-4">
          <div class="mb-2 text-xs text-parchment/45">{{ t('站点根地址', 'Site root') }}</div>
          <code class="pt-code break-all">{{ baseUrl }}</code>
        </div>
        <div class="rounded-xl border border-white/10 bg-ink-900/50 p-4">
          <div class="mb-2 text-xs text-parchment/45">{{ t('数据格式', 'Format') }}</div>
          <div class="text-sm text-parchment/80">JSON (UTF-8)</div>
        </div>
        <div class="rounded-xl border border-white/10 bg-ink-900/50 p-4">
          <div class="mb-2 text-xs text-parchment/45">{{ t('认证', 'Auth') }}</div>
          <div class="text-sm text-parchment/80">{{ t('无需认证', 'None') }}</div>
        </div>
      </div>
    </section>

    <!-- 静态数据接口 -->
    <section class="pt-panel mb-8 overflow-hidden">
      <div class="flex items-center gap-3 border-b border-white/10 px-6 py-4">
        <span class="pt-chip-jade">STATIC</span>
        <h2 class="pt-h3 text-parchment/90">{{ t('静态数据接口', 'Static data endpoints') }}</h2>
      </div>
      <ul class="divide-y divide-white/[0.06]">
        <li v-for="ep in staticEndpoints" :key="ep.path"
            class="flex flex-wrap items-center gap-3 px-6 py-4 transition-colors hover:bg-white/[.03]">
          <code class="pt-code flex-1 min-w-[16rem] break-all text-gold-300/90">{{ ep.path }}</code>
          <span class="text-sm text-parchment/55">{{ ep.desc[locale] }}</span>
          <button @click="copy(baseUrl.replace(/\/$/, '') + ep.path)"
                  class="ml-auto rounded-lg border border-white/10 px-2.5 py-1 text-xs text-parchment/55
                         transition-colors hover:border-gold-500/40 hover:text-gold-300">
            {{ copied === baseUrl.replace(/\/$/, '') + ep.path ? t('已复制', 'Copied') : t('复制', 'Copy') }}
          </button>
        </li>
      </ul>
    </section>

    <!-- 本地 API -->
    <section class="pt-panel mb-8 overflow-hidden">
      <div class="flex items-center gap-3 border-b border-white/10 px-6 py-4">
        <span class="pt-chip-gold">OPTIONAL</span>
        <h2 class="pt-h3 text-parchment/90">{{ t('本地 FastAPI 服务（可选）', 'Local FastAPI service (optional)') }}</h2>
      </div>
      <div class="px-6 py-5">
        <pre class="mb-5 overflow-x-auto rounded-xl border border-white/10 bg-ink-950/70 p-4 text-xs leading-relaxed text-jade-300/90"><code>cd api
pip install -r requirements.txt
python build_figures_db.py &amp;&amp; python load_v6.py
uvicorn api.main:app --reload      # http://127.0.0.1:8000</code></pre>
        <ul class="space-y-2">
          <li v-for="ep in apiEndpoints" :key="ep.path" class="flex flex-wrap items-center gap-3">
            <span class="pt-chip-jade w-12 justify-center">{{ ep.method }}</span>
            <code class="pt-code">{{ ep.path }}</code>
            <span class="text-sm text-parchment/50">{{ ep.desc[locale] }}</span>
          </li>
        </ul>
      </div>
    </section>

    <!-- CLI -->
    <section class="pt-panel overflow-hidden">
      <div class="flex items-center gap-3 border-b border-white/10 px-6 py-4">
        <span class="pt-chip-mute">CLI</span>
        <h2 class="pt-h3 text-parchment/90">{{ t('命令行查询', 'Command-line query') }}</h2>
      </div>
      <div class="px-6 py-5">
        <pre class="overflow-x-auto rounded-xl border border-white/10 bg-ink-950/70 p-4 text-xs leading-relaxed text-parchment/80"><code>{{ pySnippet }}</code></pre>
      </div>
    </section>
  </div>
</template>
