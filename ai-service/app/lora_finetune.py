"""
LoRA微调API接口
提供模型微调、适配器管理等功能
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from loguru import logger

from app.models.services.lora_service import (
    LoRAFineTuningService,
    create_sample_training_data
)

router = APIRouter(prefix="/lora", tags=["LoRA微调服务"])

# 全局LoRA服务实例
lora_service: Optional[LoRAFineTuningService] = None


class FineTuneRequest(BaseModel):
    """微调请求"""
    model_path: str
    data_path: str
    output_dir: str = "./lora_output"
    r: int = 8
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 4
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-4


class GenerateRequest(BaseModel):
    """生成请求"""
    prompt: str
    adapter_path: Optional[str] = None
    max_length: int = 512


class GenerateResponse(BaseModel):
    """生成响应"""
    success: bool
    generated_text: Optional[str] = None
    error: Optional[str] = None


class StatusResponse(BaseModel):
    """状态响应"""
    success: bool
    is_loaded: bool
    model_path: Optional[str] = None
    adapter_path: Optional[str] = None
    error: Optional[str] = None


@router.post("/finetune", response_model=dict)
async def start_finetune(request: FineTuneRequest, background_tasks: BackgroundTasks):
    """
    启动LoRA微调
    """
    try:
        logger.info(f"收到微调请求, 模型路径: {request.model_path}")

        # 在后台任务中执行微调
        def finetune_task():
            global lora_service

            try:
                # 初始化服务
                lora_service = LoRAFineTuningService(
                    model_path=request.model_path,
                    output_dir=request.output_dir
                )

                # 加载模型
                lora_service.load_model()

                # 准备LoRA模型
                lora_service.prepare_lora_model(
                    r=request.r,
                    lora_alpha=request.lora_alpha,
                    lora_dropout=request.lora_dropout
                )

                # 加载训练数据
                dataset = lora_service.load_training_data(request.data_path)

                # 预处理数据
                tokenized_dataset = lora_service.preprocess_data(dataset)

                # 训练模型
                lora_service.train(
                    dataset=tokenized_dataset,
                    num_train_epochs=request.num_train_epochs,
                    per_device_train_batch_size=request.per_device_train_batch_size,
                    gradient_accumulation_steps=request.gradient_accumulation_steps,
                    learning_rate=request.learning_rate
                )

                # 清理资源
                lora_service.cleanup()

                logger.info("微调任务完成")

            except Exception as e:
                logger.error(f"微调任务失败: {str(e)}")
                if lora_service:
                    lora_service.cleanup()

        # 添加后台任务
        background_tasks.add_task(finetune_task)

        return {
            "success": True,
            "message": "微调任务已启动,请在后台查看日志"
        }

    except Exception as e:
        logger.error(f"启动微调失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    使用微调后的模型生成文本
    """
    global lora_service

    try:
        logger.info(f"收到生成请求, 提示词: {request.prompt}")

        # 如果需要加载适配器
        if request.adapter_path and (lora_service is None or not hasattr(lora_service, 'lora_model')):
            lora_service = LoRAFineTuningService(model_path="./models/Qwen2.5-7B-Instruct")
            lora_service.load_model()
            lora_service.load_lora_adapter(request.adapter_path)

        # 生成文本
        if lora_service is None or lora_service.lora_model is None:
            return GenerateResponse(
                success=False,
                error="请先训练或加载LoRA模型"
            )

        generated_text = lora_service.generate_text(
            prompt=request.prompt,
            max_length=request.max_length
        )

        return GenerateResponse(
            success=True,
            generated_text=generated_text
        )

    except Exception as e:
        logger.error(f"生成文本失败: {str(e)}")
        return GenerateResponse(
            success=False,
            error=str(e)
        )


@router.get("/status", response_model=StatusResponse)
async def get_status():
    """
    获取LoRA服务状态
    """
    global lora_service

    try:
        is_loaded = lora_service is not None and lora_service.lora_model is not None

        return StatusResponse(
            success=True,
            is_loaded=is_loaded,
            model_path=lora_service.model_path if lora_service else None
        )

    except Exception as e:
        logger.error(f"获取状态失败: {str(e)}")
        return StatusResponse(
            success=False,
            error=str(e)
        )


@router.post("/create-sample-data", response_model=dict)
async def create_sample_data():
    """
    创建示例训练数据
    """
    try:
        create_sample_training_data("./agriculture_training_data.json")

        return {
            "success": True,
            "message": "示例训练数据已创建",
            "data_path": "./agriculture_training_data.json"
        }

    except Exception as e:
        logger.error(f"创建示例数据失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/load-adapter", response_model=dict)
async def load_adapter(adapter_path: str):
    """
    加载LoRA适配器
    """
    global lora_service

    try:
        logger.info(f"正在加载LoRA适配器: {adapter_path}")

        if lora_service is None:
            lora_service = LoRAFineTuningService(model_path="./models/Qwen2.5-7B-Instruct")
            lora_service.load_model()

        lora_service.load_lora_adapter(adapter_path)

        return {
            "success": True,
            "message": "LoRA适配器加载成功"
        }

    except Exception as e:
        logger.error(f"加载适配器失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/merge-weights", response_model=dict)
async def merge_weights():
    """
    合并LoRA权重
    """
    global lora_service

    try:
        if lora_service is None or lora_service.lora_model is None:
            raise HTTPException(status_code=400, detail="请先加载LoRA模型")

        logger.info("正在合并LoRA权重...")
        merged_model = lora_service.merge_lora_weights()

        # 保存合并后的模型
        output_path = "./merged_model"
        merged_model.save_pretrained(output_path)
        lora_service.tokenizer.save_pretrained(output_path)

        return {
            "success": True,
            "message": "LoRA权重合并成功",
            "output_path": output_path
        }

    except Exception as e:
        logger.error(f"合并权重失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cleanup", response_model=dict)
async def cleanup():
    """
    清理资源
    """
    global lora_service

    try:
        if lora_service is not None:
            lora_service.cleanup()
            lora_service = None

        return {
            "success": True,
            "message": "资源清理完成"
        }

    except Exception as e:
        logger.error(f"清理资源失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
