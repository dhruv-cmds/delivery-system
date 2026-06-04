from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Order, OrderItem, User

from app.schemas import OrderCreate, OrderItemCreate


from app.core import (

    UserRole,
    OrderStatus,

    MAX_ORDER_TIMES,
    MAX_TRANSFER_LIMIT,

    logger,
    
    DatabaseError,
    EmptyOrderError,
    InvalidOrderStateError,
    OrderAlreadyDeliveredError,
    OrderItemNotFoundError,
    OrderNotFoundError,
    OrderStatus,
    PermissionDeniedError,
    InvalidOperationError
)

from app.services.order_query_service import (
    get_all_orders,
    get_menu_item_for_order,
    get_order_by_id,
)


FINAL_ORDER_STATUSES = {
    OrderStatus.DELIVERED,
    OrderStatus.CANCELLED,
}


async def create_order(
        db: AsyncSession,
        order_data: OrderCreate,
        current_user: User,
    ):

    if current_user.role != UserRole.CUSTOMER:

        logger.warning(
            "Order creation denied because the user is not a customer"
        )
        raise PermissionDeniedError()

    if order_data.quantity <= 0:

        logger.warning(
            "Order creation failed because the quantity was not positive"
        )
        raise EmptyOrderError("Order item quantity must be greater than zero")
    
    if order_data.quantity > MAX_ORDER_TIMES:

        logger.warning(
            "Order creation failed because the quantity is above the allowed limit"
        )

        raise InvalidOperationError()
    

    menu_item = await get_menu_item_for_order(
        db,
        order_data.menu_item_id,
    )

    item_total = menu_item.price * Decimal(order_data.quantity)

    if item_total > MAX_TRANSFER_LIMIT:

        logger.warning(
            "Order creation failed because the total price is above the transfer limit"
        )

        raise InvalidOperationError()

    new_order = Order(
        customer_id=current_user.id,
        restaurant_id=menu_item.restaurant_id,
        total_price=item_total,
        delivery_address=order_data.delivery_address,
    )

    new_order_item = OrderItem(
        menu_item_id=menu_item.id,
        quantity=order_data.quantity,
        unit_price=menu_item.price,
        total_price=item_total,
    )

    new_order.order_items.append(new_order_item)

    try:

        db.add(new_order)

        await db.commit()

        await db.refresh(new_order)

        return new_order
    
    except IntegrityError:

        await db.rollback()

        logger.exception("Database integrity error while creating order")
        raise OrderItemNotFoundError()

    except Exception:
        
        await db.rollback()

        logger.exception("Unexpected error while creating order")
        raise DatabaseError()


async def update_order_by_id(
        db: AsyncSession,
        order_id: int,
        order_data: OrderItemCreate,
        current_user: User,
    ):

    if current_user.role == UserRole.DELIVERY_PARTNER:

        logger.warning(
            "Order item update denied because delivery partners cannot update order items"
        )
        raise PermissionDeniedError()

    order = await get_order_by_id(
        db,
        order_id,
        current_user,
    )

    if order.status == OrderStatus.DELIVERED:

        logger.warning(
            "Order item update denied because the order is already delivered"
        )
        raise OrderAlreadyDeliveredError()

    if order.status in FINAL_ORDER_STATUSES:

        logger.warning(
            "Order item update denied because the order is in a final state"
        )
        raise InvalidOrderStateError(order.status)

    if order_data.quantity <= 0:

        logger.warning(
            "Order item update failed because the quantity was not positive"
        )
        raise EmptyOrderError("Order item quantity must be greater than zero")

    menu_item = await get_menu_item_for_order(
        db,
        order_data.menu_item_id,
    )

    order_item = order.order_items[0] if order.order_items else None

    if not order_item:

        logger.warning(
            "Order item update failed because the order item was not found"
        )
        raise OrderItemNotFoundError()

    item_total = menu_item.price * Decimal(order_data.quantity)

    order.restaurant_id = menu_item.restaurant_id
    order.total_price = item_total
    order_item.menu_item_id = menu_item.id
    order_item.quantity = order_data.quantity
    order_item.unit_price = menu_item.price
    order_item.total_price = item_total

    try:

        await db.commit()

        await db.refresh(order)

        return order

    except IntegrityError:

        await db.rollback()

        logger.exception("Database integrity error while updating order")
        raise OrderItemNotFoundError()

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while updating order")
        raise DatabaseError()
    

async def update_order_status(
        db: AsyncSession,
        order_id: int,
        status: OrderStatus,
        current_user: User,
    ):

    if current_user.role == UserRole.CUSTOMER:

        logger.warning(
            "Order status update denied because customers cannot update order status"
        )
        raise PermissionDeniedError()

    order = await get_order_by_id(
        db,
        order_id,
        current_user,
    )

    if order.status == OrderStatus.DELIVERED:

        logger.warning(
            "Order status update denied because the order is already delivered"
        )
        raise OrderAlreadyDeliveredError()

    if order.status == OrderStatus.CANCELLED:

        logger.warning(
            "Order status update denied because the order is already cancelled"
        )
        raise InvalidOrderStateError(order.status)

    order.status = status

    try:

        await db.commit()

        await db.refresh(order)

        return order

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while updating order status")
        raise DatabaseError()


async def delete_order_by_id(
        db: AsyncSession,
        order_id: int,
        current_user: User
    ):

    if current_user.role == UserRole.DELIVERY_PARTNER:

        logger.warning(
            "Order deletion denied because delivery partners cannot delete orders"
        )
        raise PermissionDeniedError()

    order = await get_order_by_id(
        db,
        order_id,
        current_user,
    )

    if order.status == OrderStatus.DELIVERED:

        logger.warning(
            "Order deletion denied because the order is already delivered"
        )
        raise OrderAlreadyDeliveredError()

    if order.status in FINAL_ORDER_STATUSES:

        logger.warning(
            "Order deletion denied because the order is in a final state"
        )
        raise InvalidOrderStateError(order.status)

    try:

        await db.delete(order)

        await db.commit()

        return True
    
    except IntegrityError:

        await db.rollback()

        logger.exception("Database integrity error while deleting order")
        raise OrderNotFoundError()

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while deleting order")
        raise DatabaseError()
