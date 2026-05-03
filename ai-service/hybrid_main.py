"""
混合AI服务 - 规则引擎 + API调用 + 安全护栏
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import httpx
import json
import re

# 创建 FastAPI 应用
app = FastAPI(
    title="AI 服务模块 (混合版)",
    description="种植周期管理系统 AI 服务 - 规则引擎+API+安全护栏",
    version="2.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 安全护栏规则 ====================
SAFETY_RULES = {
    "forbidden_topics": [
        "政治", "暴力", "色情", "赌博", "毒品", "恐怖主义",
        "违法", "犯罪", "欺诈", "诈骗"
    ],
    "forbidden_keywords": [
        "制造武器", "炸弹", "毒药", "赌博", "诈骗"
    ],
    "max_response_length": 5000,
    "allowed_response_patterns": [
        r"种植|建议|农业|作物|病虫害|施肥|灌溉|收获"
    ]
}

def check_safety(message: str) -> tuple[bool, str]:
    """
    安全检查 - 规则引擎作为安全护栏
    
    Args:
        message: 用户输入的消息
        
    Returns:
        (is_safe, reason): 是否安全及原因
    """
    message_lower = message.lower()
    
    # 检查禁止话题
    for topic in SAFETY_RULES["forbidden_topics"]:
        if topic in message_lower:
            return False, f"抱歉，我不能回答关于{topic}的问题。"
    
    # 检查禁止关键词
    for keyword in SAFETY_RULES["forbidden_keywords"]:
        if keyword in message_lower:
            return False, "抱歉，您的问题包含敏感内容。"
    
    # 检查是否为农业相关
    is_agriculture_related = any(
        pattern in message_lower 
        for pattern in ["种植", "农业", "作物", "玉米", "小麦", "水稻", 
                        "病虫害", "施肥", "灌溉", "收获", "农场"]
    )
    
    if not is_agriculture_related and len(message) > 10:
        return False, "我是农业种植助手，只能回答农业相关的问题。"
    
    return True, ""

def sanitize_response(response: str) -> str:
    """
    清理响应内容 - 确保输出安全
    
    Args:
        response: 原始响应
        
    Returns:
        清理后的响应
    """
    # 检查响应长度
    if len(response) > SAFETY_RULES["max_response_length"]:
        response = response[:SAFETY_RULES["max_response_length"]] + "\n\n(回答过长，已截断)"
    
    # 检查是否包含禁止内容
    for keyword in SAFETY_RULES["forbidden_keywords"]:
        if keyword in response.lower():
            response = re.sub(keyword, "***", response, flags=re.IGNORECASE)
    
    return response

# ==================== 规则引擎 - 处理常见问题 ====================
RULES_ENGINE = {
    "玉米": {
        "种植建议": """
玉米种植建议：

1. 品种选择
   - 推荐品种：郑单958、先玉335、登海605等
   - 选择原则：根据当地气候、土壤条件选择适合的品种
   - 注意事项：选择抗病虫害能力强、适应性广的品种

2. 播种时间
   - 春播：4月中下旬至5月上旬
   - 夏播：6月上中旬
   - 土壤温度：地温稳定在10℃以上时播种

3. 土壤准备
   - 深翻整地：深度25-30cm，打破犁底层
   - 施足基肥：每亩施有机肥2000-3000kg，复合肥50kg
   - 土壤pH值：保持在6.5-7.5之间

4. 播种技术
   - 播种深度：4-5cm
   - 行距：60-70cm
   - 株距：25-30cm
   - 播种量：每亩2.5-3kg

5. 田间管理
   - 间苗定苗：3-4叶期间苗，5-6叶期定苗
   - 中耕除草：苗期中耕2-3次，保持土壤疏松
   - 追肥：拔节期追施尿素15-20kg/亩
   - 灌溉：关键时期保证水分供应

6. 病虫害防治
   - 主要病害：玉米大斑病、小斑病、丝黑穗病
   - 主要虫害：玉米螟、蚜虫、粘虫
   - 防治方法：采用综合防治，优先使用生物防治

7. 收获时机
   - 成熟标志：籽粒乳线消失，基部出现黑色层
   - 收获时间：一般在9月中下旬
   - 晾晒贮藏：水分降至13%以下安全贮藏

8. 注意事项
   - 关注天气预报，合理安排农事
   - 加强田间巡查，及时发现问题
   - 采用科学种植技术，提高产量和品质
""",
        "病虫害": """
玉米主要病虫害防治：

1. 玉米螟
   - 症状：幼虫蛀食茎秆、雌穗、雄穗
   - 防治：生物防治（赤眼蜂）、化学防治（氯虫苯甲酰胺）

