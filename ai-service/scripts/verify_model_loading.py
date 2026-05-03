"""验证模型加载"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.models.services.image_service import ImageRecognitionService

service = ImageRecognitionService()
print(f"模型状态: {'已加载' if service.model else '未加载'}")
print(f"模型路径: models/mobilenetv3.pth")
print(f"支持类别数: {len(service.class_names)}")
