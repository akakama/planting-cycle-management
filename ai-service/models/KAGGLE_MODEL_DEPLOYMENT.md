# Kaggle模型部署指南

## 训练结果

- **模型**: MobileNetV3 Large
- **数据集**: PlantVillage (38类，54,305张图片)
- **最佳准确率**: 98.69%
- **训练时间**: 31.25分钟
- **设备**: Tesla T4 GPU (Kaggle)

## 部署步骤

### 1. 从Kaggle下载模型文件

在Kaggle Notebook的右侧"Output"面板，下载以下文件：
- `mobilenetv3_best.pth` - 最佳模型权重（推荐）
- `mobilenetv3_final.pth` - 最终模型权重
- `class_mapping.json` - 类别映射
- `training_history.json` - 训练历史（可选）

### 2. 放置模型文件

将下载的文件放到项目的 `ai-service/models/` 目录：

```
planting-cycle-management/
└── ai-service/
    └── models/
        ├── mobilenetv3_best.pth      ← 最佳模型（98.69%准确率）
        └── class_mapping.json         ← 类别映射
```

### 3. 验证部署

运行测试脚本：

```bash
cd ai-service
python scripts/test_image_recognition.py
```

### 4. 启动服务

```bash
cd ai-service
python -m app.main
```

服务启动后，图像识别接口将自动加载Kaggle训练的模型。

## API使用示例

### 请求

```bash
curl -X POST "http://localhost:8000/api/image/diagnose" \
  -H "accept: application/json" \
  -F "image=@/path/to/plant_image.jpg"
```

### 响应

```json
{
  "success": true,
  "message": "识别成功",
  "result": {
    "disease_name": "番茄晚疫病（Tomato Late Blight）",
    "confidence": 0.9523,
    "treatment_suggestion": "喷施甲霜灵或烯酰吗啉，降低田间湿度"
  }
}
```

## 支持的38种病虫害

| 编号 | 作物 | 病害 | 中文名 |
|------|------|------|--------|
| 0-3 | 苹果 | 疮痂病、黑腐病、锈病、健康 | Apple Scab, Black Rot, Cedar Rust, Healthy |
| 4 | 蓝莓 | 健康 | Blueberry Healthy |
| 5-6 | 樱桃 | 白粉病、健康 | Cherry Powdery Mildew, Healthy |
| 7-10 | 玉米 | 灰斑病、锈病、大斑病、健康 | Corn Gray Leaf Spot, Common Rust, Northern Leaf Blight, Healthy |
| 11-14 | 葡萄 | 黑腐病、黑痘病、叶枯病、健康 | Grape Black Rot, Esca, Leaf Blight, Healthy |
| 15 | 柑橘 | 黄龙病 | Orange Huanglongbing |
| 16-17 | 桃 | 细菌性穿孔病、健康 | Peach Bacterial Spot, Healthy |
| 18-19 | 辣椒 | 细菌性斑点病、健康 | Pepper Bacterial Spot, Healthy |
| 20-22 | 马铃薯 | 早疫病、晚疫病、健康 | Potato Early Blight, Late Blight, Healthy |
| 23 | 树莓 | 健康 | Raspberry Healthy |
| 24 | 大豆 | 健康 | Soybean Healthy |
| 25 | 南瓜 | 白粉病 | Squash Powdery Mildew |
| 26-27 | 草莓 | 叶焦病、健康 | Strawberry Leaf Scorch, Healthy |
| 28-37 | 番茄 | 细菌性斑点病、早疫病、晚疫病、叶霉病、叶斑病、红蜘蛛、斑点病、黄化曲叶病毒、花叶病毒、健康 | Tomato Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy |

## 性能优化建议

### GPU加速

如果服务器有GPU，模型会自动使用GPU加速。检查GPU：

```python
import torch
print(torch.cuda.is_available())  # True表示GPU可用
print(torch.cuda.get_device_name(0))  # GPU型号
```

### 批量推理

对于大量图片，建议使用批量推理：

```python
import torch
from PIL import Image
from torchvision import transforms

# 批量预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 批量推理
batch_tensors = torch.stack([transform(img) for img in images])
with torch.no_grad():
    outputs = model(batch_tensors.to(device))
```

## 故障排除

### 问题1: 模型加载失败

**错误**: `RuntimeError: Error(s) in loading state_dict`

**解决**: 确保下载的是 `mobilenetv3_best.pth` 而不是其他文件

### 问题2: 内存不足

**错误**: `CUDA out of memory`

**解决**: 使用CPU模式或减小batch size

```python
# 强制使用CPU
device = torch.device('cpu')
model.to(device)
```

### 问题3: 识别准确率低

**可能原因**:
- 图片质量差、模糊
- 拍摄角度不标准
- 光线不足或过曝
- 病害不在38类范围内

**建议**:
- 提供清晰、标准角度的图片
- 确保光线充足
- 检查病害是否在支持列表中

## 更新日志

- **2026-05-02**: 在Kaggle训练完成，准确率98.69%
- 支持38种病虫害识别
- 集成到planting-cycle-management项目
