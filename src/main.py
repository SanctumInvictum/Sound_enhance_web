from fastapi import FastAPI
from contextlib import asynccontextmanager
import datetime
from src.routers.___init___ import main_router
from src.core.dependencies import get_s3_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"start time: {start_time}")

    try:
        s3_client = await get_s3_client()
        test_data = b"test"
        await s3_client.upload_file(test_data, "connection_test.txt")
    except Exception as e:
        print(f"⚠️ MinIO connection failed: {str(e)}")

    yield

app = FastAPI(lifespan=lifespan, debug=True)


app.include_router(main_router)
