"""نقاط نهاية التوثيق."""
from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...config import settings
from ...core.permissions import get_current_user
from ...core.security import create_access_token, verify_password
from ...crud import user_crud
from ...dependencies import get_db_session
from ...models import User
from ...schemas import TokenResponse, UserCreate, UserRead
from ...utils.constants import ERROR_MESSAGES
from ...utils.enums import UserRole

router = APIRouter(prefix="/auth", tags=["التوثيق"])


@router.post("/login", response_model=TokenResponse, summary="تسجيل الدخول")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db_session)
) -> TokenResponse:
    """التحقق من بيانات الدخول وإرجاع رمز JWT."""

    user = await user_crud.get_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, ERROR_MESSAGES["invalid_credentials"])
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "الحساب غير مفعل")
    access_token = create_access_token(str(user.id), timedelta(minutes=settings.access_token_expire_minutes))
    return TokenResponse(access_token=access_token, user=UserRead.model_validate(user))


@router.post("/register", response_model=UserRead, summary="إنشاء مستخدم جديد")
async def register_user(
    user_in: UserCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> UserRead:
    """إنشاء مستخدم جديد من قبل المشرف."""

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, ERROR_MESSAGES["forbidden"])
    existing = await user_crud.get_by_username(session, user_in.username)
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "اسم المستخدم مستخدم مسبقاً")
    user = await user_crud.create(session, user_in)
    return UserRead.model_validate(user)


@router.get("/me", response_model=UserRead, summary="عرض بيانات المستخدم الحالي")
async def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    """إرجاع بيانات المستخدم الحالي."""

    return UserRead.model_validate(current_user)
