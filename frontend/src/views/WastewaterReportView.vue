<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ReportDetailPanel from '../components/ReportDetailPanel.vue'; // <-- 確保這一行存在

// --- 型別定義 ---
interface ReportItem {
  id: number; item_name: string; value: number; unit: string; standard: string; is_compliant: boolean;
}
interface Report {
  id: number; report_date: string; vendor: string; status: string; items: ReportItem[];
}

// --- 響應式狀態 ---
const reports = ref<Report[]>([]);
const isLoading = ref(true);
const error = ref<string | null>(null);
const selectedReport = ref<Report | null>(null);

// --- 方法 ---
const fetchReports = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get('http://localhost:5000/api/v1/wastewater-reports');
    reports.value = response.data;
  } catch (err) {
    console.error('抓取廢水報告時發生錯誤:', err);
    error.value = '無法載入報告資料，請稍後再試。';
  } finally {
    isLoading.value = false;
  }
};

const formatDateTime = (isoString: string | null) => {
  if (!isoString) return 'N/A';
  return new Date(isoString).toLocaleDateString('zh-TW');
};

const openPanel = (report: Report) => {
  console.log('卡片被點擊了！準備開啟面板的報告是:', report);
  selectedReport.value = report;
};

const closePanel = () => {
  selectedReport.value = null;
};

// --- 生命週期掛鉤 ---
onMounted(fetchReports);
</script>

<template>
  <div>
    <h1>廢水報告管理</h1>
    
    <div v-if="isLoading">正在載入報告...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <div v-if="reports.length > 0" class="report-list">
      <div v-for="report in reports" :key="report.id" class="report-card" @click="openPanel(report)">
        <div class="card-header">
          <span class="vendor-name">{{ report.vendor }}</span>
          <span class="report-date">{{ formatDateTime(report.report_date) }}</span>
        </div>
        <div class="card-body">
          <span class="status-badge" :class="`status-${report.status}`">{{ report.status }}</span>
        </div>
      </div>
    </div>
    <div v-else-if="!isLoading">
      <p>目前沒有任何廢水報告。</p>
    </div>

    <Transition name="slide">
      <ReportDetailPanel v-if="selectedReport" :report="selectedReport" @close="closePanel" />
    </Transition>
  </div>
</template>

<style scoped>
.report-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
}

.report-card {
  background-color: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
}

.report-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.vendor-name {
  font-weight: bold;
  font-size: 1.1rem;
}

.report-date {
  color: #64748b;
  font-size: 0.9rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 50px; /* 膠囊狀 */
  font-size: 0.8rem;
  font-weight: 500;
  color: white;
}

/* 根據不同狀態給予不同顏色 */
.status-合格 {
  background-color: #10b981; /* 綠色 */
}
.status-部分項目不合格 {
  background-color: #ef4444; /* 紅色 */
}
.status-追蹤中 {
  background-color: #f59e0b; /* 黃色 */
}

.error-message {
  color: #e74c3c;
  margin-top: 1rem;
}

/* 新增：滑入/滑出的動畫效果定義 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease-out;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>