2. 大斑病
   - 症状：叶片出现大型梭形病斑
   - 防治：选用抗病品种、药剂防治（苯醚甲环唑）

3. 小斑病
   - 症状：叶片出现小型椭圆形病斑
   - 防治：轮作倒茬、药剂防治（代森锰锌）

4. 丝黑穗病
   - 症状：果穗变成黑粉
   - 防治：选用抗病品种、种子处理
""",
        "施肥": """
玉米施肥建议：

1. 基肥
   - 有机肥：2000-3000kg/亩
   - 复合肥：50kg/亩
   - 施用时间：播种前施入

2. 追肥
   - 拔节肥：尿素15-20kg/亩
   - 穗肥：尿素10kg/亩 + 磷酸二氢钾5kg/亩
   - 施用时间：拔节期和大喇叭口期

3. 注意事项
   - 根据土壤肥力调整施肥量
   - 注意氮磷钾配比
   - 避免过量施肥造成环境污染
"""
    },
    "小麦": {
        "种植建议": """
小麦种植建议：

1. 品种选择
   - 推荐品种：济麦22、烟农19、鲁麦21等
   - 选择原则：根据种植季节选择冬小麦或春小麦品种

2. 播种时间
   - 冬小麦：9月下旬至10月中旬
   - 春小麦：3月中下旬至4月上旬

3. 土壤准备
   - 深翻整地，施足基肥
   - 每亩施有机肥3000kg，复合肥50kg

4. 播种技术
   - 播种深度：3-4cm
   - 行距：15-20cm
   - 播种量：每亩10-15kg

5. 田间管理
   - 冬前管理：浇好越冬水
   - 春季管理：追施返青肥、拔节肥
   - 后期管理：防治病虫害、适时收获

6. 病虫害防治
   - 主要病害：条锈病、白粉病、赤霉病
   - 主要虫害：蚜虫、麦蜘蛛
   - 防治方法：综合防治，科学用药
""",
        "病虫害": """
小麦主要病虫害防治：

1. 条锈病
   - 症状：叶片出现黄色条状病斑
   - 防治：选用抗病品种、药剂防治（三唑类）

2. 白粉病
   - 症状：叶片出现白色粉状物
   - 防治：药剂防治（戊唑醇）

3. 赤霉病
   - 症状：穗部出现粉红色霉层
   - 防治：选用抗病品种、药剂防治（多菌灵）

4. 蚜虫
   - 症状：吸食汁液，传播病毒
   - 防治：生物防治、化学防治（吡虫啉）
"""
    },
    "水稻": {
        "种植建议": """
水稻种植建议：

1. 品种选择
   - 推荐品种：杂交水稻、常规粳稻等
   - 选择原则：根据当地气候和种植制度选择

2. 育秧技术
   - 播种时间：根据品种和当地气候确定
   - 秧田管理：科学施肥、合理灌溉

3. 移栽技术
   - 移栽时间：秧龄30-35天
   - 栽插密度：根据品种确定

4. 田间管理
   - 水分管理：浅水栽秧、深水护苗
   - 肥料管理：分蘖肥、穗肥、粒肥
   - 病虫害防治：稻瘟病、纹枯病、稻飞虱等

5. 收获
   - 适时收获：黄熟期收获
   - 晾晒贮藏：水分降至14%以下
""",
        "病虫害": """
水稻主要病虫害防治：

1. 稻瘟病
   - 症状：叶片出现褐色斑点
   - 防治：选用抗病品种、药剂防治（三环唑）

2. 纹枯病
   - 症状：茎秆出现褐色病斑
   - 防治：科学灌溉、药剂防治（井冈霉素）

3. 稻飞虱
   - 症状：吸食汁液，传播病毒
   - 防治：生物防治、化学防治（噻虫嗪）
"""
    },
    "大豆": {
        "种植建议": """
大豆种植建议：

1. 品种选择
   - 推荐品种：黑农44、合丰25等
   - 选择原则：根据当地生态条件选择

2. 播种时间
   - 春播：4月下旬至5月上旬
   - 夏播：6月上中旬

3. 播种技术
   - 播种深度：3-4cm
   - 行距：50-60cm
   - 播种量：每亩4-6kg

4. 田间管理
   - 间苗定苗：2-3真叶期间苗
   - 中耕除草：苗期中耕2-3次
   - 追肥：开花期追施磷钾肥

5. 病虫害防治
   - 主要病害：根腐病、霜霉病
   - 主要虫害：大豆食心虫、蚜虫
   - 防治方法：综合防治
""",
        "病虫害": """
大豆主要病虫害防治：

1. 根腐病
   - 症状：根部腐烂，植株萎蔫
   - 防治：轮作倒茬、种子处理

