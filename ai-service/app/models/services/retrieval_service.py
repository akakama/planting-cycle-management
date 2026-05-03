"""
向量检索服务
负责初始化 ChromaDB 连接，执行向量相似度检索
"""
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer
from app.models.schemas.retrieve import RetrievedDocument
from app.config import config


class RetrievalService:
    """向量检索服务类"""

    def __init__(self, auto_init: bool = True):
        """初始化检索服务
        
        Args:
            auto_init: 是否自动初始化知识库（默认True）
        """
        try:
            # 初始化 ChromaDB 客户端（使用本地持久化存储）
            self.client = chromadb.PersistentClient(path="./data/chromadb")

            # 获取或创建集合
            self.collection = self.client.get_or_create_collection(
                name=config.chromadb.collection_name
            )

            # 初始化嵌入模型
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

            print(f"检索服务初始化成功，集合: {config.chromadb.collection_name}")
            
            # 自动初始化知识库
            if auto_init and self.collection.count() == 0:
                print("检测到知识库为空，开始自动初始化...")
                self._init_knowledge_base()
                
        except Exception as e:
            print(f"检索服务初始化失败: {str(e)}")
            raise

    def _init_knowledge_base(self):
        """自动初始化知识库"""
        try:
            from app.init_knowledge_base import init_knowledge_base
            init_knowledge_base()
            print("知识库自动初始化完成")
        except Exception as e:
            print(f"知识库自动初始化失败: {str(e)}")
            print("请手动运行: python -m app.init_knowledge_base")

    async def search_documents(self, query: str, top_k: int = 8) -> List[RetrievedDocument]:
        """
        执行向量检索

        Args:
            query: 查询关键词
            top_k: 返回文档数量

        Returns:
            检索到的文档列表
        """
        try:
            # 转换查询为向量
            query_embedding = self.embedder.encode(query).tolist()

            # 执行检索
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            # 转换结果为文档列表
            documents = []
            if results['documents'] and results['documents'][0]:
                for i, content in enumerate(results['documents'][0]):
                    doc = RetrievedDocument(
                        content=content,
                        metadata=results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else None,
                        score=results['distances'][0][i] if results['distances'] and results['distances'][0] else 0.0
                    )
                    documents.append(doc)

            # 按相似度降序排序（ChromaDB 已经按距离排序，距离越小越相似）
            return documents

        except Exception as e:
            print(f"检索失败: {str(e)}")
            raise Exception(f"检索失败: {str(e)}")

    def get_collection_info(self) -> dict:
        """获取集合信息"""
        try:
            return {
                "name": self.collection.name,
                "count": self.collection.count(),
                "metadata": self.collection.metadata
            }
        except Exception as e:
            print(f"获取集合信息失败: {str(e)}")
            return {}
