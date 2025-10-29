"""صفحات الموردين."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from ...crud import supplier_crud
from ...dependencies import get_db_session

router = APIRouter(prefix="/suppliers")
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def suppliers_list(request: Request, session: AsyncSession = Depends(get_db_session)) -> HTMLResponse:
    suppliers = await supplier_crud.get_multi(session, skip=0, limit=100)
    context = {
        "request": request,
        "suppliers": suppliers,
        "pagination": {"page": 1, "size": 100, "total": len(suppliers)},
        "items": [("الرئيسية", "/"), ("الموردون", None)],
    }
    return templates.TemplateResponse("suppliers/list.html", context)


@router.get("/new", response_class=HTMLResponse)
async def supplier_form(request: Request) -> HTMLResponse:
    context = {
        "request": request,
        "title": "مورد جديد",
        "action": "/api/suppliers",
        "supplier": None,
        "items": [("الرئيسية", "/"), ("الموردون", "/suppliers"), ("مورد جديد", None)],
    }
    return templates.TemplateResponse("suppliers/form.html", context)
