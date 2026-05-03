<template>
  <div class="pest-image-identification">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>病虫害图片识别</span>
        </div>
      </template>

      <el-row :gutter="20">
        <!-- 左侧：图片上传区域 -->
        <el-col :span="12">
          <div class="upload-section">
            <h3>上传图片</h3>
            <p class="description">请上传病虫害图片，系统将自动识别病虫害类型</p>

            <div class="upload-area">
              <ImageUpload v-model="imageUrl" @success="handleImageUploadSuccess" />
            </div>

            <div v-if="imageUrl" class="image-preview-section">
              <h4>图片预览</h4>
              <el-image
                :src="imageUrl"
                fit="contain"
                style="width: 100%; max-height: 400px; border-radius: 4px;"
                :preview-src-list="[imageUrl]"
                preview-teleported
              />
            </div>

            <div v-if="imageUrl" class="action-buttons">
              <el-button
                type="primary"
                size="large"
                :loading="identifying"
                @click="handleIdentify"
                :disabled="!imageUrl"
              >
                {{ identifying ? '识别中...' : '开始识别' }}
              </el-button>
              <el-button
                size="large"
                @click="handleReset"
              >
                重新上传
              </el-button>
            </div>
          </div>
        </el-col>

        <!-- 右侧：识别结果区域 -->
        <el-col :span="12">
          <div class="result-section">
            <h3>识别结果</h3>

            <!-- 未识别状态 -->
            <div v-if="!identifyResult" class="no-result">
              <el-empty description="请先上传图片并进行识别">
                <template #image>
                  <el-icon :size="100" color="#909399">
                    <Picture />
                  </el-icon>
                </template>
              </el-empty>
            </div>

            <!-- 识别成功 -->
            <div v-else-if="identifyResult.success" class="result-content">
              <IdentifyResult
                :result="identifyResult"
                @confirm="handleConfirmResult"
                @edit="handleEditResult"
                @cancel="handleCancelResult"
                @retry="handleRetryIdentify"
                @manual-input="handleManualInput"
              />
            </div>

            <!-- 识别失败 -->
            <div v-else class="result-failed">
              <el-alert
                :title="identifyResult.message || '识别失败'"
                type="warning"
                :closable="false"
                show-icon
              >
                <template #default>
                  <p>{{ identifyResult.message || 'AI服务暂时不可用，请稍后重试' }}</p>
                  <div class="failed-actions">
                    <el-button type="primary" @click="handleRetryIdentify">
                      重试识别
                    </el-button>
                    <el-button @click="handleManualInput">
                      手动输入信息
                    </el-button>
                  </div>
                </template>
              </el-alert>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Picture } from '@element-plus/icons-vue'
import ImageUpload from '@/components/ImageUpload.vue'
import IdentifyResult from '@/components/IdentifyResult.vue'
import axios from 'axios'
import { extractEnhancedFeatures, matchWithKnowledgeBase, evaluateEnhancedRelevance } from '@/utils/featureExtraction'

// 响应式数据
const imageUrl = ref('')
const identifying = ref(false)
const identifyResult = ref(null)

// 图片上传成功
const handleImageUploadSuccess = (fileInfo) => {
  console.log('图片上传成功:', fileInfo)
  ElMessage.success('图片上传成功')
  // 自动触发识别
  setTimeout(() => {
    handleIdentify()
  }, 500)
}

// AI识别 - 使用后端MobileNetV3模型
const handleIdentify = async () => {
  if (!imageUrl.value) {
    ElMessage.warning('请先上传图片')
    return
  }

  identifying.value = true
  
  try {
    // 将图片转为Base64发送给后端AI服务
    const imageBase64 = await convertImageToBase64(imageUrl.value)
    
    // 获取当前种植计划ID（默认1）
    const planId = 1
    
    // 调用后端识别接口 → 后端调用AI服务 → MobileNetV3模型
    const token = localStorage.getItem('token')
    const response = await axios.post('/api/pest-records/diagnose', {
      planId: planId,
      imageBase64: imageBase64
    }, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.data.code === 200) {
      const data = response.data.data
      identifyResult.value = {
        success: true,
        diseaseName: data.pestName || '未知病虫害',
        confidence: data.confidence || 0,
        treatmentAdvice: data.treatmentMethods || '',
        preventionAdvice: data.preventionMethods || '',
        severity: data.severity || '未知',
        type: data.pestType || '病害',
        crop: data.cropType || '',
        highConfidence: data.highConfidence || false,
        additionalInfo: data.highConfidence 
          ? '深度学习模型识别 - MobileNetV3 (PlantVillage 38类)' 
          : '深度学习模型识别 - 置信度较低，建议人工确认'
      }
      ElMessage.success(`识别完成：${data.pestName}（置信度${data.confidence?.toFixed(1)}%）`)
    } else {
      identifyResult.value = {
        success: false,
        message: response.data.message || '识别失败'
      }
      ElMessage.error('识别失败')
    }
  } catch (error) {
    console.error('识别失败:', error)
    identifyResult.value = {
      success: false,
      message: 'AI服务暂时不可用，请稍后重试'
    }
    ElMessage.error('识别失败，请稍后重试')
  } finally {
    identifying.value = false
  }
}

