# 全局变量，用于存储ETCD配置
from app.utils.etcd_util import ConfigManager
from app.models.config.app_config import AppConfig
from app.models.config.es_config import ElasticSearchConfig
from app.models.config.milvus_config import MilvusConfig
from app.models.config.minio_config import MinioConfig
from app.models.config.ollama_config import OllamaConfig
from app.models.config.postgresql_config import PostgresqlConfig

from typing import Optional

ETCD_CONFIG = None


def parse_app_config(config: dict) -> AppConfig:
    app_config_dict = config.get("application")
    app_config = AppConfig(
        webHost=app_config_dict.get("webHost"),
        webPort=app_config_dict.get("webPort"),
        fileSizeLimit=app_config_dict.get("fileSizeLimit"),
        supportedFileTypeList=app_config_dict.get("supportedFileTypeList"),
        supportedFileSuffixList=app_config_dict.get("supportedFileSuffixList"),
    )
    return app_config


def parse_es_config(config: dict) -> ElasticSearchConfig:
    es_config_dict = config.get("elasticsearch")
    es_config = ElasticSearchConfig(
        url=es_config_dict.get("url"),
        username=es_config_dict.get("username"),
        password=es_config_dict.get("password"),
        caCerts=es_config_dict.get("caCerts"),
    )
    return es_config


def parse_milvus_config(config: dict) -> MilvusConfig:
    milvus_config_dict = config.get("milvus")
    milvus_config = MilvusConfig(
        host=milvus_config_dict.get("host"),
        port=milvus_config_dict.get("port"),
        collectionName=milvus_config_dict.get("collectionName"),
        dim=milvus_config_dict.get("dim"),
    )
    return milvus_config


def parse_minio_config(config: dict) -> MinioConfig:
    minio_config_dict = config.get("minio")
    minio_config = MinioConfig(
        endpoint=minio_config_dict.get("endpoint"),
        accessKey=minio_config_dict.get("accessKey"),
        secretKey=minio_config_dict.get("secretKey"),
        bucket=minio_config_dict.get("bucket"),
    )
    return minio_config


def parse_ollama_config(config: dict) -> OllamaConfig:
    ollama_config_dict = config.get("ollama")
    ollama_config = OllamaConfig(
        url=ollama_config_dict.get("url"),
        model=ollama_config_dict.get("model"),
        temperature=ollama_config_dict.get("temperature"),
        top_p=ollama_config_dict.get("top_p"),
    )
    return ollama_config


def parse_postgresql_config(config: dict) -> PostgresqlConfig:
    postgresql_config_dict = config.get("postgresql")
    postgresql_config = PostgresqlConfig(
        username=postgresql_config_dict.get("username"),
        password=postgresql_config_dict.get("password"),
        host=postgresql_config_dict.get("host"),
        port=postgresql_config_dict.get("port"),
        database=postgresql_config_dict.get("database"),
    )
    return postgresql_config


def init_config(args):
    global ETCD_CONFIG
    ETCD_CONFIG = EtcdConfig(
        host=args.host,
        port=args.port,
        prefix=args.prefix,
    )
    ETCD_CONFIG.init_config()


class EtcdConfig:
    appConfig: Optional[AppConfig]
    elasticSearchConfig: Optional[ElasticSearchConfig]
    milvusConfig: Optional[MilvusConfig]
    minioConfig: Optional[MinioConfig]
    ollamaConfig: Optional[OllamaConfig]
    postgresqlConfig: Optional[PostgresqlConfig]

    def __init__(self, host: str, port: int, prefix: str):
        self.host = host
        self.port = port
        self.prefix = prefix

        self.client = ConfigManager(
            etcd_host=self.host, etcd_port=self.port, config_prefix=self.prefix
        )
        self.config = self.client.get_config()

    def init_config(self):
        self.appConfig = parse_app_config(self.config)
        self.elasticSearchConfig = parse_es_config(self.config)
        self.milvusConfig = parse_milvus_config(self.config)
        self.minioConfig = parse_minio_config(self.config)
        self.ollamaConfig = parse_ollama_config(self.config)
        self.postgresqlConfig = parse_postgresql_config(self.config)

    def get_config(self, key: str) -> str:
        return self.config.get(key)

    def set_config(self, key: str, value: str):
        self.client.put(self.prefix + key, value)
        self.config = self.client.get_config()

    def set_config(self, key: str, value: str):
        ETCD_CONFIG[key] = value
