"""نموذج المشاريع مع العلاقات المالية."""
from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..utils.enums import ProjectStatus


class Project(Base):
    """تمثيل المشروع وكافة علاقاته المرتبطة."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    project_name: Mapped[str] = mapped_column(String(255))
    client_name: Mapped[str] = mapped_column(String(255))
    client_contact: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    start_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    expected_end_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    actual_end_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus, name="project_status"), default=ProjectStatus.DRAFT)
    total_budget: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    total_spent: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    vat_rate: Mapped[float] = mapped_column(Float, default=15.0)
    include_vat: Mapped[bool] = mapped_column(Boolean, default=True)
    completion_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    manager = relationship("User", back_populates="managed_projects", foreign_keys=[manager_id])
    creator = relationship("User", back_populates="created_projects", foreign_keys=[created_by])
    boq_items = relationship("BoqItem", back_populates="project", cascade="all, delete-orphan")
    supply_orders = relationship("SupplyOrder", back_populates="project", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="project", cascade="all, delete-orphan")
    returns = relationship("Return", back_populates="project", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="project", cascade="all, delete-orphan")

    @property
    def remaining_budget(self) -> float:
        """حساب المتبقي من الميزانية."""

        return float(self.total_budget or 0) - float(self.total_spent or 0)

    @property
    def budget_utilization_percentage(self) -> float:
        """حساب نسبة استخدام الميزانية."""

        if not self.total_budget:
            return 0.0
        return round((float(self.total_spent) / float(self.total_budget)) * 100, 2)

    def __repr__(self) -> str:
        """تمثيل نصي للمشروع."""

        return f"Project(id={self.id!r}, code={self.project_code!r})"
