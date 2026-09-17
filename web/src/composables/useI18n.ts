import { ref, computed } from 'vue'

const locale = ref<'zh' | 'en'>('zh')

export function useI18n() {
  const toggleLocale = () => {
    locale.value = locale.value === 'zh' ? 'en' : 'zh'
    localStorage.setItem('protreptic_locale', locale.value)
  }

  const initLocale = () => {
    const saved = localStorage.getItem('protreptic_locale') as 'zh' | 'en' | null
    if (saved) locale.value = saved
  }

  const t = (zh: string, en: string): string => {
    return locale.value === 'zh' ? zh : en
  }

  return {
    locale: computed(() => locale.value),
    toggleLocale,
    initLocale,
    t,
  }
}