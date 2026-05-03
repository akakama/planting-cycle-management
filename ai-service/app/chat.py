"""
对话接口实现
提供 /v1/chat/completions 接口
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas.chat import ChatCompletionRequest, ChatCompletionResponse, ChatCompletionChoice, ChatCompletionMessage, Usage
import time
import uuid

router = APIRouter()
chat_service = None  # 在应用启动时初始化


@router.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    """
    对话生成接口

    Args:
        request: 对话请求

    Returns:
        对话响应
    """
    try:
        # 检查服务是否初始化
        if chat_service is None:
            raise HTTPException(status_code=503, detail="对话服务未初始化")

        # 调用对话服务
        response_text = await chat_service.generate_response(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        # 构建响应
        response = ChatCompletionResponse(
            id=str(uuid.uuid4()),
            object="chat.completion",
            created=int(time.time()),
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=ChatCompletionMessage(
                        role="assistant",
                        content=response_text
                    ),
                    finish_reason="stop"
                )
            ],
            usage=Usage(
                prompt_tokens=sum(len(msg.content) for msg in request.messages),
                completion_tokens=len(response_text),
                total_tokens=sum(len(msg.content) for msg in request.messages) + len(response_text)
            )
        )

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话生成失败: {str(e)}")
