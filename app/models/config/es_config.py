from typing import Optional
from pydantic import BaseModel


class ElasticSearchConfig(BaseModel):
    url: str
    username: Optional[str]
    password: Optional[str]
    caCerts: Optional[str]
