"""
检索接口实现
提供 /api/retrieve 接口
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas.retrieve import RetrieveRequest, RetrieveResponse

router = APIRouter()
retrieval_service = None  # 在应用启动时初始化


@router.post("/api/retrieve", response_model=RetrieveResponse)
async def retrieve(request: RetrieveRequest):
    """
    向量检索接口

    Args:
        request: 检索请求

    Returns:
        检索响应
    """
    try:
        # 检查服务是否初始化
        if retrieval_service is None:
            raise HTTPException(status_code=503, detail="检索服务未初始化")

        # 调用检索服务
        documents = await retrieval_service.search_documents(
            query=request.query,
            top_k=request.top_k
        )

        # 构建响应
        response = RetrieveResponse(
            documents=documents,
            total=len(documents)
        )

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检索失败: {str(e)}")
