# API接口文档

## 📋 概述

本文档描述了种植周期管理系统的所有API接口，包括请求格式、响应格式和接口说明。

## 🔐 认证

所有API接口都需要在请求头中携带认证信息：

```
Authorization: Bearer {token}
```

## 📦 统一响应格式

所有接口返回统一的JSON格式：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {},
  "timestamp": 1234567890
}
```

### 响应码说明

| 响应码 | 说明 |
|--------|------|
| 200 | 操作成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 📄 分页查询参数

所有分页查询接口都支持以下参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | Integer | 否 | 当前页，默认1 |
| size | Integer | 否 | 每页大小，默认10 |
| sort | String | 否 | 排序字段 |
| order | String | 否 | 排序方式，asc或desc |
| keyword | String | 否 | 搜索关键字 |

### 分页响应格式

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "records": [],
    "total": 100,
    "size": 10,
    "current": 1,
    "pages": 10
  },
  "timestamp": 1234567890
}
```

---

## 🌱 种植计划管理

### 1. 分页查询种植计划

**接口**：`GET /api/plans`

**参数**：
- page: 当前页
- size: 每页大小
- sort: 排序字段
- order: 排序方式
- keyword: 搜索关键字

**响应**：
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "records": [
      {
        "id": 1,
        "planCode": "PLAN-1234567890",
        "planName": "春季水稻种植计划",
        "cropId": 1,
        "cropName": "水稻",
        "plotId": 1,
        "plotName": "1号地块",
        "planStartDate": "2025-03-01",
        "planEndDate": "2025-07-15",
        "actualStartDate": "2025-03-05",
        "actualEndDate": null,
        "plantingArea": 100.5,
        "expectedYield": 50000.0,
        "actualYield": null,
        "status": 3,
        "statusDesc": "进行中",
        "createdBy": 1,
        "createdTime": "2025-03-01T10:00:00",
        "updatedBy": 1,
        "updatedTime": "2025-03-15T14:30:00",
        "deleted": 0,
        "version": 1,
        "tenantId": 0,
        "remarks": "春季水稻种植"
      }
    ],
    "total": 1,
    "size": 10,
    "current": 1,
    "pages": 1
  },
  "timestamp": 1234567890
}
```

### 2. 查询种植计划详情

**接口**：`GET /api/plans/{id}`

**响应**：
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "id": 1,
    "planCode": "PLAN-1234567890",
    "planName": "春季水稻种植计划",
    "cropName": "水稻",
    "plotName": "1号地块",
    "planStartDate": "2025-03-01",
    "planEndDate": "2025-07-15",
    "actualStartDate": "2025-03-05",
    "actualEndDate": null,
    "plantingArea": 100.5,
    "expectedYield": 50000.0,
    "actualYield": null,
    "status": 3,
    "remarks": "春季水稻种植",
    "phenologyRecords": [],
    "pestRecords": [],
    "materialUsages": [],
    "harvestRecords": [],
    "yieldPredictions": [],
    "phenologyCount": 0,
    "pestCount": 0,
    "materialCount": 0,
    "harvestCount": 0,
    "totalHarvestYield": 0.0,
    "totalSaleAmount": 0.0,
    "totalMaterialCost": 0.0
  },
  "timestamp": 1234567890
}
```

### 3. 创建种植计划

**接口**：`POST /api/plans`

**请求体**：
```json
{
  "planName": "春季水稻种植计划",
  "cropId": 1,
  "plotId": 1,
  "planStartDate": "2025-03-01",
  "planEndDate": "2025-07-15",
  "plantingArea": 100.5,
  "expectedYield": 50000.0,
  "remarks": "春季水稻种植"
}
```

### 4. 更新种植计划

**接口**：`PUT /api/plans/{id}`

**请求体**：同创建接口

### 5. 删除种植计划

**接口**：`DELETE /api/plans/{id}`

### 6. 更新种植计划状态

**接口**：`PUT /api/plans/{id}/status`

**参数**：
- status: 状态（0-草稿，1-已提交，2-已审核，3-进行中，4-已完成，5-已取消）
- actualEndDate: 实际结束日期（可选）
- actualYield: 实际产量（可选）

---

## 🌾 作物管理

### 1. 分页查询作物

**接口**：`GET /api/crops`

**参数**：
- page: 当前页
- size: 每页大小
- sort: 排序字段
- order: 排序方式
- keyword: 搜索关键字

### 2. 查询所有启用的作物

**接口**：`GET /api/crops/enabled`

### 3. 查询推荐的作物

**接口**：`GET /api/crops/recommended`

### 4. 根据类别查询作物

**接口**：`GET /api/crops/category/{category}`

### 5. 根据种植季节查询作物

**接口**：`GET /api/crops/season/{season}`

### 6. 根据种植难度查询作物

**接口**：`GET /api/crops/difficulty/{difficulty}`

### 7. 查询作物详情

**接口**：`GET /api/crops/{id}`

