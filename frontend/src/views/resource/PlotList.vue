<template>
  <div class="plot-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>地块列表</span>
          <el-button type="primary" @click="handleAdd">新增地块</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="地块名称">
          <el-input v-model="searchForm.plotName" placeholder="请输入地块名称" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="code" label="地块编码" width="120" />
        <el-table-column prop="name" label="地块名称" width="150" />
        <el-table-column prop="area" label="面积(㎡)" width="100" />
        <el-table-column prop="soilType" label="土壤类型" width="120" />
        <el-table-column prop="location" label="位置" width="150" />
        <el-table-column label="经纬度" width="180">
          <template #default="{ row }">
            <span v-if="row.longitude && row.latitude">
              {{ row.longitude.toFixed(4) }}, {{ row.latitude.toFixed(4) }}
            </span>
          </template>
        </el-table-column>
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
      :title="isEdit ? '编辑地块' : '新增地块'"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="地块编码" prop="code">
          <el-input v-model="form.code" placeholder="请输入地块编码" />
        </el-form-item>
        <el-form-item label="地块名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入地块名称" />
        </el-form-item>
        <el-form-item label="面积(㎡)" prop="area">
          <el-input-number
            v-model="form.area"
            :min="0"
            :max="10000"
            :precision="2"
            placeholder="请输入面积"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="土壤类型" prop="soilType">
          <el-input v-model="form.soilType" placeholder="请输入土壤类型" />
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="form.location" placeholder="请输入位置" />
        </el-form-item>
        <el-form-item label="经度" prop="longitude">
          <el-input-number
            v-model="form.longitude"
            :min="-180"
            :max="180"
            :precision="6"
            placeholder="请输入经度"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="纬度" prop="latitude">
          <el-input-number
            v-model="form.latitude"
            :min="-90"
            :max="90"
            :precision="6"
            placeholder="请输入纬度"
            style="width: 100%"
          />
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
import { plotApi } from '@/api/plot'

// 响应式数据
const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

// 搜索表单
const searchForm = reactive({
  plotName: ''
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
  code: '',
  name: '',
  area: null,
  soilType: '',
  location: '',
  longitude: null,
  latitude: null,
  remark: ''
})

// 表单验证规则
const formRules = {
  code: [
    { required: true, message: '请输入地块编码', trigger: 'blur' },
    { min: 1, max: 20, message: '长度在1到20个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入地块名称', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在1到50个字符', trigger: 'blur' }
  ]
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      plotName: searchForm.plotName || undefined
    }
    const response = await plotApi.getList(params)
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
  searchForm.plotName = ''
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
  ElMessageBox.confirm('确定要删除该地块吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await plotApi.delete(row.id)
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
          await plotApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await plotApi.add(form)
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
    code: '',
    name: '',
    area: null,
    soilType: '',
    location: '',
    longitude: null,
    latitude: null,
    remark: ''
  })
}

// 页面加载时获取数据
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.plot-list {
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
