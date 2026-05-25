from pydantic import (

    BaseModel,
    Field
)

from decimal import Decimal
# from app.schemas import

class MenuBase (BaseModel):

    restaurant_id: int = Field(..., examples=["1", "2" , "3"])
    item_name: str = Field(..., examples=["pizza", "burger", "cold drinks"])
    description: str | None = Field(None, examples=["Cheese pizza with extra toppings"])
    price: Decimal = Field(..., examples=[499.00, 599.00, 999.00])


class MenuCreate (MenuBase):

    pass

class MenuResponse (MenuBase):

    id: int = Field(..., examples=[24])
    status: str = Field(..., examples=["AVAILABLE"])

    model_config = {

        "from_attributes" : True
    }