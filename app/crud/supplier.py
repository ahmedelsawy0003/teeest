"""عمليات الموردين."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Supplier
from ..schemas.supplier import SupplierCreate, SupplierUpdate
from ..utils.helpers import generate_code
from .base import CRUDBase


class CRUDSupplier(CRUDBase[Supplier, SupplierCreate, SupplierUpdate]):
    """عمليات المورد."""

    async def create(self, session: AsyncSession, obj_in: SupplierCreate) -> Supplier:
        data = obj_in.model_dump()
        result = await session.execute(select(Supplier.supplier_code))
        count = len(result.scalars().all()) + 1
        data["supplier_code"] = generate_code("SUP", count)
        supplier = Supplier(**data)
        session.add(supplier)
        await session.commit()
        await session.refresh(supplier)
        return supplier


supplier_crud = CRUDSupplier(Supplier)
