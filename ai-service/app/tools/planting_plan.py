"""
种植计划查询工具
从后端API查询种植计划信息
"""
import httpx
from typing import Dict, Any, Optional


class PlantingPlanQuery:
    """种植计划查询类"""

    def __init__(self, backend_url: str):
        """
        初始化种植计划查询工具

        Args:
            backend_url: 后端API地址
        """
        self.backend_url = backend_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)

    async def query_by_crop_name(self, crop_name: str) -> Optional[Dict[str, Any]]:
        """
        根据作物名称查询种植计划

        Args:
            crop_name: 作物名称

        Returns:
            种植计划数据，如果查询失败返回None
        """
        try:
            url = f"{self.backend_url}/planting-plans/ai/query"
            params = {"cropName": crop_name}

            response = await self.client.get(url, params=params)
            response.raise_for_status()

            result = response.json()
            if result.get("code") == 200:
                data = result.get("data", {})
                if data and data.get("records"):
                    # 有种植计划
                    return {
                        "has_plan": True,
                        "crop_name": crop_name,
                        "plans": data["records"],
                        "total": data.get("total", 0)
                    }
                else:
                    # 没有种植计划
                    return {
                        "has_plan": False,
                        "crop_name": crop_name,
                        "plans": [],
                        "total": 0
                    }
            else:
                print(f"查询种植计划失败: {result.get('message', '未知错误')}")
                return None

        except httpx.TimeoutException:
            print("查询种植计划超时")
            return None
        except httpx.HTTPStatusError as e:
            print(f"查询种植计划HTTP错误: {e.response.status_code}")
            return None
        except Exception as e:
            print(f"查询种植计划异常: {str(e)}")
            return None

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
