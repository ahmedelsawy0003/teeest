"""لوحة القيادة للمشاريع."""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...dependencies import get_db_session
from ...models import Payment, Project, SupplyOrder

router = APIRouter(prefix="/dashboard", tags=["لوحة القيادة"])


@router.get("/summary", summary="ملخص إحصائي")
async def dashboard_summary(session: AsyncSession = Depends(get_db_session)) -> dict[str, float | int]:
    """إرجاع ملخص سريع للأرقام."""

    projects_count = await session.scalar(select(func.count(Project.id))) or 0
    total_budget = await session.scalar(select(func.coalesce(func.sum(Project.total_budget), 0))) or 0
    total_spent = await session.scalar(select(func.coalesce(func.sum(Project.total_spent), 0))) or 0
    due_payments = await session.scalar(select(func.coalesce(func.sum(Payment.total_amount), 0))) or 0
    return {
        "عدد المشاريع النشطة": projects_count,
        "إجمالي الميزانيات": float(total_budget),
        "إجمالي المصروفات": float(total_spent),
        "المستحقات": float(due_payments),
    }


@router.get("/latest", summary="أحدث الأنشطة")
async def latest_activity(session: AsyncSession = Depends(get_db_session)) -> dict[str, list[dict[str, str]]]:
    """عرض آخر الطلبات والمدفوعات."""

    result_orders = await session.execute(
        select(SupplyOrder.order_code, SupplyOrder.total_with_vat, SupplyOrder.created_at)
        .order_by(SupplyOrder.created_at.desc())
        .limit(5)
    )
    orders = [
        {
            "الرمز": row.order_code,
            "الإجمالي": f"{row.total_with_vat}",
            "التاريخ": row.created_at.isoformat() if row.created_at else "",
        }
        for row in result_orders
    ]
    result_payments = await session.execute(
        select(Payment.payment_code, Payment.total_amount, Payment.payment_date)
        .order_by(Payment.payment_date.desc())
        .limit(5)
    )
    payments = [
        {
            "الرمز": row.payment_code,
            "الإجمالي": f"{row.total_amount}",
            "التاريخ": row.payment_date.isoformat() if row.payment_date else "",
        }
        for row in result_payments
    ]
    return {"طلبات التوريد": orders, "الدفعات": payments}
