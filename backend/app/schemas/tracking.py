from pydantic import BaseModel, Field

from app.core import OrderStatus

from decimal import Decimal

# common fields
class TrackingBase(BaseModel):

    order_id: int = Field(..., examples=[1])
    latitude: Decimal | None = Field(None, examples=[22.3072])
    longitude: Decimal | None = Field(None, examples=[73.1812])
    status: OrderStatus = Field(..., examples=[OrderStatus.PENDING])


# frontend sends this
class TrackingCreate(TrackingBase):

    pass 


# FastAPI returns this to frontend
class TrackingResponse(TrackingBase):

    id: int = Field(..., examples=[1, 2, 3])
    
    model_config = {

        "from_attributes": True
    }
