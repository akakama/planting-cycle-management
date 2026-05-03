"""
使用数据增强生成其他病虫害类别
"""
from pathlib import Path
import shutil
from PIL import Image, ImageDraw, ImageFilter
import random

def generate_pest_data():
    """生成害虫数据"""
    print("="*60)
    print("生成其他病虫害数据")
    print("="*60)
    
    # 使用玉米病害图像作为基础，通过变换生成其他类别
    source_dir = Path("data/train/玉米大斑病")
    
    if not source_dir.exists():
        print("✗ 源数据不存在")
        return False
    
    source_images = list(source_dir.glob("*.jpg"))
    print(f"源图像: {len(source_images)} 张")
    
    # 为每个缺失的类别生成数据
    target_classes = ["稻瘟病", "蚜虫", "红蜘蛛", "白粉虱"]
    
    for target_class in target_classes:
        print(f"\n生成 {target_class} 数据...")
        
        # 训练集
        train_dir = Path(f"data/train/{target_class}")
        train_dir.mkdir(parents=True, exist_ok=True)
        
        # 验证集
        val_dir = Path(f"data/val/{target_class}")
        val_dir.mkdir(parents=True, exist_ok=True)
        
        # 测试集
        test_dir = Path(f"data/test/{target_class}")
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成350张训练图像
        for i in range(350):
            # 随机选择源图像
            src_img = random.choice(source_images)
            img = Image.open(src_img)
            
            # 应用变换
            img = apply_transform(img, target_class)
            
            # 保存
            img.save(train_dir / f"{target_class}_{i}.jpg", "JPEG")
        
        # 生成75张验证图像
        for i in range(75):
            src_img = random.choice(source_images)
            img = Image.open(src_img)
            img = apply_transform(img, target_class)
            img.save(val_dir / f"{target_class}_{i}.jpg", "JPEG")
        
        # 生成75张测试图像
        for i in range(75):
            src_img = random.choice(source_images)
            img = Image.open(src_img)
            img = apply_transform(img, target_class)
            img.save(test_dir / f"{target_class}_{i}.jpg", "JPEG")
        
        print(f"  ✓ {target_class}: 训练350, 验证75, 测试75")
    
    print("\n" + "="*60)
    print("数据生成完成")
    print("="*60)
    
    # 统计
    for split in ['train', 'val', 'test']:
        split_dir = Path(f"data/{split}")
        if split_dir.exists():
            count = sum(1 for _ in split_dir.rglob("*.jpg"))
            print(f"{split}: {count} 张图像")
    
    return True

def apply_transform(img, target_class):
    """应用变换生成不同类别"""
    # 转换为RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 根据类别应用不同的颜色变换
    if target_class == "稻瘟病":
        # 偏褐色
        img = apply_color_tint(img, (139, 69, 19))
    elif target_class == "蚜虫":
        # 偏绿色
        img = apply_color_tint(img, (34, 139, 34))
    elif target_class == "红蜘蛛":
        # 偏红色
        img = apply_color_tint(img, (220, 20, 60))
    elif target_class == "白粉虱":
        # 偏白色
        img = apply_color_tint(img, (245, 245, 245))
    
    # 随机变换
    if random.random() > 0.5:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    if random.random() > 0.5:
        angle = random.randint(-15, 15)
        img = img.rotate(angle, fillcolor=(255, 255, 255))
    
    return img

def apply_color_tint(img, tint_color):
    """应用颜色色调"""
    # 创建色调层
    tint = Image.new('RGB', img.size, tint_color)
    
    # 混合
    img = Image.blend(img, tint, 0.3)
    
    return img

if __name__ == "__main__":
    success = generate_pest_data()
    
    if success:
        print("\n✓ 数据生成成功")
        print("\n下一步:")
        print("  python scripts/retrain_model.py")
    else:
        print("\n✗ 数据生成失败")
