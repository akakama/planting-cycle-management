"""
Lightweight entry point for the image recognition service.

This starts only the MobileNetV3 diagnosis route, so image recognition can run
without loading the chat, retrieval, ChromaDB, or vLLM dependencies.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.image_recognition as image_router
from app.config import config
from app.models.services.image_service import ImageRecognitionService
from app.models.utils.middleware import (
    logging_middleware,
    setup_cors_middleware,
    setup_exception_handlers,
)
from app.models.utils.logger import logger

image_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global image_service

    logger.info("初始化图像识别服务...")
    image_service = ImageRecognitionService()
    image_router.image_service = image_service
    logger.info("图像识别服务初始化完成")

    yield

    logger.info("图像识别服务已关闭")


app = FastAPI(
    title="病虫害图片识别服务",
    description="MobileNetV3 image recognition service for planting-cycle-management",
    version="1.0.0",
    lifespan=lifespan,
)

setup_cors_middleware(app)
app.middleware("http")(logging_middleware)
setup_exception_handlers(app)
app.include_router(image_router.router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "image": image_service is not None,
            "model_loaded": bool(image_service and image_service.model is not None),
            "model_path": image_service.model_path if image_service else None,
        },
    }


@app.get("/")
async def root():
    return {
        "message": "病虫害图片识别服务",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "image_main:app",
        host=config.app.host,
        port=config.app.port,
        reload=config.app.debug,
    )
