from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Restaurant, User
from app.schemas import RestaurantCreate, RestaurantResponse
from app.services import notification_service
from app.repositories import restaurant_repository

from app.core import (

    logger,
    redis_client,

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
        
        if current_user.role == UserRole.CUSTOMER:
            current_user.role = UserRole.RESTAURANT_OWNER

        new_restaurant = await restaurant_repository.persist_restaurant(
            db,
            new_restaurant,
        )

        await notification_service.create_notification(

            db=db,
            user_id=current_user.id,
            message="Your restaurant has been created successfully.",
            notification_type=NotificationType.SYSTEM
        )

        await db.commit()

        logger.info(
            "Restaurant created successfully (restaurant_id=%s, owner_id=%s)",
            new_restaurant.id,
            current_user.id
        )

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

    cache_key = f"restaurant_id:{restaurant_id}"

    cached = await redis_client.get(cache_key)

    if cached:

        logger.info(
            "Restaurant retrieved from Redis (restaurant_id=%s)",
            restaurant_id
        )

        return RestaurantResponse.model_validate_json(cached)

    restaurant = await restaurant_repository.get_restaurant_by_id(
        db,
        restaurant_id
    )

    if not restaurant:

        logger.warning(
            "Restaurant not found (restaurant_id=%s)",
            restaurant_id
        )
        raise RestaurantNotFoundError()
    
    response = RestaurantResponse.model_validate(
        restaurant,
        from_attributes=True
    )

    await redis_client.set(
        cache_key,
        response.model_dump_json(),
        ex=3600, # 1 hour
    )

    return response


async def update_restaurant(
        db: AsyncSession,
        restaurant_id: int,
        restaurant_data: RestaurantCreate,
        current_user: User,
    ):

    restaurant = await restaurant_repository.get_restaurant_by_id(
        db,
        restaurant_id,
    )

    if not restaurant:

        logger.warning(
            "Restaurant not found (restaurant_id=%s)",
            restaurant_id,
        )

        raise RestaurantNotFoundError()

    if (
        current_user.role != UserRole.ADMIN and
        restaurant.owner_id != current_user.id
    ):
        
        logger.warning(
            "Restaurant update denied: user ID %s is not the owner",
            current_user.id
        )
        raise PermissionDeniedError()

    restaurant.name = restaurant_data.name
    restaurant.phone = restaurant_data.phone
    restaurant.address = restaurant_data.address

    cache_key = f"restaurant_id:{restaurant_id}"

    try:

        restaurant = await restaurant_repository.persist_restaurant(
            db,
            restaurant,
        )

        await notification_service.create_notification(
            db=db,
            user_id=restaurant.owner_id,
            message="Your restaurant details have been updated.",
            notification_type=NotificationType.SYSTEM
        )

        await db.commit()

        response = RestaurantResponse.model_validate(

        # schema has from_attributes so you can only use payment 
        # and can use with from_attributes both works
        # use what every you like

            restaurant,
            from_attributes=True
        )

        await redis_client.set(
            cache_key,
            response.model_dump_json(),
            ex=3600 
        )

        logger.info(
            "Restaurant updated successfully (restaurant_id=%s)",
            restaurant.id
        )

        return response

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
    
    restaurant = await restaurant_repository.get_restaurant_by_id(
        db,
        restaurant_id
    )

    if not restaurant:

        logger.warning(
            "Restaurant not found (restaurant_id=%s)",
            restaurant_id,
        )

        raise RestaurantNotFoundError()

    if (
        current_user.role != UserRole.ADMIN and
        restaurant.owner_id != current_user.id
    ):
        
        logger.warning(
            "Restaurant status update denied: user ID %s is not the owner",
            current_user.id
        )
        raise PermissionDeniedError()
    
    
    if restaurant.status == status:

        logger.warning(
            "Restaurant already has status '%s' (restaurant_id=%s)",
            status,
            restaurant_id
        )

        raise RestaurantStatusAlreadySetError()
    
    restaurant.status = status

    cache_key = f"restaunrat_id:{restaurant_id}"

    try:

        restaurant = await restaurant_repository.persist_restaurant(
            db,
            restaurant,
        )

        message = RESTAURANT_STATUS_MESSAGES.get(status)

        if message:

            await notification_service.create_notification(
                db=db,
                user_id=restaurant.owner_id,
                message=message,
                notification_type=NotificationType.SYSTEM
            )

        await db.commit()

        response = RestaurantResponse.model_validate(
            restaurant,
            from_attributes=True
        )

        await redis_client.set(
            cache_key,
            response.model_dump_json(),
            ex=3600
        )

        logger.info(
            "Restaurant status updated successfully "
            "(restaurant_id=%s, status=%s)",
            restaurant.id,
            status,
        )

        return response

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


    restaurant = await restaurant_repository.get_restaurant_by_id(
        db,
        restaurant_id,
    )

    if not restaurant:

        logger.warning(
            "Restaurant not found (restaurant_id=%s)",
            restaurant_id,
        )

        raise RestaurantNotFoundError()

    if (
        current_user.role != UserRole.ADMIN and
        restaurant.owner_id != current_user.id
    ):
        
        logger.warning(
            "Restaurant deletion denied: user ID %s is not the owner",
            current_user.id
        )
        raise PermissionDeniedError()

    deleted_restaurant = restaurant

    try:

        await restaurant_repository.delete_restaurant(
            db,
            restaurant,
        )

        await notification_service.create_notification(
            db=db,
            user_id=restaurant.owner_id,
            message="Your restaurant has been removed.",
            notification_type=NotificationType.SYSTEM
        )

        await db.commit()

        logger.info(
            "Restaurant deleted successfully (restaurant_id=%s)",
            restaurant_id
        )

        return deleted_restaurant

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while deleting restaurant")
        
        raise DatabaseError()
    
    
# Cache flow:
#
# 1. GET /restaurants/{id}
#    - First checks Redis.
#    - If cache exists, return RestaurantResponse from Redis.
#    - If cache does not exist, fetch from DB and store in Redis.
#
# 2. PUT/PATCH /restaurants/{id}
#    - Update restaurant in DB.
#    - Update (or invalidate) Redis cache for the same restaurant_id.
#
# Why?
# A future GET request may read from Redis instead of the database.
# If we don't refresh the cache after an update, users could receive
# stale/outdated restaurant data even though the database was updated.
#
# Example:
# GET -> cache stores "Pizza House"
# UPDATE -> DB changes name to "Pizza Palace"
# UPDATE -> cache also changes to "Pizza Palace"
# GET -> returns fresh cached data ("Pizza Palace")
# 
# Inshort:
# User gets RestaurantResponse from cache if available.
# If restaurant data is changed by another endpoint,
# we refresh the cache here so the next GET request
# receives the updated restaurant information.