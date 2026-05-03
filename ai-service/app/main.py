"""
AI 服务模块主入口
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import config
from app.models.services.retrieval_service import RetrievalService
from app.models.services.tool_service import ToolCallService
from app.models.services.image_service import ImageRecognitionService
from app.models.services.chat_service import ChatService
from app.models.utils.middleware import setup_cors_middleware, logging_middleware, setup_exception_handlers
from app.models.utils.logger import logger
import app.chat as chat_router
import app.retrieve as retrieve_router
import app.image_recognition as image_router

# 全局服务实例
retrieval_service = None
tool_service = None
image_service = None
chat_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动事件
    global retrieval_service, tool_service, image_service, chat_service

    logger.info("初始化 AI 服务...")

    try:
        # 初始化检索服务
        logger.info("初始化检索服务...")
        retrieval_service = RetrievalService()

        # 初始化工具调用服务
        logger.info("初始化工具调用服务...")
        tool_service = ToolCallService()

        # 初始化图像识别服务
        logger.info("初始化图像识别服务...")
        image_service = ImageRecognitionService()

        # 初始化对话服务
        logger.info("初始化对话服务...")
        chat_service = ChatService(retrieval_service, tool_service)

        # 设置路由的全局服务实例
        chat_router.chat_service = chat_service
        retrieve_router.retrieval_service = retrieval_service
        image_router.image_service = image_service

        logger.info("AI 服务初始化完成")
    except Exception as e:
        logger.error(f"AI 服务初始化失败: {str(e)}")
        raise

    yield

    # 关闭事件
    logger.info("关闭 AI 服务...")
    if chat_service:
        await chat_service.close()
    logger.info("AI 服务已关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title="AI 服务模块",
    description="种植周期管理系统 AI 服务，提供对话生成、向量检索、图像识别等功能",
    version="1.0.0",
    lifespan=lifespan
)

# 配置中间件
setup_cors_middleware(app)
app.middleware("http")(logging_middleware)
setup_exception_handlers(app)

# 注册路由
app.include_router(chat_router.router)
app.include_router(retrieve_router.router)
app.include_router(image_router.router)


# 健康检查接口
@app.get("/health")
async def health_check():
    """
    健康检查接口

    Returns:
        服务状态信息
    """
    return {
        "status": "healthy",
        "services": {
            "retrieval": retrieval_service is not None,
            "tool": tool_service is not None,
            "image": image_service is not None,
            "chat": chat_service is not None
        },
        "config": {
            "host": config.app.host,
            "port": config.app.port,
            "debug": config.app.debug
        }
    }


# 根路径
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI 服务模块",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.app.host,
        port=config.app.port,
        reload=config.app.debug
    )
