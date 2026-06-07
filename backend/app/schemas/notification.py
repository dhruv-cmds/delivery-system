from pydantic import (

    BaseModel,
    Field
)

from typing import Literal

from datetime import datetime

from app.core import NotificationType, NotificationStatus

class NotificationBase(BaseModel):

    user_id: int = Field(..., examples=[57])
    
    message: str = Field(..., examples=["Your order is being prepared"])

    notification_type: NotificationType = Field(..., examples=[NotificationType.ORDER_UPDATE])


class NotificationCreate(NotificationBase):

    pass

class NotificationResponse(NotificationBase):

    id: int = Field(..., examples=[1])
    status: NotificationStatus = Field(..., examples=[NotificationStatus.UNREAD])
    created_at: datetime = Field(..., examples=["2026-05-26T14:30:00"])

    model_config = {

        "from_attributes" : True
    }
