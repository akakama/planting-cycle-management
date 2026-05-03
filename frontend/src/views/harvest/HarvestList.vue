<template>
  <div class="harvest-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>采收记录</span>
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
        <el-table-column prop="harvestDate" label="采收日期" width="120" />
        <el-table-column prop="harvestArea" label="采收面积(亩)" width="120" />
        <el-table-column prop="harvestQuantity" label="实际产量(kg)" width="120" />
        <el-table-column prop="qualityGrade" label="品质等级" width="100">
          <template #default="{ row }">
            <el-tag :type="getQualityType(row.qualityGrade)">{{ row.qualityGrade }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="harvestMethod" label="采收方式" width="100" />
        <el-table-column prop="buyer" label="买家" width="100" />
        <el-table-column prop="saleAmount" label="销售金额(元)" width="120" />
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
      :title="isEdit ? '编辑采收记录' : '新增采收记录'"
      width="700px"
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
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="采收日期" prop="harvestDate">
              <el-date-picker
                v-model="form.harvestDate"
                type="date"
                placeholder="请选择采收日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="采收面积(亩)" prop="harvestArea">
              <el-input-number v-model="form.harvestArea" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="实际产量(kg)" prop="actualYield">
              <el-input-number v-model="form.actualYield" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="品质等级" prop="qualityGrade">
              <el-select v-model="form.qualityGrade" placeholder="请选择品质等级" style="width: 100%">
                <el-option label="优" value="优" />
                <el-option label="一级" value="一级" />
                <el-option label="二级" value="二级" />
                <el-option label="良" value="良" />
                <el-option label="中" value="中" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="采收方式" prop="harvestMethod">
              <el-select v-model="form.harvestMethod" placeholder="请选择采收方式" style="width: 100%">
                <el-option label="人工采摘" value="人工采摘" />
                <el-option label="机械收割" value="机械收割" />
                <el-option label="半机械化" value="半机械化" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="买家" prop="buyer">
              <el-input v-model="form.buyer" placeholder="请输入买家" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="销售单价(元/kg)" prop="salePrice">
              <el-input-number v-model="form.salePrice" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="销售金额(元)" prop="saleAmount">
              <el-input-number v-model="form.saleAmount" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
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
import { harvestApi } from '@/api/harvest'
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
  id: null, planId: null, harvestDate: '', harvestArea: null, actualYield: null,
  qualityGrade: '', harvestMethod: '', buyer: '', salePrice: null, saleAmount: null, remarks: ''
})

const formRules = {
  planId: [{ required: true, message: '请选择种植计划', trigger: 'change' }],
  harvestDate: [{ required: true, message: '请选择采收日期', trigger: 'change' }],
  actualYield: [{ required: true, message: '请输入实际产量', trigger: 'blur' }]
}

const getQualityType = (quality) => {
  const typeMap = { '优': 'success', '一级': 'success', '二级': 'primary', '良': 'primary', '中': 'warning' }
  return typeMap[quality] || 'info'
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
    const response = await harvestApi.getList(params)
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
  ElMessageBox.confirm('确定要删除该采收记录吗？', '提示', { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' })
    .then(async () => {
      try { await harvestApi.delete(row.id); ElMessage.success('删除成功'); loadData() }
      catch (error) { console.error('删除失败:', error) }
    }).catch(() => {})
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) { await harvestApi.update(form.id, form); ElMessage.success('更新成功') }
        else { await harvestApi.add(form); ElMessage.success('新增成功') }
        dialogVisible.value = false; loadData()
      } catch (error) { console.error('提交失败:', error) }
    }
  })
}

const handleDialogClose = () => {
  formRef.value?.resetFields()
  Object.assign(form, { id: null, planId: null, harvestDate: '', harvestArea: null, actualYield: null, qualityGrade: '', harvestMethod: '', buyer: '', salePrice: null, saleAmount: null, remarks: '' })
}

onMounted(async () => { await loadCropAndPlotData(); await loadPlanOptions(); loadData() })
</script>

<style scoped>
.harvest-list { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.search-form { margin-bottom: 20px; }
.el-pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
