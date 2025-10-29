"""تجميع مسارات الواجهة."""
from fastapi import APIRouter

from . import auth, dashboard, projects, suppliers, supply_orders, payments, returns, reports

web_router = APIRouter()
web_router.include_router(dashboard.router)
web_router.include_router(auth.router)
web_router.include_router(projects.router)
web_router.include_router(suppliers.router)
web_router.include_router(supply_orders.router)
web_router.include_router(payments.router)
web_router.include_router(returns.router)
web_router.include_router(reports.router)

__all__ = ["web_router"]
