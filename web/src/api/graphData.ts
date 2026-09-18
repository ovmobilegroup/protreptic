/**
 * B1 关系图谱数据加载器（产物见 tools/build_graph_data.py，落在 web/public/data/graph/）。
 *
 * 三个文件都是全量图谱，模块级缓存一次；同一会话内切换 /graph 的视图不会重复下载。
 * 真实口径（B1 实测，见 web/public/data/graph/meta.json）：
 *   mode_edges     3298 节点 / 6684 边（related_modes 双向去重后的无向边）
 *   concept_graph  284 人物 / 13288 概念 / 13552 边（figure_code ↔ key_concepts）
 *   similar_modes  2858 条模式中 599 条有预计算邻居，共 1018 条 Top-10 邻居
 *
 * 措辞纪律：similar_modes 是「key_concepts 交集 + 同域加分」的共现打分，
 * 不是向量语义相似度；UI 文案不得写成「语义相似」。
 */
const DATA_ROOT = `${import.meta.env.BASE_URL || '/'}data/`

export interface SimilarModeEntry {
  /** 邻居模式编号（与 modes/index-*.json 同一命名空间，形如 M-AE-009） */
  modeCode: string
  score: number
  /** 与源模式共享的 key_concepts，长度 1~5（B1 实测最多 5） */
  sharedConcepts: string[]
  sameDomain: boolean
}

export interface SimilarModesPayload {
  topN: number
  modes: Record<string, SimilarModeEntry[]>
  stats: { n_modes: number; total_neighbors: number }
}

/** 磁盘格式（snake_case，见 tools/build_graph_data.py）——只在加载器内部可见 */
interface RawSimilarModesPayload {
  top_n?: number
  modes?: Record<string, Array<{ mode_code?: string; score?: number; shared_concepts?: string[]; same_domain?: boolean }>>
  stats?: { n_modes?: number; total_neighbors?: number }
}

export interface ModeGraphPayload {
  nodes: string[]
  edges: [string, string][]
  stats: { n_nodes: number; n_edges: number }
}

export interface ConceptGraphPayload {
  /** 磁盘字段名（snake_case）与 build_graph_data.py 产物一致，不做重命名以免两处漂移 */
  figure_nodes: string[]
  concept_nodes: string[]
  edges: [string, string][]
  stats: { n_figures: number; n_concepts: number; n_edges: number }
}

const loadJson = async <T>(file: string): Promise<T | null> => {
  try {
    const res = await fetch(`${DATA_ROOT}graph/${file}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return (await res.json()) as T
  } catch (err) {
    console.warn(`[graph] ${file} 加载失败`, err)
    return null
  }
}

const cache = new Map<string, Promise<any>>()

const cached = <T>(file: string): Promise<T | null> => {
  if (!cache.has(file)) {
    const p = loadJson<T>(file)
    p.catch(() => cache.delete(file))
    cache.set(file, p)
  }
  return cache.get(file) as Promise<T | null>
}

/**
 * 模式 → Top-N 相似模式（预计算，见 B1）。失败返回 null，调用方必须显示降级提示。
 *
 * 磁盘里是 snake_case（mode_code / shared_concepts / same_domain），这里统一归一成 camelCase；
 * 组件若直接吃原始 JSON，`sharedConcepts.slice()` 会在渲染期抛错，Vue 会把整块渲染成空注释
 * （症状：只有「有邻居」的模式区块凭空消失）——所以归一必须发生在这一层。
 */
export const loadSimilarModes = async (): Promise<SimilarModesPayload | null> => {
  const raw = await cached<RawSimilarModesPayload>('similar_modes.json')
  if (!raw) return null
  const modes: Record<string, SimilarModeEntry[]> = {}
  for (const [code, list] of Object.entries(raw.modes || {})) {
    modes[code] = (Array.isArray(list) ? list : []).map((e) => ({
      modeCode: String(e?.mode_code ?? ''),
      score: Number(e?.score ?? 0),
      sharedConcepts: Array.isArray(e?.shared_concepts) ? e.shared_concepts.map(String) : [],
      sameDomain: !!e?.same_domain,
    }))
  }
  return {
    topN: Number(raw.top_n ?? 0),
    modes,
    stats: {
      n_modes: Number(raw.stats?.n_modes ?? 0),
      total_neighbors: Number(raw.stats?.total_neighbors ?? 0),
    },
  }
}

/** 模式-模式关联边（related_modes 口径）。 */
export const loadModeGraph = (): Promise<ModeGraphPayload | null> =>
  cached<ModeGraphPayload>('mode_edges.json')

/** 人物-概念二分图。1.09 MB 原始 / 456 KB gzip，只在 /graph、/concepts 两个页面按需加载。 */
export const loadConceptGraph = (): Promise<ConceptGraphPayload | null> =>
  cached<ConceptGraphPayload>('concept_graph.json')

/** 无向邻接表。B1 的边已双向去重，这里对两边都登记，便于从任意节点展开 ego 网络。 */
export const adjacencyFromEdges = (edges: [string, string][]): Map<string, string[]> => {
  const adj = new Map<string, string[]>()
  const push = (a: string, b: string) => {
    const list = adj.get(a)
    if (list) list.push(b)
    else adj.set(a, [b])
  }
  for (const [a, b] of edges) {
    if (!a || !b || a === b) continue
    push(a, b)
    push(b, a)
  }
  return adj
}

export interface ConceptUsage {
  concept: string
  /** 使用该概念的人物 code，按 code 排序（跨人物用法 = 多个人物共享同一概念） */
  figures: string[]
}

/** 人物-概念边聚合成「概念 → 人物列表」，按人物数倒序（B1 实测最多 8 人共享一个概念）。 */
export const buildConceptUsage = (graph: ConceptGraphPayload): ConceptUsage[] => {
  const map = new Map<string, Set<string>>()
  for (const [figure, concept] of graph.edges) {
    if (!figure || !concept) continue
    const set = map.get(concept)
    if (set) set.add(figure)
    else map.set(concept, new Set([figure]))
  }
  return Array.from(map, ([concept, set]) => ({ concept, figures: Array.from(set).sort() }))
    .sort((a, b) => b.figures.length - a.figures.length || a.concept.localeCompare(b.concept, 'zh'))
}

/** 节点度数（用于挑默认展示的中心节点与裁剪超大图）。 */
export const degreeOf = (adj: Map<string, string[]>): Map<string, number> => {
  const deg = new Map<string, number>()
  for (const [k, v] of adj) deg.set(k, v.length)
  return deg
}
