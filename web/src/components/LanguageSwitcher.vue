<script setup lang="ts">
import { useI18n } from '../composables/useI18n'

const { locale, setLocale, t } = useI18n()
</script>

<template>
  <div class="flex rounded-xl border border-white/10 bg-ink-950/50 p-1"
       role="group" :aria-label="t('语言', 'Language')">
    <button
      @click="setLocale('zh')"
      class="rounded-lg px-3 py-1.5 text-xs font-medium transition-all duration-300 ease-silk"
      :class="locale === 'zh'
        ? 'bg-gradient-to-b from-gold-400/90 to-gold-600 text-obsidian shadow-glow'
        : 'text-parchment/70 hover:text-parchment'"
      :aria-pressed="locale === 'zh'"
    >
      中文
    </button>
    <button
      @click="setLocale('en')"
      class="rounded-lg px-3 py-1.5 text-xs font-medium transition-all duration-300 ease-silk"
      :class="locale === 'en'
        ? 'bg-gradient-to-b from-gold-400/90 to-gold-600 text-obsidian shadow-glow'
        : 'text-parchment/70 hover:text-parchment'"
      :aria-pressed="locale === 'en'"
    >
      EN
    </button>
  </div>
</template>
