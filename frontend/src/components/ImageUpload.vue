<template>
  <div class="image-upload">
    <el-upload
      :action="uploadUrl"
      :before-upload="beforeUpload"
      :on-success="handleSuccess"
      :on-error="handleError"
      :on-progress="handleProgress"
      :show-file-list="false"
      accept=".jpg,.jpeg,.png"
      :headers="uploadHeaders"
      :http-request="customUpload"
    >
      <el-button type="primary" :loading="uploading" :disabled="uploading">
        {{ uploading ? '上传中...' : '上传图片' }}
      </el-button>
    </el-upload>

    <div v-if="imageUrl" class="image-preview">
      <el-image
        :src="imageUrl"
        fit="cover"
        style="width: 200px; height: 200px; border-radius: 4px;"
      />
      <el-button
        type="danger"
        size="small"
        @click="handleRemove"
        style="margin-left: 10px;"
      >
        删除
      </el-button>
    </div>

    <div v-if="uploading" class="upload-progress">
      <el-progress :percentage="uploadProgress" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const uploadUrl = '/api/file/upload'
const uploadHeaders = {
  'Authorization': `Bearer ${localStorage.getItem('token')}`
}

const uploading = ref(false)
const uploadProgress = ref(0)
const imageUrl = ref(props.modelValue)

// 自定义上传方法：读取为 data URL，后续可直接提取 Base64 调用识别接口。
const customUpload = (options) => {
  const { file, onProgress, onSuccess, onError } = options

  // 先验证文件
  const isImage = ['image/jpeg', 'image/jpg', 'image/png'].includes(file.type)
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只支持JPG、JPEG、PNG格式的图片')
    onError(new Error('文件格式不支持'))
    return
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过10MB')
    onError(new Error('文件大小超过限制'))
    return
  }

  uploading.value = true

  const reader = new FileReader()

  reader.onprogress = (event) => {
    if (event.lengthComputable) {
      onProgress({ percent: Math.round((event.loaded / event.total) * 100) }, file)
    }
  }

  reader.onload = () => {
    uploading.value = false
    uploadProgress.value = 100

    const dataUrl = reader.result

    ElMessage.success('图片读取成功')
    onSuccess({
      code: 200,
      data: {
        url: dataUrl,
        filename: file.name
      }
    })
  }

  reader.onerror = () => {
    uploading.value = false
    uploadProgress.value = 0
    ElMessage.error('图片读取失败')
    onError(reader.error || new Error('图片读取失败'))
  }

  reader.readAsDataURL(file)
}

// 上传前验证
const beforeUpload = (file) => {
  const isImage = ['image/jpeg', 'image/jpg', 'image/png'].includes(file.type)
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只支持JPG、JPEG、PNG格式的图片')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过10MB')
    return false
  }

  uploading.value = true
  uploadProgress.value = 0
  return true
}

// 上传进度
const handleProgress = (event) => {
  if (typeof event.percent === 'number') {
    uploadProgress.value = Math.floor(event.percent)
    return
  }

  if (event.total) {
    uploadProgress.value = Math.floor((event.loaded / event.total) * 100)
  }
}

// 上传成功
const handleSuccess = (response) => {
  uploading.value = false
  uploadProgress.value = 0

  if (response.code === 200 && response.data) {
    const newImageUrl = response.data.url
    imageUrl.value = newImageUrl
    emit('update:modelValue', newImageUrl)
    emit('success', response.data)
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

// 上传失败
const handleError = (error) => {
  uploading.value = false
  uploadProgress.value = 0
  console.error('上传失败:', error)
  ElMessage.error('图片上传失败')
}

// 删除图片
const handleRemove = () => {
  imageUrl.value = ''
  emit('update:modelValue', '')
}

// 监听modelValue变化
watch(() => props.modelValue, (newVal) => {
  imageUrl.value = newVal
})
</script>

<script>
export default {
  name: 'ImageUpload'
}
</script>

<style scoped>
.image-upload {
  display: inline-block;
}

.image-preview {
  margin-top: 10px;
  display: flex;
  align-items: center;
}

.upload-progress {
  margin-top: 10px;
  width: 300px;
}
</style>
