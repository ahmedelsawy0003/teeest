"""تجميع مخططات البيانات."""
from .user import UserCreate, UserRead, UserUpdate, TokenPayload, TokenResponse
from .project import ProjectCreate, ProjectRead, ProjectUpdate
from .boq import BoqCreate, BoqRead, BoqUpdate
from .supplier import SupplierCreate, SupplierRead, SupplierUpdate
from .supply_order import (
    SupplyOrderCreate,
    SupplyOrderRead,
    SupplyOrderUpdate,
    SupplyOrderItemCreate,
    SupplyOrderItemRead,
)
from .payment import PaymentCreate, PaymentRead, PaymentUpdate
from .return import ReturnCreate, ReturnRead, ReturnUpdate, ReturnItemCreate, ReturnItemRead
from .notification import NotificationCreate, NotificationRead
from .audit import AuditLogCreate, AuditLogRead
from .attachment import AttachmentCreate, AttachmentRead
from .common import ResponseMessage, PaginatedResponse, Pagination

__all__ = [
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "TokenPayload",
    "TokenResponse",
    "ProjectCreate",
    "ProjectRead",
    "ProjectUpdate",
    "BoqCreate",
    "BoqRead",
    "BoqUpdate",
    "SupplierCreate",
    "SupplierRead",
    "SupplierUpdate",
    "SupplyOrderCreate",
    "SupplyOrderRead",
    "SupplyOrderUpdate",
    "SupplyOrderItemCreate",
    "SupplyOrderItemRead",
    "PaymentCreate",
    "PaymentRead",
    "PaymentUpdate",
    "ReturnCreate",
    "ReturnRead",
    "ReturnUpdate",
    "ReturnItemCreate",
    "ReturnItemRead",
    "NotificationCreate",
    "NotificationRead",
    "AuditLogCreate",
    "AuditLogRead",
    "AttachmentCreate",
    "AttachmentRead",
    "ResponseMessage",
    "PaginatedResponse",
    "Pagination",
]
