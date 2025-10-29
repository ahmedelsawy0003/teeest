"""خدمات التنبيه داخل النظام."""
from __future__ import annotations

from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Notification, User
from ..schemas.notification import NotificationCreate


async def create_notification(session: AsyncSession, data: NotificationCreate) -> Notification:
    """إنشاء تنبيه جديد وتخزينه."""

    notification = Notification(**data.model_dump())
    session.add(notification)
    await session.commit()
    await session.refresh(notification)
    return notification


async def notify_roles(session: AsyncSession, roles: Iterable[str], title: str, message: str) -> None:
    """إرسال تنبيه لمجموعة من الأدوار."""

    result = await session.execute(select(User).where(User.role.in_(roles)))
    users = result.scalars().all()
    for user in users:
        session.add(
            Notification(
                user_id=user.id,
                title=title,
                message=message,
            )
        )
    await session.commit()
