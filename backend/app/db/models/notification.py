from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship, mapped_column, Mapped

from datetime import datetime

from app.db import Base

if TYPE_CHECKING:
    from user import User

class Notification(Base):

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # EXAMPLES:
    # ORDER_UPDATE / PAYMENT / DELIVERY / SYSTEM
    notification_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="UNREAD",
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # RELATIONSHIPS
    
    user: Mapped["User"] = relationship(
        back_populates="notifications"
    )
