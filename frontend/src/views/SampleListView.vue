<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'; // <-- 匯入 computed
import axios from 'axios';

interface Sample {
  id: number;
  line_name: string;
  product_name: string;
  timestamp: string;
  metric_a: number;
  metric_b: number;
  operator: string;
}

// 新增一個型別給分頁資訊
interface Pagination {
  total_items: number;
  total_pages: number;
  current_page: number;
  per_page: number;
  has_next: boolean;
  has_prev: boolean;
}

// --- 響應式狀態 ---
const samples = ref<Sample[]>([]);
const pagination = ref<Pagination | null>(null);
const currentPage = ref(1); // 用來追蹤當前頁面，方便分頁按鈕使用

// 新增：用來追蹤排序狀態
const sortColumn = ref('timestamp'); // 預設排序欄位
const sortOrder = ref('desc'); // 預設排序順序

// --- 方法 ---
// 改造 fetchData，讓它同時處理分頁和排序
const fetchData = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/v1/samples', {
      params: {
        page: currentPage.value,
        per_page: 5,
        sort_by: sortColumn.value,
        order: sortOrder.value,
      }
    });
    samples.value = response.data.data;
    pagination.value = response.data.pagination;
  } catch (error) {
    console.error('抓取資料時發生錯誤:', error);
  }
};

// 新增：處理表頭點擊事件的函式
const handleSort = (columnName: string) => {
  // 如果點擊的是當前已排序的欄位，則反轉排序方向
  if (sortColumn.value === columnName) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    // 否則，設定新的排序欄位，並預設為降序
    sortColumn.value = columnName;
    sortOrder.value = 'desc';
  }
  // 重新抓取第一頁的資料
  currentPage.value = 1;
  fetchData();
};

// --- 生命週期掛鉤 ---
onMounted(() => {
  fetchData();
});

// 改造分頁按鈕的函式
const changePage = (page: number) => {
  currentPage.value = page;
  fetchData();
}

</script>

<template>
  <div>
    <table>
      <thead>
        <tr>
          <th @click="handleSort('id')">
            ID
            <span v-if="sortColumn === 'id'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
          </th>
          <th @click="handleSort('line_name')">
            產線名稱
            <span v-if="sortColumn === 'line_name'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
          </th>
          <th @click="handleSort('product_name')">產品名稱</th>
          <th @click="handleSort('timestamp')">
            時間戳記
            <span v-if="sortColumn === 'timestamp'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
          </th>
          <th @click="handleSort('metric_a')">
            指標 A
            <span v-if="sortColumn === 'metric_a'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
          </th>
          <th @click="handleSort('metric_b')">
            指標 B
            <span v-if="sortColumn === 'metric_b'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
          </th>
          <th @click="handleSort('operator')">
            操作員
            <span v-if="sortColumn === 'operator'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sample in samples" :key="sample.id">
          <td>{{ sample.id }}</td>
          <td>{{ sample.line_name }}</td>
          <td>{{ sample.product_name }}</td>
          <td>{{ sample.timestamp }}</td>
          <td>{{ sample.metric_a }}</td>
          <td>{{ sample.metric_b }}</td>
          <td>{{ sample.operator }}</td>
        </tr>
      </tbody>
    </table>

    <div class="pagination-controls" v-if="pagination">
      <button @click="changePage(pagination.current_page - 1)" :disabled="!pagination.has_prev">
        上一頁
      </button>
      <span>
        頁數 {{ pagination.current_page }} / {{ pagination.total_pages }}
      </span>
      <button @click="changePage(pagination.current_page + 1)" :disabled="!pagination.has_next">
        下一頁
      </button>
    </div>
  </div>
</template>

<style scoped>
table {
  width: 100%; /* 讓表格填滿可用寬度 */
  border-collapse: collapse; /* 讓儲存格邊框合併，看起來更簡潔 */
  margin-top: 1rem;
}

th, td {
  border: 1px solid #ddd; /* 為儲存格和表頭加上邊框 */
  padding: 12px; /* 增加內距，讓內容不要擠在一起 */
  text-align: left; /* 文字靠左對齊 */
}

thead {
  background-color: #f2f2f2; /* 為表頭加上淺灰色背景 */
  font-weight: bold;
}

tbody tr:nth-child(even) {
  background-color: #f9f9f9; /* 斑馬紋效果，讓奇偶數列顏色不同，增加可讀性 */
}

tbody tr:hover {
  background-color: #f1f1f1; /* 滑鼠懸停時改變背景色，提供互動感 */
}

/* 新增分頁控制項的樣式 */
.pagination-controls {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
}

button:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  color: #aaa;
}

/* 新增 th 的樣式，讓它看起來可以點擊 */
th {
  cursor: pointer;
  user-select: none; /* 防止點擊時選取文字 */
}

th:hover {
  background-color: #e8e8e8;
}

</style>