from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    DateTime
)

from sqlalchemy.orm import relationship, mapped_column, Mapped

from datetime import datetime

from app.db import Base

if TYPE_CHECKING:
    from delivery_partner import DeliveryPartner
    from notification import Notification
    from order import Order
    from restaurant import Restaurant

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="CUSTOMER",
        nullable=False,
        index=True
    )

    phone: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="ACTIVE",
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

    restaurants: Mapped[list["Restaurant"]] = relationship(
        back_populates="owner"
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="customer"
    )

    delivery_partner: Mapped["DeliveryPartner"] = relationship(
        back_populates="user",
        uselist=False
    )

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="user"
    )