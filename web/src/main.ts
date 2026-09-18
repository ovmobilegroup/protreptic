import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './style.css'
import App from './App.vue'
import { useI18n } from './composables/useI18n'
import { initSeo } from './composables/useSeo'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Phase30-A1: 每个路由的 title / meta description / canonical / JSON-LD（详见 composables/useSeo.ts）
initSeo(router)

// 恢复上次选择的语言（原先 initLocale 从未被调用，切换结果只存在内存里）
useI18n().initLocale()

app.mount('#app')