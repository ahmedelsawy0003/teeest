"""دوال مساعدة عامة."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Sequence

from .constants import ARABIC_MONTHS


def format_arabic_date(date_value: datetime | None) -> str:
    """تنسيق التاريخ بصيغة عربية."""

    if not date_value:
        return "غير محدد"
    month_name = ARABIC_MONTHS.get(date_value.month, str(date_value.month))
    return f"{date_value.day} {month_name} {date_value.year}"


def calculate_percentage(part: float, whole: float) -> float:
    """حساب النسبة المئوية بأمان."""

    if whole == 0:
        return 0.0
    return round((part / whole) * 100, 2)


def generate_code(prefix: str, current_index: int) -> str:
    """إنشاء رمز متسلسل موحد."""

    return f"{prefix}-{current_index:03d}"


def arabic_join(items: Sequence[str]) -> str:
    """دمج قائمة نصوص عربية بفواصل واضحة."""

    return "، ".join(items)
