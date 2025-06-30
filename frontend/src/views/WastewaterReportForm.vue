<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

// --- 1. 型別定義 (Type Definitions) ---
// 定義表單中「單筆」檢測項目的結構
interface ReportItemForm {
  id: number | string; // 在前端，新增時用時間戳當臨時ID，編輯時用後端來的真實ID
  item_name: string;
  value: number | null;
  unit: string;
  standard: string;
  is_compliant: boolean;
}

// 定義整個表單資料的結構
interface FormData {
  vendor: string;
  report_date: string;
  status: string;
  items: ReportItemForm[];
}

// --- 2. 初始化與響應式狀態 (State) ---
const formData = ref<FormData>({
  vendor: '',
  report_date: new Date().toISOString().split('T')[0], // 預設為今天日期
  status: '合格',
  items: [], // 檢測項目列表，一開始是空的
});

const isSubmitting = ref(false); // 用於防止重複提交的狀態
const router = useRouter(); // 用來操作路由，例如跳轉頁面
const route = useRoute(); // 用來讀取當前路由的資訊，例如網址中的 ID

// --- 3. 計算屬性 (Computed) ---
// 透過網址中是否存在 report_id 參數，來判斷現在是「新增」還是「編輯」模式
const isEditMode = computed(() => !!route.params.report_id);
const reportId = route.params.report_id as string; // 取得網址中的 report_id

// --- 4. 方法 (Methods) ---
/**
 * 抓取單筆報告的詳細資料 (僅在編輯模式下執行)
 */
const fetchReportData = async () => {
  try {
    const response = await axios.get(`http://localhost:5000/api/v1/wastewater-reports/${reportId}`);
    const data = response.data;
    // 將從 API 獲取的舊資料，填入我們的表單狀態中
    formData.value = {
      vendor: data.vendor,
      report_date: new Date(data.report_date).toISOString().split('T')[0],
      status: data.status,
      items: data.items.map((item: any) => ({ ...item, id: item.id })) // 在編輯模式，我們用真實的 item id 當 key
    };
  } catch (error) {
    console.error('獲取報告詳情失敗:', error);
    alert('無法載入報告資料，將返回列表頁。');
    router.push('/wastewater-reports');
  }
};

/**
 * 在檢測項目列表中，新增一個空白列
 */
const addItemRow = () => {
  formData.value.items.push({
    id: Date.now(), // 用當前的時間戳來確保 key 的唯一性，防止 v-for 出錯
    item_name: '',
    value: null,
    unit: '',
    standard: '',
    is_compliant: true,
  });
};

/**
 * 根據臨時 ID，從檢測項目列表中移除一列
 * @param id 要移除的項目的臨時 ID
 */
const removeItemRow = (id: number | string) => {
  formData.value.items = formData.value.items.filter(item => item.id !== id);
};

/**
 * 提交表單 (核心邏輯)
 */
const submitForm = async () => {
  if (isSubmitting.value) return; // 如果正在提交，則不執行任何操作

  // 簡單的前端驗證
  if (!formData.value.vendor || !formData.value.report_date) {
    alert('請填寫廠商名稱和報告日期！');
    return;
  }
  if (formData.value.items.length === 0) {
    alert('請至少新增一筆檢測項目！');
    return;
  }

  isSubmitting.value = true; // 開始提交，鎖定按鈕

  try {
    // 準備要發送到後端的資料 (payload)
    // 我們需要移除前端專用的臨時 id
    const payload = {
      ...formData.value,
      items: formData.value.items.map(({ id, ...rest }) => rest)
    };

    if (isEditMode.value) {
      // 編輯模式：發送 PUT 請求
      await axios.put(`http://localhost:5000/api/v1/wastewater-reports/${reportId}`, payload);
      alert('更新報告成功！');
    } else {
      // 新增模式：發送 POST 請求
      await axios.post('http://localhost:5000/api/v1/wastewater-reports/', payload);
      alert('新增報告成功！');
    }
    router.push('/wastewater-reports'); // 成功後，跳轉回列表頁

  } catch (error) {
    console.error('儲存報告時發生錯誤:', error);
    alert('儲存失敗，請檢查資料或稍後再試。');
  } finally {
    isSubmitting.value = false; // 無論成功或失敗，最後都要解除按鈕鎖定
  }
};

