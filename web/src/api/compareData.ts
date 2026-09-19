/**
 * compareData.ts — Phase30-B3: 跨人物/跨模式对比的数据层（不新增任何数据产物）。
 *
 * 只读既有静态分片：
 *   data/index.unified.json       统一名录（这里只取 type==='figure'：姓名、时代）
 *   data/modes/index-0..7.json    模式摘要（api/modeIndex.ts 的共享缓存；用于把 mode_code 反查回人物）
 *   data/modes/by-figure/*.json   283 个「某人的 N 条模式」分片 —— 唯一带 definition/process/source/key_concepts 的来源
 *
 * 实测事实（别想当然）：
 *   - 模式摘要索引只有 8 个字段（mode_code / figure_code / figure_name / name_zh / name_en / category / domain_*），
 *     没有定义与步骤；所以「模式级对比」也必须下载它所属人物的 by-figure 分片（约 22KB，走同一层缓存）。
 *   - 283 个人物代码在摘要索引与 by-figure 分片里一一对应，无缺口。
 *   - 场景代码（A-1-X-P 这类）没有 by-figure 分片，拿不到定义/步骤，因此不参与对比：
 *     解析不到就返回 null，由 UI 明说「该项没有模式档案」，而不是渲染一列空表。
 */

import { fetchFigureModes, fetchUnifiedIndex } from './static'
import { loadModeIndex } from './modeIndex'

export const MAX_COMPARE_ITEMS = 4

export type CompareKind = 'figure' | 'mode'

export interface CompareMode {
  code: string
  name: string
  nameEn: string
  category: string
  domain: string
  domainEn: string
  definition: string
  definitionEn: string
  stepsZh: string[]
  stepsEn: string[]
  source: string
  quote: string
  concepts: string[]
}

export interface CompareItem {
  code: string
  kind: CompareKind
  /** 人物项=人物名；模式项=模式名 */
  name: string
  nameEn: string
  /** 人物项=时代（来自名录）；模式项=空 */
  era: string
  /** 模式项的所属人物；人物项=自身 */
  figureCode: string
  figureName: string
  modes: CompareMode[]
  domainCounts: Array<{ domain: string; count: number }>
  concepts: string[]
  sources: string[]
}

export interface RegistryEntry {
  code: string
  name: string
  kind: CompareKind
  /** 人物=时代，模式=所属人物 */
  meta: string
  /** 人物=历史领域，模式=领域/分类 */
  sub: string
}

export interface CompareResolveResult {
  items: CompareItem[]
  /** 解析不到（拼错、场景代码、数据缺口）的代码，原样回显给用户 */
  missing: string[]
}

const CJK_RE = /[\u3400-\u9fff\uf900-\ufaff]/

/**
 * name_zh / name_en 在历史数据里可能是三元组 [中文, English, 分类]（见 api/modeIndex.ts
 * 的同名说明；当前已发布的摘要索引实测无此情况）。text() 会把数组用空格连成
 * "剪纸即兴法 Papercut-Improvisation Method 创作发生方法论/…" 直接印在对比表上，
 * 所以名称类字段走这里：中文取首个含汉字项，英文取首个不含汉字项。
 */
const firstName = (v: unknown, wantCjk: boolean): string => {
  const items = Array.isArray(v) ? v : [v]
  for (const item of items) {
    const s = String(item ?? '').trim()
    if (s && CJK_RE.test(s) === wantCjk) return s
  }
  return ''
}

const text = (v: unknown): string => {
  if (Array.isArray(v)) return v.map((x) => text(x)).filter(Boolean).join(' ')
  if (v === null || v === undefined) return ''
  return String(v)
}

const list = (v: unknown): string[] => {
  if (Array.isArray(v)) return v.map((x) => text(x)).filter(Boolean)
  const s = text(v)
  return s ? [s] : []
}

const unique = (values: string[]): string[] => {
  const out: string[] = []
  for (const v of values) if (v && !out.includes(v)) out.push(v)
  return out
}

