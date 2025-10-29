"""نماذج الدفعات المالية."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..utils.enums import PaymentMethod, PaymentStatus


class Payment(Base):
    """يمثل عملية دفع مرتبطة بمشروع أو طلب توريد."""

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    payment_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    supplier_id: Mapped[int | None] = mapped_column(ForeignKey("suppliers.id"), nullable=True)
    supply_order_id: Mapped[int | None] = mapped_column(ForeignKey("supply_orders.id"), nullable=True)
    payment_type: Mapped[str] = mapped_column(String(50))
    payment_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    amount: Mapped[float] = mapped_column(Numeric(14, 2))
    vat_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    total_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod, name="payment_method"), default=PaymentMethod.BANK_TRANSFER
    )
    check_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bank_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    transaction_reference: Mapped[str | None] = mapped_column(String(150), nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus, name="payment_status"), default=PaymentStatus.PENDING)
    attachment_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="payments")
    supplier = relationship("Supplier", back_populates="payments")
    supply_order = relationship("SupplyOrder", back_populates="payments")
    creator = relationship("User", back_populates="created_payments", foreign_keys=[created_by])
    approver = relationship("User", back_populates="approved_payments", foreign_keys=[approved_by])

    def __repr__(self) -> str:
        """تمثيل نصي للدفعة."""

        return f"Payment(id={self.id!r}, code={self.payment_code!r})"
