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


class DeliveryPartner(Base):

    __tablename__ = "delivery_partners"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    vehicle_type = Column(
        String(100),
        nullable=False
    )

    status = Column(
        String(20),
        default="AVAILABLE",
        nullable=False
    )

    current_location = Column(
        String(255),
        nullable=True
    )

    rating = Column(
        DECIMAL(2, 1),
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


    user = relationship(
        "User"
    )

    orders = relationship(
        "Order",
        back_populates="delivery_partner"
    )