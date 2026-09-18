import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './style.css'
import App from './App.vue'
import { useI18n } from './composables/useI18n'
import { initSeo } from './composables/useSeo'
import { initServiceWorker } from './composables/useServiceWorker'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Phase30-A1: 每个路由的 title / meta description / canonical / JSON-LD（详见 composables/useSeo.ts）
initSeo(router)

// 恢复上次选择的语言（原先 initLocale 从未被调用，切换结果只存在内存里）
useI18n().initLocale()

// Phase30-A2: 关键路由的静态页面里 #app 已带正文快照 (tools/prerender_body.py),
// 而 createApp 的 mount 不会清空容器: 挂载前先清空, 避免静态快照与渲染结果两份正文并存.
const rootEl = document.getElementById('app')
if (rootEl) rootEl.innerHTML = ''

app.mount('#app')

// Phase30-A4: 注册 service worker（离线可用）。dev 默认不注册，VITE_SW=on 可强制打开；
// 注册失败不影响页面（纯增量能力），状态由 OfflineNotice 呈现。
void initServiceWorker()
