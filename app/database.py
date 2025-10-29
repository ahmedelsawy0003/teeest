"""إعداد الاتصال بقاعدة البيانات باستخدام SQLAlchemy غير المتزامن."""
from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


class Base(DeclarativeBase):
    """قاعدة النماذج لجميع الكيانات."""


engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """تزويد جلسة قاعدة البيانات وإغلاقها بأمان."""

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
