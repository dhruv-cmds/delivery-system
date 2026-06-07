from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import NotificationCreate

from app.core import NotificationType, NotificationStatus

from app.db.models import Notification, User

from app.core import (
    
    logger,
    DatabaseError,
    PermissionDeniedError

)

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

async def get_notification_by_user_id(
        db: AsyncSession,
        notification_id: int,
        current_user: User
    ):

    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == current_user.id)
    )

    if not result:

        logger.warning(
            "You can't access another users notfications"
        )
        raise PermissionDeniedError()
    
    return await db.execute(
        select(Notification)
        .where(Notification.id == notification_id)
    )
    
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
