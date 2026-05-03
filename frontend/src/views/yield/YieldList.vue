<template>
  <div class="yield-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>产量预估</span>
          <el-button type="primary" @click="handleAdd">新增预测</el-button>
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
        <el-table-column prop="predictionDate" label="预测日期" width="120" />
        <el-table-column prop="predictedYield" label="预测产量(kg)" width="120" />
        <el-table-column prop="predictionMethod" label="预测方法" width="120">
          <template #default="{ row }">
            {{ getMethodName(row.predictionMethod) }}
          </template>
        </el-table-column>
        <el-table-column prop="confidenceLevel" label="置信度" width="100">
          <template #default="{ row }">
            <el-tag :type="getConfidenceType(row.confidenceLevel)">{{ row.confidenceLevel }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
        <el-table-column label="操作" width="150" fixed="right">
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
      :title="isEdit ? '编辑产量预测' : '新增产量预测'"
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
        <el-form-item label="预测日期" prop="predictionDate">
          <el-date-picker
            v-model="form.predictionDate"
            type="date"
            placeholder="请选择预测日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="预测产量(kg)" prop="predictedYield">
          <el-input-number v-model="form.predictedYield" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="预测方法" prop="predictionMethod">
          <el-select v-model="form.predictionMethod" placeholder="请选择预测方法" style="width: 100%">
            <el-option label="历史数据预测" value="历史数据预测" />
            <el-option label="生长模型预测" value="生长模型预测" />
            <el-option label="机器学习预测" value="机器学习预测" />
            <el-option label="专家经验预测" value="专家经验预测" />
          </el-select>
        </el-form-item>
        <el-form-item label="置信度" prop="confidenceLevel">
          <el-select v-model="form.confidenceLevel" placeholder="请选择置信度" style="width: 100%">
            <el-option label="高" value="高" />
            <el-option label="中" value="中" />
            <el-option label="低" value="低" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input v-model="form.remarks" type="textarea" :rows="3" placeholder="请输入备注" />
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
import { yieldPredictionApi } from '@/api/yieldPrediction'
import { plantingPlanApi } from '@/api/plantingPlan'
import { cropApi } from '@/api/crop'
import { plotApi } from '@/api/plot'

const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const planOptions = ref([])
const cropMap = ref({})
const plotMap = ref({})

const searchForm = reactive({ planId: null })
const pagination = reactive({ page: 1, size: 10, total: 0 })
const form = reactive({
  id: null, planId: null, predictionDate: '', predictedYield: null, predictionMethod: '', confidenceLevel: '', remarks: ''
})

const formRules = {
  planId: [{ required: true, message: '请选择种植计划', trigger: 'change' }],
  predictionDate: [{ required: true, message: '请选择预测日期', trigger: 'change' }],
  predictedYield: [{ required: true, message: '请输入预测产量', trigger: 'blur' }]
}

const getConfidenceType = (level) => {
  if (level === '高') return 'success'
  if (level === '中') return 'warning'
  return 'danger'
}

const getMethodName = (method) => {
  const nameMap = {
    'MACHINE_LEARNING': '机器学习',
    'HISTORICAL_AVERAGE': '历史平均',
    'EXPERT_ESTIMATE': '专家估算',
    'MODEL_PREDICTION': '模型预测'
  }
  return nameMap[method] || method || '未知方法'
}

const getPlanLabel = (plan) => {
  const cropName = cropMap.value[plan.cropId] || '未知作物'
  const plotName = plotMap.value[plan.plotId] || '未知地块'
  return `${cropName} - ${plotName}`
}

const getPlanDisplay = (planId) => {
  const plan = planOptions.value.find(p => p.id === planId)
  return plan ? getPlanLabel(plan) : '未知计划'
}

const loadCropAndPlotData = async () => {
  try {
    const [cropRes, plotRes] = await Promise.all([
      cropApi.getList({ page: 1, size: 1000 }),
      plotApi.getList({ page: 1, size: 1000 })
    ])
    ;(cropRes.data.records || []).forEach(c => { cropMap.value[c.id] = c.name })
    ;(plotRes.data.records || []).forEach(p => { plotMap.value[p.id] = p.name || p.plotName })
  } catch (error) { console.error('加载作物和地块数据失败:', error) }
}

const loadPlanOptions = async () => {
  try {
    const response = await plantingPlanApi.getList({ page: 1, size: 1000 })
    planOptions.value = response.data.records
  } catch (error) { console.error('加载种植计划选项失败:', error) }
}

const loadData = async () => {
  loading.value = true
  try {
    const params = { page: pagination.page, size: pagination.size, planId: searchForm.planId || undefined }
    const response = await yieldPredictionApi.getList(params)
    tableData.value = response.data.records
    pagination.total = response.data.total
  } catch (error) { console.error('加载数据失败:', error) }
  finally { loading.value = false }
}

const handleSearch = () => { pagination.page = 1; loadData() }
const handleReset = () => { searchForm.planId = null; pagination.page = 1; loadData() }
const handleAdd = () => { isEdit.value = false; dialogVisible.value = true }
const handleEdit = (row) => { isEdit.value = true; Object.assign(form, row); dialogVisible.value = true }

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该产量预测吗？', '提示', { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' })
    .then(async () => {
      try { await yieldPredictionApi.delete(row.id); ElMessage.success('删除成功'); loadData() }
      catch (error) { console.error('删除失败:', error) }
    }).catch(() => {})
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) { await yieldPredictionApi.update(form.id, form); ElMessage.success('更新成功') }
        else { await yieldPredictionApi.add(form); ElMessage.success('新增成功') }
        dialogVisible.value = false; loadData()
      } catch (error) { console.error('提交失败:', error) }
    }
  })
}

const handleDialogClose = () => {
  formRef.value?.resetFields()
  Object.assign(form, { id: null, planId: null, predictionDate: '', predictedYield: null, predictionMethod: '', confidenceLevel: '', remarks: '' })
}

onMounted(async () => { await loadCropAndPlotData(); await loadPlanOptions(); loadData() })
</script>

<style scoped>
.yield-list { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.search-form { margin-bottom: 20px; }
.el-pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
