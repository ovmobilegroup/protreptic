/**
 * 模式摘要索引（web/public/data/modes/index-0..7.json）的共享加载器。
 *
 * 为什么单独一层：A5 的全文检索倒排索引只存 doc_id，而
 * 「doc_id = 该 mode 在 modes/index-0..7.json 按序拼接后的下标」（见
 * data/search/meta.json 的 doc_id_contract，条数以 meta.json 的 mode_summaries_published 为准）。/modes 本来就要拉这 8 片，
 * /figures 的检索用同一份缓存把 doc_id 还原成「属于哪位人物」，两个视图共用一次网络请求。
 *
 * 注意：这个文件只做「加载 + 归一」，不做检索。索引里没有 mode_code，所以
 * mode_code 一类的查询仍由调用方的子串匹配兜底（见 api/fulltextSearch.ts 的说明）。
 */
const MODE_INDEX_SHARDS = 8

export interface ModeIndexEntry {
  /** 在 modes/index-0..7.json 按序拼接后的下标，与检索索引的 doc_id 同源 */
  docId: number
  modeCode: string
  figureCode: string
  figureName: string
  nameZh: string
  nameEn: string
  category: string
  domainZh: string
  domainEn: string
}

const CJK = /[\u3400-\u9fff\uf900-\ufaff]/

/**
 * 汇总索引里的名称字段并不总是字符串：源 data/modes_data.json 里有一批记录把
 * name_zh / name_en 写成历史三元组 [中文, English, 分类]（与 thinking_modes 表的
 * 标量列不一致；当前已发布的摘要实测 0 条如此，归一逻辑保留以防旧分片回落）。裸 String(数组) 会渲染成 "剪纸即兴法,Papercut-Improvisation Method,创作发生方法论/…"
 * 串进 /modes 卡片、/graph 节点与下拉、/compare 名称——所以这里取第一个合适元素：
 * 中文名取首个含汉字项，英文名取首个不含汉字项（缺失时回落中文本名）。
 * 同一份数据还会被其它加载器读到；本层归一保证调用方永远拿到标量。
 */
const pickZh = (v: unknown): string => {
  const items = Array.isArray(v) ? v : [v]
  for (const item of items) {
    const s = String(item ?? '').trim()
    if (s && CJK.test(s)) return s
  }
  for (const item of items) {
    const s = String(item ?? '').trim()
    if (s) return s
  }
  return ''
}

const pickEn = (v: unknown): string => {
  const items = Array.isArray(v) ? v : [v]
  for (const item of items) {
    const s = String(item ?? '').trim()
    if (s && !CJK.test(s)) return s
  }
  return ''
}

const DATA_ROOT = `${import.meta.env.BASE_URL || '/'}data/`

let modeIndexPromise: Promise<ModeIndexEntry[]> | null = null

const fetchShard = async (shard: number): Promise<Record<string, unknown>[]> => {
  const res = await fetch(`${DATA_ROOT}modes/index-${shard}.json`)
  if (!res.ok) throw new Error(`data/modes/index-${shard}.json HTTP ${res.status}`)
  const data = await res.json()
  if (!Array.isArray(data)) throw new Error(`data/modes/index-${shard}.json 结构异常`)
  return data as Record<string, unknown>[]
}

const load = async (): Promise<ModeIndexEntry[]> => {
  const shards = await Promise.all(
    Array.from({ length: MODE_INDEX_SHARDS }, (_, i) => fetchShard(i))
  )
  return shards.flat().map((m, docId) => ({
    docId,
    modeCode: String(m.mode_code ?? ''),
    figureCode: String(m.figure_code ?? ''),
    figureName: String(m.figure_name ?? ''),
    nameZh: pickZh(m.name_zh) || pickZh(m.name_en),
    nameEn: pickEn(m.name_en) || pickEn(m.name_zh),
    category: String(m.category ?? ''),
    domainZh: String(m.domain_zh ?? ''),
    domainEn: String(m.domain_en ?? ''),
  }))
}

/** 8 个分片只拉一次并常驻内存；失败时清缓存以便重试（与 doc_id 契约同源，顺序不可改） */
export const loadModeIndex = (): Promise<ModeIndexEntry[]> => {
  if (!modeIndexPromise) {
    modeIndexPromise = load()
    modeIndexPromise.catch(() => { modeIndexPromise = null })
  }
  return modeIndexPromise
}

/** doc_id -> figure_code，供检索结果回指人物（同一份缓存，不发额外请求） */
export const loadFigureCodeByDoc = async (): Promise<string[]> => {
  const entries = await loadModeIndex()
  const codes = new Array<string>(entries.length).fill('')
  for (const entry of entries) if (entry.docId < codes.length) codes[entry.docId] = entry.figureCode
  return codes
}
