"""مخططات الموردين."""
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

from .common import AuditInfo


class SupplierBase(BaseModel):
    """بيانات المورد الأساسية."""

    company_name: str = Field(..., min_length=2, max_length=255, description="اسم الشركة")
    tax_number: str | None = Field(default=None, description="الرقم الضريبي")
    contact_person: str | None = Field(default=None, description="مسؤول التواصل")
    phone: str | None = Field(default=None, description="الهاتف")
    email: EmailStr | None = Field(default=None, description="البريد الإلكتروني")
    address: str | None = Field(default=None, description="العنوان")
    city: str | None = Field(default=None, description="المدينة")
    specialty: str | None = Field(default=None, description="التخصص")
    rating: float = Field(default=0.0, ge=0, le=5, description="التقييم")
    notes: str | None = Field(default=None, description="ملاحظات")
    is_active: bool = Field(default=True, description="الحالة")


class SupplierCreate(SupplierBase):
    """إنشاء مورد."""


class SupplierUpdate(BaseModel):
    """تحديث بيانات المورد."""

    company_name: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    city: str | None = None
    specialty: str | None = None
    rating: float | None = Field(None, ge=0, le=5)
    notes: str | None = None
    is_active: bool | None = None


class SupplierRead(SupplierBase, AuditInfo):
    """عرض بيانات المورد."""

    id: int
    supplier_code: str
    total_transactions: int
    total_amount: float

    model_config = {
        "from_attributes": True,
    }
