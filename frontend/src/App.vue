<script setup lang="ts">
// 1. 從 components 資料夾匯入我們剛剛建立的 SampleList 元件
import SampleList from './components/SampleList.vue';
</script>

<template>
  <main>
    <h1>產線紀錄總覽</h1>
    
    <SampleList />
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