from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Order, OrderItem, User
from app.schemas import OrderCreate, OrderItemCreate

from app.core import (
    UserRole,
    OrderStatus,
    NotificationType,

    MAX_ORDER_TIMES,
    MAX_TRANSFER_LIMIT,

    logger,

    DatabaseError,
    EmptyOrderError,
    InvalidOrderStateError,
    OrderAlreadyDeliveredError,
    OrderItemNotFoundError,
    OrderNotFoundError,
    PermissionDeniedError,
    InvalidOperationError,
)

from app.services import (
    get_all_orders,
    get_menu_item_for_order,
    get_order_by_id,
    notification_service,
)


FINAL_ORDER_STATUSES = {
    OrderStatus.DELIVERED,
    OrderStatus.CANCELLED,
}


ORDER_STATUS_MESSAGES = {
    OrderStatus.PENDING: "Your order is pending.",
    OrderStatus.ACCEPTED: "Your order has been accepted.",
    OrderStatus.PREPARING: "Your order is being prepared.",
    OrderStatus.OUT_FOR_DELIVERY: "Your order is out for delivery.",
    OrderStatus.DELIVERED: "Your order has been delivered.",
    OrderStatus.CANCELLED: "Your order has been cancelled.",
    OrderStatus.REPLACE: "Your order has been replaced.",
}


async def create_order(
        db: AsyncSession,
        order_data: OrderCreate,
        current_user: User,
    ):

    if current_user.role != UserRole.CUSTOMER:

        logger.warning(
            "Order creation denied: user ID %s is not a customer",
            current_user.id
        )
        raise PermissionDeniedError()

    if order_data.quantity <= 0:

        logger.warning(
            "Order creation failed: invalid quantity (%s)",
            order_data.quantity
        )
        raise EmptyOrderError("Order item quantity must be greater than zero")

    if order_data.quantity > MAX_ORDER_TIMES:

        logger.warning(
            "Order creation failed: quantity exceeds limit (%s)",
            order_data.quantity
        )
        raise InvalidOperationError()

    menu_item = await get_menu_item_for_order(
        db,
        order_data.menu_item_id,
    )

    item_total = menu_item.price * Decimal(order_data.quantity)

    if item_total > MAX_TRANSFER_LIMIT:

        logger.warning(
            "Order creation failed: total amount exceeds limit (%s)",
            item_total
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

        await db.flush()

        await db.commit()

        try:

            await notification_service.create_notification(
                db=db,
                user_id=current_user.id,
                message="Your order has been placed successfully.",
                notification_type=NotificationType.ORDER_UPDATE
            )

            result = await db.execute(
                select(Order)
                .options(selectinload(Order.order_items))
                .where(Order.id == new_order.id)
            )

            new_order = result.scalar_one()

            await db.refresh(new_order)

            logger.info(
                "Order created successfully (order_id=%s, customer_id=%s)",
                new_order.id,
                current_user.id
            )
        
        except Exception:

            await db.rollback()

            logger.exception(
                "Notification failed"
            )
            
            raise "Notification craetion faield"

        return new_order

    except IntegrityError:

        await db.rollback()

        logger.exception("Database integrity error while creating order")
        raise OrderItemNotFoundError()

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while creating order")
        raise DatabaseError()

async def update_order_status(
        db: AsyncSession,
        order_id: int,
        status: OrderStatus,
        current_user: User,
    ):

    order = await get_order_by_id(
        db,
        order_id,
        current_user,
    )

    if order.status == OrderStatus.DELIVERED:

        logger.warning(
            "Order status update denied: order already delivered (order_id=%s)",
            order_id
        )
        raise OrderAlreadyDeliveredError()

    if order.status == OrderStatus.CANCELLED:

        logger.warning(
            "Order status update denied: order already cancelled (order_id=%s)",
            order_id
        )
        raise InvalidOrderStateError(order.status)

    order.status = status

    message = ORDER_STATUS_MESSAGES.get(status)

    try:

        await db.commit()

        if message:

            await notification_service.create_notification(
                db=db,
                user_id=order.customer_id,
                message=message,
                notification_type=NotificationType.ORDER_UPDATE
            )

        await db.refresh(order)

        logger.info(
            "Order status updated successfully (order_id=%s, status=%s)",
            order_id,
            status
        )

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

    order = await get_order_by_id(
        db,
        order_id,
        current_user,
    )

    if order.status == OrderStatus.DELIVERED:

        logger.warning(
            "Order deletion denied: order already delivered (order_id=%s)",
            order_id
        )
        raise OrderAlreadyDeliveredError()

    if order.status in FINAL_ORDER_STATUSES:

        logger.warning(
            "Order deletion denied: order is in a final state (order_id=%s, status=%s)",
            order_id,
            order.status
        )
        raise InvalidOrderStateError(order.status)

    deleted_order = order

    try:

        await db.delete(order)

        await db.commit()

        logger.info(
            "Order deleted successfully (order_id=%s)",
            order_id
        )

        return deleted_order

    except IntegrityError:

        await db.rollback()

        logger.exception("Database integrity error while deleting order")
        raise OrderNotFoundError()

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while deleting order")
        raise DatabaseError()