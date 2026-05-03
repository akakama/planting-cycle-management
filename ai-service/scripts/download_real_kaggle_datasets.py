"""
从Kaggle下载真实的病虫害数据集
"""
import subprocess
import sys
from pathlib import Path
import json

def check_kaggle_config():
    """检查Kaggle配置"""
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    
    if not kaggle_json.exists():
        print("✗ Kaggle配置文件不存在")
        return False
    
    try:
        with open(kaggle_json, 'r') as f:
            config = json.load(f)
        
        username = config.get('username', '')
        key = config.get('key', '')
        
        # 检查是否是示例配置
        if username == 'demo_user' or key == 'demo_key_for_testing_only':
            print("✗ 当前是示例配置，需要真实的API密钥")
            print("\n请按照以下步骤配置:")
            print("1. 访问 https://www.kaggle.com/account")
            print("2. 点击 'Create New API Token'")
            print(f"3. 将下载的kaggle.json放到: {Path.home() / '.kaggle'}")
            print("4. 重新运行此脚本")
            return False
        
        print(f"✓ Kaggle配置正确 (用户: {username})")
        return True
        
    except Exception as e:
        print(f"✗ 配置文件读取失败: {e}")
        return False

def download_dataset(dataset_name, target_folder, description):
    """下载单个数据集"""
    print(f"\n下载: {description}")
    print(f"数据集: {dataset_name}")
    
    target_dir = Path(f"data/datasets/{target_folder}")
    target_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        result = subprocess.run([
            "kaggle", "datasets", "download",
            "-d", dataset_name,
            "-p", str(target_dir),
            "--unzip"
        ], check=True, capture_output=True, text=True, timeout=600)
        
        print(f"✓ {description} 下载成功")
        return True
    except subprocess.TimeoutExpired:
        print(f"✗ 下载超时")
        return False
    except subprocess.CalledProcessError as e:
        print(f"✗ 下载失败: {e}")
        if e.stderr:
            print(f"  错误信息: {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ 错误: {e}")
        return False

def download_real_datasets():
    """下载真实的病虫害数据集"""
    print("="*60)
    print("下载真实Kaggle病虫害数据集")
    print("="*60)
    
    # 检查配置
    if not check_kaggle_config():
        return False
    
    # 真实数据集列表
    datasets = [
        {
            "name": "minhhuy2810/rice-diseases-image-dataset",
            "folder": "rice_diseases",
            "description": "水稻病害数据集 (1,200张图像，含稻瘟病)"
        },
        {
            "name": "smaranjitghose/corn-or-maize-leaf-disease-dataset",
            "folder": "corn_diseases",
            "description": "玉米病害数据集 (1,800张图像，含玉米大斑病)"
        },
        {
            "name": "abdallahalidev/plantvillage-dataset",
            "folder": "plantvillage",
            "description": "PlantVillage数据集 (54,305张图像，38类)"
        },
    ]
    
    success_count = 0
    
    for dataset in datasets:
        if download_dataset(dataset['name'], dataset['folder'], dataset['description']):
            success_count += 1
    
    print("\n" + "="*60)
    print(f"下载完成: {success_count}/{len(datasets)} 个数据集")
    print("="*60)
    
    return success_count > 0

if __name__ == "__main__":
    success = download_real_datasets()
    
    if success:
        print("\n✓ 真实数据集下载成功")
        print("\n下一步:")
        print("  python scripts/prepare_real_data.py  # 准备数据")
        print("  python scripts/train_model.py        # 训练模型")
    else:
        print("\n✗ 数据集下载失败")
        print("请确保:")
        print("1. 已正确配置Kaggle API密钥")
        print("2. 网络连接正常")
        sys.exit(1)
