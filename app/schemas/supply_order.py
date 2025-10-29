"""مخططات طلبات التوريد."""
from __future__ import annotations

from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field

from ..utils.enums import OrderStatus
from .common import AuditInfo


class SupplyOrderItemBase(BaseModel):
    """الحقول المشتركة لعناصر الطلب."""

    boq_item_id: int = Field(..., description="معرف بند الكميات")
    quantity_ordered: float = Field(..., ge=0, description="الكمية المطلوبة")
    quantity_delivered: float = Field(default=0.0, ge=0, description="الكمية المستلمة")
    unit_price: float = Field(..., ge=0, description="سعر الوحدة")
    notes: str | None = Field(default=None, description="ملاحظات")


class SupplyOrderItemCreate(SupplyOrderItemBase):
    """إنشاء عنصر."""


class SupplyOrderItemRead(SupplyOrderItemBase):
    """عرض عنصر."""

    id: int
    total_price: float

    model_config = {
        "from_attributes": True,
    }


class SupplyOrderBase(BaseModel):
    """الحقول الأساسية للطلب."""

    project_id: int = Field(..., description="المشروع")
    supplier_id: int = Field(..., description="المورد")
    order_date: date | None = Field(default=None, description="تاريخ الطلب")
    expected_delivery_date: date | None = Field(default=None, description="التسليم المتوقع")
    actual_delivery_date: date | None = Field(default=None, description="التسليم الفعلي")
    status: OrderStatus = Field(default=OrderStatus.DRAFT, description="حالة الطلب")
    notes: str | None = Field(default=None, description="ملاحظات")


class SupplyOrderCreate(SupplyOrderBase):
    """إنشاء طلب."""

    items: List[SupplyOrderItemCreate] = Field(default_factory=list, description="العناصر")


class SupplyOrderUpdate(BaseModel):
    """تحديث طلب."""

    supplier_id: int | None = None
    order_date: date | None = None
    expected_delivery_date: date | None = None
    actual_delivery_date: date | None = None
    status: OrderStatus | None = None
    notes: str | None = None
    items: List[SupplyOrderItemCreate] | None = None


class SupplyOrderRead(SupplyOrderBase, AuditInfo):
    """عرض الطلب."""

    id: int
    order_code: str
    total_amount: float
    vat_amount: float
    total_with_vat: float
    created_by: int | None
    approved_by: int | None
    approved_at: datetime | None
    items: List[SupplyOrderItemRead] = []

    model_config = {
        "from_attributes": True,
    }
