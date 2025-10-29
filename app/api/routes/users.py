"""إدارة المستخدمين."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.permissions import get_current_user
from ...crud import user_crud
from ...dependencies import get_db_session
from ...models import User
from ...schemas import PaginatedResponse, Pagination, UserRead, UserUpdate
from ...utils.constants import ERROR_MESSAGES

router = APIRouter(prefix="/users", tags=["المستخدمون"])


@router.get("/", response_model=PaginatedResponse[UserRead], summary="قائمة المستخدمين")
async def list_users(
    page: int = 1,
    size: int = 25,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[UserRead]:
    """إرجاع قائمة المستخدمين مع الترقيم."""

    if current_user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, ERROR_MESSAGES["forbidden"])
    skip = (page - 1) * size
    users = await user_crud.get_multi(session, skip=skip, limit=size)
    total = len(await user_crud.get_multi(session, skip=0, limit=1000))
    return PaginatedResponse(
        data=[UserRead.model_validate(user) for user in users],
        pagination=Pagination(page=page, size=size, total=total),
    )


@router.patch("/{user_id}", response_model=UserRead, summary="تحديث مستخدم")
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """تحديث بيانات مستخدم."""

    if current_user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, ERROR_MESSAGES["forbidden"])
    user = await user_crud.get(session, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    updated = await user_crud.update(session, db_obj=user, obj_in=user_in)
    return UserRead.model_validate(updated)
