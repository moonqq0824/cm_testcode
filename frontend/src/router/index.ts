import { createRouter, createWebHistory } from 'vue-router';
import SampleListView from '../views/SampleListView.vue';
import DashboardView from '../views/DashboardView.vue';
import AnalysisView from '../views/AnalysisView.vue';
import WastewaterReportView from '../views/WastewaterReportView.vue';
import WastewaterReportFormView from '../views/WastewaterReportForm.vue'; // <-- 匯入新頁面

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView,
  },
  {
    path: '/samples',
    name: 'SampleList',
    component: SampleListView,
  },
  {
    path: '/analysis', // <-- 2. 新增圖表頁面的路徑
    name: 'Analysis',
    component: AnalysisView,
  },
  {
    path: '/wastewater-reports', // <-- 新增廢水報告的路徑
    name: 'WastewaterReport',
    component: WastewaterReportView,
  },
  {
    path: '/wastewater-reports/new', // <-- 新增「新增報告」的路由
    name: 'WastewaterReportNew',
    component: WastewaterReportFormView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkActiveClass: 'active',
});

export default router;