### 8. 创建作物

**接口**：`POST /api/crops`

**请求体**：
```json
{
  "cropName": "水稻",
  "variety": "杂交水稻",
  "category": "粮食作物",
  "growthCycleDays": 120,
  "plantingSeason": "春季、夏季",
  "description": "高产水稻品种",
  "origin": "中国",
  "suitableArea": "南方地区",
  "yieldReference": 500.0,
  "priceReference": 3.0,
  "difficulty": 2,
  "isRecommended": 1,
  "cropStatus": 1
}
```

### 9. 更新作物

**接口**：`PUT /api/crops/{id}`

### 10. 删除作物

**接口**：`DELETE /api/crops/{id}`

---

## 🐛 病虫害记录管理

### 1. 分页查询病虫害记录

**接口**：`GET /api/pests`

**参数**：
- page: 当前页
- size: 每页大小
- planId: 种植计划ID（可选）
- sort: 排序字段
- order: 排序方式
- keyword: 搜索关键字

### 2. 根据种植计划查询病虫害记录

**接口**：`GET /api/pests/plan/{planId}`

### 3. 创建病虫害记录

**接口**：`POST /api/pests`

**请求体**：
```json
{
  "planId": 1,
  "pestName": "稻飞虱",
  "pestType": "pest",
  "occurrenceDate": "2025-04-15",
  "severity": 2,
  "affectedArea": 10.5,
  "treatmentMethod": "喷洒农药",
  "chemicalUsed": "噻嗪酮",
  "treatmentDate": "2025-04-16",
  "treatmentResult": "有效",
  "imageUrl": "http://example.com/image.jpg",
  "remarks": "轻度虫害"
}
```

### 4. 更新病虫害记录

**接口**：`PUT /api/pests/{id}`

### 5. 删除病虫害记录

**接口**：`DELETE /api/pests/{id}`

### 6. 病虫害图片识别

**接口**：`POST /api/pests/identify`

**请求体**：
```json
{
  "imageUrl": "http://example.com/image.jpg"
}
```

