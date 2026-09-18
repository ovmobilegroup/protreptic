/**
 * 「每日一模式」(Phase30-B4) 的数据加载与确定性选取。
 *
 * 产物（tools/build_daily_index.py，必须在 export_static_site.py 之后运行）：
 *   data/daily/index.json  { total, figures, entries: [[mode_code, figure_code]], … }  12 KB gzip —— 定位用
 *   data/daily/names.json  { names: [[name_zh, name_en, category]], … }              175 KB gzip —— names[i] 属于 entries[i]
 * 首页只拉 index.json（再按 figure_code 拉一次 modes/by-figure/{code}.json 取详情），
 * /daily 归档页才拉 names.json（列表要显示历史每天的模式名）。
 *
 * 确定性契约（与 tools/build_daily_index.py 的 day_number()/pick_index() 同构，两边必须同时改）：
 *   dayNumber(key) = floor(Date.parse(key + 'T00:00:00Z') / 86400000)
 *   index(key)     = dayNumber(key) % total
 * 口径固定为 Asia/Shanghai (UTC+8)：先把「现在」换算成北京时间的日期字符串，再用该日期定位，
 * 因此同一天内任何时刻、任何设备、任何时区打开结果一致，跨天才变。
 * 注意 entries 的顺序由构建脚本固化（by-figure 分片按 figure_code 升序，剔除隔离名单），
 * 数据集新增人物/模式会让历史选取重排 —— 这是「按日期取模」的固有性质，文案不得承诺永久不变。
 *
 * 已确证虚构的人物（H-SX-001）在构建期就被排除，前端不必再判。
 */

export const TZ_OFFSET_MINUTES = 480
export const TZ_LABEL = 'Asia/Shanghai'
export const MS_PER_DAY = 86400000
export const DAILY_ARCHIVE_PAGE_SIZE = 30

const DATA_ROOT = `${import.meta.env.BASE_URL || '/'}data/`
const DATA_MODE = import.meta.env.VITE_DATA_MODE ?? 'api'

export interface DailyIndex {
  schema: string
  generatedAt: string
  tz: string
  algorithm: string
  order: string
  total: number
  figureCount: number
  figures: Record<string, string>
  entries: Array<[string, string]>
}

/** 归档页用的名称表：与 index.entries 下标对齐 */
export interface DailyNameRow {
  nameZh: string
  nameEn: string
  category: string
}

export interface DailyPick {
  /** 北京时间口径的日期 YYYY-MM-DD */
  dateKey: string
  /** 该日期对应的「第几天」，用于展示取模算式 */
  dayNumber: number
  /** = dayNumber % total，entries 里的下标 */
  index: number
  modeCode: string
  figureCode: string
  figureName: string
}

let indexPromise: Promise<DailyIndex | null> | null = null
let namesPromise: Promise<DailyNameRow[] | null> | null = null

/** 定位索引只拉一次并常驻内存；失败时清缓存以便重试 */
export const loadDailyIndex = (): Promise<DailyIndex | null> => {
  if (!indexPromise) {
    indexPromise = (async () => {
      if (DATA_MODE !== 'static') return null
      try {
        const res = await fetch(`${DATA_ROOT}daily/index.json`)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const raw = (await res.json()) as Record<string, unknown>
        const entries = Array.isArray(raw.entries) ? (raw.entries as Array<[string, string]>) : []
        const total = Number(raw.total) || entries.length
        if (!entries.length || !total) throw new Error('daily/index.json 结构异常')
        return {
          schema: String(raw.schema ?? ''),
          generatedAt: String(raw.generated_at ?? ''),
          tz: String(raw.tz ?? TZ_LABEL),
          algorithm: String(raw.algorithm ?? ''),
          order: String(raw.order ?? ''),
          total,
          figureCount: Number(raw.figure_count) || 0,
          figures: (raw.figures as Record<string, string>) || {},
          entries,
        } satisfies DailyIndex
      } catch (err) {
        console.warn('[daily] daily/index.json 不可用：', err)
        return null
      }
    })()
    indexPromise.catch(() => { indexPromise = null })
  }
  return indexPromise
}

