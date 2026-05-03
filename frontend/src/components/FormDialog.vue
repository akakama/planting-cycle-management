<template>
  <el-dialog
    :model-value="visible"
    :title="title"
    :width="width"
    :close-on-click-modal="false"
    @update:model-value="handleVisibleChange"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      :label-width="labelWidth"
      @submit.prevent
    >
      <slot></slot>
    </el-form>

    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" :loading="loading" @click="handleConfirm">
        确定
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  width: {
    type: String,
    default: '600px'
  },
  labelWidth: {
    type: String,
    default: '100px'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'confirm', 'cancel'])

const formRef = ref(null)
const formData = defineModel('formData')
const formRules = defineModel('formRules')

const handleVisibleChange = (value) => {
  emit('update:visible', value)
}

const handleConfirm = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    emit('confirm')
  } catch (error) {
    // 验证失败，不触发confirm事件
  }
}

const handleCancel = () => {
  emit('cancel')
  emit('update:visible', false)
}

// 暴露表单引用，供父组件调用
defineExpose({
  formRef,
  resetFields: () => {
    formRef.value?.resetFields()
  },
  validate: () => {
    return formRef.value?.validate()
  }
})
</script>

<style scoped>
/* 对话框样式优化 */
:deep(.el-dialog__header) {
  padding: 20px 20px 10px;
  border-bottom: 1px solid #e4e7ed;
}

:deep(.el-dialog__body) {
  padding: 20px;
  max-height: 60vh;
  overflow-y: auto;
}

:deep(.el-dialog__footer) {
  padding: 10px 20px 20px;
  border-top: 1px solid #e4e7ed;
}
</style>
