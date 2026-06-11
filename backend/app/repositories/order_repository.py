from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import (

    DeliveryPartner, 
    Menu, 
    Order, 
    Restaurant, 
    User
)

from app.core import (

    UserRole,
)


def apply_order_visibility(statement, current_user: User):

    if current_user.role == UserRole.ADMIN:

        return statement

    if current_user.role == UserRole.CUSTOMER:

        return statement.where(
            Order.customer_id == current_user.id
        )

    if current_user.role == UserRole.DELIVERY_PARTNER:

        delivery_partner_ids = (
            select(DeliveryPartner.id)
            .where(DeliveryPartner.user_id == current_user.id)
        )

        return statement.where(
            Order.delivery_partner_id.in_(delivery_partner_ids)
        )

    if current_user.role == UserRole.RESTAURANT_OWNER:

        restaurant_ids = (
            select(Restaurant.id)
            .where(Restaurant.owner_id == current_user.id)
        )

        return statement.where(
            Order.restaurant_id.in_(restaurant_ids)
        )

    return statement.where(false())


async def get_order_by_id(
        db: AsyncSession,
        order_id: int,
        current_user: User
    ):

    statement = (
        select(Order)
        .options(
            selectinload(Order.order_items),
            selectinload(Order.restaurant),
        )
        .where(Order.id == order_id)
    )

    statement = apply_order_visibility(statement, current_user)

    order_result = await db.execute(statement)

    order = order_result.scalar_one_or_none()
    
    return order


async def get_menu_item_for_order(
        db: AsyncSession,
        menu_item_id: int,
    ):

    result = await db.execute(
        select(Menu)
        .where(Menu.id == menu_item_id)
    )

    return result.scalar_one_or_none()


async def create_order(
        db: AsyncSession,
        order: Order,
    ):

    db.add(order)

    await db.flush()

    result = await db.execute(
        select(Order)
        .options(selectinload(Order.order_items))
        .where(Order.id == order.id)
    )

    return result.scalar_one()

async def delete_order(
        db: AsyncSession,
        order: Order,
    ):
    
    await db.delete(order)


async def get_all_orders(
        db: AsyncSession,
        current_user: User
    ):

    statement = (
        select(Order)
        .options(
            selectinload(Order.order_items),
            selectinload(Order.restaurant),
        )
        .order_by(Order.created_at.desc())
    )

    statement = apply_order_visibility(statement, current_user)

    result = await db.execute(statement)
    
    return list(result.scalars().all())
