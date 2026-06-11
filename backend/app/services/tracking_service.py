from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import OrderTracking
from app.core import (
    DatabaseError,
    logger
)


async def create_tracking(
        db: AsyncSession,
        order_id: int,
        latitude,
        longitude,
    ):
    
    tracking = OrderTracking(
        order_id=order_id,
        latitude=latitude,
        longitude=longitude,
    )

    try:
        
        db.add(tracking)

        await db.commit()

        await db.refresh(tracking)
        
        logger.info(
            "Order tracking created successfully (order_id=%s)",
            order_id
        )
        
        return tracking

    except Exception:

        await db.rollback()

        logger.exception(
            "Unexpected error while creating order tracking update"
        )

        raise DatabaseError()
    
async def get_tracking_by_order(
        db: AsyncSession,
        order_id: int,
    ):

    result = await db.execute(
        select(OrderTracking)
        .where(OrderTracking.order_id == order_id)
        .order_by(OrderTracking.created_at.desc())
    )

    logger.info(
        "Order tracking retrieved successfully (order_id=%s)",
        order_id
    )

    return result.scalars().all()
