from pydantic import BaseModel
from datetime import datetime


class UploadedFileResponse(BaseModel):
    id: str
    original_filename: str
    stored_filename: str
    content_type: str
    upload_time: datetime

    class Config:
        from_attributes = True
