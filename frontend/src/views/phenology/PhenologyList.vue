<template>
  <div class="phenology-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>物候期记录</span>
          <el-button type="primary" @click="handleAdd">新增记录</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="种植计划">
          <el-select v-model="searchForm.planId" placeholder="请选择种植计划" clearable filterable>
            <el-option
              v-for="plan in planOptions"
              :key="plan.id"
              :label="getPlanLabel(plan)"
              :value="plan.id"
            />
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
        <el-table-column label="种植计划" width="200">
          <template #default="{ row }">
            {{ getPlanDisplay(row.planId) }}
          </template>
        </el-table-column>
        <el-table-column prop="phenologyName" label="物候期阶段" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.phenologyName }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="recordDate" label="记录日期" width="120" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
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
      :title="isEdit ? '编辑物候期记录' : '新增物候期记录'"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="120px">
        <el-form-item label="种植计划" prop="planId">
          <el-select v-model="form.planId" placeholder="请选择种植计划" style="width: 100%" filterable>
            <el-option
              v-for="plan in planOptions"
              :key="plan.id"
              :label="getPlanLabel(plan)"
              :value="plan.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="物候期阶段" prop="phenologyName">
          <el-select v-model="form.phenologyName" placeholder="请选择物候期阶段" style="width: 100%">
            <el-option label="播种期" value="播种期" />
            <el-option label="发芽期" value="发芽期" />
            <el-option label="出苗期" value="出苗期" />
            <el-option label="秧苗期" value="秧苗期" />
            <el-option label="定植期" value="定植期" />
            <el-option label="分蘖期" value="分蘖期" />
            <el-option label="拔节期" value="拔节期" />
            <el-option label="抽穗期" value="抽穗期" />
            <el-option label="开花期" value="开花期" />
            <el-option label="灌浆期" value="灌浆期" />
            <el-option label="结果期" value="结果期" />
            <el-option label="成熟期" value="成熟期" />
          </el-select>
        </el-form-item>
        <el-form-item label="记录日期" prop="recordDate">
          <el-date-picker
            v-model="form.recordDate"
            type="date"
            placeholder="请选择记录日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入描述"
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
import { phenologyApi } from '@/api/phenology'
import { plantingPlanApi } from '@/api/plantingPlan'
import { cropApi } from '@/api/crop'
import { plotApi } from '@/api/plot'

// 响应式数据
const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const planOptions = ref([])
const cropMap = ref({})
const plotMap = ref({})

// 搜索表单
const searchForm = reactive({
  planId: null
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
  planId: null,
  phenologyName: '',
  recordDate: '',
  description: ''
})

// 表单验证规则
const formRules = {
  planId: [{ required: true, message: '请选择种植计划', trigger: 'change' }],
  phenologyName: [{ required: true, message: '请选择物候期阶段', trigger: 'change' }],
  recordDate: [{ required: true, message: '请选择记录日期', trigger: 'change' }]
}

// 获取种植计划标签
const getPlanLabel = (plan) => {
  const cropName = cropMap.value[plan.cropId] || '未知作物'
  const plotName = plotMap.value[plan.plotId] || '未知地块'
  return `${cropName} - ${plotName}`
}

// 获取种植计划显示名称
const getPlanDisplay = (planId) => {
  const plan = planOptions.value.find(p => p.id === planId)
  if (plan) {
    return getPlanLabel(plan)
  }
  return '未知计划'
}

// 加载作物和地块数据
const loadCropAndPlotData = async () => {
  try {
    const [cropRes, plotRes] = await Promise.all([
      cropApi.getList({ page: 1, size: 1000 }),
      plotApi.getList({ page: 1, size: 1000 })
    ])
    
    // 构建作物映射
    const crops = cropRes.data.records || []
    crops.forEach(crop => {
      cropMap.value[crop.id] = crop.name
    })
    
    // 构建地块映射
    const plots = plotRes.data.records || []
    plots.forEach(plot => {
      plotMap.value[plot.id] = plot.name || plot.plotName
    })
  } catch (error) {
    console.error('加载作物和地块数据失败:', error)
  }
}

// 加载种植计划选项
const loadPlanOptions = async () => {
  try {
    const response = await plantingPlanApi.getList({ page: 1, size: 1000 })
    planOptions.value = response.data.records
  } catch (error) {
    console.error('加载种植计划选项失败:', error)
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      planId: searchForm.planId || undefined
    }
    const response = await phenologyApi.getList(params)
    tableData.value = response.data.records
    pagination.total = response.data.total
  } catch (error) {
    console.error('加载数据失败:', error)
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
  searchForm.planId = null
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
  ElMessageBox.confirm('确定要删除该物候期记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await phenologyApi.delete(row.id)
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
          await phenologyApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await phenologyApi.add(form)
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
    planId: null,
    phenologyName: '',
    recordDate: '',
    description: ''
  })
}

// 页面加载时获取数据
onMounted(async () => {
  await loadCropAndPlotData()
  await loadPlanOptions()
  loadData()
})
</script>

<style scoped>
.phenology-list {
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
