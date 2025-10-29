"""أدوات التحقق من الصلاحيات."""
from __future__ import annotations

from functools import wraps
from typing import Any, Awaitable, Callable, Coroutine

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..config import settings
from ..database import get_session
from ..models import Project, User
from ..utils.constants import ERROR_MESSAGES
from ..utils.enums import UserRole
from .security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
) -> User:
    """جلب المستخدم الحالي من الرمز."""

    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, ERROR_MESSAGES["unauthorized"])
    try:
        payload = decode_token(token)
    except ValueError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, ERROR_MESSAGES["unauthorized"]) from exc
    user_id = int(payload.get("sub"))
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, ERROR_MESSAGES["unauthorized"])
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "الحساب غير مفعل")
    return user


def require_role(*roles: UserRole) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Coroutine[Any, Any, Any]]]:
    """التحقق من امتلاك المستخدم دوراً معيناً."""

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
        @wraps(func)
        async def wrapper(*args: Any, current_user: User = Depends(get_current_user), **kwargs: Any) -> Any:
            if roles and current_user.role not in roles:
                raise HTTPException(status.HTTP_403_FORBIDDEN, ERROR_MESSAGES["forbidden"])
            return await func(*args, current_user=current_user, **kwargs)

        return wrapper

    return decorator


async def ensure_project_access(project_id: int, user: User, session: AsyncSession) -> Project:
    """التأكد من إمكانية وصول المستخدم للمشروع."""

    result = await session.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    if user.role == UserRole.ADMIN:
        return project
    if user.role == UserRole.PROJECT_MANAGER and project.manager_id == user.id:
        return project
    raise HTTPException(status.HTTP_403_FORBIDDEN, ERROR_MESSAGES["forbidden"])
