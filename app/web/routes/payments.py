"""صفحات الدفعات."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from ...crud import payment_crud
from ...dependencies import get_db_session

router = APIRouter(prefix="/payments")
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def payments_list(request: Request, session: AsyncSession = Depends(get_db_session)) -> HTMLResponse:
    payments = await payment_crud.get_multi(session, skip=0, limit=100)
    context = {
        "request": request,
        "payments": payments,
        "pagination": {"page": 1, "size": 100, "total": len(payments)},
        "items": [("الرئيسية", "/"), ("الدفعات", None)],
    }
    return templates.TemplateResponse("payments/list.html", context)
