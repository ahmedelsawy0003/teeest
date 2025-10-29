"""مخططات التنبيهات."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from ..utils.enums import NotificationType


class NotificationBase(BaseModel):
    """الحقول الأساسية للتنبيه."""

    user_id: int = Field(..., description="المستخدم")
    title: str = Field(..., description="عنوان التنبيه")
    message: str = Field(..., description="نص التنبيه")
    notification_type: NotificationType = Field(default=NotificationType.SYSTEM, description="النوع")
    related_to: str | None = Field(default=None, description="الجهة المرتبطة")
    related_id: int | None = Field(default=None, description="المعرف المرتبط")


class NotificationCreate(NotificationBase):
    """إنشاء تنبيه."""


class NotificationRead(NotificationBase):
    """عرض التنبيه."""

    id: int
    is_read: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
