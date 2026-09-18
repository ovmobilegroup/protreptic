/**
 * Phase30-A6：全文检索前端 —— 解码 A5（tools/build_search_index.py）产出的二进制倒排索引分片。
 *
 * 权威规格 = `data/search/meta.json`（spec_version 1.1-a5）与
 * `docs/architecture/web_p0_architecture.md` §4.3–4.8。查询期的分词 / 分片函数 / 权重表
 * 必须与构建脚本逐条一致：改这里等于改规格，必须同步改 tools/build_search_index.py 与文档。
 *
 * 分片格式（每片 raw 字节，线上由 Pages 做 gzip 传输、浏览器自动解压）：
 *   varint(len(body)) + body + varint(len(weights)) + weights
 *   body    = 升序 token 记录：varint(len(utf8(token))) + utf8(token) + varint(df) + varint(doc_id 升序差值)
 *   weights = 每 token 1 字节，顺序与 body 一致，取值 0/1/2 对应权重 4/2/1
 * 分片函数：bucket = crc32(utf8(token 首字符)) % 16
 *   —— 一次查询只拉「查询 token 首字符」命中的那几片（中文 4 字查询通常 <= 3 片）。
 *
 * 能力边界（UI 必须如实说明，不得宣称语义检索）：
 *   - 相关度 = 命中 token 的权重和（4 = 人物名/模式名，2 = 分类/出处/概念/领域，1 = 定义前 30 字），
 *     没有 IDF / BM25 / 长度归一；
 *   - 拉丁词不做前缀扩展（`decis` 无结果、`decision` 有结果），编号（M-ZUX-001）也不在索引里，
 *     这两类由调用方的子串匹配兜底；
 *   - 深度正文（representative_cases / modern_applications / 完整 definition）不在索引里；
 *   - 索引不可用时返回 null，调用方必须回落到子串匹配并显示「已降级为关键词匹配」。
 */
const SEARCH_ROOT = `${import.meta.env.BASE_URL || '/'}data/search/`
const DEFAULT_SHARD_COUNT = 16
/** 权重表编码 -> 权重（与构建脚本的 WEIGHT_TIERS 一致） */
const WEIGHT_BY_CODE = [4, 2, 1]

export interface SearchIndexMeta {
  spec_version?: string
  doc_count?: number
  shard_count?: number
  token_count?: number
  total_gzip_kb?: number
  doc_id_contract?: string
}

export interface FullTextHit {
  /** 该 mode 在 modes/index-0..7.json 拼接后的下标（用 api/modeIndex.ts 还原展示字段） */
  docId: number
  /** 命中 token 的权重和，不是归一化相似度 */
  score: number
  /** 命中的 token（去重），用于说明「命中了什么」 */
  tokens: string[]
}

export type FullTextNote = 'ok' | 'empty' | 'short'

export interface FullTextOutcome {
  hits: FullTextHit[]
  tokens: string[]
  /** 本次查询真正请求了的分片号，便于排查与统计 */
  shards: number[]
  note: FullTextNote
}

// ---------------------------------------------------------------- 解码工具

let crcTable: Uint32Array | null = null

const crc32 = (bytes: Uint8Array): number => {
  if (!crcTable) {
    crcTable = new Uint32Array(256)
    for (let i = 0; i < 256; i++) {
      let c = i
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1
      crcTable[i] = c >>> 0
    }
  }
  let crc = 0xffffffff
  for (let i = 0; i < bytes.length; i++) crc = crcTable[(crc ^ bytes[i]) & 0xff] ^ (crc >>> 8)
  return (crc ^ 0xffffffff) >>> 0
}

const readVarint = (buf: Uint8Array, pos: number): [number, number] => {
  let shift = 0
  let val = 0
  for (;;) {
    const byte = buf[pos]
    if (byte === undefined) throw new Error('[search] 分片被截断')
    pos += 1
    val += (byte & 0x7f) * 2 ** shift
    if (!(byte & 0x80)) return [val, pos]
    shift += 7
    if (shift > 49) throw new Error('[search] varint 过长')
  }
}

interface ShardToken {
  weight: number
  ids: number[]
}

/** 解码单片：token -> { weight, doc_ids }（与构建脚本的 decode_shard 等价） */
export const decodeSearchShard = (buf: Uint8Array): Map<string, ShardToken> => {
  const decoder = new TextDecoder('utf-8')
  let pos = 0
  let bodyLen: number
  ;[bodyLen, pos] = readVarint(buf, pos)
  const bodyEnd = pos + bodyLen
  const records: Array<[string, number[]]> = []
  while (pos < bodyEnd) {
    let tokenLen: number
    ;[tokenLen, pos] = readVarint(buf, pos)
    const token = decoder.decode(buf.subarray(pos, pos + tokenLen))
    pos += tokenLen
    let df: number
    ;[df, pos] = readVarint(buf, pos)
    const ids: number[] = []
    let prev = 0
    for (let k = 0; k < df; k++) {
      let delta: number
      ;[delta, pos] = readVarint(buf, pos)
      const docId = k === 0 ? delta : prev + delta
      ids.push(docId)
      prev = docId
    }
    records.push([token, ids])
  }
  if (pos !== bodyEnd) throw new Error('[search] 分片 token 记录体越界')

  let weightLen: number
  ;[weightLen, pos] = readVarint(buf, pos)
  if (pos + weightLen !== buf.length) throw new Error('[search] 分片权重表长度不符')

  const table = new Map<string, ShardToken>()
  for (let i = 0; i < records.length; i++) {
    const code = buf[pos + i]
    const weight = WEIGHT_BY_CODE[code]
    if (weight === undefined) throw new Error(`[search] 权重表出现未知编码 ${code}`)
    table.set(records[i][0], { weight, ids: records[i][1] })
  }
  return table
}

