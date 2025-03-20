# app/serives/init.py
from llama_index.llms.ollama import Ollama
import requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class OllamaService:
    _instance = None
    _llm = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OllamaService, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_llm(cls) -> Optional[Ollama]:
        return cls._llm


def init_ollama():
    """
    初始化 Ollama 服务
    - 检查 Ollama 服务是否可用
    - 初始化 LLM 模型
    """
    try:
        # 检查 Ollama 服务是否可用
        response = requests.get("http://localhost:11434/api/health")
        if response.status_code != 200:
            logger.error("Ollama service is not available")
            return False

        # 初始化 Ollama LLM
        llm = Ollama(
            model="llama2",  # 使用 llama2 模型，可以根据需要修改
            temperature=0.7,  # 控制输出的随机性
            request_timeout=120.0,  # 请求超时时间
            base_url="http://localhost:11434",  # Ollama 服务地址
            stop_sequences=["Human:", "Assistant:"],  # 停止词
        )

        # 存储 LLM 实例
        OllamaService._llm = llm

        # 测试 LLM
        test_response = llm.complete("Hello, are you ready?")
        logger.info(f"Ollama test response: {test_response}")

        logger.info("Ollama service initialized successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to initialize Ollama service: {e}")
        return False


# 使用示例
if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(level=logging.INFO)

    # 初始化 Ollama
    success = init_ollama()
    if success:
        # 获取 LLM 实例
        llm = OllamaService.get_llm()
        if llm:
            # 测试 LLM
            response = llm.complete("Tell me a joke")
            print(f"Response: {response}")
