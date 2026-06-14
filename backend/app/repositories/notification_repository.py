from sqlalchemy import select, update, and_

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import  NotificationStatus

from app.db.models import Notification, User


async def create_notification (
        db: AsyncSession,   
        notification: Notification
    ):

    if notification.id is None:

        db.add(notification)

    return notification


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

    return notification
    

async def mark_all_notifications_as_read(
        db: AsyncSession,
        current_user: User
    ):


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
            ), 
        )
    )

    return result.scalar_one_or_none()


async def delete_notification(
        db: AsyncSession,
        notification_id: int
    ):

    notification = await db.execute(
        select(Notification)
        .where(Notification.id == notification_id)
    )

    await db.delete(notification)

    
async def get_all_notifications(
        db: AsyncSession,
    ):

    
    result = await db.execute (
        select(Notification)
        .order_by(Notification.created_at.desc())
    )

    return result.scalars().all()


async def get_notifications_by_user_id(
        db: AsyncSession,
        user_id: int,
    ):

    result = await db.execute(
        select(Notification)
        .where(
            Notification.user_id == user_id,
            
        )
        .order_by(Notification.created_at.desc())
    )

    return result.scalars().all()