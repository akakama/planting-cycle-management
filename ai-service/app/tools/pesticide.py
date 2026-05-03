"""
农药查询工具
"""
import sqlite3
from typing import List, Dict, Any, Optional
import os


class PesticideQuery:
    """农药查询类"""

    def __init__(self, db_path: str):
        """
        初始化农药查询工具

        Args:
            db_path: 农药数据库路径
        """
        self.db_path = db_path
        self._ensure_database()

    def _ensure_database(self):
        """确保数据库存在，如果不存在则创建"""
        if not os.path.exists(self.db_path):
            # 创建数据库目录
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            # 创建数据库
            self._create_database()

    def _create_database(self):
        """创建农药数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pesticides (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    alias TEXT,
                    target_crops TEXT,
                    target_pests TEXT,
                    usage_method TEXT,
                    dosage TEXT,
                    precautions TEXT,
                    safety_period TEXT
                )
            """)

            # 插入示例数据
            sample_data = [
                ("三唑酮", "粉锈宁", "小麦、水稻、玉米", "白粉病、锈病", "喷雾", "25%可湿性粉剂，每亩30-50克", "避免在花期使用，注意安全间隔期", "7-10天"),
                ("三环唑", "稻瘟灵", "水稻", "稻瘟病", "叶面喷雾", "75%可湿性粉剂，每亩20-30克", "注意轮换使用，避免产生抗性", "14-21天"),
                ("吡虫啉", "一遍净", "水稻、小麦、棉花", "蚜虫、飞虱", "喷雾", "10%可湿性粉剂，每亩10-20克", "对蜜蜂有毒，花期禁用", "7-14天"),
            ]

            cursor.executemany("""
                INSERT INTO pesticides (name, alias, target_crops, target_pests, usage_method, dosage, precautions, safety_period)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, sample_data)

            conn.commit()
            conn.close()
            print(f"农药数据库创建成功: {self.db_path}")
        except Exception as e:
            print(f"创建农药数据库失败: {str(e)}")

    def query_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        按名称查询农药

        Args:
            name: 农药名称

        Returns:
            农药信息字典，未找到返回 None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pesticides WHERE name = ?", (name,))
            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    "name": result[1],
                    "alias": result[2],
                    "target_crops": result[3],
                    "target_pests": result[4],
                    "usage_method": result[5],
                    "dosage": result[6],
                    "precautions": result[7],
                    "safety_period": result[8]
                }
            return None
        except Exception as e:
            print(f"查询农药失败: {str(e)}")
            return None

    def query_by_crop(self, crop: str) -> List[Dict[str, Any]]:
        """
        按作物查询农药

        Args:
            crop: 作物名称

        Returns:
            农药信息列表
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pesticides WHERE target_crops LIKE ?", (f"%{crop}%",))
            results = cursor.fetchall()
            conn.close()

            pesticides = []
            for result in results:
                pesticides.append({
                    "name": result[1],
                    "alias": result[2],
                    "target_crops": result[3],
                    "target_pests": result[4],
                    "usage_method": result[5],
                    "dosage": result[6],
                    "precautions": result[7],
                    "safety_period": result[8]
                })
            return pesticides
        except Exception as e:
            print(f"查询农药失败: {str(e)}")
            return []

    def query_by_pest(self, pest: str) -> List[Dict[str, Any]]:
        """
        按病虫害查询农药

        Args:
            pest: 病虫害名称

        Returns:
            农药信息列表
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pesticides WHERE target_pests LIKE ?", (f"%{pest}%",))
            results = cursor.fetchall()
            conn.close()

            pesticides = []
            for result in results:
                pesticides.append({
                    "name": result[1],
                    "alias": result[2],
                    "target_crops": result[3],
                    "target_pests": result[4],
                    "usage_method": result[5],
                    "dosage": result[6],
                    "precautions": result[7],
                    "safety_period": result[8]
                })
            return pesticides
        except Exception as e:
            print(f"查询农药失败: {str(e)}")
            return []
