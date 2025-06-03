from src.db.DataBase import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
