"""
测试农产品价格查询功能
"""
import asyncio
import sys
sys.path.append('.')

from app.models.services.chat_service import ChatService
from app.models.services.retrieval_service import RetrievalService
from app.models.services.tool_service import ToolCallService
from app.models.schemas.chat import Message

async def test_price_query():
    """测试价格查询功能"""
    print("=" * 60)
    print("测试农产品价格查询功能")
    print("=" * 60)

    # 初始化服务
    print("\n1. 初始化服务...")
    retrieval_service = RetrievalService()
    tool_service = ToolCallService()
    chat_service = ChatService(retrieval_service, tool_service)
    print("✓ 服务初始化成功")

    # 测试用例
    test_cases = [
        "玉米多少钱一斤",
        "小麦的价格是多少",
        "水稻行情怎么样",
        "猪肉售价",
        "苹果收购价",
        "如何种植玉米"  # 这个不应该触发价格查询
    ]

    print("\n2. 开始测试...")
    for i, test_message in enumerate(test_cases, 1):
        print(f"\n--- 测试用例 {i}: {test_message} ---")

        # 检查是否触发价格查询
        price_keywords = ["价格", "行情", "多少钱", "售价", "收购价"]
        has_price_keyword = any(keyword in test_message for keyword in price_keywords)
        print(f"  包含价格关键词: {has_price_keyword}")

        products = ["水稻", "小麦", "玉米", "大豆", "棉花", "猪肉", "鸡蛋", "白菜", "萝卜", "西红柿", "黄瓜", "茄子", "辣椒", "苹果", "香蕉", "葡萄", "橙子"]
        found_product = None
        for product in products:
            if product in test_message:
                found_product = product
                break
        print(f"  找到农产品: {found_product}")

        if has_price_keyword and found_product:
            print(f"  ✓ 应该触发价格查询")
        else:
            print(f"  ✗ 不会触发价格查询")

    print("\n3. 关闭服务...")
    await chat_service.close()
    print("✓ 服务已关闭")

    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_price_query())
