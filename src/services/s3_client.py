from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from botocore.exceptions import ClientError


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
        self,
        file_bytes: bytes,
        object_name: str,
        content_type: str = "application/octet-stream"
    ):
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file_bytes,
                    ContentType=content_type
                )
                print(f"File {object_name} uploaded to {self.bucket_name}")
                return True
        except ClientError as e:
            print(f"Error uploading file: {e}")
            return False

    async def download_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(
                    Bucket=self.bucket_name,
                    Key=object_name
                )
                async with response["Body"] as stream:
                    data = await stream.read()
                    return data
        except ClientError as e:
            print(f"Error downloading file: {e}")
            return None

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(
                    Bucket=self.bucket_name,
                    Key=object_name
                )
                print(f"File {object_name} deleted from {self.bucket_name}")
                return True
        except ClientError as e:
            print(f"Error deleting file: {e}")
            return False

    async def get_file(self, object_name: str, destination_path: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                with open(destination_path, "wb") as file:
                    file.write(data)
                print(f"File {object_name} downloaded to {destination_path}")
        except ClientError as e:
            print(f"Error downloading file: {e}")
