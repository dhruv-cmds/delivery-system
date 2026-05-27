from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class WebSocketSubscribe(BaseModel):

    channel: Literal[
        "orders",
        "order_tracking",
        "notifications",
        "live_location",
    ] = Field(..., examples=["order_tracking"])

    user_id: int | None = Field(None, examples=[5])
    order_id: int | None = Field(None, examples=[12])


class LiveLocationUpdate(BaseModel):

    order_id: int = Field(..., examples=[12])
    delivery_partner_id: int = Field(..., examples=[3])
    latitude: Decimal = Field(..., examples=[28.613939])
    longitude: Decimal = Field(..., examples=[77.209023])
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WebSocketError(BaseModel):

    error: str = Field(..., examples=["Invalid message"])
    detail: str | None = Field(None, examples=["Unsupported websocket event"])