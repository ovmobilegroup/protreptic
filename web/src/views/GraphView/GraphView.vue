<script setup lang="ts">
/**
 * /graph 关系图谱（Phase30-B2）。
 *
 * 三个视图全部读 B1 的预计算分片，渲染用纯 SVG（无第三方图库，无 canvas）：
 *   1) 人物-模式-概念：所选人物的模式（modes/by-figure/{code}.json 的真实 key_concepts）
 *      + 概念节点，构成三分图；点到概念跳 /concepts。
 *   2) 模式关联：mode_edges.json 的一跳邻域（related_modes 去重无向边），虚线为
 *      similar_modes.json 的共现邻居（非向量语义相似度）。
 *   3) 全局模式网络：按度数取前 K 条模式，只画它们之间的边。
 *
 * 布局是本地实现的 Fruchterman-Reingold 弹簧模型（固定种子，结果可复现），不引入 d3/sigma。
 * 节点数上限 80：力导向是 O(n²)/轮，超过后交互会掉帧，故做硬上限并在 UI 里写清楚。
 */
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  adjacencyFromEdges,
  degreeOf,
  loadConceptGraph,
  loadModeGraph,
  loadSimilarModes,
  type ConceptGraphPayload,
  type ModeGraphPayload,
  type SimilarModesPayload,
} from '../../api/graphData'
import { loadModeIndex, type ModeIndexEntry } from '../../api/modeIndex'
import { fetchFigureModes, fetchUnifiedIndex, type UnifiedEntry } from '../../api/static'
import { useI18n } from '../../composables/useI18n'

type Kind = 'figure' | 'mode' | 'concept'
type ViewKey = 'figure' | 'mode' | 'global'

interface GNode { id: string; label: string; sub: string; kind: Kind; x: number; y: number; r: number; href?: string; query?: Record<string, string> }
interface GLink { a: number; b: number; similar?: boolean }

const W = 900
const H = 620
const MAX_NODES = 80

const router = useRouter()
const { t, locale } = useI18n()

const conceptGraph = ref<ConceptGraphPayload | null>(null)
const modeGraph = ref<ModeGraphPayload | null>(null)
const similar = ref<SimilarModesPayload | null>(null)
const modeIndex = ref<ModeIndexEntry[]>([])
const figureMeta = ref<Map<string, UnifiedEntry>>(new Map())

const state = ref<'loading' | 'ready' | 'unavailable'>('loading')
const view = ref<ViewKey>('figure')
const figureCode = ref('H-WYM-001')
const modeCode = ref('')
const conceptLimit = ref(12)
const topK = ref(60)

const nodes = ref<GNode[]>([])
const links = ref<GLink[]>([])
const figureShard = ref<any>(null)

const figureOptions = computed(() =>
  Array.from(figureMeta.value.values())
    .slice()
    .sort((a, b) => (b.n_modes || 0) - (a.n_modes || 0) || a.code.localeCompare(b.code))
)
const modeOptions = computed(() =>
  modeIndex.value.slice().sort((a, b) => a.modeCode.localeCompare(b.modeCode))
)

const modeLabel = (code: string) => {
  const hit = modeIndex.value.find((m) => m.modeCode === code)
  if (!hit) return code
  return locale.value === 'zh' ? hit.nameZh : (hit.nameEn || hit.nameZh)
}
const modeFigure = (code: string) => modeIndex.value.find((m) => m.modeCode === code)?.figureCode || ''

/* ---------- 本地力导向布局（固定种子，可复现） ---------- */
const mulberry32 = (seed: number) => () => {
  seed = (seed + 0x6d2b79f5) | 0
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296
}

const hashSeed = (s: string) => {
  let h = 2166136261
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) }
  return h >>> 0
}

