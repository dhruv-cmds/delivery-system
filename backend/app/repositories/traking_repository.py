from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import OrderTracking

    
async def get_tracking_order(
        db: AsyncSession,
        order_id: int,
    ):

    result = await db.execute(
        
        select(OrderTracking)
        .where(OrderTracking.order_id == order_id)
        .order_by(OrderTracking.created_at.desc())
    )

    return result.scalars().first()

async def get_all_traking(
        db: AsyncSession,
    ):


    result = await db.execute(

        select(OrderTracking)
    )

    return result.scalars().all()