"""مخططات المرفقات."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from ..utils.enums import AttachmentType


class AttachmentCreate(BaseModel):
    """إنشاء مرفق."""

    related_to: str = Field(..., description="نوع الكيان المرتبط")
    related_id: int = Field(..., description="معرف الكيان")
    file_name: str = Field(..., description="اسم الملف")
    file_path: str = Field(..., description="مسار الملف")
    file_size: float = Field(..., ge=0, description="حجم الملف")
    file_type: AttachmentType = Field(default=AttachmentType.DOCUMENT, description="نوع المرفق")
    uploaded_by: int | None = Field(default=None, description="المستخدم الرافع")


class AttachmentRead(AttachmentCreate):
    """عرض المرفق."""

    id: int
    uploaded_at: datetime

    model_config = {
        "from_attributes": True,
    }
