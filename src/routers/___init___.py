from fastapi import APIRouter

from src.routers.test import router as test_router

main_router = APIRouter()

main_router.include_router(test_router)