// 将图片转换为Base64
const convertImageToBase64 = (url) => {
  return new Promise((resolve, reject) => {
    if (url.startsWith('data:')) {
      const base64 = url.split(',')[1]
      resolve(base64)
      return
    }
    
    const img = new Image()
    img.crossOrigin = 'anonymous'
    img.onload = () => {
      const canvas = document.createElement('canvas')
      canvas.width = img.width
      canvas.height = img.height
      const ctx = canvas.getContext('2d')
      ctx.drawImage(img, 0, 0)
      const dataUrl = canvas.toDataURL('image/jpeg', 0.8)
      const base64 = dataUrl.split(',')[1]
      resolve(base64)
    }
    img.onerror = () => reject(new Error('图片加载失败'))
    img.src = url
  })
}

// 图片预筛选 - 检查图片是否与病虫害相关
const checkImageRelevance = async (imageUrl) => {
  try {
    // 使用本地图片分析进行预筛选
    if (imageUrl.startsWith('blob:')) {
      return await analyzeLocalImage(imageUrl)
    }
    
    // 如果是服务器图片，这里可以调用后端的预筛选接口
    // 暂时返回true，允许继续识别
    return true
  } catch (error) {
    console.error('图片预筛选失败:', error)
    // 预筛选失败时，允许继续识别
    return true
  }
}

// 从URL提取增强特征
const extractEnhancedFeaturesFromUrl = (imageUrl) => {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.crossOrigin = 'anonymous'
    
    img.onload = () => {
      try {
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext('2d')
        canvas.width = img.width
        canvas.height = img.height
        
        ctx.drawImage(img, 0, 0)
        
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
        const data = imageData.data
        
        const enhancedFeatures = extractEnhancedFeatures(data, canvas.width, canvas.height)
        
        console.log('增强特征提取结果:', enhancedFeatures)
        resolve(enhancedFeatures)
      } catch (error) {
        console.error('增强特征提取失败:', error)
        reject(error)
      }
    }
    
    img.onerror = () => {
      console.error('图片加载失败')
      reject(new Error('图片加载失败'))
    }
    
    img.src = imageUrl
  })
}

// 分析本地图片的相关性
const analyzeLocalImage = async (imageUrl) => {
  return new Promise((resolve) => {
    const img = new Image()
    img.crossOrigin = 'anonymous'
    
    img.onload = () => {
      // 创建Canvas分析图片特征
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')
      canvas.width = img.width
      canvas.height = img.height
      
      try {
        ctx.drawImage(img, 0, 0)
        
        // 获取图片像素数据
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
        const data = imageData.data
        
        // 提取增强特征
        const enhancedFeatures = extractEnhancedFeatures(data, canvas.width, canvas.height)
        
        // 判断是否与病虫害相关（使用增强版评估）
        const relevanceResult = evaluateEnhancedRelevance(enhancedFeatures)
        
        console.log('增强特征分析结果:', enhancedFeatures)
        console.log('相关性判断:', relevanceResult)
        
        resolve(relevanceResult.isRelevant)
      } catch (error) {
        console.error('图片分析失败:', error)
        resolve(true) // 分析失败时允许继续
      }
    }
    
    img.onerror = () => {
      console.error('图片加载失败')
      resolve(true) // 加载失败时允许继续
    }
    
    img.src = imageUrl
  })
}

// 分析图片特征
const analyzeImageFeatures = (data, width, height) => {
  // 提取颜色特征
  const colorFeatures = extractColorFeatures(data)
  
  // 提取纹理特征
  const textureFeatures = extractTextureFeatures(data, width, height)
  
  // 提取亮度特征
  const brightnessFeatures = extractBrightnessFeatures(data)
  
  return {
    colors: colorFeatures,
    texture: textureFeatures,
    brightness: brightnessFeatures
  }
}

// 提取颜色特征
const extractColorFeatures = (data) => {
  let greenPixels = 0
  let yellowPixels = 0
  let brownPixels = 0
  let totalPixels = data.length / 4
  
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i]
    const g = data[i + 1]
    const b = data[i + 2]
    
    // 检测绿色（健康叶片）
    if (g > r && g > b && g > 100) {
      greenPixels++
    }
    
    // 检测黄色（病害症状）
    if (r > 200 && g > 180 && b < 100) {
      yellowPixels++
    }
    
    // 检测褐色（坏死斑点）
    if (r > 100 && r < 180 && g > 80 && g < 150 && b < 100) {
      brownPixels++
    }
  }
  
  return {
    greenRatio: greenPixels / totalPixels,
    yellowRatio: yellowPixels / totalPixels,
    brownRatio: brownPixels / totalPixels,
    totalPixels
  }
}

