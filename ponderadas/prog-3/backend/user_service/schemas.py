from pydantic import BaseModel, Field, EmailStr
import datetime


class LogEntry(BaseModel):
    user_id: str
    action: str
    result: str
    cause: str = None
    timestamp: datetime.datetime = None


# Classe para representar os usuários do sistema
class UserSchema(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        schema_extra = {
            "schema_user": {
                "name": "Teste",
                "email": "teste@mail.com",
                "password": "123",
            }
        }


# Classe para o login dos usuários
class LoginUserSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        schema_extra = {"email": "teste@mail.com", "password": "123"}
