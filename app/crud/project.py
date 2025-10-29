"""عمليات إدارة المشاريع."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Project
from ..schemas.project import ProjectCreate, ProjectUpdate
from ..utils.helpers import generate_code
from .base import CRUDBase


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    """عمليات المشروع."""

    async def create(self, session: AsyncSession, obj_in: ProjectCreate) -> Project:
        code = obj_in.project_code
        if not code:
            result = await session.execute(select(Project.project_code))
            count = len(result.scalars().all()) + 1
            code = generate_code("PRJ", count)
        data = obj_in.model_dump()
        data["project_code"] = code
        project = Project(**data)
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project


project_crud = CRUDProject(Project)
