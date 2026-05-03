"""
测试图像识别服务
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from PIL import Image
import io
from app.models.services.image_service import ImageRecognitionService

async def test_image_recognition():
    """测试图像识别功能"""
    print("=" * 60)
    print("图像识别服务测试")
    print("=" * 60)
    
    # 创建服务实例
    print("\n1. 初始化图像识别服务...")
    service = ImageRecognitionService()
    
    # 检查模型是否加载
    if service.model is None:
        print("✗ 模型未加载，使用模拟模式")
    else:
        print("✓ 模型已加载，使用真实推理")
    
    # 创建测试图像（随机生成的图像）
    print("\n2. 创建测试图像...")
    test_image = Image.new('RGB', (224, 224), color=(73, 109, 137))
    
    # 转换为字节
    image_bytes = io.BytesIO()
    test_image.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()
    
    print(f"✓ 测试图像已创建，大小: {len(image_bytes)} 字节")
    
    # 执行识别
    print("\n3. 执行病虫害识别...")
    try:
        result = await service.diagnose_disease(image_bytes, confidence_threshold=0.3)
        
        if result:
            print("\n✓ 识别成功!")
            print(f"  病虫害名称: {result.disease_name}")
            print(f"  置信度: {result.confidence:.4f}")
            print(f"  治疗建议: {result.treatment_suggestion}")
        else:
            print("\n⚠ 置信度低于阈值，无法确定病虫害类型")
            
    except Exception as e:
        print(f"\n✗ 识别失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_image_recognition())