/* ------------------------------------------------------------------ *
 * 可选清单（人物 + 模式），供 /compare 的搜索面板使用
 * ------------------------------------------------------------------ */

let registryPromise: Promise<RegistryEntry[]> | null = null

const buildRegistry = async (): Promise<RegistryEntry[]> => {
  const [unified, modes] = await Promise.all([fetchUnifiedIndex(), loadModeIndex()])
  const out: RegistryEntry[] = []
  for (const f of unified?.items ?? []) {
    if (f.type !== 'figure') continue
    out.push({
      code: String(f.code || ''),
      name: String(f.name || f.code || ''),
      kind: 'figure',
      meta: text(f.era),
      sub: unique([...(f.historical_domains ?? []), ...(f.domains ?? [])]).slice(0, 2).join(' · '),
    })
  }
  for (const m of modes) {
    out.push({
      code: m.modeCode,
      name: m.nameZh || m.nameEn || m.modeCode,
      kind: 'mode',
      meta: m.figureName || m.figureCode,
      sub: m.domainZh || m.domainEn || m.category,
    })
  }
  return out
}

export const loadRegistry = (): Promise<RegistryEntry[]> => {
  if (!registryPromise) {
    registryPromise = buildRegistry()
    registryPromise.catch(() => { registryPromise = null })
  }
  return registryPromise
}

/** 字符级检索（不是语义检索）：编号/名称/领域/所属人物四路命中，前缀命中优先。 */
export const searchRegistry = (entries: RegistryEntry[], query: string, limit = 24): RegistryEntry[] => {
  const q = query.trim().toLowerCase()
  if (!q) return []
  const scored: Array<{ e: RegistryEntry; s: number }> = []
  for (const e of entries) {
    const name = e.name.toLowerCase()
    const code = e.code.toLowerCase()
    let s = 0
    if (name.startsWith(q) || code.startsWith(q)) s = 3
    else if (name.includes(q) || code.includes(q)) s = 2
    else if (e.meta.toLowerCase().includes(q) || e.sub.toLowerCase().includes(q)) s = 1
    if (s > 0) scored.push({ e, s })
  }
  scored.sort((a, b) => b.s - a.s || a.e.name.localeCompare(b.e.name))
  return scored.slice(0, limit).map((x) => x.e)
}

/* ------------------------------------------------------------------ *
 * 单项解析
 * ------------------------------------------------------------------ */

type Shard = Awaited<ReturnType<typeof fetchFigureModes>>

/** by-figure 分片缓存：同一人物被多个模式项引用时只下载一次 */
const shardCache = new Map<string, Promise<Shard>>()

const getShard = (figureCode: string): Promise<Shard> => {
  let p = shardCache.get(figureCode)
  if (!p) {
    p = fetchFigureModes(figureCode)
    shardCache.set(figureCode, p)
  }
  return p
}

const toCompareMode = (m: Record<string, unknown>): CompareMode => ({
  code: text(m.mode_code),
  name: firstOf(m.name_zh) || firstOf(m.name_en) || text(m.mode_code),
  nameEn: firstName(m.name_en, false) || text(m.name_en),
  category: text(m.category),
  domain: text(m.domain_zh) || text(m.domain_en) || '未标注领域',
  domainEn: text(m.domain_en),
  definition: text(m.definition_zh) || text(m.definition_en),
  definitionEn: text(m.definition_en),
  stepsZh: list(m.process_zh),
  stepsEn: list(m.process_en),
  source: text(m.source_chapter),
  quote: text(m.key_quote_zh) || text(m.key_quote_en),
  concepts: list(m.key_concepts),
})

/** 中文名（首个含汉字项，缺汉字时回落首个非空项） */
const firstOf = (v: unknown): string => firstName(v, true) || firstName(v, false)

const countDomains = (modes: CompareMode[]): Array<{ domain: string; count: number }> => {
  const map = new Map<string, number>()
  for (const m of modes) map.set(m.domain, (map.get(m.domain) ?? 0) + 1)
  return [...map.entries()]
    .map(([domain, count]) => ({ domain, count }))
    .sort((a, b) => b.count - a.count || a.domain.localeCompare(b.domain))
}

