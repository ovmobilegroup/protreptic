/**
 * 静态数据适配层（VITE_DATA_MODE=static）
 *
 * 无后端场景下从 `public/data/` 下的静态 JSON 取数（产物由 tools/export_static_site.py 生成），
 * 对外暴露两种等价接口：
 *   1) 具名函数 fetchFigures / fetchFigure / searchFigures / semanticSearch / getSimilar
 *      —— 与 stores/figures.ts 中同名方法语义一致（store 的 fetchFigures 负责写 state，
 *         这里返回同样的 payload，由 store 写入 state）；
 *   2) 默认导出 staticApi：axios 形状的最小 shim（`get(url, { params })`），
 *      使 stores/figures.ts 只需换一行导入即可切换数据源，其余逻辑零改动。
 *
 * 数据布局（web/public/data/）：
 *   figures.index.json       1057 条轻量索引（code / name_zh / name_en / era / domains /
 *                            historical_domains / gender / ethnicity / n_modes）
 *   figures/{code}.json      1057 个详情分片（含 description / reason / steps / expected / case / modes）
 *   modes/index-{0..7}.json  2848 条模式摘要（ModesView 用；= meta.json 的 mode_summaries_published）
 *   modes/by-figure/…        283 个「某人的 10 条模式」分片
 *   meta.json                条数与 sha256（供数据校验）
 *
 * 已知边界（诚实标注，不假装具备后端能力）：
 *   - 检索分两条路：主路径是全文检索（见 api/fulltextSearch.ts，解码 A5 的二进制倒排索引分片，
 *     覆盖人物名 / 模式名 / 分类 / 出处 / 概念 / 领域 / 定义摘要），本文件的
 *     「编号 / 名称 / 领域」子串匹配保留为降级与兜底路径（索引不可用、编号、拉丁前缀、场景条目）。
 *     两者都是字符级匹配、不是向量语义检索，故 semanticSearch 仍降级为 searchFigures 的别名，
 *     UI 文案不得宣称语义搜索；
 *   - theme(TECH/WOMEN/…)、nationality、civilization_sphere 等国际字段不在索引中，
 *     后端 /api/v1/scenarios 同样未实现这些筛选，传入时忽略（与 api 模式行为一致）；
 *   - getSimilar 未预计算相似度：按 historical_domains / domains / era / gender / ethnicity
 *     的标签重叠度打分（非向量相似度），UI 标注为「标签相似度」。
 */
import type { Figure, FigureListResponse, FiguresParams } from '../stores/figures'

const DATA_ROOT = `${import.meta.env.BASE_URL || '/'}data/`

interface IndexEntry {
  code: string
  name_zh?: string | null
  name_en?: string | null
  era?: string | null
  domains?: string[]
  historical_domains?: string[]
  gender?: string | null
  ethnicity?: string | null
  n_modes?: number
}

interface FigureShard {
  code: string
  name_zh?: string | null
  name_en?: string | null
  description_zh?: string | null
  description_en?: string | null
  reason_zh?: string | null
  reason_en?: string | null
  steps_zh?: unknown
  steps_en?: unknown
  expected_zh?: unknown
  expected_en?: unknown
  case_zh?: string | null
  case_en?: string | null
  era?: string | null
  domains?: string[]
  historical_domains?: string[]
  gender?: string | null
  ethnicity?: string | null
  modes?: number[]
}

/** getSimilar 返回的人物附带标签重叠度（0~1），供 FigureDetailView 展示百分比 */
export interface SimilarFigure extends Figure {
  similarity_score: number
}

interface StaticRequestConfig {
  params?: Record<string, unknown>
}

// ---------------------------------------------------------------- 基础读取

const fetchJson = async <T>(path: string): Promise<T> => {
  const response = await fetch(`${DATA_ROOT}${path}`)
  if (!response.ok) {
    throw new Error(`[static] 读取 ${path} 失败：HTTP ${response.status}`)
  }
  return (await response.json()) as T
}

let indexPromise: Promise<IndexEntry[]> | null = null

/** 索引只拉取一次并常驻内存（161 KB raw / 32 KB gzip） */
const loadIndex = (): Promise<IndexEntry[]> => {
  if (!indexPromise) indexPromise = fetchJson<IndexEntry[]>('figures.index.json')
  return indexPromise
}

