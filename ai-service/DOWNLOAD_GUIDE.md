# 手动下载真实数据集指南

## 🎯 推荐下载的小规模数据集

由于网络问题，建议手动下载以下较小的数据集：

---

## 数据集1: 玉米病害数据集 (推荐)

**下载地址**: https://www.kaggle.com/smaranjitghose/corn-or-maize-leaf-disease-dataset

**大小**: 约161MB (比13GB小很多)

**包含**: 
- 玉米大斑病 (Gray Leaf Spot)
- 玉米锈病 (Common Rust)
- 玉米北方叶枯病
- 约1,800张图像

**放置位置**: `ai-service/data/datasets/corn_diseases/`

---

## 数据集2: 番茄病害数据集 (可选)

**下载地址**: https://www.kaggle.com/noulman/tomato-leaf-disease-dataset

**大小**: 约50MB

**放置位置**: `ai-service/data/datasets/tomato_diseases/`

---

## 数据集3: 植物病害精选数据集 (可选)

**下载地址**: https://www.kaggle.com/vipoooool/new-plant-diseases-dataset

**大小**: 中等规模

**放置位置**: `ai-service/data/datasets/plant_diseases/`

---

## 📥 下载步骤

1. 点击上面的链接访问Kaggle数据集页面
2. 点击页面右上角的 **Download** 按钮
3. 下载ZIP文件
4. 解压ZIP文件
5. 将解压后的内容放到对应的目录

---

## 📂 目录结构示例

下载玉米病害数据集后：

```
ai-service/
└── data/
    └── datasets/
        └── corn_diseases/
            ├── Gray_Leaf_Spot/
            │   ├── image1.jpg
            │   ├── image2.jpg
            │   └── ...
            ├── Common_Rust/
            ├── Northern_Leaf_Blight/
            └── ...
```

---

## ✅ 下载完成后

运行以下命令准备数据和训练：

```bash
cd ai-service

# 1. 准备数据
python scripts/prepare_real_data.py

# 2. 训练模型
python scripts/train_model.py

# 3. 测试模型
python scripts/test_finetuned_model.py
```

---

## 💡 建议

**优先下载玉米病害数据集**：
- 大小适中 (161MB)
- 包含玉米大斑病
- 图像质量好
- 足够训练使用

这个数据集比13GB的水稻数据集小很多，下载更快！

---

**下载完成后告诉我，我会帮你准备数据并开始训练！**
