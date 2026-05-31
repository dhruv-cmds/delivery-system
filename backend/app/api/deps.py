from fastapi import Depends, Security
from jose import jwt, JWTError, ExpiredSignatureError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .dbcon import get_db

from app.db.models import User

from app.core import (
    UserRole,
    setting,
    AdminAccessRequiredError,
    TokenExpiredError,
    InvalidTokenError,
    UserNotFoundError,
)

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_schema = HTTPBearer(auto_error=True)

async def get_current_user(
        
        credentials: HTTPAuthorizationCredentials = Security(bearer_schema),
        db: AsyncSession = Depends(get_db)
    ):

    token = credentials.credentials

    try:

        payload = jwt.decode(

            token, 
            setting.SECRET_KEY, 
            algorithms=[setting.ALGORITHM]
        )

        subject = payload.get("sub")

        if subject is None:

            raise InvalidTokenError("Invalid token payload")

        user_id = int(subject)
        
    except ExpiredSignatureError:

        raise TokenExpiredError()
    
    except (JWTError, TypeError, ValueError):

        raise InvalidTokenError()
    
    user_result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )

    user = user_result.scalar_one_or_none()

    if user is None:

        raise UserNotFoundError()
    
    return user

async def get_admin(current_user = Depends(get_current_user)):

    if current_user.role != UserRole.ADMIN.value:

        raise AdminAccessRequiredError()
    
    return current_user
