from pydantic import BaseModel


class MinioConfig(BaseModel):
    endpoint: str
    accessKey: str
    secretKey: str
    bucket: str
