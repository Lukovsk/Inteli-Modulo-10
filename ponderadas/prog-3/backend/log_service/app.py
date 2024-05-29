from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import uvicorn

app = FastAPI()

fake_db = {
    "log": [],
    "user": [],
    "todo": [],
    "notify": [],
    "image": [],
}


class LogEntry(BaseModel):
    service: str
    user_id: str
    action: str
    result: str
    cause: str = None
    timestamp: datetime.datetime = None


@app.post("/log")
async def log_action(log_entry: LogEntry):
    if not log_entry.timestamp:
        log_entry.timestamp = datetime.datetime.now()

    print(f"Log: {log_entry}")
    fake_db["log"].append(log_entry)
    return {"status": "success", "log": log_entry}


@app.post("/user")
async def user_action(log_entry: LogEntry):
    if not log_entry.timestamp:
        log_entry.timestamp = datetime.datetime.now()

    print(f"Log: {log_entry}")
    fake_db["user"].append(log_entry)

    return {"status": "success", "log": log_entry}


@app.post("/todo")
async def todo_action(log_entry: LogEntry):
    if not log_entry.timestamp:
        log_entry.timestamp = datetime.datetime.now()

    print(f"Log: {log_entry}")
    fake_db["todo"].append(log_entry)

    return {"status": "success", "log": log_entry}


@app.post("/notify")
async def notify_action(log_entry: LogEntry):
    if not log_entry.timestamp:
        log_entry.timestamp = datetime.datetime.now()

    print(f"Log: {log_entry}")
    fake_db["notify"].append(log_entry)

    return {"status": "success", "log": log_entry}


@app.post("/image")
async def image_action(log_entry: LogEntry):
    if not log_entry.timestamp:
        log_entry.timestamp = datetime.datetime.now()

    print(f"Log: {log_entry}")
    fake_db["image"].append(log_entry)

    return {"status": "success", "log": log_entry}


@app.post("/ping")
async def ping():
    return {"status": "success"}


@app.get("/")
async def get_logs():
    return fake_db


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
