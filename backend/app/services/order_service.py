from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Order, OrderItem, User

from app.schemas import OrderCreate, OrderItemCreate

from app.core import (

    UserRole,

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
    OrderStatus.DELIVERED.value,
    OrderStatus.CANCELLED.value,
}


async def create_order(
        db: AsyncSession,
        order_data: OrderCreate,
        current_user: User,
    ):

    if current_user.role != UserRole.CUSTOMER.value:

        logger.warning("Non-customer attempted to create order")
        raise PermissionDeniedError()

    if order_data.quantity <= 0:

        logger.warning("Order attempted with non-positive quantity")
        raise EmptyOrderError("Order item quantity must be greater than zero")
    
    if order_data.quantity > 20:

        logger.warning(
            f"Max order item limit exicuted"
            f"You can make 20 orders at the same time"
        )

        raise InvalidOperationError()
    

    menu_item = await get_menu_item_for_order(
        db,
        order_data.menu_item_id,
    )

    item_total = menu_item.price * Decimal(order_data.quantity)

    if item_total > 50000:

        logger.warning(
            f"Max transer limit exicuted."
            f"You Cannot make order that price is more the 50000"
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

        logger.exception("Integrity error while creating order")
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

    if current_user.role == UserRole.DELIVERY_PARTNER.value:

        logger.warning("Delivery partner attempted to update order item")
        raise PermissionDeniedError()

    order = await get_order_by_id(
        db,
        order_id,
        current_user,
    )

    if order.status == OrderStatus.DELIVERED.value:

        logger.warning("Delivered order update attempted")
        raise OrderAlreadyDeliveredError()

    if order.status in FINAL_ORDER_STATUSES:

        logger.warning("Final order update attempted")
        raise InvalidOrderStateError(order.status)

    if order_data.quantity <= 0:

        logger.warning("Order update attempted with non-positive quantity")
        raise EmptyOrderError("Order item quantity must be greater than zero")

    menu_item = await get_menu_item_for_order(
        db,
        order_data.menu_item_id,
    )

    order_item = order.order_items[0] if order.order_items else None

    if not order_item:

        logger.warning("Order item not found while updating order")
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

        logger.exception("Integrity error while updating order")
        raise OrderItemNotFoundError()

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while updating order")
        raise DatabaseError()
    

async def update_order_status(
        db: AsyncSession,
        order_id: int,
        status: str,
        current_user: User,
    ):

    if current_user.role == UserRole.CUSTOMER.value:

        logger.warning("Customer attempted to update order status")
        raise PermissionDeniedError()

    order = await get_order_by_id(
        db,
        order_id,
        current_user,
    )

    if order.status == OrderStatus.DELIVERED.value:

        logger.warning("Delivered order status update attempted")
        raise OrderAlreadyDeliveredError()

    if order.status == OrderStatus.CANCELLED.value:

        logger.warning("Cancelled order status update attempted")
        raise InvalidOrderStateError(order.status)

    valid_statuses = {order_status.value for order_status in OrderStatus}

    if status not in valid_statuses:

        logger.warning("Invalid order status update attempted")
        raise InvalidOrderStateError(status)

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

    if current_user.role == UserRole.DELIVERY_PARTNER.value:

        logger.warning("Delivery partner attempted to delete order")
        raise PermissionDeniedError()

    order = await get_order_by_id(
        db,
        order_id,
        current_user,
    )

    if order.status == OrderStatus.DELIVERED.value:

        logger.warning("Delivered order delete attempted")
        raise OrderAlreadyDeliveredError()

    if order.status in FINAL_ORDER_STATUSES:

        logger.warning("Final order delete attempted")
        raise InvalidOrderStateError(order.status)

    try:

        await db.delete(order)

        await db.commit()

        return True
    
    except IntegrityError:

        await db.rollback()

        logger.exception("Integrity error while deleting order")
        raise OrderNotFoundError()

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while deleting order")
        raise DatabaseError()
