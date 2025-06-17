from src.core.db_methods import BaseDAO
from src.models.upload import UploadedFile


class UploadDAO(BaseDAO):
    model = UploadedFile
