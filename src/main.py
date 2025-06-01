from fastapi import FastAPI
from contextlib import asynccontextmanager
import datetime
from src.routers.___init___ import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"start time: {start_time}")
    yield

app = FastAPI(lifespan=lifespan, debug=True)

app.include_router(main_router)
