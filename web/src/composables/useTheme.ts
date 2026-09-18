import { ref, watch } from 'vue'

export type Theme = 'dark' | 'light'

const STORAGE_KEY = 'protreptic-theme'

const read = (): Theme => {
  if (typeof window === 'undefined') return 'dark'
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved === 'light' || saved === 'dark') return saved
  } catch { /* ignore */ }
  return 'dark'
}

const theme = ref<Theme>(read())

/**
 * Phase30-A4: 安装成 PWA 之后，浏览器窗口/状态栏用的是这几个值，也要跟着主题走。
 * 两个 manifest 只有 theme_color / background_color 不同（静态托管没有服务端，
 * 换肤只能靠切换 <link rel="manifest">），meta theme-color 则由这里同步。
 */
const THEME_COLOR: Record<Theme, string> = { dark: '#04060c', light: '#f8f5f0' }
const MANIFEST_FILE: Record<Theme, string> = {
  dark: 'manifest.webmanifest',
  light: 'manifest-light.webmanifest',
}

const apply = (t: Theme) => {
  if (typeof document === 'undefined') return
  const root = document.documentElement
  if (t === 'light') root.setAttribute('data-theme', 'light')
  else root.removeAttribute('data-theme')

  const meta = document.getElementById('pt-theme-color')
  if (meta) meta.setAttribute('content', THEME_COLOR[t])

  const link = document.getElementById('pt-manifest')
  if (link) {
    const base = (import.meta.env.BASE_URL || '/')
    link.setAttribute('href', `${base}${MANIFEST_FILE[t]}`)
  }
}

apply(theme.value)

watch(theme, (t) => {
  apply(t)
  try { localStorage.setItem(STORAGE_KEY, t) } catch { /* ignore */ }
})

export function useTheme() {
  const toggleTheme = () => { theme.value = theme.value === 'dark' ? 'light' : 'dark' }
  const setTheme = (t: Theme) => { theme.value = t }
  return { theme, toggleTheme, setTheme }
}
