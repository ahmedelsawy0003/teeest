"""واجهات التقارير."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.pdf_generator import generate_table_pdf
from ...dependencies import get_db_session
from ...models import Payment, Project, Supplier

router = APIRouter(prefix="/reports", tags=["التقارير"])


@router.get("/financial", summary="تقرير مالي")
async def financial_report(session: AsyncSession = Depends(get_db_session)) -> dict[str, float]:
    """إرجاع ملخص مالي بسيط."""

    total_budget = await session.scalar(select(func.coalesce(func.sum(Project.total_budget), 0))) or 0
    total_spent = await session.scalar(select(func.coalesce(func.sum(Project.total_spent), 0))) or 0
    payments = await session.scalar(select(func.coalesce(func.sum(Payment.total_amount), 0))) or 0
    return {
        "إجمالي الميزانيات": float(total_budget),
        "إجمالي المصروفات": float(total_spent),
        "إجمالي الدفعات": float(payments),
    }


@router.get("/financial/pdf", summary="تصدير مالي PDF")
async def financial_report_pdf(session: AsyncSession = Depends(get_db_session)) -> bytes:
    """تصدير التقرير المالي PDF."""

    data = await financial_report(session)
    headers = ["البند", "القيمة"]
    rows = [(key, value) for key, value in data.items()]
    return generate_table_pdf("تقرير مالي", headers, rows)
