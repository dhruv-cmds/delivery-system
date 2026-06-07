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
    summary="Register a new user",
    description=(
        "Create a new user account with a unique username. "
        "Passwords are securely hashed before storage."
    ),
)
@limiter.limit("3/second")
async def sign_up(
    request: Request,
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await auth_service.sign_up(
        db,
        user,
    )


@router.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="Authenticate user",
    description=(
        "Verify user credentials and return a JWT access token "
        "for authenticated requests."
    ),
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