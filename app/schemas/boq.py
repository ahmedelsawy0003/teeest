"""مخططات بنود الكميات."""
from __future__ import annotations

from pydantic import BaseModel, Field

from ..utils.enums import BoqCategory, BoqUnit
from .common import AuditInfo


class BoqBase(BaseModel):
    """الحقول المشتركة."""

    project_id: int = Field(..., description="معرف المشروع")
    item_code: str = Field(..., min_length=1, max_length=50, description="رقم البند")
    item_name: str = Field(..., min_length=1, max_length=255, description="اسم البند")
    description: str | None = Field(default=None, description="الوصف")
    category: BoqCategory = Field(default=BoqCategory.OTHER, description="التصنيف")
    quantity: float = Field(default=0.0, ge=0, description="الكمية")
    unit: BoqUnit = Field(default=BoqUnit.PIECE, description="الوحدة")
    unit_price: float = Field(default=0.0, ge=0, description="سعر الوحدة")
    actual_quantity: float = Field(default=0.0, ge=0, description="الكمية المنفذة")
    supplier_id: int | None = Field(default=None, description="المورد")
    notes: str | None = Field(default=None, description="ملاحظات")


class BoqCreate(BoqBase):
    """إنشاء بند."""


class BoqUpdate(BaseModel):
    """تحديث بند."""

    item_name: str | None = None
    description: str | None = None
    category: BoqCategory | None = None
    quantity: float | None = Field(None, ge=0)
    unit: BoqUnit | None = None
    unit_price: float | None = Field(None, ge=0)
    actual_quantity: float | None = Field(None, ge=0)
    supplier_id: int | None = None
    notes: str | None = None


class BoqRead(BoqBase, AuditInfo):
    """عرض بند."""

    id: int
    total_price: float

    model_config = {
        "from_attributes": True,
    }
