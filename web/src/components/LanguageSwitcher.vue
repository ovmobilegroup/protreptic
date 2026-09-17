<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from '../composables/useI18n'

const { locale, toggleLocale } = useI18n()

const currentFlag = computed(() => locale.value === 'zh' ? '🇨🇳' : '🇺🇸')
const currentLang = computed(() => locale.value === 'zh' ? '中文' : 'English')
</script>

<template>
  <div class="relative" @click.outside="showDropdown = false">
    <button
      @click="showDropdown = !showDropdown"
      class="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
      aria-haspopup="true"
      aria-expanded="false"
    >
      <span>{{ currentFlag }}</span>
      <span>{{ currentLang }}</span>
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" leave-active-class="transition ease-in duration-75" leave-to-class="transform opacity-0 scale-95">
      <div v-if="showDropdown" class="absolute right-0 mt-2 w-32 bg-white rounded-md shadow-lg py-1 border border-gray-200 z-50">
        <button
          @click="() => { toggleLocale(); showDropdown = false }"
          class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
        >
          <span>🇨🇳</span>
          <span>中文</span>
          <span v-if="locale === 'zh'" class="ml-auto text-indigo-600">✓</span>
        </button>
        <button
          @click="() => { toggleLocale(); showDropdown = false }"
          class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
        >
          <span>🇺🇸</span>
          <span>English</span>
          <span v-if="locale === 'en'" class="ml-auto text-indigo-600">✓</span>
        </button>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showDropdown: false,
    }
  },
}
</script>