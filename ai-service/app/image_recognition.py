"""
图像识别接口实现
提供 /api/image/diagnose 接口
同时提供 /api/pest/diagnose 接口（匹配后端调用）
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas.image import DiagnoseResponse, ImageDiagnoseRequest
from app.config import config
import base64

router = APIRouter()
image_service = None


def infer_crop_type(disease_name: str) -> str:
    """Infer crop type from the bilingual PlantVillage class name."""
    crop_map = {
        "苹果": "苹果",
        "Apple": "苹果",
        "蓝莓": "蓝莓",
        "Blueberry": "蓝莓",
        "樱桃": "樱桃",
        "Cherry": "樱桃",
        "玉米": "玉米",
        "Corn": "玉米",
        "葡萄": "葡萄",
        "Grape": "葡萄",
        "柑橘": "柑橘",
        "Orange": "柑橘",
        "桃": "桃",
        "Peach": "桃",
        "辣椒": "辣椒",
        "Pepper": "辣椒",
        "马铃薯": "马铃薯",
        "Potato": "马铃薯",
        "树莓": "树莓",
        "Raspberry": "树莓",
        "大豆": "大豆",
        "Soybean": "大豆",
        "南瓜": "南瓜",
        "Squash": "南瓜",
        "草莓": "草莓",
        "Strawberry": "草莓",
        "番茄": "番茄",
        "Tomato": "番茄",
    }

    for marker, crop_type in crop_map.items():
        if marker in disease_name:
            return crop_type
    return ""


def infer_prevention_methods(disease_name: str) -> str:
    """Provide concise prevention advice for the recognized crop/disease."""
    if "健康" in disease_name or "Healthy" in disease_name:
        return "保持合理水肥管理和田间通风，定期巡查叶片状态，发现异常及时隔离处理。"

    if "病毒" in disease_name or "Virus" in disease_name:
        return "选用抗病品种和健康种苗，及时防治蚜虫、粉虱等传毒媒介，清除病株并避免接触传播。"

    if "细菌" in disease_name or "Bacterial" in disease_name:
        return "使用健康种苗，避免叶面长期潮湿，减少机械伤口，雨后及时排湿并清理病残体。"

    if "红蜘蛛" in disease_name or "Spider" in disease_name or "Mites" in disease_name:
        return "保持适宜湿度，清除杂草和老叶，保护天敌，定期检查叶背虫口密度。"

    return "选用抗病品种，合理轮作，保持田间通风透光，及时清除病叶病株并避免高湿环境。"


@router.post("/api/image/diagnose", response_model=DiagnoseResponse)
async def diagnose_image_json(request_body: ImageDiagnoseRequest):
    """
    图像识别接口（JSON方式，匹配后端调用）

    后端发送: {"planId": 1, "imageBase64": "base64编码的图片"}
    """
    try:
        if image_service is None:
            raise HTTPException(status_code=503, detail="图像识别服务未初始化")

        try:
            image_bytes = base64.b64decode(request_body.imageBase64)
        except Exception:
            raise HTTPException(status_code=400, detail="无效的Base64图片数据")

        if len(image_bytes) > config.image_recognition.max_image_size:
            raise HTTPException(status_code=413, detail="图像文件过大")

        result = await image_service.diagnose_disease(
            image_bytes=image_bytes,
            confidence_threshold=config.image_recognition.confidence_threshold
        )

        if result:
            crop_type = infer_crop_type(result.disease_name)
            return DiagnoseResponse(
                pestName=result.disease_name,
                pestType="病害",
                cropType=crop_type,
                symptoms="",
                treatmentMethods=result.treatment_suggestion,
                preventionMethods=infer_prevention_methods(result.disease_name),
                severity="中",
                season="",
                confidence=result.confidence * 100,
                highConfidence=result.confidence > 0.85
            )
        else:
            return DiagnoseResponse(
                pestName="未知病虫害",
                pestType="待识别",
                cropType="",
                symptoms="无法识别具体病虫害类型",
                treatmentMethods="建议人工诊断",
                preventionMethods="建议重新拍摄清晰的叶片正反面图片，并结合田间症状请农技人员复核。",
                severity="未知",
                season="",
                confidence=50.0,
                highConfidence=False
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图像识别失败: {str(e)}")
