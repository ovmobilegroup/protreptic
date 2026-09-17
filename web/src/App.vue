<script setup lang="ts">
import { RouterView } from 'vue-router'
import LanguageSwitcher from './components/LanguageSwitcher.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <header class="bg-white border-b border-gray-200 sticky top-0 z-40">
      <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" aria-label="Main navigation">
        <div class="flex h-16 items-center justify-between">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center space-x-2">
              <span class="text-2xl">🧭</span>
              <span class="text-xl font-bold text-indigo-700">Protreptic</span>
            </router-link>
          </div>
          
          <div class="hidden md:flex md:items-center md:space-x-8">
            <router-link 
              to="/figures" 
              class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              历史人物库
            </router-link>
            <router-link 
              to="/modes" 
              class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              思维模式库
            </router-link>
            <router-link 
              to="/templates" 
              class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              复盘模板
            </router-link>
            <router-link 
              to="/api" 
              class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              API 文档
            </router-link>
          </div>

          <div class="flex items-center space-x-4">
            <LanguageSwitcher />
          </div>
        </div>
      </nav>
    </header>

    <main class="flex-1">
      <RouterView />
    </main>

    <footer class="bg-gray-900 text-gray-400 py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p>Protreptic v2.1.0 — 以史为鉴，知兴替；以人为鉴，明得失。</p>
        <p class="mt-2 text-sm">
          <a href="https://github.com/ovmobilegroup/protreptic" class="hover:text-white" target="_blank" rel="noopener">
            GitHub
          </a>
          · MIT License
        </p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* Global styles handled by Tailwind */
</style>