/**
 * useCompare.ts — Phase30-B3: 跨人物/跨模式对比的选中集合。
 *
 * 为什么做成模块级单例：入口有两处（人物档案页的「加入对比」与 /compare 的搜索面板），
 * 它们必须共享同一份选中集合；组件级 ref 做不到。
 *
 * 真相来源：URL 的 ?items=code1,code2（可分享、可直接打开，见 CompareView 的同步逻辑）。
 * localStorage 只是「上次选了谁」的粘性记忆，页面带 ?items= 打开时以 URL 为准覆盖它。
 *
 * 上限 4 项（任务口径 2-4）；超出不静默截断，返回 'full' 让调用方给出提示。
 */
import { ref } from 'vue'
import { MAX_COMPARE_ITEMS } from '../api/compareData'

export type AddResult = 'added' | 'duplicate' | 'full'

const STORAGE_KEY = 'protreptic_compare_items'

/** 构建期/prerender 快照里没有 localStorage —— 缺了就当空集合，绝不抛错。 */
const readStored = (): string[] => {
  try {
    if (typeof localStorage === 'undefined') return []
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    if (!Array.isArray(parsed)) return []
    return dedupe(parsed.map((v) => String(v))).slice(0, MAX_COMPARE_ITEMS)
  } catch {
    return []
  }
}

const dedupe = (codes: string[]): string[] => {
  const out: string[] = []
  for (const c of codes) {
    const clean = String(c || '').trim()
    if (clean && !out.includes(clean)) out.push(clean)
  }
  return out
}

const persist = (codes: string[]) => {
  try {
    if (typeof localStorage !== 'undefined') localStorage.setItem(STORAGE_KEY, JSON.stringify(codes))
  } catch { /* 隐私模式忽略 */ }
}

/** 全应用共享的选中集合（按加入顺序，顺序即对照表列序） */
const codes = ref<string[]>(readStored())

export const addCompare = (code: string): AddResult => {
  const clean = String(code || '').trim()
  if (!clean || codes.value.includes(clean)) return 'duplicate'
  if (codes.value.length >= MAX_COMPARE_ITEMS) return 'full'
  codes.value = [...codes.value, clean]
  persist(codes.value)
  return 'added'
}

export const removeCompare = (code: string) => {
  codes.value = codes.value.filter((c) => c !== code)
  persist(codes.value)
}

export const clearCompare = () => {
  codes.value = []
  persist(codes.value)
}

/** 以外部来源（URL ?items=）整体替换选中集合 */
export const setCompare = (raw: string[]) => {
  const next = dedupe(raw).slice(0, MAX_COMPARE_ITEMS)
  if (next.join(',') === codes.value.join(',')) return
  codes.value = next
  persist(codes.value)
}

export function useCompare() {
  return { codes, add: addCompare, remove: removeCompare, clear: clearCompare, set: setCompare }
}

export { MAX_COMPARE_ITEMS }
