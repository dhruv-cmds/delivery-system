from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import limiter
from app.services import auth_service
from app.api.dbcon import get_db

from app.schemas import (

    LoginRequest,
    UserCreate,
    UserResponse,
    TokenResponse,
)

router = APIRouter(tags=["AUTHENTICATION"])


@router.post(
    "/auth/signup",
    response_model=UserResponse,
    summary="Create a user account",
    description=(
        "Register a new user account. The password is hashed before storage, "
        "and the username must be unique."
    )
)
@limiter.limit("3/second")
async def sign_up(
    request: Request,
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):

    return await auth_service.sign_up(
        db,
        user
    )


@router.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="Log in and get an access token",
    description=(
        "Authenticate with an email address and password. Returns a JWT bearer "
        "token that can be used in the Authorization header for protected endpoints."
    )
)
@limiter.limit("5/minute")
async def login(
    request: Request,
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db),
):

    return await auth_service.login(
        db,
        credentials.email,
        credentials.password,
    )
