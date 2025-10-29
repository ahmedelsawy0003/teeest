"""نقطة إنشاء وتشغيل تطبيق FastAPI."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .config import settings


def create_app() -> FastAPI:
    """إنشاء تطبيق FastAPI مهيأ بجميع الوسطاء والمسارات."""

    application = FastAPI(
        title="ProManage",
        version="1.0.0",
        default_response_class=JSONResponse,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.allowed_origins] or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(SessionMiddleware, secret_key=settings.secret_key, same_site="lax")

    @application.middleware("http")
    async def add_user_to_request(request: Request, call_next):
        """إرفاق المستخدم بالطلب لأغراض الواجهة الرسومية."""

        request.state.user = None
        response = await call_next(request)
        return response

    static_path = Path("app/static")
    application.mount("/static", StaticFiles(directory=str(static_path)), name="static")

    from .api.routes import api_router
    from .web.routes import web_router

    application.include_router(api_router)
    application.include_router(web_router)

    @application.get("/health", tags=["الصحة"])
    async def health_check() -> dict[str, str]:
        """التحقق من حالة التطبيق."""

        return {"message": "النظام يعمل"}

    return application


app = create_app()
