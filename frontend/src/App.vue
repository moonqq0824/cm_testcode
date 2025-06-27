<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 1. 定義 TypeScript 的型別，讓程式碼更嚴謹
interface Sample {
  id: number;
  line_name: string;
  product_name: string;
  timestamp: string;
  metric_a: number;
  metric_b: number;
  operator: string;
}

// 2. 建立一個「響應式」的變數來存放我們的資料
//    ref() 就像一個魔法盒，裡面的東西一變，畫面就會自動更新
const samples = ref<Sample[]>([]);

// 3. 定義一個非同步函式來抓取資料
const fetchData = async () => {
  try {
    // 使用 aioxs 向我們的後端 API 發送 GET 請求
    const response = await axios.get('http://localhost:5000/api/v1/samples');
    // 將 API 回傳的 data 陣列，存入我們的魔法盒中
    // 注意要用 .value 來存取 ref 的內容
    samples.value = response.data.data;
  } catch (error) {
    console.error('抓取資料時發生錯誤:', error);
    // 在這裡可以加入錯誤處理的邏輯，例如顯示錯誤訊息
  }
};

// 4. 使用 onMounted 生命週期掛鉤
//    這能確保在畫面元件「掛載」到頁面上後，才執行抓取資料的動作
onMounted(() => {
  fetchData();
});
</script>

<template>
  <main>
    <h1>產線紀錄總覽</h1>
    
    <ul>
      <li v-for="sample in samples" :key="sample.id">
        {{ sample.timestamp }} - [{{ sample.line_name }}] - 操作員: {{ sample.operator }}
      </li>
    </ul>
  </main>
</template>

<style scoped>
main {
  padding: 2rem;
}

h1 {
  margin-bottom: 1rem;
}
</style>