// 提取纹理特征
const extractTextureFeatures = (data, width, height) => {
  let edgeCount = 0
  let contrastSum = 0
  
  // 简化的边缘检测
  for (let y = 1; y < height - 1; y++) {
    for (let x = 1; x < width - 1; x++) {
      const idx = (y * width + x) * 4
      const brightness = (data[idx] + data[idx + 1] + data[idx + 2]) / 3
      
      const rightIdx = (y * width + (x + 1)) * 4
      const rightBrightness = (data[rightIdx] + data[rightIdx + 1] + data[rightIdx + 2]) / 3
      
      const diff = Math.abs(brightness - rightBrightness)
      contrastSum += diff
      
      if (diff > 30) {
        edgeCount++
      }
    }
  }
  
  return {
    edgeRatio: edgeCount / (width * height),
    avgContrast: contrastSum / (width * height)
  }
}

// 提取亮度特征
const extractBrightnessFeatures = (data) => {
  let totalBrightness = 0
  let darkPixels = 0
  let brightPixels = 0
  
  for (let i = 0; i < data.length; i += 4) {
    const brightness = (data[i] + data[i + 1] + data[i + 2]) / 3
    totalBrightness += brightness
    
    if (brightness < 50) {
      darkPixels++
    } else if (brightness > 200) {
      brightPixels++
    }
  }
  
  const avgBrightness = totalBrightness / (data.length / 4)
  
  return {
    avgBrightness,
    darkRatio: darkPixels / (data.length / 4),
    brightRatio: brightPixels / (data.length / 4)
  }
}

// 评估图片相关性
const evaluateRelevance = (features) => {
  const { colors, texture, brightness } = features
  
  // 规则1：图片应该有一定的绿色（植物叶片）
  const hasVegetation = colors.greenRatio > 0.3
  
  // 规则2：应该有一些病害症状的颜色（黄色、褐色）
  const hasDiseaseSymptoms = colors.yellowRatio > 0.05 || colors.brownRatio > 0.05
  
  // 规则3：图片不能太暗或太亮
  const properLighting = brightness.avgBrightness > 50 && brightness.avgBrightness < 220
  
  // 规则4：应该有一定的纹理（叶片、斑点等）
  const hasTexture = texture.edgeRatio > 0.1
  
  // 规则5：不能是纯色图片（如纯绿色背景）
  const notSolidColor = colors.greenRatio < 0.95
  
  // 综合判断
  const relevanceScore = 
    (hasVegetation ? 1 : 0) * 0.3 +
    (hasDiseaseSymptoms ? 1 : 0) * 0.3 +
    (properLighting ? 1 : 0) * 0.15 +
    (hasTexture ? 1 : 0) * 0.15 +
    (notSolidColor ? 1 : 0) * 0.1
  
  console.log('相关性评分:', relevanceScore)
  console.log('详细判断:', {
    hasVegetation,
    hasDiseaseSymptoms,
    properLighting,
    hasTexture,
    notSolidColor
  })
  
  // 相关性评分阈值：0.4以上认为是相关图片
  return relevanceScore > 0.4
}

// 重置
const handleReset = () => {
  imageUrl.value = ''
  identifyResult.value = null
}

// 确认识别结果
const handleConfirmResult = (result) => {
  if (result && result.success) {
    ElMessage.success(`已确认识别结果：${result.diseaseName}`)
    // 这里可以添加将结果复制到剪贴板等操作
  }
}

// 编辑识别结果
const handleEditResult = (result) => {
  if (result && result.success) {
    ElMessage.info('您可以手动修改识别结果')
  }
}

// 取消识别结果
const handleCancelResult = () => {
  identifyResult.value = null
}

// 重试识别
const handleRetryIdentify = () => {
  identifyResult.value = null
  handleIdentify()
}

// 手动输入
const handleManualInput = () => {
  ElMessage.info('请手动输入病虫害信息')
  // 这里可以打开一个手动输入的对话框
}
</script>

<script>
export default {
  name: 'PestImageIdentification'
}
</script>

<style scoped>
.pest-image-identification {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 18px;
  font-weight: bold;
}

.upload-section,
.result-section {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  min-height: 500px;
}

h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #303133;
  font-size: 16px;
}

.description {
  color: #606266;
  margin-bottom: 20px;
  font-size: 14px;
}

.upload-area {
  margin-bottom: 20px;
}

.image-preview-section {
  margin-top: 20px;
}

.image-preview-section h4 {
  margin-bottom: 10px;
  color: #606266;
  font-size: 14px;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.no-result {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
}

.result-content {
  height: 100%;
}

.result-failed {
  padding: 20px;
}

.failed-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}
</style>
