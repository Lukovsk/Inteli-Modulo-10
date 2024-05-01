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
@app.get("/id:{id}", tags=["todo"])
async def get_task_by_id(id: int):
    if not database.is_connected:
        await database.connect()

    return await Todo.objects.get(id=id)


# return all todos by a user id
@app.get("/user:{user_id}", tags=["todo"])
async def get_task_by_id(user_id: int):
    if not database.is_connected:
        await database.connect()

    return await Todo.objects.all(user_id=user_id)


# create a todo
@app.post("/", dependencies=[Depends(jwtBearer())], tags=["todo"])
async def create_task(todo: TaskSchema = Body(default=None)):
    if not database.is_connected:
        await database.connect()

    await Todo.objects.create(
        title=todo.title, content=todo.content, user_id=todo.user_id
    )
    return {"success": "Successfully created"}


@app.put("/", dependencies=[Depends(jwtBearer())])
async def update_task(new_task: TaskSchema):
    if not database.is_connected:
        await database.connect()

    return await Todo.objects.update_or_create(
        id=new_task.id,
        title=new_task.title,
        content=new_task.content,
        user_id=new_task.user_id,
    )


@app.delete("/{id}", dependencies=[Depends(jwtBearer())])
async def delete_task(id: int):
    if not database.is_connected:
        await database.connect()

    return await Todo.objects.delete(id=id)
