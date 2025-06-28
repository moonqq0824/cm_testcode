<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 定義統計數據的型別
interface Stats {
  total_records: number;
  avg_metric_a: number;
  avg_metric_b: number;
  latest_record_time: string | null;
}

// 建立響應式變數來存放統計數據
const stats = ref<Stats | null>(null);
const isLoading = ref(true); // 加上一個載入狀態，提升使用者體驗
const error = ref<string | null>(null); // 用來存放錯誤訊息

// 抓取統計數據
const fetchStats = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get('http://localhost:5000/api/v1/statistics/main-metrics');
    stats.value = response.data;
  } catch (err) {
    console.error('抓取統計數據時發生錯誤:', err);
    error.value = '無法載入統計數據，請稍後再試。';
  } finally {
    isLoading.value = false;
  }
};

// 在元件掛載後執行
onMounted(fetchStats);

// 一個簡單的函式來格式化日期
const formatDateTime = (isoString: string | null) => {
  if (!isoString) return '無';
  return new Date(isoString).toLocaleString('zh-TW');
}
</script>

<template>
  <div>
    <h1>首頁儀表板</h1>
    
    <div v-if="isLoading">正在載入數據...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <div v-if="stats" class="stats-grid">
      <div class="stat-card">
        <div class="card-title">總紀錄筆數</div>
        <div class="card-value">{{ stats.total_records }}</div>
        <div class="card-footer">筆</div>
      </div>

      <div class="stat-card">
        <div class="card-title">指標 A 平均值</div>
        <div class="card-value">{{ stats.avg_metric_a }}</div>
        <div class="card-footer">單位</div>
      </div>
      
      <div class="stat-card">
        <div class="card-title">指標 B 平均值</div>
        <div class="card-value">{{ stats.avg_metric_b }}</div>
        <div class="card-footer">單位</div>
      </div>
      
      <div class="stat-card">
        <div class="card-title">最新一筆紀錄時間</div>
        <div class="card-value small-text">{{ formatDateTime(stats.latest_record_time) }}</div>
        <div class="card-footer">時間</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.stat-card {
  background-color: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
}

.card-title {
  color: #64748b;
  font-size: 0.9rem;
}

.card-value {
  font-size: 2.25rem;
  font-weight: bold;
  color: #0C809F; /* 主色 */
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  line-height: 1.1;
}

.card-value.small-text {
  font-size: 1.1rem; /* 日期時間字體小一點 */
}

.card-footer {
  margin-top: auto; /* 將 footer 推到卡片底部 */
  color: #94a3b8;
  font-size: 0.8rem;
}

.error-message {
  color: #e74c3c;
  margin-top: 1rem;
}
</style>