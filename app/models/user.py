"""نموذج المستخدمين في النظام."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..utils.enums import UserRole


class User(Base):
    """يمثل مستخدم النظام مع دوره وصلاحياته."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), default=UserRole.PROJECT_MANAGER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    avatar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    managed_projects = relationship(
        "Project",
        back_populates="manager",
        foreign_keys="Project.manager_id",
        cascade="all, delete-orphan",
    )
    created_projects = relationship(
        "Project",
        back_populates="creator",
        foreign_keys="Project.created_by",
    )
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    created_supply_orders = relationship(
        "SupplyOrder",
        back_populates="creator",
        foreign_keys="SupplyOrder.created_by",
    )
    approved_supply_orders = relationship(
        "SupplyOrder",
        back_populates="approver",
        foreign_keys="SupplyOrder.approved_by",
    )
    created_payments = relationship(
        "Payment",
        back_populates="creator",
        foreign_keys="Payment.created_by",
    )
    approved_payments = relationship(
        "Payment",
        back_populates="approver",
        foreign_keys="Payment.approved_by",
    )

    def __repr__(self) -> str:
        """تمثيل نصي واضح للمستخدم."""

        return f"User(id={self.id!r}, username={self.username!r})"
