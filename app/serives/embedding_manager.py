# app/services/embedding_manager.py
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.settings import Settings
import time
from typing import Optional, List
from app.utils.log import log


class EmbeddingManager:
    _instance = None
    _embed_model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def init(cls) -> bool:
        """
        初始化 Embedding 模型
        """
        start_time = time.time()
        try:
            from config.etcd_config import ETCD_CONFIG

            # 初始化 Embedding 模型
            cls._embed_model = OllamaEmbedding(
                model_name="nomic-embed-text",
                base_url=ETCD_CONFIG.ollamaConfig.url,
                embed_batch_size=100,
            )

            # 设置为全局默认 embedding 模型
            Settings.embed_model = cls._embed_model

            duration = int((time.time() - start_time) * 1000)
            log.info(f"init embedding model[nomic-embed-text], duration: {duration} ms")
            return True

        except Exception as e:
            log.error(f"Failed to initialize embedding model: {e}")
            return False

    @classmethod
    def get_embedding(cls, text: str) -> Optional[List[float]]:
        """
        获取文本的嵌入向量
        """
        try:
            if cls._embed_model is None:
                raise ValueError("Embedding model not initialized")

            return cls._embed_model.get_text_embedding(text)

        except Exception as e:
            log.error(f"Error getting embedding: {e}")
            return None

    @classmethod
    def get_model(cls) -> Optional[OllamaEmbedding]:
        """
        获取 Embedding 模型实例
        """
        return cls._embed_model
