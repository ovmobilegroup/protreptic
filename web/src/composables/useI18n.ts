import { ref, computed } from 'vue'

const locale = ref<'zh' | 'en'>('zh')

export function useI18n() {
  const setLocale = (next: 'zh' | 'en') => {
    locale.value = next
    try {
      localStorage.setItem('protreptic_locale', next)
    } catch { /* 隐私模式下忽略 */ }
  }

  const toggleLocale = () => setLocale(locale.value === 'zh' ? 'en' : 'zh')

  const initLocale = () => {
    try {
      const saved = localStorage.getItem('protreptic_locale') as 'zh' | 'en' | null
      if (saved === 'zh' || saved === 'en') locale.value = saved
    } catch { /* 忽略 */ }
  }

  const t = (zh: string, en: string): string => (locale.value === 'zh' ? zh : en)

  return {
    locale: computed(() => locale.value),
    setLocale,
    toggleLocale,
    initLocale,
    t,
  }
}
