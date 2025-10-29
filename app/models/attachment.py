"""نموذج المرفقات."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..utils.enums import AttachmentType


class Attachment(Base):
    """ملفات مرتبطة بالمشاريع أو الكيانات."""

    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    related_to: Mapped[str] = mapped_column(String(100))
    related_id: Mapped[int] = mapped_column(Integer)
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(255))
    file_size: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    file_type: Mapped[AttachmentType] = mapped_column(
        Enum(AttachmentType, name="attachment_type"), default=AttachmentType.DOCUMENT
    )
    uploaded_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    project = relationship(
        "Project",
        primaryjoin="and_(Attachment.related_to=='project', foreign(Attachment.related_id)==Project.id)",
        back_populates="attachments",
        viewonly=True,
    )

    def __repr__(self) -> str:
        """تمثيل نصي للمرفق."""

        return f"Attachment(id={self.id!r}, file_name={self.file_name!r})"
