"""تجميع مسارات API."""
from fastapi import APIRouter

from . import auth, users, projects, suppliers, supply_orders, payments, returns, dashboard, reports, notifications

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/api")
api_router.include_router(users.router, prefix="/api")
api_router.include_router(projects.router, prefix="/api")
api_router.include_router(suppliers.router, prefix="/api")
api_router.include_router(supply_orders.router, prefix="/api")
api_router.include_router(payments.router, prefix="/api")
api_router.include_router(returns.router, prefix="/api")
api_router.include_router(dashboard.router, prefix="/api")
api_router.include_router(reports.router, prefix="/api")
api_router.include_router(notifications.router, prefix="/api")

__all__ = ["api_router"]
