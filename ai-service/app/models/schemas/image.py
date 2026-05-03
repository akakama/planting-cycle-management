"""
图像识别相关的数据模型
"""
from pydantic import BaseModel, Field
from typing import Optional


class DiagnosisResult(BaseModel):
    """诊断结果模型"""
    disease_name: str = Field(..., description="病虫害名称")
    confidence: float = Field(..., ge=0, le=1, description="置信度")
    treatment_suggestion: str = Field(..., description="治疗建议")


class ImageDiagnoseRequest(BaseModel):
    """图像识别请求模型（匹配后端）"""
    planId: int = Field(..., description="种植计划ID")
    imageBase64: str = Field(..., description="Base64编码的图片")


class ImageDiagnoseResponse(BaseModel):
    """图像识别响应模型（内部使用）"""
    success: bool = Field(..., description="是否成功识别")
    result: Optional[DiagnosisResult] = Field(None, description="诊断结果")
    message: str = Field(..., description="提示信息")


class DiagnoseResponse(BaseModel):
    """诊断响应模型（匹配后端期望格式）"""
    pestName: str = Field(..., description="病虫害名称")
    pestType: str = Field(default="病害", description="病虫害类型")
    cropType: str = Field(default="", description="作物类型")
    symptoms: str = Field(default="", description="症状")
    treatmentMethods: str = Field(..., description="治疗方法")
    preventionMethods: str = Field(default="", description="预防方法")
    severity: str = Field(default="中", description="严重程度")
    season: str = Field(default="", description="季节")
    confidence: float = Field(..., description="置信度(0-100)")
    highConfidence: bool = Field(default=False, description="是否高置信度")
