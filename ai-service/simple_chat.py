"""
简化的AI聊天服务
模拟千问(Qwen2.5-7B)的响应,用于测试
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time
import uuid
import re

app = FastAPI(title="简化AI服务", version="1.0.0")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "qwen2.5-7b"
    messages: List[Message]
    temperature: float = 0.7
    max_tokens: int = 2048


class ChatCompletionMessage(BaseModel):
    role: str
    content: str


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatCompletionMessage
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Usage


def generate_ai_response(message: str) -> str:
    """
    生成AI回复 (模拟千问的响应)
    """
    message = message.lower()
    
    # 作物种植相关
    if "小麦" in message and ("怎么种" in message or "如何" in message or "种植" in message):
        return ("小麦种植要点：\n"
                "1. 播种时间：一般在9月下旬至10月上旬播种\n"
                "2. 土壤要求：选择土层深厚、肥沃、排水良好的土壤\n"
                "3. 施肥：基肥充足，追肥适时，注意氮磷钾配比\n"
                "4. 灌溉：保持土壤湿润，避免积水\n"
                "5. 病虫害防治：注意防治锈病、白粉病、蚜虫等\n"
                "6. 采收：一般在次年5-6月成熟，适时采收")
    
    elif "玉米" in message and ("怎么种" in message or "如何" in message or "种植" in message):
        return ("玉米种植要点：\n"
                "1. 播种时间：春季4-5月播种\n"
                "2. 土壤要求：选择肥沃、疏松、排水良好的土壤\n"
                "3. 施肥：重施基肥，及时追肥\n"
                "4. 密度：合理密植，一般每亩3500-4000株\n"
                "5. 病虫害防治：注意防治玉米螟、大斑病等\n"
                "6. 采收：一般在秋季9-10月成熟")
    
    elif "水稻" in message and ("怎么种" in message or "如何" in message or "种植" in message):
        return ("水稻种植要点：\n"
                "1. 育秧：选择适宜品种，培育壮秧\n"
                "2. 插秧：适时插秧，合理密植\n"
                "3. 水分管理：浅水插秧，深水返青，浅水分蘖\n"
                "4. 施肥：基肥、分蘖肥、穗肥分期施用\n"
                "5. 病虫害防治：注意防治稻瘟病、纹枯病、二化螟等\n"
                "6. 采收：一般在秋季成熟")
    
    # 病虫害防治相关
    elif "病虫害" in message or "防治" in message:
        return ("病虫害综合防治措施：\n"
                "1. 农业防治：选用抗病品种，合理轮作，清洁田园\n"
                "2. 生物防治：保护和利用天敌，使用生物农药\n"
                "3. 物理防治：灯光诱杀，色板诱杀\n"
                "4. 化学防治：科学使用农药，交替用药，避免抗药性\n"
                "5. 预防为主：加强田间管理，提高作物抗性")
    
    # 施肥相关
    elif "施肥" in message:
        return ("科学施肥原则：\n"
                "1. 基肥足：播种前施足基肥，保证作物前期生长\n"
                "2. 追肥适时：根据作物生长阶段及时追肥\n"
                "3. 氮磷钾配比：合理搭配氮、磷、钾肥\n"
                "4. 有机无机结合：有机肥与化肥配合使用\n"
                "5. 因地制宜：根据土壤肥力和作物需要调整施肥量")
    
    # 灌溉相关
    elif "灌溉" in message or "浇水" in message:
        return ("科学灌溉原则：\n"
                "1. 少量多次：避免大水漫灌，采用小水勤浇\n"
                "2. 见干见湿：土壤表面干燥后再浇\n"
                "3. 适时灌溉：根据作物需水规律和天气情况\n"
                "4. 节水灌溉：采用滴灌、喷灌等节水技术\n"
                "5. 避免积水：雨后及时排水，防止渍害")
    
    # 采收相关
    elif "采收" in message or "收获" in message:
        return ("采收要点：\n"
                "1. 适时采收：根据作物成熟度确定采收时间\n"
                "2. 选择天气：晴天采收，避免雨天\n"
                "3. 方法正确：采用正确的采收方法，避免损伤\n"
                "4. 及时处理：采收后及时晾晒或冷藏\n"
                "5. 质量分级：按质量标准进行分级包装")
    
    # 价格相关
    elif "价格" in message or "多少钱" in message:
        return "农产品价格查询功能正在开发中，敬请期待！"
    
    # 天气相关
    elif "天气" in message or "气温" in message:
        return "天气查询功能正在开发中，敬请期待！"
    
    # 默认回答
    else:
        return ("您好！我是智能种植助手，可以帮您解答关于：\n"
                "• 作物种植技术（小麦、玉米、水稻等）\n"
                "• 病虫害防治方法\n"
                "• 科学施肥技巧\n"
                "• 灌溉管理要点\n"
                "• 采收注意事项\n\n"
                "请问您想了解哪方面的内容？")


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    对话生成接口
    """
    try:
        # 获取用户消息
        user_message = ""
        for msg in request.messages:
            if msg.role == "user":
                user_message = msg.content
                break
        
        # 生成AI回复
        response_text = generate_ai_response(user_message)
        
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
                prompt_tokens=len(user_message),
                completion_tokens=len(response_text),
                total_tokens=len(user_message) + len(response_text)
            )
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话生成失败: {str(e)}")


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "简化AI服务",
        "model": "模拟千问(Qwen2.5-7B)"
    }


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "简化AI服务",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
