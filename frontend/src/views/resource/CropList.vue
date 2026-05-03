<template>
  <div class="crop-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>作物列表</span>
          <el-button type="primary" @click="handleAdd">新增作物</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="作物名称">
          <el-input v-model="searchForm.name" placeholder="请输入作物名称" clearable />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="searchForm.category" placeholder="请选择分类" clearable>
            <el-option label="粮食作物" value="粮食作物" />
            <el-option label="经济作物" value="经济作物" />
            <el-option label="蔬菜" value="蔬菜" />
            <el-option label="水果" value="水果" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="作物名称" width="150" />
        <el-table-column prop="variety" label="品种" width="150" />
        <el-table-column prop="category" label="分类" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.category || '粮食作物' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="growthCycle" label="生长周期(天)" width="120" />
        <el-table-column prop="plantingSeason" label="种植季节" width="120">
          <template #default="{ row }">
            {{ getPlantingSeason(row.plantingRequirements) }}
          </template>
        </el-table-column>
        <el-table-column prop="plantingRequirements" label="种植要求" show-overflow-tooltip />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadData"
        @current-change="loadData"
      />
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑作物' : '新增作物'"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="作物名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入作物名称" />
        </el-form-item>
        <el-form-item label="品种" prop="variety">
          <el-input v-model="form.variety" placeholder="请输入品种" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%">
            <el-option label="粮食作物" value="粮食作物" />
            <el-option label="经济作物" value="经济作物" />
            <el-option label="蔬菜" value="蔬菜" />
            <el-option label="水果" value="水果" />
          </el-select>
        </el-form-item>
        <el-form-item label="生长周期(天)" prop="growthCycle">
          <el-input-number
            v-model="form.growthCycle"
            :min="1"
            :max="365"
            placeholder="请输入生长周期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="种植季节" prop="plantingSeason">
          <el-select v-model="form.plantingSeason" placeholder="请选择种植季节" style="width: 100%">
            <el-option label="春季" value="春季" />
            <el-option label="夏季" value="夏季" />
            <el-option label="秋季" value="秋季" />
            <el-option label="冬季" value="冬季" />
          </el-select>
        </el-form-item>
        <el-form-item label="种植要求" prop="plantingRequirements">
          <el-input
            v-model="form.plantingRequirements"
            type="textarea"
            :rows="4"
            placeholder="请输入种植要求"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { cropApi } from '@/api/crop'

// 响应式数据
const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

// 搜索表单
const searchForm = reactive({
  name: '',
  category: ''
})

// 分页信息
const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

// 表单数据
const form = reactive({
  id: null,
  name: '',
  variety: '',
  category: '',
  growthCycle: null,
  plantingSeason: '',
  plantingRequirements: ''
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入作物名称', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在1到50个字符', trigger: 'blur' }
  ],
  growthCycle: [
    { type: 'number', min: 1, max: 365, message: '生长周期在1-365天之间', trigger: 'blur' }
  ]
}

// 从种植要求中提取种植季节
const getPlantingSeason = (plantingRequirements) => {
  if (!plantingRequirements) return '未知'
  if (plantingRequirements.includes('春季')) return '春季'
  if (plantingRequirements.includes('夏季')) return '夏季'
  if (plantingRequirements.includes('秋季')) return '秋季'
  if (plantingRequirements.includes('冬季')) return '冬季'
  return '未知'
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      name: searchForm.name || undefined,
      category: searchForm.category || undefined
    }
    console.log('正在加载数据，参数:', params)
    const response = await cropApi.getList(params)
    console.log('API响应:', response)
    
    if (response && response.data) {
      tableData.value = response.data.records || []
      pagination.total = response.data.total || 0
      console.log('数据加载成功，共', response.data.total, '条记录')
    } else {
      console.error('API响应格式错误:', response)
      tableData.value = []
      pagination.total = 0
    }
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败: ' + (error.message || '未知错误'))
    tableData.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadData()
}

// 重置
const handleReset = () => {
  searchForm.name = ''
  searchForm.category = ''
  pagination.page = 1
  loadData()
}

// 新增
const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  isEdit.value = true
  Object.assign(form, row)
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该作物吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await cropApi.delete(row.id)
        ElMessage.success('删除成功')
        loadData()
      } catch (error) {
        console.error('删除失败:', error)
      }
    })
    .catch(() => {})
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await cropApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await cropApi.add(form)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        loadData()
      } catch (error) {
        console.error('提交失败:', error)
      }
    }
  })
}

// 对话框关闭
const handleDialogClose = () => {
  formRef.value?.resetFields()
  Object.assign(form, {
    id: null,
    name: '',
    variety: '',
    category: '',
    growthCycle: null,
    plantingSeason: '',
    plantingRequirements: ''
  })
}

// 页面加载时获取数据
onMounted(() => {
  console.log('作物列表页面已加载')
  console.log('当前token:', localStorage.getItem('token'))
  loadData()
})
</script>

<style scoped>
.crop-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.el-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
