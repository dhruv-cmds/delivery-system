import json

from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Order, OrderItem, User
from app.schemas import OrderCreate, OrderResponse, MenuResponse
from app.repositories import order_repository

from app.core import (

    UserRole,
    OrderStatus,
    MenuStatus,
    NotificationType,
    MenuNotFoundError,

    MAX_ORDER_TIMES,
    MAX_TRANSFER_LIMIT,

    logger,
    redis_client,

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
    notification_service
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

    menu_item = await order_repository.get_menu_item_for_order(
        db,
        order_data.menu_item_id,
    )

    if not menu_item:

        logger.warning(
            "Menu item not found for order processing (menu_item_id=%s)",
            order_data.menu_item_id
        )

        raise OrderItemNotFoundError("Menu item not found")

    if menu_item.status != MenuStatus.AVAILABLE:

        logger.warning(
            "Menu item unavailable for ordering (menu_item_id=%s)",
            order_data.menu_item_id
        )

        raise InvalidOperationError("Menu item is not available")
    
    logger.info(
        "Menu item retrieved for order processing (menu_item_id=%s)",
        order_data.menu_item_id
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

        new_order = await order_repository.create_order(
            db,
            new_order
        )
            
        await db.commit()

        try:

            await notification_service.create_notification(
                db=db,
                user_id=current_user.id,
                message="Your order has been placed successfully.",
                notification_type=NotificationType.ORDER_UPDATE
            )

            logger.info(
                "Notification created successfully for (order_id=%s, customer_id=%s)",
                new_order.id,
                current_user.id
            )

        except Exception:

            logger.exception(
                "Failed to create notification for order_id=%s",
                new_order.id
            )
                
    except IntegrityError:

        await db.rollback()

        logger.exception("Database integrity error while creating order")

        raise OrderItemNotFoundError()

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while creating order")
        
        raise DatabaseError()

    logger.info(
        "Order created successfully (order_id=%s, customer_id=%s)",
        new_order.id,
        current_user.id,
    )

    return new_order


async def update_order_status(
        db: AsyncSession,
        order_id: int,
        status: OrderStatus,
        current_user: User,
    ):

    order = await order_repository.get_order_by_id(
        db,
        order_id,
        current_user,
    )

    if not order:

        logger.warning(
            "Order not found or access denied (order_id=%s, user_id=%s)",
            order_id,
            current_user.id
        )

        raise OrderNotFoundError()
    

    logger.info(
        "Order retrieved successfully (order_id=%s)",
        order_id
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

        logger.info(
            "Order status updated successfully (order_id=%s, status=%s)",
            order_id,
            status
        )

        cache_key = f"order_id:{order_id}"

        response = OrderResponse.model_validate(

        # schema has from_attributes so you can only use payment 
        # and can use with from_attributes both works
        # use what every you like

            order,
            from_attributes=True
        )

        await redis_client.set(
            cache_key,
            response.model_dump_json(),
            ex=3600  # 1 hour
        )

        return response

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while updating order status")
        raise DatabaseError()


async def delete_order_by_id(
        db: AsyncSession,
        order_id: int,
        current_user: User
    ):

    order = await order_repository.get_order_by_id(
        db,
        order_id,
        current_user,
    )

    if not order:

        logger.warning(
            "Order not found or access denied (order_id=%s, user_id=%s)",
            order_id,
            current_user.id
        )

        raise OrderNotFoundError()
    

    logger.info(
        "Order retrieved successfully (order_id=%s)",
        order_id
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

        await order_repository.delete_order(
            db,
            order
        )

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
    

async def get_all_orders(
        db: AsyncSession,
        current_user: User
    ):

    orders = await order_repository.get_all_orders(
        db,
        current_user
    )
    

    logger.info(
        "All order retrieved successfully for user (user_id=%s)",
        current_user.id
    )

    return orders

async def get_order_by_id (
        db: AsyncSession,
        order_id: int,
        current_user: User
    ):

    order = await order_repository.get_order_by_id(
        db,
        order_id,
        current_user
    )   

    if not order:

        logger.warning(
            "Order not found or access denied (order_id=%s, user_id=%s)",
            order_id,
            current_user.id
        )

        raise OrderNotFoundError()
    
    cache_key = f"order_id:{order_id}"

    cached = await redis_client.get(cache_key)

    if cached:

        logger.info(
            "Order retrived from Redis (order_id=%s)",
            order_id
        )

        return OrderResponse.model_validate_json(cached)
    
    
    response = OrderResponse.model_validate(

        order,
        from_attributes=True
    )

    await redis_client.set(
        cache_key,
        response.model_dump_json(),
        ex=300
    )

    logger.info(
        "Order retrieved successfully (order_id=%s)",
        order_id
    )

    return response

async def get_order_by_menu_id(
        
        db: AsyncSession,
        menu_id: int
    ):

    cache_key = f"menu_id:{menu_id}"

    cached = await redis_client.get(cache_key)

    if cached:

        logger.info(
            "Order retrived from Redis (order_id=%s)",
            menu_id
        )

        return MenuResponse.model_validate_json(cached)
    
    menu = await order_repository.get_menu_item_for_order(
        db,
        menu_id
    )

    if not menu:

        logger.warning(
            "Order not found by menu ID %s",
            menu_id
        )
        raise MenuNotFoundError()
    
    response = MenuResponse.model_validate(

        menu,
        from_attributes=True
    )
    
    await redis_client.set(
        cache_key,
        response.model_dump_json(),
        ex=3600
    )

    return response