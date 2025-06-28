import { createRouter, createWebHistory } from 'vue-router';
import SampleListView from '../views/SampleListView.vue';
import DashboardView from '../views/DashboardView.vue'; // <-- 1. 匯入我們的新頁面

const routes = [
  {
    path: '/', // <-- 2. 修改這裡
    name: 'Dashboard',
    component: DashboardView // 不再是 redirect，而是直接指向 DashboardView 元件
  },
  {
    path: '/samples',
    name: 'SampleList',
    component: SampleListView
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkActiveClass: 'active',
});

export default router;