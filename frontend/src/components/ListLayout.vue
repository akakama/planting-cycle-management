<template>
  <div class="list-layout">
    <el-card>
      <template #header>
        <div class="list-header">
          <span class="list-title">{{ title }}</span>
          <el-button v-if="showAdd" type="primary" @click="$emit('add')">
            新增
          </el-button>
        </div>
      </template>

      <!-- 搜索栏插槽 -->
      <div v-if="$slots.search" class="search-section">
        <slot name="search"></slot>
      </div>

      <!-- 表格内容插槽 -->
      <div class="table-section">
        <slot></slot>
      </div>

      <!-- 分页器插槽 -->
      <div v-if="$slots.pagination" class="pagination-section">
        <slot name="pagination"></slot>
      </div>
    </el-card>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  showAdd: {
    type: Boolean,
    default: false
  }
})

defineEmits(['add'])
</script>

<style scoped>
.list-layout {
  padding: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.list-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.search-section {
  margin-bottom: 20px;
}

.table-section {
  margin-bottom: 20px;
}

.pagination-section {
  display: flex;
  justify-content: flex-end;
}
</style>
