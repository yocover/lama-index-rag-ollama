import time
from typing import List, Any

from llama_index.core.base.embeddings.base import BaseEmbedding, Embedding
from pydantic import PrivateAttr

from app.utils.log import log


class CustomTimedEmbeddingWrapper(BaseEmbedding):
    """A wrapper class for BaseEmbedding to measure and log the time taken by embedding method."""

    _embed: BaseEmbedding = PrivateAttr()
    _message: str = PrivateAttr()
    _dim: int = PrivateAttr()

    def __init__(self, embed: BaseEmbedding, message: str, dim: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.model_name = embed.model_name
        self.__dict__["_embed"] = embed  # 通过直接设置 __dict__ 来绕过 Pydantic 的检查
        self.__dict__["_message"] = message
        self.__dict__["_dim"] = dim

    def _get_query_embedding(self, query: str) -> Embedding:
        start_time = time.time()
        results = self._embed._get_query_embedding(query)
        log.info(
            f"{self._message}, _get_query_embedding took {int((time.time() - start_time) * 1000)} ms"
        )
        return results

    async def _aget_query_embedding(self, query: str) -> Embedding:
        start_time = time.time()
        results = await self._embed._aget_query_embedding(query)
        log.info(
            f"{self._message}, _aget_query_embedding took {int((time.time() - start_time) * 1000)} ms"
        )
        return results

    def get_query_embedding(self, query: str) -> Embedding:
        log.info(f"{self._message}, start get_query_embedding")
        start_time = time.time()
        results = self._embed.get_query_embedding(query)
        log.info(
            f"{self._message}, get_query_embedding took {int((time.time() - start_time) * 1000)} ms"
        )
        return results

    async def aget_query_embedding(self, query: str) -> Embedding:
        log.info(f"{self._message}, start aget_query_embedding")
        start_time = time.time()
        results = await self._embed.aget_query_embedding(query)
        log.info(
            f"{self._message}, aget_query_embedding took {int((time.time() - start_time) * 1000)} ms"
        )
        return results

    def _get_text_embedding(self, text: str) -> List[float]:
        """
        Get text embedding.
        """
        return self._embed._get_text_embedding(text)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        """
        Async get text embedding.
        """
        response = await self._embed._aget_text_embedding(text)
        return response

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get text embedding.
        """
        return self._embed._get_text_embeddings(texts)

    async def _aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Async get text embeddings.
        """
        return await self._embed._aget_text_embeddings(texts)

    def get_text_embedding(self, text: str) -> Embedding:
        return self._embed.get_text_embedding(text)

    async def aget_text_embedding(self, text: str) -> Embedding:
        return await self._embed.aget_text_embedding(text)

    def get_text_embedding_batch(
        self,
        texts: List[str],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[Embedding]:
        return self._embed.get_text_embedding_batch(
            texts, show_progress=show_progress, **kwargs
        )

    async def aget_text_embedding_batch(
        self, texts: List[str], show_progress: bool = False
    ) -> List[Embedding]:
        return await self._embed.aget_text_embedding_batch(
            texts, show_progress=show_progress
        )

    def get_dim(self):
        return self._dim
