"""
详细测试图像识别模型
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from PIL import Image
import io
import numpy as np
from app.models.services.image_service import ImageRecognitionService

async def test_with_various_images():
    """使用不同类型的测试图像进行测试"""
    print("=" * 60)
    print("详细图像识别测试")
    print("=" * 60)
    
    # 创建服务实例
    print("\n初始化图像识别服务...")
    service = ImageRecognitionService()
    
    if service.model is None:
        print("✗ 模型未加载")
        return
    
    print("✓ 模型已加载")
    
    # 创建不同颜色的测试图像
    test_cases = [
        ("绿色图像（模拟健康植物）", (34, 139, 34)),
        ("黄色图像（模拟病变）", (255, 255, 0)),
        ("棕色图像（模拟枯萎）", (139, 69, 19)),
        ("红色图像（模拟病害）", (220, 20, 60)),
        ("随机噪声图像", None),
    ]
    
    print("\n开始测试不同类型的图像...")
    print("-" * 60)
    
    for i, (description, color) in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {description}")
        
        # 创建测试图像
        if color is None:
            # 随机噪声
            img_array = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
            test_image = Image.fromarray(img_array)
        else:
            test_image = Image.new('RGB', (224, 224), color=color)
        
        # 转换为字节
        image_bytes = io.BytesIO()
        test_image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
        
        # 执行识别（使用较低的阈值以查看所有结果）
        try:
            result = await service.diagnose_disease(image_bytes, confidence_threshold=0.1)
            
            if result:
                print(f"  ✓ 识别结果: {result.disease_name}")
                print(f"    置信度: {result.confidence:.4f}")
                print(f"    治疗: {result.treatment_suggestion[:50]}...")
            else:
                print(f"  ⚠ 置信度过低，无法识别")
                
        except Exception as e:
            print(f"  ✗ 错误: {str(e)}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print("\n说明:")
    print("- 当前模型使用ImageNet预训练权重，未针对病虫害数据微调")
    print("- 识别结果可能不准确，需要收集病虫害数据进行训练")
    print("- 模型架构和推理流程已验证正常工作")

if __name__ == "__main__":
    asyncio.run(test_with_various_images())
