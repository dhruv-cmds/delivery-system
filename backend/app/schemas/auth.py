from pydantic import (

    BaseModel,
    Field
)

from app.schemas import (

    PasswordStr,
    Email
)

class LoginRequest (BaseModel):
    
    email: Email = Field (..., examples=["adamexample@gmail.com"])
    password : PasswordStr = Field (..., examples=["Strongpass123"])

class TokenResponse (BaseModel):

    access_token: str = Field (

        ..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...."]
    )

    token_type : str = Field (

        "bearer",
        examples=["bearer"]
    )