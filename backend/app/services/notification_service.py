from sqlalchemy.ext.asyncio import AsyncSession

from app.core import (
    logger,
    DatabaseError,
    PermissionDeniedError,
    NotificationNotFoundError,
    NotificationType,
    NotificationStatus,
    UserRole,
)

from app.db.models import Notification, User

from app.repositories import notification_repository


async def create_notification(
    db: AsyncSession,
    user_id: int,
    message: str,
    notification_type: NotificationType,
):

    notification = Notification(
        user_id=user_id,
        message=message,
        notification_type=notification_type,
    )

    try:

        async with db.begin():

            notification = (
                await notification_repository.create_notification(
                    db,
                    notification,
                )
            )

        await db.refresh(notification)

        logger.info(
            "Notification created successfully (user_id=%s, type=%s)",
            user_id,
            notification_type,
        )

        return notification

    except Exception:

        logger.exception(
            "Unexpected error while creating notification"
        )

        raise DatabaseError()


async def get_user_notifications(
    db: AsyncSession,
    current_user: User,
):

    return await notification_repository.get_user_notifications(
        db,
        current_user,
    )


async def get_notification_by_id(
    db: AsyncSession,
    notification_id: int,
    current_user: User,
):

    notification = (
        await notification_repository.get_notification_by_id(
            db,
            notification_id,
            current_user,
        )
    )

    if not notification:

        logger.warning(
            "Notification not found or access denied "
            "(notification_id=%s, user_id=%s)",
            notification_id,
            current_user.id,
        )

        raise NotificationNotFoundError()

    return notification


async def mark_notification_as_read(
    db: AsyncSession,
    notification_id: int,
    current_user: User,
):

    notification = (
        await notification_repository.get_notification_by_id(
            db,
            notification_id,
            current_user,
        )
    )

    if not notification:

        logger.warning(
            "Notification not found "
            "(notification_id=%s, user_id=%s)",
            notification_id,
            current_user.id,
        )

        raise NotificationNotFoundError()

    try:

        async with db.begin():

            notification.status = (
                NotificationStatus.READ
            )

        await db.refresh(notification)

        return notification

    except Exception:

        logger.exception(
            "Unexpected error while marking notification as read"
        )

        raise DatabaseError()


async def mark_all_notifications_as_read(
    db: AsyncSession,
    current_user: User,
):

    try:

        async with db.begin():

            await (
                notification_repository
                .mark_all_notifications_as_read(
                    db,
                    current_user,
                )
            )

        logger.info(
            "All notifications marked as read "
            "(user_id=%s)",
            current_user.id,
        )

        return {
            "message": (
                "All notifications marked as read"
            )
        }

    except Exception:

        logger.exception(
            "Unexpected error while marking "
            "all notifications as read"
        )

        raise DatabaseError()


async def delete_notification(
    db: AsyncSession,
    notification_id: int,
    current_user: User,
):

    notification = (
        await notification_repository
        .get_notification_by_id(
            db,
            notification_id,
            current_user,
        )
    )

    if not notification:

        logger.warning(
            "Notification deletion failed: "
            "notification not found "
            "(notification_id=%s, user_id=%s)",
            notification_id,
            current_user.id,
        )

        raise NotificationNotFoundError()

    try:

        async with db.begin():

            await notification_repository.delete_notification(
                db,
                notification_id,
            )

        logger.info(
            "Notification deleted successfully "
            "(notification_id=%s)",
            notification_id,
        )

        return True

    except Exception:

        logger.exception(
            "Unexpected error while deleting "
            "notification"
        )

        raise DatabaseError()


async def get_all_notifications(
    db: AsyncSession,
    current_user: User,
):

    if current_user.role != UserRole.ADMIN:

        logger.warning(
            "Notification access denied: "
            "user ID %s is not an administrator",
            current_user.id,
        )

        raise PermissionDeniedError()

    return await (
        notification_repository
        .get_all_notifications(db)
    )


async def get_notifications_by_user_id(
    db: AsyncSession,
    user_id: int,
    current_user: User,
):

    if current_user.role != UserRole.ADMIN:

        logger.warning(
            "User notification access denied: "
            "user ID %s is not an administrator",
            current_user.id,
        )

        raise PermissionDeniedError()

    return await (
        notification_repository
        .get_notifications_by_user_id(
            db,
            user_id,
        )
    )