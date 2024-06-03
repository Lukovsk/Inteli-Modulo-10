from fastapi import BackgroundTasks, FastAPI, HTTPException, UploadFile, File
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
from decouple import config
import shutil


app = FastAPI(debug=True)
logger = LoggerClient(service="image", route="image")

NOTIFY_SERVICE_URL = config("NOTIFY_SERVICE_URL", "http://localhost:8005")


class ImageProcessResult(BaseModel):
    image_id: str
    status: str
    detail: str


files_dir = Path("files")
files_dir.mkdir(parents=True, exist_ok=True)

from supabase import create_client, Client

supabase_url = config("SUPABASE_URL")
supabase_key = config("SUPABASE_API_KEY")
bucket_name = config("SUPABASE_BUCKET")
print(supabase_url)
supabase: Client = create_client(supabase_url, supabase_key)


@app.get("/{user_id}")
async def get_image(user_id: str):
    try:
        images = supabase.storage.from_(bucket_name).list(path=f"profiles/{user_id}/")
        image = supabase.storage.from_(bucket_name).get_public_url(
            path=f"profiles/{user_id}/{images[0]['name']}"
        )
        return image
    except IndexError:
        raise HTTPException(status_code=404, detail="Could not find image")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Got error finding image: {str(e)}"
        )


supabase_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(supabase_dir, "files")


@app.post("/upload/{user_id}")
async def upload_image(user_id: str, file: UploadFile = File(...)):

    file_name = f"{file.filename}"
    supa_path = f"profiles/{user_id}/{file_name}"

    try:
        with open(f"{file_path}/{file_name}", "wb") as w:
            shutil.copyfileobj(file.file, w)
            with open(f"{file_path}/{file_name}", "+rb") as r:
                content = r.read()

                supa_pictures = supabase.storage.from_(bucket_name).list(
                    path=f"profiles/{user_id}"
                )
                if len(supa_pictures) > 0:
                    for picture in supa_pictures:
                        supabase.storage.from_(bucket_name).remove(
                            paths=[f"profiles/{user_id}/{str(picture['name'])}"]
                        )

                supabase.storage.from_(bucket_name).upload(path=supa_path, file=content)

        image_url = f"{supabase_url}/storage/v1/object/public/{bucket_name}/{file_name}"

        return {"message": "Imagem salva com sucesso", "image_url": image_url}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao salvar a imagem: {str(e)}"
        )
    finally:
        if os.path.exists(f"{file_path}/{file_name}"):
            os.remove(f"{file_path}/{file_name}")


@app.post("/rembg/{user_id}")
async def remove_background(user_id: str, background_tasks: BackgroundTasks):
    try:
        image = supabase.storage.from_(bucket_name).list(path=f"profiles/{user_id}/")[0]
        file = supabase.storage.from_(bucket_name).download(
            path=f"profiles/{user_id}/{image['name']}"
        )
        file_location = files_dir / image["name"]
        async with aiofiles.open(file_location, "wb") as out_file:
            await out_file.write(file)

        background_tasks.add_task(
            process_image, file_location, user_id, f"nobg-{image['name']}"
        )
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


async def process_image(file_location: Path, user_id: str, file_name: str):
    await logger.log(
        user_id="System", action="start_image_processing", result="success", cause=None
    )
    try:
        await remove_back(file_location, user_id, file_name)

        # result = ImageProcessResult(
        #     image_id=image_id, status="processed", detail="Image processed successfully"
        # )
        # requests.post(f"{NOTIFY_SERVICE_URL}/", json=result.dict())

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


async def remove_back(input_path: Path, user_id: str, file_name: str):
    try:
        input_image = Image.open(input_path)
        output_image = remove_bg(input_image)
        file = output_image.tobytes()

        supa_path = f"profiles/{user_id}/{file_name}"
        supabase.storage.from_(bucket_name).upload(path=supa_path, file=file)
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
