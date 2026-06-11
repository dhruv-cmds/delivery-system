from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Menu, Restaurant


async def get_restaurant_by_id(
    db: AsyncSession,
    restaurant_id: int
):
    result = await db.execute(
        select(Restaurant).where(
            Restaurant.id == restaurant_id
        )
    )

    return result.scalar_one_or_none()


async def get_menu_by_id(
    db: AsyncSession,
    menu_id: int
):
    result = await db.execute(
        select(Menu).where(
            Menu.id == menu_id
        )
    )

    return result.scalar_one_or_none()


async def get_menu_by_name(
    db: AsyncSession,
    restaurant_id: int,
    item_name: str
):
    result = await db.execute(
        select(Menu).where(
            and_(
                Menu.restaurant_id == restaurant_id,
                Menu.item_name == item_name
            )
        )
    )

    return result.scalar_one_or_none()


async def get_menu_by_restaurant_id(
    db: AsyncSession,
    restaurant_id: int
):
    result = await db.execute(
        select(Menu).where(
            Menu.restaurant_id == restaurant_id
        )
    )

    return result.scalars().all()