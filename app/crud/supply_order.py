"""عمليات طلبات التوريد."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import SupplyOrder, SupplyOrderItem
from ..schemas.supply_order import SupplyOrderCreate, SupplyOrderItemCreate, SupplyOrderUpdate
from ..utils.helpers import generate_code
from .base import CRUDBase


class CRUDSupplyOrder(CRUDBase[SupplyOrder, SupplyOrderCreate, SupplyOrderUpdate]):
    """عمليات الطلب."""

    async def create(self, session: AsyncSession, obj_in: SupplyOrderCreate) -> SupplyOrder:
        data = obj_in.model_dump(exclude={"items"})
        result = await session.execute(select(SupplyOrder.order_code))
        count = len(result.scalars().all()) + 1
        data["order_code"] = generate_code("SO", count)
        order = SupplyOrder(**data)
        session.add(order)
        await session.flush()
        await self._sync_items(session, order, obj_in.items)
        await session.commit()
        await session.refresh(order)
        return order

    async def update(self, session: AsyncSession, *, db_obj: SupplyOrder, obj_in: SupplyOrderUpdate) -> SupplyOrder:
        data = obj_in.model_dump(exclude_unset=True, exclude={"items"})
        for field, value in data.items():
            setattr(db_obj, field, value)
        if obj_in.items is not None:
            await self._sync_items(session, db_obj, obj_in.items)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def _sync_items(
        self, session: AsyncSession, order: SupplyOrder, items: list[SupplyOrderItemCreate]
    ) -> None:
        await session.execute(
            select(SupplyOrderItem).where(SupplyOrderItem.supply_order_id == order.id)
        )
        await session.execute(
            SupplyOrderItem.__table__.delete().where(SupplyOrderItem.supply_order_id == order.id)
        )
        session.flush()
        for item in items:
            session.add(
                SupplyOrderItem(
                    supply_order_id=order.id,
                    boq_item_id=item.boq_item_id,
                    quantity_ordered=item.quantity_ordered,
                    quantity_delivered=item.quantity_delivered,
                    unit_price=item.unit_price,
                    notes=item.notes,
                )
            )


supply_order_crud = CRUDSupplyOrder(SupplyOrder)
