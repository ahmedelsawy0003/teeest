"""نموذج التنبيهات."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..utils.enums import NotificationType


class Notification(Base):
    """تنبيه مرتبط بمستخدم محدد."""

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text)
    notification_type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type"), default=NotificationType.SYSTEM
    )
    related_to: Mapped[str | None] = mapped_column(String(100), nullable=True)
    related_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

    def __repr__(self) -> str:
        """تمثيل نصي للتنبيه."""

        return f"Notification(id={self.id!r}, user={self.user_id!r})"
