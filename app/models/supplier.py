"""نموذج الموردين."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Supplier(Base):
    """المورد الذي يتعامل مع المشاريع."""

    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    supplier_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    company_name: Mapped[str] = mapped_column(String(255))
    tax_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    contact_person: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    specialty: Mapped[str | None] = mapped_column(String(100), nullable=True)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    total_transactions: Mapped[int] = mapped_column(Integer, default=0)
    total_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    boq_items = relationship("BoqItem", back_populates="supplier")
    supply_orders = relationship("SupplyOrder", back_populates="supplier")
    payments = relationship("Payment", back_populates="supplier")
    returns = relationship("Return", back_populates="supplier")

    def __repr__(self) -> str:
        """تمثيل نصي للمورد."""

        return f"Supplier(id={self.id!r}, code={self.supplier_code!r})"
