"""ثوابت النصوص العربية المستخدمة في التطبيق."""
from __future__ import annotations

STATUS_LABELS = {
    "draft": "مسودة",
    "active": "قيد التنفيذ",
    "on_hold": "متوقف",
    "completed": "مكتمل",
    "cancelled": "ملغي",
    "pending": "معلق",
    "approved": "معتمد",
    "rejected": "مرفوض",
}

SUCCESS_MESSAGES = {
    "project_created": "تم إنشاء المشروع بنجاح",
    "project_updated": "تم تحديث المشروع بنجاح",
    "project_deleted": "تم حذف المشروع بنجاح",
    "supplier_created": "تم إضافة المورد بنجاح",
    "payment_created": "تم تسجيل الدفعة بنجاح",
}

ERROR_MESSAGES = {
    "invalid_credentials": "اسم المستخدم أو كلمة المرور غير صحيحة",
    "unauthorized": "غير مصرح لك بالوصول",
    "not_found": "العنصر المطلوب غير موجود",
    "validation_error": "البيانات المدخلة غير صحيحة",
    "forbidden": "ليست لديك الصلاحية لإتمام العملية",
    "file_too_large": "حجم الملف يتجاوز الحد المسموح",
}

ARABIC_MONTHS = {
    1: "يناير",
    2: "فبراير",
    3: "مارس",
    4: "أبريل",
    5: "مايو",
    6: "يونيو",
    7: "يوليو",
    8: "أغسطس",
    9: "سبتمبر",
    10: "أكتوبر",
    11: "نوفمبر",
    12: "ديسمبر",
}
