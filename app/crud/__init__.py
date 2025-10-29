"""تجميع وحدات CRUD."""
from .user import user_crud
from .project import project_crud
from .boq import boq_crud
from .supplier import supplier_crud
from .supply_order import supply_order_crud
from .payment import payment_crud
from .return import return_crud

__all__ = [
    "user_crud",
    "project_crud",
    "boq_crud",
    "supplier_crud",
    "supply_order_crud",
    "payment_crud",
    "return_crud",
]
