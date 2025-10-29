"""صفحات التقارير."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.routes.reports import financial_report
from ...dependencies import get_db_session

router = APIRouter(prefix="/reports")
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def reports_home(request: Request, session: AsyncSession = Depends(get_db_session)) -> HTMLResponse:
    report = await financial_report(session)
    context = {
        "request": request,
        "report": report,
        "items": [("الرئيسية", "/"), ("التقارير", None)],
    }
    return templates.TemplateResponse("reports/financial.html", context)
