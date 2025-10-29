"""إعدادات تطبيق ProManage باستخدام Pydantic Settings."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """كائن الإعدادات العامة للتطبيق."""

    secret_key: str = Field(..., alias="SECRET_KEY", min_length=32)
    database_url: str = Field("sqlite+aiosqlite:///./promanage.db", alias="DATABASE_URL")
    access_token_expire_minutes: int = Field(1440, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    allowed_origins: List[AnyHttpUrl | str] = Field(default_factory=list, alias="ALLOWED_ORIGINS")
    allowed_hosts: List[str] = Field(default_factory=lambda: ["*"], alias="ALLOWED_HOSTS")
    max_upload_size: int = Field(5 * 1024 * 1024, alias="MAX_UPLOAD_SIZE")
    upload_folder: Path = Field(Path("app/static/uploads"), alias="UPLOAD_FOLDER")
    vat_rate: float = Field(15.0, alias="VAT_RATE")

    class Config:
        """تهيئة قراءة المتغيرات من ملف env."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @field_validator("allowed_origins", "allowed_hosts", mode="before")
    @classmethod
    def split_str(cls, value: List[str] | str) -> List[str]:
        """تحويل السلاسل النصية إلى قائمة."""

        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """إرجاع نسخة مخبأة من الإعدادات لتقليل القراءة من القرص."""

    settings = Settings()  # type: ignore[call-arg]
    settings.upload_folder.mkdir(parents=True, exist_ok=True)
    return settings


settings = get_settings()
