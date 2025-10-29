"""واجهات الموردين."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.permissions import get_current_user
from ...crud import supplier_crud
from ...dependencies import get_db_session
from ...models import User
from ...schemas import PaginatedResponse, Pagination, SupplierCreate, SupplierRead, SupplierUpdate
from ...utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

router = APIRouter(prefix="/suppliers", tags=["الموردون"])


@router.get("/", response_model=PaginatedResponse[SupplierRead], summary="قائمة الموردين")
async def list_suppliers(
    page: int = 1,
    size: int = 25,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[SupplierRead]:
    """عرض الموردين."""

    skip = (page - 1) * size
    suppliers = await supplier_crud.get_multi(session, skip=skip, limit=size)
    total = len(await supplier_crud.get_multi(session, skip=0, limit=1000))
    return PaginatedResponse(
        data=[SupplierRead.model_validate(supplier) for supplier in suppliers],
        pagination=Pagination(page=page, size=size, total=total),
    )


@router.post("/", response_model=SupplierRead, status_code=201, summary="إضافة مورد")
async def create_supplier(
    supplier_in: SupplierCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> SupplierRead:
    """إنشاء مورد جديد."""

    supplier = await supplier_crud.create(session, supplier_in)
    return SupplierRead.model_validate(supplier)


@router.patch("/{supplier_id}", response_model=SupplierRead, summary="تحديث مورد")
async def update_supplier(
    supplier_id: int,
    supplier_in: SupplierUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> SupplierRead:
    """تحديث بيانات المورد."""

    supplier = await supplier_crud.get(session, supplier_id)
    if not supplier:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    updated = await supplier_crud.update(session, db_obj=supplier, obj_in=supplier_in)
    return SupplierRead.model_validate(updated)


@router.delete("/{supplier_id}", summary="حذف مورد")
async def delete_supplier(supplier_id: int, session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    """حذف المورد."""

    supplier = await supplier_crud.get(session, supplier_id)
    if not supplier:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ERROR_MESSAGES["not_found"])
    await supplier_crud.remove(session, obj_id=supplier_id)
    return {"message": "تم حذف المورد بنجاح"}
