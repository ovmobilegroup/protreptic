/**
 * useSeo.ts — Phase30-A1: 每个路由的 document.title / meta description / canonical / JSON-LD。
 *
 * 背景与约束（实测，别踩）：
 *  1) 预渲染的 1350 个页面（tools/prerender_routes.py）已经写好了该路由的
 *     title / description / canonical / og / JSON-LD。所以本模块不去重复注入结构化数据：
 *     落地页 head 里已有、且 url 与当前路由一致的 <script type="application/ld+json">
 *     直接沿用；只有 SPA 内部跳转让它过期（url 对不上）时才移除，换成我们的动态节点。
 *  2) 路由是 createWebHistory，真实地址形如 /protreptic/minds/H-WYM-001/（一律带尾斜杠，
 *     线上不带尾斜杠会 301）。canonical 必须用这个形式，不能用 index.unified.json 里那个
 *     哈希形式的 href（#/minds/...），那是死字段。
 *  3) title/description 一律用中文，与预渲染 head 保持一致：同一个 URL 无论是静态直连
 *     还是站内跳转进来，都必须看到同一份 head，否则就是两份内容打架。
 */
import type { RouteLocationNormalized, Router } from 'vue-router'

export const SEO_ORIGIN = 'https://ovmobilegroup.github.io'
export const SEO_SITE_NAME = 'Protreptic 思想典藏'
export const SEO_DEFAULT_TITLE = 'Protreptic · 思想典藏 — 历史人物思维模式库'
export const SEO_DEFAULT_DESCRIPTION =
  '2858 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。'

/** 本模块注入的动态 JSON-LD 节点的 id，用来和预渲染写死的那个区分开 */
const JSONLD_ID = 'pt-jsonld-dynamic'

/* ------------------------------------------------------------------ *
 * Phase30-A3 社交分享图 (og:image)
 * 路由 -> 图片路径的规则与 tools/og_image.py 的 og_rel_path() 同构:
 * 这是镜像实现, 两边必须同时改; 后端那侧由 tools/build_og_images.py 画图,
 * 构建期由 tools/apply_og_meta.py 写进每个预渲染页面的 head.
 *   ''            -> og/site.png
 *   daily         -> og/pages/daily.png          (figures/modes/templates/api 同理)
 *   minds/<code>  -> og/minds/<code>.png
 *   figures/<code>-> og/figures/<code>.png
 *   templates/<id>-> og/templates/<id>.png
 * 图片文件名用代码原值 (含空格的 code 在 URL 里由 encodeURIComponent 编码).
 * ------------------------------------------------------------------ */
const OG_DIR = 'og'
const OG_PAGE_SLUGS = ['daily', 'figures', 'modes', 'templates', 'api']

export function ogImagePath(path = ''): string {
  const clean = String(path || '').replace(/^\/+|\/+$/g, '')
  if (!clean) return `${OG_DIR}/site.png`
  const [head, ...rest] = clean.split('/')
  const tail = rest.join('/')
  if (!tail) return OG_PAGE_SLUGS.includes(head) ? `${OG_DIR}/pages/${head}.png` : `${OG_DIR}/site.png`
  if (tail.includes('/')) return `${OG_DIR}/site.png`
  if (head === 'minds') return `${OG_DIR}/minds/${tail}.png`
  if (head === 'figures') return `${OG_DIR}/figures/${tail}.png`
  if (head === 'templates') return `${OG_DIR}/templates/${tail}.png`
  return `${OG_DIR}/site.png`
}

/** 分享图绝对 URL: base 已规范化成 '/protreptic/', 每个路径段单独编码 */
export function ogImageUrl(path = ''): string {
  const base = import.meta.env.BASE_URL || '/'
  const encoded = ogImagePath(path).split('/').map((seg) => encodeURIComponent(seg)).join('/')
  return `${SEO_ORIGIN}${base}${encoded}`
}

export function ogImageAlt(title = ''): string {
  return title ? `${title} — ${SEO_SITE_NAME}` : `${SEO_SITE_NAME} — 历史人物思维模式库`
}

