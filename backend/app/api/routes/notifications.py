from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import limiter

from app.schemas import NotificationResponse

from app.services import notification_service

from app.api import (
    
    get_current_user,
    get_db
)


routes = APIRouter(
    prefix="/notification",
    tags=["Notification"]
)

@routes.get(
    "/",
    response_model= list[NotificationResponse],
    summary="Get a list of notifications",
    description="Only current user can get all notfication"
)
@limiter.limit("3/second")
async def get_user_notifications(
        request: Request,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await notification_service.get_user_notifications(
        db,
        current_user,
    )


@routes.get(
    "/{notification_id}",
    response_model= NotificationResponse,
    summary="Get a specific notification",
    description="Only current user can get specific notfication"
)
@limiter.limit("3/second")
async def get_user_notifications_by_id(
        request: Request,
        notification_id: int,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await notification_service.get_notification_by_user_id(
        db,
        notification_id,
        current_user,
    )


@routes.patch(
    "/{notification_id}/read",
    response_model= NotificationResponse,
    summary="check a notification ha been readed or not",
    description="Only current user can get specific notfication"
)
@limiter.limit("3/second")
async def mark_notification_as_read(
        request: Request,
        notification_id: int,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await notification_service.mark_notification_as_read(
        db,
        notification_id,
        current_user,
    )


@routes.delete(
    "/{notification_id}",
    response_model= NotificationResponse,
    summary="Delete a notification",
    description="Only current user can delete theire notfication"
)
@limiter.limit("3/second")
async def delete_notification(
        request: Request,
        notification_id: int,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await notification_service.delete_notification(
        db,
        notification_id,
        current_user,
    )