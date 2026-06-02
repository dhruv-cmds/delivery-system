from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import (
    limiter, 
)

from app.services import user_service
from app.api.dbcon import get_db

from app.api.deps import (
    get_current_user, 
    get_admin,
)

from app.schemas import UserResponse

router = APIRouter(tags=["Users"])

@router.get(
    "/id/{user_id}",
    response_model=UserResponse,
    summary="Get user by id number",
    description="Recive a details of a specific user"
)
@limiter.limit("3/second")
async def get_user_by_id(
        request: Request,
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
    ):

    return await user_service.get_user_by_id(
        db,
        user_id
    )


@router.get(
    "/all_users",
    response_model=list[UserResponse],
    summary="Get all users",
    description="Recive details of all users"
)
@limiter.limit("3/second")
async def get_all_users(
        request: Request,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_admin)
    ):

    return await user_service.get_all_users(db)


@router.get(
    "/email/{user_email}",
    response_model=UserResponse,
    summary="Get a users by email",
    description="Recive details of a user by email"
)
@limiter.limit("3/second")
async def get_user_by_email(
        request: Request,
        user_email: str,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
    ):

    return await user_service.get_user_by_email(
        db,
        user_email
    )


@router.get(
    "/username/{username}",
    response_model=UserResponse,
    summary="Get a users by username",
    description="Recive details of a user by username"
)
@limiter.limit("3/second")
async def get_user_by_username(
        request: Request,
        username: str,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
    ):

    return await user_service.get_user_by_username(
        db,
        username
    )