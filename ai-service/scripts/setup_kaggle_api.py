"""
Kaggle API配置助手
帮助用户配置Kaggle API密钥
"""
import os
import json
from pathlib import Path

def setup_kaggle_api():
    """配置Kaggle API"""
    print("="*60)
    print("Kaggle API 配置助手")
    print("="*60)

    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"

    # 创建目录
    kaggle_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n✓ Kaggle目录: {kaggle_dir}")

    # 检查是否已有配置
    if kaggle_json.exists():
        print("✓ 已存在Kaggle配置文件")
        return True

    print("\n需要配置Kaggle API密钥")
    print("\n获取API密钥的步骤:")
    print("1. 访问 https://www.kaggle.com/")
    print("2. 登录你的Kaggle账号")
    print("3. 点击右上角头像 -> Account")
    print("4. 滚动到 'API' 部分")
    print("5. 点击 'Create New API Token'")
    print("6. 会自动下载 kaggle.json 文件")
    print(f"7. 将下载的文件复制到: {kaggle_dir}")

    # 提供手动输入选项
    print("\n或者，你可以手动输入API密钥:")
    choice = input("是否手动输入API密钥? (y/n): ").strip().lower()

    if choice == 'y':
        username = input("请输入Kaggle用户名: ").strip()
        api_key = input("请输入Kaggle API密钥: ").strip()

        if username and api_key:
            # 创建配置文件
            config = {
                "username": username,
                "key": api_key
            }

            with open(kaggle_json, 'w') as f:
                json.dump(config, f)

            # 设置文件权限（Windows上可能不需要）
            try:
                os.chmod(kaggle_json, 0o600)
            except:
                pass

            print(f"\n✓ API密钥已保存到: {kaggle_json}")
            return True
        else:
            print("\n✗ 用户名或密钥不能为空")
            return False
    else:
        print(f"\n请将下载的 kaggle.json 文件放到: {kaggle_dir}")
        print("然后重新运行此脚本")
        return False

if __name__ == "__main__":
    success = setup_kaggle_api()
    if success:
        print("\n✓ Kaggle API配置完成")
        print("现在可以运行下载脚本了")
    else:
        print("\n✗ Kaggle API配置未完成")
        print("请按照上述步骤配置后再试")
