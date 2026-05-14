from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(50),
        default="CUSTOMER",
        nullable=False,
        index=True
    )

    phone = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )

    status = Column(
        String(50),
        default="ACTIVE",
        nullable=False,
        index=True
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

    restaurants = relationship(
        "Restaurant",
        back_populates="owner"
    )

    orders = relationship(
        "Order",
        back_populates="customer"
    )

    delivery_partner = relationship(
        "DeliveryPartner",
        back_populates="user",
        uselist=False
    )

    
    notifications = relationship(
        "Notification",
        back_populates="user"
    )