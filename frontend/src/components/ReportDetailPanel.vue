<script setup lang="ts">
// --- 型別定義 ---
// 我們從主頁面複製一份過來，確保資料型別一致
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

// --- Props & Emits ---
// 1. defineProps: 定義這個元件可以從「外部(父層)」接收哪些資料
//    我們定義了一個名為 `report` 的 prop，用來接收要顯示的報告物件
const props = defineProps<{
  report: Report | null;
}>();

// 2. defineEmits: 定義這個元件可以向「外部(父層)」發送哪些事件
//    我們定義了一個名為 `close` 的事件，用來通知父層「使用者想關閉面板了」
const emit = defineEmits(['close']);

// --- 方法 ---
const formatDateTime = (isoString: string | null) => {
  if (!isoString) return 'N/A';
  return new Date(isoString).toLocaleString('zh-TW');
};
</script>

<template>
  <div v-if="report" class="panel-overlay" @click.self="emit('close')">
    <div class="panel-container">
      <div class="panel-header">
        <h3>{{ report.vendor }} - 廢水報告詳情</h3>
        <button class="close-btn" @click="emit('close')">×</button>
      </div>
      <div class="panel-body">
        <p><strong>報告日期：</strong>{{ formatDateTime(report.report_date) }}</p>
        <p><strong>總體狀態：</strong>{{ report.status }}</p>

        <h4>檢測項目詳情</h4>
        <table class="items-table">
          <thead>
            <tr>
              <th>項目名稱</th>
              <th>檢測值</th>
              <th>單位</th>
              <th>標準值</th>
              <th>是否合格</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in report.items" :key="item.id">
              <td>{{ item.item_name }}</td>
              <td>{{ item.value }}</td>
              <td>{{ item.unit }}</td>
              <td>{{ item.standard }}</td>
              <td>{{ item.is_compliant ? '是' : '否' }}</td>
            </tr>
          </tbody>
        </table>

        <div class="panel-actions" v-if="report">
          <template v-if="report.status === '部分項目不合格'">
            <button class="action-btn track-btn">處理與追蹤</button>
            <button class="action-btn doc-btn">產生公文</button>
          </template>
          <p v-else class="no-action-text">目前狀態無需額外操作。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.panel-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: flex-end; /* 讓面板靠右 */
  z-index: 100;
}

.panel-container {
  width: 50%;
  max-width: 600px;
  min-width: 400px;
  height: 100%;
  background-color: white;
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.panel-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #64748b;
}

.panel-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex-grow: 1;
}

.items-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
.items-table th,
.items-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
.items-table thead {
  background-color: #f2f2f2;
}

.panel-actions {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.panel-actions {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.track-btn {
  background-color: #f59e0b; /* 黃色 */
  color: white;
  border-color: #f59e0b;
}

.doc-btn {
  background-color: #64748b; /* 灰色 */
  color: white;
  border-color: #64748b;
}

.action-btn:hover {
  opacity: 0.9;
}

.no-action-text {
  color: #64748b;
  font-size: 0.9rem;
  margin: 0;
}
</style>
