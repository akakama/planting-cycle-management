"""
公共数据模型和错误响应
"""
from pydantic import BaseModel, Field
from typing import Optional, Any


class ErrorDetail(BaseModel):
    """错误详情"""
    field: Optional[str] = Field(None, description="错误字段")
    message: str = Field(..., description="错误消息")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    code: int = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    details: Optional[list[ErrorDetail]] = Field(None, description="错误详情列表")
    timestamp: int = Field(..., description="时间戳")
