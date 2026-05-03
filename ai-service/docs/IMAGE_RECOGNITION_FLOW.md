# 图像识别流程详细分析

## 一、当前图像识别流程

### 1. 完整流程图

```
用户上传图像
    ↓
API接口接收 (POST /api/image/diagnose)
    ↓
格式验证 (JPEG/PNG/JPG)
    ↓
大小验证 (最大10MB)
    ↓
图像预处理
    ├─ 调整尺寸 (224×224)
    ├─ 转换为Tensor
    └─ 标准化 (ImageNet均值和标准差)
    ↓
模型推理 (MobileNetV3)
    ↓
Softmax概率计算
    ↓
置信度判断 (阈值0.6)
    ↓
返回结果 (病虫害名称 + 治疗建议)
```

### 2. 核心组件详解

#### 2.1 API接口层 (`app/image_recognition.py`)

**功能**：
- 接收用户上传的图像文件
- 验证图像格式和大小
- 调用图像识别服务
- 返回识别结果

**关键代码**：
```python
@router.post("/api/image/diagnose", response_model=ImageDiagnoseResponse)
async def diagnose_image(image: UploadFile = File(...)):
    # 验证格式
    if image.content_type not in config.image_recognition.supported_formats:
        raise HTTPException(status_code=400, detail="不支持的图像格式")

    # 读取图像
    image_bytes = await image.read()

    # 调用服务
    result = await image_service.diagnose_disease(
        image_bytes=image_bytes,
        confidence_threshold=0.6
    )
```

#### 2.2 图像识别服务 (`app/models/services/image_service.py`)

**功能**：
- 加载MobileNetV3模型
- 图像预处理
- 模型推理
- 结果后处理

**关键组件**：

##### A. 模型加载
```python
def __init__(self):
    # 加载预训练模型
    self.model = torch.load(config.image_recognition.model_path)
    self.model.eval()  # 设置为评估模式
```

##### B. 图像预处理
```python
self.transform = transforms.Compose([
    transforms.Resize((224, 224)),           # 调整尺寸
    transforms.ToTensor(),                    # 转为Tensor
    transforms.Normalize(                     # 标准化
        [0.485, 0.456, 0.406],               # ImageNet均值
        [0.229, 0.224, 0.225]                # ImageNet标准差
    )
])
```

##### C. 推理流程
```python
async def diagnose_disease(self, image_bytes, confidence_threshold=0.6):
    # 1. 加载图像
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert('RGB')

    # 2. 预处理
    input_tensor = self.transform(image).unsqueeze(0)

    # 3. 推理
    with torch.no_grad():
        outputs = self.model(input_tensor)
        probabilities = F.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    # 4. 判断置信度
    if confidence.item() < confidence_threshold:
        return None

    # 5. 返回结果
    disease_info = self.class_names[predicted.item()]
    return DiagnosisResult(
        disease_name=disease_info["name"],
        confidence=confidence.item(),
        treatment_suggestion=disease_info["treatment"]
    )
```

#### 2.3 模型架构 (`MobileNetV3 Small`)

**结构**：
```
输入: 224×224×3
    ↓
特征提取 (MobileNetV3 Small骨干网络)
    ↓
全局平均池化
    ↓
分类器:
    Linear(576, 1024)
    Hardswish()
    Dropout(0.2)
    Linear(1024, 6)
    ↓
输出: 6类病虫害概率
```

### 3. 支持的病虫害类别

| ID | 病虫害名称 | 治疗建议 |
|----|-----------|---------|
| 0 | 小麦白粉病 | 使用三唑酮等杀菌剂喷施，注意轮换使用以避免抗性 |
| 1 | 稻瘟病 | 使用三环唑等药剂防治，注意在发病初期及时施药 |
| 2 | 玉米大斑病 | 使用苯醚甲环唑等药剂，加强田间管理，及时清除病叶 |
| 3 | 蚜虫 | 使用吡虫啉等杀虫剂，注意保护天敌，避免在花期使用 |
| 4 | 红蜘蛛 | 使用阿维菌素等杀螨剂，注意轮换用药，避免产生抗性 |
| 5 | 白粉虱 | 使用噻虫嗪等药剂，配合黄色粘虫板进行物理防治 |

### 4. 当前使用的组件

| 组件 | 用途 | 文件路径 |
|------|------|---------|
| FastAPI | Web框架 | `app/main.py` |
| PyTorch | 深度学习框架 | `requirements.txt` |
| torchvision | 图像处理和模型 | `requirements.txt` |
| PIL | 图像加载 | `requirements.txt` |
| MobileNetV3 | 特征提取模型 | `models/mobilenetv3.pth` |

### 5. 数据流示例

```
输入: 用户上传的小麦叶片图像 (JPEG, 2.3MB)
    ↓
验证: 格式✓ 大小✓
    ↓
预处理:
    - 原始: 1920×1080×3
    - 调整: 224×224×3
    - Tensor: [1, 3, 224, 224]
    - 标准化: 均值[0.485, 0.456, 0.406]
    ↓
推理:
    - MobileNetV3输出: [1, 6]
    - Softmax: [0.1768, 0.1654, 0.1689, 0.1623, 0.1587, 0.1679]
    - 最大值: 类别0 (小麦白粉病), 置信度0.1768
    ↓
判断: 0.1768 < 0.6 → 置信度过低
    ↓
输出: None (无法识别)
```

## 二、当前问题分析

### 1. 模型问题
- ❌ 使用ImageNet预训练权重，未在病虫害数据上训练
- ❌ 识别准确率低（置信度通常<0.2）
- ❌ 无法有效区分不同病虫害

### 2. 数据问题
- ❌ 缺少真实的病虫害图像数据集
- ❌ 没有标注数据用于训练
- ❌ 模型未见过实际的病虫害特征

### 3. 改进方向
- ✅ 收集真实病虫害图像数据集
- ✅ 对模型进行微调训练
- ✅ 调整置信度阈值
- ✅ 增加数据增强

## 三、下一步计划

1. **搜索真实数据集**：寻找公开的病虫害图像数据集
2. **数据准备**：下载、整理、标注数据
3. **模型微调**：使用真实数据训练模型
4. **评估优化**：测试模型性能，调整参数

---

**文档创建时间**: 2026-04-17
**当前模型状态**: 已部署但未训练
**需要改进**: 数据集收集和模型微调
