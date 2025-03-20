from pydantic import BaseModel


class PostgresqlConfig(BaseModel):
    username: str
    password: str
    host: str
    port: int
    database: str
