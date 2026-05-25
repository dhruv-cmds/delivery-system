from pydantic import StringConstraints
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
        min_length=2,
        max_length=100
    )
]

PhoneStr = Annotated[
    str,
    StringConstraints(
        min_length=2,
        max_length=100
    )
]

EmailStr = Annotated[
    str,
    StringConstraints(
        min_length=2,
        max_length=100
    )
]