"""واجهات المرتجعات."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.permissions import get_current_user
from ...crud import return_crud
from ...dependencies import get_db_session
from ...models import User
from ...schemas import PaginatedResponse, Pagination, ReturnCreate, ReturnRead, ReturnUpdate
from ...utils.constants import ERROR_MESSAGES

router = APIRouter(prefix="/returns", tags=["المرتجعات"])


@router.get("/", response_model=PaginatedResponse[ReturnRead], summary="قائمة المرتجعات")
async def list_returns(
    page: int = 1,
    size: int = 25,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[ReturnRead]:
    """عرض المرتجعات."""

    skip = (page - 1) * size
    items = await return_crud.get_multi(session, skip=skip, limit=size)
    total = len(await return_crud.get_multi(session, skip=0, limit=1000))
    return PaginatedResponse(
        data=[ReturnRead.model_validate(item) for item in items],
        pagination=Pagination(page=page, size=size, total=total),
    )


@router.post("/", response_model=ReturnRead, status_code=201, summary="تسجيل مرتجع")
async def create_return(
    return_in: ReturnCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> ReturnRead:
    """إنشاء مرتجع جديد."""

    record = await return_crud.create(session, return_in)
    record.created_by = current_user.id
    await session.commit()
    await session.refresh(record)
    return ReturnRead.model_validate(record)


@router.patch("/{return_id}", response_model=ReturnRead, summary="تحديث مرتجع")
async def update_return(
    return_id: int,
    return_in: ReturnUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> ReturnRead:
    """تحديث بيانات مرتجع."""

    record = await return_crud.get(session, return_id)
    if not record:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    updated = await return_crud.update(session, db_obj=record, obj_in=return_in)
    return ReturnRead.model_validate(updated)
