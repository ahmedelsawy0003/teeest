"""نموذج سجل التدقيق."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class AuditLog(Base):
    """يسجل الإجراءات الهامة داخل النظام."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(50))
    entity_type: Mapped[str] = mapped_column(String(100))
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="audit_logs")

    def __repr__(self) -> str:
        """تمثيل نصي للسجل."""

        return f"AuditLog(id={self.id!r}, action={self.action!r})"
