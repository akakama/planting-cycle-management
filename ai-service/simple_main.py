"""
简化的AI服务 - 使用规则引擎替代复杂的机器学习模型
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import pymysql
from datetime import datetime

# 创建 FastAPI 应用
app = FastAPI(
    title="AI 服务模块 (简化版)",
    description="种植周期管理系统 AI 服务 - 基于规则引擎",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 农业知识库
AGRICULTURAL_KNOWLEDGE = {
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
"""
    }
}

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    conversation_id: Optional[str] = None

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'planting_db',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def get_current_planting_plans():
    """获取当前种植计划"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """
        SELECT 
            pp.id,
            c.name as crop_name,
            p.name as plot_name,
            pp.planting_date,
            pp.expected_harvest_date,
            pp.status,
            pp.remark
        FROM planting_plan pp
        LEFT JOIN crop c ON pp.crop_id = c.id
        LEFT JOIN plot p ON pp.plot_id = p.id
        ORDER BY pp.id
        """
        cursor.execute(sql)
        plans = cursor.fetchall()
        return plans
    except Exception as e:
        print(f"查询种植计划失败: {e}")
        return []
    finally:
        conn.close()

def get_phenology_records():
    """获取物候期记录"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """
        SELECT 
            pr.id,
            c.name as crop_name,
            p.name as plot_name,
            pr.phenology_name,
            pr.record_date,
            pr.description
        FROM phenology_record pr
        LEFT JOIN planting_plan pp ON pr.plan_id = pp.id
        LEFT JOIN crop c ON pp.crop_id = c.id
        LEFT JOIN plot p ON pp.plot_id = p.id
        ORDER BY pr.record_date DESC
        LIMIT 10
        """
        cursor.execute(sql)
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"查询物候期记录失败: {e}")
        return []
    finally:
        conn.close()

def format_planting_plans(plans):
    """格式化种植计划"""
    if not plans:
        return "当前没有种植计划数据。"
    
    result = "## 📋 当前种植计划\n\n"
    for plan in plans:
        status_emoji = {
            '进行中': '🔄',
            '未开始': '⏳',
            '已完成': '✅'
        }.get(plan['status'], '📌')
        
        result += f"**{plan['id']}. {plan['crop_name']} - {plan['plot_name']}**\n"
        result += f"- 状态：{status_emoji} {plan['status']}\n"
        result += f"- 播种日期：{plan['planting_date']}\n"
        result += f"- 预计收获：{plan['expected_harvest_date']}\n"
        if plan['remark']:
            result += f"- 备注：{plan['remark']}\n"
        result += "\n"
    
    return result

def format_phenology_records(records):
    """格式化物候期记录"""
    if not records:
        return "当前没有物候期记录数据。"
    
    result = "## 🌱 最近物候期记录\n\n"
    for record in records:
        result += f"**{record['crop_name']} - {record['plot_name']}**\n"
        result += f"- 物候期：{record['phenology_name']}\n"
        result += f"- 记录日期：{record['record_date']}\n"
        if record['description']:
            result += f"- 描述：{record['description'][:50]}...\n"
        result += "\n"
    
    return result

def get_agricultural_advice(message: str) -> str:
    """根据用户输入获取农业建议"""
    message_lower = message.lower()
    
    # 处理快捷问题
    if "当前种植计划" in message or "种植计划" in message:
        # 获取数据库中的种植计划
        plans = get_current_planting_plans()
        result = format_planting_plans(plans)
        
        # 添加AI生成的建议
        result += "\n---\n\n"
        result += "## 💡 AI种植建议\n\n"
        result += "根据当前种植计划，建议关注以下几点：\n\n"
        result += "1. **及时跟踪物候期**：定期记录作物生长阶段，便于科学管理\n"
        result += "2. **关注天气变化**：根据天气预报调整农事安排\n"
        result += "3. **加强田间管理**：注意水肥管理，及时除草防虫\n"
        result += "4. **做好采收准备**：提前安排采收工具和销售渠道\n"
        
        return result
    
    if "病虫害情况" in message or "病虫害" in message:
        # 获取物候期记录
        records = get_phenology_records()
        result = format_phenology_records(records)
        
        # 添加病虫害防治建议
        result += "\n---\n\n"
        result += "## 🐛 病虫害防治建议\n\n"
        result += "当前季节需要重点防治以下病虫害：\n\n"
        result += "**小麦**：\n"
        result += "- 蚜虫：使用吡虫啉或啶虫脒防治\n"
        result += "- 锈病：喷施三唑酮或戊唑醇\n\n"
        result += "**玉米**：\n"
        result += "- 玉米螟：释放赤眼蜂或喷施氯虫苯甲酰胺\n"
        result += "- 大斑病：喷施苯醚甲环唑\n\n"
        result += "**水稻**：\n"
        result += "- 稻飞虱：喷施吡蚜酮\n"
        result += "- 纹枯病：喷施井冈霉素\n"
        
        return result
    
    if "种植建议" in message:
        # 获取种植计划
        plans = get_current_planting_plans()
        result = "## 🌾 种植建议\n\n"
        
        if plans:
            result += "根据当前种植计划，为您提供以下建议：\n\n"
            
            # 按作物类型分组
            crop_plans = {}
            for plan in plans:
                crop_name = plan['crop_name']
                if crop_name not in crop_plans:
                    crop_plans[crop_name] = []
                crop_plans[crop_name].append(plan)
            
            for crop_name, crop_plan_list in crop_plans.items():
                result += f"### {crop_name}\n\n"
                if crop_name in AGRICULTURAL_KNOWLEDGE:
                    # 获取知识库中的种植建议
                    advice = AGRICULTURAL_KNOWLEDGE[crop_name]["种植建议"]
                    # 提取关键信息
                    lines = advice.split('\n')
                    key_points = []
                    for line in lines:
                        if line.strip() and (line.strip().startswith('1.') or line.strip().startswith('2.') or line.strip().startswith('3.')):
                            key_points.append(line.strip())
                    result += '\n'.join(key_points[:3]) + "\n\n"
                else:
                    result += "- 选择优良品种，合理密植\n"
                    result += "- 科学施肥，适时灌溉\n"
                    result += "- 加强田间管理，及时防治病虫害\n\n"
        else:
            result += "当前没有种植计划，建议先制定种植计划。\n\n"
        
        result += "---\n\n"
        result += "## 📌 通用建议\n\n"
        result += "1. **品种选择**：选择适合当地气候和土壤的优良品种\n"
        result += "2. **适时播种**：根据作物特性和气候条件确定最佳播种期\n"
        result += "3. **科学管理**：合理施肥、灌溉，加强病虫害防治\n"
        result += "4. **及时采收**：关注作物成熟度，适时采收确保品质\n"
        
        return result
    
    # 检查是否询问具体问题（品种选择、播种时间、土壤准备等）
    specific_keywords = ["品种选择", "播种时间", "土壤准备", "播种技术", "田间管理", "收获时机", "注意事项"]
    for keyword in specific_keywords:
        if keyword in message:
            # 检查是否询问特定作物
            for crop, knowledge in AGRICULTURAL_KNOWLEDGE.items():
                if crop in message:
                    # 提取该作物的种植建议
                    advice = knowledge["种植建议"]
                    lines = advice.split('\n')
                    
                    # 查找并提取相关段落
                    result_lines = []
                    in_section = False
                    section_num = None
                    
                    for i, line in enumerate(lines):
                        # 检查是否是目标章节的开始
                        if keyword in line and (line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.'))):
                            in_section = True
                            section_num = line.strip()[0]
                            result_lines.append(line)
                        # 如果在目标章节内，继续添加内容
                        elif in_section:
                            # 检查是否到了下一个章节（遇到下一个数字编号）
                            if line.strip() and line.strip()[0].isdigit() and line.strip()[0] != section_num:
                                in_section = False
                            else:
                                result_lines.append(line)
                    
                    if result_lines:
                        return f"## {crop} - {keyword}\n\n" + '\n'.join(result_lines)
                    else:
                        return f"未找到{crop}关于{keyword}的具体信息。"
            
            # 如果没有指定作物，返回通用建议
            return f"请指定具体的作物名称，例如：'小麦{keyword}'或'玉米{keyword}'"
    
    # 检查是否询问特定作物的种植建议
    for crop, knowledge in AGRICULTURAL_KNOWLEDGE.items():
        if crop in message:
            return knowledge["种植建议"]
    
    # 检查是否询问病虫害防治
    if "防治" in message:
        for crop, knowledge in AGRICULTURAL_KNOWLEDGE.items():
            if crop in message:
                return knowledge.get("病虫害", "关于病虫害防治，请提供更具体的作物名称。")
    
    # 通用农业建议
    return """
您好！我是农业种植助手，可以为您提供以下作物的种植建议：

🌽 **玉米** - 适合春季和夏季种植，需充足阳光和水分
🌾 **小麦** - 分冬小麦和春小麦，是重要的粮食作物
🌾 **水稻** - 需要充足的水源，适合水田种植
🌱 **大豆** - 蛋白质含量高，可与玉米间作
🥔 **马铃薯** - 喜凉爽气候，对土壤要求疏松

请告诉我您想了解哪种作物的种植信息，或者有什么具体的农业问题需要咨询？

例如：
- "今年种玉米有什么建议"
- "小麦病虫害如何防治"
- "水稻种植技术"
"""

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
        
        for msg in messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        # 如果没有找到用户消息，尝试使用旧格式
        if not user_message and "message" in request:
            user_message = request["message"]
        
        # 获取农业建议
        reply = get_agricultural_advice(user_message)
        
        # 返回OpenAI格式响应
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": reply
                    }
                }
            ]
        }
    except Exception as e:
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": f"抱歉，处理您的请求时出现错误：{str(e)}"
                    }
                }
            ]
        }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "simplified_ai_service",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI 服务模块 (简化版)",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)