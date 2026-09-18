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

const apply = (t: Theme) => {
  if (typeof document === 'undefined') return
  const root = document.documentElement
  if (t === 'light') root.setAttribute('data-theme', 'light')
  else root.removeAttribute('data-theme')
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
