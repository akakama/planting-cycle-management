"""
天气查询工具
"""
import httpx
from typing import Dict, Any, Optional


class WeatherQuery:
    """天气查询类"""

    def __init__(self, api_key: str, api_url: str):
        """
        初始化天气查询工具

        Args:
            api_key: 天气 API 密钥
            api_url: 天气 API 地址
        """
        self.api_key = api_key
        self.api_url = api_url
        self.client = httpx.AsyncClient(timeout=10.0)

    async def query_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """
        查询天气信息

        Args:
            city: 城市名称

        Returns:
            天气信息字典，查询失败返回 None
        """
        try:
            # 如果没有配置 API 密钥，返回模拟数据
            if not self.api_key:
                return self._get_mock_weather(city)

            # 调用真实的天气 API
            response = await self.client.get(
                f"{self.api_url}?key={self.api_key}&city={city}"
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"查询天气失败: {str(e)}")
            # 返回模拟数据作为降级方案
            return self._get_mock_weather(city)

    def _get_mock_weather(self, city: str) -> Dict[str, Any]:
        """
        获取模拟天气数据

        Args:
            city: 城市名称

        Returns:
            模拟的天气信息
        """
        return {
            "city": city,
            "temperature": "25°C",
            "weather": "晴",
            "humidity": "60%",
            "wind": "东风 3级",
            "note": "（模拟数据，请配置真实的天气 API）"
        }

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
