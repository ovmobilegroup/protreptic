<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'
import { useI18n } from './composables/useI18n'
import { useTheme } from './composables/useTheme'
import OfflineNotice from './components/OfflineNotice.vue'

const route = useRoute()
const { t } = useI18n()
const { theme, toggleTheme } = useTheme()

const links = computed(() => [
  { to: '/figures', zh: '历史人物库', en: 'Figures' },
  { to: '/modes', zh: '思维模式库', en: 'Modes' },
  { to: '/concepts', zh: '概念索引', en: 'Concepts' },
  { to: '/graph', zh: '关系图谱', en: 'Graph' },
  { to: '/templates', zh: '复盘模板', en: 'Templates' },
  { to: '/api', zh: 'API 文档', en: 'API' },
])

const isActive = (to: string) => route.path.startsWith(to)
</script>

<template>
  <div class="relative flex min-h-screen flex-col">
    <!-- 背景光晕 -->
    <div aria-hidden="true" class="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      <div class="absolute -top-40 left-1/2 h-[520px] w-[820px] -translate-x-1/2 rounded-full
                  bg-gold-500/10 blur-[120px] animate-glow-pulse"></div>
      <div class="absolute top-1/3 -right-40 h-[420px] w-[520px] rounded-full
                  bg-jade-400/10 blur-[130px]"></div>
      <div class="absolute bottom-0 left-1/4 h-[360px] w-[520px] rounded-full
                  bg-gold-700/10 blur-[130px]"></div>
    </div>

    <!-- 顶栏 -->
    <header class="sticky top-0 z-40 border-b border-white/10 bg-ink-950/70 backdrop-blur-xl">
      <nav class="pt-container" aria-label="主导航">
        <div class="flex h-16 items-center justify-between gap-4">
          <RouterLink to="/figures" class="group flex items-center gap-3 shrink-0">
            <span class="relative grid h-9 w-9 place-items-center rounded-xl border border-gold-500/40
                         bg-gradient-to-br from-gold-500/25 to-transparent text-lg
                         transition-transform duration-500 ease-silk group-hover:scale-105">
              🧭
            </span>
            <span class="flex flex-col leading-none">
              <span class="font-display text-lg font-bold tracking-wide text-parchment">Protreptic</span>
              <span class="pt-code mt-0.5 text-[10px]">思想典藏 · ARCHIVE OF MINDS</span>
            </span>
          </RouterLink>

          <div class="hidden items-center gap-1 md:flex">
            <RouterLink
              v-for="l in links" :key="l.to" :to="l.to"
              class="relative rounded-lg px-3.5 py-2 text-sm font-medium transition-colors duration-300"
              :class="isActive(l.to) ? 'text-gold-300' : 'text-parchment/60 hover:text-parchment'"
            >
              {{ t(l.zh, l.en) }}
              <span v-if="isActive(l.to)"
                    class="absolute inset-x-3 -bottom-px h-px bg-gradient-to-r from-transparent via-gold-400 to-transparent"></span>
            </RouterLink>
          </div>

          <div class="flex items-center gap-2 sm:gap-3">
            <button
              @click="toggleTheme"
              :title="theme === 'dark' ? t('切换到浅色模式', 'Switch to light mode') : t('切换到深色模式', 'Switch to dark mode')"
              :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
              class="grid h-9 w-9 place-items-center rounded-xl border border-white/10 bg-white/[.04]
                     text-parchment/70 transition-all duration-300 ease-silk
                     hover:border-gold-500/45 hover:text-gold-300 hover:bg-gold-500/10"
            >
              <svg v-if="theme === 'dark'" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 3v2m0 14v2M5.6 5.6l1.4 1.4m10 10l1.4 1.4M3 12h2m14 0h2M5.6 18.4l1.4-1.4m10-10l1.4-1.4M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z" />
              </svg>
            </button>
            <LanguageSwitcher />
          </div>
        </div>

        <!-- 移动端导航 -->
        <div class="flex gap-1 overflow-x-auto pb-2 md:hidden">
          <RouterLink
            v-for="l in links" :key="l.to" :to="l.to"
            class="whitespace-nowrap rounded-lg px-3 py-1.5 text-xs font-medium transition-colors"
            :class="isActive(l.to) ? 'bg-gold-500/[0.12] text-gold-300' : 'text-parchment/55 hover:text-parchment'"
          >
            {{ t(l.zh, l.en) }}
          </RouterLink>
        </div>
      </nav>
    </header>

    <main class="flex-1">
      <RouterView v-slot="{ Component }">
        <transition
          mode="out-in"
          enter-active-class="transition duration-300 ease-silk"
          enter-from-class="opacity-0 translate-y-2"
          leave-active-class="transition duration-150 ease-in"
          leave-to-class="opacity-0"
        >
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>

    <footer class="mt-20 border-t border-white/10 bg-ink-950/60">
      <div class="pt-container py-10">
        <div class="pt-hairline mb-8"></div>
        <div class="flex flex-col items-center gap-3 text-center">
          <p class="font-display text-sm text-parchment/70">
            以史为鉴，知兴替；以人为鉴，明得失。
          </p>
          <p class="text-xs text-parchment/40">
            Protreptic · 2868 条思维模式 × 284 位历史人物 · 中英双语
          </p>
          <div class="mt-2 flex items-center gap-3 text-xs text-parchment/45">
            <a href="https://github.com/ovmobilegroup/protreptic" target="_blank" rel="noopener"
               class="rounded-lg px-3 py-1.5 transition-colors hover:bg-white/5 hover:text-gold-300">GitHub</a>
            <span class="text-parchment/20">·</span>
            <span>MIT License</span>
          </div>
        </div>
      </div>
    </footer>

    <!-- Phase30-A4: 断网提示 / 新版本提示（右下角浮层，SW 不支持时不渲染） -->
    <OfflineNotice />
  </div>
</template>