/** og:type: 人物档案用 profile, 模板用 article, 其余 website (与 tools/apply_og_meta.py 一致) */
export function ogTypeForPath(path = ''): string {
  const clean = String(path || '').replace(/^\/+|\/+$/g, '')
  if (clean.startsWith('minds/')) return 'profile'
  if (clean.startsWith('templates/')) return 'article'
  return 'website'
}

export type SeoKind = 'person' | 'scenario' | 'template' | 'static'
export type JsonLd = Record<string, unknown>

declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    description?: string
    /** 静态入口页（/figures /modes /templates /api）才声明；参数路由由视图在数据到位后自己设 */
    seoKind?: SeoKind
    /** Phase30-A4: catch-all 兜底页置真 —— 写 meta robots=noindex，并撤掉 canonical */
    noindex?: boolean
    noCanonical?: boolean
  }
}

export function truncateSeo(text: string | null | undefined, limit = 150): string {
  const clean = String(text ?? '').replace(/\s+/g, ' ').trim()
  return clean.length <= limit ? clean : clean.slice(0, limit - 1) + '…'
}

/** 站点绝对 URL：base 已被规范化成 '/protreptic/'，path 里有无首尾斜杠都能接受 */
export function siteUrl(path = ''): string {
  const base = import.meta.env.BASE_URL || '/'
  const clean = String(path).replace(/^\/+/, '').replace(/\/+$/, '')
  return clean ? `${SEO_ORIGIN}${base}${clean}/` : `${SEO_ORIGIN}${base}`
}

/** 与 tools/prerender_routes.py 的 render_head() 保持同形，避免静态/动态两套 schema 打架 */
export function buildJsonLd(
  kind: SeoKind,
  opts: { name: string; description: string; path: string; code?: string },
): JsonLd {
  const url = siteUrl(opts.path)
  const ld: JsonLd = {
    '@context': 'https://schema.org',
    '@type': kind === 'person' ? 'Person' : kind === 'template' ? 'Article' : 'CreativeWork',
    name: opts.name,
    description: truncateSeo(opts.description),
    url,
    isPartOf: { '@type': 'WebSite', name: SEO_SITE_NAME, url: siteUrl('') },
  }
  if (kind === 'person') {
    ld.identifier = opts.code || ''
    ld.alternateName = opts.code || ''
  } else if (kind === 'template') {
    ld.headline = opts.name
  } else if (kind === 'scenario') {
    ld.identifier = opts.code || ''
  }
  return ld
}

function upsertMeta(attr: 'name' | 'property', key: string, content: string): void {
  let el = document.head.querySelector<HTMLMetaElement>(`meta[${attr}="${key}"]`)
  if (!el) {
    el = document.createElement('meta')
    el.setAttribute(attr, key)
    document.head.appendChild(el)
  }
  el.setAttribute('content', content)
}

function upsertCanonical(href: string): void {
  let el = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]')
  if (!el) {
    el = document.createElement('link')
    el.setAttribute('rel', 'canonical')
    document.head.appendChild(el)
  }
  el.setAttribute('href', href)
}

function readJsonLd(script: HTMLScriptElement): JsonLd | null {
  try {
    const parsed = JSON.parse(script.textContent || 'null')
    return parsed && typeof parsed === 'object' ? (parsed as JsonLd) : null
  } catch {
    return null
  }
}

/** 是本站预渲染注入的那种节点吗？（带 url，且 isPartOf.name 是本站名） */
function isOwnStaticJsonLd(ld: JsonLd | null): boolean {
  if (!ld || typeof ld.url !== 'string') return false
  const part = ld.isPartOf as JsonLd | undefined
  return !!part && part.name === SEO_SITE_NAME
}

function syncStructuredData(url: string, ld: JsonLd | null): void {
  const head = document.head
  const scripts = Array.from(head.querySelectorAll<HTMLScriptElement>('script[type="application/ld+json"]'))
  const dynamic = scripts.find((s) => s.id === JSONLD_ID) ?? null

  for (const script of scripts) {
    if (script === dynamic) continue
    const parsed = readJsonLd(script)
    if (!isOwnStaticJsonLd(parsed)) continue // 不是我们注入的，不动它
    if (parsed?.url === url) {
      dynamic?.remove() // 落地页的静态结构化数据就是当前路由：沿用，不重复注入
      return
    }
    script.remove() // SPA 跳转后它已过期，留着会与当前路由的 schema 冲突
  }

  if (!ld) {
    dynamic?.remove()
    return
  }
  const node = dynamic ?? document.createElement('script')
  node.id = JSONLD_ID
  node.setAttribute('type', 'application/ld+json')
  node.textContent = JSON.stringify(ld)
  if (!dynamic) head.appendChild(node)
}

