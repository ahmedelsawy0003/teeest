"""اعتمادات FastAPI المشتركة."""
from __future__ import annotations

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session


async def get_db_session() -> AsyncSession:
    """إرجاع جلسة قاعدة بيانات."""

    async for session in get_session():
        return session
    raise RuntimeError("تعذر إنشاء جلسة قاعدة البيانات")


def pagination_params(page: int = Query(1, ge=1), size: int = Query(25, ge=1, le=200)) -> dict[str, int]:
    """إرجاع إعدادات الترقيم."""

    return {"page": page, "size": size}
