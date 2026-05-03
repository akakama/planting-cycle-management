<template>
  <div class="calendar-page">
    <!-- 统计概览 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" style="color: #409eff"><Calendar /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ totalEvents }}</div>
              <div class="stat-label">本月事件</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" style="color: #67c23a"><Crop /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ plantingCount }}</div>
              <div class="stat-label">种植事件</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" style="color: #e6a23c"><Orange /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ harvestCount }}</div>
              <div class="stat-label">采收事件</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" style="color: #f56c6c"><Warning /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ upcomingCount }}</div>
              <div class="stat-label">即将到来</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <!-- 日历主体 -->
      <el-col :span="18">
        <el-card>
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <span class="title">{{ currentYear }}年{{ currentMonth }}月 种植日历</span>
                <el-tag type="info" size="small">共 {{ plantingPlans.length }} 个计划</el-tag>
              </div>
              <div class="header-right">
                <!-- 事件类型筛选 -->
                <el-select v-model="filterType" placeholder="事件类型" clearable size="small" style="width: 120px; margin-right: 10px;">
                  <el-option label="全部" value="" />
                  <el-option label="种植" value="planting" />
                  <el-option label="采收" value="harvest" />
                </el-select>
                <el-button-group>
                  <el-button size="small" @click="prevMonth"><el-icon><ArrowLeft /></el-icon></el-button>
                  <el-button size="small" @click="goToday">今天</el-button>
                  <el-button size="small" @click="nextMonth"><el-icon><ArrowRight /></el-icon></el-button>
                </el-button-group>
                <el-button type="primary" size="small" @click="showAddPlanDialog">
                  <el-icon><Plus /></el-icon> 添加计划
                </el-button>
              </div>
            </div>
          </template>

          <el-calendar v-model="currentDate">
            <template #date-cell="{ data }">
              <div class="calendar-cell" @click="handleCellClick(data.day)">
                <div class="date-number" :class="{ 'is-today': data.day === todayStr }">
                  {{ data.day.split('-').slice(2).join('-') }}
                </div>
                <div v-if="getFilteredEventsForDate(data.day).length > 0" class="event-list">
                  <div
                    v-for="(event, index) in getFilteredEventsForDate(data.day).slice(0, 3)"
                    :key="event.planId + '-' + index"
                    class="event-item"
                    :class="`event-${event.type}`"
                    @click.stop="showEventDetail(event, data.day)"
                  >
                    <el-icon v-if="event.type === 'planting'"><Crop /></el-icon>
                    <el-icon v-else><Orange /></el-icon>
                    <span>{{ event.title }}</span>
                  </div>
                  <div v-if="getFilteredEventsForDate(data.day).length > 3" class="more-events">
                    +{{ getFilteredEventsForDate(data.day).length - 3 }} 更多
                  </div>
                </div>
              </div>
            </template>
          </el-calendar>
        </el-card>
      </el-col>

      <!-- 事件列表侧边栏 -->
      <el-col :span="6">
        <el-card class="event-sidebar">
          <template #header>
            <div class="sidebar-header">
              <span>本月事件列表</span>
              <el-tag size="small">{{ monthEvents.length }}</el-tag>
            </div>
          </template>
          <el-scrollbar height="500px">
            <div v-if="monthEvents.length === 0" class="empty-events">
              <el-empty description="暂无事件" :image-size="80" />
            </div>
            <div v-else class="event-timeline">
              <div v-for="event in monthEvents" :key="event.date + '-' + event.event.planId" class="timeline-item">
                <div class="timeline-date">{{ formatDisplayDate(event.date) }}</div>
                <div class="timeline-content" :class="`event-${event.event.type}`" @click="showEventDetail(event.event, event.date)">
                  <el-icon v-if="event.event.type === 'planting'"><Crop /></el-icon>
                  <el-icon v-else><Orange /></el-icon>
                  <span>{{ event.event.title }}</span>
                </div>
              </div>
            </div>
          </el-scrollbar>
        </el-card>
      </el-col>
    </el-row>

    <!-- 事件详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="事件详情" width="500px">
      <el-descriptions v-if="currentEvent" :column="1" border>
        <el-descriptions-item label="事件类型">
          <el-tag :type="currentEvent.type === 'planting' ? 'success' : 'warning'">
            {{ currentEvent.type === 'planting' ? '种植' : '采收' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="标题">{{ currentEvent.title }}</el-descriptions-item>
        <el-descriptions-item label="作物名称">{{ currentEvent.cropName }}</el-descriptions-item>
        <el-descriptions-item label="地块名称">{{ currentEvent.plotName }}</el-descriptions-item>
        <el-descriptions-item label="日期">{{ currentEventDate }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentEvent.status)">{{ currentEvent.status || '未开始' }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="goToPlanDetail">查看计划详情</el-button>
      </template>
    </el-dialog>

    <!-- 快速添加种植计划对话框 -->
    <el-dialog v-model="addPlanDialogVisible" title="快速添加种植计划" width="600px">
      <el-form ref="planFormRef" :model="newPlan" :rules="planRules" label-width="100px">
        <el-form-item label="作物" prop="cropId">
          <el-select v-model="newPlan.cropId" placeholder="请选择作物" style="width: 100%" filterable>
            <el-option v-for="crop in cropOptions" :key="crop.id" :label="crop.name" :value="crop.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="地块" prop="plotId">
          <el-select v-model="newPlan.plotId" placeholder="请选择地块" style="width: 100%" filterable>
            <el-option v-for="plot in plotOptions" :key="plot.id" :label="plot.name" :value="plot.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="种植日期" prop="plantingDate">
          <el-date-picker v-model="newPlan.plantingDate" type="date" placeholder="选择种植日期" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="预计采收" prop="expectedHarvestDate">
          <el-date-picker v-model="newPlan.expectedHarvestDate" type="date" placeholder="选择预计采收日期" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="种植面积">
          <el-input-number v-model="newPlan.plantingArea" :min="0" :precision="2" placeholder="种植面积(亩)" style="width: 100%" />
        </el-form-item>
        <el-form-item label="预计产量">
          <el-input-number v-model="newPlan.expectedYield" :min="0" :precision="2" placeholder="预计产量(kg)" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addPlanDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitNewPlan" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>

    <!-- 日期事件列表对话框 -->
    <el-dialog v-model="dateEventsDialogVisible" :title="`${selectedDate} 的事件`" width="500px">
      <div v-if="selectedDateEvents.length === 0" class="empty-events">
        <el-empty description="该日期暂无事件" :image-size="80" />
      </div>
      <div v-else class="date-events-list">
        <div v-for="(event, index) in selectedDateEvents" :key="index" class="date-event-item" :class="`event-${event.type}`" @click="showEventDetail(event, selectedDate)">
          <el-icon v-if="event.type === 'planting'"><Crop /></el-icon>
          <el-icon v-else><Orange /></el-icon>
          <span>{{ event.title }}</span>
          <el-tag size="small" :type="event.type === 'planting' ? 'success' : 'warning'">
            {{ event.type === 'planting' ? '种植' : '采收' }}
          </el-tag>
        </div>
      </div>
      <template #footer>
        <el-button @click="dateEventsDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="quickAddForDate">添加计划</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { Crop, Orange, Calendar, Warning, Plus, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { plantingPlanApi } from '@/api/plantingPlan'
import { cropApi } from '@/api/crop'
import { plotApi } from '@/api/plot'

const router = useRouter()

// 响应式数据
const currentDate = ref(new Date())
const plantingPlans = ref([])
const calendarEvents = ref([])
const detailDialogVisible = ref(false)
const currentEvent = ref(null)
const currentEventDate = ref('')
const filterType = ref('')

// 作物和地块选项
const cropOptions = ref([])
const plotOptions = ref([])

// 添加计划相关
const addPlanDialogVisible = ref(false)
const planFormRef = ref(null)
const newPlan = ref({
  cropId: null,
  plotId: null,
  plantingDate: null,
  expectedHarvestDate: null,
  plantingArea: null,
  expectedYield: null
})
const submitting = ref(false)

// 表单验证规则
const planRules = {
  cropId: [{ required: true, message: '请选择作物', trigger: 'change' }],
  plotId: [{ required: true, message: '请选择地块', trigger: 'change' }],
  plantingDate: [{ required: true, message: '请选择种植日期', trigger: 'change' }],
  expectedHarvestDate: [{ required: true, message: '请选择预计采收日期', trigger: 'change' }]
}

// 日期事件列表
const dateEventsDialogVisible = ref(false)
const selectedDate = ref('')
const selectedDateEvents = ref([])

// 今日日期字符串
const todayStr = computed(() => {
  const today = new Date()
  return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
})

// 格式化显示日期
const formatDisplayDate = (dateStr) => {
  const parts = dateStr.split('-')
  return `${parseInt(parts[1])}月${parseInt(parts[2])}日`
}

// 获取当前月份和年份
const currentYear = computed(() => currentDate.value.getFullYear())
const currentMonth = computed(() => currentDate.value.getMonth() + 1)

// 统计数据
const totalEvents = computed(() => monthEvents.value.length)
const plantingCount = computed(() => monthEvents.value.filter(e => e.event.type === 'planting').length)
const harvestCount = computed(() => monthEvents.value.filter(e => e.event.type === 'harvest').length)
const upcomingCount = computed(() => {
  const today = new Date()
  const todayStr2 = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
  return monthEvents.value.filter(e => e.date >= todayStr2).length
})

// 本月事件列表
const monthEvents = computed(() => {
  const year = currentYear.value
  const month = String(currentMonth.value).padStart(2, '0')
  const monthPrefix = `${year}-${month}`
  
  const events = []
  calendarEvents.value.forEach(eventGroup => {
    if (eventGroup.date.startsWith(monthPrefix)) {
      eventGroup.events.forEach(event => {
        if (!filterType.value || event.type === filterType.value) {
          events.push({ date: eventGroup.date, event })
        }
      })
    }
  })
  
  return events.sort((a, b) => a.date.localeCompare(b.date))
})

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
    cropOptions.value = response.data.records || []
  } catch (error) {
    console.error('加载作物选项失败:', error)
  }
}

