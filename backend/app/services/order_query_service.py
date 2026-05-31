from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import DeliveryPartner, Menu, Order, User

from app.core import (

    UserRole,
    
    logger,
    InvalidOperationError,
    OrderItemNotFoundError,
    OrderNotFoundError,
)


def apply_order_visibility(statement, current_user: User):

    if current_user.role == UserRole.ADMIN.value:

        return statement

    if current_user.role == UserRole.CUSTOMER.value:

        return statement.where(
            Order.customer_id == current_user.id
        )

    if current_user.role == UserRole.DELIVERY_PARTNER.value:

        delivery_partner_ids = (
            select(DeliveryPartner.id)
            .where(DeliveryPartner.user_id == current_user.id)
        )

        return statement.where(
            Order.delivery_partner_id.in_(delivery_partner_ids)
        )

    return statement.where(false())


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

    statement = apply_order_visibility(statement, current_user)

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

    statement = apply_order_visibility(statement, current_user)

    order_result = await db.execute(statement)

    order = order_result.scalar_one_or_none()

    if not order:

        logger.warning("Order not found")
        raise OrderNotFoundError()
    
    return order
