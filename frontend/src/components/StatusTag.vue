<template>
  <el-tag :type="tagType" :effect="effect">
    {{ displayText }}
  </el-tag>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: [String, Number],
    required: true
  },
  type: {
    type: String,
    default: 'default' // default | plan | quality | severity
  }
})

// 根据类型获取标签样式和文本
const { tagType, displayText } = computed(() => {
  switch (props.type) {
    case 'plan':
      // 种植计划状态
      const planMap = {
        '未开始': { type: 'info', text: '未开始' },
        '进行中': { type: 'success', text: '进行中' },
        '已完成': { type: '', text: '已完成' }
      }
      return planMap[props.status] || { type: 'info', text: props.status }

    case 'quality':
      // 品质等级
      const qualityMap = {
        优: { type: 'success', text: '优' },
        良: { type: 'primary', text: '良' },
        中: { type: 'warning', text: '中' },
        差: { type: 'danger', text: '差' }
      }
      return qualityMap[props.status] || { type: 'info', text: props.status }

    case 'severity':
      // 严重程度
      const severityMap = {
        轻度: { type: 'success', text: '轻度' },
        中度: { type: 'warning', text: '中度' },
        重度: { type: 'danger', text: '重度' }
      }
      return severityMap[props.status] || { type: 'info', text: props.status }

    case 'material':
      // 农资类型
      const materialMap = {
        化肥: { type: 'success', text: '化肥' },
        农药: { type: 'warning', text: '农药' },
        种子: { type: 'primary', text: '种子' },
        其他: { type: 'info', text: '其他' }
      }
      return materialMap[props.status] || { type: 'info', text: props.status }

    case 'category':
      // 作物分类
      const categoryMap = {
        粮食作物: { type: 'success', text: '粮食作物' },
        经济作物: { type: 'primary', text: '经济作物' },
        蔬菜: { type: 'warning', text: '蔬菜' },
        水果: { type: 'danger', text: '水果' }
      }
      return categoryMap[props.status] || { type: 'info', text: props.status }

    case 'factor':
      // 影响因素
      const factorMap = {
        适宜: { type: 'success', text: '适宜' },
        良好: { type: 'success', text: '良好' },
        轻微: { type: 'success', text: '轻微' },
        一般: { type: 'warning', text: '一般' },
        中度: { type: 'warning', text: '中度' },
        不适宜: { type: 'danger', text: '不适宜' },
        严重: { type: 'danger', text: '严重' }
      }
      return factorMap[props.status] || { type: 'info', text: props.status }

    default:
      return { type: 'info', text: props.status }
  }
}).value

// 标签效果
const effect = computed(() => {
  return 'light'
})
</script>

<style scoped>
/* 状态标签样式 */
:deep(.el-tag) {
  font-weight: 500;
}
</style>
