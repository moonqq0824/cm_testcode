<script setup lang="ts">
import { ref } from 'vue';

// 預先定義表單資料的結構
const formData = ref({
  vendor: '',
  report_date: new Date().toISOString().split('T')[0], // 預設為今天
  status: '合格',
  items: [],
});
</script>

<template>
  <div>
    <h1>新增廢水報告</h1>
    <form class="report-form">
      <div class="form-group">
        <label for="vendor">廠商名稱</label>
        <input type="text" id="vendor" v-model="formData.vendor" />
      </div>

      <div class="form-group">
        <label for="report_date">報告日期</label>
        <input type="date" id="report_date" v-model="formData.report_date" />
      </div>

      <div class="form-group">
        <label for="status">總體狀態</label>
        <select id="status" v-model="formData.status">
          <option>合格</option>
          <option>部分項目不合格</option>
          <option>追蹤中</option>
        </select>
      </div>

      <h3 class="items-title">檢測項目</h3>
      <div class="items-placeholder">(動態項目表格區域)</div>

      <div class="form-actions">
        <button type="submit" class="btn-primary">儲存報告</button>
        <button type="button" class="btn-secondary">取消</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.report-form {
  max-width: 800px;
  margin-top: 2rem;
}
.form-group {
  margin-bottom: 1.5rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
input[type='text'],
input[type='date'],
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

.items-title {
  margin-top: 2rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}
.items-placeholder {
  padding: 2rem;
  text-align: center;
  color: #999;
  border: 2px dashed #ddd;
  border-radius: 8px;
  margin-top: 1rem;
}
.form-actions {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
}
button {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: 1px solid transparent;
  font-weight: 500;
  cursor: pointer;
}
.btn-primary {
  background-color: #0c809f;
  color: white;
  border-color: #0c809f;
}
.btn-secondary {
  background-color: #6c757d;
  color: white;
  border-color: #6c757d;
}
</style>
