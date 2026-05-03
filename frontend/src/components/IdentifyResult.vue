<template>
  <el-card class="identify-result-card" v-if="result">
    <template #header>
      <div class="card-header">
        <span class="title">识别结果</span>
        <el-tag :type="result.success ? 'success' : 'warning'" size="small">
          {{ result.success ? '识别成功' : '识别失败' }}
        </el-tag>
      </div>
    </template>

    <template v-if="result.success">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="病虫害名称">
          <span class="disease-name">{{ result.diseaseName }}</span>
          <el-tag v-if="result.type" :type="result.type === 'disease' ? 'danger' : 'warning'" size="small" style="margin-left: 10px;">
            {{ result.type === 'disease' ? '病害' : '虫害' }}
          </el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="作物类型" v-if="result.crop">
          {{ result.crop }}
        </el-descriptions-item>

        <el-descriptions-item label="严重程度" v-if="result.severity">
          <el-tag :type="getSeverityType(result.severity)" size="small">
            {{ result.severity === '高' ? '高' : result.severity === '中' ? '中' : '低' }}
          </el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="置信度">
          <div class="confidence-container">
            <el-progress
              :percentage="getConfidencePercentage(result.confidence)"
              :color="getConfidenceColor(result.confidence)"
              :stroke-width="20"
              :show-text="false"
            />
            <span class="confidence-value">{{ formatConfidence(result.confidence) }}%</span>
          </div>
        </el-descriptions-item>

        <el-descriptions-item label="匹配特征" v-if="result.matchedFeatures && result.matchedFeatures.length > 0">
          <div class="matched-features">
            <el-tag 
              v-for="(feature, index) in result.matchedFeatures" 
              :key="index"
              size="small"
              type="info"
              style="margin: 2px;"
            >
              {{ feature.type }}: {{ feature.value }}
            </el-tag>
          </div>
        </el-descriptions-item>

        <el-descriptions-item label="防治建议">
          <div class="advice-content">{{ result.treatmentAdvice }}</div>
        </el-descriptions-item>

        <el-descriptions-item label="预防措施" v-if="result.preventionAdvice">
          <div class="advice-content">{{ result.preventionAdvice }}</div>
        </el-descriptions-item>

        <el-descriptions-item label="其他信息" v-if="result.additionalInfo">
          {{ result.additionalInfo }}
        </el-descriptions-item>

        <el-descriptions-item label="其他可能的识别结果" v-if="result.allMatches && result.allMatches.length > 1">
          <div class="other-matches">
            <div 
              v-for="(match, index) in result.allMatches.slice(1)" 
              :key="index"
              class="match-item"
            >
              <span class="match-name">{{ match.name }}</span>
              <el-tag size="small" type="info">{{ match.confidence }}%</el-tag>
            </div>
          </div>
        </el-descriptions-item>
      </el-descriptions>

      <div class="actions">
        <el-button type="primary" @click="handleConfirm">
          确认并保存
        </el-button>
        <el-button @click="handleEdit">
          手动修改
        </el-button>
        <el-button type="danger" @click="handleCancel">
          取消
        </el-button>
      </div>
    </template>

    <template v-else>
      <el-alert
        :title="result.message || 'AI服务暂时不可用'"
        type="warning"
        :closable="false"
        show-icon
      />
      <div class="actions">
        <el-button type="primary" @click="handleManualInput">
          手动输入病虫害信息
        </el-button>
        <el-button @click="handleRetry">
          重试识别
        </el-button>
        <el-button type="danger" @click="handleCancel">
          取消
        </el-button>
      </div>
    </template>
  </el-card>
</template>

<script setup>
const props = defineProps({
  result: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['confirm', 'edit', 'cancel', 'retry', 'manual-input'])

const getConfidencePercentage = (confidence) => {
  const value = Number(confidence)
  if (Number.isNaN(value)) return 0
  return Math.min(100, Math.max(0, value))
}

const formatConfidence = (confidence) => {
  return getConfidencePercentage(confidence).toFixed(2)
}

// 根据置信度返回颜色
const getConfidenceColor = (confidence) => {
  const value = getConfidencePercentage(confidence)
  if (value >= 80) return '#67c23a' // 绿色
  if (value >= 60) return '#e6a23c' // 橙色
  return '#f56c6c' // 红色
}

// 根据严重程度返回标签类型
const getSeverityType = (severity) => {
  if (severity === '高') return 'danger'
  if (severity === '中') return 'warning'
  return 'info'
}

// 确认并保存
const handleConfirm = () => {
  emit('confirm', props.result)
}

// 手动修改
const handleEdit = () => {
  emit('edit', props.result)
}

// 取消
const handleCancel = () => {
  emit('cancel')
}

// 重试识别
const handleRetry = () => {
  emit('retry')
}

// 手动输入
const handleManualInput = () => {
  emit('manual-input')
}
</script>

<script>
export default {
  name: 'IdentifyResult'
}
</script>

<style scoped>
.identify-result-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 16px;
  font-weight: bold;
}

.disease-name {
  font-weight: bold;
  color: #303133;
}

.confidence-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.confidence-value {
  font-weight: bold;
  min-width: 50px;
  text-align: right;
}

.advice-content {
  white-space: pre-wrap;
  line-height: 1.6;
  color: #606266;
}

.matched-features {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.other-matches {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.match-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 10px;
  background: #f5f7fa;
  border-radius: 4px;
}

.match-name {
  font-size: 14px;
  color: #606266;
}

.actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}
</style>
