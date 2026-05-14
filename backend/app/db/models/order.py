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


class Order(Base):

    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False
    )

    delivery_partner_id = Column(
        Integer,
        ForeignKey("delivery_partners.id"),
        nullable=True
    )

    status = Column(
        String(20),
        default="PENDING",
        nullable=False
    )

    total_price = Column(
        DECIMAL(10, 2),
        nullable=False
    )

    delivery_address = Column(
        String(255),
        nullable=False
    )

    payment_status = Column(
        String(20),
        default="PENDING",
        nullable=False
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
    
    restaurant = relationship(
        "Restaurant",
        back_populates="orders"
    )

    delivery_partner = relationship(
        "DeliveryPartner",
        back_populates="orders"
    )

    tracking_updates = relationship(
        "OrderTracking",
        back_populates="order",
        cascade="all, delete-orphan"
    )
    
    customer = relationship(
        "User",
        foreign_keys=[customer_id],
        back_populates="orders"
    )