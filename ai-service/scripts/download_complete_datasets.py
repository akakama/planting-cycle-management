"""
下载包含所有6类病虫害的多样化数据集
"""
import kagglehub
from pathlib import Path
import shutil

def download_complete_datasets():
    """下载完整的数据集"""
    print("="*60)
    print("下载包含所有6类病虫害的数据集")
    print("="*60)
    
    # 完整数据集列表
    datasets = [
        {
            "id": "smaranjitghose/corn-or-maize-leaf-disease-dataset",
            "name": "玉米病害",
            "folder": "corn_diseases",
            "classes": ["玉米大斑病"]
        },
        {
            "id": "rashikrahmanpritom/plant-disease-recognition-dataset",
            "name": "植物病害识别",
            "folder": "plant_disease_recognition",
            "classes": ["小麦白粉病"]
        },
        {
            "id": "shayanfazeli/pest-detection",
            "name": "害虫检测",
            "folder": "pest_detection",
            "classes": ["蚜虫", "红蜘蛛", "白粉虱"]
        },
        {
            "id": "noulman/tomato-leaf-disease-dataset",
            "name": "番茄病害",
            "folder": "tomato_diseases",
            "classes": ["多种病害"]
        },
        {
            "id": "muhammadardiputra/project-on-rice-plant-diseases-detection",
            "name": "水稻病害",
            "folder": "rice_diseases",
            "classes": ["稻瘟病"]
        }
    ]
    
    success_count = 0
    
    for i, dataset in enumerate(datasets, 1):
        print(f"\n[{i}/{len(datasets)}] 下载: {dataset['name']}")
        print(f"ID: {dataset['id']}")
        print(f"包含: {', '.join(dataset['classes'])}")
        
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
    count = download_complete_datasets()
    print(f"\n✓ 成功下载 {count} 个数据集")
    print("\n下一步: python scripts/prepare_balanced_data.py")
