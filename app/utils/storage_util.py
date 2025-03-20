# app/utils/storage_util.py
from minio import Minio
from minio.error import S3Error
import os
import logging
from typing import Optional, BinaryIO, List
from datetime import timedelta

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(
        self,
        endpoint: str = "localhost:9000",
        access_key: str = "minioadmin",
        secret_key: str = "minioadmin",
        secure: bool = False,
        bucket_name: str = "documents",
    ):
        """
        初始化存储管理器

        Args:
            endpoint: MinIO服务地址
            access_key: 访问密钥
            secret_key: 秘密密钥
            secure: 是否使用HTTPS
            bucket_name: 默认桶名称
        """
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.bucket_name = bucket_name
        self._ensure_bucket()

    def _ensure_bucket(self):
        """确保桶存在"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Bucket '{self.bucket_name}' created successfully")
        except S3Error as e:
            logger.error(f"Error creating bucket: {e}")
            raise

    def upload_file(
        self,
        file_path: str,
        object_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> bool:
        """
        上传文件

        Args:
            file_path: 本地文件路径
            object_name: 对象名称（如果为None，使用文件名）
            content_type: 内容类型（如果为None，自动检测）

        Returns:
            bool: 是否上传成功
        """
        try:
            if object_name is None:
                object_name = os.path.basename(file_path)

            # 上传文件
            self.client.fput_object(
                self.bucket_name, object_name, file_path, content_type=content_type
            )
            logger.info(f"'{file_path}' successfully uploaded as '{object_name}'")
            return True
        except S3Error as e:
            logger.error(f"Error uploading file: {e}")
            return False

    def upload_bytes(
        self, data: bytes, object_name: str, content_type: Optional[str] = None
    ) -> bool:
        """
        上传字节数据

        Args:
            data: 字节数据
            object_name: 对象名称
            content_type: 内容类型

        Returns:
            bool: 是否上传成功
        """
        try:
            from io import BytesIO

            data_stream = BytesIO(data)

            self.client.put_object(
                self.bucket_name,
                object_name,
                data_stream,
                length=len(data),
                content_type=content_type,
            )
            logger.info(f"Data successfully uploaded as '{object_name}'")
            return True
        except S3Error as e:
            logger.error(f"Error uploading data: {e}")
            return False

    def download_file(self, object_name: str, file_path: str) -> bool:
        """
        下载文件

        Args:
            object_name: 对象名称
            file_path: 保存路径

        Returns:
            bool: 是否下载成功
        """
        try:
            self.client.fget_object(self.bucket_name, object_name, file_path)
            logger.info(f"'{object_name}' successfully downloaded to '{file_path}'")
            return True
        except S3Error as e:
            logger.error(f"Error downloading file: {e}")
            return False

    def get_file_url(self, object_name: str, expires: int = 7200) -> Optional[str]:
        """
        获取文件的预签名URL

        Args:
            object_name: 对象名称
            expires: URL过期时间（秒）

        Returns:
            str: 预签名URL
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket_name, object_name, expires=timedelta(seconds=expires)
            )
            return url
        except S3Error as e:
            logger.error(f"Error getting file URL: {e}")
            return None

    def list_files(self, prefix: str = "") -> List[str]:
        """
        列出文件

        Args:
            prefix: 前缀过滤

        Returns:
            List[str]: 文件名列表
        """
        try:
            objects = self.client.list_objects(self.bucket_name, prefix=prefix)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            logger.error(f"Error listing files: {e}")
            return []

    def delete_file(self, object_name: str) -> bool:
        """
        删除文件

        Args:
            object_name: 对象名称

        Returns:
            bool: 是否删除成功
        """
        try:
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"'{object_name}' successfully deleted")
            return True
        except S3Error as e:
            logger.error(f"Error deleting file: {e}")
            return False
