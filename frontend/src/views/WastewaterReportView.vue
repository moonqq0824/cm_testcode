<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ReportDetailPanel from '../components/ReportDetailPanel.vue';

// --- 型別定義 ---
interface ReportItem {
  id: number;
  item_name: string;
  value: number;
  unit: string;
  standard: string;
  is_compliant: boolean;
}
interface Report {
  id: number;
  report_date: string;
  vendor: string;
  status: string;
  items: ReportItem[];
}

// --- 響應式狀態 ---
const reports = ref<Report[]>([]);
const isLoading = ref(true);
const error = ref<string | null>(null);
const selectedReport = ref<Report | null>(null);
const filterOptions = ['全部', '合格', '部分項目不合格', '追蹤中'];
const activeFilter = ref('全部');
const searchTerm = ref('');
let debounceTimer: number;

// --- 方法 ---
// 這是 fetchData 函式的唯一定義
const fetchData = async () => {
  try {
    isLoading.value = true;
    const params: { status?: string; search?: string } = {};
    if (activeFilter.value !== '全部') {
      params.status = activeFilter.value;
    }
    if (searchTerm.value.trim() !== '') {
      params.search = searchTerm.value.trim();
    }

    const response = await axios.get('http://localhost:5000/api/v1/wastewater-reports', { params });
    reports.value = response.data;
  } catch (err) {
    console.error('抓取廢水報告時發生錯誤:', err);
    error.value = '無法載入報告資料，請稍後再試。';
  } finally {
    isLoading.value = false;
  }
};

const selectFilter = (status: string) => {
  activeFilter.value = status;
  fetchData();
};

const onSearchInput = () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetchData();
  }, 500);
};

const formatDateTime = (isoString: string | null) => {
  if (!isoString) return 'N/A';
  return new Date(isoString).toLocaleDateString('zh-TW');
};

const openPanel = (report: Report) => {
  selectedReport.value = report;
};

const closePanel = () => {
  selectedReport.value = null;
};

// --- 生命週期掛鉤 ---
onMounted(fetchData);
</script>

<template>
  <div>
    <h1>廢水報告管理</h1>

    <div class="toolbar">
      <div class="filter-tabs">
        <button
          v-for="option in filterOptions"
          :key="option"
          :class="{ active: activeFilter === option }"
          @click="selectFilter(option)"
        >
          {{ option }}
        </button>
      </div>
      <input
        type="text"
        class="search-input"
        placeholder="依廠商名稱搜尋..."
        v-model="searchTerm"
        @input="onSearchInput"
      />
      <router-link to="/wastewater-reports/new" class="btn btn-primary">＋ 新增報告</router-link>
    </div>

    <div v-if="isLoading">正在載入報告...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="reports.length > 0" class="report-list">
      <div
        v-for="report in reports"
        :key="report.id"
        class="report-card"
        @click="openPanel(report)"
      >
        <div class="card-header">
          <span class="vendor-name">{{ report.vendor }}</span>
          <span class="report-date">{{ formatDateTime(report.report_date) }}</span>
        </div>
        <div class="card-body">
          <span class="status-badge" :class="`status-${report.status}`">{{ report.status }}</span>
          <router-link :to="`/wastewater-reports/${report.id}/edit`" class="edit-link">
            編輯
          </router-link>
        </div>
      </div>
    </div>
    <div v-else-if="!isLoading" class="no-data">
      <p>在目前的篩選條件下，沒有任何廢水報告。</p>
    </div>

    <Transition name="slide">
      <ReportDetailPanel v-if="selectedReport" :report="selectedReport" @close="closePanel" />
    </Transition>
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.filter-tabs {
  display: inline-flex; /* 改為 inline-flex 讓背景寬度自適應 */
  gap: 0.25rem; /* 稍微減少間距 */
  background-color: #e2e8f0;
  padding: 0.25rem;
  border-radius: 50px; /* 讓容器本身也變成膠囊狀 */
  width: fit-content;
}
.filter-tabs button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 50px; /* 讓按鈕本身也變成膠囊狀 */
  background-color: transparent;
  color: #4a5568;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.filter-tabs button.active {
  background-color: white;
  color: #0C809F;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.search-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  min-width: 250px;
}
.search-input:focus {
  outline: none;
  border-color: #0c809f;
  box-shadow: 0 0 0 2px rgba(12, 128, 159, 0.2);
}
.no-data {
  margin-top: 2rem;
  color: #64748b;
}
.report-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}
.report-card {
  background-color: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
}
.report-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 500;
  color: white;
}
.status-合格 {
  background-color: #10b981;
}
.status-部分項目不合格 {
  background-color: #ef4444;
}
.status-追蹤中 {
  background-color: #f59e0b;
}
.error-message {
  color: #e74c3c;
  margin-top: 1rem;
}
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease-out;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
/* 修改 toolbar 的樣式 */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

/* 新增 actions-group 的樣式 */
.actions-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.add-btn {
  background-color: #0c809f;
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  transition: opacity 0.2s;
}
.add-btn:hover {
  opacity: 0.9;
}
.card-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.edit-link {
  font-size: 0.9rem;
  color: #0C809F;
  text-decoration: none;
}
.edit-link:hover {
  text-decoration: underline;
}
</style>
