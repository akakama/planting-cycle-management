"""
图像识别服务
使用 MobileNetV3 模型进行病虫害图像识别
支持 CPU 和 GPU 推理
"""
from typing import Optional, Dict
from PIL import Image
import torch
import torch.nn.functional as F
from torchvision import transforms
import io
import os
from app.models.schemas.image import DiagnosisResult
from app.config import config


class ImageRecognitionService:
    """图像识别服务类"""

    def __init__(self):
        """初始化图像识别服务"""
        try:
            # 设置设备（优先GPU，自动降级到CPU）
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            print(f"图像识别使用设备: {self.device}")
            
            # 检查模型文件
            model_candidates = [
                "models/mobilenetv3_best.pth",               # Kaggle训练的最佳模型（38类，98.69%准确率）
                "models/mobilenetv3_plantvillage_best.pth",  # PlantVillage最佳模型
                "models/mobilenetv3_plantvillage.pth",       # PlantVillage模型
                "models/mobilenetv3_gpu_trained.pth",        # GPU训练模型
                config.image_recognition.model_path           # 默认配置路径
            ]
            
            self.model = None
            self.model_path = None
            
            for model_path in model_candidates:
                if os.path.exists(model_path):
                    print(f"尝试加载模型: {model_path}")
                    try:
                        from torchvision import models as tv_models
                        import torch.nn as nn
                        
                        base_model = tv_models.mobilenet_v3_large(weights=None)
                        num_classes = 38
                        base_model.classifier[3] = nn.Linear(
                            base_model.classifier[3].in_features, 
                            num_classes
                        )
                        
                        state_dict = torch.load(model_path, map_location=self.device)
                        base_model.load_state_dict(state_dict)
                        base_model.to(self.device)
                        base_model.eval()
                        
                        self.model = base_model
                        self.model_path = model_path
                        print(f"✓ 模型加载成功: {model_path}")
                        break
                    except Exception as e:
                        print(f"✗ 加载失败: {e}")
                        continue
            
            if self.model is None:
                print("警告: 所有模型文件加载失败，将使用模拟模式")
            
            # 定义图像预处理
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])

            # 病虫害类别映射（PlantVillage 38类，包含中文翻译和防治建议）
            self.class_names = self._load_class_mapping()

            print(f"图像识别服务初始化成功，支持 {len(self.class_names)} 种病虫害")
        except Exception as e:
            print(f"图像识别服务初始化失败: {str(e)}")
            self.model = None

    def _load_class_mapping(self) -> Dict[int, Dict]:
        """加载病虫害类别映射"""
        
        # PlantVillage 38类病虫害（中文翻译 + 防治建议）
        class_mapping = {
            0: {"name": "苹果疮痂病", "name_en": "Apple Scab", 
                "treatment": "喷施多菌灵或代森锰锌，及时清除病叶病果"},
            1: {"name": "苹果黑腐病", "name_en": "Apple Black Rot",
                "treatment": "剪除病枝病果，喷施甲基硫菌灵或戊唑醇"},
            2: {"name": "苹果锈病", "name_en": "Apple Cedar Rust",
                "treatment": "喷施三唑酮或腈菌唑，清除附近柏树"},
            3: {"name": "苹果健康", "name_en": "Apple Healthy",
                "treatment": "无病害，继续做好预防管理"},
            4: {"name": "蓝莓健康", "name_en": "Blueberry Healthy",
                "treatment": "无病害，继续做好预防管理"},
            5: {"name": "樱桃白粉病", "name_en": "Cherry Powdery Mildew",
                "treatment": "喷施三唑酮或腈菌唑，加强通风透光"},
            6: {"name": "樱桃健康", "name_en": "Cherry Healthy",
                "treatment": "无病害，继续做好预防管理"},
            7: {"name": "玉米灰斑病", "name_en": "Corn Gray Leaf Spot",
                "treatment": "选用抗病品种，喷施苯醚甲环唑或吡唑醚菌酯"},
            8: {"name": "玉米锈病", "name_en": "Corn Common Rust",
                "treatment": "喷施三唑酮或腈菌唑，及时清除病叶"},
            9: {"name": "玉米大斑病", "name_en": "Corn Northern Leaf Blight",
                "treatment": "喷施苯醚甲环唑，加强田间管理，合理密植"},
            10: {"name": "玉米健康", "name_en": "Corn Healthy",
                "treatment": "无病害，继续做好预防管理"},
            11: {"name": "葡萄黑腐病", "name_en": "Grape Black Rot",
                "treatment": "清除病果病叶，喷施甲基硫菌灵或代森锰锌"},
            12: {"name": "葡萄黑痘病", "name_en": "Grape Esca",
                "treatment": "剪除病枝，喷施戊唑醇或苯醚甲环唑"},
            13: {"name": "葡萄叶枯病", "name_en": "Grape Leaf Blight",
                "treatment": "清除病叶，喷施代森锰锌或百菌清"},
            14: {"name": "葡萄健康", "name_en": "Grape Healthy",
                "treatment": "无病害，继续做好预防管理"},
            15: {"name": "柑橘黄龙病", "name_en": "Orange Huanglongbing",
                "treatment": "立即挖除病树，防治木虱，严格检疫"},
            16: {"name": "桃细菌性穿孔病", "name_en": "Peach Bacterial Spot",
                "treatment": "喷施农用链霉素或噻唑锌，避免伤口"},
            17: {"name": "桃健康", "name_en": "Peach Healthy",
                "treatment": "无病害，继续做好预防管理"},
            18: {"name": "辣椒细菌性斑点病", "name_en": "Pepper Bacterial Spot",
                "treatment": "喷施农用链霉素或噻唑锌，加强通风"},
            19: {"name": "辣椒健康", "name_en": "Pepper Healthy",
                "treatment": "无病害，继续做好预防管理"},
            20: {"name": "马铃薯早疫病", "name_en": "Potato Early Blight",
                "treatment": "喷施代森锰锌或百菌清，及时清除病叶"},
            21: {"name": "马铃薯晚疫病", "name_en": "Potato Late Blight",
                "treatment": "喷施甲霜灵或烯酰吗啉，及时清除病株"},
            22: {"name": "马铃薯健康", "name_en": "Potato Healthy",
                "treatment": "无病害，继续做好预防管理"},
            23: {"name": "树莓健康", "name_en": "Raspberry Healthy",
                "treatment": "无病害，继续做好预防管理"},
            24: {"name": "大豆健康", "name_en": "Soybean Healthy",
                "treatment": "无病害，继续做好预防管理"},
            25: {"name": "南瓜白粉病", "name_en": "Squash Powdery Mildew",
                "treatment": "喷施三唑酮或腈菌唑，加强通风透光"},
            26: {"name": "草莓叶焦病", "name_en": "Strawberry Leaf Scorch",
                "treatment": "清除病叶，喷施代森锰锌或百菌清"},
            27: {"name": "草莓健康", "name_en": "Strawberry Healthy",
                "treatment": "无病害，继续做好预防管理"},
            28: {"name": "番茄细菌性斑点病", "name_en": "Tomato Bacterial Spot",
                "treatment": "喷施农用链霉素或噻唑锌，避免伤口"},
            29: {"name": "番茄早疫病", "name_en": "Tomato Early Blight",
                "treatment": "喷施代森锰锌或百菌清，及时清除病叶"},
            30: {"name": "番茄晚疫病", "name_en": "Tomato Late Blight",
                "treatment": "喷施甲霜灵或烯酰吗啉，降低田间湿度"},
            31: {"name": "番茄叶霉病", "name_en": "Tomato Leaf Mold",
                "treatment": "加强通风降湿，喷施多菌灵或甲基硫菌灵"},
            32: {"name": "番茄叶斑病", "name_en": "Tomato Septoria Leaf Spot",
                "treatment": "清除病叶，喷施代森锰锌或百菌清"},
            33: {"name": "番茄红蜘蛛", "name_en": "Tomato Spider Mites",
                "treatment": "喷施阿维菌素或螺螨酯，注意轮换用药"},
            34: {"name": "番茄斑点病", "name_en": "Tomato Target Spot",
                "treatment": "喷施苯醚甲环唑或吡唑醚菌酯"},
            35: {"name": "番茄黄化曲叶病毒病", "name_en": "Tomato Yellow Leaf Curl Virus",
                "treatment": "防治烟粉虱，拔除病株，选用抗病品种"},
            36: {"name": "番茄花叶病毒病", "name_en": "Tomato Mosaic Virus",
                "treatment": "防治蚜虫，拔除病株，避免接触传染"},
            37: {"name": "番茄健康", "name_en": "Tomato Healthy",
                "treatment": "无病害，继续做好预防管理"}
        }
        
        return class_mapping

    async def diagnose_disease(self, image_bytes: bytes, confidence_threshold: float = 0.6) -> Optional[DiagnosisResult]:
        """
        诊断病虫害

        Args:
            image_bytes: 图像字节数据
            confidence_threshold: 置信度阈值

        Returns:
            诊断结果，置信度低于阈值返回 None
        """
        try:
            # 如果模型未加载，返回模拟结果
            if self.model is None:
                return self._get_mock_diagnosis()

            # 加载图像
            image = Image.open(io.BytesIO(image_bytes))
            original_format = image.format
            image = image.convert('RGB')

            # 验证图像格式
            if original_format and original_format.upper() not in ['JPEG', 'PNG', 'JPG']:
                raise ValueError(f"不支持的图像格式: {original_format}")

            # 预处理图像
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)

            # 推理
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = F.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)

            # 判断置信度
            confidence_value = confidence.item()
            predicted_class = predicted.item()
            
            if confidence_value < confidence_threshold:
                # 返回低置信度结果（而不是None）
                return DiagnosisResult(
                    disease_name="识别置信度过低",
                    confidence=confidence_value,
                    treatment_suggestion=f"置信度仅{confidence_value:.2%}，建议拍摄更清晰的病害图片或咨询农业专家"
                )

            # 获取病虫害信息
            disease_info = self.class_names.get(predicted_class, {
                "name": f"未知病虫害(类别{predicted_class})",
                "name_en": "Unknown",
                "treatment": "建议咨询农业专家"
            })

            # 返回诊断结果
            return DiagnosisResult(
                disease_name=f"{disease_info['name']}（{disease_info.get('name_en', '')}）",
                confidence=confidence_value,
                treatment_suggestion=disease_info["treatment"]
            )

        except ValueError as e:
            raise Exception(f"图像验证失败: {str(e)}")
        except Exception as e:
            print(f"图像处理失败: {str(e)}")
            raise Exception(f"图像处理失败: {str(e)}")

    def _get_mock_diagnosis(self) -> Optional[DiagnosisResult]:
        """
        获取模拟诊断结果（当模型未加载时）

        Returns:
            模拟的诊断结果
        """
        import random
        # 随机选择一个病虫害
        disease_info = random.choice(list(self.class_names.values()))
        confidence = random.uniform(0.7, 0.95)

        return DiagnosisResult(
            disease_name=f"{disease_info['name']}（模拟结果）",
            confidence=confidence,
            treatment_suggestion=f"{disease_info['treatment']}（注意：当前为模拟模式，请检查模型文件）"
        )
