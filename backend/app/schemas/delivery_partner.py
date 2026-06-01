from pydantic import (

    BaseModel,
    Field
)


from decimal import Decimal


class DeliveryPartnerBase(BaseModel):

    vehicle_type: str = Field(..., examples=["Two wheeler", "Four wheeler"])

class DeliveryPartnerCreate(DeliveryPartnerBase):

    pass 

class DeliveryPartnerResponse(DeliveryPartnerBase):

    id: int = Field(..., examples=[603])
    user_id: int = Field(None, examples=[79])
    status: str = Field(..., examples=["PENDING"]) 

    rating: Decimal | None = Field(None, examples=[5.00, 3.9])
    latitude: Decimal | None = Field(None, examples=[22.3072])
    longitude: Decimal | None = Field(None, examples=[73.1812])

    model_config = {

        "from_attributes" : True
    }