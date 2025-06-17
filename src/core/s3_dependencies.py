from src.services.s3_client import S3Client
from src.config import settings


async def get_s3_client():
    if not hasattr(get_s3_client, "client"):
        get_s3_client.client = S3Client(
            access_key=settings.S3_AWS_ACCESS_KEY_ID,
            secret_key=settings.S3_AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.S3_URL,
            bucket_name=settings.S3_BUCKET_NAME
        )

    return get_s3_client.client