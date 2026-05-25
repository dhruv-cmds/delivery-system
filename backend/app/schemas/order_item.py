from pydantic import BaseModel, Field


from decimal import Decimal

# Base = common fields
class OrderItemBase (BaseModel):

    menu_item_id: int = Field(..., examples=[23])
    quantity: int = Field(..., examples=[2])


# Create = frontend sends this
class OrderItemCreate (OrderItemBase):

    pass 


# Response = FastAPI returns this to frontend
class OrderItemResponse (OrderItemBase):

    id: int = Field(..., examples=[1, 2, 3])
    order_id: int = Field(..., examples=[1, 2, 3, 4])
    menu_item_id: int = Field(..., examples=[23, 54, 57])
    quantity: int = Field(..., examples=[9, 99, 999])
    unit_price: Decimal = Field(..., examples=[199.00, 299.00, 399.00])
    total_price = Decimal = Field(..., examples=[1999.00, 2999.00, 3999.00])

    model_config = {

        "from_attributes": True
    }