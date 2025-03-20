from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core.settings import Settings
from pymilvus import Collection
import time
from typing import Optional, List, Dict, Any
from app.utils.log import log


class MilvusManager:
    _instance = None
    _vector_store = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MilvusManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def init(
        cls,
        host: str = "localhost",
        port: int = 19530,
        collection_name: str = "document_vectors",
        dim: int = 768,
    ) -> bool:
        """
        初始化 Milvus 向量存储
        """
        start_time = time.time()
        try:
            # 初始化 MilvusVectorStore
            cls._vector_store = MilvusVectorStore(
                host=host,
                port=port,
                collection_name=collection_name,
                dim=dim,
                similarity_metric="L2",
                enable_dynamic_field=True,  # 启用动态字段，允许插入额外的字段
            )

            # 设置为全局默认向量存储
            Settings.vector_store = cls._vector_store

            duration = int((time.time() - start_time) * 1000)
            log.info(
                f"init milvus vector store[collection: {collection_name}], duration: {duration} ms"
            )
            return True

        except Exception as e:
            log.error(f"Failed to initialize Milvus vector store: {e}")
            return False

    @classmethod
    def get_vector_store(cls) -> Optional[MilvusVectorStore]:
        return cls._vector_store

    @classmethod
    def list_collections(cls) -> List[str]:
        """
        列出所有集合
        """
        try:
            if not cls._vector_store:
                return []
            collections = cls._vector_store._client.list_collections()
            log.info(f"Available collections: {collections}")
            return collections
        except Exception as e:
            log.error(f"Failed to list collections: {e}")
            return []

    @classmethod
    def show_collection_info(cls, collection_name: str = "document_vectors") -> Optional[List[Dict[str, Any]]]:
        """
        显示集合信息和数据
        """
        try:
            if not cls._vector_store:
                return None
                
            # 获取集合统计信息
            collection = Collection(collection_name)
            collection.load()  # 确保集合已加载
            log.info(f"Collection {collection_name} statistics: {collection.num_entities}")
            
            # 使用 pymilvus 的原生查询
            results = collection.query(
                expr="id != ''",  # 查询所有记录
                output_fields=["id", "text", "metadata"],  # 指定要返回的字段
                limit=5  # 限制返回数量
            )
            
            log.info(f"Sample data from collection: {results}")
            return results
        except Exception as e:
            log.error(f"Failed to show collection info: {e}")
            return None 