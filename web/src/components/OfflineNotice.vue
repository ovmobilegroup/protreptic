<script setup lang="ts">
/**
 * OfflineNotice.vue — Phase30-A4: 断网提示 + 更新提示（右下角常驻，不挡内容）。
 *
 * 两种状态互斥地显示：
 *   1) 离线（navigator.onLine === false）：告诉用户「现在是本地缓存」，并如实报告
 *      预热进度（mode/index 分片 0..7 是否已经在缓存里）—— 不假装离线等于全功能。
 *   2) 新版本已就绪：SW 在新版 install 时 skipWaiting 接管了页面，这里只提示，
 *      绝不自动 reload（用户可能正在读长文）。
 *
 * 只在真的有话说的时候出现；SW 不支持（老浏览器 / dev）时整块不渲染。
 */
import { computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from '../composables/useI18n'
import { useServiceWorker } from '../composables/useServiceWorker'

const { t } = useI18n()
const { state, offline, updateReady, warmed, version, applyUpdate, checkForUpdate } = useServiceWorker()

const supported = computed(() => state.value !== 'unsupported')
const visible = computed(() => supported.value && (offline.value || updateReady.value))

const warmLabel = computed(() => {
  const w = warmed.value
  if (!w || !w.total) return ''
  return t(`模式分片已缓存 ${w.done}/${w.total}`, `${w.done}/${w.total} mode shards cached`)
})

const onVisibility = () => {
  if (document.visibilityState === 'visible') void checkForUpdate()
}

onMounted(() => {
  document.addEventListener('visibilitychange', onVisibility)
})
onUnmounted(() => {
  document.removeEventListener('visibilitychange', onVisibility)
})
</script>

<template>
  <Transition
    enter-active-class="transition duration-300 ease-silk"
    enter-from-class="opacity-0 translate-y-3"
    leave-active-class="transition duration-200 ease-in"
    leave-to-class="opacity-0 translate-y-3"
  >
    <div
      v-if="visible"
      class="pointer-events-none fixed inset-x-0 bottom-4 z-50 flex justify-center px-4"
      role="status"
      aria-live="polite"
    >
      <div class="pt-panel pointer-events-auto flex max-w-xl flex-col gap-2 px-4 py-3 sm:flex-row sm:items-center sm:gap-4">
        <template v-if="offline">
          <span class="flex items-center gap-2 text-sm text-parchment/85">
            <span class="h-2 w-2 shrink-0 rounded-full bg-gold-400 shadow-glow"></span>
            <span class="font-medium text-gold-200">{{ t('离线模式', 'Offline mode') }}</span>
          </span>
          <span class="text-xs leading-relaxed text-parchment/60">
            {{ t('正在读取本地缓存，已收录的内容照常可查。', 'Reading from the local cache — cached content still works.') }}
            <span v-if="warmLabel" class="pt-code ml-1">{{ warmLabel }}</span>
          </span>
        </template>

        <template v-else-if="updateReady">
          <span class="text-sm text-parchment/85">
            {{ t('新版本已就绪，刷新后生效。', 'A new version is ready — refresh to apply.') }}
          </span>
          <button
            type="button"
            class="pt-btn-gold shrink-0 px-3 py-1.5 text-xs"
            @click="applyUpdate"
          >
            {{ t('刷新', 'Refresh') }}
          </button>
        </template>

        <span v-if="version" class="pt-code hidden shrink-0 sm:block">{{ version }}</span>
      </div>
    </div>
  </Transition>
</template>
