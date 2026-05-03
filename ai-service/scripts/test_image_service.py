"""
简单测试图像识别服务
"""
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json
import os

# 加载模型
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"使用设备: {device}")

model = models.mobilenet_v3_large(weights=None)
model.classifier[3] = nn.Linear(model.classifier[3].in_features, 38)
state_dict = torch.load('models/mobilenetv3_best.pth', map_location=device)
model.load_state_dict(state_dict)
model.to(device)
model.eval()
print("✓ 模型加载成功")

# 加载类别映射
with open('models/class_mapping.json', 'r') as f:
    class_mapping = json.load(f)
print(f"✓ 类别映射加载成功 ({len(class_mapping)} 类)")

# 预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 创建测试图像（随机噪声）
print("\n创建测试图像...")
test_image = Image.new('RGB', (224, 224), color=(120, 150, 100))
input_tensor = transform(test_image).unsqueeze(0).to(device)

# 推理
print("执行推理...")
with torch.no_grad():
    output = model(input_tensor)
    probs = torch.softmax(output, dim=1)
    top5_probs, top5_indices = torch.topk(probs, 5)

print("\n预测结果 (Top 5):")
print("-" * 70)
for i in range(5):
    idx = top5_indices[0, i].item()
    prob = top5_probs[0, i].item()
    class_name = class_mapping.get(str(idx), f"类别{idx}")
    print(f"  {i+1}. {class_name}: {prob:.4f} ({prob*100:.2f}%)")

print("\n" + "=" * 70)
print("✅ 图像识别服务测试成功!")
print("=" * 70)
print("\n下一步:")
print("  1. 启动AI服务: python -m app.main")
print("  2. 访问接口: POST http://localhost:8000/api/image/diagnose")
print("  3. 使用前端上传植物图片进行识别")
