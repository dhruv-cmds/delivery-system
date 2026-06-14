from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import limiter

from app.schemas import NotificationResponse

from app.services import notification_service

from app.api import (
    get_current_user,
    require_admin_access,
    get_db
)

routes = APIRouter(
    prefix="/notification",
    tags=["NOTIFICATION"]
)

admin = APIRouter(
    prefix="/admin/notification",
    tags=["ADMIN NOTIFICATIONS"]
)


@routes.get(
    "/",
    response_model=list[NotificationResponse],
    summary="Get notifications",
    description="Retrieve all notifications for the authenticated user."
)
@limiter.limit("120/minute")
async def get_user_notifications(
        request: Request,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await notification_service.get_user_notifications(
        db,
        current_user,
    )


@routes.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Get notification",
    description="Retrieve a notification by its ID."
)
@limiter.limit("120/minute")
async def get_notification_by_id(
        request: Request,
        notification_id: int,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await notification_service.get_notification_by_id(
        db,
        notification_id,
        current_user,
    )


@routes.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    summary="Mark notification as read",
    description="Mark a notification as read."
)
@limiter.limit("60/minute")
async def mark_notification_as_read(
        request: Request,
        notification_id: int,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await notification_service.mark_notification_as_read(
        db,
        notification_id,
        current_user,
    )


@routes.patch(
    "/read-all",
    summary="Mark all notifications as read",
    description="Mark all user notifications as read."
)
@limiter.limit("20/minute")
async def mark_all_notifications_as_read(
        request: Request,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await notification_service.mark_all_notifications_as_read(
        db,
        current_user,
    )


@routes.delete(
    "/{notification_id}",
    summary="Delete notification",
    description="Delete a notification by its ID."
)
@limiter.limit("60/minute")
async def delete_notification(
        request: Request,
        notification_id: int,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await notification_service.delete_notification(
        db,
        notification_id,
        current_user,
    )


@admin.get(
    "/all",
    response_model=list[NotificationResponse],
    summary="Get all notifications",
    description="Retrieve all notifications in the system."
)
@limiter.limit("60/minute")
async def get_all_notifications(
        request: Request,
        current_user=Depends(require_admin_access),
        db: AsyncSession = Depends(get_db)
    ):

    return await notification_service.get_all_notifications(
        db,
        current_user,
    )


@admin.get(
    "/user/{user_id}",
    response_model=list[NotificationResponse],
    summary="Get user notifications",
    description="Retrieve all notifications for a specific user."
)
@limiter.limit("60/minute")
async def get_notifications_by_user_id(
        request: Request,
        user_id: int,
        current_user=Depends(require_admin_access),
        db: AsyncSession = Depends(get_db)
    ):

    return await notification_service.get_notifications_by_user_id(
        db,
        user_id,
    )
