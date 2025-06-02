from fastapi import APIRouter

from src.routers.test import router as test_router
from src.routers.users import router as users_router

main_router = APIRouter()

main_router.include_router(test_router)
main_router.include_router(users_router)