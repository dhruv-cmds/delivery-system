from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Restaurant, User
from app.schemas import RestaurantCreate

from app.core import (
    logger,
    DatabaseError,
    RestaurantNotFoundError,
    RestaurantAlreadyExistsError,
    PermissionDeniedError,
)


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

        await db.commit()

        await db.refresh(new_restaurant)

        return new_restaurant

    except IntegrityError:

        await db.rollback()

        logger.exception("Integrity error while creating restaurant")
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
        logger.warning("Restaurant not found")
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

    if restaurant.owner_id != current_user.id:

        logger.warning(
            "User attempted to update restaurant they do not own"
        )
        raise PermissionDeniedError()

    restaurant.name = restaurant_data.name
    restaurant.phone = restaurant_data.phone
    restaurant.address = restaurant_data.address

    try:
        await db.commit()

        await db.refresh(restaurant)

        return restaurant

    except IntegrityError:

        await db.rollback()

        logger.exception("Integrity error while updating restaurant")
        raise RestaurantAlreadyExistsError()

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while updating restaurant")
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

    if restaurant.owner_id != current_user.id:

        logger.warning(
            "User attempted to delete restaurant they do not own"
        )
        raise PermissionDeniedError()

    try:

        await db.delete(restaurant)

        await db.commit()

        return True

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while deleting restaurant")
        raise DatabaseError()