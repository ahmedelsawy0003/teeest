"""نماذج بنود الكميات."""
from __future__ import annotations

from sqlalchemy import Enum, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..utils.enums import BoqCategory, BoqUnit


class BoqItem(Base):
    """عنصر في جدول الكميات لمشروع معين."""

    __tablename__ = "boq_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    item_code: Mapped[str] = mapped_column(String(50), index=True)
    item_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[BoqCategory] = mapped_column(Enum(BoqCategory, name="boq_category"), default=BoqCategory.OTHER)
    quantity: Mapped[float] = mapped_column(Float, default=0.0)
    unit: Mapped[BoqUnit] = mapped_column(Enum(BoqUnit, name="boq_unit"), default=BoqUnit.PIECE)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    actual_quantity: Mapped[float] = mapped_column(Float, default=0.0)
    supplier_id: Mapped[int | None] = mapped_column(ForeignKey("suppliers.id"), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    project = relationship("Project", back_populates="boq_items")
    supplier = relationship("Supplier", back_populates="boq_items")
    supply_order_items = relationship("SupplyOrderItem", back_populates="boq_item", cascade="all, delete-orphan")
    return_items = relationship("ReturnItem", back_populates="boq_item", cascade="all, delete-orphan")

    @property
    def total_price(self) -> float:
        """حساب إجمالي تكلفة البند."""

        return round(float(self.quantity or 0) * float(self.unit_price or 0), 2)

    @property
    def remaining_quantity(self) -> float:
        """إرجاع الكمية المتبقية مقارنة بالمنفذ."""

        return float(self.quantity or 0) - float(self.actual_quantity or 0)

    def __repr__(self) -> str:
        """تمثيل نصي للبند."""

        return f"BoqItem(id={self.id!r}, code={self.item_code!r})"
