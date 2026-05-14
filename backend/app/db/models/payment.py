from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    DECIMAL
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
        unique=True
    )

    amount = Column(
        DECIMAL(10, 2),
        nullable=False
    )

    # UPI / COD / CARD
    payment_method = Column(
        String(20),
        nullable=False
    )

    status = Column(
        String(20),
        default="PENDING",
        nullable=False
    )

    # EXAMPLE:
    # txn_928374923
    transaction_reference = Column(
        String(100),
        nullable=True
    )

    paid_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # RELATIONSHIPS

    order = relationship(
        "Order"
    )