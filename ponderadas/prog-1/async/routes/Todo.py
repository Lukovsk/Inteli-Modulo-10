from fastapi import APIRouter, Depends, Body
from schemas import TaskSchema
from auth.jwt_bearer import jwtBearer
from db import database, Task


app = APIRouter(prefix="/todo", tags=["todo"])


# return all tasks
@app.get("/")
async def read_tasks():
    if not database.is_connected:
        await database.connect()

    return await Task.objects.all()


# retur task by id
@app.get("/id:{id}", tags=["task"])
async def get_task_by_id(id: int):
    if not database.is_connected:
        await database.connect()

    return await Task.objects.get(id=id)


# return all tasks by a user id
@app.get("/user:{user_id}", tags=["task"])
async def get_task_by_id(user_id: int):
    if not database.is_connected:
        await database.connect()

    return await Task.objects.all(user_id=user_id)


# create a task
@app.post("/", dependencies=[Depends(jwtBearer())], tags=["task"])
async def create_task(task: TaskSchema = Body(default=None)):
    if not database.is_connected:
        await database.connect()

    await Task.objects.create(
        title=task.title, content=task.content, user_id=task.user_id
    )
    return {"success": "Successfully created"}


@app.put("/", dependencies=[Depends(jwtBearer())])
async def update_task(new_task: TaskSchema):
    if not database.is_connected:
        await database.connect()

    return await Task.objects.update_or_create(
        id=new_task.id,
        title=new_task.title,
        content=new_task.content,
        user_id=new_task.user_id,
    )


@app.delete("/{id}", dependencies=[Depends(jwtBearer())])
async def delete_task(id: int):
    if not database.is_connected:
        await database.connect()

    return await Task.objects.delete(id=id)
