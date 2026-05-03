"""
检索相关的数据模型
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class RetrievedDocument(BaseModel):
    """检索到的文档模型"""
    content: str = Field(..., description="文档内容")
    metadata: Optional[Dict[str, Any]] = Field(None, description="文档元数据")
    score: float = Field(..., description="相似度分数")


class RetrieveRequest(BaseModel):
    """检索请求模型"""
    query: str = Field(..., min_length=1, description="查询关键词")
    top_k: int = Field(default=5, gt=0, le=20, description="返回文档数量")


class RetrieveResponse(BaseModel):
    """检索响应模型"""
    documents: List[RetrievedDocument] = Field(..., description="检索到的文档列表")
    total: int = Field(..., description="总文档数")
