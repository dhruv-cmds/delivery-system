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


# common/shared fields
class UserBase(BaseModel):
    
    username: NameStr = Field (..., examples=["adam"])
    name: NameStr = Field (..., examples=["adam das"])
    phone: PhoneStr = Field (..., examples=["9876543201"])
    email: Email = Field (..., examples=["adamexample@gmail.com"])


# frontend sends this to FastAPI
class UserCreate(UserBase):

    password: PasswordStr = Field (..., examples=["Strongpass123"])


# FastAPI returns this to frontend
class UserResponse(UserBase):

    id: int = Field(..., examples=[1])
    role: str = Field(..., examples=["CUSTOMER"])
    status: str = Field(..., examples=["ACTIVE"])

    model_config = {
        "from_attributes": True
    }