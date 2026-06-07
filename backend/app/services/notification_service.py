from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import NotificationCreate

from app.core import NotificationType, NotificationStatus

from app.db.models import Notification, User

from app.core import (
    
    logger,
    DatabaseError,
    PermissionDeniedError

)

from app.core import UserRole

async def create_notification (
        db: AsyncSession,
        user_id: int,
        message: str,
        notification_type: NotificationType
        
    ):

    notification = Notification (

        user_id=user_id,
        message=message,
        notification_type=notification_type
    )

    try:

        db.add(notification)

        await db.commit()

        await db.refresh(notification)

        return notification
        
    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while creating notification")
        raise DatabaseError()
    

async def get_user_notifications(    
        db: AsyncSession,
        current_user: User
    ):

    result = await db.execute(

        select(Notification)
        .where(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
    )

    return result.scalars().all()

async def get_notification_by_id(
        db: AsyncSession,
        notification_id: int,
        current_user: User
    ):

    result = await db.execute(
        select(Notification)
        .where(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    )

    notification = result.scalar_one_or_none()

    if not notification:

        logger.warning(
            "Notification not found or does not belong to the user"
        )
        raise PermissionDeniedError()

    return notification
    
async def mark_notification_as_read(
        db: AsyncSession,
        notification_id: int,
        current_user: User
    ):

    result = await db.execute(

        select(Notification)
        .where(
            (Notification.id == notification_id),
            (Notification.user_id == current_user.id)
        )
    )

    notification = result.scalar_one_or_none()

    if not notification:

        logger.warning(
            "Notification read failed because the notification was not found"
        )
        return None
    
    notification.status = NotificationStatus.READ

    try:

        await db.commit()

        await db.refresh(notification)

        return notification

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while marking notification as read")
        raise DatabaseError()
    

async def mark_all_notifications_as_read(
        db: AsyncSession,
        current_user: User
    ):

    try:

        await db.execute(
            update(Notification)
            .where(
                Notification.user_id == current_user.id,
                Notification.status == NotificationStatus.UNREAD
            )
            .values(
                status=NotificationStatus.READ
            )
        )

        await db.commit()

        return {
            "message": "All notifications marked as read"
        }

    except Exception:

        await db.rollback()

        logger.exception(
            "Unexpected error while marking all notifications as read"
        )
        raise DatabaseError()


async def delete_notification(
        db: AsyncSession,
        notification_id: int,
        current_user: User
    ):

    result = await db.execute(

        select(Notification)
        .where(
            (Notification.id == notification_id),
            (Notification.user_id == current_user.id)
        )
    )

    notification = result.scalar_one_or_none()

    if not notification:

        logger.warning(
            "Notification deletion failed because the notification was not found"
        )

        return None

    try:

        await db.delete(notification)

        await db.commit()

        return True

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while deleting notification")
        raise DatabaseError()  
    

async def get_all_notifications(
        db: AsyncSession,
        current_user: User
    ):

    if current_user.role != UserRole.ADMIN:

        logger.warning(
            "Notfications access denied because the user is not admin"
        )
        raise PermissionDeniedError()
    
    result = await db.execute (
        select(Notification)
        .order_by(Notification.created_at.desc())
    )

    return result.scalars().all()


async def get_notifications_by_user_id(
        db: AsyncSession,
        user_id: int,
        current_user: User
    ):

    if current_user.role != UserRole.ADMIN:

        logger.warning(
        "Notification access denied beacause the user is not admin")
        raise PermissionDeniedError()
    

    result = await db.execute(
        select(Notification)
        .where(
            Notification.user_id == user_id
        )
        .order_by(Notification.created_at.desc())
    )

    return result.scalars().all()