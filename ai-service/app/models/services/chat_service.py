"""
对话服务
整合检索服务和工具调用服务，调用 vLLM 生成回答
"""
from typing import List
import httpx
from app.models.schemas.chat import Message
from app.models.services.retrieval_service import RetrievalService
from app.models.services.tool_service import ToolCallService
from app.tools.data_query import DataQueryTool
from app.config import config


class ChatService:
    """对话服务类"""

    def __init__(self, retrieval_service: RetrievalService, tool_service: ToolCallService):
        """
        初始化对话服务

        Args:
            retrieval_service: 检索服务实例
            tool_service: 工具调用服务实例
        """
        self.retrieval_service = retrieval_service
        self.tool_service = tool_service
        self.client = httpx.AsyncClient(timeout=30.0)
        
        # 初始化智能数据查询工具
        self.data_query = DataQueryTool(config.tools.backend_url)
        
        print("对话服务初始化成功")

    async def generate_response(self, messages: List[Message], temperature: float = 0.4, max_tokens: int = 4096) -> str:
        """
        生成对话响应

        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大生成 token 数

        Returns:
            生成的回答文本
        """
        try:
            # 获取用户问题
            user_message = messages[-1].content

            # 优先使用智能数据查询工具
            data_result = await self.data_query.query(user_message)
            if data_result and data_result.get("success"):
                return self._format_data_result(data_result)

            # 然后检查是否需要工具调用
            tool_results = await self._check_and_call_tools(user_message)

            # 如果有种植计划查询结果、价格查询结果或天气查询结果，直接返回，不经过大模型
            if tool_results:
                if "【种植计划查询结果】" in tool_results:
                    # 如果有种植计划，直接返回；如果没有，需要经过大模型使用知识库制定计划
                    if "找到" in tool_results and "个" in tool_results and "的种植计划" in tool_results:
                        # 有种植计划，直接返回
                        return tool_results
                    else:
                        # 没有种植计划，需要经过大模型
                        pass
                elif "【农产品价格查询结果】" in tool_results or "【天气查询结果】" in tool_results:
                    # 直接返回工具查询结果
                    return tool_results

            # 判断是否需要检索知识库
            should_retrieve = True

            # 知识检索
            context = ""
            if should_retrieve:
                retrieved_docs = await self.retrieval_service.search_documents(user_message, top_k=8)
                context = self._build_context(retrieved_docs)

            # 构建请求消息
            request_messages = self._build_request_messages(messages, context, tool_results)

            # 调用 vLLM
            response = await self._call_vllm(request_messages, temperature, max_tokens)

            # 提取回答
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception("vLLM 返回格式错误")

        except httpx.TimeoutException:
            raise Exception("vLLM 请求超时")
        except httpx.HTTPStatusError as e:
            raise Exception(f"vLLM 请求失败: {e.response.status_code}")
        except Exception as e:
            print(f"模型推理失败: {str(e)}")
            raise Exception(f"模型推理失败: {str(e)}")

    def _build_context(self, documents: List) -> str:
        """
        构建知识库上下文

        Args:
            documents: 检索到的文档列表

        Returns:
            上下文字符串
        """
        if not documents:
            return ""

        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"【参考资料 {i}】\n{doc.content}")

        return "\n\n".join(context_parts)

    def _format_data_result(self, data_result: dict) -> str:
        """
        格式化数据查询结果
        
        Args:
            data_result: 数据查询结果
            
        Returns:
            格式化后的字符串
        """
        result_type = data_result.get("type")
        data = data_result.get("data", {})
        
        if result_type == "today_tasks":
            return self._format_today_tasks(data)
        elif result_type == "calendar_start":
            return self._format_calendar_start(data)
        elif result_type == "planting_plans":
            return self._format_planting_plans(data)
        elif result_type == "plots":
            return self._format_plots(data)
        elif result_type == "date_range_tasks":
            return self._format_date_range_tasks(data)
        elif result_type == "status_tasks":
            return self._format_status_tasks(data)
        else:
            return data_result.get("message", "查询成功")
    
    def _format_today_tasks(self, data: dict) -> str:
        """格式化今天的任务"""
        lines = [f"📅 今天（{data.get('date')}）的种植任务："]
        plans = data.get("plans", [])
        
        if not plans:
            lines.append("今天没有种植任务安排。")
        else:
            lines.append(f"共有 {data.get('total', 0)} 个任务：\n")
            for i, plan in enumerate(plans, 1):
                lines.append(f"{i}. 种植日期：{plan.get('plantingDate', 'N/A')}")
                lines.append(f"   预计收获：{plan.get('expectedHarvestDate', 'N/A')}")
                lines.append(f"   状态：{plan.get('status', 'N/A')}")
                if plan.get('remark'):
                    lines.append(f"   备注：{plan.get('remark')}")
                lines.append("")
        
        return "\n".join(lines)
    
    def _format_calendar_start(self, data: dict) -> str:
        """格式化种植日历开始时间"""
        return f"📆 种植日历从 {data.get('start_date')} 开始，目前共有 {data.get('total_plans', 0)} 个种植计划。"
    
    def _format_planting_plans(self, data: dict) -> str:
        """格式化种植计划"""
        crop = data.get("crop")
        status = data.get("status")
        plans = data.get("plans", [])
        
        lines = [f"🌱 {crop}的种植计划："]
        if status:
            lines[0] = f"🌱 {crop}（{status}）的种植计划："
        
        if not plans:
            lines.append(f"未找到{crop}的种植计划。")
        else:
            lines.append(f"共找到 {data.get('total', 0)} 个计划：\n")
            for i, plan in enumerate(plans, 1):
                lines.append(f"{i}. 种植日期：{plan.get('plantingDate', 'N/A')}")
                lines.append(f"   预计收获：{plan.get('expectedHarvestDate', 'N/A')}")
                lines.append(f"   状态：{plan.get('status', 'N/A')}")
                if plan.get('remark'):
                    lines.append(f"   备注：{plan.get('remark')}")
                lines.append("")
        
        return "\n".join(lines)
    
    def _format_plots(self, data: dict) -> str:
        """格式化地块信息"""
        plots = data.get("plots", [])
        
        lines = [f"🗺️ 地块信息："]
        lines.append(f"共有 {data.get('total', 0)} 个地块：\n")
        
        for i, plot in enumerate(plots[:10], 1):  # 只显示前10个
            lines.append(f"{i}. {plot.get('name', 'N/A')}（{plot.get('code', 'N/A')}）")
            lines.append(f"   面积：{plot.get('area', 'N/A')} 平方米")
            lines.append(f"   位置：{plot.get('location', 'N/A')}")
            lines.append(f"   土壤类型：{plot.get('soilType', 'N/A')}")
            if plot.get('remark'):
                lines.append(f"   备注：{plot.get('remark')}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_date_range_tasks(self, data: dict) -> str:
        """格式化日期范围任务"""
        date_range = data.get("date_range", {})
        plans = data.get("plans", [])
        
        lines = [f"📅 {date_range.get('startDate')} 至 {date_range.get('endDate')} 的种植任务："]
        
        if not plans:
            lines.append("该时间段没有种植任务。")
        else:
            lines.append(f"共有 {data.get('total', 0)} 个任务：\n")
            for i, plan in enumerate(plans, 1):
                lines.append(f"{i}. 种植日期：{plan.get('plantingDate', 'N/A')}")
                lines.append(f"   状态：{plan.get('status', 'N/A')}")
                if plan.get('remark'):
                    lines.append(f"   备注：{plan.get('remark')}")
                lines.append("")
        
        return "\n".join(lines)
    
    def _format_status_tasks(self, data: dict) -> str:
        """格式化状态任务"""
        status = data.get("status")
        plans = data.get("plans", [])
        
        lines = [f"📋 {status}的种植任务："]
        
        if not plans:
            lines.append(f"没有{status}的任务。")
        else:
            lines.append(f"共有 {data.get('total', 0)} 个任务：\n")
            for i, plan in enumerate(plans, 1):
                lines.append(f"{i}. 种植日期：{plan.get('plantingDate', 'N/A')}")
                lines.append(f"   预计收获：{plan.get('expectedHarvestDate', 'N/A')}")
                if plan.get('remark'):
                    lines.append(f"   备注：{plan.get('remark')}")
                lines.append("")
        
        return "\n".join(lines)

    async def _check_and_call_tools(self, message: str) -> str:
        """
        检查并调用工具

        Args:
            message: 用户消息

        Returns:
            工具调用结果字符串
        """
        tool_results = []

        # 检查是否需要种植计划查询（优先级最高）
        planting_plan_keywords = ["种植计划", "种植规划", "计划", "规划"]
        if any(keyword in message for keyword in planting_plan_keywords):
            try:
                # 尝试提取作物名称
                crops = ["水稻", "小麦", "玉米", "大豆", "棉花", "番茄", "黄瓜", "茄子", "辣椒", "白菜", "萝卜", "西红柿", "苹果", "香蕉", "葡萄", "橙子", "土豆", "红薯"]
                found_crop = None
                for crop in crops:
                    if crop in message:
                        found_crop = crop
                        break

                if found_crop:
                    result = await self.tool_service.call_tool("planting_plan", {"crop_name": found_crop})
                    if result["success"]:
                        plan_data = result["data"]
                        if plan_data["has_plan"]:
                            tool_results.append(f"【种植计划查询结果】")
                            tool_results.append(f"找到 {plan_data['total']} 个 {found_crop} 的种植计划：")
                            for plan in plan_data["plans"]:
                                tool_results.append(f"- 计划ID: {plan.get('id', 'N/A')}")
                                tool_results.append(f"  作物ID: {plan.get('cropId', 'N/A')}")
                                tool_results.append(f"  地块ID: {plan.get('plotId', 'N/A')}")
                                tool_results.append(f"  种植日期: {plan.get('plantingDate', 'N/A')}")
                                tool_results.append(f"  预计收获日期: {plan.get('expectedHarvestDate', 'N/A')}")
                                tool_results.append(f"  状态: {plan.get('status', 'N/A')}")
                                if plan.get('remark'):
                                    tool_results.append(f"  备注: {plan.get('remark', 'N/A')}")
                                tool_results.append("")
                        else:
                            tool_results.append(f"【种植计划查询结果】")
                            tool_results.append(f"未找到 {found_crop} 的种植计划，需要基于知识库制定种植计划。")
            except Exception as e:
                print(f"种植计划查询失败: {str(e)}")

        # 检查是否需要农药查询
        pesticide_keywords = ["农药", "药剂", "防治", "杀虫", "杀菌"]
        if any(keyword in message for keyword in pesticide_keywords):
            try:
                # 尝试提取作物或病虫害名称
                if "小麦" in message:
                    result = await self.tool_service.call_tool("pesticide", {"crop": "小麦"})
                    if result["success"]:
                        tool_results.append(f"【农药查询结果】\n{result['message']}")
                        for pesticide in result["data"][:2]:  # 只显示前2个
                            tool_results.append(f"- {pesticide['name']}: {pesticide['dosage']}")
            except Exception as e:
                print(f"农药查询失败: {str(e)}")

        # 检查是否需要天气查询
        weather_keywords = ["天气", "气温", "温度", "降雨", "湿度"]
        if any(keyword in message for keyword in weather_keywords):
            try:
                # 尝试提取城市名称（简单实现）
                city = "北京"  # 默认城市，实际应该从消息中提取
                result = await self.tool_service.call_tool("weather", {"city": city})
                if result["success"]:
                    tool_results.append(f"【天气查询结果】\n{result['message']}")
                    weather = result["data"]
                    tool_results.append(f"- 温度: {weather.get('temperature', 'N/A')}")
                    tool_results.append(f"- 天气: {weather.get('weather', 'N/A')}")
            except Exception as e:
                print(f"天气查询失败: {str(e)}")

        # 检查是否需要农产品价格查询
        price_keywords = ["价格", "行情", "多少钱", "售价", "收购价"]
        if any(keyword in message for keyword in price_keywords):
            try:
                # 尝试提取农产品名称
                products = ["水稻", "小麦", "玉米", "大豆", "棉花", "猪肉", "鸡蛋", "白菜", "萝卜", "西红柿", "黄瓜", "茄子", "辣椒", "苹果", "香蕉", "葡萄", "橙子"]
                found_product = None
                for product in products:
                    if product in message:
                        found_product = product
                        break

                if found_product:
                    result = await self.tool_service.call_tool("agricultural_price", {
                        "product_name": found_product
                    })
                    if result["success"]:
                        tool_results.append(f"【农产品价格查询结果】\n{result['message']}")
                        price_data = result["data"]
                        if price_data.get("prices"):
                            tool_results.append(f"- 平均价格: {price_data.get('average_price', 'N/A')}元/斤")
                            tool_results.append(f"- 价格区间: {price_data.get('price_range', {}).get('min', 'N/A')} - {price_data.get('price_range', {}).get('max', 'N/A')}元/斤")
                            tool_results.append(f"- 价格趋势: {price_data.get('trend', 'N/A')}")
                            tool_results.append(f"- 更新时间: {price_data.get('update_time', 'N/A')}")

                            # 添加数据来源信息
                            tool_results.append("\n【数据来源】")
                            for price_info in price_data.get("prices", [])[:3]:  # 只显示前3个
                                source = price_info.get("source", "未知来源")
                                source_url = price_info.get("source_url", "")
                                market = price_info.get("market", "")
                                tool_results.append(f"- {market}: {source}")
                                if source_url:
                                    tool_results.append(f"  链接: {source_url}")
            except Exception as e:
                print(f"农产品价格查询失败: {str(e)}")

        return "\n\n".join(tool_results) if tool_results else ""

    def _build_request_messages(self, messages: List[Message], context: str, tool_results: str) -> List[dict]:
        """
        构建请求消息

        Args:
            messages: 原始消息列表
            context: 知识库上下文
            tool_results: 工具调用结果

        Returns:
            构建后的消息列表
        """
        # 构建系统提示 - 结构化格式
        system_prompt = """【角色定位】
你是农业种植专家，具备作物栽培、土壤肥料、植物保护等专业背景。

【核心能力】
• 作物栽培：播种、育苗、田间管理、采收
• 土壤肥料：土壤改良、科学施肥、养分管理
• 植物保护：病虫害诊断与防治、农药科学使用
• 农业气象：天气影响分析、农事时机建议

【回答策略】
请按以下步骤分析和回答问题：

第一步：识别问题类型
- 价格查询 → 使用【实时查询结果】直接回答
- 天气咨询 → 使用【实时查询结果】直接回答  
- 种植计划 → 有计划直接展示，无计划则制定详细方案
- 技术咨询 → 使用【参考资料】专业解答

第二步：分析关键要素
- 明确作物类型、生长阶段、地区气候
- 识别病虫害症状、土壤条件、管理目标

第三步：组织专业回答
- 先给出结论或核心建议
- 再展开具体操作步骤
- 最后补充注意事项和科学原理

【Few-shot示例】

示例1 - 价格查询：
Q: 玉米多少钱一斤？
A: 根据最新市场数据：
• 平均价格：1.2元/斤
• 价格区间：1.0-1.5元/斤  
• 价格趋势：稳中有升
• 数据来源：农业部市场监测

示例2 - 种植技术：
Q: 玉米怎么种？
A: 玉米种植技术要点：

一、播种准备
• 时间：4月下旬-5月上旬（地温≥10℃）
• 选种：选择适宜当地气候的杂交种
• 整地：深翻20-25cm，施足底肥

二、种植密度
• 紧凑型：4000-4500株/亩
• 平展型：3000-3500株/亩

三、田间管理
• 苗期：及时间苗、定苗，中耕除草
• 穗期：追施穗肥，及时灌溉
• 花粒期：防倒伏，适当晚收

四、病虫害防治
• 大斑病：发病初期喷施多菌灵
• 玉米螟：心叶期撒施颗粒剂
• 杂草：苗后使用烟嘧磺隆

示例3 - 病虫害诊断：
Q: 玉米叶子发黄是什么原因？
A: 玉米叶片发黄的常见原因及对策：

一、缺素症（最常见）
• 缺氮：下部叶片先黄，追施尿素10-15kg/亩
• 缺锌：新叶脉间失绿，叶面喷施硫酸锌
• 缺铁：新叶黄化，调节土壤pH值

二、病害
• 大斑病：叶片出现梭形病斑，喷施多菌灵
• 矮花叶病：叶片黄化条纹，拔除病株

三、生理性原因
• 涝害：根系缺氧，及时排水
• 干旱：水分不足，适时灌溉
• 药害：除草剂过量，加强水肥管理

【回答要求】
• 专业准确：基于农学原理和科学依据
• 逻辑清晰：分点分段，层次分明
• 操作具体：给出明确的时间、用量、方法
• 实用性强：结合实际生产条件给出建议
"""

        # 添加工具调用结果到系统提示(放在前面，优先级更高)
        if tool_results:
            system_prompt += f"\n\n【实时查询结果】\n{tool_results}"

        # 添加上下文到系统提示
        if context:
            system_prompt += f"\n\n【参考资料】\n{context}"

        # 构建消息列表
        request_messages = [
            {"role": "system", "content": system_prompt}
        ]

        # 添加历史消息
        for msg in messages:
            request_messages.append({
                "role": msg.role.value,
                "content": msg.content
            })

        return request_messages

    async def _call_vllm(self, messages: List[dict], temperature: float, max_tokens: int) -> httpx.Response:
        """
        调用 vLLM API

        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大 token 数

        Returns:
            vLLM 响应
        """
        payload = {
            "model": config.vllm.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = await self.client.post(
            f"{config.vllm.api_url}/v1/chat/completions",
            json=payload
        )

        response.raise_for_status()
        return response

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
        await self.tool_service.close()