2. 霜霉病
   - 症状：叶片出现不规则病斑
   - 防治：药剂防治（甲霜灵）

3. 大豆食心虫
   - 症状：幼虫蛀食豆荚
   - 防治：性诱剂诱杀、药剂防治
"""
    },
    "马铃薯": {
        "种植建议": """
马铃薯种植建议：

1. 品种选择
   - 推荐品种：费乌瑞它、大西洋等
   - 选择原则：根据用途和当地条件选择

2. 种薯处理
   - 催芽：播种前15-20天催芽
   - 切块：每块带1-2个芽眼

3. 播种技术
   - 播种时间：春季3-4月，秋季8-9月
   - 播种深度：10-15cm
   - 行距：70cm，株距：25cm

4. 田间管理
   - 中耕培土：苗期培土2-3次
   - 追肥：现蕾期追施钾肥
   - 病虫害防治：晚疫病、蚜虫等

5. 收获贮藏
   - 收获时间：植株枯黄时收获
   - 贮藏条件：温度2-4℃，湿度85-90%
""",
        "病虫害": """
马铃薯主要病虫害防治：

1. 晚疫病
   - 症状：叶片出现褐色斑点
   - 防治：选用抗病品种、药剂防治（甲霜灵）

2. 病毒病
   - 症状：叶片出现花叶、皱缩
   - 防治：选用无毒种薯、防治传毒媒介

3. 蚜虫
   - 症状：吸食汁液，传播病毒
   - 防治：生物防治、化学防治
"""
    }
}

def check_rules_engine(message: str) -> tuple[bool, str]:
    """
    检查规则引擎是否能处理该问题
    
    Args:
        message: 用户输入
        
    Returns:
        (can_handle, response): 是否能处理及响应内容
    """
    message_lower = message.lower()
    
    # 检查是否询问特定作物
    for crop, knowledge in RULES_ENGINE.items():
        if crop in message:
            # 检查具体问题类型
            if "种植" in message or "建议" in message:
                return True, knowledge["种植建议"]
            elif "病虫害" in message or "防治" in message:
                return True, knowledge.get("病虫害", knowledge["种植建议"])
            elif "施肥" in message:
                return True, knowledge.get("施肥", knowledge["种植建议"])
            else:
                return True, knowledge["种植建议"]
    
    # 通用农业问题
    if any(keyword in message_lower for keyword in ["你好", "帮助", "能做什么"]):
        return True, """
您好！我是农业种植助手，可以为您提供以下作物的种植建议：

🌽 **玉米** - 适合春季和夏季种植，需充足阳光和水分
🌾 **小麦** - 分冬小麦和春小麦，是重要的粮食作物
🌾 **水稻** - 需要充足的水源，适合水田种植
🌱 **大豆** - 蛋白质含量高，可与玉米间作
🥔 **马铃薯** - 喜凉爽气候，对土壤要求疏松

我可以帮您解答以下问题：
- 某种作物的种植建议
- 病虫害防治方法
- 施肥技术
- 收获时机

请告诉我您想了解什么？
"""
    
    return False, ""

# ==================== API配置 ====================
API_CONFIG = {
    "openai": {
        "enabled": False,
        "api_key": "",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-3.5-turbo"
    },
    "deepseek": {
        "enabled": False,
        "api_key": "",
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat"
    },
    "qwen": {
        "enabled": False,
        "api_key": "",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-turbo"
    }
}

async def call_api(message: str, conversation_history: List[Dict] = None) -> str:
    """
    调用外部API处理复杂问题
    
    Args:
        message: 用户消息
        conversation_history: 对话历史
        
    Returns:
        API响应内容
    """
    # 查找可用的API
    available_api = None
    for api_name, config in API_CONFIG.items():
        if config["enabled"] and config["api_key"]:
            available_api = api_name
            break
    
    if not available_api:
        return None
    
    config = API_CONFIG[available_api]
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 构建请求
            messages = []
            
            # 添加系统提示
            system_prompt = """你是专业的农业种植助手，专门帮助农民解决种植过程中的各种问题。
