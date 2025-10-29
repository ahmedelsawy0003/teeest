"""أدوات الأمان والتوثيق."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from ..config import settings
from ..utils.constants import ERROR_MESSAGES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """تجزئة كلمة المرور باستخدام bcrypt."""

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """التحقق من صحة كلمة المرور."""

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """إنشاء رمز JWT للوصول."""

    expire = datetime.now(tz=timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode: dict[str, Any] = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    """فك تشفير الرمز وإرجاع البيانات الداخلية."""

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload
    except JWTError as exc:
        raise ValueError(ERROR_MESSAGES["unauthorized"]) from exc
