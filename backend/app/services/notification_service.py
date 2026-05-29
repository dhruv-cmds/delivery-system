from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import NotificationCreate


from app.db.models import Notification


from app.core import (
    
    logger,

    DatabaseError

)

async def create_notification (
        db: AsyncSession,
        data: NotificationCreate
    ):

    notification = Notification (

        user_id=data.user_id,
        message=data.message,
        notification_type=data.notification_type,
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
        user_id: int
    ):

    result = await db.execute(

        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    )

    return result.scalars().all()

async def mark_notification_as_read(
        db: AsyncSession,
        notification_id:int,
        user_id:int
    ):

    result = await db.execute(

        select(Notification)
        .where(
            (Notification.id == notification_id),
            (Notification.user_id == user_id)
        )
    )

    notification = result.scalar_one_or_none()

    if not notification:

        logger.warning("No notification to read")
        return None
    
    notification.status = "READ"


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
        user_id: int
    ):

    result = await db.execute(

        select(Notification)
        .where(
            (Notification.id == notification_id),
            (Notification.user_id == user_id)
        )
    )

    notification = result.scalar_one_or_none()

    if not notification:

        logger.warning("No notification to delete")

        return None

    try:

        await db.delete(notification)

        await db.commit()

        return True

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while deleting notification")
        raise DatabaseError()  