const runLayout = (seedKey: string) => {
  const ns = nodes.value
  const ls = links.value
  if (!ns.length) return
  const rnd = mulberry32(hashSeed(seedKey))
  const cx = W / 2
  const cy = H / 2
  ns.forEach((n, i) => {
    const angle = (i / ns.length) * Math.PI * 2 + rnd() * 0.4
    const radius = Math.min(W, H) * (0.18 + rnd() * 0.22)
    n.x = cx + Math.cos(angle) * radius
    n.y = cy + Math.sin(angle) * radius * 0.85
  })
  const k = Math.sqrt((W * H) / ns.length) * 0.62
  const iterations = ns.length > 40 ? 220 : 300
  for (let it = 0; it < iterations; it++) {
    const cool = 1 - it / iterations
    const dx = new Array<number>(ns.length).fill(0)
    const dy = new Array<number>(ns.length).fill(0)
    for (let i = 0; i < ns.length; i++) {
      for (let j = i + 1; j < ns.length; j++) {
        let vx = ns[i].x - ns[j].x
        let vy = ns[i].y - ns[j].y
        let d = Math.hypot(vx, vy)
        if (d < 0.01) { vx = 0.01; vy = 0.01; d = 0.014 }
        const rep = ((k * k) / d) * 0.05
        dx[i] += (vx / d) * rep; dy[i] += (vy / d) * rep
        dx[j] -= (vx / d) * rep; dy[j] -= (vy / d) * rep
      }
    }
    for (const l of ls) {
      const a = ns[l.a]
      const b = ns[l.b]
      if (!a || !b) continue
      const vx = b.x - a.x
      const vy = b.y - a.y
      const d = Math.hypot(vx, vy) || 0.01
      const att = (d * d) / k * 0.012
      dx[l.a] += (vx / d) * att; dy[l.a] += (vy / d) * att
      dx[l.b] -= (vx / d) * att; dy[l.b] -= (vy / d) * att
    }
    for (let i = 0; i < ns.length; i++) {
      const d = Math.hypot(dx[i], dy[i]) || 1
      const step = Math.min(d, k * 0.16 * (0.35 + cool))
      ns[i].x += (dx[i] / d) * step
      ns[i].y += (dy[i] / d) * step
      ns[i].x = Math.max(46, Math.min(W - 46, ns[i].x))
      ns[i].y = Math.max(34, Math.min(H - 26, ns[i].y))
    }
  }
}

const buildFigureView = async () => {
  const cg = conceptGraph.value
  if (!cg) return
  const shard = await fetchFigureModes(figureCode.value)
  figureShard.value = shard
  const codes: string[] = []
  const conceptSpread = new Map<string, number>()
  for (const [, concept] of cg.edges) conceptSpread.set(concept, (conceptSpread.get(concept) || 0) + 1)

  const meta = figureMeta.value.get(figureCode.value)
  const ns: GNode[] = [{
    id: figureCode.value,
    label: meta?.name || figureCode.value,
    sub: meta?.era || '',
    kind: 'figure',
    x: 0, y: 0, r: 15,
    href: `/minds/${figureCode.value}`,
  }]
  const seenConcept = new Set<string>()
  for (const m of (shard?.modes || [])) {
    if (!m.mode_code) continue
    codes.push(m.mode_code)
    const mi = ns.length
    ns.push({
      id: m.mode_code,
      label: locale.value === 'zh' ? pick(m.name_zh) : (pick(m.name_en) || pick(m.name_zh)),
      sub: m.mode_code,
      kind: 'mode',
      x: 0, y: 0, r: 8,
      href: `/minds/${figureCode.value}`,
    })
    const concepts: string[] = Array.isArray(m.key_concepts) ? m.key_concepts : []
    for (const c of concepts) {
      if (!seenConcept.has(c)) {
        seenConcept.add(c)
        ns.push({ id: `c:${c}`, label: c, sub: '', kind: 'concept', x: 0, y: 0, r: 6 })
      }
      const ci = ns.findIndex((n) => n.id === `c:${c}`)
      links.value.push({ a: mi, b: ci })
    }
    links.value.push({ a: 0, b: mi })
  }
  // 概念节点按全局共享度排序，只保留前 N 个（模式节点与其连边同步裁掉孤儿）
  const conceptIdx = ns.map((n, i) => ({ n, i })).filter((x) => x.n.kind === 'concept')
  conceptIdx.sort((a, b) => (conceptSpread.get(b.n.label) || 0) - (conceptSpread.get(a.n.label) || 0))
  const keep = new Set(conceptIdx.slice(0, conceptLimit.value).map((x) => x.i))
  const keptNodes: GNode[] = []
  const remap = new Map<number, number>()
  ns.forEach((n, i) => {
    if (n.kind === 'concept' && !keep.has(i)) return
    remap.set(i, keptNodes.length)
    keptNodes.push(n)
  })
  const keptLinks: GLink[] = []
  for (const l of links.value) {
    const a = remap.get(l.a)
    const b = remap.get(l.b)
    if (a === undefined || b === undefined) continue
    keptLinks.push({ a, b })
  }
  nodes.value = keptNodes.slice(0, MAX_NODES)
  links.value = keptLinks.filter((l) => l.a < nodes.value.length && l.b < nodes.value.length)
  runLayout(`figure:${figureCode.value}:${conceptLimit.value}:${locale.value}`)
}

