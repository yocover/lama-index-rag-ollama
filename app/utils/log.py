import os
import sys
import time
import logging
from types import FrameType
from typing import cast
from loguru import logger

from config.setting import BASE_DIR, LOG_DIR_NAME, APP_NAME


class Logger:
    """输出日志到文件和控制台"""

    def __init__(self):
        log_dir = os.path.join(BASE_DIR, LOG_DIR_NAME)
        # 文件的命名
        log_name = (
            f"Fast_{time.strftime('%Y-%m-%d', time.localtime()).replace('-', '_')}.log"
        )
        log_path = os.path.join(log_dir, APP_NAME + "_{time:YYYY-MM-DD}.log")
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 判断日志文件夹是否存在，不存则创建
        if not os.path.exists(log_dir):
            os.chmod(BASE_DIR, 0o755)
            os.makedirs(log_dir)
        # 日志输出格式
        formatter = "{time:YYYY-MM-DD HH:mm:ss} | {level}: {message}"
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明
        self.logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "  # 颜色>时间
            "{process.name} | "  # 进程名
            "{thread.name} | "  # 线程名
            "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
            ":<cyan>{line}</cyan> | "  # 行号
            "<level>{level}</level>: "  # 等级
            "<level>{message}</level>",  # 日志内容
        )
        # 日志写入文件
        self.logger.add(
            log_path,  # 写入目录指定文件
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} - "  # 时间
            "{process.name} | "  # 进程名
            "{thread.name} | "  # 线程名
            "{module}.{function}:{line} - {level} -{message}",  # 模块名.方法名:行号
            encoding="utf-8",
            retention="7 days",  # 设置历史保留时长
            backtrace=True,  # 回溯
            diagnose=True,  # 诊断
            enqueue=True,  # 异步写入
            rotation="00:00",  # 每日更新时间
            # rotation="5kb",  # 切割，设置文件大小，rotation="12:00"，rotation="1 week"
            # filter="my_module"  # 过滤模块
            # compression="zip"   # 文件压缩
        )

    def init_config(self):
        LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn")

        # change handler for default uvicorn logger
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in LOGGER_NAMES:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler()]

        # change handler for global logger
        root_logger = logging.getLogger()
        root_logger.handlers = [InterceptHandler()]

    def get_logger(self):
        return self.logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


Loggers = Logger()
log = Loggers.get_logger()
