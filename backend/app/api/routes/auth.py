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

router = APIRouter(tags=["Authentication"])


@router.post(
    "/signup",
    response_model=UserResponse,
    summary="User Registration",
    description=(
        "Create a new user."
        "Password are hashed and User's username need to be unique"
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
    "/login",
    response_model=TokenResponse,
    summary="User login and obtain JWT bearer token",
    description=(
        "Authenticate with email and password to receive an access token. "
        "Use the returned Bearer token for protected endpoints via the Authorization header."
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
