# 真实病虫害图像数据集资源

## 一、公开数据集汇总

### 1. PlantVillage Dataset ⭐⭐⭐⭐⭐
**来源**: Penn State University
**网址**: https://plantvillage.psu.edu/
**GitHub**: https://github.com/spMohanty/PlantVillage-Dataset

**数据集信息**:
- **图像数量**: 54,305张
- **类别数量**: 38类（14种植物，包含健康和病害）
- **图像尺寸**: 256×256
- **格式**: JPG
- **大小**: 约1.5GB

**包含的病虫害**:
- ✅ 苹果：苹果黑星病、苹果锈病
- ✅ 玉米：玉米大斑病、玉米灰斑病、玉米锈病
- ✅ 马铃薯：早疫病、晚疫病
- ✅ 番茄：早疫病、晚疫病、叶霉病、斑点病等
- ✅ 葡萄：黑腐病、叶枯病等
- ✅ 小麦：部分病害图像

**下载方式**:
```bash
# 从GitHub下载
git clone https://github.com/spMohanty/PlantVillage-Dataset.git

# 或从Kaggle下载
kaggle datasets download -d abdallahalidev/plantvillage-dataset
```

**许可证**: CC0 Public Domain

---

### 2. PlantDoc Dataset ⭐⭐⭐⭐
**来源**: Research Paper "PlantDoc: A Dataset for Visual Plant Disease Detection"
**GitHub**: https://github.com/pratikkamal/PlantDoc-Dataset

**数据集信息**:
- **图像数量**: 2,589张
- **类别数量**: 13种植物，27类病害
- **特点**: 真实田间环境，背景复杂

**包含的病虫害**:
- ✅ 小麦：小麦叶锈病、小麦白粉病
- ✅ 玉米：玉米大斑病、玉米锈病
- ✅ 水稻：稻瘟病、纹枯病
- ✅ 番茄：多种病害
- ✅ 马铃薯：早疫病、晚疫病

**下载方式**:
```bash
git clone https://github.com/pratikkamal/PlantDoc-Dataset.git
```

**论文**: https://arxiv.org/abs/1911.09348

---

### 3. Rice Diseases Dataset ⭐⭐⭐⭐
**来源**: Kaggle
**网址**: https://www.kaggle.com/minhhuy2810/rice-diseases-image-dataset

**数据集信息**:
- **图像数量**: 1,200张
- **类别数量**: 4类（健康 + 3种病害）
- **病害类型**:
  - 稻瘟病 (Blast)
  - 细菌性叶枯病 (Bacterial Blight)
  - 褐斑病 (Brown Spot)

**下载方式**:
```bash
kaggle datasets download -d minhhuy2810/rice-diseases-image-dataset
```

---

### 4. Wheat Disease Dataset ⭐⭐⭐⭐
**来源**: Kaggle
**网址**: https://www.kaggle.com/olympic2019/wheat-disease-dataset

**数据集信息**:
- **图像数量**: 3,000+张
- **类别数量**: 多种小麦病害
- **病害类型**:
  - 小麦白粉病
  - 小麦锈病
  - 小麦赤霉病

**下载方式**:
```bash
kaggle datasets download -d olympic2019/wheat-disease-dataset
```

---

### 5. Corn or Maize Leaf Disease Dataset ⭐⭐⭐⭐
**来源**: Kaggle
**网址**: https://www.kaggle.com/smaranjitghose/corn-or-maize-leaf-disease-dataset

**数据集信息**:
- **图像数量**: 1,800张
- **类别数量**: 4类
- **病害类型**:
  - 玉米大斑病 (Gray Leaf Spot)
  - 玉米锈病 (Common Rust)
  - 玉米北方叶枯病 (Northern Leaf Blight)

**下载方式**:
```bash
kaggle datasets download -d smaranjitghose/corn-or-maize-leaf-disease-dataset
```

---

### 6. IP102 Dataset ⭐⭐⭐⭐
**来源**: Insect Pest Recognition Dataset
**论文**: https://arxiv.org/abs/1908.01900

**数据集信息**:
- **图像数量**: 75,000+张
- **类别数量**: 102类害虫
- **特点**: 专门针对害虫识别

**包含的害虫**:
- ✅ 蚜虫类
- ✅ 红蜘蛛
- ✅ 白粉虱
- ✅ 其他农业害虫

**下载方式**:
- 官方网站: http://mftp.mmcheng.net/MLPart/IP102.rar

---

### 7. AgriVision Dataset ⭐⭐⭐
**来源**: Agricultural Disease Detection
**网址**: https://www.kaggle.com/farahsebaba/agrivision-dataset

**数据集信息**:
- **图像数量**: 5,000+张
- **类别数量**: 多种作物病害
- **特点**: 包含多种作物

---

### 8. Plant-Pathology Dataset ⭐⭐⭐⭐
**来源**: Kaggle Competition
**网址**: https://www.kaggle.com/c/plant-pathology-2021-fgvc8

