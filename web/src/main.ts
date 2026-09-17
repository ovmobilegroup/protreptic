import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './style.css'
import App from './App.vue'
import { useI18n } from './composables/useI18n'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// 恢复上次选择的语言（原先 initLocale 从未被调用，切换结果只存在内存里）
useI18n().initLocale()

app.mount('#app')