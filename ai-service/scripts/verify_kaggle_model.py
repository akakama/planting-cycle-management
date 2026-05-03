"""
验证Kaggle训练的模型是否能正确加载
"""
import torch
import torch.nn as nn
from torchvision import models
import os

def verify_model():
    """验证模型加载"""
    print("=" * 70)
    print("验证Kaggle MobileNetV3模型")
    print("=" * 70)
    
    model_path = "models/mobilenetv3_best.pth"
    
    if not os.path.exists(model_path):
        print(f"\n✗ 错误: 找不到模型文件 {model_path}")
        print("\n请按以下步骤操作:")
        print("1. 在Kaggle Notebook右侧Output面板下载 mobilenetv3_best.pth")
        print("2. 将文件放到 ai-service/models/ 目录")
        return False
    
    file_size = os.path.getsize(model_path) / 1024 / 1024
    print(f"\n✓ 找到模型文件: {model_path}")
    print(f"  文件大小: {file_size:.2f} MB")
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\n使用设备: {device}")
    if torch.cuda.is_available():
        print(f"  GPU型号: {torch.cuda.get_device_name(0)}")
    
    print("\n加载模型...")
    try:
        model = models.mobilenet_v3_large(weights=None)
        
        num_classes = 38
        in_features = model.classifier[3].in_features
        model.classifier[3] = nn.Linear(in_features, num_classes)
        
        state_dict = torch.load(model_path, map_location=device)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        
        print("✓ 模型加载成功!")
        
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        print(f"\n模型信息:")
        print(f"  类别数: {num_classes}")
        print(f"  总参数: {total_params:,}")
        print(f"  可训练参数: {trainable_params:,}")
        
        print("\n测试推理...")
        dummy_input = torch.randn(1, 3, 224, 224).to(device)
        
        with torch.no_grad():
            output = model(dummy_input)
            probs = torch.softmax(output, dim=1)
            pred = output.argmax(1).item()
            confidence = probs[0, pred].item()
        
        print(f"✓ 推理测试成功!")
        print(f"  输出形状: {output.shape}")
        print(f"  预测类别: {pred}")
        print(f"  置信度: {confidence:.4f}")
        
        print("\n" + "=" * 70)
        print("✓ 模型验证通过，可以正常使用!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n✗ 模型加载失败: {e}")
        print("\n可能的原因:")
        print("1. 文件损坏或不完整")
        print("2. PyTorch版本不兼容")
        print("3. 文件不是state_dict格式")
        return False

def verify_class_mapping():
    """验证类别映射"""
    print("\n" + "=" * 70)
    print("验证类别映射")
    print("=" * 70)
    
    mapping_path = "models/class_mapping.json"
    
    if not os.path.exists(mapping_path):
        print(f"\n✗ 找不到类别映射文件: {mapping_path}")
        print("  请从Kaggle下载 class_mapping.json")
        return False
    
    import json
    with open(mapping_path, 'r') as f:
        mapping = json.load(f)
    
    print(f"\n✓ 类别映射加载成功")
    print(f"  类别数: {len(mapping)}")
    print("\n  前10个类别:")
    for i in range(min(10, len(mapping))):
        print(f"    {i}: {mapping[str(i)]}")
    
    return True

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    model_ok = verify_model()
    mapping_ok = verify_class_mapping()
    
    if model_ok and mapping_ok:
        print("\n" + "=" * 70)
        print("🎉 所有验证通过!")
        print("\n下一步:")
        print("  1. 启动AI服务: python -m app.main")
        print("  2. 访问接口: POST http://localhost:8000/api/image/diagnose")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("⚠ 部分验证失败，请检查上述错误信息")
        print("=" * 70)
