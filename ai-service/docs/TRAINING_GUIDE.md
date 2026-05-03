# 病虫害图像识别模型训练完整指南

## 📋 目录

1. [当前流程分析](#当前流程分析)
2. [数据集资源](#数据集资源)
3. [训练步骤](#训练步骤)
4. [使用说明](#使用说明)

---

## 一、当前流程分析

### 1. 图像识别完整流程

```
用户上传图像
    ↓
API接口 (POST /api/image/diagnose)
    ↓
格式验证 (JPEG/PNG, 最大10MB)
    ↓
图像预处理
    ├─ 调整尺寸: 224×224
    ├─ 转换为Tensor
    └─ 标准化: ImageNet均值和标准差
    ↓
模型推理 (MobileNetV3 Small)
    ↓
Softmax概率计算
    ↓
置信度判断 (阈值0.6)
    ↓
返回结果 (病虫害名称 + 置信度 + 治疗建议)
```

### 2. 核心组件

| 组件 | 文件 | 功能 |
|------|------|------|
| API接口 | `app/image_recognition.py` | 接收图像、验证、返回结果 |
| 识别服务 | `app/models/services/image_service.py` | 模型加载、预处理、推理 |
| 模型文件 | `models/mobilenetv3.pth` | MobileNetV3 Small (5.97MB) |
| 配置文件 | `config.yaml` | 模型路径、阈值等配置 |

### 3. 当前问题

- ❌ 使用ImageNet预训练权重，未在病虫害数据上训练
- ❌ 识别准确率低（置信度通常<0.2）
- ❌ 缺少真实病虫害图像数据

---

## 二、数据集资源

### 推荐数据集（已标注来源）

#### 1. PlantVillage Dataset ⭐⭐⭐⭐⭐
- **来源**: Penn State University
- **网址**: https://plantvillage.psu.edu/
- **GitHub**: https://github.com/spMohanty/PlantVillage-Dataset
- **Kaggle**: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
- **数据**: 54,305张图像，38类
- **包含**: 玉米大斑病、部分小麦病害
- **引用**: Mohanty et al., 2016

#### 2. PlantDoc Dataset ⭐⭐⭐⭐⭐
- **来源**: Singh et al., 2019
- **GitHub**: https://github.com/pratikkamal/PlantDoc-Dataset
- **论文**: https://arxiv.org/abs/1911.09348
- **数据**: 2,589张图像，27类
- **包含**: 小麦白粉病、稻瘟病、玉米大斑病

#### 3. Rice Diseases Dataset ⭐⭐⭐⭐
- **来源**: Kaggle
- **网址**: https://www.kaggle.com/minhhuy2810/rice-diseases-image-dataset
- **数据**: 1,200张图像，4类
- **包含**: 稻瘟病

#### 4. Wheat Disease Dataset ⭐⭐⭐⭐
- **来源**: Kaggle
- **网址**: https://www.kaggle.com/olympic2019/wheat-disease-dataset
- **数据**: 3,000+张图像
- **包含**: 小麦白粉病

#### 5. Corn Disease Dataset ⭐⭐⭐⭐
- **来源**: Kaggle
- **网址**: https://www.kaggle.com/smaranjitghose/corn-or-maize-leaf-disease-dataset
- **数据**: 1,800张图像，4类
- **包含**: 玉米大斑病

#### 6. IP102 Dataset ⭐⭐⭐⭐⭐
- **来源**: Wu et al., 2019
- **论文**: https://arxiv.org/abs/1908.01900
- **下载**: http://mftp.mmcheng.net/MLPart/IP102.rar
- **数据**: 75,000+张图像，102类害虫
- **包含**: 蚜虫、红蜘蛛、白粉虱

### 数据集统计

| 数据集 | 图像数 | 包含目标病害 | 推荐度 |
|--------|--------|-------------|--------|
| PlantVillage | 54,305 | 玉米大斑病 | ⭐⭐⭐⭐⭐ |
| PlantDoc | 2,589 | 小麦白粉病、稻瘟病、玉米大斑病 | ⭐⭐⭐⭐⭐ |
| Rice Diseases | 1,200 | 稻瘟病 | ⭐⭐⭐⭐ |
| Wheat Disease | 3,000+ | 小麦白粉病 | ⭐⭐⭐⭐ |
| Corn Disease | 1,800 | 玉米大斑病 | ⭐⭐⭐⭐ |
| IP102 | 75,000+ | 蚜虫、红蜘蛛、白粉虱 | ⭐⭐⭐⭐⭐ |

---

## 三、训练步骤

### 步骤1: 下载真实数据集

```bash
cd ai-service

# 运行下载脚本
python scripts/download_datasets.py

# 选择下载选项:
# a - 下载所有数据集（推荐）
# b - 快速下载（仅小规模数据集）
```

**手动下载方法**:

```bash
# 安装Kaggle CLI
pip install kaggle

# 配置API密钥（从 https://www.kaggle.com/account 下载）
# 将kaggle.json放到 ~/.kaggle/ 目录

# 下载各个数据集
kaggle datasets download -d abdallahalidev/plantvillage-dataset
kaggle datasets download -d minhhuy2810/rice-diseases-image-dataset
kaggle datasets download -d olympic2019/wheat-disease-dataset
kaggle datasets download -d smaranjitghose/corn-or-maize-leaf-disease-dataset

# 下载PlantDoc
git clone https://github.com/pratikkamal/PlantDoc-Dataset.git
```

### 步骤2: 准备和标注数据

```bash
# 运行数据准备脚本
python scripts/prepare_dataset.py
```

**脚本功能**:
- 整理数据集为统一格式
- 映射标签到6类目标病虫害
- 验证图像有效性
- 划分训练集(70%)、验证集(15%)、测试集(15%)

**输出目录结构**:
```
data/
├── train/
│   ├── 小麦白粉病/
│   ├── 稻瘟病/
│   ├── 玉米大斑病/
│   ├── 蚜虫/
│   ├── 红蜘蛛/
│   └── 白粉虱/
├── val/
│   └── (同上)
└── test/
    └── (同上)
```

### 步骤3: 微调训练模型

```bash
# 运行训练脚本
python scripts/train_model.py
```

**训练参数**:
- Epochs: 50
- Batch Size: 32
- Learning Rate: 0.001
- 优化器: Adam
- 调度器: Cosine Annealing
- 数据增强: 随机裁剪、翻转、旋转、颜色抖动

**训练策略**:
1. **第一阶段**: 冻结骨干网络，只训练分类器
2. **第二阶段**: 解冻骨干网络，端到端微调（可选）

**输出文件**:
- `models/mobilenetv3_finetuned.pth` - 微调后的模型
- `models/training_history.json` - 训练历史

### 步骤4: 评估和部署

```bash
# 测试集评估（训练脚本会自动执行）
# 输出各类别准确率和总体准确率

# 部署新模型
# 将 models/mobilenetv3_finetuned.pth 复制为 models/mobilenetv3.pth
# 或修改 config.yaml 中的模型路径
```

---

## 四、使用说明

### 1. 完整训练流程

```bash
# 1. 下载数据集
python scripts/download_datasets.py

# 2. 准备数据
python scripts/prepare_dataset.py

# 3. 训练模型
python scripts/train_model.py

# 4. 重启AI服务
python app/main.py
```

### 2. 快速开始（使用小规模数据）

```bash
# 快速下载
python scripts/download_datasets.py  # 选择 'b'

# 准备和训练
python scripts/prepare_dataset.py
python scripts/train_model.py
```

### 3. API调用示例

```python
import requests

# 上传图像进行识别
url = "http://localhost:8000/api/image/diagnose"
files = {'image': open('disease_image.jpg', 'rb')}
response = requests.post(url, files=files)

result = response.json()
print(f"病虫害: {result['result']['disease_name']}")
print(f"置信度: {result['result']['confidence']}")
print(f"治疗建议: {result['result']['treatment_suggestion']}")
```

### 4. 预期效果

**训练前**:
- 置信度: < 0.2
- 准确率: 随机猜测水平
- 无法有效识别

**训练后**:
- 置信度: > 0.7
- 准确率: 80-95%
- 能准确识别6类病虫害

---

## 五、文件清单

### 脚本文件

| 文件 | 功能 |
|------|------|
| `scripts/download_datasets.py` | 下载公开数据集 |
| `scripts/prepare_dataset.py` | 准备和标注数据 |
| `scripts/train_model.py` | 模型微调训练 |
| `scripts/download_mobilenetv3.py` | 创建基础模型 |
| `scripts/test_image_recognition.py` | 测试识别功能 |

### 文档文件

| 文件 | 内容 |
|------|------|
| `docs/IMAGE_RECOGNITION_FLOW.md` | 图像识别流程详解 |
| `docs/PLANT_DISEASE_DATASETS.md` | 数据集资源汇总 |
| `docs/TRAINING_GUIDE.md` | 本文档 |

### 数据目录

| 目录 | 内容 |
|------|------|
| `data/datasets/` | 下载的原始数据集 |
| `data/processed/` | 处理后的统一格式数据 |
| `data/train/` | 训练集 |
| `data/val/` | 验证集 |
| `data/test/` | 测试集 |
| `models/` | 模型文件 |

---

## 六、注意事项

### 1. 数据集引用

使用数据集时请引用原始论文：

```bibtex
@article{mohanty2016using,
  title={Using deep learning for image-based plant disease detection},
  author={Mohanty, Sharada P and Hughes, David P and Salath{\'e}, Marcel},
  journal={arXiv preprint arXiv:1604.03169},
  year={2016}
}

@article{singh2020plantdoc,
  title={PlantDoc: A Dataset for Visual Plant Disease Detection},
  author={Singh, Davinder and Jain, Kanchan and Hazarika, Gaurav},
  journal={arXiv preprint arXiv:1911.09348},
  year={2019}
}
```

### 2. 训练建议

- **数据量**: 建议每类至少100张图像
- **数据增强**: 使用多种增强技术提高泛化能力
- **学习率**: 从小学习率开始，逐步调整
- **验证**: 定期在验证集上评估，保存最佳模型

### 3. 硬件要求

- **GPU**: 推荐使用GPU训练（CPU训练较慢）
- **内存**: 至少8GB RAM
- **存储**: 数据集约需5-10GB空间

---

## 七、故障排除

### 问题1: Kaggle下载失败

**解决方法**:
1. 确保已安装kaggle CLI: `pip install kaggle`
2. 配置API密钥到 `~/.kaggle/kaggle.json`
3. 或手动从网页下载

### 问题2: 内存不足

**解决方法**:
- 减小batch_size（如16或8）
- 减少数据加载器workers数量
- 使用更小的图像尺寸

### 问题3: 训练不收敛

**解决方法**:
- 降低学习率
- 增加数据增强
- 检查数据标注是否正确
- 尝试不同的优化器

---

**文档创建时间**: 2026-04-17
**适用版本**: MobileNetV3 Small
**目标类别**: 6类病虫害
**预计训练时间**: 2-4小时（GPU）/ 8-12小时（CPU）

🎯
