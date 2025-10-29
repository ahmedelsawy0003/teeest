"""نماذج طلبات التوريد."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..utils.enums import OrderStatus


class SupplyOrder(Base):
    """يمثل طلب توريد مرتبط بمشروع ومورد."""

    __tablename__ = "supply_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    order_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    expected_delivery_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    actual_delivery_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, name="order_status"), default=OrderStatus.DRAFT)
    total_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    vat_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    total_with_vat: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="supply_orders")
    supplier = relationship("Supplier", back_populates="supply_orders")
    creator = relationship("User", back_populates="created_supply_orders", foreign_keys=[created_by])
    approver = relationship("User", back_populates="approved_supply_orders", foreign_keys=[approved_by])
    order_items = relationship("SupplyOrderItem", back_populates="supply_order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="supply_order")

    def __repr__(self) -> str:
        """تمثيل نصي."""

        return f"SupplyOrder(id={self.id!r}, code={self.order_code!r})"


class SupplyOrderItem(Base):
    """العناصر داخل طلب التوريد."""

    __tablename__ = "supply_order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    supply_order_id: Mapped[int] = mapped_column(ForeignKey("supply_orders.id", ondelete="CASCADE"))
    boq_item_id: Mapped[int] = mapped_column(ForeignKey("boq_items.id"))
    quantity_ordered: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    quantity_delivered: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    supply_order = relationship("SupplyOrder", back_populates="order_items")
    boq_item = relationship("BoqItem", back_populates="supply_order_items")

    @property
    def total_price(self) -> float:
        """حساب إجمالي سعر الصنف."""

        return round(float(self.quantity_ordered or 0) * float(self.unit_price or 0), 2)

    def __repr__(self) -> str:
        """تمثيل نصي للعنصر."""

        return f"SupplyOrderItem(id={self.id!r}, order_id={self.supply_order_id!r})"
