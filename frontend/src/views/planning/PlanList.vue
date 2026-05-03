<template>
  <div class="plan-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>种植计划列表</span>
          <el-button type="primary" @click="handleAdd">新增种植计划</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="作物">
          <el-select v-model="searchForm.cropId" placeholder="请选择作物" clearable filterable>
            <el-option
              v-for="crop in cropOptions"
              :key="crop.id"
              :label="crop.name"
              :value="crop.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="地块">
          <el-select v-model="searchForm.plotId" placeholder="请选择地块" clearable filterable>
            <el-option
              v-for="plot in plotOptions"
              :key="plot.id"
              :label="plot.name"
              :value="plot.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="未开始" value="未开始" />
            <el-option label="进行中" value="进行中" />
            <el-option label="已完成" value="已完成" />
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
        <el-table-column prop="cropName" label="作物名称" width="120" />
        <el-table-column prop="plotName" label="地块名称" width="120" />
        <el-table-column prop="plantingDate" label="种植日期" width="120" />
        <el-table-column prop="expectedHarvestDate" label="预计采收日期" width="120" />
        <el-table-column prop="plantingArea" label="种植面积(亩)" width="120" />
        <el-table-column prop="expectedYield" label="预计产量(kg)" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
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
      :title="isEdit ? '编辑种植计划' : '新增种植计划'"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="120px">
        <el-form-item label="作物" prop="cropId">
          <el-select v-model="form.cropId" placeholder="请选择作物" style="width: 100%" filterable>
            <el-option
              v-for="crop in cropOptions"
              :key="crop.id"
              :label="crop.name"
              :value="crop.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="地块" prop="plotId">
          <el-select v-model="form.plotId" placeholder="请选择地块" style="width: 100%" filterable>
            <el-option
              v-for="plot in plotOptions"
              :key="plot.id"
              :label="plot.name"
              :value="plot.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="种植日期" prop="plantingDate">
          <el-date-picker
            v-model="form.plantingDate"
            type="date"
            placeholder="请选择种植日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="预计采收日期" prop="expectedHarvestDate">
          <el-date-picker
            v-model="form.expectedHarvestDate"
            type="date"
            placeholder="请选择预计采收日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="种植面积(亩)" prop="plantingArea">
          <el-input-number
            v-model="form.plantingArea"
            :min="0"
            :max="10000"
            :precision="2"
            placeholder="请输入种植面积"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="预计产量(kg)" prop="expectedYield">
          <el-input-number
            v-model="form.expectedYield"
            :min="0"
            :max="1000000"
            :precision="2"
            placeholder="请输入预计产量"
            style="width: 100%"
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
import { plantingPlanApi } from '@/api/plantingPlan'
import { cropApi } from '@/api/crop'
import { plotApi } from '@/api/plot'

// 响应式数据
const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const cropOptions = ref([])
const plotOptions = ref([])

// 搜索表单
const searchForm = reactive({
  cropId: null,
  plotId: null,
  status: ''
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
  cropId: null,
  plotId: null,
  plantingDate: '',
  expectedHarvestDate: '',
  plantingArea: null,
  expectedYield: null
})

// 表单验证规则
const formRules = {
  cropId: [{ required: true, message: '请选择作物', trigger: 'change' }],
  plotId: [{ required: true, message: '请选择地块', trigger: 'change' }],
  plantingDate: [{ required: true, message: '请选择种植日期', trigger: 'change' }],
  expectedHarvestDate: [{ required: true, message: '请选择预计采收日期', trigger: 'change' }]
}

// 获取状态标签类型
const getStatusType = (status) => {
  const typeMap = {
    '未开始': 'info',
    '进行中': 'success',
    '已完成': ''
  }
  return typeMap[status] || 'info'
}

// 加载作物选项
const loadCropOptions = async () => {
  try {
    const response = await cropApi.getList({ page: 1, size: 1000 })
    cropOptions.value = response.data.records
  } catch (error) {
    console.error('加载作物选项失败:', error)
  }
}

// 加载地块选项
const loadPlotOptions = async () => {
  try {
    const response = await plotApi.getList({ page: 1, size: 1000 })
    plotOptions.value = response.data.records
  } catch (error) {
    console.error('加载地块选项失败:', error)
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      cropId: searchForm.cropId || undefined,
      plotId: searchForm.plotId || undefined,
      status: searchForm.status || undefined
    }
    const response = await plantingPlanApi.getList(params)
    
    // 填充作物名称和地块名称
    const records = response.data.records || []
    for (const record of records) {
      // 查找作物名称
      const crop = cropOptions.value.find(c => c.id === record.cropId)
      record.cropName = crop ? crop.name : '未知作物'
      
      // 查找地块名称
      const plot = plotOptions.value.find(p => p.id === record.plotId)
      record.plotName = plot ? plot.name : '未知地块'
    }
    
    tableData.value = records
    pagination.total = response.data.total
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败: ' + (error.message || '未知错误'))
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
  searchForm.cropId = null
  searchForm.plotId = null
  searchForm.status = ''
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
  ElMessageBox.confirm('确定要删除该种植计划吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await plantingPlanApi.delete(row.id)
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
          await plantingPlanApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await plantingPlanApi.add(form)
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
    cropId: null,
    plotId: null,
    plantingDate: '',
    expectedHarvestDate: '',
    plantingArea: null,
    expectedYield: null
  })
}

// 页面加载时获取数据
onMounted(async () => {
  await Promise.all([loadCropOptions(), loadPlotOptions()])
  loadData()
})
</script>

<style scoped>
.plan-list {
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
