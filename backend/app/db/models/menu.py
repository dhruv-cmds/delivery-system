from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    ForeignKey
)

from sqlalchemy.orm import relationship

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
        nullable=False
    )

    item_name = Column(
        String(255),
        nullable=False,  
    )

    description = Column(
        String(255),
        nullable=True
    )

    price = Column(
        DECIMAL(10 , 2),
        nullable=False
    )

    status = Column(
        String(20),
        default="AVAILABLE",
        nullable=False
    )

    restaurant = relationship(
        "Restaurant",
        back_populates="menu_items"
    )