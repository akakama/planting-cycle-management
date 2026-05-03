"""
农产品价格查询工具
支持实时农产品价格查询
"""
import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from loguru import logger


class AgriculturalPriceQuery:
    """农产品价格查询类"""

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        """
        初始化农产品价格查询工具

        Args:
            api_key: 农产品价格 API 密钥
            api_url: 农产品价格 API 地址
        """
        self.api_key = api_key
        self.api_url = api_url
        self.client = httpx.AsyncClient(timeout=10.0)

        # 农产品价格缓存(用于模拟数据)
        self.price_cache = self._initialize_price_cache()

        logger.info("农产品价格查询工具初始化完成")

    def _initialize_price_cache(self) -> Dict[str, List[Dict]]:
        """
        初始化农产品价格缓存(模拟数据)

        Returns:
            价格缓存字典
        """
        # 数据来源信息
        data_sources = {
            "北京新发地": {
                "name": "北京新发地农产品批发市场",
                "url": "http://www.xinfadi.com.cn/",
                "type": "批发市场",
                "description": "北京最大的农产品批发市场"
            },
            "上海江桥": {
                "name": "上海江桥批发市场",
                "url": "http://www.jqmarket.com/",
                "type": "批发市场",
                "description": "上海重要的农产品批发市场"
            },
            "广州江南": {
                "name": "广州江南果菜批发市场",
                "url": "http://www.jnmarket.com/",
                "type": "批发市场",
                "description": "华南地区最大的果菜批发市场"
            },
            "郑州粮食批发": {
                "name": "郑州粮食批发市场",
                "url": "http://www.lzm.com.cn/",
                "type": "粮食市场",
                "description": "全国重要的粮食批发市场"
            },
            "济南粮食市场": {
                "name": "济南粮食市场",
                "url": "http://www.jnls.com/",
                "type": "粮食市场",
                "description": "山东省重要的粮食批发市场"
            },
            "大连粮食": {
                "name": "大连粮食交易市场",
                "url": "http://www.dlgrain.com/",
                "type": "粮食市场",
                "description": "东北地区重要的粮食交易市场"
            },
            "长春粮食": {
                "name": "长春粮食批发市场",
                "url": "http://www.ccgrain.com/",
                "type": "粮食市场",
                "description": "吉林省重要的粮食批发市场"
            },
            "哈尔滨粮食": {
                "name": "哈尔滨粮食批发市场",
                "url": "http://www.hrbgrain.com/",
                "type": "粮食市场",
                "description": "黑龙江省重要的粮食批发市场"
            },
            "沈阳粮食": {
                "name": "沈阳粮食批发市场",
                "url": "http://www.sygrain.com/",
                "type": "粮食市场",
                "description": "辽宁省重要的粮食批发市场"
            },
            "新疆棉花": {
                "name": "新疆棉花交易市场",
                "url": "http://www.xjcotton.com/",
                "type": "棉花市场",
                "description": "全国重要的棉花交易中心"
            },
            "山东棉花": {
                "name": "山东棉花交易市场",
                "url": "http://www.sdcotton.com/",
                "type": "棉花市场",
                "description": "山东省重要的棉花交易中心"
            }
        }

        def add_source_info(market_name: str, price_data: dict) -> dict:
            """添加数据来源信息"""
            result = price_data.copy()
            if market_name in data_sources:
                result["source"] = data_sources[market_name]["name"]
                result["source_url"] = data_sources[market_name]["url"]
                result["source_type"] = data_sources[market_name]["type"]
                result["source_description"] = data_sources[market_name]["description"]
            else:
                result["source"] = "农业价格监测平台"
                result["source_url"] = "http://www.moa.gov.cn/"
                result["source_type"] = "官方监测"
                result["source_description"] = "农业农村部价格监测数据"
            return result

        cache = {
            "水稻": [
                add_source_info("北京新发地", {"market": "北京新发地", "price": 3.2, "unit": "元/斤", "date": "2024-01-15", "trend": "up"}),
                add_source_info("上海江桥", {"market": "上海江桥", "price": 3.1, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"}),
                add_source_info("广州江南", {"market": "广州江南", "price": 3.3, "unit": "元/斤", "date": "2024-01-15", "trend": "down"})
            ],
            "小麦": [
                add_source_info("郑州粮食批发", {"market": "郑州粮食批发", "price": 1.8, "unit": "元/斤", "date": "2024-01-15", "trend": "up"}),
                add_source_info("济南粮食市场", {"market": "济南粮食市场", "price": 1.7, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"})
            ],
            "玉米": [
                add_source_info("大连粮食", {"market": "大连粮食", "price": 1.5, "unit": "元/斤", "date": "2024-01-15", "trend": "up"}),
                add_source_info("长春粮食", {"market": "长春粮食", "price": 1.4, "unit": "元/斤", "date": "2024-01-15", "trend": "down"})
            ],
            "大豆": [
                add_source_info("哈尔滨粮食", {"market": "哈尔滨粮食", "price": 2.8, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"}),
                add_source_info("沈阳粮食", {"market": "沈阳粮食", "price": 2.7, "unit": "元/斤", "date": "2024-01-15", "trend": "up"})
            ],
            "棉花": [
                add_source_info("新疆棉花", {"market": "新疆棉花", "price": 18.5, "unit": "元/斤", "date": "2024-01-15", "trend": "up"}),
                add_source_info("山东棉花", {"market": "山东棉花", "price": 18.0, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"})
            ],
            "猪肉": [
                add_source_info("北京新发地", {"market": "北京新发地", "price": 15.5, "unit": "元/斤", "date": "2024-01-15", "trend": "down"}),
                add_source_info("上海江桥", {"market": "上海江桥", "price": 16.0, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"})
            ],
            "鸡蛋": [
                add_source_info("北京新发地", {"market": "北京新发地", "price": 4.8, "unit": "元/斤", "date": "2024-01-15", "trend": "up"}),
                add_source_info("广州江南", {"market": "广州江南", "price": 4.6, "unit": "元/斤", "date": "2024-01-15", "trend": "down"})
            ],
            "蔬菜类": {
                "白菜": [
                    add_source_info("北京新发地", {"market": "北京新发地", "price": 1.2, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"}),
                    add_source_info("上海江桥", {"market": "上海江桥", "price": 1.1, "unit": "元/斤", "date": "2024-01-15", "trend": "down"})
                ],
                "萝卜": [
                    add_source_info("北京新发地", {"market": "北京新发地", "price": 1.5, "unit": "元/斤", "date": "2024-01-15", "trend": "up"}),
                    add_source_info("广州江南", {"market": "广州江南", "price": 1.4, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"})
                ],
                "西红柿": [
                    add_source_info("北京新发地", {"market": "北京新发地", "price": 3.5, "unit": "元/斤", "date": "2024-01-15", "trend": "down"}),
                    add_source_info("上海江桥", {"market": "上海江桥", "price": 3.6, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"})
                ],
                "黄瓜": [
                    add_source_info("北京新发地", {"market": "北京新发地", "price": 4.2, "unit": "元/斤", "date": "2024-01-15", "trend": "up"}),
                    add_source_info("广州江南", {"market": "广州江南", "price": 4.0, "unit": "元/斤", "date": "2024-01-15", "trend": "down"})
                ],
                "茄子": [
                    add_source_info("北京新发地", {"market": "北京新发地", "price": 3.8, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"}),
                    add_source_info("上海江桥", {"market": "上海江桥", "price": 3.7, "unit": "元/斤", "date": "2024-01-15", "trend": "up"})
                ],
                "辣椒": [
                    add_source_info("北京新发地", {"market": "北京新发地", "price": 5.5, "unit": "元/斤", "date": "2024-01-15", "trend": "up"}),
                    add_source_info("广州江南", {"market": "广州江南", "price": 5.2, "unit": "元/斤", "date": "2024-01-15", "trend": "down"})
                ]
            },
            "水果类": {
                "苹果": [
                    add_source_info("北京新发地", {"market": "北京新发地", "price": 6.5, "unit": "元/斤", "date": "2024-01-15", "trend": "down"}),
                    add_source_info("上海江桥", {"market": "上海江桥", "price": 6.8, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"})
                ],
                "香蕉": [
                    add_source_info("北京新发地", {"market": "北京新发地", "price": 3.2, "unit": "元/斤", "date": "2024-01-15", "trend": "up"}),
                    add_source_info("广州江南", {"market": "广州江南", "price": 3.0, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"})
                ],
                "葡萄": [
                    add_source_info("北京新发地", {"market": "北京新发地", "price": 8.5, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"}),
                    add_source_info("上海江桥", {"market": "上海江桥", "price": 8.2, "unit": "元/斤", "date": "2024-01-15", "trend": "down"})
                ],
                "橙子": [
                    add_source_info("北京新发地", {"market": "北京新发地", "price": 5.8, "unit": "元/斤", "date": "2024-01-15", "trend": "up"}),
                    add_source_info("广州江南", {"market": "广州江南", "price": 5.5, "unit": "元/斤", "date": "2024-01-15", "trend": "stable"})
                ]
            }
        }
        return cache

    async def query_price(
        self,
        product_name: str,
        market_name: Optional[str] = None,
        days: int = 7
    ) -> Optional[Dict[str, Any]]:
        """
        查询农产品价格

        Args:
            product_name: 农产品名称
            market_name: 市场名称(可选)
            days: 查询天数

        Returns:
            价格信息字典
        """
        try:
            # 如果没有配置 API 密钥,返回缓存数据
            if not self.api_key or not self.api_url:
                return self._get_cached_price(product_name, market_name)

            # 调用真实的农产品价格 API
            params = {
                "product": product_name,
                "days": days
            }
            if market_name:
                params["market"] = market_name

            response = await self.client.get(
                f"{self.api_url}",
                params=params
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            logger.error(f"查询农产品价格失败: {str(e)}")
            # 返回缓存数据作为降级方案
            return self._get_cached_price(product_name, market_name)

    def _get_cached_price(
        self,
        product_name: str,
        market_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        从缓存获取价格信息

        Args:
            product_name: 农产品名称
            market_name: 市场名称

        Returns:
            价格信息字典
        """
        # 标准化产品名称
        product_name = self._normalize_product_name(product_name)

        # 查找价格数据
        prices = self.price_cache.get(product_name, [])

        # 如果是蔬菜或水果类别,需要从嵌套字典中查找
        if not prices:
            for category in ["蔬菜类", "水果类"]:
                if category in self.price_cache:
                    category_prices = self.price_cache[category]
                    if product_name in category_prices:
                        prices = category_prices[product_name]
                        break

        # 过滤市场
        if market_name and prices:
            prices = [p for p in prices if market_name in p["market"]]

        # 如果没有找到价格数据
        if not prices:
            return {
                "product": product_name,
                "prices": [],
                "message": f"暂无{product_name}的价格数据"
            }

        # 构建返回数据
        return {
            "product": product_name,
            "prices": prices,
            "average_price": sum(p["price"] for p in prices) / len(prices),
            "price_range": {
                "min": min(p["price"] for p in prices),
                "max": max(p["price"] for p in prices)
            },
            "trend": self._calculate_trend(prices),
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "模拟数据(请配置真实API)"
        }

    def _normalize_product_name(self, product_name: str) -> str:
        """
        标准化产品名称

        Args:
            product_name: 原始产品名称

        Returns:
            标准化后的产品名称
        """
        # 产品名称映射
        name_mapping = {
            "稻谷": "水稻",
            "稻米": "水稻",
            "大米": "水稻",
            "麦子": "小麦",
            "玉米粒": "玉米",
            "黄豆": "大豆",
            "生猪": "猪肉",
            "土鸡蛋": "鸡蛋",
            "大白菜": "白菜",
            "白萝卜": "萝卜",
            "番茄": "西红柿",
            "红苹果": "苹果",
            "绿香蕉": "香蕉"
        }

        return name_mapping.get(product_name, product_name)

    def _calculate_trend(self, prices: List[Dict]) -> str:
        """
        计算价格趋势

        Args:
            prices: 价格列表

        Returns:
            趋势字符串
        """
        if not prices:
            return "unknown"

        up_count = sum(1 for p in prices if p["trend"] == "up")
        down_count = sum(1 for p in prices if p["trend"] == "down")
        stable_count = sum(1 for p in prices if p["trend"] == "stable")

        if up_count > down_count and up_count > stable_count:
            return "上涨"
        elif down_count > up_count and down_count > stable_count:
            return "下跌"
        else:
            return "平稳"

    async def query_price_history(
        self,
        product_name: str,
        days: int = 30
    ) -> Optional[Dict[str, Any]]:
        """
        查询历史价格趋势

        Args:
            product_name: 农产品名称
            days: 查询天数

        Returns:
            历史价格数据
        """
        try:
            # 生成历史价格数据(模拟)
            current_data = await self.query_price(product_name)
            
            if not current_data or not current_data["prices"]:
                return None

            base_price = current_data["average_price"]
            history = []

            for i in range(days):
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                # 模拟价格波动(±5%)
                import random
                variation = random.uniform(-0.05, 0.05)
                price = base_price * (1 + variation)
                
                history.append({
                    "date": date,
                    "price": round(price, 2),
                    "unit": "元/斤"
                })

            # 按日期排序
            history.reverse()

            return {
                "product": product_name,
                "history": history,
                "trend": current_data["trend"],
                "data_source": "模拟数据"
            }

        except Exception as e:
            logger.error(f"查询历史价格失败: {str(e)}")
            return None

    async def get_price_comparison(
        self,
        products: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        获取多个农产品的价格对比

        Args:
            products: 农产品列表

        Returns:
            价格对比数据
        """
        try:
            comparison = []

            for product in products:
                price_data = await self.query_price(product)
                if price_data and price_data["prices"]:
                    comparison.append({
                        "product": product,
                        "average_price": price_data["average_price"],
                        "price_range": price_data["price_range"],
                        "trend": price_data["trend"]
                    })

            # 按价格排序
            comparison.sort(key=lambda x: x["average_price"], reverse=True)

            return {
                "products": comparison,
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data_source": "模拟数据"
            }

        except Exception as e:
            logger.error(f"获取价格对比失败: {str(e)}")
            return None

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()


# 便捷函数
async def get_agricultural_price(
    product_name: str,
    market_name: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    查询农产品价格(便捷函数)

    Args:
        product_name: 农产品名称
        market_name: 市场名称(可选)

    Returns:
        价格信息字典
    """
    query = AgriculturalPriceQuery()
    result = await query.query_price(product_name, market_name)
    await query.close()
    return result
