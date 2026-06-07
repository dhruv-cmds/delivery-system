from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import (
    limiter, 
)

from app.services import user_service
from app.api.dbcon import get_db

from app.api.deps import (  
    require_admin_access,
)

from app.schemas import UserResponse

router = APIRouter(tags=["Users"])

@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a user by their ID."
)
@limiter.limit("3/second")
async def get_user_by_id(
        request: Request,
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_admin_access)
    ):

    return await user_service.get_user_by_id(
        db,
        user_id,
        current_user
    )


@router.get(
    "/users",
    response_model=list[UserResponse],
    summary="Get all users",
    description="Retrieve all registered users."
)
@limiter.limit("3/second")
async def get_all_users(
        request: Request,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_admin_access)
    ):

    return await user_service.get_all_users(db)


@router.get(
    "/email/{user_email}",
    response_model=UserResponse,
    summary="Get user by email",
    description="Retrieve a user by their email address."
)
@limiter.limit("3/second")
async def get_user_by_email(
        request: Request,
        user_email: str,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_admin_access)
    ):

    return await user_service.get_user_by_email(
        db,
        user_email,
        current_user
    )


@router.get(
    "/username/{username}",
    response_model=UserResponse,
    summary="Get user by username",
    description="Retrieve a user by their username."
)
@limiter.limit("3/second")
async def get_user_by_username(
        request: Request,
        username: str,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_admin_access)
    ):

    return await user_service.get_user_by_username(
        db,
        username
    )