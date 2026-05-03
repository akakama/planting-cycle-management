"""
下载真实的病虫害数据集
"""
import kagglehub
from pathlib import Path
import shutil

def download_real_pest_data():
    """下载真实的病虫害数据"""
    print("="*60)
    print("下载真实的病虫害数据集")
    print("="*60)
    
    # 真实数据集列表
    datasets = [
        {
            "id": "minhhuy2810/rice-diseases-image-dataset",
            "name": "水稻病害（稻瘟病）",
            "folder": "rice_diseases_real",
            "target_class": "稻瘟病"
        },
        {
            "id": "shayanfazeli/pest-detection",
            "name": "害虫检测（蚜虫等）",
            "folder": "pest_detection_real",
            "target_class": "蚜虫"
        },
        {
            "id": "nirmalsankalana/leaf-pest-detection",
            "name": "叶片害虫检测",
            "folder": "leaf_pest_real",
            "target_class": "红蜘蛛"
        },
        {
            "id": "jay7080dev/plant-pest-detection",
            "name": "植物害虫检测",
            "folder": "plant_pest_real",
            "target_class": "白粉虱"
        }
    ]
    
    success_count = 0
    
    for i, dataset in enumerate(datasets, 1):
        print(f"\n[{i}/{len(datasets)}] 下载: {dataset['name']}")
        print(f"ID: {dataset['id']}")
        print(f"目标类别: {dataset['target_class']}")
        
        try:
            # 下载数据集
            path = kagglehub.dataset_download(dataset['id'])
            print(f"✓ 下载成功: {path}")
            
            # 复制到data目录
            target_dir = Path(f"data/datasets/{dataset['folder']}")
            target_dir.mkdir(parents=True, exist_ok=True)
            
            source_path = Path(path)
            
            # 复制文件
            print("复制文件...")
            for item in source_path.iterdir():
                if item.is_file():
                    shutil.copy(item, target_dir / item.name)
                elif item.is_dir():
                    shutil.copytree(item, target_dir / item.name, dirs_exist_ok=True)
            
            print(f"✓ 数据已保存到: {target_dir}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ 下载失败: {e}")
            print("继续下一个数据集...")
    
    print("\n" + "="*60)
    print(f"下载完成: {success_count}/{len(datasets)} 个数据集")
    print("="*60)
    
    return success_count

if __name__ == "__main__":
    count = download_real_pest_data()
    print(f"\n✓ 成功下载 {count} 个数据集")
    print("\n下一步: python scripts/prepare_all_real_data.py")
