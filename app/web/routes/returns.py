"""صفحات المرتجعات."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from ...crud import return_crud
from ...dependencies import get_db_session

router = APIRouter(prefix="/returns")
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def returns_list(request: Request, session: AsyncSession = Depends(get_db_session)) -> HTMLResponse:
    returns = await return_crud.get_multi(session, skip=0, limit=100)
    context = {
        "request": request,
        "returns": returns,
        "pagination": {"page": 1, "size": 100, "total": len(returns)},
        "items": [("الرئيسية", "/"), ("المرتجعات", None)],
    }
    return templates.TemplateResponse("returns/list.html", context)
