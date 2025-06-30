<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// --- 型別定義 ---
interface Sample {
  id: number;
  line_name: string;
  product_name: string;
  timestamp: string;
  metric_a: number;
  metric_b: number;
  operator: string;
}
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
const currentPage = ref(1);
const sortColumn = ref('timestamp');
const sortOrder = ref('desc');
const filterOptions = ['全部', '產線A', '產線B', '產線C'];
const activeFilter = ref('全部');
const selectedIds = ref<number[]>([]);

// --- 計算屬性 ---
const isAllSelected = computed({
  get: () => {
    const pageIds = samples.value.map(s => s.id);
    return pageIds.length > 0 && pageIds.every(id => selectedIds.value.includes(id));
  },
  set: (value: boolean) => {
    const pageIds = samples.value.map(s => s.id);
    if (value) {
      pageIds.forEach(id => {
        if (!selectedIds.value.includes(id)) {
          selectedIds.value.push(id);
        }
      });
    } else {
      selectedIds.value = selectedIds.value.filter(id => !pageIds.includes(id));
    }
  }
});

// --- 方法 ---
const fetchData = async () => {
  try {
    const params: any = {
      page: currentPage.value,
      per_page: 5,
      sort_by: sortColumn.value,
      order: sortOrder.value,
    };
    if (activeFilter.value !== '全部') {
      params.line_name = activeFilter.value;
    }
    const response = await axios.get('http://localhost:5000/api/v1/samples', { params });
    samples.value = response.data.data;
    pagination.value = response.data.pagination;
  } catch (error) {
    console.error('抓取資料時發生錯誤:', error);
  }
};

const handleSort = (columnName: string) => {
  if (sortColumn.value === columnName) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortColumn.value = columnName;
    sortOrder.value = 'desc';
  }
  currentPage.value = 1;
  fetchData();
};

const selectFilter = (option: string) => {
  activeFilter.value = option;
  currentPage.value = 1;
  fetchData();
};

const changePage = (page: number) => {
  if (page < 1 || (pagination.value && page > pagination.value.total_pages) || !pagination.value) return;
  currentPage.value = page;
  fetchData();
};

const deleteSelected = async () => {
  if (selectedIds.value.length === 0) {
    alert('請先勾選要刪除的項目');
    return;
  }
  if (window.confirm(`你確定要刪除這 ${selectedIds.value.length} 筆紀錄嗎？`)) {
    try {
      await axios.delete('http://localhost:5000/api/v1/samples', {
        data: { ids: selectedIds.value }
      });
      selectedIds.value = [];
      fetchData();
    } catch (error) {
      console.error('刪除時發生錯誤:', error);
      alert('刪除失敗，請稍後再試。');
    }
  }
};

// --- 生命週期掛鉤 ---
onMounted(fetchData);
</script>

<template>
  <div>
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
      <button class="btn btn-danger" v-if="selectedIds.length > 0" @click="deleteSelected">
        刪除已選 ({{ selectedIds.length }})
      </button>
    </div>

    <table>
      <thead>
        <tr>
          <th><input type="checkbox" v-model="isAllSelected" /></th>
          <th @click="handleSort('id')">ID <span v-if="sortColumn === 'id'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="handleSort('line_name')">產線名稱 <span v-if="sortColumn === 'line_name'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="handleSort('product_name')">產品名稱</th>
          <th @click="handleSort('timestamp')">時間戳記 <span v-if="sortColumn === 'timestamp'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="handleSort('metric_a')">指標 A <span v-if="sortColumn === 'metric_a'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="handleSort('metric_b')">指標 B <span v-if="sortColumn === 'metric_b'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="handleSort('operator')">操作員 <span v-if="sortColumn === 'operator'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sample in samples" :key="sample.id" :class="{ selected: selectedIds.includes(sample.id) }">
          <td><input type="checkbox" :value="sample.id" v-model="selectedIds" /></td>
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

    <div class="pagination-controls" v-if="pagination && pagination.total_items > 0">
      <button class="btn btn-outline" @click="changePage(pagination.current_page - 1)" :disabled="!pagination.has_prev">
        上一頁
      </button>
      <span>
        頁數 {{ pagination.current_page }} / {{ pagination.total_pages }}
      </span>
      <button class="btn btn-outline" @click="changePage(pagination.current_page + 1)" :disabled="!pagination.has_next">
        下一頁
      </button>
    </div>
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
  display: inline-flex;
  gap: 0.25rem;
  background-color: #e2e8f0;
  padding: 0.25rem;
  border-radius: 50px;
  width: fit-content;
}

.filter-tabs button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 50px;
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

tbody tr.selected {
  background-color: #fed7d7 !important;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  cursor: pointer;
  user-select: none;
}
th:hover {
  background-color: #e8e8e8;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

thead {
  background-color: #f2f2f2;
  font-weight: bold;
}

tbody tr:nth-child(even):not(.selected) {
  background-color: #f9f9f9;
}

tbody tr:not(.selected):hover {
  background-color: #f1f1f1;
}

.pagination-controls {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-controls button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
  border-radius: 6px;
}

.pagination-controls button:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  color: #aaa;
}
</style>