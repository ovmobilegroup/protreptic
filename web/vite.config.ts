import { defineConfig, type Plugin } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'
import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { resolve } from 'node:path'

// 部署目标是 GitHub Pages 项目站点 /protreptic/, 子路径统一由 base 决定,
// 路由 createWebHistory(import.meta.env.BASE_URL) 与静态数据路径
// import.meta.env.BASE_URL + 'data/' 都跟着它走.
// 根路径部署 (docker/Dockerfile.web + nginx) 用 VITE_BASE=/ 覆盖.
const BASE_PATH = process.env.VITE_BASE || '/protreptic/'

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

export default defineConfig({
  base: BASE_PATH,
  plugins: [vue(), spaFallback404('dist')],
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
})
