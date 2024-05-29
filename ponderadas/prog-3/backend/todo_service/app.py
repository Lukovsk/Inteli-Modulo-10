from fastapi import FastAPI
from db.db import database, Todo
from routes import todo_app
import uvicorn

app = FastAPI()

app.include_router(todo_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
