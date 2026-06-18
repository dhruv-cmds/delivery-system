import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import OrderTracking, User

from app.core import (
    DatabaseError,
    InvalidLongitudeError,
    InvalidLatitudeError,
    OrderNotFoundError,
    PermissionDeniedError,
    UserRole,

    redis_client,

    logger
)

from app.repositories import traking_repository
from app.schemas import TrackingCreate, TrackingResponse

#  only res owners can admin can make order traking service then share wiht use through notification or link (only admin can do rn)
async def create_tracking(
        db: AsyncSession,
        tracking: TrackingCreate
    ):
    
    if tracking.latitude < -90 or tracking.latitude > 90:
        raise  InvalidLatitudeError()

    if tracking.longitude < -180 or tracking.longitude > 180:
        raise  InvalidLongitudeError()
    
    new_tracking = OrderTracking(
        order_id=tracking.order_id,
        latitude=tracking.latitude,
        longitude=tracking.longitude,
    )

    try:
        
        db.add(new_tracking)

        await db.commit()
        
        await db.refresh(new_tracking)

        logger.info(
            "Order tracking created successfully (order_id=%s)",
            tracking.order_id
        )
        
        return new_tracking

    except Exception:

        await db.rollback()

        logger.exception(
            "Unexpected error while creating order tracking update"
        )

        raise DatabaseError()
    
async def get_tracking_by_order(
        db: AsyncSession,
        order_id: int,
        current_user: User
    ):
    
    tracking = await traking_repository.get_tracking_order(
        db,
        order_id
    )

    if not tracking:

        logger.warning(

            "Traking not found by (order_id=%s)",
            order_id
        )

        raise OrderNotFoundError()
    
    if (
         current_user.role != UserRole.ADMIN
         and tracking.order.customer_id != current_user.id 
    ):
        
        logger.warning(
            "Traking for order denied: user ID %s is not the owner of order",
            current_user.id
        )
         
        raise PermissionDeniedError()
    

    cache_key = f"tracking:order:{order_id}"

    cache_fetch = await redis_client.get(cache_key)

    if cache_fetch:
        logger.info(
            "Tracking retrieved from Redis (order_id=%s)",
            order_id,
        )

        return TrackingResponse.model_validate_json(cache_fetch)
    
    response = TrackingResponse.model_validate(

        tracking,
        from_attributes=True,
    )

    await redis_client.set(
        cache_key,
        response.model_dump_json(),
        ex=300
    )
    
    logger.info(
        "Order tracking retrieved successfully (order_id=%s)",
        order_id
    )

    return response

async def get_all_tracking (
        db: AsyncSession,
    ):

    return await traking_repository.get_all_traking(db)
