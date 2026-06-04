from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from .order_item import OrderItemCreate, OrderItemResponse

from app.core import OrderStatus, PaymentStatus


class OrderCreate(OrderItemCreate):

    delivery_address: str = Field(
        ...,
        examples=["101 Food Street, Alkapuri, Vadodara"]
    )


class OrderResponse(BaseModel):

    id: int = Field(..., examples=[1])
    customer_id: int = Field(..., examples=[10])
    restaurant_id: int = Field(..., examples=[5])
    delivery_partner_id: int | None = Field(None, examples=[2])
    status: OrderStatus = Field(..., examples=[OrderStatus.PENDING])
    total_price: Decimal = Field(..., examples=[499.00])
    delivery_address: str = Field(
        ...,
        examples=["101 Food Street, Alkapuri, Vadodara"]
    )
    payment_status: PaymentStatus = Field(..., examples=[PaymentStatus.PENDING])
    created_at: datetime = Field(..., examples=["2026-05-26T14:30:00"])
    updated_at: datetime = Field(..., examples=["2026-05-26T14:30:00"])
    order_items: list[OrderItemResponse] = Field(default_factory=list)

    model_config = {

        "from_attributes": True
    }
