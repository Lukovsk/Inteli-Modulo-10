from fastapi import APIRouter, Depends, Body
from auth.jwt_handler import signJWT
from auth.jwt_bearer import jwtBearer
from db import database, User
from schemas import UserSchema, LoginUserSchema

app = APIRouter(prefix="/user", tags=["user"])


# return all users
@app.get("/", tags=["user"])
async def read_users():
    if not database.is_connected:
        await database.connect()

    return await User.objects.all()


# return user by id
@app.get("/{id}", tags=["user"])
async def get_user_by_id(user_id: int):
    if not database.is_connected:
        await database.connect()

    return await User.objects.get(id=user_id)


# create a user
@app.post("/signup", tags=["user"])
async def sign_up(user: UserSchema = Body(default=None)):
    if not database.is_connected:
        await database.connect()

    await User.objects.create(name=user.name, email=user.email, password=user.password)
    return signJWT((await User.objects.get(email=user.email)).id)


# Função que verifica os dados do usuário
async def check_user(data: LoginUserSchema):
    if not database.is_connected:
        await database.connect()

    users = await User.objects.all()
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


# Recebe uma requisição do POST para logar um usuário
@app.post("/login", tags=["user"])
async def user_login(user: UserSchema = Body(default=None)):
    if check_user(user):
        return signJWT((await User.objects.get(email=user.email)).id)
    return {"error": "Dados inválidos"}


@app.delete("/{id}")
async def delete(id: int):
    if not database.is_connected:
        await database.connect()

    return await User.objects.delete(id=id)
