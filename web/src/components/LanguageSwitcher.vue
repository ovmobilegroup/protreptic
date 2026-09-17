<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useI18n } from '../composables/useI18n'

const { locale, toggleLocale } = useI18n()

const currentFlag = computed(() => locale.value === 'zh' ? '🇨🇳' : '🇺🇸')
const currentLang = computed(() => locale.value === 'zh' ? '中文' : 'English')

// 修复：showDropdown 原先写在第二个 <script>（Options API）块里，与 <script setup lang="ts">
// 语言类型不一致会导致 SFC 编译失败（组件被 App.vue 引用时直接构建报错），且根节点用了
// 不存在的 @click.outside 修饰符。这里统一收敛到 setup：ref + 显式外部点击监听。
const showDropdown = ref(false)
const root = ref<HTMLElement | null>(null)

const onDocumentClick = (event: MouseEvent) => {
  if (root.value && !root.value.contains(event.target as Node)) showDropdown.value = false
}

onMounted(() => document.addEventListener('click', onDocumentClick))
onBeforeUnmount(() => document.removeEventListener('click', onDocumentClick))

const selectLang = () => {
  toggleLocale()
  showDropdown.value = false
}
</script>

<template>
  <div ref="root" class="relative">
    <button
      @click="showDropdown = !showDropdown"
      class="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
      aria-haspopup="true"
      :aria-expanded="showDropdown"
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
          @click="selectLang"
          class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
        >
          <span>🇨🇳</span>
          <span>中文</span>
          <span v-if="locale === 'zh'" class="ml-auto text-indigo-600">✓</span>
        </button>
        <button
          @click="selectLang"
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