const shardPromises = new Map<string, Promise<FigureShard>>()

/** 每个详情分片只拉一次；失败时清缓存以便重试（同名文件带空格，如 "Sun Quan" → %20） */
const loadShard = (code: string): Promise<FigureShard> => {
  let promise = shardPromises.get(code)
  if (!promise) {
    promise = fetchJson<FigureShard>(`figures/${encodeURIComponent(code)}.json`)
    shardPromises.set(code, promise)
    promise.catch(() => shardPromises.delete(code))
  }
  return promise
}

// ---------------------------------------------------------------- 字段归一

const asNumber = (value: unknown, fallback: number): number => {
  const n = Number(value)
  return Number.isFinite(n) && n > 0 ? Math.floor(n) : fallback
}

const pickLang = (zh: string | null | undefined, en: string | null | undefined, lang: string): string => {
  if (lang === 'en') return en || zh || ''
  return zh || en || ''
}

/** 静态产物里 steps/expected 来自 DB 的 JSON 文本列，这里统一解析成数组/可读文本 */
const toStringArray = (value: unknown): string[] => {
  if (Array.isArray(value)) return value.map(item => String(item))
  if (typeof value !== 'string') return []
  const text = value.trim()
  if (!text) return []
  if (text.startsWith('[')) {
    try {
      const parsed = JSON.parse(text)
      if (Array.isArray(parsed)) return parsed.map(item => String(item))
    } catch {
      /* 不是合法 JSON，按普通文本处理 */
    }
  }
  return [text]
}

const toText = (value: unknown): string => {
  const items = toStringArray(value)
  return items.join('；')
}

const toFigure = (entry: IndexEntry, shard: FigureShard | undefined, lang: string): Figure => ({
  code: entry.code,
  name: pickLang(shard?.name_zh ?? entry.name_zh, shard?.name_en ?? entry.name_en, lang),
  description: pickLang(shard?.description_zh, shard?.description_en, lang),
  modes: Array.isArray(shard?.modes) ? shard!.modes : [],
  reason: pickLang(shard?.reason_zh, shard?.reason_en, lang),
  steps: toStringArray(lang === 'en' ? shard?.steps_en ?? shard?.steps_zh : shard?.steps_zh ?? shard?.steps_en),
  expected: toText(lang === 'en' ? shard?.expected_en ?? shard?.expected_zh : shard?.expected_zh ?? shard?.expected_en),
  case: pickLang(shard?.case_zh, shard?.case_en, lang),
  era: entry.era ?? shard?.era ?? null,
  historical_domains: entry.historical_domains ?? shard?.historical_domains ?? [],
  domains: entry.domains ?? shard?.domains ?? [],
  gender: entry.gender ?? shard?.gender ?? null,
  ethnicity: entry.ethnicity ?? shard?.ethnicity ?? null,
})

/** 索引条目 + 详情分片 → 与后端 FigureResponse 一致的 Figure */
const hydrate = async (entry: IndexEntry, lang: string): Promise<Figure> => {
  let shard: FigureShard | undefined
  try {
    shard = await loadShard(entry.code)
  } catch (err) {
    // 分片缺失时降级为索引字段（列表仍可用，只是详情字段为空）
    console.warn('[static] 详情分片读取失败，降级为索引字段:', entry.code, err)
  }
  return toFigure(entry, shard, lang)
}

// ---------------------------------------------------------------- 筛选匹配

const matchesKeyword = (entry: IndexEntry, query: string): boolean => {
  const q = query.trim().toLowerCase()
  if (!q) return true
  const haystack = [
    entry.code,
    entry.name_zh,
    entry.name_en,
    ...(entry.domains || []),
    ...(entry.historical_domains || []),
  ]
  return haystack.some(value => typeof value === 'string' && value.toLowerCase().includes(q))
}

const matchesFilters = (entry: IndexEntry, params: FiguresParams): boolean => {
  if (params.era && entry.era !== params.era) return false
  if (params.gender && entry.gender !== params.gender) return false
  if (params.ethnicity && entry.ethnicity !== params.ethnicity) return false
  if (params.domain && !(entry.domains || []).includes(params.domain)) return false
  if (params.historical_domain && !(entry.historical_domains || []).includes(params.historical_domain)) return false
  if (params.search && !matchesKeyword(entry, params.search)) return false
  return true
}

