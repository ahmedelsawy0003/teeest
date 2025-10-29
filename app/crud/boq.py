"""عمليات بنود الكميات."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import BoqItem
from ..schemas.boq import BoqCreate, BoqUpdate
from ..utils.helpers import generate_code
from .base import CRUDBase


class CRUDBoq(CRUDBase[BoqItem, BoqCreate, BoqUpdate]):
    """عمليات خاصة ببنود الكميات."""

    async def create(self, session: AsyncSession, obj_in: BoqCreate) -> BoqItem:
        data = obj_in.model_dump()
        if not data.get("item_code"):
            result = await session.execute(select(BoqItem.item_code).where(BoqItem.project_id == obj_in.project_id))
            count = len(result.scalars().all()) + 1
            data["item_code"] = generate_code("BOQ", count)
        boq_item = BoqItem(**data)
        session.add(boq_item)
        await session.commit()
        await session.refresh(boq_item)
        return boq_item


boq_crud = CRUDBoq(BoqItem)
