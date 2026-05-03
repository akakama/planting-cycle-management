"""
下载更多可用的病虫害数据集
"""
import kagglehub
from pathlib import Path
import shutil

def download_more_datasets():
    """下载更多数据集"""
    print("="*60)
    print("下载更多病虫害数据集")
    print("="*60)
    
    # 更多数据集
    datasets = [
        {
            "id": "arjuntejaswi/plant-village",
            "name": "Plant Village精选",
            "folder": "plant_village"
        },
        {
            "id": "vipoooool/new-plant-diseases-dataset",
            "name": "新植物病害数据集",
            "folder": "new_plant_diseases"
        },
        {
            "id": "abdallahalidev/plantvillage-dataset",
            "name": "PlantVillage数据集",
            "folder": "plantvillage"
        },
        {
            "id": "sadmansakibmahi/plant-disease-classification-ai-model",
            "name": "植物病害分类",
            "folder": "plant_classification"
        }
    ]
    
    success_count = 0
    
    for i, dataset in enumerate(datasets, 1):
        print(f"\n[{i}/{len(datasets)}] 下载: {dataset['name']}")
        print(f"ID: {dataset['id']}")
        
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
    count = download_more_datasets()
    print(f"\n✓ 成功下载 {count} 个数据集")
