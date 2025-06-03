from fastapi import APIRouter

from src.routers.users import router as users_router
from src.routers.upload import router as upload_router

main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(upload_router)