"""طبقة العمليات الأساسية على قاعدة البيانات."""
from __future__ import annotations

from typing import Any, Generic, Iterable, Sequence, TypeVar

from sqlalchemy import Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """كلاس أساسي يوفّر العمليات المشتركة."""

    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def get(self, session: AsyncSession, obj_id: Any) -> ModelType | None:
        """جلب عنصر بالمعرف."""

        result = await session.execute(select(self.model).where(self.model.id == obj_id))
        return result.scalar_one_or_none()

    async def get_multi(self, session: AsyncSession, *, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """جلب مجموعة من العناصر مع الترقيم."""

        result = await session.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, session: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """إنشاء عنصر جديد."""

        data = obj_in.model_dump() if hasattr(obj_in, "model_dump") else obj_in
        db_obj = self.model(**data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self, session: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        """تحديث عنصر قائم."""

        data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, "model_dump") else obj_in
        for field, value in data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, *, obj_id: Any) -> None:
        """حذف عنصر."""

        await session.execute(delete(self.model).where(self.model.id == obj_id))
        await session.commit()
