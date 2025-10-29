"""التعدادات المستخدمة في النظام."""
from __future__ import annotations

from enum import Enum


class UserRole(str, Enum):
    """أدوار المستخدمين داخل النظام."""

    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    ACCOUNTANT = "accountant"


class ProjectStatus(str, Enum):
    """حالات المشاريع."""

    DRAFT = "draft"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderStatus(str, Enum):
    """حالات طلبات التوريد."""

    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    IN_DELIVERY = "in_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    """حالات الدفعات المالية."""

    PENDING = "pending"
    APPROVED = "approved"
    PAID = "paid"
    CANCELLED = "cancelled"


class ReturnStatus(str, Enum):
    """حالات المرتجعات."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REFUNDED = "refunded"


class NotificationType(str, Enum):
    """أنواع التنبيهات."""

    SUPPLY_ORDER = "supply_order"
    PAYMENT = "payment"
    APPROVAL = "approval"
    ALERT = "alert"
    SYSTEM = "system"


class AttachmentType(str, Enum):
    """أنواع المرفقات."""

    CONTRACT = "contract"
    INVOICE = "invoice"
    IMAGE = "image"
    DOCUMENT = "document"
    OTHER = "other"


class PaymentMethod(str, Enum):
    """طرق الدفع المتاحة."""

    CASH = "cash"
    CHECK = "check"
    BANK_TRANSFER = "bank_transfer"
    CREDIT = "credit"


class BoqCategory(str, Enum):
    """تصنيفات بنود الكميات."""

    CIVIL = "civil"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    FINISHING = "finishing"
    EQUIPMENT = "equipment"
    OTHER = "other"


class BoqUnit(str, Enum):
    """وحدات القياس المستخدمة في بنود الكميات."""

    METER = "meter"
    SQM = "sqm"
    CBM = "cbm"
    TON = "ton"
    KG = "kg"
    PIECE = "piece"
    DAY = "day"
    MONTH = "month"
