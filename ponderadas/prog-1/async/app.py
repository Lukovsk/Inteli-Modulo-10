from fastapi import FastAPI
from routes import user_app, todo_app
from db.db import database, User, Todo
import uvicorn

app = FastAPI()

app.include_router(user_app)
app.include_router(todo_app)

if __name__ == '__main__':
    uvicorn.run(app)