const pick = (v: any): string => (Array.isArray(v) ? (v[0] ?? '') : (v ?? ''))

const buildModeView = () => {
  const mg = modeGraph.value
  if (!mg) return
  const adj = adjacencyFromEdges(mg.edges)
  const center = modeCode.value || Array.from(degreeOf(adj)).sort((a, b) => b[1] - a[1])[0]?.[0] || ''
  modeCode.value = center
  const adjacent = (adj.get(center) || []).slice(0, 24)
  const neighbour = adjacent.slice()
  // 预计算的相似邻居里大多数（1018 条中 778 条）不在 related_modes 邻接表里，
  // 只当边画会被静默丢掉，所以这里把它们补成节点（合计上限 25 + 中心）。
  for (const sim of (similar.value?.modes?.[center] || [])) {
    if (sim.modeCode && sim.modeCode !== center && !neighbour.includes(sim.modeCode) && neighbour.length < 25) {
      neighbour.push(sim.modeCode)
    }
  }
  const ids = [center, ...neighbour]
  const idx = new Map(ids.map((id, i) => [id, i]))
  nodes.value = ids.map((id, i) => ({
    id,
    label: modeLabel(id),
    sub: id,
    kind: 'mode' as Kind,
    x: 0, y: 0, r: i === 0 ? 15 : 8,
    href: modeFigure(id) ? `/minds/${modeFigure(id)}` : undefined,
  }))
  const ls: GLink[] = []
  for (const id of adjacent) {
    const a = idx.get(center)
    const b = idx.get(id)
    if (a !== undefined && b !== undefined) ls.push({ a, b })
  }
  const sims = similar.value?.modes?.[center] || []
  for (const s of sims) {
    const b = idx.get(s.modeCode)
    const a = idx.get(center)
    if (a !== undefined && b !== undefined) ls.push({ a, b, similar: true })
  }
  links.value = ls
  nodes.value = nodes.value.slice(0, MAX_NODES)
  runLayout(`mode:${center}`)
}

const buildGlobalView = () => {
  const mg = modeGraph.value
  if (!mg) return
  const adj = adjacencyFromEdges(mg.edges)
  const top = Array.from(degreeOf(adj)).sort((a, b) => b[1] - a[1]).slice(0, Math.min(topK.value, MAX_NODES))
  const idx = new Map(top.map(([id], i) => [id, i]))
  const deg = new Map(top)
  nodes.value = top.map(([id], i) => ({
    id,
    label: modeLabel(id),
    sub: id,
    kind: 'mode' as Kind,
    x: 0, y: 0,
    r: 6 + Math.min(8, Math.round((deg.get(id) || 1) / 3)),
    href: modeFigure(id) ? `/minds/${modeFigure(id)}` : undefined,
  }))
  const ls: GLink[] = []
  for (const [a, b] of mg.edges) {
    const ia = idx.get(a)
    const ib = idx.get(b)
    if (ia !== undefined && ib !== undefined) ls.push({ a: ia, b: ib })
  }
  links.value = ls
  runLayout(`global:${topK.value}`)
}

const rebuild = async () => {
  links.value = []
  nodes.value = []
  if (view.value === 'figure') await buildFigureView()
  else if (view.value === 'mode') buildModeView()
  else buildGlobalView()
}

const onNodeClick = (n: GNode) => {
  if (n.kind === 'concept') {
    router.push({ name: 'concepts', query: { c: n.label } })
    return
  }
  if (n.href) router.push(n.href)
}

