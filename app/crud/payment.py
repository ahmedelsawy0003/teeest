"""عمليات الدفعات."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Payment
from ..schemas.payment import PaymentCreate, PaymentUpdate
from ..utils.helpers import generate_code
from .base import CRUDBase


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    """عمليات الدفعات."""

    async def create(self, session: AsyncSession, obj_in: PaymentCreate) -> Payment:
        data = obj_in.model_dump()
        result = await session.execute(select(Payment.payment_code))
        count = len(result.scalars().all()) + 1
        data["payment_code"] = generate_code("PAY", count)
        payment = Payment(**data)
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        return payment


payment_crud = CRUDPayment(Payment)
