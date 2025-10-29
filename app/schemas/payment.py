"""مخططات الدفعات."""
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field

from ..utils.enums import PaymentMethod, PaymentStatus
from .common import AuditInfo


class PaymentBase(BaseModel):
    """البيانات الأساسية للدفعة."""

    project_id: int = Field(..., description="المشروع")
    supplier_id: int | None = Field(default=None, description="المورد")
    supply_order_id: int | None = Field(default=None, description="طلب التوريد")
    payment_type: str = Field(..., description="نوع الدفعة")
    payment_date: date | None = Field(default=None, description="تاريخ الدفع")
    amount: float = Field(..., ge=0, description="المبلغ")
    vat_amount: float = Field(default=0.0, ge=0, description="ضريبة القيمة المضافة")
    total_amount: float = Field(default=0.0, ge=0, description="الإجمالي")
    payment_method: PaymentMethod = Field(default=PaymentMethod.BANK_TRANSFER, description="طريقة الدفع")
    check_number: str | None = Field(default=None, description="رقم الشيك")
    bank_name: str | None = Field(default=None, description="اسم البنك")
    transaction_reference: str | None = Field(default=None, description="رقم العملية")
    status: PaymentStatus = Field(default=PaymentStatus.PENDING, description="حالة الدفعة")
    notes: str | None = Field(default=None, description="ملاحظات")


class PaymentCreate(PaymentBase):
    """إنشاء دفعة."""


class PaymentUpdate(BaseModel):
    """تحديث الدفعة."""

    payment_type: str | None = None
    payment_date: date | None = None
    amount: float | None = Field(None, ge=0)
    vat_amount: float | None = Field(None, ge=0)
    total_amount: float | None = Field(None, ge=0)
    payment_method: PaymentMethod | None = None
    check_number: str | None = None
    bank_name: str | None = None
    transaction_reference: str | None = None
    status: PaymentStatus | None = None
    notes: str | None = None


class PaymentRead(PaymentBase, AuditInfo):
    """عرض الدفعة."""

    id: int
    payment_code: str
    attachment_path: str | None
    approved_by: int | None
    approved_at: datetime | None

    model_config = {
        "from_attributes": True,
    }
