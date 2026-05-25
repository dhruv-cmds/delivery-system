from pydantic import (
    
    BaseModel, 
    Field
)


from app.schemas import (

    NameStr,
    PasswordStr,
    PhoneStr,
    Email
)


class UserBase (BaseModel):
    
    username: NameStr = Field (..., examples=["adam"])
    name: NameStr = Field (..., examples=["adam das"])
    phone: PhoneStr = Field (..., examples=["9876543201"])
    email: Email = Field (..., examples=["adamexample@gmail.com"])

class UserCreate (UserBase):

    password: PasswordStr = Field (..., examples=["Strongpass123"])

class UserResponse (UserBase):

    id: int = Field(..., examples=[1])
    role: str = Field(..., examples=["CUSTOMER"])
    status: str = Field(..., examples=["ACTIVE"])

    model_config = {
        "from_attributes": True
    }