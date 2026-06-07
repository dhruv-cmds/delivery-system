from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Restaurant, User
from app.schemas import RestaurantCreate
from app.services import notification_service

from app.core import (

    logger,

    UserRole,
    RestaurantStatus,
    NotificationType,

    DatabaseError,
    
    RestaurantNotFoundError,
    RestaurantAlreadyExistsError,
    RestaurantStatusAlreadySetError,
    PermissionDeniedError,
)

RESTAURANT_STATUS_MESSAGES = {
    RestaurantStatus.PENDING: "Your restaurant is pending review.",
    RestaurantStatus.APPROVED: "Your restaurant has been approved.",
    RestaurantStatus.REJECTED: "Your restaurant has been rejected.",
    RestaurantStatus.SUSPENDED: "Your restaurant has been suspended.",
    RestaurantStatus.CLOSED: "Your restaurant has been closed.",
    RestaurantStatus.OPEN: "Your restaurant is open.",
}

async def create_restaurant(
        db: AsyncSession,
        restaurant: RestaurantCreate,
        current_user: User,
    ):
    
    new_restaurant = Restaurant(
        name=restaurant.name,
        phone=restaurant.phone,
        address=restaurant.address,
        owner_id=current_user.id,
    )

    try:
        db.add(new_restaurant)

        if current_user.role == UserRole.CUSTOMER:

            current_user.role = UserRole.RESTAURANT_OWNER
          
        await db.commit()

        await notification_service.create_notification(

            db=db,
            user_id=current_user.id,
            message="Your restaurant has been created successfully.",
            notification_type=NotificationType.SYSTEM
        )

        await db.refresh(new_restaurant)

        return new_restaurant

    except IntegrityError:

        await db.rollback()

        logger.exception("Database integrity error while creating restaurant")
        raise RestaurantAlreadyExistsError()

    except Exception:
        
        await db.rollback()

        logger.exception("Unexpected error while creating restaurant")
        raise DatabaseError()


async def get_restaurant_by_id(
        db: AsyncSession,
        restaurant_id: int,
    ):


    result = await db.execute(
        select(Restaurant)
        .where(Restaurant.id == restaurant_id)
    )

    restaurant = result.scalar_one_or_none()

    if not restaurant:

        logger.warning(
            "Restaurant lookup failed because the restaurant was not found"
        )
        raise RestaurantNotFoundError()

    return restaurant


async def update_restaurant(
        db: AsyncSession,
        restaurant_id: int,
        restaurant_data: RestaurantCreate,
        current_user: User,
    ):

    restaurant = await get_restaurant_by_id(
        db,
        restaurant_id,
    )

    if (
        current_user.role != UserRole.ADMIN and
        restaurant.owner_id != current_user.id
    ):
        
        logger.warning(
            "Restaurant update denied because the user does not own the restaurant"
        )
        raise PermissionDeniedError()

    restaurant.name = restaurant_data.name
    restaurant.phone = restaurant_data.phone
    restaurant.address = restaurant_data.address

    try:
        await db.commit()

        await notification_service.create_notification(
            db=db,
            user_id=restaurant.owner_id,
            message="Your restaurant details have been updated.",
            notification_type=NotificationType.SYSTEM
        )

        await db.refresh(restaurant)

        return restaurant

    except IntegrityError:

        await db.rollback()

        logger.exception("Database integrity error while updating restaurant")
        raise RestaurantAlreadyExistsError()

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while updating restaurant")
        raise DatabaseError()

async def update_restaurant_status(
        db: AsyncSession,
        restaurant_id: int,
        status: RestaurantStatus,
        current_user: User
    ):
    
    restaurant = await get_restaurant_by_id(
        db,
        restaurant_id
    )

    if (
        current_user.role != UserRole.ADMIN and
        restaurant.owner_id != current_user.id
    ):
        
        logger.warning(
            "Another restaurant owner can't chagne the restaurant status"
        )
        raise PermissionDeniedError()
    
    
    if restaurant.status == status:

        logger.warning(
            "Restaurant already has the requested status"
        )

        raise RestaurantStatusAlreadySetError()
    
    restaurant.status = status

    try:

        await db.commit()

        message = RESTAURANT_STATUS_MESSAGES.get(status)

        if message:

            await notification_service.create_notification(
                db=db,
                user_id=restaurant.owner_id,
                message=message,
                notification_type=NotificationType.SYSTEM
            )

        await db.refresh(restaurant)

        return restaurant

    except Exception:

        await db.rollback()

        logger.exception(
            "Unexpected error while updating restaurant status"
        )
        raise DatabaseError()

    

async def delete_restaurant_by_id(
        db: AsyncSession,
        restaurant_id: int,
        current_user: User,
    ):


    restaurant = await get_restaurant_by_id(
        db,
        restaurant_id,
    )

    if (
        current_user.role != UserRole.ADMIN and
        restaurant.owner_id != current_user.id
    ):
        
        logger.warning(
            "Restaurant deletion denied because the user does not own the restaurant"
        )
        raise PermissionDeniedError()

    deleted_restaurant = restaurant

    try:

        await db.delete(restaurant)

        await db.commit()

        await notification_service.create_notification(
            db=db,
            user_id=restaurant.owner_id,
            message="Your restaurant has been removed.",
            notification_type=NotificationType.SYSTEM
        )

        return deleted_restaurant

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while deleting restaurant")
        raise DatabaseError()
