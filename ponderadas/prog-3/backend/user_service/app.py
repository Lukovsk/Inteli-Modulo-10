from fastapi import FastAPI
from db.db import database, User
from routes import user_app
import uvicorn

app = FastAPI()

app.include_router(user_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
