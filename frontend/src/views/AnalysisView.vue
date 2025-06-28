<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// 1. 告訴 Chart.js 我們要使用哪些元件
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

// 2. 定義 Chart.js 需要的資料結構的初始狀態
const chartData = ref({
  labels: [],
  datasets: []
});

// 定義圖表的設定選項
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: '產線指標 A 交叉比對'
    }
  }
});

const isLoading = ref(true);

// 3. 抓取圖表專用的 API 資料
const fetchChartData = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get('http://localhost:5000/api/v1/charts/line-comparison');
    chartData.value = response.data;
  } catch (error) {
    console.error('抓取圖表資料時發生錯誤:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchChartData);
</script>

<template>
  <div>
    <h1>產線分析圖表</h1>
    
    <div class="chart-container">
      <div v-if="isLoading">正在載入圖表...</div>
      <Line v-else :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  position: relative;
  height: 60vh; /* 給圖表一個高度，例如視窗高度的 60% */
  width: 100%;
}
</style>