import datetime

from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["Tests"]
)


@router.get("/health_check", tags=["health check"])
async def root() -> dict[str, str]:
    return {"msg":"Hello World"}


@router.get("/ping")
async def ping() -> None:
    ping_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"ping time: {ping_time}")
