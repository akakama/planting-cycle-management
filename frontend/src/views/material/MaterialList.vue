<template>
  <div class="material-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>农资管理</span>
          <el-button type="primary" @click="handleAdd">新增农资</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="农资名称">
          <el-input v-model="searchForm.name" placeholder="请输入农资名称" clearable />
        </el-form-item>
        <el-form-item label="农资类型">
          <el-select v-model="searchForm.type" placeholder="请选择农资类型" clearable>
            <el-option label="化肥" value="FERTILIZER" />
            <el-option label="农药" value="PESTICIDE" />
            <el-option label="种子" value="SEED" />
            <el-option label="其他" value="OTHER" />
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
        <el-table-column prop="name" label="农资名称" width="150" />
        <el-table-column prop="type" label="农资类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getTypeColor(row.type)">{{ getTypeName(row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="specification" label="规格" width="100" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="stockQuantity" label="库存" width="120">
          <template #default="{ row }">
            <el-progress
              :percentage="getStockPercentage(row.stockQuantity)"
              :color="getStockColor(row.stockQuantity)"
              :format="() => `${row.stockQuantity} ${row.unit}`"
            />
          </template>
        </el-table-column>
        <el-table-column prop="supplier" label="供应商" width="150" />
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
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
      :title="isEdit ? '编辑农资' : '新增农资'"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="农资名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入农资名称" />
        </el-form-item>
        <el-form-item label="农资类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择农资类型" style="width: 100%">
            <el-option label="化肥" value="FERTILIZER" />
            <el-option label="农药" value="PESTICIDE" />
            <el-option label="种子" value="SEED" />
            <el-option label="其他" value="OTHER" />
          </el-select>
        </el-form-item>
        <el-form-item label="规格" prop="specification">
          <el-input v-model="form.specification" placeholder="请输入规格" />
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-select v-model="form.unit" placeholder="请选择单位" style="width: 100%">
            <el-option label="吨" value="吨" />
            <el-option label="千克" value="千克" />
            <el-option label="克" value="克" />
            <el-option label="升" value="升" />
            <el-option label="毫升" value="毫升" />
            <el-option label="袋" value="袋" />
            <el-option label="瓶" value="瓶" />
          </el-select>
        </el-form-item>
        <el-form-item label="库存" prop="stock">
          <el-input-number
            v-model="form.stock"
            :min="0"
            :max="10000"
            :precision="2"
            placeholder="请输入库存"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="供应商" prop="supplier">
          <el-input v-model="form.supplier" placeholder="请输入供应商" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="form.remark"
            type="textarea"
            :rows="4"
            placeholder="请输入备注"
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
import { materialApi } from '@/api/material'

// 响应式数据
const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

// 搜索表单
const searchForm = reactive({
  name: '',
  type: ''
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
  type: '',
  specification: '',
  unit: '',
  stock: null,
  supplier: '',
  remark: ''
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入农资名称', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在1到50个字符', trigger: 'blur' }
  ],
  type: [{ required: true, message: '请选择农资类型', trigger: 'change' }],
  unit: [{ required: true, message: '请选择单位', trigger: 'change' }]
}

// 获取农资类型颜色
const getTypeColor = (type) => {
  const colorMap = {
    FERTILIZER: 'success',
    PESTICIDE: 'warning',
    SEED: 'primary',
    OTHER: 'info'
  }
  return colorMap[type] || 'info'
}

// 获取类型中文名称
const getTypeName = (type) => {
  const nameMap = {
    FERTILIZER: '化肥',
    PESTICIDE: '农药',
    SEED: '种子',
    OTHER: '其他'
  }
  return nameMap[type] || type
}

// 获取库存百分比（假设最大库存为100）
const getStockPercentage = (stock) => {
  const maxStock = 100
  const percentage = (stock / maxStock) * 100
  return Math.min(percentage, 100)
}

// 获取库存颜色
const getStockColor = (stock) => {
  if (stock < 10) {
    return '#f56c6c' // 红色警告
  } else if (stock < 30) {
    return '#e6a23c' // 橙色
  } else {
    return '#67c23a' // 绿色
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      name: searchForm.name || undefined,
      type: searchForm.type || undefined
    }
    const response = await materialApi.getList(params)
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
  searchForm.name = ''
  searchForm.type = ''
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
  ElMessageBox.confirm('确定要删除该农资吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await materialApi.delete(row.id)
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
          await materialApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await materialApi.add(form)
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
    type: '',
    specification: '',
    unit: '',
    stock: null,
    supplier: '',
    remark: ''
  })
}

// 页面加载时获取数据
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.material-list {
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
