"""
使用kagglehub下载真实病虫害数据集
"""
import kagglehub
from pathlib import Path
import shutil
import sys

def download_with_kagglehub():
    """使用kagglehub下载数据集"""
    print("="*60)
    print("使用kagglehub下载真实病虫害数据集")
    print("="*60)
    
    # 数据集列表
    datasets = [
        {
            "id": "smaranjitghose/corn-or-maize-leaf-disease-dataset",
            "name": "玉米病害数据集",
            "folder": "corn_diseases"
        },
        {
            "id": "minhhuy2810/rice-diseases-image-dataset", 
            "name": "水稻病害数据集",
            "folder": "rice_diseases"
        }
    ]
    
    success_count = 0
    
    for dataset in datasets:
        print(f"\n下载: {dataset['name']}")
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
            print("复制文件到项目目录...")
            for item in source_path.iterdir():
                if item.is_file():
                    shutil.copy(item, target_dir / item.name)
                elif item.is_dir():
                    shutil.copytree(item, target_dir / item.name, dirs_exist_ok=True)
            
            print(f"✓ 数据已保存到: {target_dir}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ 下载失败: {e}")
    
    print("\n" + "="*60)
    print(f"下载完成: {success_count}/{len(datasets)} 个数据集")
    print("="*60)
    
    return success_count > 0

if __name__ == "__main__":
    success = download_with_kagglehub()
    
    if success:
        print("\n✓ 数据集下载成功")
        print("\n下一步:")
        print("  python scripts/prepare_real_data.py  # 准备数据")
        print("  python scripts/train_model.py        # 训练模型")
    else:
        print("\n✗ 下载失败")
        sys.exit(1)
