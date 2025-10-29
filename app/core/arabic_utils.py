"""أدوات مساعدة لمعالجة النصوص العربية."""
from __future__ import annotations

import locale
from datetime import datetime

ARABIC_LOCALE = "ar_SA.UTF-8"

try:
    locale.setlocale(locale.LC_TIME, ARABIC_LOCALE)
except locale.Error:
    pass


def format_datetime_arabic(date_value: datetime | None) -> str:
    """عرض التاريخ بصيغة عربية."""

    if not date_value:
        return "غير محدد"
    return date_value.strftime("%d %B %Y")
