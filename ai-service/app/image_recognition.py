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
            return DiagnoseResponse(
                pestName=result.disease_name,
                pestType="病害",
                symptoms="",
                treatmentMethods=result.treatment_suggestion,
                preventionMethods="",
                severity="中",
                season="",
                confidence=result.confidence * 100,
                highConfidence=result.confidence > 0.85
            )
        else:
            return DiagnoseResponse(
                pestName="未知病虫害",
                pestType="待识别",
                symptoms="无法识别具体病虫害类型",
                treatmentMethods="建议人工诊断",
                preventionMethods="",
                severity="未知",
                season="",
                confidence=50.0,
                highConfidence=False
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图像识别失败: {str(e)}")
