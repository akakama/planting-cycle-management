# 快速开始指南

## 🚀 一键训练流程

### 前提条件

1. 已安装Python 3.8+
2. 已安装PyTorch和torchvision
3. （可选）已配置Kaggle CLI用于下载数据集

### 快速执行

```bash
# 进入AI服务目录
cd ai-service

# 步骤1: 下载数据集（选择 'b' 快速下载）
python scripts/download_datasets.py

# 步骤2: 准备数据
python scripts/prepare_dataset.py

# 步骤3: 训练模型
python scripts/train_model.py

# 步骤4: 重启服务
python app/main.py
```

## 📋 详细步骤

### 1. 下载数据集

**自动下载**（推荐）:
```bash
python scripts/download_datasets.py
# 选择 'a' - 下载所有数据集
# 或选择 'b' - 快速下载（小规模）
```

**手动下载**:
- PlantVillage: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
- Rice Diseases: https://www.kaggle.com/minhhuy2810/rice-diseases-image-dataset
- Wheat Disease: https://www.kaggle.com/olympic2019/wheat-disease-dataset
- Corn Disease: https://www.kaggle.com/smaranjitghose/corn-or-maize-leaf-disease-dataset
- PlantDoc: https://github.com/pratikkamal/PlantDoc-Dataset

### 2. 准备数据

```bash
python scripts/prepare_dataset.py
```

**输出**:
- `data/train/` - 训练集（70%）
- `data/val/` - 验证集（15%）
- `data/test/` - 测试集（15%）

### 3. 训练模型

```bash
python scripts/train_model.py
```

**训练参数**:
- Epochs: 50
- Batch Size: 32
- Learning Rate: 0.001
- 预计时间: 2-4小时（GPU）

### 4. 测试和使用

**测试识别**:
```bash
python scripts/test_image_recognition.py
```

**API调用**:
```python
import requests

url = "http://localhost:8000/api/image/diagnose"
files = {'image': open('your_image.jpg', 'rb')}
response = requests.post(url, files=files)

print(response.json())
```

## ⚙️ 配置选项

### 修改训练参数

编辑 `scripts/train_model.py`:

```python
trainer.train(
    epochs=100,        # 训练轮数
    batch_size=16,     # 批次大小
    learning_rate=0.0001,  # 学习率
    freeze_backbone=False  # 是否冻结骨干网络
)
```

### 修改置信度阈值

编辑 `config.yaml`:

```yaml
image_recognition:
  confidence_threshold: 0.5  # 降低阈值以获取更多结果
```

## 📊 预期结果

### 训练前
- 准确率: ~16.7%
- 置信度: < 0.2
- 效果: 无法有效识别

### 训练后
- 准确率: 80-95%
- 置信度: > 0.7
- 效果: 准确识别6类病虫害

## 🔧 故障排除

### 问题: Kaggle下载失败

**解决**:
```bash
# 安装Kaggle CLI
pip install kaggle

# 配置API密钥
# 1. 访问 https://www.kaggle.com/account
# 2. 点击 "Create New API Token"
# 3. 将kaggle.json放到 ~/.kaggle/ 目录
```

### 问题: 内存不足

**解决**:
- 减小batch_size: 16或8
- 减少数据加载器workers
- 使用更小的图像尺寸

### 问题: 训练不收敛

**解决**:
- 降低学习率: 0.0001
- 增加数据增强
- 检查数据标注

## 📚 更多信息

- 完整分析报告: `docs/COMPLETE_ANALYSIS_REPORT.md`
- 训练指南: `docs/TRAINING_GUIDE.md`
- 数据集资源: `docs/PLANT_DISEASE_DATASETS.md`
- 流程分析: `docs/IMAGE_RECOGNITION_FLOW.md`

---

**创建时间**: 2026-04-17
**预计完成时间**: 4-6小时
**难度**: 中等

🎯
