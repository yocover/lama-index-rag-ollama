from typing import List
from pydantic import BaseModel


class AppConfig(BaseModel):
    webHost: str
    webPort: int
    fileSizeLimit: int
    supportedFileTypeList: List[str]
    supportedFileSuffixList: List[str]
