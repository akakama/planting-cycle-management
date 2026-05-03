"""
准备平衡的病虫害数据集
"""
from pathlib import Path
import shutil
import random

def prepare_balanced_data():
    """准备平衡的数据"""
    print("="*60)
    print("准备平衡的病虫害数据集")
    print("="*60)
    
    # 清空旧数据
    print("\n清空旧数据...")
    for split in ['train', 'val', 'test']:
        split_dir = Path(f"data/{split}")
        if split_dir.exists():
            shutil.rmtree(split_dir)
    
    # 目标：每类至少500张图像
    target_per_class = 500
    
    # 类别数据收集
    class_data = {
        "小麦白粉病": [],
        "稻瘟病": [],
        "玉米大斑病": [],
        "蚜虫": [],
        "红蜘蛛": [],
        "白粉虱": []
    }
    
    # 1. 处理玉米病害数据
    print("\n[1/3] 处理玉米病害数据...")
    source_dir = Path("data/datasets/corn_diseases/data")
    if source_dir.exists():
        for class_dir in source_dir.iterdir():
            if not class_dir.is_dir():
                continue
            
            images = list(class_dir.glob("*.*"))
            class_data["玉米大斑病"].extend(images)
        
        print(f"  玉米大斑病: {len(class_data['玉米大斑病'])} 张")
    
    # 2. 处理植物病害识别数据
    print("\n[2/3] 处理植物病害识别数据...")
    source_dir = Path("data/datasets/plant_disease_recognition")
    if source_dir.exists():
        # 查找Powdery类别
        for powdery_dir in source_dir.rglob("Powdery"):
            if powdery_dir.is_dir():
                images = list(powdery_dir.glob("*.*"))
                class_data["小麦白粉病"].extend(images)
        
        print(f"  小麦白粉病: {len(class_data['小麦白粉病'])} 张")
    
    # 3. 处理Plant Village数据
    print("\n[3/3] 处理Plant Village数据...")
    source_dir = Path("data/datasets/plant_village")
    if source_dir.exists():
        # 查找所有类别
        for class_dir in source_dir.rglob("*"):
            if not class_dir.is_dir():
                continue
            
            class_name = class_dir.name.lower()
            images = list(class_dir.glob("*.*"))
            
            if not images:
                continue
            
            # 映射到目标类别
            if "rice" in class_name and "blast" in class_name:
                class_data["稻瘟病"].extend(images)
                print(f"  稻瘟病: {len(images)} 张 (from {class_dir.name})")
            elif "wheat" in class_name and "powdery" in class_name:
                class_data["小麦白粉病"].extend(images)
                print(f"  小麦白粉病: {len(images)} 张 (from {class_dir.name})")
            elif "corn" in class_name or "maize" in class_name:
                class_data["玉米大斑病"].extend(images)
                print(f"  玉米大斑病: {len(images)} 张 (from {class_dir.name})")
    
    # 统计
    print("\n" + "="*60)
    print("数据统计")
    print("="*60)
    
    for class_name, images in class_data.items():
        print(f"{class_name}: {len(images)} 张")
    
    # 平衡数据：每类最多取target_per_class张
    print("\n平衡数据...")
    balanced_data = {}
    
    for class_name, images in class_data.items():
        if len(images) > target_per_class:
            # 随机选择
            selected = random.sample(images, target_per_class)
        else:
            selected = images
        
        balanced_data[class_name] = selected
        print(f"{class_name}: {len(selected)} 张 (平衡后)")
    
    # 划分数据集
    print("\n划分数据集...")
    total_count = 0
    
    for class_name, images in balanced_data.items():
        if not images:
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
        
        # 复制到对应目录
        for split, split_images in [('train', train_images), ('val', val_images), ('test', test_images)]:
            target_dir = Path(f"data/{split}/{class_name}")
            target_dir.mkdir(parents=True, exist_ok=True)
            
            for i, img in enumerate(split_images):
                target_file = target_dir / f"{class_name}_{i}.jpg"
                shutil.copy(img, target_file)
                total_count += 1
        
        print(f"{class_name}: 训练{len(train_images)}, 验证{len(val_images)}, 测试{len(test_images)}")
    
    # 最终统计
    print("\n" + "="*60)
    print("数据准备完成")
    print("="*60)
    
    for split in ['train', 'val', 'test']:
        split_dir = Path(f"data/{split}")
        if split_dir.exists():
            count = sum(1 for _ in split_dir.rglob("*.jpg"))
            print(f"{split}: {count} 张图像")
    
    print(f"\n总计: {total_count} 张图像")
    
    return total_count > 0

if __name__ == "__main__":
    success = prepare_balanced_data()
    
    if success:
        print("\n✓ 数据准备成功")
        print("\n下一步:")
        print("  python scripts/retrain_model.py")
    else:
        print("\n✗ 数据准备失败")
