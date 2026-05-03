"""
Kaggle API配置和真实数据集下载脚本
"""
import os
from pathlib import Path
import subprocess
import sys

def check_kaggle_config():
    """检查Kaggle API配置"""
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"

    print("="*60)
    print("Kaggle API 配置检查")
    print("="*60)

    if kaggle_json.exists():
        print("✓ Kaggle API已配置")
        print(f"  配置文件: {kaggle_json}")
        return True
    else:
        print("✗ Kaggle API未配置")
        print("\n配置步骤:")
        print("1. 访问 https://www.kaggle.com/account")
        print("2. 滚动到 'API' 部分")
        print("3. 点击 'Create New API Token'")
        print("4. 下载 kaggle.json 文件")
        print(f"5. 将文件放到: {kaggle_dir}")
        print("\n或者手动创建配置文件:")
        print(f"  mkdir -p {kaggle_dir}")
        print(f"  # 创建 kaggle.json 包含:")
        print('  {"username":"YOUR_USERNAME","key":"YOUR_KEY"}')

        # 尝试创建目录
        kaggle_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n✓ 已创建目录: {kaggle_dir}")

        return False

def download_with_retry(dataset_name, target_dir, max_retries=3):
    """带重试的数据集下载"""
    for attempt in range(max_retries):
        try:
            print(f"\n尝试下载 {dataset_name} (第{attempt+1}次)...")
            result = subprocess.run([
                "kaggle", "datasets", "download",
                "-d", dataset_name,
                "-p", str(target_dir),
                "--unzip"
            ], check=True, capture_output=True, text=True)
            print(f"✓ {dataset_name} 下载成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ 下载失败: {e}")
            if attempt < max_retries - 1:
                print("等待5秒后重试...")
                import time
                time.sleep(5)
        except Exception as e:
            print(f"✗ 错误: {e}")

    return False

def download_real_datasets():
    """下载真实病虫害数据集"""
    print("\n" + "="*60)
    print("下载真实病虫害数据集")
    print("="*60)

    base_dir = Path("data/datasets")
    base_dir.mkdir(parents=True, exist_ok=True)

    # 数据集列表
    datasets = [
        ("minhhuy2810/rice-diseases-image-dataset", "rice_diseases", "水稻病害 (1,200张)"),
        ("smaranjitghose/corn-or-maize-leaf-disease-dataset", "corn_diseases", "玉米病害 (1,800张)"),
    ]

    success_count = 0

    for dataset_name, folder_name, description in datasets:
        print(f"\n下载: {description}")
        print(f"数据集: {dataset_name}")

        target_dir = base_dir / folder_name
        target_dir.mkdir(exist_ok=True)

        if download_with_retry(dataset_name, target_dir):
            success_count += 1
        else:
            print(f"⚠️  {description} 下载失败，将跳过")

    print("\n" + "="*60)
    print(f"下载完成: {success_count}/{len(datasets)} 个数据集")
    print("="*60)

    return success_count > 0

def main():
    """主函数"""
    # 检查Kaggle配置
    if not check_kaggle_config():
        print("\n请先配置Kaggle API，然后重新运行此脚本")
        print("\n临时方案: 使用GitHub数据集")
        use_github = input("是否尝试从GitHub下载PlantDoc数据集? (y/n): ").strip().lower()

        if use_github == 'y':
            print("\n从GitHub下载PlantDoc...")
            try:
                result = subprocess.run([
                    "git", "clone",
                    "https://github.com/pratikkamal/PlantDoc-Dataset.git",
                    "data/datasets/plantdoc"
                ], check=True)
                print("✓ PlantDoc下载成功")
                return True
            except:
                print("✗ GitHub下载也失败")
                return False
        return False

    # 下载真实数据集
    return download_real_datasets()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
