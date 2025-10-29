"""خدمات سجل التدقيق."""
from __future__ import annotations

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import AuditLog
from ..schemas.audit import AuditLogCreate


async def log_action(session: AsyncSession, data: AuditLogCreate, request: Request | None = None) -> AuditLog:
    """تسجيل إجراء في قاعدة البيانات."""

    payload = data.model_dump()
    if request:
        payload.setdefault("ip_address", request.client.host if request.client else None)
    audit_log = AuditLog(**payload)
    session.add(audit_log)
    await session.commit()
    await session.refresh(audit_log)
    return audit_log
