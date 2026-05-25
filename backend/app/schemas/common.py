from pydantic import StringConstraints, EmailStr
from typing import Annotated

NameStr = Annotated[
    str,
    StringConstraints(
        min_length=2,
        max_length=100
    )
]

PasswordStr = Annotated[
    str,
    StringConstraints(
        min_length=8,
        max_length=100
    )
]

PhoneStr = Annotated[
    str,
    StringConstraints(
        min_length=7,
        max_length=100
    )
]

EmailStr = Annotated[
    EmailStr,
    StringConstraints(
        max_length=100
    )
]