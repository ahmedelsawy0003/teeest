"""نماذج المرتجعات."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..utils.enums import ReturnStatus


class Return(Base):
    """تمثيل عملية مرتجع مواد."""

    __tablename__ = "returns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    return_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    supplier_id: Mapped[int | None] = mapped_column(ForeignKey("suppliers.id"), nullable=True)
    supply_order_id: Mapped[int | None] = mapped_column(ForeignKey("supply_orders.id"), nullable=True)
    return_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    status: Mapped[ReturnStatus] = mapped_column(Enum(ReturnStatus, name="return_status"), default=ReturnStatus.PENDING)
    total_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    reason: Mapped[str] = mapped_column(String(50))
    reason_details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="returns")
    supplier = relationship("Supplier", back_populates="returns")
    supply_order = relationship("SupplyOrder")
    items = relationship("ReturnItem", back_populates="return_record", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """تمثيل نصي."""

        return f"Return(id={self.id!r}, code={self.return_code!r})"


class ReturnItem(Base):
    """عنصر داخل المرتجع."""

    __tablename__ = "return_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    return_id: Mapped[int] = mapped_column(ForeignKey("returns.id", ondelete="CASCADE"))
    boq_item_id: Mapped[int] = mapped_column(ForeignKey("boq_items.id"))
    quantity_returned: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    return_record = relationship("Return", back_populates="items")
    boq_item = relationship("BoqItem", back_populates="return_items")

    @property
    def total_price(self) -> float:
        """حساب القيمة الإجمالية."""

        return round(float(self.quantity_returned or 0) * float(self.unit_price or 0), 2)

    def __repr__(self) -> str:
        """تمثيل نصي."""

        return f"ReturnItem(id={self.id!r}, return_id={self.return_id!r})"
