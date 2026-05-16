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


class Payment(Base):

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
        unique=True,
        index=True
    )

    amount: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False
    )

    # EXAMPLES:
    # UPI / COD / CARD
    payment_method: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False,
        index=True
    )

    # EXAMPLE:
    # txn_928374923
    transaction_reference: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        unique=True
    )

    paid_at: Mapped[datetime] = mapped_column(
        DateTime,
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

    order: Mapped["Order"] = relationship(
        "Order"
    )