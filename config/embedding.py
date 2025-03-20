from llama_index.embeddings.ollama import OllamaEmbedding

from app.custom.custom_timed_embedding_wrapper import CustomTimedEmbeddingWrapper


class EmbeddingManager:
    _embedding_ollama_omic_embed_text = None
    _embedding_ollama_bge_large = None
    _embedding_ollama_bge_m3 = None

    @staticmethod
    def get_embedding_ollama_omic_embed_text():
        if EmbeddingManager._embedding_ollama_omic_embed_text is None:
            EmbeddingManager._embedding_ollama_omic_embed_text = (
                get_embedding_ollama_nomic_embed_text()
            )
        return EmbeddingManager._embedding_ollama_omic_embed_text

    @staticmethod
    def get_embedding_ollama_bge_large():
        if EmbeddingManager._embedding_ollama_bge_large is None:
            EmbeddingManager._embedding_ollama_bge_large = (
                get_embedding_ollama_bge_large()
            )
        return EmbeddingManager._embedding_ollama_bge_large

    @staticmethod
    def get_embedding_ollama_bge_m3():
        if EmbeddingManager._embedding_ollama_bge_m3 is None:
            EmbeddingManager._embedding_ollama_bge_m3 = get_embedding_ollama_bge_m3()
        return EmbeddingManager._embedding_ollama_bge_m3


def get_embedding_ollama_bge_large():
    # ollama 的 bge-large-en-v1.5 模型
    from config.etcd_config import ETCD_CONFIG

    ollama_embedding = OllamaEmbedding(
        model_name="imcurie/bge-large-en-v1.5",
        base_url=ETCD_CONFIG.ollamaConfig.url,
        embed_batch_size=100,
    )

    return CustomTimedEmbeddingWrapper(
        ollama_embedding, message="ollama_bge_large", dim=1024
    )


def get_embedding_ollama_bge_m3():
    # ollama embedding model: bge-m3
    from config.etcd_config import ETCD_CONFIG

    ollama_embedding = OllamaEmbedding(
        base_url=ETCD_CONFIG.ollamaConfig.url,
        model_name="bge-m3",
        embed_batch_size=100,
    )
    return CustomTimedEmbeddingWrapper(
        ollama_embedding, message="ollama bge m3", dim=1024
    )


def get_embedding_ollama_nomic_embed_text():
    # ollama embedding model: nomic-embed-text
    from config.etcd_config import ETCD_CONFIG

    ollama_embedding = OllamaEmbedding(
        base_url=ETCD_CONFIG.ollamaConfig.url,
        model_name="nomic-embed-text",
        embed_batch_size=100,
    )
    return CustomTimedEmbeddingWrapper(
        ollama_embedding, message="ollama nomic embed text", dim=1024
    )
