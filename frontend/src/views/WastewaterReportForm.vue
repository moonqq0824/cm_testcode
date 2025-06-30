<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// --- 型別定義 ---
interface ReportItemForm {
  id: number; // 這是一個前端專用的臨時 ID，用來當作 v-for 的 key
  item_name: string;
  value: number | null;
  unit: string;
  standard: string;
  is_compliant: boolean;
}

// --- 響應式狀態 ---
const formData = ref<{
  vendor: string;
  report_date: string;
  status: string;
  items: ReportItemForm[];
}>({
  vendor: '',
  report_date: new Date().toISOString().split('T')[0],
  status: '合格',
  items: [], // 檢測項目列表，一開始是空的
});

const isSubmitting = ref(false);
const router = useRouter();

// --- 方法 ---
// 新增「新增一列」的函式
const addItemRow = () => {
  formData.value.items.push({
    id: Date.now(), // 用當前的時間戳來確保 key 的唯一性
    item_name: '',
    value: null,
    unit: '',
    standard: '',
    is_compliant: true,
  });
};

// 新增「移除一列」的函式
const removeItemRow = (id: number) => {
  formData.value.items = formData.value.items.filter(item => item.id !== id);
};

// 提交表單的函式 (已串接 API)
const submitForm = async () => {
  if (isSubmitting.value) return;

  if (!formData.value.vendor || !formData.value.report_date) {
    alert('請填寫廠商名稱和報告日期！');
    return;
  }
  if (formData.value.items.length === 0) {
    alert('請至少新增一筆檢測項目！');
    return;
  }

  isSubmitting.value = true;

  try {
    // 準備要發送到後端的資料 (payload)
    // 我們需要移除前端專用的臨時 id
    const payload = {
      ...formData.value,
      items: formData.value.items.map(({ id, ...rest }) => rest)
    };

    await axios.post('http://localhost:5000/api/v1/wastewater-reports/', payload);
    
    alert('新增報告成功！');
    router.push('/wastewater-reports');

  } catch (error) {
    console.error('儲存報告時發生錯誤:', error);
    alert('儲存失敗，請檢查資料或稍後再試。');
  } finally {
    isSubmitting.value = false;
  }
};

const cancelForm = () => {
    router.push('/wastewater-reports');
}

</script>

<template>
  <div>
    <h1>新增廢水報告</h1>
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
        <div class="item-row item-header">
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
/* ... (大部分樣式不變) ... */
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; }
.items-list { display: flex; flex-direction: column; gap: 1rem; }
.item-row { display: grid; grid-template-columns: 3fr 2fr 1fr 1fr 1.5fr auto; gap: 1rem; align-items: center; }
.item-header { font-weight: 500; color: #334155; font-size: 0.9rem; padding: 0 0.75rem; }
.add-item-btn { margin-top: 1rem; padding: 0.5rem 1rem; border: 1px dashed #0C809F; background-color: transparent; color: #0C809F; cursor: pointer; border-radius: 6px; width: fit-content; font-weight: 500; }
.add-item-btn:hover { background-color: rgba(12, 128, 159, 0.05); }
.delete-item-btn { background-color: #fee2e2; color: #ef4444; border: none; border-radius: 50%; width: 28px; height: 28px; font-size: 20px; line-height: 28px; text-align: center; cursor: pointer; padding: 0; transition: background-color 0.2s; }
.delete-item-btn:hover { background-color: #fecaca; }
.report-form { max-width: 900px; margin-top: 2rem; }
.form-group { margin-bottom: 1.5rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
input[type="text"], input[type="date"], input[type="number"], select { width: 100%; padding: 0.75rem; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; box-sizing: border-box; }
.items-title { margin-top: 2rem; border-bottom: 1px solid #eee; padding-bottom: 0.5rem; }
.form-actions { margin-top: 2rem; display: flex; gap: 1rem; }
button { padding: 0.75rem 1.5rem; border-radius: 8px; border: 1px solid transparent; font-weight: 500; cursor: pointer; }
.btn-primary { background-color: #0C809F; color: white; border-color: #0C809F; }
.btn-primary:disabled { background-color: #94a3b8; cursor: not-allowed; }
.btn-secondary { background-color: #6c757d; color: white; border-color: #6c757d; }
</style>