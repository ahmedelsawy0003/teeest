"""واجهات التنبيهات."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.permissions import get_current_user
from ...dependencies import get_db_session
from ...models import Notification, User
from ...schemas import NotificationRead
from ...utils.constants import ERROR_MESSAGES

router = APIRouter(prefix="/notifications", tags=["التنبيهات"])


@router.get("/", response_model=list[NotificationRead], summary="قائمة التنبيهات")
async def list_notifications(
    session: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)
) -> list[NotificationRead]:
    """عرض التنبيهات للمستخدم الحالي."""

    result = await session.execute(select(Notification).where(Notification.user_id == current_user.id))
    notifications = result.scalars().all()
    return [NotificationRead.model_validate(notification) for notification in notifications]


@router.post("/{notification_id}/read", summary="تحديد التنبيه كمقروء")
async def mark_notification(notification_id: int, session: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> dict[str, str]:
    """تحديث حالة التنبيه."""

    notification = await session.get(Notification, notification_id)
    if not notification or notification.user_id != current_user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    notification.is_read = True
    await session.commit()
    return {"message": "تم تحديث التنبيه"}