// 加载地块选项
const loadPlotOptions = async () => {
  try {
    const response = await plotApi.getList({ page: 1, size: 1000 })
    plotOptions.value = response.data.records || []
  } catch (error) {
    console.error('加载地块选项失败:', error)
  }
}

// 加载种植计划数据（与PlanList共用同一API）
const loadPlantingPlans = async () => {
  try {
    const response = await plantingPlanApi.getList({ page: 1, size: 1000 })
    const records = response.data.records || []
    
    // 填充作物名称和地块名称
    for (const record of records) {
      const crop = cropOptions.value.find(c => c.id === record.cropId)
      record.cropName = crop ? crop.name : '未知作物'

      const plot = plotOptions.value.find(p => p.id === record.plotId)
      record.plotName = plot ? plot.name : '未知地块'
    }
    
    plantingPlans.value = records
    
    // 将种植计划转换为日历事件
    const events = []
    records.forEach(plan => {
      // 添加种植事件
      if (plan.plantingDate) {
        events.push({
          date: plan.plantingDate,
          events: [{
            type: 'planting',
            title: `${plan.cropName} - 播种`,
            planId: plan.id,
            cropName: plan.cropName,
            plotName: plan.plotName,
            status: plan.status
          }]
        })
      }
      
      // 添加预计采收事件
      if (plan.expectedHarvestDate) {
        events.push({
          date: plan.expectedHarvestDate,
          events: [{
            type: 'harvest',
            title: `${plan.cropName} - 采收`,
            planId: plan.id,
            cropName: plan.cropName,
            plotName: plan.plotName,
            status: plan.status
          }]
        })
      }
    })
    
    calendarEvents.value = events
  } catch (error) {
    console.error('加载种植计划失败:', error)
    ElMessage.error('加载种植计划失败: ' + (error.message || '未知错误'))
  }
}

