"""
使用真实测试数据评估模型
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import torch
from PIL import Image
from pathlib import Path
import asyncio
from app.models.services.image_service import ImageRecognitionService

def evaluate_on_real_data():
    """在真实测试数据上评估模型"""
    print("="*60)
    print("使用真实数据评估模型")
    print("="*60)
    
    # 加载模型
    print("\n加载模型...")
    service = ImageRecognitionService()
    
    if service.model is None:
        print("✗ 模型加载失败")
        return
    
    print("✓ 模型加载成功")
    
    # 测试真实数据
    test_dir = Path("data/test")
    
    if not test_dir.exists():
        print("✗ 测试数据未找到")
        return
    
    print("\n评估真实测试数据:")
    print("-"*60)
    
    total = 0
    correct = 0
    results = {}
    
    for class_dir in test_dir.iterdir():
        if not class_dir.is_dir():
            continue
        
        class_name = class_dir.name
        results[class_name] = {"total": 0, "correct": 0}
        
        print(f"\n测试类别: {class_name}")
        
        for img_file in list(class_dir.glob("*.jpg"))[:20]:  # 每类测试20张
            # 加载图像
            image = Image.open(img_file)
            
            # 转换为bytes
            import io
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='JPEG')
            img_bytes = img_bytes.getvalue()
            
            # 识别
            result = asyncio.run(service.diagnose_disease(img_bytes, confidence_threshold=0.1))
            
            results[class_name]["total"] += 1
            total += 1
            
            if result and result.disease_name == class_name:
                results[class_name]["correct"] += 1
                correct += 1
                status = "✓"
            else:
                status = "✗"
            
            predicted = result.disease_name if result else "无法识别"
            confidence = f"{result.confidence:.2f}" if result else "N/A"
            
            print(f"  {status} 预测: {predicted:10s} | 置信度: {confidence}")
    
    # 打印结果
    print("\n" + "="*60)
    print("评估结果")
    print("="*60)
    
    for class_name, stats in results.items():
        if stats["total"] > 0:
            acc = stats["correct"] / stats["total"] * 100
            print(f"{class_name}: {acc:.1f}% ({stats['correct']}/{stats['total']})")
    
    if total > 0:
        overall_acc = correct / total * 100
        print("-"*60)
        print(f"总体准确率: {overall_acc:.1f}% ({correct}/{total})")

if __name__ == "__main__":
    evaluate_on_real_data()
