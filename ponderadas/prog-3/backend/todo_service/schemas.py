from pydantic import BaseModel, Field
import datetime


class LogEntry(BaseModel):
    user_id: str
    action: str
    result: str
    timestamp: datetime.datetime = None


class TaskSchema(BaseModel):
    content: str = Field(default=None)
    user_id: int = Field(default=None)
    check: bool = Field(default=None)

    # Configuração criada para documentação do modelo
    class Config:
        schema_extra = {
            "post_teste": {
                "content": "Conteúdo do post teste",
                "user_id": 1,
                "check": True,
            },
        }
