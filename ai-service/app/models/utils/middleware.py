"""
中间件配置
"""
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.models.utils.exceptions import AIServiceError
from app.models.schemas.common import ErrorResponse
from app.models.utils.logger import logger
import time


def setup_cors_middleware(app):
    """
    配置 CORS 中间件

    Args:
        app: FastAPI 应用实例
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境应限制为后端地址
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def logging_middleware(request: Request, call_next):
    """
    请求日志中间件

    Args:
        request: 请求对象
        call_next: 下一个中间件或路由处理器

    Returns:
        响应对象
    """
    start_time = time.time()
    logger.info(f"请求开始: {request.method} {request.url.path}")

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"请求完成: {request.method} {request.url.path} - "
        f"状态码: {response.status_code} - 耗时: {process_time:.2f}s"
    )

    return response


def setup_exception_handlers(app):
    """
    配置全局异常处理

    Args:
        app: FastAPI 应用实例
    """
    @app.exception_handler(AIServiceError)
    async def ai_service_exception_handler(request: Request, exc: AIServiceError):
        """AI 服务异常处理器"""
        logger.error(f"AI 服务异常: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                code=500,
                message=str(exc),
                timestamp=int(time.time())
            ).dict()
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """通用异常处理器"""
        logger.error(f"未捕获的异常: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                code=500,
                message="服务器内部错误",
                timestamp=int(time.time())
            ).dict()
        )
