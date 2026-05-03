"""
准备真实的Kaggle病虫害数据集
将下载的数据整理为统一格式用于训练
"""
import os
from pathlib import Path
from PIL import Image
import shutil

def prepare_rice_diseases():
    """准备水稻病害数据集"""
    print("\n处理水稻病害数据集...")
    
    source_dir = Path("data/datasets/rice_diseases")
    if not source_dir.exists():
        print("  ⚠️  未找到水稻病害数据集，跳过")
        return 0
    
    count = 0
    
    # 查找所有图像文件
    for img_file in source_dir.rglob("*.*"):
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            # 根据文件夹名称判断类别
            parent_name = img_file.parent.name.lower()
            
            # 映射到目标类别
            if 'blast' in parent_name:
                target_class = "稻瘟病"
            else:
                continue  # 跳过其他类别
            
            # 复制到训练目录
            target_dir = Path(f"data/train/{target_class}")
            target_dir.mkdir(parents=True, exist_ok=True)
            
            target_file = target_dir / f"rice_{count}.jpg"
            shutil.copy(img_file, target_file)
            count += 1
    
    print(f"  ✓ 水稻病害: {count} 张图像")
    return count

def prepare_corn_diseases():
    """准备玉米病害数据集"""
    print("\n处理玉米病害数据集...")
    
    source_dir = Path("data/datasets/corn_diseases")
    if not source_dir.exists():
        print("  ⚠️  未找到玉米病害数据集，跳过")
        return 0
    
    count = 0
    
    # 查找所有图像文件
    for img_file in source_dir.rglob("*.*"):
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            parent_name = img_file.parent.name.lower()
            
            # 映射到目标类别
            if 'gray' in parent_name or 'spot' in parent_name:
                target_class = "玉米大斑病"
            else:
                continue
            
            target_dir = Path(f"data/train/{target_class}")
            target_dir.mkdir(parents=True, exist_ok=True)
            
            target_file = target_dir / f"corn_{count}.jpg"
            shutil.copy(img_file, target_file)
            count += 1
    
    print(f"  ✓ 玉米病害: {count} 张图像")
    return count

def prepare_plantvillage():
    """准备PlantVillage数据集"""
    print("\n处理PlantVillage数据集...")
    
    source_dir = Path("data/datasets/plantvillage")
    if not source_dir.exists():
        print("  ⚠️  未找到PlantVillage数据集，跳过")
        return 0
    
    count = 0
    
    # PlantVillage的类别映射
    mapping = {
        "Corn_(maize)_Gray_leaf_spot": "玉米大斑病",
        "Corn_(maize)_Common_rust_": "玉米大斑病",
        "Corn_(maize)_Northern_Leaf_Blight": "玉米大斑病",
    }
    
    # 查找所有类别文件夹
    for class_dir in source_dir.rglob("*"):
        if not class_dir.is_dir():
            continue
        
        class_name = class_dir.name
        
        # 查找映射
        target_class = None
        for key, value in mapping.items():
            if key in class_name:
                target_class = value
                break
        
        if not target_class:
            continue
        
        # 复制图像
        for img_file in class_dir.glob("*.*"):
            if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                target_dir = Path(f"data/train/{target_class}")
                target_dir.mkdir(parents=True, exist_ok=True)
                
                target_file = target_dir / f"plantvillage_{count}.jpg"
                shutil.copy(img_file, target_file)
                count += 1
    
    print(f"  ✓ PlantVillage: {count} 张图像")
    return count

def split_dataset():
    """划分数据集为训练、验证、测试集"""
    print("\n划分数据集...")
    
    import random
    
    class_names = ["小麦白粉病", "稻瘟病", "玉米大斑病", "蚜虫", "红蜘蛛", "白粉虱"]
    
    for class_name in class_names:
        train_dir = Path(f"data/train/{class_name}")
        
        if not train_dir.exists():
            continue
        
        # 获取所有图像
        images = list(train_dir.glob("*.jpg"))
        
        if len(images) < 10:
            print(f"  ⚠️  {class_name}: 图像太少 ({len(images)})，跳过")
            continue
        
        # 随机打乱
        random.shuffle(images)
        
        # 划分: 70% 训练, 15% 验证, 15% 测试
        n_total = len(images)
        n_train = int(n_total * 0.7)
        n_val = int(n_total * 0.15)
        
        train_images = images[:n_train]
        val_images = images[n_train:n_train+n_val]
        test_images = images[n_train+n_val:]
        
        # 创建目录
        val_dir = Path(f"data/val/{class_name}")
        test_dir = Path(f"data/test/{class_name}")
        val_dir.mkdir(parents=True, exist_ok=True)
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # 移动文件
        for img in val_images:
            shutil.move(str(img), val_dir / img.name)
        
        for img in test_images:
            shutil.move(str(img), test_dir / img.name)
        
        print(f"  ✓ {class_name}: 训练{len(train_images)} 验证{len(val_images)} 测试{len(test_images)}")

def main():
    """主函数"""
    print("="*60)
    print("准备真实病虫害数据集")
    print("="*60)
    
    # 清空旧数据
    print("\n清空旧数据...")
    for split in ['train', 'val', 'test']:
        split_dir = Path(f"data/{split}")
        if split_dir.exists():
            shutil.rmtree(split_dir)
    
    # 处理各个数据集
    total = 0
    total += prepare_rice_diseases()
    total += prepare_corn_diseases()
    total += prepare_plantvillage()
    
    if total == 0:
        print("\n✗ 未找到任何数据集")
        print("请确保已下载数据集到 data/datasets/ 目录")
        return False
    
    # 划分数据集
    split_dataset()
    
    # 统计
    print("\n" + "="*60)
    print("数据准备完成")
    print("="*60)
    
    for split in ['train', 'val', 'test']:
        split_dir = Path(f"data/{split}")
        if split_dir.exists():
            count = sum(1 for _ in split_dir.rglob("*.jpg"))
            print(f"{split}: {count} 张图像")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✓ 可以开始训练了:")
        print("  python scripts/train_model.py")
