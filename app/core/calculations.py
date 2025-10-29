"""دوال الحسابات المالية للمشاريع."""
from __future__ import annotations

from decimal import Decimal

from ..models import BoqItem, Payment, Project


def calculate_project_budget(project: Project) -> float:
    """جمع إجمالي بنود الكميات لتحديث الميزانية."""

    total = sum(Decimal(item.total_price) for item in project.boq_items)
    if project.include_vat:
        total = total * (Decimal("1.0") + Decimal(project.vat_rate) / Decimal("100"))
    project.total_budget = float(total)
    return project.total_budget


def calculate_project_spent(project: Project) -> float:
    """جمع الدفعات المعتمدة للموردين."""

    total = sum(Decimal(payment.total_amount) for payment in project.payments if payment.status == "approved")
    project.total_spent = float(total)
    return project.total_spent