// 获取指定日期的事件（带筛选）
const getFilteredEventsForDate = (dateStr) => {
  const eventGroup = calendarEvents.value.find(item => item.date === dateStr)
  if (!eventGroup) return []
  
  if (!filterType.value) return eventGroup.events
  return eventGroup.events.filter(e => e.type === filterType.value)
}

// 处理单元格点击
const handleCellClick = (dateStr) => {
  const events = getFilteredEventsForDate(dateStr)
  if (events.length > 0) {
    selectedDate.value = dateStr
    selectedDateEvents.value = events
    dateEventsDialogVisible.value = true
  }
}

// 上个月
const prevMonth = () => {
  const newDate = new Date(currentDate.value)
  newDate.setMonth(newDate.getMonth() - 1)
  currentDate.value = newDate
}

// 下个月
const nextMonth = () => {
  const newDate = new Date(currentDate.value)
  newDate.setMonth(newDate.getMonth() + 1)
  currentDate.value = newDate
}

// 今天
const goToday = () => {
  currentDate.value = new Date()
}

// 显示事件详情
const showEventDetail = (event, date) => {
  currentEvent.value = event
  currentEventDate.value = date
  detailDialogVisible.value = true
  dateEventsDialogVisible.value = false
}

// 跳转到计划详情
const goToPlanDetail = () => {
  if (currentEvent.value?.planId) {
    router.push('/planning/plans')
  }
  detailDialogVisible.value = false
}

