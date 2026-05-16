from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    DateTime,
    DECIMAL,
    ForeignKey
)

from decimal import Decimal

from sqlalchemy.orm import relationship, mapped_column, Mapped

from datetime import datetime

from app.db import Base

if TYPE_CHECKING:
    from order import Order
    from user import User


class DeliveryPartner(Base):

    __tablename__ = "delivery_partners"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True
    )

    vehicle_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False,
        index=True
    )

    latitude: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 7),
        nullable=True
    )

    longitude: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 7),
        nullable=True
    )

    rating: Mapped[Decimal] = mapped_column(
        DECIMAL(2, 1),
        nullable=True
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
        back_populates="delivery_partner"
    )

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="delivery_partner"
    )