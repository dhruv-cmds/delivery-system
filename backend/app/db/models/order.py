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
    from delivery_partner import DeliveryPartner
    from order_tracking import OrderTracking
    from restaurant import Restaurant
    from user import User


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id"),
        nullable=False,
        index=True
    )

    delivery_partner_id: Mapped[int] = mapped_column(
        ForeignKey("delivery_partners.id"),
        nullable=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False,
        index=True
    )

    total_price: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False
    )

    delivery_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    payment_status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
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

    restaurant: Mapped["Restaurant"] = relationship(
        back_populates="orders"
    )

    delivery_partner: Mapped["DeliveryPartner"] = relationship(
        back_populates="orders"
    )

    tracking_updates: Mapped[list["OrderTracking"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )

    customer: Mapped["User"] = relationship(
        foreign_keys=[customer_id],
        back_populates="orders"
    )