const load = async () => {
  const [cg, mg, sm, idx, unified] = await Promise.all([
    loadConceptGraph(),
    loadModeGraph(),
    loadSimilarModes(),
    loadModeIndex().catch(() => [] as ModeIndexEntry[]),
    fetchUnifiedIndex(),
  ])
  if (!mg || !cg) { state.value = 'unavailable'; return }
  conceptGraph.value = cg
  modeGraph.value = mg
  similar.value = sm
  modeIndex.value = idx
  figureMeta.value = new Map((unified?.items || []).filter((i) => i.type === 'figure').map((i) => [i.code, i]))
  if (!figureMeta.value.has(figureCode.value)) {
    figureCode.value = figureOptions.value[0]?.code || figureCode.value
  }
  state.value = 'ready'
  await rebuild()
}

watch(view, () => { void rebuild() })
watch(conceptLimit, () => { if (view.value === 'figure') void rebuild() })
watch(topK, () => { if (view.value === 'global') void rebuild() })
watch(figureCode, () => { if (view.value === 'figure') void rebuild() })
watch(modeCode, () => { if (view.value === 'mode') void rebuild() })
watch(locale, () => { void rebuild() })
onMounted(load)

const svgEdges = computed(() => links.value.map((l) => ({
  similar: !!l.similar,
  x1: nodes.value[l.a]?.x ?? 0, y1: nodes.value[l.a]?.y ?? 0,
  x2: nodes.value[l.b]?.x ?? 0, y2: nodes.value[l.b]?.y ?? 0,
})))

const kindFill = (kind: Kind) => (kind === 'figure' ? 'rgb(var(--pt-jade-400))' : kind === 'mode' ? 'rgb(var(--pt-gold-400))' : 'rgb(var(--pt-overlay))')
</script>