// ---------------------------------------------------------------- 5 个数据方法

/** 与 store.fetchFigures 同参数：返回同样的 FigureListResponse，由 store 写入 state */
export const fetchFigures = async (params: FiguresParams = {}): Promise<FigureListResponse> => {
  const lang = params.lang ?? 'zh'
  const page = asNumber(params.page, 1)
  const pageSize = asNumber(params.page_size, 20)
  const index = await loadIndex()
  const filtered = index.filter(entry => matchesFilters(entry, params))
  const start = (page - 1) * pageSize
  const pageEntries = filtered.slice(start, start + pageSize)
  const data = await Promise.all(pageEntries.map(entry => hydrate(entry, lang)))
  return {
    success: true,
    data,
    meta: {
      total: filtered.length,
      page,
      page_size: pageSize,
      total_pages: Math.ceil(filtered.length / pageSize),
    },
  }
}

/** 与 store.fetchFigure 同参数：命中详情分片返回 Figure，未收录返回 null */
export const fetchFigure = async (code: string, lang = 'zh'): Promise<Figure | null> => {
  const index = await loadIndex()
  const key = code.trim().toUpperCase()
  const entry = index.find(item => item.code.toUpperCase() === key)
  if (entry) return hydrate(entry, lang)

  // 索引没收录但分片存在（历史遗留编码）：仍尝试直读分片
  try {
    const shard = await loadShard(code)
    return toFigure({ code: shard.code || code }, shard, lang)
  } catch {
    return null
  }
}

/** 与 store.searchFigures 同参数：内存子串匹配（编号 / 中英名称 / 领域） */
export const searchFigures = async (query: string, lang = 'zh', limit = 20): Promise<Figure[]> => {
  if (!query || !query.trim()) return []
  const index = await loadIndex()
  const hits = index.filter(entry => matchesKeyword(entry, query)).slice(0, asNumber(limit, 20))
  return Promise.all(hits.map(entry => hydrate(entry, lang)))
}

/**
 * 静态模式没有向量检索：semanticSearch 是 searchFigures 的别名（也不走全文倒排索引）。
 * UI 文案必须写清是「倒排匹配 / 关键词匹配」，不得宣称语义搜索（诚实标注）。
 */
export const semanticSearch = searchFigures

/**
 * 全文检索接入点（A0 §4.7 第 5 条约定的 `searchFullText(query)`）。
 * 实现放在 api/fulltextSearch.ts：解码 A5 的索引分片，按 token 权重和排序；
 * index 不可用时 searchFullText 返回 null，调用方必须降级为子串匹配并显示「已降级为关键词匹配」。
 */
export { searchFullText, loadSearchMeta, tokenizeQuery } from './fulltextSearch'

const overlapCount = (a: string[] = [], b: string[] = []): number => a.filter(value => b.includes(value)).length

/** 标签重叠度：历史领域(权重3) / 思维领域(权重2) / 时代(2) / 性别(0.5) / 民族(0.5)，归一到 0~1 */
const tagSimilarity = (source: IndexEntry, target: IndexEntry): number => {
  const raw =
    3 * overlapCount(source.historical_domains, target.historical_domains) +
    2 * overlapCount(source.domains, target.domains) +
    (source.era && source.era === target.era ? 2 : 0) +
    (source.gender && source.gender === target.gender ? 0.5 : 0) +
    (source.ethnicity && source.ethnicity === target.ethnicity ? 0.5 : 0)
  const capacity = 3 * (source.historical_domains?.length || 0) + 2 * (source.domains?.length || 0) + 3
  return capacity > 0 ? Math.min(1, raw / capacity) : 0
}

