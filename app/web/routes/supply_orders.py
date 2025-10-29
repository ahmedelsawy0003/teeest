"""صفحات طلبات التوريد."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from ...crud import supply_order_crud
from ...dependencies import get_db_session

router = APIRouter(prefix="/supply-orders")
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def supply_orders_list(request: Request, session: AsyncSession = Depends(get_db_session)) -> HTMLResponse:
    orders = await supply_order_crud.get_multi(session, skip=0, limit=100)
    context = {
        "request": request,
        "orders": orders,
        "pagination": {"page": 1, "size": 100, "total": len(orders)},
        "items": [("الرئيسية", "/"), ("طلبات التوريد", None)],
    }
    return templates.TemplateResponse("supply_orders/list.html", context)
