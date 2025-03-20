# app/api/milvus_test.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from llama_index.core import Document
from app.serives.embedding_manager import EmbeddingManager
from app.serives.milvus_manager import MilvusManager
from app.utils.log import log

router = APIRouter()


class DocumentInput(BaseModel):
    text: str
    metadata: Optional[dict] = None


class SearchInput(BaseModel):
    query_text: str
    top_k: int = 5


@router.post("/milvus/add")
async def add_document(doc_input: DocumentInput):
    """
    添加文档到 Milvus
    """
    try:
        vector_store = MilvusManager.get_vector_store()
        if not vector_store:
            raise HTTPException(
                status_code=500, detail="Milvus vector store not initialized"
            )

        # 首先生成文档的嵌入向量
        embedding = EmbeddingManager.get_embedding(doc_input.text)
        if not embedding:
            raise HTTPException(status_code=500, detail="Failed to generate embedding")

        # 创建文档并设置嵌入向量
        doc = Document(
            text=doc_input.text,
            metadata=doc_input.metadata or {},
            embedding=embedding,  # 添加嵌入向量
        )

        # 添加到向量存储
        vector_store.add([doc])

        return {
            "status": "success",
            "message": "Document added successfully",
            "document": {"text": doc_input.text, "metadata": doc_input.metadata},
        }
    except Exception as e:
        log.error(f"Error adding document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/milvus/search")
async def search_documents(search_input: SearchInput):
    """
    搜索相似文档
    """
    try:
        vector_store = MilvusManager.get_vector_store()
        if not vector_store:
            raise HTTPException(
                status_code=500, detail="Milvus vector store not initialized"
            )

        # 获取查询文本的嵌入向量
        embedding = EmbeddingManager.get_embedding(search_input.query_text)
        if not embedding:
            raise HTTPException(status_code=500, detail="Failed to generate embedding")

        # 执行向量搜索
        results = vector_store.similarity_search(
            search_input.query_text,
            k=search_input.top_k,
        )

        # 格式化结果
        formatted_results = []
        for doc in results:
            formatted_results.append(
                {
                    "text": doc.text,
                    "metadata": doc.metadata,
                    "score": getattr(doc, "score", None),  # 如果有相似度分数
                }
            )

        return {
            "status": "success",
            "query": search_input.query_text,
            "results": formatted_results,
        }
    except Exception as e:
        log.error(f"Error searching documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/milvus/status")
async def get_milvus_status():
    """
    获取 Milvus 状态
    """
    try:
        # 获取所有集合
        collections = MilvusManager.list_collections()

        # 获取当前使用的集合
        vector_store = MilvusManager.get_vector_store()
        current_collection = vector_store.collection_name if vector_store else None

        return {
            "status": "success",
            "collections": collections,
            "current_collection": current_collection,
        }
    except Exception as e:
        log.error(f"Error getting Milvus status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/milvus/data")
async def get_collection_data():
    """
    获取集合中的数据
    """
    try:
        data = MilvusManager.show_collection_info()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
