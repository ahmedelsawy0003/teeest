"""دوال التحقق من صحة البيانات."""
from __future__ import annotations

import re
from typing import Annotated

from fastapi import HTTPException, status

from .constants import ERROR_MESSAGES

PASSWORD_PATTERN = re.compile(r"^(?=.*[A-Z])(?=.*\d).{8,}$")


def validate_password(password: str) -> None:
    """التحقق من قوة كلمة المرور ورفع استثناء عند المخالفة."""

    if not PASSWORD_PATTERN.match(password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="يجب أن تحتوي كلمة المرور على ٨ أحرف على الأقل مع حرف كبير ورقم",
        )


def ensure_file_size(file_size: int, max_size: int) -> None:
    """التحقق من حجم الملف قبل رفعه."""

    if file_size > max_size:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, ERROR_MESSAGES["file_too_large"])


def ensure_permission(condition: bool) -> None:
    """التحقق من الصلاحيات ورفع استثناء عند عدم توفرها."""

    if not condition:
        raise HTTPException(status.HTTP_403_FORBIDDEN, ERROR_MESSAGES["forbidden"])
