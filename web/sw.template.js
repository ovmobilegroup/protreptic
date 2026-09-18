/*!
 * Protreptic service worker (Phase30-A4) — 离线可用的静态知识库外壳.
 *
 * 这是模板, 不要直接改 web/dist/sw.js: 构建期由 tools/build_sw.py 注入
 * BUILD_ID / DATA_REV / 预缓存清单, 产物写到 web/dist/sw.js (= 线上 /protreptic/sw.js).
 * 线上 scope 就是 /protreptic/ (Pages 不能下发 Service-Worker-Allowed 响应头).
 *
 * 缓存契约 (与 docs/architecture/web_p0_architecture.md 第 3 节一致):
 *   protreptic-shell-<BUILD_ID>   index.html / assets/* / favicon / manifest / icons / templates/*.md
 *                                 — cache-first
 *   protreptic-data-<DATA_REV>    data/** — cache-first, install 期尽力预缓存三件索引,
 *                                 激活后后台预热 modes/index-0..7.json
 *   activate 时删掉所有 protreptic- 前缀但不在当前名单里的缓存 —— 升级不会卡在旧缓存.
 *
 * 导航 (mode === 'navigate'): network-first.
 *   在线: 原样返回, 包括 Pages 对未收录路径的 404 (不能把真 404 洗成 200).
 *   离线/超时: 返回缓存的通用 index.html 并**构造 200** —— 地址栏 URL 不变,
 *   Vue Router 按真实路径渲染, 数据再走缓存 —— 所以不用预缓存 1350 个预渲染页.
 */
'use strict'

const BUILD_ID = '__BUILD_ID__'
const DATA_REV = '__DATA_REV__'
const BASE = '__BASE__'
const SHELL_ENTRY = '__SHELL_ENTRY__'
const PRECACHE_CRITICAL = __PRECACHE_CRITICAL__
const PRECACHE_SHELL_SOFT = __PRECACHE_SHELL_SOFT__
const PRECACHE_DATA = __PRECACHE_DATA__
const WARM_URLS = __WARM_URLS__

const CACHE_PREFIX = 'protreptic-'
const SHELL_CACHE = CACHE_PREFIX + 'shell-' + BUILD_ID
const DATA_CACHE = CACHE_PREFIX + 'data-' + DATA_REV
const KEEP = [SHELL_CACHE, DATA_CACHE]
const VERSION = BUILD_ID + '.' + DATA_REV

const NAV_TIMEOUT_MS = 4000

// ------------------------------------------------------------------ 工具

function log(...args) {
  console.log('[sw]', ...args)
}

async function fetchFresh(url) {
  // cache: 'reload' 绕过 HTTP 缓存, 预缓存/预热拿到的必须是本次构建的产物
  return fetch(new Request(url, { cache: 'reload', credentials: 'same-origin' }))
}

async function fetchWithTimeout(request, ms) {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), ms)
  try {
    return await fetch(request, { signal: controller.signal })
  } finally {
    clearTimeout(timer)
  }
}

function broadcast(message) {
  return self.clients
    .matchAll({ type: 'window', includeUncontrolled: true })
    .then((clients) => clients.forEach((client) => {
      try { client.postMessage(message) } catch (err) { /* 客户端已关闭 */ }
    }))
    .catch(() => {})
}

function offlinePage(url) {
  const safe = String(url).replace(/[<>&"]/g, '')
  return '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<title>暂不可用 · Protreptic</title><style>' +
    'html,body{margin:0;height:100%;background:#04060c;color:#f3ece0;' +
    'font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;' +
    'display:grid;place-items:center;text-align:center}' +
    'main{max-width:32rem;padding:2rem}' +
    'h1{font-size:1.25rem;color:#f0d79f;margin:0 0 .75rem}' +
    'p{color:rgba(243,236,224,.65);line-height:1.7;font-size:.9rem;margin:.4rem 0}' +
    'code{color:rgba(143,240,221,.8);font-size:.8rem}' +
    'a{color:#f0d79f;text-decoration:none;border-bottom:1px solid rgba(212,162,76,.5)}' +
    '</style></head><body><main><h1>这一页还没有缓存</h1>' +
    '<p>当前离线，且该页面不在本地缓存中。</p>' +
    '<p><a href="' + BASE + 'figures">回到历史人物库</a></p>' +
    '<p><code>' + safe + '</code></p></main></body></html>'
}

// ------------------------------------------------------------------ 策略

async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName)
  const hit = await cache.match(request, { ignoreSearch: true })
  if (hit) return hit
  const response = await fetch(request)
  if (response && response.ok && response.type === 'basic') {
    try { await cache.put(request, response.clone()) } catch (err) { /* 配额满等, 不影响本次响应 */ }
  }
  return response
}

async function navigateStrategy(request) {
  try {
    const response = await fetchWithTimeout(request, NAV_TIMEOUT_MS)
    if (response) return response // 含 Pages 的真 404, 不洗成 200
  } catch (err) {
    log('navigation network failed, falling back to shell:', request.url, String(err))
  }
  const cache = await caches.open(SHELL_CACHE)
  const shell = await cache.match(SHELL_ENTRY)
  if (shell) {
    const body = await shell.blob()
    return new Response(body, {
      status: 200,
      statusText: 'OK',
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'no-store',
        'X-Protreptic-Shell': VERSION,
      },
    })
  }
  return new Response(offlinePage(request.url), {
    status: 503,
    statusText: 'Offline and not cached',
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' },
  })
}

