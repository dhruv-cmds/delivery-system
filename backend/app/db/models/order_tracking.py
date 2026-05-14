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


class OrderTracking(Base):

    __tablename__ = "order_trackings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    status = Column(
        String(20),
        default="PENDING",
        nullable=False
    )

    latitude = Column(
        DECIMAL(10, 7),
        nullable=True
    )

    longitude = Column(
        DECIMAL(10, 7),
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

    order = relationship(
        "Order",
        back_populates="tracking_updates"
    )
