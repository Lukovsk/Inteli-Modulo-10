from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests
import uvicorn
from logger import LoggerClient

app = FastAPI()

# URL do aplicativo Flutter para notificação
FLUTTER_APP_URL = os.getenv("FLUTTER_APP_URL", "http://localhost:8002")
logger = LoggerClient(service="notify", route="notify")


class Notification(BaseModel):
    image_id: str
    status: str
    detail: str


# Modifique a função notify para incluir logs
@app.post("/notify")
async def notify(notification: Notification):
    logger.log(
        user_id="System", action="send_notification", result="success", cause=None
    )
    response = requests.post(
        f"{FLUTTER_APP_URL}/notification/", json=notification.dict()
    )
    if response.status_code != 200:
        logger.log(
            user_id="system",
            action="notification_failed",
            result="error",
            cause=response.content,
        )
        raise HTTPException(
            status_code=response.status_code, detail="Failed to notify Flutter app"
        )
    return {"status": "Notification sent successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
