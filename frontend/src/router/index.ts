import { createRouter, createWebHistory } from 'vue-router';
import SampleListView from '../views/SampleListView.vue';
import DashboardView from '../views/DashboardView.vue';
import AnalysisView from '../views/AnalysisView.vue'; // <-- 1. 匯入新的圖表頁面

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView
  },
  {
    path: '/samples',
    name: 'SampleList',
    component: SampleListView
  },
  {
    path: '/analysis', // <-- 2. 新增圖表頁面的路徑
    name: 'Analysis',
    component: AnalysisView
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkActiveClass: 'active',
});

export default router;