from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
)

from internal.config import settings

DATABASE_URL = settings.DB_URL

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def db_session() -> AsyncGenerator[AsyncSession, Any]:
    async with SessionLocal() as session:
        yield session
