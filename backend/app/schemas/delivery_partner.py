from pydantic import (

    BaseModel,
    Field
)

from app.core import VehicleTypeStatus

from decimal import Decimal

from app.core import DeliveryPartnerStatus

class DeliveryPartnerBase(BaseModel):

    vehicle_type: VehicleTypeStatus = Field(
        ..., 
        examples=[
            VehicleTypeStatus.TWO_WHEELER,
            VehicleTypeStatus.FOUR_WHEELER
        ]
    )

class DeliveryPartnerCreate(DeliveryPartnerBase):

    pass 

class DeliveryPartnerResponse(DeliveryPartnerBase):

    id: int = Field(..., examples=[603])
    user_id: int = Field(..., examples=[79])
    status: DeliveryPartnerStatus = Field(..., examples=[DeliveryPartnerStatus.AVAILABLE])

    rating: Decimal | None = Field(None, examples=[5.00, 3.9])
    latitude: Decimal | None = Field(None, examples=[22.3072])
    longitude: Decimal | None = Field(None, examples=[73.1812])

    model_config = {

        "from_attributes" : True
    }