// 显示添加计划对话框
const showAddPlanDialog = () => {
  newPlan.value = {
    cropId: null,
    plotId: null,
    plantingDate: null,
    expectedHarvestDate: null,
    plantingArea: null,
    expectedYield: null
  }
  addPlanDialogVisible.value = true
}

// 快速添加（从日期对话框）
const quickAddForDate = () => {
  newPlan.value.plantingDate = selectedDate.value
  dateEventsDialogVisible.value = false
  addPlanDialogVisible.value = true
}

// 提交新计划（与PlanList共用同一API）
const submitNewPlan = async () => {
  if (!planFormRef.value) return
  
  await planFormRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await plantingPlanApi.add(newPlan.value)
        ElMessage.success('添加成功')
        addPlanDialogVisible.value = false
        loadPlantingPlans()
      } catch (error) {
        console.error('添加失败:', error)
        ElMessage.error('添加失败: ' + (error.message || '未知错误'))
      } finally {
        submitting.value = false
      }
    }
  })
}

// 页面加载时获取数据
onMounted(async () => {
  await Promise.all([loadCropOptions(), loadPlotOptions()])
  loadPlantingPlans()
})
</script>

<style scoped>
.calendar-page {
  padding: 20px;
}

/* 统计卡片样式 */
.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  font-size: 40px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

/* 日历头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-left .title {
  font-size: 18px;
  font-weight: bold;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 日历单元格 */
.calendar-cell {
  height: 100%;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.date-number {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 4px;
}

.date-number.is-today {
  color: #409eff;
}

.event-list {
  flex: 1;
  overflow-y: auto;
}

.event-item {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 4px;
  margin: 2px 0;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.event-item:hover {
  transform: scale(1.02);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.event-planting {
  background-color: #f0f9ff;
  color: #10b981;
  border-left: 3px solid #10b981;
}

.event-harvest {
  background-color: #fff7ed;
  color: #f59e0b;
  border-left: 3px solid #f59e0b;
}

.event-item span {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.more-events {
  font-size: 11px;
  color: #909399;
  text-align: center;
  padding: 2px;
}

/* 侧边栏 */
.event-sidebar {
  height: 100%;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-events {
  padding: 20px;
  text-align: center;
}

.event-timeline {
  padding: 10px 0;
}

.timeline-item {
  margin-bottom: 15px;
}

.timeline-date {
  font-size: 12px;
  color: #909399;
  margin-bottom: 5px;
}

.timeline-content {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.timeline-content:hover {
  transform: translateX(5px);
}

/* 日期事件列表 */
.date-events-list {
  max-height: 400px;
  overflow-y: auto;
}

.date-event-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.date-event-item:hover {
  transform: translateX(5px);
}

/* 日历样式调整 */
:deep(.el-calendar-table .el-calendar-day) {
  height: 100px;
  padding: 4px;
}

:deep(.el-calendar-table td.is-selected .el-calendar-day) {
  background-color: #ecf5ff;
}

:deep(.el-calendar-table td.is-today .el-calendar-day) {
  background-color: #f0f9ff;
}
</style>
