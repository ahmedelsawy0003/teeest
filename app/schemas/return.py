"""مخططات المرتجعات."""
from __future__ import annotations

from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field

from ..utils.enums import ReturnStatus
from .common import AuditInfo


class ReturnItemBase(BaseModel):
    """البيانات الأساسية لعنصر المرتجع."""

    boq_item_id: int = Field(..., description="معرف بند الكميات")
    quantity_returned: float = Field(..., ge=0, description="الكمية المرتجعة")
    unit_price: float = Field(..., ge=0, description="سعر الوحدة")
    notes: str | None = Field(default=None, description="ملاحظات")


class ReturnItemCreate(ReturnItemBase):
    """إنشاء عنصر."""


class ReturnItemRead(ReturnItemBase):
    """عرض عنصر."""

    id: int
    total_price: float

    model_config = {
        "from_attributes": True,
    }


class ReturnBase(BaseModel):
    """البيانات الأساسية للمرتجع."""

    project_id: int = Field(..., description="المشروع")
    supplier_id: int | None = Field(default=None, description="المورد")
    supply_order_id: int | None = Field(default=None, description="طلب التوريد")
    return_date: date | None = Field(default=None, description="تاريخ المرتجع")
    status: ReturnStatus = Field(default=ReturnStatus.PENDING, description="حالة المرتجع")
    total_amount: float = Field(default=0.0, ge=0, description="القيمة")
    reason: str = Field(..., description="سبب المرتجع")
    reason_details: str | None = Field(default=None, description="تفاصيل إضافية")
    notes: str | None = Field(default=None, description="ملاحظات")


class ReturnCreate(ReturnBase):
    """إنشاء مرتجع."""

    items: List[ReturnItemCreate] = Field(default_factory=list)


class ReturnUpdate(BaseModel):
    """تحديث المرتجع."""

    return_date: date | None = None
    status: ReturnStatus | None = None
    total_amount: float | None = Field(None, ge=0)
    reason: str | None = None
    reason_details: str | None = None
    notes: str | None = None
    items: List[ReturnItemCreate] | None = None


class ReturnRead(ReturnBase, AuditInfo):
    """عرض المرتجع."""

    id: int
    return_code: str
    approved_by: int | None
    approved_at: datetime | None
    items: List[ReturnItemRead] = []

    model_config = {
        "from_attributes": True,
    }
