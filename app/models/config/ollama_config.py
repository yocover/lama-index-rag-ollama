from typing import Any, Dict

from pydantic import BaseModel


class OllamaConfig(BaseModel):
    url: str
    model: str
    temperature: float
    top_p: float

