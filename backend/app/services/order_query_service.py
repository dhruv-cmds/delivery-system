from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Menu, Order, User

from app.core import (
    logger,
    InvalidOperationError,
    OrderItemNotFoundError,
    OrderNotFoundError,
)


async def get_menu_item_for_order(
        db: AsyncSession,
        menu_item_id: int,
    ):

    result = await db.execute(
        select(Menu)
        .where(Menu.id == menu_item_id)
    )

    menu_item = result.scalar_one_or_none()

    if not menu_item:

        logger.warning("Menu item not found while processing order")
        raise OrderItemNotFoundError("Menu item not found")

    if menu_item.status != "AVAILABLE":

        logger.warning("Unavailable menu item used while processing order")
        raise InvalidOperationError("Menu item is not available")

    return menu_item


async def get_all_orders(
        db: AsyncSession,
        current_user: User
    ):

    statement = (
        select(Order)
        .options(selectinload(Order.order_items))
        .order_by(Order.created_at.desc())
    )

    if current_user:

        statement = statement.where(Order.customer_id == current_user.id)

    result = await db.execute(statement)

    return list(result.scalars().all())


async def get_order_by_id(
        db: AsyncSession,
        order_id: int,
        current_user: User
    ):

    statement = (
        select(Order)
        .options(selectinload(Order.order_items))
        .where(Order.id == order_id)
    )

    if current_user:

        statement = statement.where(Order.customer_id == current_user.id)

    order_result = await db.execute(statement)

    order = order_result.scalar_one_or_none()

    if not order:

        logger.warning("Order not found")
        raise OrderNotFoundError()
    
    return order