**响应**：
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "success": true,
    "diseaseName": "稻飞虱",
    "confidence": 0.95,
    "treatmentAdvice": "使用噻嗪酮等药剂防治",
    "additionalInfo": "建议在傍晚施药"
  },
  "timestamp": 1234567890
}
```

### 7. 保存识别结果并创建记录

**接口**：`POST /api/pests/save-with-identify`

**请求体**：同创建病虫害记录

---

## 📅 物候期记录管理

### 1. 分页查询物候期记录

**接口**：`GET /api/phenology`

**参数**：
- page: 当前页
- size: 每页大小
- planId: 种植计划ID（可选）
- sort: 排序字段
- order: 排序方式
- keyword: 搜索关键字

### 2. 根据种植计划查询物候期记录

**接口**：`GET /api/phenology/plan/{planId}`

### 3. 创建物候期记录

**接口**：`POST /api/phenology`

**请求体**：
```json
{
  "planId": 1,
  "phenologyName": "播种期",
  "phenologyDate": "2025-03-05",
  "phenologyStatus": 1,
  "description": "完成播种工作",
  "imageUrl": "http://example.com/image.jpg",
  "expectedDate": "2025-03-01",
  "remarks": "天气适宜"
}
```

### 4. 更新物候期记录

**接口**：`PUT /api/phenology/{id}`

### 5. 删除物候期记录

**接口**：`DELETE /api/phenology/{id}`

---

## 💊 农资使用记录管理

### 1. 分页查询农资使用记录

**接口**：`GET /api/materials/usage`

**参数**：
- page: 当前页
- size: 每页大小
- planId: 种植计划ID（可选）
- materialId: 农资ID（可选）
- sort: 排序字段
- order: 排序方式
- keyword: 搜索关键字

### 2. 根据种植计划查询农资使用记录

**接口**：`GET /api/materials/usage/plan/{planId}`

### 3. 根据农资查询使用记录

**接口**：`GET /api/materials/usage/material/{materialId}`

### 4. 统计农资总成本

**接口**：`GET /api/materials/usage/plan/{planId}/total-cost`

**响应**：
```json
{
  "code": 200,
  "message": "操作成功",
  "data": 5000.0,
  "timestamp": 1234567890
}
```

### 5. 创建农资使用记录

**接口**：`POST /api/materials/usage`

**请求体**：
```json
{
  "planId": 1,
  "materialId": 1,
  "usageQuantity": 100.0,
  "unit": "kg",
  "usageDate": "2025-04-01",
  "applicationMethod": "喷洒",
  "operator": "张三",
  "unitPrice": 50.0,
  "totalPrice": 5000.0,
  "recommendType": "manual",
  "remarks": "施肥"
}
```

### 6. 更新农资使用记录

**接口**：`PUT /api/materials/usage/{id}`

### 7. 删除农资使用记录

**接口**：`DELETE /api/materials/usage/{id}`

---

## 🚜 农资管理

### 1. 分页查询农资

**接口**：`GET /api/materials`

**参数**：
- page: 当前页
- size: 每页大小
- sort: 排序字段
- order: 排序方式
- keyword: 搜索关键字

### 2. 查询所有启用的农资

**接口**：`GET /api/materials/enabled`

### 3. 查询推荐的农资

**接口**：`GET /api/materials/recommended`

### 4. 根据类型查询农资

**接口**：`GET /api/materials/type/{materialType}`

### 5. 根据类别查询农资

**接口**：`GET /api/materials/category/{category}`

### 6. 根据供应商查询农资

**接口**：`GET /api/materials/supplier/{supplier}`

### 7. 查询库存不足的农资

**接口**：`GET /api/materials/low-stock`

### 8. 查询农资详情

**接口**：`GET /api/materials/{id}`

### 9. 创建农资

**接口**：`POST /api/materials`

**请求体**：
```json
{
  "materialCode": "FERT-001",
  "materialName": "复合肥",
  "materialType": "fertilizer",
  "category": "氮磷钾复合肥",
  "specification": "15-15-15",
  "unit": "kg",
  "stockQuantity": 1000.0,
  "minStockWarning": 100.0,
  "unitPrice": 50.0,
  "supplier": "农资公司",
  "brand": "知名品牌",
  "storageCondition": "干燥通风",
  "isRecommended": 1,
  "materialStatus": 1
}
```

### 10. 更新农资

**接口**：`PUT /api/materials/{id}`

### 11. 删除农资

**接口**：`DELETE /api/materials/{id}`

---

## 🌾 采收记录管理

### 1. 分页查询采收记录

**接口**：`GET /api/harvests`

**参数**：
- page: 当前页
- size: 每页大小
- planId: 种植计划ID（可选）
- harvester: 采收人员（可选）
- sort: 排序字段
- order: 排序方式
- keyword: 搜索关键字

### 2. 根据种植计划查询采收记录

**接口**：`GET /api/harvests/plan/{planId}`

### 3. 根据采收人员查询

**接口**：`GET /api/harvests/harvester/{harvester}`

### 4. 根据批次号查询

**接口**：`GET /api/harvests/batch/{batchNumber}`

### 5. 统计总产量

**接口**：`GET /api/harvests/plan/{planId}/total-yield`

### 6. 统计总销售额

**接口**：`GET /api/harvests/plan/{planId}/total-sale-amount`

### 7. 统计平均销售价格

**接口**：`GET /api/harvests/plan/{planId}/average-sale-price`

### 8. 创建采收记录

**接口**：`POST /api/harvests`

**请求体**：
```json
{
  "planId": 1,
  "harvestDate": "2025-07-10",
  "actualYield": 48000.0,
  "qualityGrade": 1,
  "saleAmount": 144000.0,
  "harvester": "张三",
  "batchNumber": "BATCH-20250710-001",
  "storageLocation": "1号仓库",
  "remarks": "丰收"
}
```

### 9. 更新采收记录

**接口**：`PUT /api/harvests/{id}`

### 10. 删除采收记录

**接口**：`DELETE /api/harvests/{id}`

---

## 📊 枚举值说明

### 种植计划状态（PlanStatus）

| 值 | 说明 |
|----|------|
| 0 | 草稿 |
| 1 | 已提交 |
| 2 | 已审核 |
| 3 | 进行中 |
| 4 | 已完成 |
| 5 | 已取消 |

### 病虫害严重程度（PestSeverity）

| 值 | 说明 |
|----|------|
| 1 | 低 |
| 2 | 中 |
| 3 | 高 |
| 4 | 严重 |

### 采收质量等级（QualityGrade）

| 值 | 说明 |
|----|------|
| 1 | 优 |
| 2 | 良 |
| 3 | 中 |
| 4 | 差 |

### 物候期状态（PhenologyStatus）

| 值 | 说明 |
|----|------|
| 1 | 正常 |
| 2 | 异常 |
| 3 | 延迟 |
| 4 | 提前 |

### 病虫害类型（PestType）

| 值 | 说明 |
|----|------|
| disease | 病害 |
| pest | 虫害 |

### 农资类型（MaterialType）

| 值 | 说明 |
|----|------|
| fertilizer | 肥料 |
| pesticide | 农药 |
| seed | 种子 |
| tool | 工具 |
| other | 其他 |

---

## 🔒 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 操作成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 📝 注意事项

1. 所有日期格式统一使用：`yyyy-MM-dd`
2. 所有时间格式统一使用：`yyyy-MM-ddTHH:mm:ss`
3. 所有金额单位统一使用：元
4. 所有数量单位根据具体业务确定
5. 分页查询默认返回10条记录
6. 排序默认按创建时间降序
7. 关键字搜索支持模糊匹配

---

**API接口文档版本：v2.0.0**
**最后更新时间：2025-06-18**
