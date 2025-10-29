"""مخططات المشاريع."""
from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..utils.enums import ProjectStatus
from .common import AuditInfo
from .user import UserRead


class ProjectBase(BaseModel):
    """بيانات المشروع الأساسية."""

    project_name: str = Field(..., min_length=3, max_length=255, description="اسم المشروع")
    client_name: str = Field(..., description="اسم العميل")
    client_contact: str | None = Field(default=None, description="طريقة التواصل")
    location: str | None = Field(default=None, description="الموقع")
    start_date: date | None = Field(default=None, description="تاريخ البداية")
    expected_end_date: date | None = Field(default=None, description="تاريخ الانتهاء المتوقع")
    actual_end_date: date | None = Field(default=None, description="تاريخ الانتهاء الفعلي")
    status: ProjectStatus = Field(default=ProjectStatus.DRAFT, description="حالة المشروع")
    vat_rate: float = Field(default=15.0, ge=0, description="نسبة الضريبة")
    include_vat: bool = Field(default=True, description="هل الأسعار شاملة للضريبة")
    completion_percentage: float = Field(default=0.0, ge=0, le=100, description="نسبة الإنجاز")
    description: str | None = Field(default=None, description="وصف المشروع")
    notes: str | None = Field(default=None, description="ملاحظات")
    manager_id: int | None = Field(default=None, description="المسؤول")


class ProjectCreate(ProjectBase):
    """إنشاء مشروع جديد."""

    project_code: str | None = Field(default=None, description="كود المشروع")


class ProjectUpdate(BaseModel):
    """تحديث بيانات المشروع."""

    project_name: Optional[str] = Field(None, min_length=3, max_length=255)
    client_name: Optional[str] = None
    client_contact: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    status: Optional[ProjectStatus] = None
    vat_rate: Optional[float] = Field(None, ge=0)
    include_vat: Optional[bool] = None
    completion_percentage: Optional[float] = Field(None, ge=0, le=100)
    description: Optional[str] = None
    notes: Optional[str] = None
    manager_id: Optional[int] = None


class ProjectRead(ProjectBase, AuditInfo):
    """عرض المشروع مع تفاصيل إضافية."""

    id: int
    project_code: str
    total_budget: float
    total_spent: float
    remaining_budget: float
    budget_utilization_percentage: float
    creator: UserRead | None = None

    model_config = {
        "from_attributes": True,
    }
