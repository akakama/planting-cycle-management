"""
准备真实的玉米病害数据集
"""
from pathlib import Path
import shutil
import random

def prepare_corn_data():
    """准备玉米病害数据"""
    print("="*60)
    print("准备真实玉米病害数据集")
    print("="*60)
    
    source_dir = Path("data/datasets/corn_diseases/data")
    
    if not source_dir.exists():
        print("✗ 数据集未找到")
        return False
    
    # 清空旧数据
    print("\n清空旧数据...")
    for split in ['train', 'val', 'test']:
        split_dir = Path(f"data/{split}")
        if split_dir.exists():
            shutil.rmtree(split_dir)
    
    # 类别映射
    class_mapping = {
        "Gray_Leaf_Spot": "玉米大斑病",
        "Common_Rust": "玉米大斑病",  # 锈病也归为大斑病
        "Blight": "玉米大斑病",
    }
    
    # 统计
    total_count = 0
    
    print("\n处理数据...")
    for source_class, target_class in class_mapping.items():
        class_dir = source_dir / source_class
        
        if not class_dir.exists():
            continue
        
        # 获取所有图像
        images = list(class_dir.glob("*.*"))
        print(f"  {source_class}: {len(images)} 张图像 -> {target_class}")
        
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
            target_dir = Path(f"data/{split}/{target_class}")
            target_dir.mkdir(parents=True, exist_ok=True)
            
            for img in split_images:
                target_file = target_dir / f"corn_{total_count}.jpg"
                shutil.copy(img, target_file)
                total_count += 1
        
        print(f"    训练: {len(train_images)}, 验证: {len(val_images)}, 测试: {len(test_images)}")
    
    print("\n" + "="*60)
    print("数据准备完成")
    print("="*60)
    
    # 统计最终数据
    for split in ['train', 'val', 'test']:
        split_dir = Path(f"data/{split}")
        if split_dir.exists():
            count = sum(1 for _ in split_dir.rglob("*.jpg"))
            print(f"{split}: {count} 张图像")
    
    print(f"\n总计: {total_count} 张真实玉米病害图像")
    
    return total_count > 0

if __name__ == "__main__":
    success = prepare_corn_data()
    
    if success:
        print("\n✓ 数据准备成功")
        print("\n下一步:")
        print("  python scripts/train_model.py")
    else:
        print("\n✗ 数据准备失败")
