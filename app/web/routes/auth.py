"""صفحات التوثيق."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ...config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request) -> HTMLResponse:
    """عرض صفحة تسجيل الدخول."""

    return templates.TemplateResponse("auth/login.html", {"request": request, "items": [("الرئيسية", "/"), ("تسجيل الدخول", None)]})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request) -> HTMLResponse:
    """عرض صفحة التسجيل."""

    return templates.TemplateResponse(
        "auth/register.html", {"request": request, "items": [("الرئيسية", "/"), ("مستخدم جديد", None)]}
    )
