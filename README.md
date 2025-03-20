# lama index rag project for ollama


lama-index-rag-ollama/
├── app/
│   ├── api/                 # FastAPI 路由
│   │   ├── documents.py     # 文档管理接口
│   │   └── qa.py           # 问答接口
│   ├── core/               # 核心业务逻辑
│   │   ├── document_processor.py
│   │   ├── vector_store.py
│   │   └── llm_service.py
│   ├── models/            # 数据模型
│   │   ├── document.py
│   │   └── qa.py
│   ├── services/         # 外部服务集成
│   │   ├── elasticsearch.py
│   │   ├── ollama.py
│   │   └── postgres.py
│   └── utils/           # 工具函数
├── config/             # 配置文件
├── tests/             # 测试用例
└── docker/            # Docker相关配置