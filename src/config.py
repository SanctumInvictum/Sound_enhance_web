from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str

    S3_AWS_ACCESS_KEY_ID: str = Field(..., env="S3_AWS_ACCESS_KEY_ID")
    S3_AWS_SECRET_ACCESS_KEY: str = Field(..., env="S3_AWS_SECRET_ACCESS_KEY")
    S3_URL: str = Field(..., env="S3_URL")
    S3_BUCKET_NAME: str = Field(..., env="S3_BUCKET_NAME")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
print(settings.model_dump())