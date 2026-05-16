from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    DateTime,
    DECIMAL,
    ForeignKey
)

from sqlalchemy.orm import relationship, mapped_column, Mapped

from datetime import datetime

from decimal import Decimal

from app.db import Base

if TYPE_CHECKING:
    from restaurant import Restaurant



class Menu(Base):

    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id"),
        nullable=False,
        index=True
    )

    item_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    price: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="AVAILABLE",
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
        back_populates="menu_items"
    )
