<script setup lang="ts">
// 目前不需要任何 script 邏輯
</script>

<template>
  <aside class="sidebar">
    <h1 class="sidebar-title">數據平台</h1>
    <nav class="nav-menu">
      <a href="#" class="nav-link active">產線紀錄總覽</a>
      <a href="#" class="nav-link">首頁儀表板</a>
      <a href="#" class="nav-link">產線分析圖表</a>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  background-color: #F7FAFC;
  border-right: 1px solid #e2e8f0;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.sidebar-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #2D3748;
}

.nav-menu {
  display: flex;
  flex-direction: column;
}

.nav-link {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  color: #4a5568;
  margin-bottom: 0.5rem;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background-color: #e2e8f0;
}

.nav-link.active {
  background-color: #0C809F;
  color: white;
  font-weight: bold;
}
</style>