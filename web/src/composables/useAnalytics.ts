/**
 * useAnalytics.ts -- Phase45-A: GoatCounter 访问统计的 SPA 路由追踪。
 *
 * 背景与约束 (实测口径, 别踩):
 *  1) 统计脚本由构建期开关注入: web/vite.config.ts 的 goatcounter-head 插件。
 *     VITE_GOATCOUNTER_CODE 有值 -> <head> 里出现一行
 *     script data-goatcounter="https://<code>.goatcounter.com/count" async
 *     src="https://gc.zgo.at/count.js";
 *     缺省 (空值) -> 一个字节都不注入, 站点保持 inert 状态。
 *  2) count.js 只在首次载入上报一次; 本站是 history 模式 SPA, index.html 不在
 *     路由之间重载, 站内跳转必须自己补报, 否则深链页只算进入时那一条。
 *  3) 未注入时不得报错: 这里只读 DOM 上有没有那个 script 标签 / window.goatcounter,
 *     不假设它一定存在, 也不会为它加载任何东西。
 *  4) 首屏不要重复计数: 载入那一次已经由 count.js 计入, 所以本模块跳过第一次
 *     afterEach 且目标路径就是进入时那个 pathname 的那次上报。
 *
 * 与 SEO 的顺序: main.ts 里 initSeo(router) 先注册 afterEach, 本模块后注册 --
 *   vue-router 的 afterEach 按注册顺序执行, 因此上报时 document.title 已经是本路由的
 *   标题 (useSeo 的 applyRouteSeo 刚写过), 上报的 title 不会串页。
 *   不要把 initAnalytics 挪到 initSeo 之前。
 */
import type { Router } from 'vue-router'

/** GoatCounter count.js 暴露的最小接口, 本模块只用到 count */
interface GoatCounter {
  count?: (vars?: { path?: string; title?: string }) => void
}

/** 注入标记属性: 与 vite.config.ts 生成的标签严格同名, 是是否已接入的唯一判据 */
const SCRIPT_SELECTOR = 'script[data-goatcounter]'

/** 页面里有没有统计脚本; 缺省构建为 false, 此时本模块全程静默 */
export function hasAnalytics(): boolean {
  if (typeof document === 'undefined') return false
  return !!document.querySelector(SCRIPT_SELECTOR)
}

function goatcounter(): GoatCounter | undefined {
  if (typeof window === 'undefined') return undefined
  return (window as unknown as { goatcounter?: GoatCounter }).goatcounter
}

/**
 * 上报一次站内跳转。仅当脚本已注入、且 count.js 已就绪时才会发出;
 * 就绪前发生的跳转会被安静跳过: 宁可少一条, 也不要报错或伪造计数。
 */
function report(pathname: string): void {
  const gc = goatcounter()
  if (typeof gc?.count !== 'function') return
  gc.count({ path: pathname, title: document.title })
}

export function initAnalytics(router: Router): void {
  if (!hasAnalytics()) return

  // 进入本站时的地址: count.js 已经为它计过一次, 不能重复计。
  const entryPath = typeof window === 'undefined' ? '' : window.location.pathname
  let entryHandled = false

  router.afterEach((to) => {
    // START_LOCATION (路由尚未解析) 时 matched 为空, 拿它上报会把路径算成站点根,
    // useSeo.applyRouteSeo 里为同一个坑写过注释。
    if (!to.matched.length) return

    const pathname = window.location.pathname
    if (!entryHandled) {
      entryHandled = true
      // 进入时那一次已由 count.js 计入。只有载入后地址立刻被路由改写 (例如 / 重定向到
      // /figures) 才补报: 那是用户实际停留的另一个地址。
      if (pathname === entryPath) return
    }
    report(pathname)
  })
}
