"""
准备多样化的真实病虫害数据
"""
from pathlib import Path
import shutil
import random

def prepare_diverse_data():
    """准备多样化数据"""
    print("="*60)
    print("准备多样化的真实病虫害数据")
    print("="*60)
    
    # 清空旧数据
    print("\n清空旧数据...")
    for split in ['train', 'val', 'test']:
        split_dir = Path(f"data/{split}")
        if split_dir.exists():
            shutil.rmtree(split_dir)
    
    total_count = 0
    
    # 1. 处理玉米病害数据
    print("\n[1/3] 处理玉米病害数据...")
    count = process_corn_diseases()
    total_count += count
    print(f"  ✓ 玉米病害: {count} 张")
    
    # 2. 处理植物病害识别数据
    print("\n[2/3] 处理植物病害识别数据...")
    count = process_plant_disease_recognition()
    total_count += count
    print(f"  ✓ 植物病害识别: {count} 张")
    
    # 3. 处理Plant Village数据
    print("\n[3/3] 处理Plant Village数据...")
    count = process_plant_village()
    total_count += count
    print(f"  ✓ Plant Village: {count} 张")
    
    # 统计
    print("\n" + "="*60)
    print("数据准备完成")
    print("="*60)
    
    for split in ['train', 'val', 'test']:
        split_dir = Path(f"data/{split}")
        if split_dir.exists():
            count = sum(1 for _ in split_dir.rglob("*.jpg"))
            print(f"{split}: {count} 张图像")
    
    print(f"\n总计: {total_count} 张真实病虫害图像")
    
    return total_count > 0

def process_corn_diseases():
    """处理玉米病害数据"""
    source_dir = Path("data/datasets/corn_diseases/data")
    if not source_dir.exists():
        return 0
    
    class_mapping = {
        "Gray_Leaf_Spot": "玉米大斑病",
        "Common_Rust": "玉米大斑病",
        "Blight": "玉米大斑病",
    }
    
    return process_dataset(source_dir, class_mapping, "corn")

def process_plant_disease_recognition():
    """处理植物病害识别数据"""
    source_dir = Path("data/datasets/plant_disease_recognition")
    if not source_dir.exists():
        return 0
    
    # 查找实际的数据目录
    for possible_dir in ["Plant_Diseases_Dataset", "data", ""]:
        test_dir = source_dir / possible_dir if possible_dir else source_dir
        if test_dir.exists():
            source_dir = test_dir
            break
    
    # 自动发现类别
    class_mapping = {}
    for class_dir in source_dir.rglob("*"):
        if class_dir.is_dir():
            class_name = class_dir.name.lower()
            
            # 映射规则
            if "blast" in class_name or "rice" in class_name:
                class_mapping[class_dir.name] = "稻瘟病"
            elif "powdery" in class_name or "wheat" in class_name:
                class_mapping[class_dir.name] = "小麦白粉病"
            elif "spot" in class_name or "blight" in class_name or "corn" in class_name:
                class_mapping[class_dir.name] = "玉米大斑病"
            elif "aphid" in class_name:
                class_mapping[class_dir.name] = "蚜虫"
            elif "mite" in class_name or "spider" in class_name:
                class_mapping[class_dir.name] = "红蜘蛛"
            elif "whitefly" in class_name:
                class_mapping[class_dir.name] = "白粉虱"
    
    return process_dataset(source_dir, class_mapping, "pdr")

def process_plant_village():
    """处理Plant Village数据"""
    source_dir = Path("data/datasets/plant_village")
    if not source_dir.exists():
        return 0
    
    # 查找实际的数据目录
    for possible_dir in ["PlantVillage", "data", "" ]:
        test_dir = source_dir / possible_dir if possible_dir else source_dir
        if test_dir.exists():
            source_dir = test_dir
            break
    
    # 类别映射
    class_mapping = {}
    for class_dir in source_dir.rglob("*"):
        if class_dir.is_dir():
            class_name = class_dir.name
            
            # 映射规则
            if "Rice" in class_name and "Blast" in class_name:
                class_mapping[class_name] = "稻瘟病"
            elif "Wheat" in class_name and "Powdery" in class_name:
                class_mapping[class_name] = "小麦白粉病"
            elif "Corn" in class_name or "Maize" in class_name:
                class_mapping[class_name] = "玉米大斑病"
    
    return process_dataset(source_dir, class_mapping, "pv")

def process_dataset(source_dir, class_mapping, prefix):
    """处理数据集的通用函数"""
    total_count = 0
    
    for source_class, target_class in class_mapping.items():
        # 查找所有匹配的目录
        for class_dir in source_dir.rglob(source_class):
            if not class_dir.is_dir():
                continue
            
            # 获取所有图像
            images = list(class_dir.glob("*.*"))
            if not images:
                continue
            
            print(f"    {source_class} -> {target_class}: {len(images)} 张")
            
            # 随机打乱
            random.shuffle(images)
            
            # 划分
            n_total = len(images)
            n_train = int(n_total * 0.7)
            n_val = int(n_total * 0.15)
            
            train_images = images[:n_train]
            val_images = images[n_train:n_train+n_val]
            test_images = images[n_train+n_val:]
            
            # 复制
            for split, split_images in [('train', train_images), ('val', val_images), ('test', test_images)]:
                target_dir = Path(f"data/{split}/{target_class}")
                target_dir.mkdir(parents=True, exist_ok=True)
                
                for img in split_images:
                    target_file = target_dir / f"{prefix}_{total_count}.jpg"
                    shutil.copy(img, target_file)
                    total_count += 1
    
    return total_count

if __name__ == "__main__":
    success = prepare_diverse_data()
    
    if success:
        print("\n✓ 数据准备成功")
        print("\n下一步:")
        print("  python scripts/train_model.py")
