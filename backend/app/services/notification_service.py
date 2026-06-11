from sqlalchemy import select, update, and_

from sqlalchemy.ext.asyncio import AsyncSession

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

        logger.info(
            "Notification created successfully (user_id=%s, type=%s)",
            user_id,
            notification_type
        )
        
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
            and_(
                (Notification.id == notification_id),
                (Notification.user_id == current_user.id)
            )
        )
    )

    notification = result.scalar_one_or_none()

    if not notification:

        logger.warning(
            "Notification not found or access denied (notification_id=%s, user_id=%s)",
            notification_id,
            current_user.id
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
            and_(
                (Notification.id == notification_id),
                (Notification.user_id == current_user.id)
            ),
        )
    )

    notification = result.scalar_one_or_none()

    if not notification:

        logger.warning(
        "Notification not found (notification_id=%s, user_id=%s)",
        notification_id,
        current_user.id
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
                and_(
                    Notification.user_id == current_user.id,
                    Notification.status == NotificationStatus.UNREAD
                ),
            )
            .values(
                status=NotificationStatus.READ
            )
        )

        await db.commit()

        logger.info(
            "All notifications marked as read (user_id=%s)",
            current_user.id
        )
        
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
            and_(
                (Notification.id == notification_id),
                (Notification.user_id == current_user.id)
            ), 
        )
    )

    notification = result.scalar_one_or_none()

    if not notification:

        logger.warning(
            "Notification deletion failed: notification not found (notification_id=%s, user_id=%s)",
            notification_id,
            current_user.id
        )

        return None

    try:

        await db.delete(notification)

        await db.commit()

        logger.info(
            "Notification deleted successfully (notification_id=%s)",
            notification_id
        )

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
            "Notification access denied: user ID %s is not an administrator",
            current_user.id
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
            "User notification access denied: user ID %s is not an administrator",
            current_user.id
        )
        
        raise PermissionDeniedError()
    

    result = await db.execute(
        select(Notification)
        .where(
            Notification.user_id == user_id
        )
        .order_by(Notification.created_at.desc())
    )

    return result.scalars().all()