// ---------------------------------------------------------------- 分词（必须与构建脚本一致）

const CJK_RANGES = /^[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]$/
const ALNUM = /^[\p{L}\p{N}]$/u

const isCjk = (ch: string): boolean => CJK_RANGES.test(ch)
const isAlnum = (ch: string): boolean => ALNUM.test(ch)

/** 与 tools/build_search_index.py 的 tokenize() 等价：NFKC + 连续 CJK 取 2-gram + 拉丁数字小写词（长度 >= 2） */
export const tokenizeQuery = (text: string): string[] => {
  if (!text) return []
  const chars = Array.from(text.normalize('NFKC'))
  const out: string[] = []
  let i = 0
  while (i < chars.length) {
    const ch = chars[i]
    if (isCjk(ch)) {
      let j = i
      while (j < chars.length && isCjk(chars[j])) j++
      const run = chars.slice(i, j)
      if (run.length === 1) out.push(run[0])
      else for (let k = 0; k < run.length - 1; k++) out.push(run[k] + run[k + 1])
      i = j
    } else if (isAlnum(ch)) {
      let j = i
      while (j < chars.length && isAlnum(chars[j]) && !isCjk(chars[j])) j++
      const word = chars.slice(i, j).join('').toLowerCase()
      if (word.length >= 2) out.push(word)
      i = j
    } else {
      i += 1
    }
  }
  return out
}

const shardOf = (token: string, shardCount: number): number =>
  crc32(new TextEncoder().encode(Array.from(token)[0])) % shardCount

// ---------------------------------------------------------------- 加载

let metaPromise: Promise<SearchIndexMeta | null> | null = null

/** meta.json 只读一次；失败返回 null（索引不可用 -> 调用方降级），不抛异常 */
export const loadSearchMeta = (): Promise<SearchIndexMeta | null> => {
  if (!metaPromise) {
    metaPromise = fetch(`${SEARCH_ROOT}meta.json`)
      .then((res) => (res.ok ? (res.json() as Promise<SearchIndexMeta>) : null))
      .catch(() => null)
  }
  return metaPromise
}

const shardCache = new Map<number, Promise<Map<string, ShardToken>>>()

const fetchShard = async (shard: number, shardCount: number): Promise<Map<string, ShardToken>> => {
  const res = await fetch(`${SEARCH_ROOT}index-${shard}.bin`)
  if (!res.ok) throw new Error(`data/search/index-${shard}.bin HTTP ${res.status}`)
  return decodeSearchShard(new Uint8Array(await res.arrayBuffer()))
}

/** 分片常驻内存（二次查询不再走网络）；失败时清缓存以便下次重试 */
const loadShard = (shard: number, shardCount: number): Promise<Map<string, ShardToken>> => {
  let promise = shardCache.get(shard)
  if (!promise) {
    promise = fetchShard(shard, shardCount)
    shardCache.set(shard, promise)
    promise.catch(() => shardCache.delete(shard))
  }
  return promise
}

/** 已解码分片数（调试/状态展示用） */
export const loadedShardCount = (): number => shardCache.size

// ---------------------------------------------------------------- 检索

export const MIN_QUERY_CHARS = 2

/**
 * 全文检索：分词 -> 按首字符定分片 -> 解 posting -> 权重和打分 -> 按 (分数降序, doc_id 升序)。
 * 索引不可用（meta 或分片拉取失败）返回 null，调用方必须降级为子串匹配并如实告知用户。
 * 命中为 0 时返回 note='empty'（不是失败：拉丁前缀、编号这类查不到是已知边界）。
 */
export const searchFullText = async (query: string, limit = 500): Promise<FullTextOutcome | null> => {
  const raw = (query || '').trim()
  const tokens = Array.from(new Set(tokenizeQuery(raw)))
  if (!raw || tokens.length === 0) {
    return { hits: [], tokens: [], shards: [], note: 'short' }
  }

  const meta = await loadSearchMeta()
  const shardCount =
    meta && typeof meta.shard_count === 'number' && meta.shard_count > 0
      ? meta.shard_count
      : DEFAULT_SHARD_COUNT

  const shards = Array.from(new Set(tokens.map((tk) => shardOf(tk, shardCount)))).sort((a, b) => a - b)

  let tables: Map<string, ShardToken>[]
  try {
    tables = await Promise.all(shards.map((s) => loadShard(s, shardCount)))
  } catch (err) {
    console.warn('[search] 倒排索引分片不可用，调用方需降级为关键词匹配：', err)
    return null
  }

  const scores = new Map<number, FullTextHit>()
  for (const table of tables) {
    for (const tk of tokens) {
      const entry = table.get(tk)
      if (!entry) continue
      for (const docId of entry.ids) {
        const hit = scores.get(docId)
        if (hit) {
          hit.score += entry.weight
          hit.tokens.push(tk)
        } else {
          scores.set(docId, { docId, score: entry.weight, tokens: [tk] })
        }
      }
    }
  }

  const hits = Array.from(scores.values())
    .sort((a, b) => b.score - a.score || a.docId - b.docId)
    .slice(0, Math.max(1, limit))

  return { hits, tokens, shards, note: hits.length ? 'ok' : 'empty' }
}
