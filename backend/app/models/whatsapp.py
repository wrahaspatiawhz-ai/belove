from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.base import CreatedAtMixin, IdMixin, TimestampMixin, enum_type
from app.models.enums import ConversationMode, MessageDirection


class WaConversation(IdMixin, TimestampMixin, Base):
    __tablename__ = "wa_conversations"

    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id", ondelete="SET NULL"), index=True
    )
    wa_phone: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    mode: Mapped[ConversationMode] = mapped_column(
        enum_type(ConversationMode, "conversation_mode"),
        default=ConversationMode.bot,
        server_default=ConversationMode.bot.value,
        nullable=False,
    )
    bot_state: Mapped[str | None] = mapped_column(String(100))
    last_inbound_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class WaMessage(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "wa_messages"

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("wa_conversations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    order_id: Mapped[int | None] = mapped_column(
        ForeignKey("orders.id", ondelete="SET NULL"), index=True
    )
    wa_msg_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    direction: Mapped[MessageDirection] = mapped_column(
        enum_type(MessageDirection, "message_direction"), nullable=False
    )
    type: Mapped[str | None] = mapped_column(String(50))
    body: Mapped[str | None] = mapped_column(Text)
    media_path: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str | None] = mapped_column(String(50))
