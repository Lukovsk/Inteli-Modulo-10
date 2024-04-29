from pydantic import BaseModel, Field, EmailStr

class TaskSchema(BaseModel):
    id : int = Field(default=None, gt=0)
    title: str = Field(default=None)
    content: str = Field(default=None)
    user_id: int = Field(default=None)
    # Configuração criada para documentação do modelo
    class Config:
        schema_extra = {
            "post_teste" : {
                "title": "Post Teste",
                "content": "Conteúdo do post teste",
                "user_id": 1
            }
        }

# Classe para representar os usuários do sistema
class UserSchema(BaseModel):
    id : int = Field(default=None, gt=0)
    name : str = Field(default=None)
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    class Config:
        schema_extra = {
            "schema_user" : {
                "name": "Teste",
                "email": "teste@mail.com",
                "password":"123"
            }
        }
# Classe para o login dos usuários
class LoginUserSchema(BaseModel):
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    class Config:
        schema_extra = {
            "user_teste" : {
                "email": "teste@mail.com",
                "password":"123"
            }
        }