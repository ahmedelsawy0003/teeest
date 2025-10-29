"""واجهات طلبات التوريد."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.permissions import get_current_user
from ...crud import supply_order_crud
from ...dependencies import get_db_session
from ...models import User
from ...schemas import PaginatedResponse, Pagination, SupplyOrderCreate, SupplyOrderRead, SupplyOrderUpdate
from ...utils.constants import ERROR_MESSAGES

router = APIRouter(prefix="/supply-orders", tags=["طلبات التوريد"])


@router.get("/", response_model=PaginatedResponse[SupplyOrderRead], summary="قائمة طلبات التوريد")
async def list_orders(
    page: int = 1,
    size: int = 25,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[SupplyOrderRead]:
    """عرض الطلبات."""

    skip = (page - 1) * size
    orders = await supply_order_crud.get_multi(session, skip=skip, limit=size)
    total = len(await supply_order_crud.get_multi(session, skip=0, limit=1000))
    return PaginatedResponse(
        data=[SupplyOrderRead.model_validate(order) for order in orders],
        pagination=Pagination(page=page, size=size, total=total),
    )


@router.post("/", response_model=SupplyOrderRead, status_code=201, summary="إنشاء طلب")
async def create_order(
    order_in: SupplyOrderCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> SupplyOrderRead:
    """إضافة طلب جديد."""

    order = await supply_order_crud.create(session, order_in)
    order.created_by = current_user.id
    await session.commit()
    await session.refresh(order)
    return SupplyOrderRead.model_validate(order)


@router.patch("/{order_id}", response_model=SupplyOrderRead, summary="تحديث طلب")
async def update_order(
    order_id: int,
    order_in: SupplyOrderUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> SupplyOrderRead:
    """تحديث الطلب."""

    order = await supply_order_crud.get(session, order_id)
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    updated = await supply_order_crud.update(session, db_obj=order, obj_in=order_in)
    return SupplyOrderRead.model_validate(updated)
