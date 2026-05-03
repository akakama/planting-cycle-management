"""
数据集准备和标注脚本
将下载的数据集整理为统一格式，并映射到目标病虫害类别
"""
import os
import sys
from pathlib import Path
import shutil
import json
from PIL import Image
from typing import Dict, List, Tuple
import random

class DatasetPreparer:
    """数据集准备器"""

    def __init__(self, raw_dir="data/datasets", processed_dir="data/processed"):
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        # 目标病虫害类别
        self.target_classes = {
            0: "小麦白粉病",
            1: "稻瘟病",
            2: "玉米大斑病",
            3: "蚜虫",
            4: "红蜘蛛",
            5: "白粉虱"
        }

        # 创建输出目录
        for class_name in self.target_classes.values():
            (self.processed_dir / class_name).mkdir(parents=True, exist_ok=True)

        # 标签映射规则
        self.label_mapping = {
            # PlantVillage映射
            "Corn_(maize)_Gray_leaf_spot": 2,  # 玉米大斑病
            "Corn_(maize)_Common_rust_": 2,    # 玉米锈病 -> 玉米大斑病
            "Corn_(maize)_Northern_Leaf_Blight": 2,  # 玉米北方叶枯病

            # Rice Diseases映射
            "Blast": 1,  # 稻瘟病
            "rice_blast": 1,
            "blast": 1,

            # Wheat Disease映射
            "wheat_powdery_mildew": 0,  # 小麦白粉病
            "powdery_mildew": 0,
            "Wheat_Powdery_Mildew": 0,

            # Corn Disease映射
            "Gray_Leaf_Spot": 2,  # 玉米大斑病
            "Common_Rust": 2,
            "Northern_Leaf_Blight": 2,

            # PlantDoc映射
            "Wheat___Leaf_Rust": 0,  # 小麦锈病 -> 小麦白粉病
            "Wheat___Powdery_Mildew": 0,
            "Rice___Blast": 1,
            "Corn___Gray_Leaf_Spot": 2,
            "Corn___Common_Rust": 2,

            # 害虫映射
            "Aphid": 3,
            "aphid": 3,
            "Spider_Mite": 4,
            "spider_mite": 4,
            "Whitefly": 5,
            "whitefly": 5,
        }

        self.stats = {class_name: 0 for class_name in self.target_classes.values()}

    def validate_image(self, image_path: Path) -> bool:
        """验证图像是否有效"""
        try:
            img = Image.open(image_path)
            img.verify()
            return True
        except:
            return False

    def process_plantvillage(self):
        """处理PlantVillage数据集"""
        print("\n处理 PlantVillage 数据集...")
        plantvillage_dir = self.raw_dir / "plantvillage"

        if not plantvillage_dir.exists():
            print("⚠️  PlantVillage数据集未找到，跳过")
            return

        # PlantVillage数据集结构: raw/color/
        color_dir = plantvillage_dir / "raw" / "color"
        if not color_dir.exists():
            color_dir = plantvillage_dir

        count = 0
        for class_dir in color_dir.iterdir():
            if not class_dir.is_dir():
                continue

            class_name = class_dir.name

            # 查找映射
            target_class_id = None
            for key, value in self.label_mapping.items():
                if key in class_name:
                    target_class_id = value
                    break

            if target_class_id is None:
                continue

            target_class_name = self.target_classes[target_class_id]

            # 复制图像
            for img_file in class_dir.glob("*.JPG"):
                if self.validate_image(img_file):
                    dest = self.processed_dir / target_class_name / f"plantvillage_{count}.JPG"
                    shutil.copy(img_file, dest)
                    self.stats[target_class_name] += 1
                    count += 1

        print(f"✓ PlantVillage处理完成，提取 {count} 张图像")

    def process_rice_diseases(self):
        """处理水稻病害数据集"""
        print("\n处理 Rice Diseases 数据集...")
        rice_dir = self.raw_dir / "rice_diseases"

        if not rice_dir.exists():
            print("⚠️  Rice Diseases数据集未找到，跳过")
            return

        count = 0
        for class_dir in rice_dir.iterdir():
            if not class_dir.is_dir():
                continue

            class_name = class_dir.name

            # 查找映射
            target_class_id = None
            for key, value in self.label_mapping.items():
                if key.lower() in class_name.lower():
                    target_class_id = value
                    break

            if target_class_id is None:
                continue

            target_class_name = self.target_classes[target_class_id]

            # 复制图像
            for img_file in class_dir.glob("*.*"):
                if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    if self.validate_image(img_file):
                        dest = self.processed_dir / target_class_name / f"rice_{count}{img_file.suffix}"
                        shutil.copy(img_file, dest)
                        self.stats[target_class_name] += 1
                        count += 1

        print(f"✓ Rice Diseases处理完成，提取 {count} 张图像")

    def process_wheat_diseases(self):
        """处理小麦病害数据集"""
        print("\n处理 Wheat Disease 数据集...")
        wheat_dir = self.raw_dir / "wheat_diseases"

        if not wheat_dir.exists():
            print("⚠️  Wheat Disease数据集未找到，跳过")
            return

        count = 0
        for class_dir in wheat_dir.iterdir():
            if not class_dir.is_dir():
                continue

            class_name = class_dir.name

            # 查找映射
            target_class_id = None
            for key, value in self.label_mapping.items():
                if key.lower() in class_name.lower():
                    target_class_id = value
                    break

            if target_class_id is None:
                continue

            target_class_name = self.target_classes[target_class_id]

            # 复制图像
            for img_file in class_dir.glob("*.*"):
                if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    if self.validate_image(img_file):
                        dest = self.processed_dir / target_class_name / f"wheat_{count}{img_file.suffix}"
                        shutil.copy(img_file, dest)
                        self.stats[target_class_name] += 1
                        count += 1

        print(f"✓ Wheat Disease处理完成，提取 {count} 张图像")

    def process_corn_diseases(self):
        """处理玉米病害数据集"""
        print("\n处理 Corn Disease 数据集...")
        corn_dir = self.raw_dir / "corn_diseases"

        if not corn_dir.exists():
            print("⚠️  Corn Disease数据集未找到，跳过")
            return

        count = 0
        for class_dir in corn_dir.iterdir():
            if not class_dir.is_dir():
                continue

            class_name = class_dir.name

            # 查找映射
            target_class_id = None
            for key, value in self.label_mapping.items():
                if key.lower() in class_name.lower():
                    target_class_id = value
                    break

            if target_class_id is None:
                continue

            target_class_name = self.target_classes[target_class_id]

            # 复制图像
            for img_file in class_dir.glob("*.*"):
                if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    if self.validate_image(img_file):
                        dest = self.processed_dir / target_class_name / f"corn_{count}{img_file.suffix}"
                        shutil.copy(img_file, dest)
                        self.stats[target_class_name] += 1
                        count += 1

        print(f"✓ Corn Disease处理完成，提取 {count} 张图像")

    def process_plantdoc(self):
        """处理PlantDoc数据集"""
        print("\n处理 PlantDoc 数据集...")
        plantdoc_dir = self.raw_dir / "plantdoc"

        if not plantdoc_dir.exists():
            print("⚠️  PlantDoc数据集未找到，跳过")
            return

        count = 0
        for class_dir in plantdoc_dir.iterdir():
            if not class_dir.is_dir():
                continue

            class_name = class_dir.name

            # 查找映射
            target_class_id = None
            for key, value in self.label_mapping.items():
                if key in class_name:
                    target_class_id = value
                    break

            if target_class_id is None:
                continue

            target_class_name = self.target_classes[target_class_id]

            # 复制图像
            for img_file in class_dir.glob("*.*"):
                if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    if self.validate_image(img_file):
                        dest = self.processed_dir / target_class_name / f"plantdoc_{count}{img_file.suffix}"
                        shutil.copy(img_file, dest)
                        self.stats[target_class_name] += 1
                        count += 1

        print(f"✓ PlantDoc处理完成，提取 {count} 张图像")

    def split_dataset(self, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
        """划分数据集为训练集、验证集、测试集"""
        print("\n划分数据集...")

        splits = {
            "train": Path("data/train"),
            "val": Path("data/val"),
            "test": Path("data/test")
        }

        # 创建目录
        for split_path in splits.values():
            for class_name in self.target_classes.values():
                (split_path / class_name).mkdir(parents=True, exist_ok=True)

        # 划分每个类别的图像
        for class_id, class_name in self.target_classes.items():
            class_dir = self.processed_dir / class_name
            images = list(class_dir.glob("*.*"))

            if not images:
                continue

            # 随机打乱
            random.shuffle(images)

            # 计算划分点
            n_total = len(images)
            n_train = int(n_total * train_ratio)
            n_val = int(n_total * val_ratio)

            # 划分
            train_images = images[:n_train]
            val_images = images[n_train:n_train+n_val]
            test_images = images[n_train+n_val:]

            # 复制到对应目录
            for img in train_images:
                shutil.copy(img, splits["train"] / class_name / img.name)

            for img in val_images:
                shutil.copy(img, splits["val"] / class_name / img.name)

            for img in test_images:
                shutil.copy(img, splits["test"] / class_name / img.name)

            print(f"  {class_name}: 训练{len(train_images)} 验证{len(val_images)} 测试{len(test_images)}")

    def save_statistics(self):
        """保存统计信息"""
        print("\n数据集统计:")
        print("="*60)

        total = 0
        for class_name, count in self.stats.items():
            print(f"{class_name}: {count} 张")
            total += count

        print("="*60)
        print(f"总计: {total} 张图像")

        # 保存到JSON
        stats_file = self.processed_dir / "statistics.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump({
                "per_class": self.stats,
                "total": total
            }, f, indent=2, ensure_ascii=False)

        print(f"\n✓ 统计信息已保存到: {stats_file}")

    def prepare_all(self):
        """准备所有数据集"""
        print("="*60)
        print("开始准备数据集")
        print("="*60)

        # 处理各个数据集
        self.process_plantvillage()
        self.process_rice_diseases()
        self.process_wheat_diseases()
        self.process_corn_diseases()
        self.process_plantdoc()

        # 保存统计信息
        self.save_statistics()

        # 划分数据集
        self.split_dataset()

        print("\n" + "="*60)
        print("数据集准备完成")
        print("="*60)


def main():
    """主函数"""
    preparer = DatasetPreparer()
    preparer.prepare_all()


if __name__ == "__main__":
    main()
