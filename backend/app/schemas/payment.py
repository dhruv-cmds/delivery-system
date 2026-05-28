from pydantic import (

    BaseModel,
    Field
)

from decimal import Decimal

from datetime import datetime

from typing import Literal


class PaymentBase(BaseModel):

    # Literal means only these values are allowed:
    
    payment_method: Literal[
        "UPI",
        "CARD",
        "COD",
        "ONLINE"  
    ] = Field(
        ..., 
        examples=[
            "UPI",
            "CARD",
            "COD",
            "ONLINE"
        ]
    )

class PaymentCreate(PaymentBase):

    pass 

class PaymentResponse(PaymentBase):

    id: int = Field(..., examples=[1])
    order_id: int = Field(..., examples=[454])
    amount: Decimal = Field(..., examples=[799.00])
    status: str = Field(..., examples=["PENDING"])

    paid_at: datetime | None = Field(
        None,
        examples=["2026-05-26T14:30:00"]
    )
    
    transaction_reference: str | None =  Field(
        None,
        examples=["txn_928374923"]
    )
    
    model_config = {

        "from_attributes" : True
    }
