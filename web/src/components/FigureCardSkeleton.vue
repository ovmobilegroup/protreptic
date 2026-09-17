<script setup lang="ts">
</script>

<template>
  <article class="bg-white rounded-xl border border-gray-200 shadow-sm animate-pulse">
    <div class="px-5 py-4 border-b border-gray-100">
      <div class="h-5 w-20 bg-gray-200 rounded"></div>
    </div>
    <div class="p-5 space-y-4">
      <div class="h-6 w-3/4 bg-gray-200 rounded"></div>
      <div class="h-4 w-full bg-gray-200 rounded"></div>
      <div class="h-4 w-5/6 bg-gray-200 rounded"></div>
      <div class="h-4 w-4/6 bg-gray-200 rounded"></div>
      <div class="flex flex-wrap gap-2">
        <div class="h-6 w-16 bg-gray-200 rounded-full"></div>
        <div class="h-6 w-16 bg-gray-200 rounded-full"></div>
        <div class="h-6 w-16 bg-gray-200 rounded-full"></div>
      </div>
      <div class="flex flex-wrap gap-2">
        <div class="h-6 w-20 bg-gray-200 rounded"></div>
        <div class="h-6 w-20 bg-gray-200 rounded"></div>
      </div>
      <div class="flex items-center gap-2 text-xs">
        <div class="h-4 w-16 bg-gray-200 rounded"></div>
        <div class="h-4 w-16 bg-gray-200 rounded"></div>
      </div>
    </div>
    <div class="px-5 pb-4 pt-2 border-t border-gray-50">
      <div class="w-full h-10 bg-gray-200 rounded-lg"></div>
    </div>
  </article>
</template>

<style scoped>
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>