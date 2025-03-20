from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR_NAME = "logs"

APP_NAME = "lama-rag"
SERVER_NAME = "lama-rag-app"

ES_INDEX_PREFIX = APP_NAME + "_"
MILVUS_COLLECTION_PREFIX = APP_NAME + "_"

MILVUS_SIMILARITY_METRIC = "COSINE"
MILVUS_INDEX_TYPE = "HNSW"

ETCD_HOST = "localhost"
ETCD_PORT = 2379
ETCD_PREFIX = "lama-rag/dev/config"
