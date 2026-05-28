from pydantic import (

    BaseModel,
    Field
)

from typing import Literal

from datetime import datetime


class NotificationBase(BaseModel):

    user_id: int = Field(..., examples=[57])
    
    message: str = Field(..., examples=["Your order is being prepared"])

    notification_type: Literal[

        "ORDER_UPDATE",
        "PAYMENT",
        "DELIVERY",
        "SYSTEM"
    ] = Field(..., examples=["ORDER_UPDATE"])


class NotificationCreate(NotificationBase):

    pass 

class NotificationResponse(NotificationBase):

    id: int = Field(..., examples=[1])
    status: Literal["UNREAD", "READ"] = Field(..., examples=["UNREAD"])
    created_at: datetime = Field(..., examples=["2026-05-26T14:30:00"])

    model_config = {

        "from_attributes" : True
    }
