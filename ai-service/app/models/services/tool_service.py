"""
工具调用服务
支持农药查询、天气查询、农产品价格查询和种植计划查询工具
"""
from typing import Dict, Any, Optional
from app.tools.pesticide import PesticideQuery
from app.tools.weather import WeatherQuery
from app.tools.agricultural_price import AgriculturalPriceQuery
from app.tools.planting_plan import PlantingPlanQuery
from app.config import config


class ToolCallService:
    """工具调用服务类"""

    def __init__(self):
        """初始化工具调用服务"""
        try:
            # 初始化农药查询工具
            self.pesticide_query = PesticideQuery(config.tools.pesticide_db_path)

            # 初始化天气查询工具
            self.weather_query = WeatherQuery(
                config.tools.weather_api_key,
                config.tools.weather_api_url
            )

            # 初始化农产品价格查询工具
            self.price_query = AgriculturalPriceQuery(
                config.tools.price_api_key if hasattr(config.tools, 'price_api_key') else None,
                config.tools.price_api_url if hasattr(config.tools, 'price_api_url') else None
            )

            # 初始化种植计划查询工具
            self.planting_plan_query = PlantingPlanQuery(config.tools.backend_url)

            print("工具调用服务初始化成功")
        except Exception as e:
            print(f"工具调用服务初始化失败: {str(e)}")
            raise

    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用指定工具

        Args:
            tool_name: 工具名称（pesticide、weather、agricultural_price 或 planting_plan）
            parameters: 工具参数

        Returns:
            工具调用结果
        """
        try:
            if tool_name == "pesticide":
                return await self._call_pesticide_tool(parameters)
            elif tool_name == "weather":
                return await self._call_weather_tool(parameters)
            elif tool_name == "agricultural_price":
                return await self._call_price_tool(parameters)
            elif tool_name == "planting_plan":
                return await self._call_planting_plan_tool(parameters)
            else:
                raise ValueError(f"未知的工具: {tool_name}")
        except Exception as e:
            print(f"工具调用失败: {str(e)}")
            raise Exception(f"工具调用失败: {str(e)}")

    async def _call_pesticide_tool(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用农药查询工具

        Args:
            parameters: 查询参数（name、crop 或 pest）

        Returns:
            查询结果
        """
        try:
            # 按名称查询
            if "name" in parameters:
                result = self.pesticide_query.query_by_name(parameters["name"])
                if result:
                    return {
                        "success": True,
                        "data": result,
                        "message": f"找到农药: {result['name']}"
                    }
                else:
                    return {
                        "success": False,
                        "data": None,
                        "message": f"未找到农药: {parameters['name']}"
                    }

            # 按作物查询
            elif "crop" in parameters:
                results = self.pesticide_query.query_by_crop(parameters["crop"])
                if results:
                    return {
                        "success": True,
                        "data": results,
                        "message": f"找到 {len(results)} 种适用于 {parameters['crop']} 的农药"
                    }
                else:
                    return {
                        "success": False,
                        "data": None,
                        "message": f"未找到适用于 {parameters['crop']} 的农药"
                    }

            # 按病虫害查询
            elif "pest" in parameters:
                results = self.pesticide_query.query_by_pest(parameters["pest"])
                if results:
                    return {
                        "success": True,
                        "data": results,
                        "message": f"找到 {len(results)} 种防治 {parameters['pest']} 的农药"
                    }
                else:
                    return {
                        "success": False,
                        "data": None,
                        "message": f"未找到防治 {parameters['pest']} 的农药"
                    }

            else:
                return {
                    "success": False,
                    "data": None,
                    "message": "请提供查询参数（name、crop 或 pest）"
                }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"农药查询失败: {str(e)}"
            }

    async def _call_weather_tool(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用天气查询工具

        Args:
            parameters: 查询参数（city）

        Returns:
            查询结果
        """
        try:
            if "city" not in parameters:
                return {
                    "success": False,
                    "data": None,
                    "message": "请提供城市名称"
                }

            result = await self.weather_query.query_weather(parameters["city"])
            if result:
                return {
                    "success": True,
                    "data": result,
                    "message": f"查询到 {parameters['city']} 的天气信息"
                }
            else:
                return {
                    "success": False,
                    "data": None,
                    "message": f"查询 {parameters['city']} 天气失败"
                }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"天气查询失败: {str(e)}"
            }

    async def _call_price_tool(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用农产品价格查询工具

        Args:
            parameters: 查询参数（product_name, market_name）

        Returns:
            查询结果
        """
        try:
            if "product_name" not in parameters:
                return {
                    "success": False,
                    "data": None,
                    "message": "请提供农产品名称"
                }

            result = await self.price_query.query_price(
                parameters["product_name"],
                parameters.get("market_name")
            )
            if result and result.get("prices"):
                return {
                    "success": True,
                    "data": result,
                    "message": f"查询到 {parameters['product_name']} 的价格信息"
                }
            else:
                return {
                    "success": False,
                    "data": None,
                    "message": f"查询 {parameters['product_name']} 价格失败"
                }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"农产品价格查询失败: {str(e)}"
            }

    async def _call_planting_plan_tool(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用种植计划查询工具

        Args:
            parameters: 查询参数（crop_name）

        Returns:
            查询结果
        """
        try:
            if "crop_name" not in parameters:
                return {
                    "success": False,
                    "data": None,
                    "message": "请提供作物名称"
                }

            result = await self.planting_plan_query.query_by_crop_name(parameters["crop_name"])
            if result:
                if result["has_plan"]:
                    return {
                        "success": True,
                        "data": result,
                        "message": f"找到 {result['total']} 个 {parameters['crop_name']} 的种植计划"
                    }
                else:
                    return {
                        "success": True,
                        "data": result,
                        "message": f"未找到 {parameters['crop_name']} 的种植计划"
                    }
            else:
                return {
                    "success": False,
                    "data": None,
                    "message": f"查询 {parameters['crop_name']} 种植计划失败"
                }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"种植计划查询失败: {str(e)}"
            }

    async def close(self):
        """关闭工具服务"""
        await self.weather_query.close()
        await self.price_query.close()
        await self.planting_plan_query.close()
