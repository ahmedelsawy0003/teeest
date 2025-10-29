"""مخططات مشتركة بين الكيانات."""
from __future__ import annotations

from datetime import datetime
from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseMessage(BaseModel):
    """نموذج رسالة استجابة بسيطة."""

    message: str = Field(..., description="رسالة باللغة العربية توضّح نتيجة العملية")


class Pagination(BaseModel):
    """تفاصيل الترقيم."""

    page: int = Field(1, ge=1, description="رقم الصفحة الحالية")
    size: int = Field(25, ge=1, le=200, description="عدد العناصر في الصفحة")
    total: int = Field(0, ge=0, description="إجمالي العناصر")


class PaginatedResponse(BaseModel, Generic[T]):
    """استجابة تحتوي على بيانات مع تفاصيل الترقيم."""

    data: Sequence[T]
    pagination: Pagination


class AuditInfo(BaseModel):
    """بيانات الإنشاء والتحديث."""

    created_at: datetime | None = Field(default=None, description="تاريخ الإنشاء")
    updated_at: datetime | None = Field(default=None, description="تاريخ آخر تعديل")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
