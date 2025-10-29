"""مخططات المستخدمين."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from ..utils.enums import UserRole


class UserBase(BaseModel):
    """حقول المستخدم الأساسية."""

    username: str = Field(..., min_length=3, max_length=50, description="اسم المستخدم")
    email: EmailStr = Field(..., description="البريد الإلكتروني")
    full_name: str = Field(..., min_length=3, max_length=255, description="الاسم الكامل")
    phone: str | None = Field(default=None, description="رقم الهاتف")
    role: UserRole = Field(default=UserRole.PROJECT_MANAGER, description="دور المستخدم")
    is_active: bool = Field(default=True, description="حالة التفعيل")


class UserCreate(UserBase):
    """إدخال المستخدم الجديد."""

    password: str = Field(..., min_length=8, description="كلمة المرور")


class UserUpdate(BaseModel):
    """تحديث بيانات المستخدم."""

    full_name: Optional[str] = Field(None, min_length=3, max_length=255)
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)


class UserRead(UserBase):
    """عرض بيانات المستخدم."""

    id: int
    avatar: str | None = None
    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class TokenPayload(BaseModel):
    """حمولة رمز الدخول."""

    sub: str
    exp: int


class TokenResponse(BaseModel):
    """استجابة تسجيل الدخول."""

    access_token: str
    token_type: str = "bearer"
    user: UserRead