请用简洁、准确、实用的语言回答用户的问题。
如果不确定答案，请诚实地说明，不要编造信息。
回答应该基于农业科学知识，提供实用的建议。"""
            
            messages.append({"role": "system", "content": system_prompt})
            
            # 添加对话历史
            if conversation_history:
                for msg in conversation_history:
                    messages.append(msg)
            
            # 添加当前用户消息
            messages.append({"role": "user", "content": message})
            
            # 调用API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config['api_key']}"
            }
            
            payload = {
                "model": config["model"],
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = await client.post(
                f"{config['base_url']}/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return None
                
    except Exception as e:
        print(f"API调用失败: {str(e)}")
        return None

# ==================== 请求和响应模型 ====================
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    messages: Optional[List[Dict]] = None

class ChatResponse(BaseModel):
    reply: str
    conversation_id: Optional[str] = None
    source: str  # 来源：rules_engine 或 api

# ==================== 主处理逻辑 ====================
async def process_message(message: str, conversation_history: List[Dict] = None) -> tuple[str, str]:
    """
    处理用户消息的主逻辑
    
    Args:
        message: 用户消息
        conversation_history: 对话历史
        
    Returns:
        (response, source): 响应内容和来源
    """
    # 1. 安全检查
    is_safe, safety_reason = check_safety(message)
    if not is_safe:
        return safety_reason, "safety_guard"
    
    # 2. 规则引擎检查
    can_handle, response = check_rules_engine(message)
    if can_handle:
        return sanitize_response(response), "rules_engine"
    
    # 3. 调用API处理复杂问题
    api_response = await call_api(message, conversation_history)
    if api_response:
        return sanitize_response(api_response), "api"
    
    # 4. 默认响应
    return """
抱歉，我暂时无法回答这个问题。您可以：

1. 询问具体作物的种植建议（如：玉米、小麦、水稻、大豆、马铃薯）
2. 咨询病虫害防治方法
3. 了解施肥技术
4. 询问收获时机

如果您的问题比较复杂，建议您：
- 将问题分解为具体的问题
- 提供更多的背景信息
- 联系专业的农业技术部门

我将继续学习更多农业知识，为您提供更好的服务！
""", "default"

# ==================== API端点 ====================
@app.post("/v1/chat/completions")
async def chat_completions(request: dict):
    """
    聊天完成接口 - 兼容OpenAI格式
    
    Args:
        request: 聊天请求（OpenAI格式）
        
    Returns:
        聊天响应（OpenAI格式）
    """
    try:
        # 从OpenAI格式请求中提取用户消息
        messages = request.get("messages", [])
        user_message = ""
        conversation_history = []
        
        for msg in messages:
            conversation_history.append(msg)
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
        
        # 如果没有找到用户消息，尝试使用旧格式
        if not user_message and "message" in request:
            user_message = request["message"]
        
        # 处理消息
        response, source = await process_message(user_message, conversation_history)
        
        # 返回OpenAI格式响应
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": response
                    },
                    "index": 0
                }
            ],
            "model": "hybrid-ai-service",
            "source": source
        }
    except Exception as e:
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": f"抱歉，处理您的请求时出现错误：{str(e)}"
                    },
                    "index": 0
                }
            ]
        }

@app.post("/config")
async def configure_api(config_data: dict):
    """
    配置API密钥
    
    Args:
        config_data: 配置数据
        
    Returns:
        配置结果
    """
    try:
        api_name = config_data.get("api_name")
        api_key = config_data.get("api_key")
        
        if api_name in API_CONFIG:
            # 更新配置
            if api_key:
                API_CONFIG[api_name]["enabled"] = True
                API_CONFIG[api_name]["api_key"] = api_key
            else:
                API_CONFIG[api_name]["enabled"] = False
                API_CONFIG[api_name]["api_key"] = ""
            
            return {
                "success": True,
                "message": f"{api_name} API配置已更新",
                "enabled": API_CONFIG[api_name]["enabled"]
            }
        else:
            return {
                "success": False,
                "message": f"不支持的API: {api_name}"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"配置失败: {str(e)}"
        }

@app.get("/config")
async def get_config():
    """
    获取当前配置
    
    Returns:
        当前配置信息
    """
    return {
        "api_config": {
            api_name: {
                "enabled": config["enabled"],
                "model": config["model"]
            }
            for api_name, config in API_CONFIG.items()
        },
        "safety_rules": {
            "forbidden_topics_count": len(SAFETY_RULES["forbidden_topics"]),
            "forbidden_keywords_count": len(SAFETY_RULES["forbidden_keywords"]),
            "max_response_length": SAFETY_RULES["max_response_length"]
        },
        "rules_engine": {
            "crops_count": len(RULES_ENGINE),
            "crops": list(RULES_ENGINE.keys())
        }
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "hybrid_ai_service",
        "version": "2.0.0",
        "features": {
            "rules_engine": True,
            "api_integration": any(config["enabled"] for config in API_CONFIG.values()),
            "safety_guard": True
        }
    }

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI 服务模块 (混合版)",
        "version": "2.0.0",
        "description": "规则引擎 + API调用 + 安全护栏",
        "docs": "/docs",
        "health": "/health",
        "config": "/config"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
