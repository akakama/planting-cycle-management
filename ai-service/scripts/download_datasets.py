"""
病虫害图像数据集下载和准备脚本
支持从多个公开数据集下载图像数据
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
import json

class DatasetDownloader:
    """数据集下载器"""

    def __init__(self, base_dir="data/datasets"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.metadata = {}

    def check_kaggle_cli(self):
        """检查Kaggle CLI是否安装"""
        try:
            result = subprocess.run(["kaggle", "--version"],
                                    capture_output=True, text=True)
            return True
        except FileNotFoundError:
            print("⚠️  Kaggle CLI未安装")
            print("安装方法: pip install kaggle")
            print("配置方法: 将kaggle.json放到 ~/.kaggle/ 目录")
            return False

    def download_plantvillage(self):
        """
        下载PlantVillage数据集
        来源: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
        """
        print("\n" + "="*60)
        print("下载 PlantVillage Dataset")
        print("="*60)
        print("来源: Penn State University")
        print("图像数量: 54,305张")
        print("类别数量: 38类")
        print("大小: 约1.5GB")

        target_dir = self.base_dir / "plantvillage"
        target_dir.mkdir(exist_ok=True)

        if self.check_kaggle_cli():
            print("\n开始下载...")
            try:
                subprocess.run([
                    "kaggle", "datasets", "download",
                    "-d", "abdallahalidev/plantvillage-dataset",
                    "-p", str(target_dir),
                    "--unzip"
                ], check=True)
                print("✓ PlantVillage下载完成")

                self.metadata["plantvillage"] = {
                    "source": "https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset",
                    "images": 54305,
                    "classes": 38,
                    "citation": "Mohanty et al., 2016"
                }
            except Exception as e:
                print(f"✗ 下载失败: {str(e)}")
        else:
            print("\n手动下载方法:")
            print("1. 访问: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset")
            print("2. 点击Download")
            print(f"3. 解压到: {target_dir}")

    def download_rice_diseases(self):
        """
        下载水稻病害数据集
        来源: https://www.kaggle.com/minhhuy2810/rice-diseases-image-dataset
        """
        print("\n" + "="*60)
        print("下载 Rice Diseases Dataset")
        print("="*60)
        print("来源: Kaggle")
        print("图像数量: 1,200张")
        print("类别数量: 4类（含稻瘟病）")

        target_dir = self.base_dir / "rice_diseases"
        target_dir.mkdir(exist_ok=True)

        if self.check_kaggle_cli():
            print("\n开始下载...")
            try:
                subprocess.run([
                    "kaggle", "datasets", "download",
                    "-d", "minhhuy2810/rice-diseases-image-dataset",
                    "-p", str(target_dir),
                    "--unzip"
                ], check=True)
                print("✓ Rice Diseases下载完成")

                self.metadata["rice_diseases"] = {
                    "source": "https://www.kaggle.com/minhhuy2810/rice-diseases-image-dataset",
                    "images": 1200,
                    "classes": 4,
                    "contains": ["稻瘟病"]
                }
            except Exception as e:
                print(f"✗ 下载失败: {str(e)}")
        else:
            print("\n手动下载方法:")
            print("1. 访问: https://www.kaggle.com/minhhuy2810/rice-diseases-image-dataset")
            print("2. 点击Download")
            print(f"3. 解压到: {target_dir}")

    def download_wheat_diseases(self):
        """
        下载小麦病害数据集
        来源: https://www.kaggle.com/olympic2019/wheat-disease-dataset
        """
        print("\n" + "="*60)
        print("下载 Wheat Disease Dataset")
        print("="*60)
        print("来源: Kaggle")
        print("图像数量: 3,000+张")
        print("包含: 小麦白粉病")

        target_dir = self.base_dir / "wheat_diseases"
        target_dir.mkdir(exist_ok=True)

        if self.check_kaggle_cli():
            print("\n开始下载...")
            try:
                subprocess.run([
                    "kaggle", "datasets", "download",
                    "-d", "olympic2019/wheat-disease-dataset",
                    "-p", str(target_dir),
                    "--unzip"
                ], check=True)
                print("✓ Wheat Disease下载完成")

                self.metadata["wheat_diseases"] = {
                    "source": "https://www.kaggle.com/olympic2019/wheat-disease-dataset",
                    "images": 3000,
                    "contains": ["小麦白粉病"]
                }
            except Exception as e:
                print(f"✗ 下载失败: {str(e)}")
        else:
            print("\n手动下载方法:")
            print("1. 访问: https://www.kaggle.com/olympic2019/wheat-disease-dataset")
            print("2. 点击Download")
            print(f"3. 解压到: {target_dir}")

    def download_corn_diseases(self):
        """
        下载玉米病害数据集
        来源: https://www.kaggle.com/smaranjitghose/corn-or-maize-leaf-disease-dataset
        """
        print("\n" + "="*60)
        print("下载 Corn Disease Dataset")
        print("="*60)
        print("来源: Kaggle")
        print("图像数量: 1,800张")
        print("包含: 玉米大斑病")

        target_dir = self.base_dir / "corn_diseases"
        target_dir.mkdir(exist_ok=True)

        if self.check_kaggle_cli():
            print("\n开始下载...")
            try:
                subprocess.run([
                    "kaggle", "datasets", "download",
                    "-d", "smaranjitghose/corn-or-maize-leaf-disease-dataset",
                    "-p", str(target_dir),
                    "--unzip"
                ], check=True)
                print("✓ Corn Disease下载完成")

                self.metadata["corn_diseases"] = {
                    "source": "https://www.kaggle.com/smaranjitghose/corn-or-maize-leaf-disease-dataset",
                    "images": 1800,
                    "contains": ["玉米大斑病"]
                }
            except Exception as e:
                print(f"✗ 下载失败: {str(e)}")
        else:
            print("\n手动下载方法:")
            print("1. 访问: https://www.kaggle.com/smaranjitghose/corn-or-maize-leaf-disease-dataset")
            print("2. 点击Download")
            print(f"3. 解压到: {target_dir}")

    def download_plantdoc(self):
        """
        下载PlantDoc数据集
        来源: https://github.com/pratikkamal/PlantDoc-Dataset
        """
        print("\n" + "="*60)
        print("下载 PlantDoc Dataset")
        print("="*60)
        print("来源: GitHub")
        print("图像数量: 2,589张")
        print("包含: 小麦白粉病、稻瘟病、玉米大斑病")

        target_dir = self.base_dir / "plantdoc"

        print("\n开始下载...")
        try:
            subprocess.run([
                "git", "clone",
                "https://github.com/pratikkamal/PlantDoc-Dataset.git",
                str(target_dir)
            ], check=True)
            print("✓ PlantDoc下载完成")

            self.metadata["plantdoc"] = {
                "source": "https://github.com/pratikkamal/PlantDoc-Dataset",
                "images": 2589,
                "classes": 27,
                "citation": "Singh et al., 2019"
            }
        except Exception as e:
            print(f"✗ 下载失败: {str(e)}")
            print("\n手动下载方法:")
            print("1. 访问: https://github.com/pratikkamal/PlantDoc-Dataset")
            print("2. 点击Code -> Download ZIP")
            print(f"3. 解压到: {target_dir}")

    def save_metadata(self):
        """保存数据集元数据"""
        metadata_file = self.base_dir / "datasets_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        print(f"\n✓ 元数据已保存到: {metadata_file}")

    def download_all(self):
        """下载所有推荐的数据集"""
        print("\n" + "="*60)
        print("开始下载所有推荐数据集")
        print("="*60)

        # 下载各个数据集
        self.download_plantvillage()
        self.download_rice_diseases()
        self.download_wheat_diseases()
        self.download_corn_diseases()
        self.download_plantdoc()

        # 保存元数据
        self.save_metadata()

        print("\n" + "="*60)
        print("所有数据集下载完成")
        print("="*60)

    def download_quick(self):
        """快速下载（仅下载小规模数据集）"""
        print("\n" + "="*60)
        print("快速下载模式（小规模数据集）")
        print("="*60)

        self.download_rice_diseases()
        self.download_wheat_diseases()
        self.download_corn_diseases()

        self.save_metadata()

        print("\n" + "="*60)
        print("快速下载完成")
        print("="*60)


def main():
    """主函数"""
    print("="*60)
    print("病虫害图像数据集下载工具")
    print("="*60)
    print("\n可用的数据集:")
    print("1. PlantVillage (54,305张, 38类)")
    print("2. Rice Diseases (1,200张, 含稻瘟病)")
    print("3. Wheat Disease (3,000+张, 含小麦白粉病)")
    print("4. Corn Disease (1,800张, 含玉米大斑病)")
    print("5. PlantDoc (2,589张, 27类)")
    print("\n下载选项:")
    print("a. 下载所有数据集（推荐）")
    print("b. 快速下载（仅小规模数据集）")
    print("c. 单独下载PlantVillage")
    print("d. 单独下载PlantDoc")

    choice = input("\n请选择下载选项 (a/b/c/d): ").strip().lower()

    downloader = DatasetDownloader()

    if choice == 'a':
        downloader.download_all()
    elif choice == 'b':
        downloader.download_quick()
    elif choice == 'c':
        downloader.download_plantvillage()
        downloader.save_metadata()
    elif choice == 'd':
        downloader.download_plantdoc()
        downloader.save_metadata()
    else:
        print("无效的选择")


if __name__ == "__main__":
    main()
