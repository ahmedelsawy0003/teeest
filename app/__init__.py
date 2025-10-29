"""تهيئة حزمة ProManage."""
from __future__ import annotations

from fastapi import FastAPI


def create_application() -> FastAPI:
    """إنشاء التطبيق الرئيسي دون التسبب في استيراد دائري."""

    from .main import create_app

    return create_app()


__all__ = ["create_application"]
