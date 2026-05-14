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
        nullable=False
    )

    name = Column(
        String(100), 
        nullable=False
    )

    email = Column(
        String(255), 
        unique=True, 
        nullable=False
    )

    hashed_password = Column(
        String(255), 
        nullable=False
    )

    role = Column(
        String(50), 
        default="CUSTOMER", 
        nullable=False
    )

    phone = Column(
        String(30), 
        unique=True, 
        nullable=False
    )

    status = Column(
        String(50), 
        default="ACTIVE",
        nullable=False
    )

    timestamps = Column(
        DateTime, 
        default=datetime.utcnow
    )
    
    restaurants = relationship (
        "Restaurant",
        back_populates="owner"
    )