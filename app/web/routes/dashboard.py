"""صفحة لوحة المعلومات."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.routes.dashboard import dashboard_summary, latest_activity
from ...dependencies import get_db_session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def dashboard_view(request: Request, session: AsyncSession = Depends(get_db_session)) -> HTMLResponse:
    """عرض البيانات الإحصائية."""

    summary = await dashboard_summary(session)
    latest = await latest_activity(session)
    context = {
        "request": request,
        "summary": summary,
        "latest_orders": latest["طلبات التوريد"],
        "latest_payments": latest["الدفعات"],
        "items": [("الرئيسية", None)],
    }
    return templates.TemplateResponse("dashboard/index.html", context)
