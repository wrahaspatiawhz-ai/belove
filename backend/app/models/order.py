from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.base import CreatedAtMixin, IdMixin, TimestampMixin, enum_type
from app.models.enums import DtfStatus, OrderFileKind, OrderStatus


class Order(IdMixin, TimestampMixin, Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("total >= 0", name="total_non_negative"),
    )

    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    public_token: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), nullable=False, index=True
    )
    status: Mapped[OrderStatus] = mapped_column(
        enum_type(OrderStatus, "order_status"),
        default=OrderStatus.pending,
        server_default=OrderStatus.pending.value,
        nullable=False,
        index=True,
    )
    total: Mapped[int] = mapped_column(
        BigInteger, default=0, server_default=text("0"), nullable=False
    )
    special_request: Mapped[str | None] = mapped_column(Text)
    shipping_address: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)


class OrderItem(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "order_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="quantity_positive"),
        CheckConstraint("unit_price >= 0", name="unit_price_non_negative"),
        CheckConstraint("subtotal >= 0", name="subtotal_non_negative"),
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    variant_id: Mapped[int | None] = mapped_column(
        ForeignKey("product_variants.id", ondelete="SET NULL"), index=True
    )
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    variant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[str | None] = mapped_column(String(50))
    color: Mapped[str | None] = mapped_column(String(50))
    unit_price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[int] = mapped_column(BigInteger, nullable=False)


class OrderFile(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "order_files"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    kind: Mapped[OrderFileKind] = mapped_column(
        enum_type(OrderFileKind, "order_file_kind"),
        default=OrderFileKind.design,
        server_default=OrderFileKind.design.value,
        nullable=False,
    )
    dtf_status: Mapped[DtfStatus] = mapped_column(
        enum_type(DtfStatus, "dtf_status"),
        default=DtfStatus.pending,
        server_default=DtfStatus.pending.value,
        nullable=False,
    )


class OrderStatusHistory(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "order_status_history"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    from_status: Mapped[OrderStatus | None] = mapped_column(
        enum_type(OrderStatus, "order_status_history_from_status")
    )
    to_status: Mapped[OrderStatus] = mapped_column(
        enum_type(OrderStatus, "order_status_history_to_status"), nullable=False
    )
    changed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    note: Mapped[str | None] = mapped_column(Text)
