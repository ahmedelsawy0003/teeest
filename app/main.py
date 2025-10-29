"""نقطة تشغيل تطبيق FastAPI."""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .api.routes import api_router
from .config import settings
from .web.routes import web_router

app = FastAPI(title="ProManage", version="1.0.0", default_response_class=JSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.allowed_origins] or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)


@app.middleware("http")
async def add_user_to_request(request: Request, call_next):
    """إرفاق المستخدم بالطلب لأغراض الواجهة."""

    request.state.user = None
    response = await call_next(request)
    return response


app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api_router)
app.include_router(web_router)


@app.get("/health", tags=["الصحة"])
async def health_check() -> dict[str, str]:
    """التحقق من حالة التطبيق."""

    return {"message": "النظام يعمل"}
