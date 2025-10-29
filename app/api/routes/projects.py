"""واجهات برمجة المشاريع."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.excel_handler import parse_boq_excel
from ...core.permissions import get_current_user
from ...crud import boq_crud, project_crud
from ...dependencies import get_db_session
from ...models import Project, User
from ...schemas import BoqCreate, BoqRead, PaginatedResponse, Pagination, ProjectCreate, ProjectRead, ProjectUpdate
from ...utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES
from ...utils.enums import BoqCategory, BoqUnit

router = APIRouter(prefix="/projects", tags=["المشاريع"])


@router.get("/", response_model=PaginatedResponse[ProjectRead], summary="قائمة المشاريع")
async def list_projects(
    page: int = 1,
    size: int = 25,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[ProjectRead]:
    """عرض قائمة المشاريع."""

    skip = (page - 1) * size
    projects = await project_crud.get_multi(session, skip=skip, limit=size)
    total = len(await project_crud.get_multi(session, skip=0, limit=1000))
    data = [ProjectRead.model_validate(project) for project in projects]
    return PaginatedResponse(data=data, pagination=Pagination(page=page, size=size, total=total))


@router.post("/", response_model=ProjectRead, status_code=201, summary="إنشاء مشروع")
async def create_project(
    project_in: ProjectCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> ProjectRead:
    """إنشاء مشروع جديد."""

    project = await project_crud.create(session, project_in)
    project.created_by = current_user.id
    await session.commit()
    await session.refresh(project)
    return ProjectRead.model_validate(project)


@router.get("/{project_id}", response_model=ProjectRead, summary="عرض مشروع")
async def get_project(project_id: int, session: AsyncSession = Depends(get_db_session)) -> ProjectRead:
    """الحصول على مشروع."""

    project = await project_crud.get(session, project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    return ProjectRead.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectRead, summary="تحديث مشروع")
async def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> ProjectRead:
    """تحديث بيانات مشروع."""

    project = await project_crud.get(session, project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    updated = await project_crud.update(session, db_obj=project, obj_in=project_in)
    return ProjectRead.model_validate(updated)


@router.post("/{project_id}/boq", response_model=BoqRead, summary="إضافة بند")
async def add_boq_item(
    project_id: int,
    boq_in: BoqCreate,
    session: AsyncSession = Depends(get_db_session),
) -> BoqRead:
    """إضافة بند جديد للمشروع."""

    project = await project_crud.get(session, project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    item = await boq_crud.create(session, boq_in)
    return BoqRead.model_validate(item)


@router.post("/{project_id}/boq/upload", summary="رفع ملف بنود")
async def upload_boq(
    project_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """رفع ملف إكسل وإضافة بنوده."""

    project = await project_crud.get(session, project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    contents = await file.read()
    items = parse_boq_excel(contents)
    for item in items:
        category_value = item["category"].lower()
        unit_value = item["unit"].lower()
        category = next((c for c in BoqCategory if c.value == category_value), BoqCategory.OTHER)
        unit = next((u for u in BoqUnit if u.value == unit_value), BoqUnit.PIECE)
        await boq_crud.create(
            session,
            BoqCreate(
                project_id=project_id,
                item_code=str(item["item_code"]),
                item_name=str(item["item_name"]),
                description=str(item.get("description") or ""),
                category=category,
                quantity=float(item["quantity"]),
                unit=unit,
                unit_price=float(item["unit_price"]),
            ),
        )
    return {"message": SUCCESS_MESSAGES["project_updated"]}