/**
 * 點擊取消按鈕，返回列表頁
 */
const cancelForm = () => {
    router.push('/wastewater-reports');
}

// --- 5. 生命週期掛鉤 (Lifecycle Hook) ---
onMounted(() => {
  // 當元件被掛載到畫面上時，檢查是否為編輯模式
  if (isEditMode.value) {
    // 如果是，就去抓取該筆報告的舊資料來填充表單
    fetchReportData();
  }
});
</script>

<template>
  <div>
    <h1>{{ isEditMode ? '編輯廢水報告' : '新增廢水報告' }}</h1>
    
    <form class="report-form" @submit.prevent="submitForm">
      <div class="form-grid">
        <div class="form-group">
          <label for="vendor">廠商名稱</label>
          <input type="text" id="vendor" v-model="formData.vendor" required />
        </div>

        <div class="form-group">
          <label for="report_date">報告日期</label>
          <input type="date" id="report_date" v-model="formData.report_date" required />
        </div>

        <div class="form-group">
          <label for="status">總體狀態</label>
          <select id="status" v-model="formData.status">
            <option>合格</option>
            <option>部分項目不合格</option>
            <option>追蹤中</option>
          </select>
        </div>
      </div>

      <h3 class="items-title">檢測項目</h3>
      
      <div class="items-list">
        <div v-if="formData.items.length > 0" class="item-row item-header">
          <span>項目名稱</span>
          <span>檢測值</span>
          <span>單位</span>
          <span>標準值</span>
          <span>是否合格</span>
          <span></span> </div>
        <div v-for="item in formData.items" :key="item.id" class="item-row">
          <input type="text" placeholder="項目名稱" v-model="item.item_name" required>
          <input type="number" placeholder="檢測值" v-model.number="item.value" required step="any">
          <input type="text" placeholder="單位" v-model="item.unit">
          <input type="text" placeholder="標準值" v-model="item.standard">
          <select v-model="item.is_compliant">
            <option :value="true">合格</option>
            <option :value="false">不合格</option>
          </select>
          <button type="button" class="delete-item-btn" @click="removeItemRow(item.id)">×</button>
        </div>
      </div>

      <button type="button" class="add-item-btn" @click="addItemRow">＋ 新增檢測項目</button>
      
      <div class="form-actions">
        <button type="submit" class="btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? '儲存中...' : '儲存報告' }}
        </button>
        <button type="button" class="btn-secondary" @click="cancelForm">取消</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.report-form {
  max-width: 900px;
  margin-top: 2rem;
  padding: 2rem;
  background-color: #fff;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #334155;
}

input[type="text"],
input[type="date"],
input[type="number"],
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box; /* 確保 padding 不會撐大寬度 */
}

input:focus, select:focus {
  outline: none;
  border-color: #0C809F;
  box-shadow: 0 0 0 3px rgba(12, 128, 159, 0.2);
}

.items-title {
  margin-top: 2rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
}

.item-row {
  display: grid;
  grid-template-columns: 3fr 2fr 1fr 1fr 1.5fr auto;
  gap: 1rem;
  align-items: center;
}

.item-header {
  font-weight: 500;
  color: #334155;
  font-size: 0.9rem;
  padding: 0 0.75rem;
  margin-bottom: -0.5rem; /* 讓表頭和第一行更靠近 */
}

.add-item-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  border: 1px dashed #0C809F;
  background-color: transparent;
  color: #0C809F;
  cursor: pointer;
  border-radius: 6px;
  width: fit-content;
  font-weight: 500;
  transition: background-color 0.2s;
}

.add-item-btn:hover {
  background-color: rgba(12, 128, 159, 0.05);
}

.delete-item-btn {
  background-color: #fee2e2;
  color: #ef4444;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  font-size: 20px;
  line-height: 28px;
  text-align: center;
  cursor: pointer;
  padding: 0;
  transition: background-color 0.2s;
}

.delete-item-btn:hover {
  background-color: #fecaca;
}

.form-actions {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

button {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: 1px solid transparent;
  font-weight: 500;
  cursor: pointer;
}

.btn-primary {
  background-color: #0C809F;
  color: white;
  border-color: #0C809F;
}

.btn-primary:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border-color: #6c757d;
}
</style>