from fastapi import APIRouter, Depends, Body
from schemas import TaskSchema
from auth.jwt_bearer import jwtBearer
from db import database, Todo


app = APIRouter(prefix="/todo", tags=["todo"])


# return all todos
@app.get("/")
async def read_tasks():
    if not database.is_connected:
        await database.connect()

    return await Todo.objects.all()


# retur todo by id
@app.get("/id:{id}")
async def get_task_by_id(id: int):
    if not database.is_connected:
        await database.connect()

    return await Todo.objects.get(id=id)


# return all todos by a user id
@app.get("/user:{user_id}")
async def get_task_by_id(user_id: int):
    if not database.is_connected:
        await database.connect()

    return await Todo.objects.all(user_id=user_id)


# create a todo
@app.post("/", dependencies=[Depends(jwtBearer())])
async def create_task(todo: TaskSchema = Body(default=None)):
    if not database.is_connected:
        await database.connect()

    await Todo.objects.create(content=todo.content, user_id=todo.user_id, check=False)
    return {"success": "Successfully created"}


@app.put("/check/{id}", dependencies=[Depends(jwtBearer())])
async def check_todo(id: int):
    if not database.is_connected:
        await database.connect()

    todo = await Todo.objects.get(id=id)

    return await Todo.objects.update_or_create(
        id=todo.id,
        check=not todo.check,
    )


@app.put("/", dependencies=[Depends(jwtBearer())])
async def update_task(new_task: TaskSchema):
    if not database.is_connected:
        await database.connect()

    return await Todo.objects.update_or_create(
        id=new_task.id,
        content=new_task.content,
        user_id=new_task.user_id,
        check=new_task.check,
    )


@app.delete("/{id}", dependencies=[Depends(jwtBearer())])
async def delete_task(id: int):
    if not database.is_connected:
        await database.connect()

    return await Todo.objects.delete(id=id)
