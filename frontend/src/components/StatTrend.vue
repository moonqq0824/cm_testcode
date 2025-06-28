<script setup lang="ts">
import { computed } from 'vue';

// 1. 定義這個元件接收的「屬性 (props)」
const props = defineProps({
  current: {
    type: Number,
    required: true,
  },
  previous: {
    type: Number,
    required: true,
  },
});

// 2. 使用「計算屬性 (computed)」來決定趨勢
const trend = computed(() => {
  if (props.current > props.previous) return 'up';
  if (props.current < props.previous) return 'down';
  return 'stable';
});

const difference = computed(() => {
    return (props.current - props.previous).toFixed(2);
});
</script>

<template>
  <div class="trend-indicator" :class="`trend-${trend}`">
    <span v-if="trend === 'up'">▲</span>
    <span v-if="trend === 'down'">▼</span>
    <span v-if="trend !== 'stable'">{{ Math.abs(difference) }}</span>
    <span v-else>- 持平</span>
  </div>
</template>

<style scoped>
.trend-indicator {
  font-size: 0.85rem;
  font-weight: bold;
}
.trend-up {
  color: #10b981; /* 綠色 */
}
.trend-down {
  color: #ef4444; /* 紅色 */
}
.trend-stable {
    color: #64748b; /* 灰色 */
}
</style>