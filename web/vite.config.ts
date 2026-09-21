import { defineConfig, loadEnv, type Plugin } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'
import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { resolve } from 'node:path'

// 部署目标是 GitHub Pages 项目站点 /protreptic/, 子路径统一由 base 决定,
// 路由 createWebHistory(import.meta.env.BASE_URL) 与静态数据路径
// import.meta.env.BASE_URL + 'data/' 都跟着它走.
// 根路径部署 (docker/Dockerfile.web + nginx) 用 VITE_BASE=/ 覆盖.
const BASE_PATH = process.env.VITE_BASE || '/protreptic/'

/** 访问统计开关的落点文件 (提交入库, 一行激活): 见 docs/community/analytics_setup.md */
const GOATCOUNTER_FILE = fileURLToPath(new URL('./goatcounter.json', import.meta.url))

/**
 * GitHub Pages 没有 SPA rewrite, 直接访问 /protreptic/figures/H-ZL-08 会落到站点根
 * 404.html. 把构建产物 index.html 复制一份成 404.html, 深链即可拿到完全相同的 SPA
 * 外壳, 资源引用已是 /protreptic/assets/... 绝对路径, 可直接使用.
 * 用 closeBundle 而非 generateBundle, 保证 vite:build-html 已写出 index.html,
 * 不依赖插件之间的执行顺序.
 */
function spaFallback404(outDir: string): Plugin {
  return {
    name: 'spa-fallback-404',
    apply: 'build',
    closeBundle() {
      const index = resolve(outDir, 'index.html')
      if (!existsSync(index)) {
        this.warn('404.html fallback not generated: index.html missing at ' + index)
        return
      }
      const html = readFileSync(index)
      writeFileSync(resolve(outDir, '404.html'), html)
    },
  }
}

/**
 * 读 goatcounter.json 的 code 字段。文件缺失或 JSON 坏了都当成「未接入」处理:
 * 统计是附加能力, 不该让整站构建挂掉。
 */
function goatcounterCodeFromFile(): string {
  try {
    const cfg = JSON.parse(readFileSync(GOATCOUNTER_FILE, 'utf8')) as { code?: unknown }
    return String(cfg.code ?? '').trim()
  } catch {
    return ''
  }
}

/**
 * Phase45-A: 访问统计 (GoatCounter) 构建期开关 —— 卡片 t_eb3de8e7.
 *
 * 纪律:
 *   * 有 code  -> 往 <head> 注入一行官方 count.js, data-goatcounter 指向该站点;
 *   * 无 code (缺省) -> 一个字节都不注入. 不许留 404 脚本, 不许留占位域名
 *     (Phase30-C3 的 YOUR_INSTANCE 占位符就是这么被撤掉的, 别再来一次).
 *
 * 为什么不用 Vite 的 %VITE_XXX% HTML 占位符: %VAR% 是无条件文本替换, 变量为空时
 *   会留下 `https://.goatcounter.com/count` 这种坏 URL —— 恰好是上面禁止的占位/坏脚本.
 *   条件注入只能自己写。
 *
 * 深链为什么不另改一处: tools/prerender_routes.py 的预渲染页是以构建产物
 *   dist/index.html 为壳、只改 head 里几行再写出的, 所以本注入会自动出现在每个
 *   预渲染深链页里 (首页 / 404.html / 深链 三者同源, 不会只有首页有脚本).
 *
 * 取数优先级: 环境变量 VITE_GOATCOUNTER_CODE (CI / 命令行) > goatcounter.json 的 code.
 *   本地验证: VITE_GOATCOUNTER_CODE=abc123 npm run build
 */
function goatcounterHead(code: string): Plugin {
  return {
    name: 'goatcounter-head',
    apply: 'build',
    transformIndexHtml(html: string) {
      if (!code) return html
      const tag =
        `<script data-goatcounter="https://${code}.goatcounter.com/count" ` +
        `async src="${BASE_PATH}count.js"></script>`  // 自托管(ISC)，绕过对 gc.zgo.at 的拦截
      if (!html.includes('</head>')) {
        throw new Error('[goatcounter] web/index.html 里找不到 </head>, 注入位置无法确定')
      }
      // 必须写成 <script ...></script>: 自闭合 <script .../> 会被 HTML 解析器当成
      // raw text 起始标签, 其后的标签全被吞成脚本文本 (Phase30-A3 踩过, 整页空白).
      return html.replace('</head>', `    ${tag}\n  </head>`)
    },
  }
}

export default defineConfig(({ mode }) => {
  // prefix 传 '' 才能读到非 VITE_ 前缀的变量; process.env 覆盖 .env 文件,
  // 因此 CI / 命令行 `VITE_GOATCOUNTER_CODE=xxx npm run build` 可以直接压过文件里的值.
  const env = { ...loadEnv(mode, process.cwd(), ''), ...process.env }
  const goatcounterCode = String(env.VITE_GOATCOUNTER_CODE || '').trim() || goatcounterCodeFromFile()

  return {
    base: BASE_PATH,
    plugins: [vue(), goatcounterHead(goatcounterCode), spaFallback404('dist')],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      port: 3000,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        },
      },
    },
  }
})
