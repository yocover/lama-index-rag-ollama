# main.py
import argparse
import signal
import sys

from fastapi import FastAPI, Request
import uvicorn
from app.models.business_exception import BusinessException
from app.models.common_resp import resp, resp_500
from app.serives.init import init_llama_rag
from app.serives.milvus_manager import MilvusManager
from app.utils.log import Loggers
from config.setting import ETCD_HOST, ETCD_PORT, ETCD_PREFIX
from config.etcd_config import init_config

from fastapi.middleware.cors import CORSMiddleware
from app.middleware.logging import LoggingMiddleware

from app.utils.log import log

from app.api import milvus_test


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)


# 业务异常 处理器
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return resp(code=exc.code, message=exc.message)


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return resp_500(message=str(exc))


@app.get("/")
async def read_root():
    return {"Hello": "World", "Name": "FastAPI", "Version": "0.1.0"}


def signal_handler(sig, frame):
    """处理退出信号"""
    log.info("Received shutdown signal, gracefully shutting down...")
    sys.exit(0)


app.include_router(milvus_test.router, prefix="/api")


def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="RAG Project Configuration Tool")

    parser.add_argument("-host", type=str, default=ETCD_HOST, help="ETCD host")
    parser.add_argument("-port", type=int, default=ETCD_PORT, help="ETCD port")
    parser.add_argument("-prefix", type=str, default=ETCD_PREFIX, help="Config prefix")

    # 解析命令行参数
    args = parser.parse_args()

    # 初始化配置管理器
    init_config(args)

    from config.etcd_config import ETCD_CONFIG

    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    config = uvicorn.Config(
        app="main:app",
        host=ETCD_CONFIG.appConfig.webHost,
        port=ETCD_CONFIG.appConfig.webPort,
        reload=True,
    )

    server = uvicorn.Server(config)

    # 初始化日志 让 loguru 使用 uvicorn 的日志
    Loggers.init_config()

    init_llama_rag()

    try:
        server.run()
    except Exception as e:
        log.error(f"Server run failed: {e}")
    finally:
        log.info("Server shutdown complete")


if __name__ == "__main__":
    main()
