import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import FiguresView from '../views/FiguresView.vue'
import ModesView from '../views/ModesView.vue'
import TemplatesView from '../views/TemplatesView.vue'
import ApiDocsView from '../views/ApiDocsView.vue'
import FigureDetailView from '../views/FigureDetailView.vue'
import MindView from '../views/MindView.vue'
import TemplateDetailView from '../views/TemplateDetailView.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/figures',
  },
  {
    path: '/figures',
    name: 'figures',
    component: FiguresView,
    meta: {
      title: '历史人物库 - 统一名录',
      description: '全部历史人物与现代场景的统一检索名录：每条都有出处、操作步骤与现代应用，中英双语。',
      seoKind: 'static',
    },
  },
  {
    path: '/modes',
    name: 'modes',
    component: ModesView,
    meta: {
      title: '思维模式库 - 可执行方法总览',
      description: '从历史人物案例中提炼的思维模式总览：定义、操作步骤、出处与原话。',
      seoKind: 'static',
    },
  },
  {
    path: '/templates',
    name: 'templates',
    component: TemplatesView,
    meta: {
      title: '复盘模板库 - 历史案例工具',
      description: '把赤壁、隆中对等 7 个历史经典案例转化为可直接套用的复盘模板。',
      seoKind: 'static',
    },
  },
  {
    path: '/templates/:id',
    name: 'template-detail',
    component: TemplateDetailView,
    props: true,
    meta: {
      title: '复盘模板',
      description: '历史经典案例复盘模板：把历史决策现场转成可直接套用的复盘清单。',
    },
  },
  {
    path: '/api',
    name: 'api',
    component: ApiDocsView,
    meta: {
      title: 'API 文档',
      description: 'Protreptic 静态数据分片与数据结构说明。',
      seoKind: 'static',
    },
  },
  {
    path: '/minds/:code',
    name: 'mind',
    component: MindView,
    props: true,
    meta: {
      title: '人物模式档案',
      description: '历史人物的思维模式档案：定义、操作步骤、出处与原话。',
    },
  },
  {
    path: '/figures/:code',
    name: 'figure-detail',
    component: FigureDetailView,
    props: true,
    meta: {
      title: '场景档案',
      description: '现代处境场景关联的思维模式档案：来源人物、操作步骤与引用原话。',
    },
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