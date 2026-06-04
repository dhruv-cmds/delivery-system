from pydantic import (
    
    BaseModel,
    Field
)

from .common import (

    NameStr,
    PhoneStr
)

from app.core import RestaurantStatus

# common/shared fields
class RestaurantBase(BaseModel):

    name: NameStr = Field(
        ..., 
        examples=[
            "Noodle Nest", "Cafe Aroma", 
            "The Taste Hub"
        ]
    )
    
    phone: PhoneStr = Field(..., examples=["9892760261"])

    address: str = Field(
        ..., 
        examples=[
            "101 Food Street, Alkapuri, Vadodara", 
            "12 Pizza Plaza, Akota, Vadodara"
        ]
    )


# frontend sends this to FastAPI
class RestaurantCreate(RestaurantBase):

    pass 


# FastAPI returns this to frontend
class RestaurantResponse(RestaurantBase):

    id: int = Field(..., examples=[35])
    owner_id: int | None = Field(None, examples=[1])
    status: RestaurantStatus = Field(..., examples=[RestaurantStatus.OPEN])

    model_config = {

        "from_attributes" : True
    }
