# 统一数据模型与API接口规范

## 📋 目录

1. [数据模型统一](#数据模型统一)
2. [API接口规范](#api接口规范)
3. [数据关联逻辑](#数据关联逻辑)
4. [实现方案](#实现方案)

---

## 数据模型统一

### 当前问题分析

**现有数据结构问题**：
1. 各模块数据字段不一致
2. 缺少统一的关联字段
3. 命名规范不统一
4. 缺少数据版本控制
5. 缺少数据状态管理

### 统一数据模型设计

#### 1. 基础实体类（BaseEntity）

所有实体类都继承的基础类，包含通用字段：

```java
package com.planting.entity;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableLogic;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

@Data
public abstract class BaseEntity implements Serializable {
    
    /**
     * 创建人ID
     */
    @TableField(fill = FieldFill.INSERT)
    private Long createdBy;
    
    /**
     * 创建时间
     */
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdTime;
    
    /**
     * 更新人ID
     */
    @TableField(fill = FieldFill.UPDATE)
    private Long updatedBy;
    
    /**
     * 更新时间
     */
    @TableField(fill = FieldFill.UPDATE)
    private LocalDateTime updatedTime;
    
    /**
     * 删除标记（0-未删除，1-已删除）
     */
    @TableLogic
    private Integer deleted;
    
    /**
     * 版本号（乐观锁）
     */
    @TableField(fill = FieldFill.INSERT)
    private Integer version;
    
    /**
     * 租户ID（多租户支持）
     */
    @TableField(fill = FieldFill.INSERT)
    private Long tenantId;
    
    /**
     * 数据状态（0-草稿，1-已提交，2-已审核，3-已作废）
     */
    private Integer status;
    
    /**
     * 备注
     */
    private String remarks;
}
```

#### 2. 实体关联关系

**核心关联关系**：

```
种植计划（PlantingPlan）
    ├─ 作物（Crop）- 多对一
    ├─ 地块（Plot）- 多对一
    ├─ 物候期记录（PhenologyRecord）- 一对多
    ├─ 病虫害记录（PestRecord）- 一对多
    ├─ 农资使用记录（MaterialUsage）- 一对多
    ├─ 采收记录（HarvestRecord）- 一对多
    ├─ 产量预测（YieldPrediction）- 一对多
    └─ AI问答记录（AiChatRecord）- 一对多

作物（Crop）
    ├─ 作物品种（CropVariety）- 一对多
    └─ 种植计划（PlantingPlan）- 一对多

地块（Plot）
    ├─ 种植计划（PlantingPlan）- 一对多
    └─ 土壤信息（SoilInfo）- 一对一

农资（AgriculturalMaterial）
    └─ 农资使用记录（MaterialUsage）- 一对多

用户（User）
    ├─ 种植计划（PlantingPlan）- 一对多
    ├─ 物候期记录（PhenologyRecord）- 一对多
    ├─ 病虫害记录（PestRecord）- 一对多
    └─ 采收记录（HarvestRecord）- 一对多
```

#### 3. 统一实体类规范

**命名规范**：
- 实体类：使用驼峰命名，如 `PlantingPlan`
- 数据库表：使用下划线命名，如 `planting_plan`
- 字段命名：使用驼峰命名，数据库使用下划线

**字段规范**：

| 字段类型 | Java类型 | 数据库类型 | 说明 |
|---------|---------|-----------|------|
| 主键 | Long | BIGINT AUTO_INCREMENT | 使用 @TableId(type = IdType.AUTO) |
| 外键 | Long | BIGINT | 关联其他表的ID |
| 字符串 | String | VARCHAR | 根据实际长度定义 |
| 日期 | LocalDate | DATE | 日期类型 |
| 时间 | LocalDateTime | DATETIME | 日期时间类型 |
| 数量 | BigDecimal | DECIMAL | 金额、数量等 |
| 布尔 | Boolean | TINYINT | 0-否，1-是 |
| 状态 | Integer | TINYINT | 使用枚举或常量 |
| 备注 | String | TEXT | 长文本 |

#### 4. 统一状态枚举

```java
package com.planting.enums;

/**
 * 种植计划状态
 */
public enum PlanStatus {
    DRAFT(0, "草稿"),
    SUBMITTED(1, "已提交"),
    APPROVED(2, "已审核"),
    IN_PROGRESS(3, "进行中"),
    COMPLETED(4, "已完成"),
    CANCELLED(5, "已取消");
    
    private final Integer code;
    private final String desc;
    
    PlanStatus(Integer code, String desc) {
        this.code = code;
        this.desc = desc;
    }
    
    public Integer getCode() {
        return code;
    }
    
    public String getDesc() {
        return desc;
    }
}

/**
 * 病虫害严重程度
 */
public enum PestSeverity {
    LOW(1, "低"),
    MEDIUM(2, "中"),
    HIGH(3, "高"),
    SEVERE(4, "严重");
    
    private final Integer code;
    private final String desc;
    
    PestSeverity(Integer code, String desc) {
        this.code = code;
        this.desc = desc;
    }
    
    public Integer getCode() {
        return code;
    }
    
    public String getDesc() {
        return desc;
    }
}

/**
 * 采收质量等级
 */
public enum QualityGrade {
    EXCELLENT(1, "优"),
    GOOD(2, "良"),
    AVERAGE(3, "中"),
    POOR(4, "差");
    
    private final Integer code;
    private final String desc;
    
    QualityGrade(Integer code, String desc) {
        this.code = code;
        this.desc = desc;
    }
    
    public Integer getCode() {
        return code;
    }
    
    public String getDesc() {
        return desc;
    }
}
```

---

## API接口规范

### 统一响应格式

**成功响应**：
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    // 具体数据
  },
  "timestamp": 1719792000000
}
```

**失败响应**：
```json
{
  "code": 400,
  "message": "操作失败",
  "error": "详细错误信息",
  "timestamp": 1719792000000
}
```

**分页响应**：
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "records": [],
    "total": 100,
    "size": 10,
    "current": 1,
    "pages": 10
  },
  "timestamp": 1719792000000
}
```

### 统一接口规范

#### 1. RESTful API规范

**URL规范**：
- 使用小写字母和连字符
- 使用复数名词
- 版本号：`/api/v1/`

**HTTP方法规范**：
- GET：查询
- POST：创建
- PUT：更新（全量）
- PATCH：更新（部分）
- DELETE：删除

#### 2. 接口命名规范

**资源接口**：
```
GET    /api/v1/plans              # 获取种植计划列表
GET    /api/v1/plans/{id}         # 获取种植计划详情
POST   /api/v1/plans              # 创建种植计划
PUT    /api/v1/plans/{id}         # 更新种植计划
DELETE /api/v1/plans/{id}         # 删除种植计划
```

**关联接口**：
```
GET    /api/v1/plans/{id}/phenology       # 获取物候期记录
GET    /api/v1/plans/{id}/pests            # 获取病虫害记录
GET    /api/v1/plans/{id}/harvests         # 获取采收记录
GET    /api/v1/plans/{id}/materials        # 获取农资使用记录
```

**操作接口**：
```
POST   /api/v1/plans/{id}/submit          # 提交种植计划
POST   /api/v1/plans/{id}/approve         # 审核种植计划
POST   /api/v1/plans/{id}/cancel          # 取消种植计划
```

#### 3. 统一接口参数

**查询参数**：
```
GET /api/v1/plans?page=1&size=10&sort=createdTime,desc
```

**分页参数**：
- page：页码（从1开始）
- size：每页大小（默认10）
- sort：排序字段（格式：字段名,方向）

**筛选参数**：
- 状态筛选：`?status=1,2,3`
- 日期范围：`?startDate=2025-01-01&endDate=2025-12-31`
- 关键字搜索：`?keyword=水稻`

---

## 数据关联逻辑

### 1. 种植计划关联逻辑

**核心关联**：
```java
// 种植计划关联作物
PlantingPlan plan = new PlantingPlan();
plan.setCropId(cropId);  // 作物ID
plan.setPlotId(plotId);  // 地块ID
plan.setPlanCode(generatePlanCode());  // 计划编号
plan.setStatus(PlanStatus.DRAFT.getCode());  // 初始状态
```

**数据流转**：
```
创建种植计划
    ↓
关联作物和地块
    ↓
生成计划编号
    ↓
初始化物候期记录
    ↓
初始化农资使用计划
    ↓
初始化产量预测
```

### 2. 物候期关联逻辑

**关联种植计划**：
```java
PhenologyRecord record = new PhenologyRecord();
record.setPlanId(planId);  // 种植计划ID
record.setPhenologyName(phenologyName);
record.setPhenologyDate(phenologyDate);
record.setStatus(1);  // 1-正常，2-异常
```

**自动生成物候期**：
```java
// 根据作物类型自动生成物候期模板
List<PhenologyTemplate> templates = getPhenologyTemplates(cropId);
for (PhenologyTemplate template : templates) {
    PhenologyRecord record = new PhenologyRecord();
    record.setPlanId(planId);
    record.setPhenologyName(template.getName());
    record.setExpectedDate(calculateExpectedDate(plan, template));
    phenologyRecordService.save(record);
}
```

### 3. 病虫害关联逻辑

**关联种植计划**：
```java
PestRecord record = new PestRecord();
record.setPlanId(planId);  // 种植计划ID
record.setPestName(pestName);
record.setPestType(pestType);  // disease-病害，pest-虫害
record.setSeverity(PestSeverity.HIGH.getCode());
record.setOccurrenceDate(occurrenceDate);
```

**AI识别集成**：
```java
// AI识别结果自动关联到种植计划
PestRecord record = new PestRecord();
record.setPlanId(planId);
record.setPestName(diagnosisResult.getDiseaseName());
record.setConfidence(diagnosisResult.getConfidence());
record.setPreventionAdvice(diagnosisResult.getAdvice());
record.setIsAiIdentified(true);
record.setIdentifyTime(LocalDateTime.now());
```

### 4. 农资使用关联逻辑

**关联种植计划和农资**：
```java
MaterialUsage usage = new MaterialUsage();
usage.setPlanId(planId);  // 种植计划ID
usage.setMaterialId(materialId);  // 农资ID
usage.setUsageQuantity(quantity);
usage.setUsageDate(usageDate);
usage.setApplicationMethod(method);
```

**自动推荐农资**：
```java
// 根据病虫害自动推荐农资
List<Material> recommendedMaterials = recommendMaterials(pestName);
for (Material material : recommendedMaterials) {
    MaterialUsage usage = new MaterialUsage();
    usage.setPlanId(planId);
    usage.setMaterialId(material.getId());
    usage.setUsageQuantity(calculateQuantity(plan, material));
    usage.setRecommendType("auto");  // auto-自动，manual-手动
    materialUsageService.save(usage);
}
```

### 5. 采收记录关联逻辑

**关联种植计划**：
```java
HarvestRecord record = new HarvestRecord();
record.setPlanId(planId);  // 种植计划ID
record.setHarvestDate(harvestDate);
record.setHarvestArea(area);
record.setActualYield(yield);
record.setQualityGrade(QualityGrade.GOOD.getCode());
```

**自动更新种植计划**：
```java
// 采收后自动更新种植计划状态
PlanPlan plan = planService.getById(planId);
plan.setActualEndDate(harvestDate);
plan.setActualYield(totalYield);
plan.setStatus(PlanStatus.COMPLETED.getCode());
planService.updateById(plan);
```

---

## 实现方案

### 1. 实体类改造

**步骤1**：创建BaseEntity
```java
// 创建 com.planting.entity.BaseEntity
// 所有实体类继承BaseEntity
```

**步骤2**：改造现有实体类
```java
@Data
@TableName("planting_plan")
public class PlantingPlan extends BaseEntity {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    // 移除重复字段（createdBy, createdTime等）
    // 统一使用BaseEntity中的字段
}
```

**步骤3**：添加关联字段
```java
// 在需要关联的实体类中添加关联字段
@Data
@TableName("phenology_record")
public class PhenologyRecord extends BaseEntity {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private Long planId;  // 关联种植计划
    
    // 添加关联查询字段（不存储）
    @TableField(exist = false)
    private String planName;
    
    @TableField(exist = false)
    private String planCode;
}
```

### 2. Service层改造

**统一Service接口**：
```java
public interface BaseService<T> {
    /**
     * 根据ID查询
     */
    T getById(Long id);
    
    /**
     * 查询列表
     */
    List<T> list();
    
    /**
     * 分页查询
     */
    PageResult<T> page(PageParam param);
    
    /**
     * 保存
     */
    boolean save(T entity);
    
    /**
     * 更新
     */
    boolean updateById(T entity);
    
    /**
     * 删除
     */
    boolean removeById(Long id);
    
    /**
     * 批量删除
     */
    boolean removeByIds(List<Long> ids);
}
```

**实现关联查询**：
```java
@Service
public class PhenologyRecordServiceImpl extends ServiceImpl<PhenologyRecordMapper, PhenologyRecord> 
    implements PhenologyRecordService {
    
    @Autowired
    private PlantingPlanService planService;
    
    @Override
    public PageResult<PhenologyRecord> page(PageParam param) {
        // 查询数据
        Page<PhenologyRecord> page = this.page(new Page<>(param.getPage(), param.getSize()));
        
        // 填充关联数据
        List<PhenologyRecord> records = page.getRecords();
        fillPlanInfo(records);
        
        return PageResult.of(page);
    }
    
    private void fillPlanInfo(List<PhenologyRecord> records) {
        Set<Long> planIds = records.stream()
            .map(PhenologyRecord::getPlanId)
            .collect(Collectors.toSet());
        
        if (planIds.isEmpty()) return;
        
        List<PlantingPlan> plans = planService.listByIds(planIds);
        Map<Long, PlantingPlan> planMap = plans.stream()
            .collect(Collectors.toMap(PlantingPlan::getId, p -> p));
        
        for (PhenologyRecord record : records) {
            PlantingPlan plan = planMap.get(record.getPlanId());
            if (plan != null) {
                record.setPlanName(plan.getPlanName());
                record.setPlanCode(plan.getPlanCode());
            }
        }
    }
}
```

### 3. Controller层改造

**统一Controller规范**：
```java
@RestController
@RequestMapping("/api/v1/phenology-records")
public class PhenologyRecordController {
    
    @Autowired
    private PhenologyRecordService service;
    
    /**
     * 分页查询
     */
    @GetMapping
    public Result<PageResult<PhenologyRecord>> page(
        @RequestParam(defaultValue = "1") Integer page,
        @RequestParam(defaultValue = "10") Integer size,
        @RequestParam(required = false) Long planId
    ) {
        PageParam param = new PageParam(page, size);
        param.put("planId", planId);
        return Result.success(service.page(param));
    }
    
    /**
     * 根据ID查询
     */
    @GetMapping("/{id}")
    public Result<PhenologyRecord> getById(@PathVariable Long id) {
        return Result.success(service.getById(id));
    }
    
    /**
     * 保存
     */
    @PostMapping
    public Result<Void> save(@RequestBody PhenologyRecord entity) {
        service.save(entity);
        return Result.success();
    }
    
    /**
     * 更新
     */
    @PutMapping("/{id}")
    public Result<Void> update(@PathVariable Long id, @RequestBody PhenologyRecord entity) {
        entity.setId(id);
        service.updateById(entity);
        return Result.success();
    }
    
    /**
     * 删除
     */
    @DeleteMapping("/{id}")
    public Result<Void> delete(@PathVariable Long id) {
        service.removeById(id);
        return Result.success();
    }
}
```

**统一关联查询接口**：
```java
@RestController
@RequestMapping("/api/v1/plans")
public class PlantingPlanController {
    
    /**
     * 获取种植计划详情（包含所有关联数据）
     */
    @GetMapping("/{id}")
    public Result<PlanDetailVO> getDetail(@PathVariable Long id) {
        PlanDetailVO detail = planService.getDetail(id);
        return Result.success(detail);
    }
    
    /**
     * 获取种植计划的物候期记录
     */
    @GetMapping("/{id}/phenology")
    public Result<List<PhenologyRecord>> getPhenology(@PathVariable Long id) {
        List<PhenologyRecord> records = phenologyService.getByPlanId(id);
        return Result.success(records);
    }
    
    /**
     * 获取种植计划的病虫害记录
     */
    @GetMapping("/{id}/pests")
    public Result<List<PestRecord>> getPests(@PathVariable Long id) {
        List<PestRecord> records = pestService.getByPlanId(id);
        return Result.success(records);
    }
    
    /**
     * 获取种植计划的采收记录
     */
    @GetMapping("/{id}/harvests")
    public Result<List<HarvestRecord>> getHarvests(@PathVariable Long id) {
        List<HarvestRecord> records = harvestService.getByPlanId(id);
        return Result.success(records);
    }
    
    /**
     * 获取种植计划的农资使用记录
     */
    @GetMapping("/{id}/materials")
    public Result<List<MaterialUsage>> getMaterials(@PathVariable Long id) {
        List<MaterialUsage> records = materialUsageService.getByPlanId(id);
        return Result.success(records);
    }
}
```

### 4. 前端改造

**统一API调用**：
```javascript
// api/phenology.js
import request from '@/utils/request'

export default {
  // 分页查询
  page(params) {
    return request({
      url: '/api/v1/phenology-records',
      method: 'get',
      params
    })
  },
  
  // 根据ID查询
  getById(id) {
    return request({
      url: `/api/v1/phenology-records/${id}`,
      method: 'get'
    })
  },
  
  // 保存
  save(data) {
    return request({
      url: '/api/v1/phenology-records',
      method: 'post',
      data
    })
  },
  
  // 更新
  update(id, data) {
    return request({
      url: `/api/v1/phenology-records/${id}`,
      method: 'put',
      data
    })
  },
  
  // 删除
  delete(id) {
    return request({
      url: `/api/v1/phenology-records/${id}`,
      method: 'delete'
    })
  },
  
  // 根据种植计划ID查询
  getByPlanId(planId) {
    return request({
      url: `/api/v1/plans/${planId}/phenology`,
      method: 'get'
    })
  }
}
```

**统一数据展示**：
```vue
<template>
  <div class="phenology-record-list">
    <!-- 列表展示 -->
    <el-table :data="records">
      <el-table-column prop="planName" label="种植计划" />
      <el-table-column prop="planCode" label="计划编号" />
      <el-table-column prop="phenologyName" label="物候期名称" />
      <el-table-column prop="phenologyDate" label="日期" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import phenologyApi from '@/api/phenology'
import { useRoute } from 'vue-router'

const route = useRoute()
const records = ref([])

onMounted(async () => {
  const planId = route.params.planId
  const res = await phenologyApi.getByPlanId(planId)
  records.value = res.data
})

const getStatusType = (status) => {
  const map = { 1: 'success', 2: 'warning' }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = { 1: '正常', 2: '异常' }
  return map[status] || '未知'
}
</script>
```

---

## 实施步骤

### 第一阶段：数据模型统一（1-2天）
1. ✅ 创建BaseEntity基类
2. ✅ 创建统一枚举类
3. ✅ 改造现有实体类
4. ✅ 添加关联字段

### 第二阶段：API接口统一（2-3天）
1. ✅ 统一响应格式
2. ✅ 统一接口命名
3. ✅ 实现关联查询接口
4. ✅ 更新Controller层

### 第三阶段：Service层改造（2-3天）
1. ✅ 创建BaseService接口
2. ✅ 实现关联查询逻辑
3. ✅ 实现数据填充逻辑
4. ✅ 添加业务逻辑

### 第四阶段：前后端联调（2-3天）
1. ✅ 更新前端API调用
2. ✅ 更新前端数据展示
3. ✅ 测试关联功能
4. ✅ 优化用户体验

### 第五阶段：测试与优化（1-2天）
1. ✅ 单元测试
2. ✅ 集成测试
3. ✅ 性能优化
4. ✅ 文档更新

---

## 预期效果

### 数据统一
- ✅ 所有实体类继承BaseEntity
- ✅ 统一字段命名规范
- ✅ 统一状态枚举
- ✅ 统一数据关联

### API统一
- ✅ 统一响应格式
- ✅ 统一接口命名
- ✅ 统一参数规范
- ✅ 统一错误处理

### 逻辑关联
- ✅ 种植计划关联所有业务数据
- ✅ 自动生成关联数据
- ✅ 自动推荐农资
- ✅ 自动更新状态

### 用户体验
- ✅ 数据展示更完整
- ✅ 操作流程更顺畅
- ✅ 信息查询更便捷
- ✅ 系统使用更友好

---

**现在开始实施统一数据模型和API接口规范！**

🎯
