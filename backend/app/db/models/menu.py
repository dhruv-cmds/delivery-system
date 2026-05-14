from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db import Base


class Menu(Base):

    __tablename__ = "menu_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False,

        # GOOD:
        # restaurant menu queried frequently
        index=True
    )

    item_name = Column(
        String(255),
        nullable=False
    )

    description = Column(
        String(255),
        nullable=True
    )

    price = Column(
        DECIMAL(10, 2),
        nullable=False
    )

    status = Column(
        String(20),
        default="AVAILABLE",
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

    restaurant = relationship(
        "Restaurant",
        back_populates="menu_items"
    )