<template>
  <div class="pt-container pb-20 pt-10">
    <section class="mb-8">
      <div class="mb-3 flex flex-wrap items-center gap-3">
        <span class="pt-hairline w-10"></span>
        <span class="pt-code">{{ t('关系图谱 · 人物-模式-概念', 'RELATION GRAPH · FIGURE-MODE-CONCEPT') }}</span>
      </div>
      <h1 class="pt-h1 !text-4xl">{{ t('关系图谱', 'Relation graph') }}</h1>
      <p class="pt-prose mt-3 max-w-3xl">
        用本地计算的力导向布局展示人物、模式、概念之间的真实关联（数据来自 B1 预计算分片，无第三方图库）。
        点节点可跳到对应人物档案或概念用法。
      </p>
    </section>

    <div v-if="state === 'loading'" class="pt-skeleton h-96"></div>

    <div v-else-if="state === 'unavailable'" class="pt-panel px-6 py-10 text-center">
      <p class="text-parchment/70">{{ t('图谱数据不可用', 'Graph data unavailable') }}</p>
      <p class="mt-2 font-mono text-xs text-parchment/40">data/graph/mode_edges.json · concept_graph.json</p>
    </div>

    <template v-else>
      <div class="mb-4 flex flex-wrap gap-2">
        <button type="button" :class="view === 'figure' ? 'pt-btn-gold' : 'pt-btn-ghost'" @click="view = 'figure'">
          {{ t('人物-模式-概念', 'Figure-Mode-Concept') }}
        </button>
        <button type="button" :class="view === 'mode' ? 'pt-btn-gold' : 'pt-btn-ghost'" @click="view = 'mode'">
          {{ t('模式关联', 'Mode relations') }}
        </button>
        <button type="button" :class="view === 'global' ? 'pt-btn-gold' : 'pt-btn-ghost'" @click="view = 'global'">
          {{ t('全局模式网络', 'Global mode network') }}
        </button>
      </div>

      <div class="pt-panel mb-4 flex flex-wrap items-end gap-4 p-4">
        <label v-if="view === 'figure'" class="flex min-w-0 flex-col gap-1 text-xs text-parchment/50">
          {{ t('人物', 'Figure') }}
          <select v-model="figureCode" class="pt-input max-w-full">
            <option v-for="f in figureOptions" :key="f.code" :value="f.code">{{ f.name || f.code }}（{{ f.n_modes || 0 }}）</option>
          </select>
        </label>

        <label v-if="view === 'figure'" class="flex flex-col gap-1 text-xs text-parchment/50">
          {{ t('概念节点上限', 'Concept nodes') }}
          <select v-model.number="conceptLimit" class="pt-input">
            <option :value="6">6</option>
            <option :value="12">12</option>
            <option :value="18">18</option>
            <option :value="24">24</option>
          </select>
        </label>

        <label v-if="view === 'mode'" class="flex min-w-0 flex-col gap-1 text-xs text-parchment/50">
          {{ t('中心模式', 'Center mode') }}
          <select v-model="modeCode" class="pt-input max-w-full">
            <option v-for="m in modeOptions" :key="m.modeCode" :value="m.modeCode">{{ m.modeCode }} · {{ m.nameZh }}</option>
          </select>
        </label>

        <label v-if="view === 'global'" class="flex flex-col gap-1 text-xs text-parchment/50">
          {{ t('节点数（按度数取前 K）', 'Top-K nodes') }}
          <select v-model.number="topK" class="pt-input">
            <option :value="20">20</option>
            <option :value="40">40</option>
            <option :value="60">60</option>
            <option :value="80">80</option>
          </select>
        </label>

        <div class="ml-auto flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-parchment/55">
          <span data-graph-stat>{{ t('节点', 'Nodes') }} <b class="text-parchment">{{ nodes.length }}</b></span>
          <span data-graph-stat>{{ t('边', 'Edges') }} <b class="text-parchment">{{ links.length }}</b></span>
          <span class="pt-chip-mute">{{ t('本地力导向布局', 'Local force layout') }}</span>
        </div>
      </div>

      <div class="pt-panel w-full max-w-full overflow-hidden p-2 sm:p-4">
        <svg
          :viewBox="`0 0 ${W} ${H}`"
          preserveAspectRatio="xMidYMid meet"
          class="block h-auto w-full"
          data-graph-svg
          role="img"
          :aria-label="t('人物-模式-概念关系图谱', 'Figure-mode-concept relation graph')"
        >
          <g>
            <line
              v-for="(e, i) in svgEdges" :key="`e${i}`"
              :x1="e.x1" :y1="e.y1" :x2="e.x2" :y2="e.y2"
              :stroke="e.similar ? 'rgb(var(--pt-gold-400) / 0.35)' : 'rgb(var(--pt-jade-400) / 0.22)'"
              :stroke-width="e.similar ? 1 : 1.2"
              :stroke-dasharray="e.similar ? '4 3' : undefined"
            />
          </g>
          <g>
            <g
              v-for="n in nodes" :key="n.id"
              data-graph-node
              :class="n.href || n.kind === 'concept' ? 'cursor-pointer' : 'cursor-default'"
              @click="onNodeClick(n)"
            >
              <title>{{ n.label }}{{ n.sub && n.sub !== n.label ? ` · ${n.sub}` : '' }}</title>
              <circle
                :cx="n.x" :cy="n.y" :r="n.r"
                :fill="kindFill(n.kind)"
                :fill-opacity="n.kind === 'concept' ? 0.25 : 0.9"
                :stroke="n.kind === 'concept' ? 'rgb(var(--pt-gold-400) / 0.55)' : 'rgb(var(--pt-ink-950) / 0.6)'"
                stroke-width="1.5"
              />
              <text
                :x="n.x" :y="n.y + n.r + 12"
                text-anchor="middle"
                class="fill-parchment/75"
                style="font-size: 11px"
              >{{ n.label.length > 12 ? `${n.label.slice(0, 12)}…` : n.label }}</text>
            </g>
          </g>
        </svg>
      </div>

      <div class="mt-4 flex flex-wrap items-center gap-x-6 gap-y-2 text-xs text-parchment/55">
        <span class="flex items-center gap-2"><span class="h-3 w-3 rounded-full bg-jade-400"></span>{{ t('人物', 'Figure') }}</span>
        <span class="flex items-center gap-2"><span class="h-3 w-3 rounded-full bg-gold-400"></span>{{ t('模式', 'Mode') }}</span>
        <span class="flex items-center gap-2"><span class="h-3 w-3 rounded-full border border-gold-400/60 bg-white/20"></span>{{ t('概念', 'Concept') }}</span>
        <span class="flex items-center gap-2"><span class="h-0.5 w-6 bg-jade-400/40"></span>{{ t('关联边', 'Relation') }}</span>
        <span class="flex items-center gap-2"><span class="h-0.5 w-6 border-t border-dashed border-gold-400/60"></span>{{ t('相似模式边（概念交集预计算）', 'Similar edge (concept overlap)') }}</span>
      </div>
    </template>
  </div>
</template>