export interface SeoInput {
  title?: string
  description?: string
  /** 路由路径（不含 base），如 'minds/H-WYM-001'；省略则取当前地址 */
  path?: string
  jsonLd?: JsonLd | null
  /** 传 null 表示这一页不该有 canonical（兜底页用它撤掉上一条路由留下的 canonical） */
  canonical?: string | null
  /** 传 null / 省略表示移除 robots meta；兜底页传 'noindex,follow' */
  robots?: string | null
}

function currentPath(): string {
  const base = import.meta.env.BASE_URL || '/'
  const pathname = window.location.pathname
  return pathname.startsWith(base) ? pathname.slice(base.length) : pathname.replace(/^\/+/, '')
}

/** 视图/路由都可以调；重复调用是幂等的 */
export function setSeo(input: SeoInput = {}): void {
  const title = (input.title || '').trim()
  const url = siteUrl(input.path ?? currentPath())
  const description = truncateSeo(input.description || SEO_DEFAULT_DESCRIPTION, 150)

  document.title = title ? `${title} | ${SEO_SITE_NAME}` : SEO_DEFAULT_TITLE
  upsertMeta('name', 'description', description)
  upsertMeta('property', 'og:title', title || SEO_SITE_NAME)
  upsertMeta('property', 'og:description', description)
  upsertMeta('property', 'og:url', url)
  const ogPath = input.path ?? currentPath()
  const ogImage = ogImageUrl(ogPath)
  upsertMeta('property', 'og:type', ogTypeForPath(ogPath))
  upsertMeta('property', 'og:image', ogImage)
  upsertMeta('property', 'og:image:width', '1200')
  upsertMeta('property', 'og:image:height', '630')
  upsertMeta('property', 'og:image:alt', ogImageAlt(title))
  upsertMeta('name', 'twitter:card', 'summary_large_image')
  upsertMeta('name', 'twitter:image', ogImage)
  upsertMeta('name', 'twitter:image:alt', ogImageAlt(title))
  if (input.canonical === null) {
    document.head.querySelector('link[rel="canonical"]')?.remove()
  } else {
    upsertCanonical(input.canonical || url)
  }

  if (input.robots) upsertMeta('name', 'robots', input.robots)
  else document.head.querySelector('meta[name="robots"]')?.remove()

  syncStructuredData(url, input.jsonLd ?? null)
}

/** 路由级默认值：静态入口页带 JSON-LD；参数路由只设 head 骨架，等视图数据到位后再升级 */
export function applyRouteSeo(to: RouteLocationNormalized): void {
  // START_LOCATION（matched 为空）时路由还没解析出目标：拿它去改 head 会把路径算成站点根，
  // 从而把预渲染页面自带的、url 正确的静态 JSON-LD 当成"过期节点"删掉（实测踩过）。
  if (!to.matched.length) return
  const name = typeof to.name === 'string' ? to.name : ''
  const paramRoute = name === 'mind' || name === 'figure-detail' || name === 'template-detail'
  const kind = to.meta.seoKind
  const title = to.meta.title || ''
  const description = to.meta.description || SEO_DEFAULT_DESCRIPTION
  setSeo({
    title,
    description,
    path: to.path,
    jsonLd: !paramRoute && kind ? buildJsonLd(kind, { name: title, description, path: to.path }) : null,
    // 兜底页：无 canonical + noindex（预渲染的 1350 个收录路由都不带 noindex）
    canonical: to.meta.noCanonical ? null : undefined,
    robots: to.meta.noindex ? 'noindex,follow' : null,
  })
}

export function initSeo(router: Router): void {
  router.afterEach((to) => applyRouteSeo(to))
  applyRouteSeo(router.currentRoute.value)
}
