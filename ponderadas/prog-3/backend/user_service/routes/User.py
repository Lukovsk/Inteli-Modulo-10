from fastapi import APIRouter, Body
from auth.jwt_handler import signJWT
from db import database, User
from schemas import UserSchema, LoginUserSchema
from controllers import LoggerClient

app = APIRouter(prefix="/user", tags=["user"])

logger = LoggerClient(service="user", route="user")


# return all users
@app.get("/", tags=["user"])
async def read_users():
    if not database.is_connected:
        await database.connect()

    await logger.log(user_id="Admin", action="get all users")
    return await User.objects.all()


# return user by id
@app.get("/{id}", tags=["user"])
async def get_user_by_id(user_id: int):
    if not database.is_connected:
        await database.connect()

    await logger.log(user_id=user_id, action="get user by id")
    return await User.objects.get(id=user_id)


# create a user
@app.post("/signup", tags=["user"])
async def sign_up(user: UserSchema = Body(default=None)):
    if not database.is_connected:
        await database.connect()

    new_user = await User.objects.create(
        name=user.name, email=user.email, password=user.password
    )
    await logger.log(user_id=new_user.id, action="created user (signup action)")
    return signJWT(new_user.id)


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
async def user_login(body: UserSchema = Body(default=None)):

    if check_user(body):
        user = await User.objects.get(email=body.email)
        await logger.log(user_id=user.id, action="user login")
        return signJWT(user.id)

    await logger.log(
        user_id=body.email,
        action="user login",
        result="failed",
        cause="invalid data",
    )

    return {"error": "Dados inválidos"}


@app.delete("/{id}")
async def delete(id: int):
    if not database.is_connected:
        await database.connect()

    await logger.log(user_id=id, action="deleting user")
    return await User.objects.delete(id=id)
