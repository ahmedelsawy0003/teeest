"""مخططات سجل التدقيق."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class AuditLogCreate(BaseModel):
    """إنشاء سجل تدقيق."""

    user_id: int | None = Field(default=None, description="المستخدم")
    action: str = Field(..., description="الإجراء")
    entity_type: str = Field(..., description="نوع الكيان")
    entity_id: int | None = Field(default=None, description="معرف الكيان")
    details: dict | None = Field(default=None, description="تفاصيل إضافية")
    ip_address: str | None = Field(default=None, description="عنوان IP")
    description: str | None = Field(default=None, description="وصف")


class AuditLogRead(AuditLogCreate):
    """عرض سجل التدقيق."""

    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