self.addEventListener('fetch', (event) => {
  const request = event.request
  if (request.method !== 'GET') return
  const url = new URL(request.url)
  if (url.origin !== self.location.origin) return
  if (!url.pathname.startsWith(BASE)) return
  if (request.headers.get('range')) return // Range 请求（断点续传/媒体）不拦截

  if (request.mode === 'navigate') {
    event.respondWith(navigateStrategy(request))
    return
  }
  const relative = url.pathname.slice(BASE.length)
  if (relative.startsWith('data/')) {
    event.respondWith(cacheFirst(request, DATA_CACHE))
    return
  }
  event.respondWith(cacheFirst(request, SHELL_CACHE))
})

// ------------------------------------------------------------------ 生命周期

async function precache(cache, urls, critical) {
  const failed = []
  for (const url of urls) {
    try {
      const response = await fetchFresh(url)
      if (!response.ok) throw new Error('HTTP ' + response.status)
      await cache.put(url, response)
    } catch (err) {
      failed.push(url + ' (' + String(err) + ')')
    }
  }
  if (critical && failed.length) {
    throw new Error('关键预缓存失败: ' + failed.join(', '))
  }
  return failed
}

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const shell = await caches.open(SHELL_CACHE)
    await precache(shell, PRECACHE_CRITICAL, true)   // 外壳缺一块 = 安装失败
    // 7 个复盘模板 markdown（合计约 104 KB raw）也属于「外壳」级别的常驻内容
    const shellSoftFailed = await precache(shell, PRECACHE_SHELL_SOFT, false)
    if (shellSoftFailed.length) log('模板预缓存部分失败(不阻塞安装):', shellSoftFailed)
    // 索引三件套属于 data/**，必须落在 DATA_CACHE：页面请求走的是
    // cacheFirst(DATA_CACHE)，放进 shell 缓存等于装了却用不上（实测 /figures 离线空列表）。
    const data = await caches.open(DATA_CACHE)
    const softFailed = await precache(data, PRECACHE_DATA, false) // 索引类尽力而为
    if (softFailed.length) log('索引预缓存部分失败(不阻塞安装):', softFailed)
    log('installed', VERSION, 'shell=' + PRECACHE_CRITICAL.length,
        'templates=' + PRECACHE_SHELL_SOFT.length, 'data=' + PRECACHE_DATA.length)
    await self.skipWaiting() // 新版本立刻接管, 避免旧 SW 长期占位
  })())
})

async function warmData() {
  const cache = await caches.open(DATA_CACHE)
  const queue = WARM_URLS.slice()
  const failed = []
  let ok = 0
  const worker = async () => {
    while (queue.length) {
      const url = queue.shift()
      try {
        const hit = await cache.match(url)
        if (hit) { ok += 1; continue }
        const response = await fetchFresh(url)
        if (!response.ok) throw new Error('HTTP ' + response.status)
        await cache.put(url, response)
        ok += 1
      } catch (err) {
        failed.push(url)
      }
    }
  }
  await Promise.all([worker(), worker(), worker()])
  return { ok, failed }
}

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const names = await caches.keys()
    const stale = names.filter((name) => name.startsWith(CACHE_PREFIX) && KEEP.indexOf(name) === -1)
    await Promise.all(stale.map((name) => {
      log('删除旧缓存', name)
      return caches.delete(name)
    }))
    await self.clients.claim()
    const warmed = await warmData()
    log('activated', VERSION, 'caches=' + KEEP.join(','), 'warm=' + warmed.ok + '/' + WARM_URLS.length)
    broadcast({
      type: 'PROTREPTIC_WARMED',
      version: VERSION,
      warmed: warmed.ok,
      failed: warmed.failed,
      total: WARM_URLS.length,
    })
  })())
})

self.addEventListener('message', (event) => {
  const data = event.data || {}
  const reply = (payload) => {
    try { (event.source || event.target).postMessage(payload) } catch (err) { /* ignore */ }
  }
  if (data.type === 'SKIP_WAITING') {
    self.skipWaiting()
    return
  }
  if (data.type === 'WARM') {
    event.waitUntil(warmData().then((result) => reply({
      type: 'PROTREPTIC_WARMED', version: VERSION,
      warmed: result.ok, failed: result.failed, total: WARM_URLS.length,
    })))
    return
  }
  if (data.type === 'WARM_STATUS') {
    // 页面想知道「本地已经缓存了多少模式分片」时按需回报（激活期的广播只覆盖当时在线的页面）
    event.waitUntil((async () => {
      const cache = await caches.open(DATA_CACHE)
      let done = 0
      for (const url of WARM_URLS) {
        if (await cache.match(url)) done += 1
      }
      reply({
        type: 'PROTREPTIC_WARMED', version: VERSION,
        warmed: done, failed: [], total: WARM_URLS.length,
      })
    })())
    return
  }
  if (data.type === 'VERSION') {
    reply({
      type: 'PROTREPTIC_VERSION',
      version: VERSION,
      buildId: BUILD_ID,
      dataRev: DATA_REV,
      base: BASE,
      shellCache: SHELL_CACHE,
      dataCache: DATA_CACHE,
      shell: PRECACHE_CRITICAL.length,
      shellSoft: PRECACHE_SHELL_SOFT.length,
      data: PRECACHE_DATA.length,
      warm: WARM_URLS.length,
    })
  }
})
