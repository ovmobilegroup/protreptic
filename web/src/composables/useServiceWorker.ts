/**
 * useServiceWorker.ts — Phase30-A4: SW 注册 / 更新 / 离线状态 / 断网提示数据源。
 *
 * 契约（与 tools/build_sw.py 注入的 dist/sw.js 一致）:
 *   - 注册地址是 BASE_URL 下的 sw.js；线上 BASE_URL 就是 /protreptic/，
 *     因此 scope 天然落在 /protreptic/。Pages 不能下发自定义响应头，
 *     这已经是能拿到的最大范围。
 *   - 开发模式默认不注册（dev server 每次都是新资源，注册只会拖慢调试）；
 *     需要本地验证时用 VITE_SW=on 打开。
 *   - 更新策略：SW 安装时 skipWaiting、激活时 clients.claim，新版立刻接管。
 *     页面不自动 reload（会把用户正在填的内容丢掉），而是把 updateReady
 *     置真，由 OfflineNotice 提示「已更新，点此刷新」。
 *
 * 状态是模块级单例（多个组件共享同一份），通过 useServiceWorker() 读取。
 */
import { readonly, ref } from 'vue'

export type ServiceWorkerState =
  | 'unsupported' // 浏览器没有 SW（或非 http(s) 环境）
  | 'idle'
  | 'registering'
  | 'ready'
  | 'failed'

const BASE = import.meta.env.BASE_URL || '/'
const SW_URL = `${BASE}sw.js`

const state = ref<ServiceWorkerState>('idle')
const version = ref('')
const errorMessage = ref('')
const updateReady = ref(false)
const offline = ref(typeof navigator !== 'undefined' ? !navigator.onLine : false)
const online = ref(!offline.value)
const warmed = ref<{ done: number; total: number } | null>(null)
const warmFailed = ref<string[]>([])

let registration: ServiceWorkerRegistration | null = null
let hadController = false
let initialized = false

const isSupported = (): boolean => {
  if (typeof navigator === 'undefined' || !('serviceWorker' in navigator)) return false
  if (typeof window === 'undefined') return false
  return window.location.protocol === 'http:' || window.location.protocol === 'https:'
}

/** 开发模式默认不注册；VITE_SW=on 强制打开（用于本地验证离线行为） */
const shouldRegister = (): boolean => {
  const flag = String(import.meta.env.VITE_SW ?? '').toLowerCase()
  if (flag === 'on' || flag === 'true' || flag === '1') return true
  if (flag === 'off' || flag === 'false' || flag === '0') return false
  return import.meta.env.PROD
}

const trackConnectivity = (): void => {
  if (typeof window === 'undefined') return
  const sync = () => {
    offline.value = !navigator.onLine
    online.value = navigator.onLine
    if (offline.value) askWarmStatus()
  }
  window.addEventListener('online', sync)
  window.addEventListener('offline', sync)
  sync()
}

const handleMessage = (event: MessageEvent): void => {
  const data = (event.data || {}) as Record<string, unknown>
  if (data.type === 'PROTREPTIC_WARMED') {
    warmed.value = {
      done: Number(data.warmed ?? 0),
      total: Number(data.total ?? 0),
    }
    warmFailed.value = Array.isArray(data.failed) ? data.failed.map(String) : []
  } else if (data.type === 'PROTREPTIC_VERSION') {
    version.value = String(data.version ?? '')
  }
}

const postToSw = (message: Record<string, unknown>): void => {
  const target = registration?.active ?? navigator.serviceWorker.controller
  try {
    target?.postMessage(message)
  } catch {
    /* SW 刚被回收，忽略 */
  }
}

const askVersion = (reg: ServiceWorkerRegistration | null): void => {
  registration = reg ?? registration
  postToSw({ type: 'VERSION' })
}

/** 离线提示里要如实报出「本地缓存了多少模式分片」，按需向 SW 要一次统计 */
const askWarmStatus = (): void => postToSw({ type: 'WARM_STATUS' })

/** 注册 SW。幂等：重复调用只生效一次。返回是否注册成功。 */
export async function initServiceWorker(): Promise<boolean> {
  if (initialized) return state.value === 'ready'
  initialized = true

  trackConnectivity()

  if (!isSupported()) {
    state.value = 'unsupported'
    return false
  }
  navigator.serviceWorker.addEventListener('message', handleMessage)

  if (!shouldRegister()) {
    state.value = 'idle'
    return false
  }

  hadController = !!navigator.serviceWorker.controller
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    // 只有在原先已被某个 SW 控制的前提下才算升级；首次注册不算
    if (hadController) updateReady.value = true
    hadController = true
    askVersion(registration)
  })

  state.value = 'registering'
  try {
    registration = await navigator.serviceWorker.register(SW_URL, {
      scope: BASE,
      updateViaCache: 'none',
    })
    registration.addEventListener('updatefound', () => {
      const installing = registration?.installing
      if (!installing) return
      installing.addEventListener('statechange', () => {
        if (installing.state === 'installed' && navigator.serviceWorker.controller) {
          updateReady.value = true
        }
      })
    })
    await navigator.serviceWorker.ready
    state.value = 'ready'
    askVersion(registration)
    askWarmStatus()
    return true
  } catch (err) {
    state.value = 'failed'
    errorMessage.value = err instanceof Error ? err.message : String(err)
    return false
  }
}

/** 主动检查更新（例如标签页重新可见时） */
export async function checkForUpdate(): Promise<void> {
  try {
    await registration?.update()
  } catch {
    /* 离线时 update() 会抛，忽略 */
  }
}

/** 刷新以应用新版本（由用户点击触发，绝不自动 reload） */
export function applyUpdate(): void {
  window.location.reload()
}

export function useServiceWorker() {
  return {
    state: readonly(state),
    version: readonly(version),
    errorMessage: readonly(errorMessage),
    updateReady: readonly(updateReady),
    offline: readonly(offline),
    online: readonly(online),
    warmed: readonly(warmed),
    warmFailed: readonly(warmFailed),
    applyUpdate,
    checkForUpdate,
  }
}
