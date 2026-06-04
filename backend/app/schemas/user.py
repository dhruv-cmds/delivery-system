from pydantic import (
    
    BaseModel, 
    Field
)


from .common import (

    NameStr,
    PasswordStr,
    PhoneStr,
    Email
)

from app.core import (

    UserRole,
    UserStatus
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
    role: UserRole = Field(..., examples=[UserRole.CUSTOMER])
    status: UserStatus = Field(..., examples=[UserStatus.ACTIVE])

    model_config = {
        "from_attributes": True
    }
