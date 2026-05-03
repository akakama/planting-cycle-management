"""
使用Kaggle API下载真实病虫害数据集（小规模版本）
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
        print("请先配置Kaggle API:")
        print("1. 访问 https://www.kaggle.com/account")
        print("2. 点击 'Create New API Token'")
        print(f"3. 将kaggle.json放到: {Path.home() / '.kaggle'}")
        return False
    
    try:
        with open(kaggle_json, 'r') as f:
            config = json.load(f)
        
        username = config.get('username', '')
        key = config.get('key', '')
        
        if username == 'demo_user' or key == 'demo_key_for_testing_only':
            print("✗ 需要真实的Kaggle API密钥")
            return False
        
        print(f"✓ Kaggle配置正确 (用户: {username})")
        return True
        
    except Exception as e:
        print(f"✗ 配置文件读取失败: {e}")
        return False

def download_small_datasets():
    """下载小规模的真实数据集"""
    print("="*60)
    print("下载小规模真实病虫害数据集")
    print("="*60)
    
    if not check_kaggle_config():
        return False
    
    # 小规模数据集列表
    datasets = [
        {
            "name": "smaranjitghose/corn-or-maize-leaf-disease-dataset",
            "folder": "corn_diseases",
            "description": "玉米病害数据集 (~100MB, 1,800张)",
            "size": "~100MB"
        },
        {
            "name": "noulman/tomato-leaf-disease-dataset",
            "folder": "tomato_diseases",
            "description": "番茄病害数据集 (~50MB)",
            "size": "~50MB"
        },
        {
            "name": "vipoooool/new-plant-diseases-dataset",
            "folder": "plant_diseases",
            "description": "植物病害数据集 (精选版)",
            "size": "中等"
        },
    ]
    
    print("\n可用的小规模数据集:")
    for i, ds in enumerate(datasets, 1):
        print(f"{i}. {ds['description']} - {ds['size']}")
    
    print("\n开始下载...")
    
    success_count = 0
    
    for dataset in datasets:
        print(f"\n下载: {dataset['description']}")
        print(f"数据集: {dataset['name']}")
        
        target_dir = Path(f"data/datasets/{dataset['folder']}")
        target_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            result = subprocess.run([
                "kaggle", "datasets", "download",
                "-d", dataset['name'],
                "-p", str(target_dir),
                "--unzip"
            ], check=True, capture_output=True, text=True, timeout=600)
            
            print(f"✓ 下载成功")
            success_count += 1
        except subprocess.TimeoutExpired:
            print(f"✗ 下载超时")
        except subprocess.CalledProcessError as e:
            print(f"✗ 下载失败: {e}")
        except Exception as e:
            print(f"✗ 错误: {e}")
    
    print("\n" + "="*60)
    print(f"下载完成: {success_count}/{len(datasets)} 个数据集")
    print("="*60)
    
    return success_count > 0

def download_with_kagglehub():
    """使用kagglehub下载（新方法）"""
    print("\n使用kagglehub下载...")
    
    try:
        import kagglehub
    except ImportError:
        print("安装kagglehub...")
        subprocess.run([sys.executable, "-m", "pip", "install", "kagglehub", "-q"])
        import kagglehub
    
    # 下载玉米病害数据集（较小）
    print("\n下载玉米病害数据集...")
    try:
        path = kagglehub.dataset_download("smaranjitghose/corn-or-maize-leaf-disease-dataset")
        print(f"✓ 下载成功: {path}")
        
        # 复制到data目录
        target_dir = Path("data/datasets/corn_diseases")
        target_dir.mkdir(parents=True, exist_ok=True)
        
        import shutil
        source_path = Path(path)
        for item in source_path.iterdir():
            if item.is_file():
                shutil.copy(item, target_dir / item.name)
            elif item.is_dir():
                shutil.copytree(item, target_dir / item.name, dirs_exist_ok=True)
        
        print(f"✓ 数据已复制到: {target_dir}")
        return True
        
    except Exception as e:
        print(f"✗ 下载失败: {e}")
        return False

if __name__ == "__main__":
    print("选择下载方式:")
    print("1. 使用Kaggle CLI下载小规模数据集")
    print("2. 使用kagglehub下载（推荐）")
    
    choice = input("\n请选择 (1/2): ").strip()
    
    if choice == '1':
        success = download_small_datasets()
    elif choice == '2':
        success = download_with_kagglehub()
    else:
        print("使用kagglehub下载...")
        success = download_with_kagglehub()
    
    if success:
        print("\n✓ 数据集下载成功")
        print("\n下一步:")
        print("  python scripts/prepare_real_data.py")
        print("  python scripts/train_model.py")
    else:
        print("\n✗ 下载失败")
        sys.exit(1)
