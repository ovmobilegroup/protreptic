import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import FiguresView from '../views/FiguresView.vue'
import ModesView from '../views/ModesView.vue'
import TemplatesView from '../views/TemplatesView.vue'
import ApiDocsView from '../views/ApiDocsView.vue'
import FigureDetailView from '../views/FigureDetailView.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/figures',
  },
  {
    path: '/figures',
    name: 'figures',
    component: FiguresView,
    meta: { title: '历史人物库' },
  },
  {
    path: '/modes',
    name: 'modes',
    component: ModesView,
    meta: { title: '思维模式库' },
  },
  {
    path: '/templates',
    name: 'templates',
    component: TemplatesView,
    meta: { title: '复盘模板' },
  },
  {
    path: '/api',
    name: 'api',
    component: ApiDocsView,
    meta: { title: 'API 文档' },
  },
  {
    path: '/figures/:code',
    name: 'figure-detail',
    component: FigureDetailView,
    props: true,
    meta: { title: '人物详情' },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

export default router