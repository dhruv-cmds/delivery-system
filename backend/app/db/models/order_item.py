from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    DECIMAL,
    ForeignKey
)
from sqlalchemy.orm import relationship, mapped_column, Mapped

from datetime import datetime
from decimal import Decimal

from app.db import Base

if TYPE_CHECKING:
    from order import Order
    from menu import Menu


class OrderItem(Base):

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
        index=True
    )

    menu_item_id: Mapped[int] = mapped_column(
        ForeignKey("menu_items.id"),
        nullable=False,
        index=True
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False,
        default=1
    )

    unit_price: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False
    )

    total_price: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False
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

    order: Mapped["Order"] = relationship(
        back_populates="order_items"
    )

    menu_item: Mapped["Menu"] = relationship(
        back_populates="order_items"
    )
