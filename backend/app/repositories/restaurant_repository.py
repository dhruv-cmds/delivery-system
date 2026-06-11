from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Restaurant


async def persist_restaurant(
        db: AsyncSession,
        restaurant: Restaurant,
    ):

    if restaurant.id is None:
        db.add(restaurant)

    await db.flush()

    return restaurant


async def get_restaurant_by_id(
    db: AsyncSession,
    restaurant_id: int,
):
    result = await db.execute(
        select(Restaurant)
        .where(Restaurant.id == restaurant_id)
    )

    return result.scalar_one_or_none()


async def delete_restaurant(
    db: AsyncSession,
    restaurant: Restaurant,
):
    await db.delete(restaurant)