export const loadCompareItem = async (rawCode: string): Promise<CompareItem | null> => {
  const code = String(rawCode || '').trim()
  if (!code) return null
  const registry = await loadRegistry()
  const entry = registry.find((e) => e.code === code)
  if (!entry) return null

  if (entry.kind === 'figure') {
    const shard = await getShard(code)
    if (!shard) return null
    const modes = (shard.modes ?? []).map((m: Record<string, unknown>) => toCompareMode(m))
    const name = shard.figure_name || entry.name
    return {
      code,
      kind: 'figure',
      name,
      nameEn: '',
      era: entry.meta,
      figureCode: shard.figure_code || code,
      figureName: name,
      modes,
      domainCounts: countDomains(modes),
      concepts: unique(modes.flatMap((m) => m.concepts)),
      sources: unique(modes.map((m) => m.source)),
    }
  }

  const modeEntry = (await loadModeIndex()).find((m) => m.modeCode === code)
  if (!modeEntry) return null
  const shard = await getShard(modeEntry.figureCode)
  const raw = (shard?.modes ?? []).find((m: Record<string, unknown>) => text(m.mode_code) === code)
  if (!raw) return null
  const mode = toCompareMode(raw as Record<string, unknown>)
  return {
    code,
    kind: 'mode',
    name: mode.name,
    nameEn: mode.nameEn,
    era: '',
    figureCode: modeEntry.figureCode,
    figureName: shard?.figure_name || modeEntry.figureName,
    modes: [mode],
    domainCounts: countDomains([mode]),
    concepts: mode.concepts,
    sources: mode.source ? [mode.source] : [],
  }
}

/** 顺序解析，保序去重；解析不到的代码进 missing，不静默丢弃。 */
export const loadCompareItems = async (rawCodes: string[]): Promise<CompareResolveResult> => {
  const codes = unique(rawCodes.map((c) => String(c || '').trim())).slice(0, MAX_COMPARE_ITEMS)
  const resolved = await Promise.all(codes.map((c) => loadCompareItem(c)))
  const items: CompareItem[] = []
  const missing: string[] = []
  resolved.forEach((item, i) => {
    if (item) items.push(item)
    else missing.push(codes[i])
  })
  return { items, missing }
}

/* ------------------------------------------------------------------ *
 * 领域分布对比 / 共同概念
 * ------------------------------------------------------------------ */

export interface DomainRow {
  domain: string
  counts: number[]
  total: number
}

/** 领域 × 项 的矩阵：行=领域（并集，按总条数降序），列顺序与 items 一致 */
export const buildDomainMatrix = (items: CompareItem[]): DomainRow[] => {
  const domains: string[] = []
  for (const item of items) for (const d of item.domainCounts) if (!domains.includes(d.domain)) domains.push(d.domain)
  const rows = domains.map((domain) => {
    const counts = items.map((i) => i.domainCounts.find((d) => d.domain === domain)?.count ?? 0)
    return { domain, counts, total: counts.reduce((a, b) => a + b, 0) }
  })
  rows.sort((a, b) => b.total - a.total || a.domain.localeCompare(b.domain))
  return rows
}

export interface SharedConcept {
  concept: string
  codes: string[]
}

/** 出现在 >= min 项里的概念（按项数降序、概念名字典序） */
export const buildSharedConcepts = (items: CompareItem[], min = 2): SharedConcept[] => {
  const map = new Map<string, string[]>()
  for (const item of items) {
    for (const c of item.concepts) {
      const arr = map.get(c) ?? []
      if (!arr.includes(item.code)) arr.push(item.code)
      map.set(c, arr)
    }
  }
  return [...map.entries()]
    .filter(([, codes]) => codes.length >= min)
    .map(([concept, codes]) => ({ concept, codes }))
    .sort((a, b) => b.codes.length - a.codes.length || a.concept.localeCompare(b.concept))
}
