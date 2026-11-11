from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.base import IdMixin, TimestampMixin, enum_type
from app.models.enums import ProductionStepName, ProductionStepStatus


class ProductionStep(IdMixin, TimestampMixin, Base):
    __tablename__ = "production_steps"
    __table_args__ = (
        UniqueConstraint("order_id", "step", name="uq_production_steps_order_id_step"),
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    step: Mapped[ProductionStepName] = mapped_column(
        enum_type(ProductionStepName, "production_step_name"), nullable=False
    )
    status: Mapped[ProductionStepStatus] = mapped_column(
        enum_type(ProductionStepStatus, "production_step_status"),
        default=ProductionStepStatus.pending,
        server_default=ProductionStepStatus.pending.value,
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    note: Mapped[str | None] = mapped_column(Text)


class Shipment(IdMixin, TimestampMixin, Base):
    __tablename__ = "shipments"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    courier: Mapped[str | None] = mapped_column(String(100))
    tracking_number: Mapped[str | None] = mapped_column(String(100))
    shipped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    note: Mapped[str | None] = mapped_column(Text)
