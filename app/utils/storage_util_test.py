# app/utils/storage_util_test.py
import os
import sys
from app.utils.storage_util import StorageManager


# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)


def test_storage_util():
    # 初始化存储管理器
    storage = StorageManager(
        endpoint="localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        bucket_name="documents",
    )

    # 测试上传文件
    test_file = "config/project-dev.yml"
    success = storage.upload_file(test_file)
    print(f"Upload file: {'success' if success else 'failed'}")

    # 测试获取文件列表
    files = storage.list_files()
    print("\nFiles in storage:")
    for file in files:
        print(f"- {file}")

        # 获取文件的访问URL
        url = storage.get_file_url(file)
        print(f"  URL: {url}")
