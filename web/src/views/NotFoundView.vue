<script setup lang="ts">
/**
 * NotFoundView.vue — Phase30-A4: 路由 catch-all 兜底页。
 *
 * 为什么要它：离线时 SW 对未知路径会返回缓存的外壳（200），在线时 Pages 对未收录
 * 路径返回 404.html（也是同一个 SPA 外壳）。两种情况下 Vue Router 都需要一条
 * catch-all 路由来渲染一个「真的没有这一页」的界面，否则用户看到的是空白页 ——
 * 与在线的 404 表现不一致。head 由 router meta 处理（noindex + 无 canonical）。
 */
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()

const links = [
  { to: '/figures', zh: '历史人物库', en: 'Figures' },
  { to: '/modes', zh: '思维模式库', en: 'Modes' },
  { to: '/templates', zh: '复盘模板', en: 'Templates' },
]
</script>

<template>
  <section class="pt-container py-20 sm:py-28">
    <div class="mx-auto max-w-2xl text-center">
      <p class="pt-code">ERROR 404 · NOT FOUND</p>
      <h1 class="pt-h1 pt-gradient-text mt-4">这一页不在典藏里</h1>
      <p class="mt-5 text-sm leading-relaxed text-parchment/60">
        {{ t(
          '该地址没有被收录：可能链接写错了，或这条内容还没进入名录。',
          'This address is not in the archive — the link may be wrong, or the entry is not catalogued yet.',
        ) }}
      </p>
      <div class="mt-8 flex flex-wrap justify-center gap-2">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to" class="pt-btn-ghost px-4 py-2 text-sm">
          {{ t(l.zh, l.en) }}
        </RouterLink>
      </div>
      <p class="mt-8 text-xs text-parchment/40">
        {{ t('也可以从首页的检索框按人物名或模式名重新找。', 'You can also search by figure or mode name from the home list.') }}
      </p>
    </div>
  </section>
</template>
