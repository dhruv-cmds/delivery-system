from passlib.context import CryptContext

from jose import jwt

from datetime import (
    datetime, 
    timedelta, 
    timezone
)

from .config import setting


pwd_content = CryptContext(schemes=["bycrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_content.hash(password)


def verify_password(plain, hashed):
    return pwd_content.verify(plain, hashed)


def create_access_token(data: dict):
    
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode, 
        setting.SECRET_KEY, setting.ALGORITHM
    )

    return token