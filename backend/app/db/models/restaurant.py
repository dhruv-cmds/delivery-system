from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.db import Base


class Restaurant(Base):

    __tablename__ = "restaurants"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        nullable=False,
        index=True
    )

    address = Column(
        String(255),
        nullable=False
    )

    phone = Column(
        String(20),
        unique=True,
        nullable=False
    )

    status = Column(
        String(50),
        default="OPEN",
        nullable=False,
        index=True
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
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

    owner = relationship(
        "User",
        back_populates="restaurants"
    )

    orders = relationship(
        "Order",
        back_populates="restaurant"
    )

    menu_items = relationship(
        "Menu",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )