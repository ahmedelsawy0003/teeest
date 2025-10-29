"""واجهات الدفعات."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.permissions import get_current_user
from ...crud import payment_crud
from ...dependencies import get_db_session
from ...models import User
from ...schemas import PaginatedResponse, Pagination, PaymentCreate, PaymentRead, PaymentUpdate
from ...utils.constants import ERROR_MESSAGES

router = APIRouter(prefix="/payments", tags=["الدفعات"])


@router.get("/", response_model=PaginatedResponse[PaymentRead], summary="قائمة الدفعات")
async def list_payments(
    page: int = 1,
    size: int = 25,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[PaymentRead]:
    """عرض الدفعات."""

    skip = (page - 1) * size
    payments = await payment_crud.get_multi(session, skip=skip, limit=size)
    total = len(await payment_crud.get_multi(session, skip=0, limit=1000))
    return PaginatedResponse(
        data=[PaymentRead.model_validate(payment) for payment in payments],
        pagination=Pagination(page=page, size=size, total=total),
    )


@router.post("/", response_model=PaymentRead, status_code=201, summary="إضافة دفعة")
async def create_payment(
    payment_in: PaymentCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> PaymentRead:
    """تسجيل دفعة جديدة."""

    payment = await payment_crud.create(session, payment_in)
    payment.created_by = current_user.id
    await session.commit()
    await session.refresh(payment)
    return PaymentRead.model_validate(payment)


@router.patch("/{payment_id}", response_model=PaymentRead, summary="تحديث دفعة")
async def update_payment(
    payment_id: int,
    payment_in: PaymentUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> PaymentRead:
    """تحديث دفعة."""

    payment = await payment_crud.get(session, payment_id)
    if not payment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    updated = await payment_crud.update(session, db_obj=payment, obj_in=payment_in)
    return PaymentRead.model_validate(updated)
