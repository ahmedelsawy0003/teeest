"""عمليات المستخدمين."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from ..schemas.user import UserCreate, UserUpdate
from ..utils.validators import validate_password
from ..core.security import hash_password
from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """عمليات خاصة بالمستخدم."""

    async def get_by_username(self, session: AsyncSession, username: str) -> User | None:
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, obj_in: UserCreate) -> User:
        validate_password(obj_in.password)
        hashed = hash_password(obj_in.password)
        user = User(
            username=obj_in.username,
            email=obj_in.email,
            full_name=obj_in.full_name,
            phone=obj_in.phone,
            role=obj_in.role,
            hashed_password=hashed,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def update(self, session: AsyncSession, *, db_obj: User, obj_in: UserUpdate) -> User:
        data = obj_in.model_dump(exclude_unset=True)
        if "password" in data and data["password"]:
            validate_password(data["password"])
            data["hashed_password"] = hash_password(data.pop("password"))
        return await super().update(session, db_obj=db_obj, obj_in=data)


user_crud = CRUDUser(User)
