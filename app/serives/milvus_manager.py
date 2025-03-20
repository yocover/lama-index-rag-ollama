# app/services/milvus_manager.py
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core.settings import Settings
from pymilvus import (
    connections,
    Collection,
    utility,
    CollectionSchema,
    FieldSchema,
    DataType,
)
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
        dim: int = 768,  # nomic-embed-text 的维度是 768
    ) -> bool:
        """
        初始化 Milvus 向量存储
        """
        start_time = time.time()
        try:
            # 首先建立连接
            connections.connect(alias="default", host=host, port=port)

            # 检查集合是否存在
            if not utility.has_collection(collection_name):
                # 只在集合不存在时创建
                log.info(f"Creating new collection: {collection_name}")
                # 定义集合的 schema
                fields = [
                    # 主键字段，用于唯一标识每条记录
                    FieldSchema(
                        name="id",
                        dtype=DataType.VARCHAR,  # 字符串类型
                        max_length=100,  # 最大长度100
                        is_primary=True,  # 设为主键
                    ),
                    # 向量字段，存储文档的嵌入向量
                    FieldSchema(
                        name="vector",
                        dtype=DataType.FLOAT_VECTOR,  # 浮点数向量类型
                        dim=dim,  # 向量维度，这里是768（nomic-embed-text模型的输出维度）
                    ),
                    # 文本字段，存储原始文档内容
                    FieldSchema(
                        name="text",
                        dtype=DataType.VARCHAR,  # 字符串类型
                        max_length=65535,  # 最大长度65535，用于存储较长文本
                    ),
                    # 元数据字段，存储额外信息
                    FieldSchema(
                        name="metadata",
                        dtype=DataType.JSON,  # JSON类型，可以存储结构化数据
                    ),
                ]
                schema = CollectionSchema(fields=fields)

                # 创建集合
                collection = Collection(collection_name, schema)

                # 创建索引
                index_params = {
                    "metric_type": "L2",  # 距离度量类型：L2 欧氏距离，用于计算向量之间的相似度
                    "index_type": "IVF_FLAT",  # 索引类型：IVF_FLAT 是一种基于聚类的索引方法
                    "params": {"nlist": 1024},  # 聚类簇的数量，影响检索精度和速度的平衡
                }
                collection.create_index("vector", index_params)
            else:
                log.info(f"Collection {collection_name} already exists, loading...")
                collection = Collection(collection_name)

            # 加载集合到内存
            collection.load()

            # 初始化 MilvusVectorStore
            cls._vector_store = MilvusVectorStore(
                host=host, port=port, collection_name=collection_name, dim=dim
            )

            # 设置为全局默认向量存储
            Settings.vector_store = cls._vector_store

            log.info(f"Collection schema: {collection.schema}")
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
        """
        获取 Milvus 向量存储实例
        """
        return cls._vector_store

    @classmethod
    def list_collections(cls):
        """
        列出所有集合
        """
        try:
            collections = utility.list_collections()
            log.info(f"Available collections: {collections}")
            return collections
        except Exception as e:
            log.error(f"Failed to list collections: {e}")
            return []

    @classmethod
    def show_collection_info(
        cls, collection_name: str = "document_vectors"
    ) -> Optional[List[Dict[str, Any]]]:
        """
        显示集合信息和数据
        """
        try:

            if not cls._vector_store:
                return None

            collection = Collection(collection_name)
            # 显示统计信息
            log.info(
                f"Collection {collection_name} statistics: {collection.num_entities}"
            )

            # 查询所有数据
            collection.load()
            results = collection.query(
                expr="id != ''",
                output_fields=["id", "text", "metadata"],
                limit=5,  # 限制返回前5条以避免输出过多
            )
            log.info(f"Sample data from collection: {collection_name}")
            return results
        except Exception as e:
            log.error(f"Failed to show collection info: {e}")
            return None