/** 名称表（仅 /daily 归档页需要）：同样只拉一次 */
export const loadDailyNames = (): Promise<DailyNameRow[] | null> => {
  if (!namesPromise) {
    namesPromise = (async () => {
      if (DATA_MODE !== 'static') return null
      try {
        const res = await fetch(`${DATA_ROOT}daily/names.json`)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const raw = (await res.json()) as { names?: unknown }
        const rows = Array.isArray(raw.names) ? raw.names : []
        return rows.map((row) => {
          const r = Array.isArray(row) ? row : []
          return { nameZh: String(r[0] ?? ''), nameEn: String(r[1] ?? ''), category: String(r[2] ?? '') }
        })
      } catch (err) {
        console.warn('[daily] daily/names.json 不可用：', err)
        return null
      }
    })()
    namesPromise.catch(() => { namesPromise = null })
  }
  return namesPromise
}

/** 北京时间口径下的日期字符串（YYYY-MM-DD） */
export const dateKeyOf = (date: Date): string =>
  new Date(date.getTime() + TZ_OFFSET_MINUTES * 60000).toISOString().slice(0, 10)

/** 今天（北京时间） */
export const todayKey = (): string => dateKeyOf(new Date())

const DATE_KEY_RE = /^\d{4}-\d{2}-\d{2}$/

export const isDateKey = (value: unknown): boolean => {
  const key = String(value ?? '')
  if (!DATE_KEY_RE.test(key)) return false
  const ms = Date.parse(`${key}T00:00:00Z`)
  return Number.isFinite(ms) && new Date(ms).toISOString().slice(0, 10) === key
}

/**
 * 日期 -> 「第几天」。UTC 零点加 +8h 仍落在同一 UTC 日，
 * 所以 floor(Date.parse(key + 'T00:00:00Z') / 86400000) 就是该日期（北京时间口径）的天序号。
 */
export const dayNumber = (key: string): number => Math.floor(Date.parse(`${key}T00:00:00Z`) / MS_PER_DAY)

/** 日期偏移（按日历天，始终在同一天序列里走） */
export const shiftDateKey = (key: string, days: number): string =>
  new Date(Date.parse(`${key}T00:00:00Z`) + days * MS_PER_DAY).toISOString().slice(0, 10)

/** 核心选取：同一 key 永远得到同一条（负数取模也归一） */
export const pickAt = (index: DailyIndex, key: string): DailyPick | null => {
  if (!index.entries.length || !index.total) return null
  const dn = dayNumber(key)
  const i = ((dn % index.total) + index.total) % index.total
  const entry = index.entries[i]
  if (!entry) return null
  return {
    dateKey: key,
    dayNumber: dn,
    index: i,
    modeCode: String(entry[0] ?? ''),
    figureCode: String(entry[1] ?? ''),
    figureName: index.figures[String(entry[1] ?? '')] || '',
  }
}

/** 今天选中的那一条（首页模块用） */
export const pickToday = async (key = todayKey()): Promise<DailyPick | null> => {
  const index = await loadDailyIndex()
  return index ? pickAt(index, key) : null
}

/** 从 endKey 往前 count 天（含当天）的选取结果，倒序返回（/daily 归档列表用） */
export const listDays = (index: DailyIndex, endKey: string, count: number): DailyPick[] => {
  const out: DailyPick[] = []
  for (let i = 0; i < count; i += 1) {
    const key = shiftDateKey(endKey, -i)
    const pick = pickAt(index, key)
    if (pick) out.push(pick)
  }
  return out
}

const WEEKDAYS_ZH = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
const WEEKDAYS_EN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

/** 该日期的星期（用固定口径的日历日算，不受本地时区影响） */
export const weekdayLabel = (key: string, locale: string): string => {
  const d = new Date(Date.parse(`${key}T00:00:00Z`))
  const day = d.getUTCDay()
  return locale === 'en' ? WEEKDAYS_EN[day] : WEEKDAYS_ZH[day]
}

/** 名称表按下标取值（下标即 entries 下标） */
export const nameFor = (names: DailyNameRow[] | null, index: number): DailyNameRow | null =>
  names && index >= 0 && index < names.length ? names[index] : null
