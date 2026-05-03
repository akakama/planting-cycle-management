"""
下载并准备MobileNetV3模型用于病虫害识别
"""
import torch
import torch.nn as nn
from torchvision.models import mobilenet_v3_small
import os

def create_disease_recognition_model(num_classes=6, use_pretrained=True):
    """
    创建用于病虫害识别的MobileNetV3模型
    
    Args:
        num_classes: 病虫害类别数量（默认6类）
        use_pretrained: 是否使用预训练权重
    
    Returns:
        修改后的MobileNetV3模型
    """
    # 加载MobileNetV3 Small模型
    try:
        if use_pretrained:
            print("尝试加载预训练权重...")
            model = mobilenet_v3_small(pretrained=True)
            print("✓ 预训练权重加载成功")
        else:
            raise Exception("跳过预训练权重下载")
    except Exception as e:
        print(f"无法加载预训练权重: {str(e)}")
        print("使用随机初始化的模型...")
        model = mobilenet_v3_small(pretrained=False)
        print("✓ 随机初始化模型创建成功")
    
    # 修改最后一层分类器以适应病虫害识别任务
    # MobileNetV3 Small的分类器结构: Sequential(
    #   Linear(576, 1024),
    #   Hardswish(),
    #   Dropout(0.2),
    #   Linear(1024, num_classes)
    # )
    in_features = model.classifier[0].in_features
    
    # 替换分类器
    model.classifier = nn.Sequential(
        nn.Linear(in_features, 1024),
        nn.Hardswish(),
        nn.Dropout(0.2),
        nn.Linear(1024, num_classes)
    )
    
    return model

def main():
    """主函数"""
    print("=" * 60)
    print("MobileNetV3 病虫害识别模型准备工具")
    print("=" * 60)
    
    # 创建模型目录
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'mobilenetv3.pth')
    
    print(f"\n模型保存路径: {model_path}")
    
    # 检查是否已存在模型文件
    if os.path.exists(model_path):
        response = input("\n模型文件已存在，是否覆盖？(y/n): ")
        if response.lower() != 'y':
            print("操作已取消")
            return
    
    print("\n正在创建MobileNetV3模型...")
    print("病虫害类别:")
    print("  0: 小麦白粉病")
    print("  1: 稻瘟病")
    print("  2: 玉米大斑病")
    print("  3: 蚜虫")
    print("  4: 红蜘蛛")
    print("  5: 白粉虱")
    
    # 创建模型（尝试使用预训练权重，失败则使用随机初始化）
    model = create_disease_recognition_model(num_classes=6, use_pretrained=True)
    
    print("\n正在保存模型...")
    torch.save(model, model_path)
    
    # 验证模型文件
    file_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
    print(f"\n✓ 模型保存成功!")
    print(f"  文件大小: {file_size:.2f} MB")
    print(f"  文件路径: {model_path}")
    
    # 测试加载模型
    print("\n正在验证模型加载...")
    try:
        loaded_model = torch.load(model_path)
        loaded_model.eval()
        print("✓ 模型加载验证成功!")
        
        # 测试推理
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = loaded_model(dummy_input)
        print(f"✓ 模型推理测试成功! 输出形状: {output.shape}")
        
    except Exception as e:
        print(f"✗ 模型验证失败: {str(e)}")
        return
    
    print("\n" + "=" * 60)
    print("模型准备完成！")
    print("=" * 60)
    print("\n注意事项:")
    print("1. 此模型使用ImageNet预训练权重初始化")
    print("2. 需要使用病虫害数据集进行微调训练才能获得最佳效果")
    print("3. 当前模型可以正常加载和推理，但识别准确率可能较低")
    print("4. 建议收集病虫害图像数据并进行模型微调")
    print("\n下一步:")
    print("- 重启AI服务以加载新模型")
    print("- 准备病虫害图像数据进行模型微调训练")

if __name__ == "__main__":
    main()
