"""صفحات إدارة المشاريع."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from ...crud import project_crud
from ...dependencies import get_db_session
from ...schemas import ProjectCreate, ProjectUpdate

router = APIRouter(prefix="/projects")
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def list_projects(request: Request, session: AsyncSession = Depends(get_db_session)) -> HTMLResponse:
    """عرض قائمة المشاريع."""

    projects = await project_crud.get_multi(session, skip=0, limit=100)
    context = {
        "request": request,
        "projects": projects,
        "pagination": {"page": 1, "size": 100, "total": len(projects)},
        "items": [("الرئيسية", "/"), ("المشاريع", None)],
    }
    return templates.TemplateResponse("projects/list.html", context)


@router.get("/new", response_class=HTMLResponse)
async def new_project_form(request: Request) -> HTMLResponse:
    """عرض نموذج مشروع جديد."""

    context = {
        "request": request,
        "title": "مشروع جديد",
        "action": "/api/projects",
        "project": None,
        "items": [("الرئيسية", "/"), ("المشاريع", "/projects"), ("مشروع جديد", None)],
    }
    return templates.TemplateResponse("projects/form.html", context)


@router.get("/{project_id}", response_class=HTMLResponse)
async def project_detail(project_id: int, request: Request, session: AsyncSession = Depends(get_db_session)) -> HTMLResponse:
    """عرض تفاصيل مشروع."""

    project = await project_crud.get(session, project_id)
    if not project:
        return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)
    context = {
        "request": request,
        "project": project,
        "items": [("الرئيسية", "/"), ("المشاريع", "/projects"), (project.project_name, None)],
    }
    return templates.TemplateResponse("projects/detail.html", context)


@router.get("/{project_id}/upload", response_class=HTMLResponse)
async def project_upload(project_id: int, request: Request) -> HTMLResponse:
    """عرض نموذج رفع ملف بنود."""

    context = {
        "request": request,
        "project_id": project_id,
        "items": [("الرئيسية", "/"), ("المشاريع", "/projects"), ("رفع بنود", None)],
    }
    return templates.TemplateResponse("projects/upload_boq.html", context)
