import time

import requests
from app.serives.embedding_manager import EmbeddingManager
from app.utils.log import log
from llama_index.core.settings import Settings
from llama_index.core.callbacks import LlamaDebugHandler, CallbackManager
from llama_index.llms.ollama import Ollama
from app.serives.milvus_manager import MilvusManager


def init_embedding():
    """
    初始化 Embedding 服务
    """
    EmbeddingManager.init()


def init_milvus():
    """
    初始化 Milvus 服务
    """
    start_time = time.time()
    from config.etcd_config import ETCD_CONFIG

    try:
        MilvusManager.init(
            host=ETCD_CONFIG.milvusConfig.host,
            port=ETCD_CONFIG.milvusConfig.port,
            collection_name=ETCD_CONFIG.milvusConfig.collectionName,
            dim=ETCD_CONFIG.milvusConfig.dim,
        )
    except Exception as e:
        log.error(f"Failed to initialize Milvus service: {e}")
        return False

    duration = int((time.time() - start_time) * 1000)
    log.info(
        f"init milvus vector store[collection: {ETCD_CONFIG.milvusConfig.collectionName}], duration: {duration} ms"
    )
    return True


def init_ollama_llm():
    """
    初始化 Ollama LLM 服务
    """
    start_time = time.time()
    from config.etcd_config import ETCD_CONFIG

    try:

        # 从配置中获取 Ollama 配置
        ollama_config = ETCD_CONFIG.ollamaConfig

        # 检查 Ollama 服务是否可用
        response = requests.get(ollama_config.url)
        if response.status_code != 200:
            log.error("Ollama service is not available")
            return False

        # 初始化 Ollama LLM 并设置为全局默认 LLM
        llm = Ollama(
            model=ollama_config.model,  # 从配置中获取模型名称
            temperature=ollama_config.temperature,
            request_timeout=120.0,
            base_url=ollama_config.url,
            # stop_sequences=["Human:", "Assistant:"],
        )

        # 设置为全局默认 LLM
        Settings.llm = llm

        # 测试 LLM
        test_response = llm.complete("Hello, are you ready?")
        log.info(f"Ollama test response: {test_response}")

        duration = int((time.time() - start_time) * 1000)
        log.info(
            f"init llm ollama[model: {ollama_config.model}], duration: {duration} ms"
        )
        return True

    except Exception as e:
        log.error(f"Failed to initialize Ollama service: {e}")
        return False


def init_callback_manager():
    print("init_callback_manager")
    start_time = time.time()
    llama_debug = LlamaDebugHandler(print_trace_on_end=True, logger=log)

    Settings.callback_manager = CallbackManager([llama_debug])
    log.info(
        f"init_callback_manager success, duration: {int((time.time() - start_time) * 1000)} ms"
    )


def init_chunk_config():
    print("init_chunk_config")
    Settings.chunk_size = 512
    Settings.chunk_overlap = 32


def init_llama_rag():
    print("init_llama_rag")
    init_callback_manager()
    init_ollama_llm()
    init_chunk_config()
    init_milvus()
    init_embedding()