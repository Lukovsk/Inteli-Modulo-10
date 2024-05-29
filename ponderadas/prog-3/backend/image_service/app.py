from fastapi import BackgroundTasks, FastAPI, UploadFile, File
import aiofiles
import requests
import os
from pydantic import BaseModel
import uvicorn
from logger import LoggerClient
from pathlib import Path
from rembg import remove as remove_bg
from PIL import Image
from datetime import datetime
import io

app = FastAPI(debug=True)
logger = LoggerClient(service="image", route="image")

NOTIFY_SERVICE_URL = os.getenv("NOTIFY_SERVICE_URL", "http://localhost:8005")


class ImageProcessResult(BaseModel):
    image_id: str
    status: str
    detail: str


files_dir = Path("files")
files_dir.mkdir(parents=True, exist_ok=True)


@app.post("/upload")
async def upload_image(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        file_location = files_dir / file.filename
        async with aiofiles.open(file_location, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        background_tasks.add_task(process_image, file_location)
        return {"info": "Image uploaded successfully"}
    except Exception as e:
        print(f"Error uploading image: {e}")
        await logger.log(
            user_id="System",
            action="error_uploading_image",
            result="error",
            cause=str(e),
        )
        return {"error": "Failed to upload image"}


async def process_image(file_location: Path):
    await logger.log(
        user_id="System", action="start_image_processing", result="success", cause=None
    )
    try:
        image_id = file_location.stem
        now = datetime.now()
        output_path = file_location.with_name(
            f"{now.strftime('%d-%H-%M-%S')}_{file_location.stem}_nobg.png"
        )
        await remove_background(file_location, output_path)

        result = ImageProcessResult(
            image_id=image_id, status="processed", detail="Image processed successfully"
        )
        requests.post(f"{NOTIFY_SERVICE_URL}/", json=result.dict())

        await logger.log(
            user_id="System",
            action="finish_image_processing",
            result="success",
            cause=None,
        )
    except Exception as e:
        await logger.log(
            user_id="System",
            action="image_processing_failed",
            result="error",
            cause=str(e),
        )
    finally:
        try:
            file_location.unlink()
        except Exception as e:
            print(f"Failed to delete file: {e}")
            await logger.log(
                user_id="System",
                action="image_deleting_failed",
                result="error",
                cause=str(e),
            )


async def remove_background(input_path: Path, output_path: Path):
    try:
        input_image = Image.open(input_path)
        output_image = remove_bg(input_image)
        output_image.save(output_path)
    except Exception as e:
        print(f"Failed to remove background: {e}")
        await logger.log(
            user_id="System",
            action="background_removing_failed",
            result="error",
            cause=str(e),
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
