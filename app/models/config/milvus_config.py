from pydantic import BaseModel


class MilvusConfig(BaseModel):
    host: str
    port: int
    collectionName: str
    dim: int
