"""عمليات المرتجعات."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Return, ReturnItem
from ..schemas.return import ReturnCreate, ReturnItemCreate, ReturnUpdate
from ..utils.helpers import generate_code
from .base import CRUDBase


class CRUDReturn(CRUDBase[Return, ReturnCreate, ReturnUpdate]):
    """عمليات المرتجع."""

    async def create(self, session: AsyncSession, obj_in: ReturnCreate) -> Return:
        data = obj_in.model_dump(exclude={"items"})
        result = await session.execute(select(Return.return_code))
        count = len(result.scalars().all()) + 1
        data["return_code"] = generate_code("RET", count)
        record = Return(**data)
        session.add(record)
        await session.flush()
        await self._sync_items(session, record, obj_in.items)
        await session.commit()
        await session.refresh(record)
        return record

    async def update(self, session: AsyncSession, *, db_obj: Return, obj_in: ReturnUpdate) -> Return:
        data = obj_in.model_dump(exclude_unset=True, exclude={"items"})
        for field, value in data.items():
            setattr(db_obj, field, value)
        if obj_in.items is not None:
            await self._sync_items(session, db_obj, obj_in.items)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def _sync_items(self, session: AsyncSession, record: Return, items: list[ReturnItemCreate]) -> None:
        await session.execute(ReturnItem.__table__.delete().where(ReturnItem.return_id == record.id))
        session.flush()
        for item in items:
            session.add(
                ReturnItem(
                    return_id=record.id,
                    boq_item_id=item.boq_item_id,
                    quantity_returned=item.quantity_returned,
                    unit_price=item.unit_price,
                    notes=item.notes,
                )
            )


return_crud = CRUDReturn(Return)
