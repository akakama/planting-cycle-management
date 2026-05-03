"""
智能数据查询工具
根据用户问题自动选择合适的后端接口查询数据
"""
import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import re


class DataQueryTool:
    """智能数据查询工具类"""
    
    def __init__(self, backend_url: str):
        """
        初始化数据查询工具
        
        Args:
            backend_url: 后端API地址
        """
        self.backend_url = backend_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
        
        # 作物名称列表
        self.crops = [
            "水稻", "小麦", "玉米", "大豆", "棉花", 
            "番茄", "黄瓜", "茄子", "辣椒", "白菜", 
            "萝卜", "西红柿", "苹果", "香蕉", "葡萄", 
            "橙子", "土豆", "红薯", "马铃薯", "花生"
        ]
        
        # 状态关键词
        self.status_keywords = {
            "进行中": ["进行中", "正在", "当前", "现在"],
            "已完成": ["已完成", "完成", "结束", "收获"],
            "未开始": ["未开始", "计划", "将要", "准备"]
        }
        
        print("智能数据查询工具初始化成功")
    
    async def query(self, user_message: str) -> Optional[Dict[str, Any]]:
        """
        根据用户问题智能选择查询接口
        
        Args:
            user_message: 用户消息
            
        Returns:
            查询结果字典，包含查询类型和数据
        """
        # 1. 检查是否询问今天的任务
        if self._is_today_task_query(user_message):
            return await self._query_today_tasks()
        
        # 2. 检查是否询问种植日历开始时间
        if self._is_calendar_start_query(user_message):
            return await self._query_calendar_start()
        
        # 3. 检查是否询问特定作物的种植计划
        crop = self._extract_crop(user_message)
        if crop:
            status = self._extract_status(user_message)
            return await self._query_planting_plans(crop, status)
        
        # 4. 检查是否询问地块信息
        if self._is_plot_query(user_message):
            return await self._query_plots()
        
        # 5. 检查是否询问日期范围内的任务
        date_range = self._extract_date_range(user_message)
        if date_range:
            return await self._query_date_range_tasks(date_range)
        
        # 6. 检查是否询问状态相关的任务
        status = self._extract_status(user_message)
        if status:
            return await self._query_status_tasks(status)
        
        return None
    
    def _is_today_task_query(self, message: str) -> bool:
        """检查是否询问今天的任务"""
        today_keywords = ["今天", "今日", "当天"]
        task_keywords = ["任务", "安排", "计划", "种植"]
        return any(t in message for t in today_keywords) and any(k in message for k in task_keywords)
    
    def _is_calendar_start_query(self, message: str) -> bool:
        """检查是否询问种植日历开始时间"""
        keywords = ["种植日历", "日历", "从哪天开始", "什么时候开始", "开始时间"]
        return any(k in message for k in keywords)
    
    def _is_plot_query(self, message: str) -> bool:
        """检查是否询问地块信息"""
        keywords = ["地块", "田地", "土地", "有哪些地"]
        return any(k in message for k in keywords)
    
    def _extract_crop(self, message: str) -> Optional[str]:
        """从消息中提取作物名称"""
        for crop in self.crops:
            if crop in message:
                return crop
        return None
    
    def _extract_status(self, message: str) -> Optional[str]:
        """从消息中提取状态"""
        for status, keywords in self.status_keywords.items():
            if any(k in message for k in keywords):
                return status
        return None
    
    def _extract_date_range(self, message: str) -> Optional[Dict[str, str]]:
        """从消息中提取日期范围"""
        # 提取"最近X天"、"本周"、"本月"等
        if "最近" in message:
            match = re.search(r'最近(\d+)天', message)
            if match:
                days = int(match.group(1))
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
                return {
                    "startDate": start_date.strftime("%Y-%m-%d"),
                    "endDate": end_date.strftime("%Y-%m-%d")
                }
        
        if "本周" in message:
            today = datetime.now()
            start_date = today - timedelta(days=today.weekday())
            return {
                "startDate": start_date.strftime("%Y-%m-%d"),
                "endDate": today.strftime("%Y-%m-%d")
            }
        
        if "本月" in message:
            today = datetime.now()
            start_date = today.replace(day=1)
            return {
                "startDate": start_date.strftime("%Y-%m-%d"),
                "endDate": today.strftime("%Y-%m-%d")
            }
        
        return None
    
    async def _query_today_tasks(self) -> Dict[str, Any]:
        """查询今天的任务"""
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"{self.backend_url}/planting-plans/ai/query"
        params = {"date": today}
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 200:
                plans = data.get("data", {}).get("records", [])
                total = data.get("data", {}).get("total", 0)
                return {
                    "type": "today_tasks",
                    "success": True,
                    "data": {
                        "date": today,
                        "total": total,
                        "plans": plans
                    },
                    "message": f"今天（{today}）有 {total} 个种植任务"
                }
        except Exception as e:
            print(f"查询今天任务失败: {str(e)}")
        
        return {"type": "today_tasks", "success": False, "message": "查询失败"}
    
    async def _query_calendar_start(self) -> Dict[str, Any]:
        """查询种植日历开始时间"""
        url = f"{self.backend_url}/planting-plans/ai/query"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 200:
                plans = data.get("data", {}).get("records", [])
                if plans:
                    # 找到最早的种植日期
                    earliest_date = min(
                        plan.get("plantingDate") for plan in plans 
                        if plan.get("plantingDate")
                    )
                    return {
                        "type": "calendar_start",
                        "success": True,
                        "data": {
                            "start_date": earliest_date,
                            "total_plans": len(plans)
                        },
                        "message": f"种植日历从 {earliest_date} 开始，共有 {len(plans)} 个种植计划"
                    }
        except Exception as e:
            print(f"查询种植日历失败: {str(e)}")
        
        return {"type": "calendar_start", "success": False, "message": "查询失败"}
    
    async def _query_planting_plans(self, crop: str, status: Optional[str] = None) -> Dict[str, Any]:
        """查询种植计划"""
        url = f"{self.backend_url}/planting-plans/ai/query"
        params = {"cropName": crop}
        if status:
            params["status"] = status
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 200:
                plans = data.get("data", {}).get("records", [])
                total = data.get("data", {}).get("total", 0)
                
                message = f"找到 {total} 个 {crop} 的种植计划"
                if status:
                    message += f"（状态：{status}）"
                
                return {
                    "type": "planting_plans",
                    "success": True,
                    "data": {
                        "crop": crop,
                        "status": status,
                        "total": total,
                        "plans": plans
                    },
                    "message": message
                }
        except Exception as e:
            print(f"查询种植计划失败: {str(e)}")
        
        return {"type": "planting_plans", "success": False, "message": "查询失败"}
    
    async def _query_plots(self) -> Dict[str, Any]:
        """查询地块信息"""
        url = f"{self.backend_url}/ai/data/plots"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 200:
                plots = data.get("data", {}).get("records", [])
                total = data.get("data", {}).get("total", 0)
                return {
                    "type": "plots",
                    "success": True,
                    "data": {
                        "total": total,
                        "plots": plots
                    },
                    "message": f"共有 {total} 个地块"
                }
        except Exception as e:
            print(f"查询地块失败: {str(e)}")
        
        return {"type": "plots", "success": False, "message": "查询失败"}
    
    async def _query_date_range_tasks(self, date_range: Dict[str, str]) -> Dict[str, Any]:
        """查询日期范围内的任务"""
        url = f"{self.backend_url}/planting-plans/ai/query"
        params = date_range
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 200:
                plans = data.get("data", {}).get("records", [])
                total = data.get("data", {}).get("total", 0)
                return {
                    "type": "date_range_tasks",
                    "success": True,
                    "data": {
                        "date_range": date_range,
                        "total": total,
                        "plans": plans
                    },
                    "message": f"在 {date_range['startDate']} 至 {date_range['endDate']} 期间有 {total} 个种植任务"
                }
        except Exception as e:
            print(f"查询日期范围任务失败: {str(e)}")
        
        return {"type": "date_range_tasks", "success": False, "message": "查询失败"}
    
    async def _query_status_tasks(self, status: str) -> Dict[str, Any]:
        """查询特定状态的任务"""
        url = f"{self.backend_url}/planting-plans/ai/query"
        params = {"status": status}
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 200:
                plans = data.get("data", {}).get("records", [])
                total = data.get("data", {}).get("total", 0)
                return {
                    "type": "status_tasks",
                    "success": True,
                    "data": {
                        "status": status,
                        "total": total,
                        "plans": plans
                    },
                    "message": f"有 {total} 个{status}的种植任务"
                }
        except Exception as e:
            print(f"查询状态任务失败: {str(e)}")
        
        return {"type": "status_tasks", "success": False, "message": "查询失败"}
    
    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()
