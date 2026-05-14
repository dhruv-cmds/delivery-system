from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    message = Column(
        Text,
        nullable=False
    )

    # EXAMPLES:
    # ORDER_UPDATE / PAYMENT / DELIVERY / SYSTEM
    notification_type = Column(
        String(100),
        nullable=False,
        index=True
    )

    status = Column(
        String(20),
        default="UNREAD",
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

    notifications = relationship(
        "Notification",
        back_populates="user"
    )

    user = relationship(
        "User"
    )