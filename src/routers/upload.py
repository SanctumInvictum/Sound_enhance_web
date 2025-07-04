from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Request

from src.core.rabbit_dependencies import get_rabbitmq_client
from src.dao.upload import UploadDAO
from src.services.rabbit_client import AsyncRabbitMQClient
from src.services.s3_client import S3Client
from src.core.users_dependencies import get_current_user
from src.core.s3_dependencies import get_s3_client
from src.models.users import Users


router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/upload_file")
async def upload(
        file: UploadFile = File(...),
        user: Users = Depends(get_current_user),
        s3_client: S3Client = Depends(get_s3_client),
        rabbit_client: AsyncRabbitMQClient = Depends(get_rabbitmq_client)
):
    if file.content_type not in ["audio/wav", "audio/mpeg", "video/mp4"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_bytes = await file.read()
    stored_filename = f"{uuid4()}_{file.filename}"
    await s3_client.upload_file(
        file_bytes=file_bytes,
        object_name=stored_filename,
        content_type=file.content_type
    )

    await UploadDAO.add(
        user_id=user.id,
        original_filename=file.filename,
        stored_filename=stored_filename,
        content_type=file.content_type,
    )
    # отправляем в очередь
    await rabbit_client.send(
        {"stored_filename": stored_filename, "user_id": user.id},
        queue_name="preprocessing_queue"
    )

    return {"status": "uploaded", "stored_filename": stored_filename}


@router.get("/all_user_files")
async def my_files(
    user: Users = Depends(get_current_user)
):
    pass