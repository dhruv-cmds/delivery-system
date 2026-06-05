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
    PermissionDeniedError,
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

            raise InvalidTokenError()

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

async def require_admin_access(current_user = Depends(get_current_user)):

    if current_user.role != UserRole.ADMIN:

        raise AdminAccessRequiredError()

    return current_user


async def get_access_manager(current_user = Depends(get_current_user)):

    if current_user.role not in (
        UserRole.ADMIN,
        UserRole.RESTAURANT_OWNER
    ):

        raise PermissionDeniedError()
    
    return current_user


async def require_restaurant_access(current_user = Depends(get_current_user)):

    if current_user.role not in (
        UserRole.ADMIN,
        UserRole.RESTAURANT_OWNER,
        UserRole.CUSTOMER
    ):

        raise PermissionDeniedError()
    
    return current_user


async def get_order_manager(current_user = Depends(get_current_user)):

    if current_user.role not in (
        UserRole.ADMIN,
        UserRole.RESTAURANT_OWNER,
        UserRole.DELIVERY_PARTNER
    ):

        raise PermissionDeniedError()
    
    return current_user