/** 与 store.getSimilar 同参数：按标签重叠度取 top-k（非向量相似度，UI 标注「标签相似度」） */
export const getSimilar = async (code: string, lang = 'zh', topK = 5): Promise<SimilarFigure[]> => {
  const index = await loadIndex()
  const key = code.trim().toUpperCase()
  const source = index.find(item => item.code.toUpperCase() === key)
  if (!source) return []

  const ranked = index
    .filter(entry => entry.code !== source.code)
    .map(entry => ({ entry, score: tagSimilarity(source, entry) }))
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score || a.entry.code.localeCompare(b.entry.code))
    .slice(0, asNumber(topK, 5))

  const figures = await Promise.all(ranked.map(item => hydrate(item.entry, lang)))
  return figures.map((figure, i) => ({ ...figure, similarity_score: ranked[i].score }))
}

// ---------------------------------------------------------------- axios 形状 shim

const readParams = (config?: StaticRequestConfig): Record<string, unknown> => config?.params ?? {}

const DETAIL_URL = /^\/api\/v1\/scenarios\/([^/]+)$/
const SIMILAR_URL = /^\/api\/v1\/scenarios\/(?:batch\/)?([^/]+)\/similar$/
const SEARCH_URL = '/api/v1/scenarios/search'
const SEMANTIC_URLS = ['/api/v1/scenarios/semantic-search', '/api/v1/scenarios/batch/semantic-search']

/** 只实现 stores/figures.ts 用到的路由子集；未实现的接口直接报错，绝不静默返回空数据 */
const get = async <T = any>(url: string, config?: StaticRequestConfig): Promise<{ data: T }> => {
  const params = readParams(config)
  const lang = typeof params.lang === 'string' ? params.lang : 'zh'
  if (url === SEARCH_URL || SEMANTIC_URLS.includes(url)) {
    const query = String(params.q ?? '')

    const limit = asNumber(params.limit ?? params.top_k, 20)
    const data = await searchFigures(query, lang, limit)
    return {
      data: {
        success: true,
        data,
        meta: {
          total: data.length,
          query,
          search_type: url === SEARCH_URL ? 'keyword' : 'keyword-index(static)',
          model: 'static-in-memory',
        },
      } as unknown as T,
    }
  }

  const similar = SIMILAR_URL.exec(url)
  if (similar) {
    const code = decodeURIComponent(similar[1])
    const data = await getSimilar(code, lang, asNumber(params.top_k, 5))
    return {
      data: {
        success: true,
        data,
        meta: { total: data.length, source_code: code, search_type: 'tag-overlap(static)' },
      } as unknown as T,
    }
  }

  const detail = DETAIL_URL.exec(url)
  if (detail) {
    const code = decodeURIComponent(detail[1])
    const figure = await fetchFigure(code, lang)
    if (!figure) throw new Error(`[static] 人物不存在：${code}`)
    return { data: { success: true, data: figure } as unknown as T }
  }

  if (/^\/api\/v1\/scenarios\/?$/.test(url)) {
    return { data: (await fetchFigures(params as FiguresParams)) as unknown as T }
  }

  throw new Error(`[static] 适配层未实现该接口：${url}`)
}

/** 人物专属模式分片：data/modes/by-figure/{figure_code}.json */
export interface FigureModesPayload {
  figure_code: string
  figure_name: string
  count: number
  modes: any[]
}

export const fetchFigureModes = async (code: string): Promise<FigureModesPayload | null> => {
  if (!code) return null
  try {
    const res = await fetch(`${DATA_ROOT}modes/by-figure/${encodeURIComponent(code)}.json`)
    if (!res.ok) return null
    return (await res.json()) as FigureModesPayload
  } catch {
    return null
  }
}

/** 统一名录索引：人物(283) + 场景(N) 合并 */
export interface UnifiedEntry {
  code: string
  name: string
  type: 'figure' | 'scenario'
  era?: string
  domains?: string[]
  historical_domains?: string[]
  gender?: string
  ethnicity?: string
  n_modes?: number
  description?: string
  href?: string
}

export interface UnifiedIndex {
  schema: string
  counts: { total: number; figures: number; scenarios: number; with_modes: number }
  items: UnifiedEntry[]
}

export const fetchUnifiedIndex = async (): Promise<UnifiedIndex | null> => {
  try {
    const res = await fetch(`${DATA_ROOT}index.unified.json`)
    if (!res.ok) return null
    return (await res.json()) as UnifiedIndex
  } catch {
    return null
  }
}

const staticApi = { get }

export const useApi = () => staticApi

export default staticApi