**数据集信息**:
- **图像数量**: 18,000+张
- **类别数量**: 12类
- **作物**: 苹果
- **病害**: 多种苹果病害

---

## 二、数据集对比分析

| 数据集 | 图像数量 | 类别数 | 包含目标病害 | 推荐度 |
|--------|---------|--------|-------------|--------|
| PlantVillage | 54,305 | 38 | 玉米大斑病、部分小麦病害 | ⭐⭐⭐⭐⭐ |
| PlantDoc | 2,589 | 27 | 小麦白粉病、稻瘟病、玉米大斑病 | ⭐⭐⭐⭐⭐ |
| Rice Diseases | 1,200 | 4 | 稻瘟病 | ⭐⭐⭐⭐ |
| Wheat Disease | 3,000+ | 多种 | 小麦白粉病 | ⭐⭐⭐⭐ |
| Corn Disease | 1,800 | 4 | 玉米大斑病 | ⭐⭐⭐⭐ |
| IP102 | 75,000+ | 102 | 蚜虫、红蜘蛛、白粉虱 | ⭐⭐⭐⭐⭐ |

## 三、推荐数据集组合

### 方案一：全面覆盖（推荐）
```
PlantVillage (基础) + PlantDoc (补充) + IP102 (害虫)
```
- **优点**: 覆盖所有6种目标病虫害
- **图像总数**: 约130,000张
- **训练时间**: 较长

### 方案二：精简高效
```
PlantDoc (病害) + IP102 (害虫)
```
- **优点**: 数据量适中，针对性强
- **图像总数**: 约77,000张
- **训练时间**: 适中

### 方案三：快速验证
```
Rice Diseases + Wheat Disease + Corn Disease
```
- **优点**: 数据量小，快速训练
- **图像总数**: 约6,000张
- **训练时间**: 短

## 四、数据集下载脚本

### 1. Kaggle数据集下载

**前提条件**:
```bash
# 安装Kaggle CLI
pip install kaggle

# 配置API密钥
# 1. 访问 https://www.kaggle.com/account
# 2. 点击 "Create New API Token"
# 3. 将kaggle.json放到 ~/.kaggle/ 目录
```

**下载命令**:
```bash
# PlantVillage
kaggle datasets download -d abdallahalidev/plantvillage-dataset

# Rice Diseases
kaggle datasets download -d minhhuy2810/rice-diseases-image-dataset

# Wheat Disease
kaggle datasets download -d olympic2019/wheat-disease-dataset

# Corn Disease
kaggle datasets download -d smaranjitghose/corn-or-maize-leaf-disease-dataset
```

### 2. GitHub数据集下载

```bash
# PlantDoc
git clone https://github.com/pratikkamal/PlantDoc-Dataset.git

# PlantVillage (原始)
git clone https://github.com/spMohanty/PlantVillage-Dataset.git
```

### 3. 直接下载

```bash
# IP102 Dataset
wget http://mftp.mmcheng.net/MLPart/IP102.rar
unrar x IP102.rar
```

## 五、数据集使用建议

### 1. 数据预处理
- 统一图像尺寸：224×224
- 数据增强：旋转、翻转、亮度调整
- 数据划分：训练集70%、验证集15%、测试集15%

### 2. 标签映射
需要将数据集的原始标签映射到我们的6类病虫害：

| 数据集原始标签 | 映射到 |
|--------------|--------|
| Wheat Powdery Mildew | 小麦白粉病 |
| Rice Blast | 稻瘟病 |
| Corn Gray Leaf Spot | 玉米大斑病 |
| Aphid | 蚜虫 |
| Spider Mite | 红蜘蛛 |
| Whitefly | 白粉虱 |

### 3. 训练策略
- **迁移学习**: 使用当前MobileNetV3作为预训练模型
- **微调**: 冻结前几层，只训练后几层
- **学习率**: 初始0.001，使用余弦退火
- **批次大小**: 32
- **训练轮数**: 50-100

## 六、数据集引用格式

### PlantVillage
```
@article{mohanty2016using,
  title={Using deep learning for image-based plant disease detection},
  author={Mohanty, Sharada P and Hughes, David P and Salath{\'e}, Marcel},
  journal={arXiv preprint arXiv:1604.03169},
  year={2016}
}
```

### PlantDoc
```
@article{singh2020plantdoc,
  title={PlantDoc: A Dataset for Visual Plant Disease Detection},
  author={Singh, Davinder and Jain, Kanchan and Hazarika, Gaurav},
  journal={arXiv preprint arXiv:1911.09348},
  year={2019}
}
```

### IP102
```
@article{wu2019ip102,
  title={IP102: A Large-Scale Benchmark Dataset for Insect Pest Recognition},
  author={Wu, Xiaoping and Zhan, Cheng and Zhang, Yang and Yang, Ming and Ding, Lei},
  journal={arXiv preprint arXiv:1908.01900},
  year={2019}
}
```

---

**文档创建时间**: 2026-04-17
**数据集总数**: 8个主要数据集
**推荐方案**: PlantVillage + PlantDoc + IP102
**预计图像总数**: 约130,000张
