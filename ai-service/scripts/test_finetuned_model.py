"""
测试微调后的模型
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import torch
from PIL import Image
import io
from app.models.services.image_service import ImageRecognitionService

def test_finetuned_model():
    """测试微调后的模型"""
    print("="*60)
    print("测试微调后的模型")
    print("="*60)

    # 临时修改模型路径
    import app.config as config_module
    original_path = config_module.config.image_recognition.model_path
    config_module.config.image_recognition.model_path = "models/mobilenetv3_finetuned.pth"

    # 创建服务
    print("\n加载微调后的模型...")
    service = ImageRecognitionService()

    if service.model is None:
        print("✗ 模型加载失败")
        return

    print("✓ 模型加载成功")

    # 测试图像
    test_images = [
        ("小麦白粉病", (200, 180, 150)),
        ("稻瘟病", (180, 200, 160)),
        ("玉米大斑病", (160, 180, 200)),
        ("蚜虫", (150, 200, 150)),
        ("红蜘蛛", (200, 150, 150)),
        ("白粉虱", (220, 220, 200)),
    ]

    print("\n测试识别效果:")
    print("-"*60)

    correct = 0
    total = len(test_images)

    for true_label, color in test_images:
        # 创建测试图像
        img = Image.new('RGB', (224, 224), color=color)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        # 识别
        import asyncio
        result = asyncio.run(service.diagnose_disease(img_bytes, confidence_threshold=0.3))

        if result:
            predicted = result.disease_name
            confidence = result.confidence
            is_correct = predicted == true_label
            correct += is_correct

            status = "✓" if is_correct else "✗"
            print(f"{status} 真实: {true_label:10s} | 预测: {predicted:10s} | 置信度: {confidence:.4f}")
        else:
            print(f"✗ 真实: {true_label:10s} | 无法识别")

    print("-"*60)
    accuracy = correct / total * 100
    print(f"准确率: {accuracy:.2f}% ({correct}/{total})")

    # 恢复原始路径
    config_module.config.image_recognition.model_path = original_path

    print("\n" + "="*60)
    print("测试完成")
    print("="*60)

if __name__ == "__main__":
    test_finetuned_model()
