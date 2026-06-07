from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import (

    MenuResponse,
    OrderCreate,
    OrderResponse,
)

from app.services import order_service, order_query_service

from app.core import limiter, OrderStatus

from app.api import (
    get_db,
    get_current_user,
    get_access_manager,
)

router = APIRouter(
    prefix="/order",
    tags=["ORDERS"]
)

@router.post(
    "/",
    response_model=OrderResponse,
    summary="Create order",
    description="Create a new order for the authenticated user."
)
@limiter.limit("3/second")
async def create_order(
        request: Request,
        order_data: OrderCreate,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):

    return await order_service.create_order(
        db,
        order_data,
        current_user
    )


@router.patch(
    "/status/{order_id}",
    response_model=OrderResponse,
    summary="Update order status",
    description="Update the status of an order."
)
@limiter.limit("3/second")
async def update_order_status(
        request: Request,
        order_id: int,
        status: OrderStatus,
        current_user=Depends(get_access_manager),
        db: AsyncSession = Depends(get_db)
    ):

    return await order_service.update_order_status(
        db,
        order_id,
        status,
        current_user
    )


@router.delete(
    "/delete/{order_id}",
    response_model=OrderResponse,
    summary="Delete order",
    description="Delete an order by ID."
)
@limiter.limit("3/second")
async def delete_order_by_id(
        request: Request,
        order_id: int,
        current_user=Depends(get_access_manager),
        db: AsyncSession = Depends(get_db)
    ):

    return await order_service.delete_order_by_id(
        db,
        order_id,
        current_user
    )


@router.get(
    "/menu_item/{menu_item_id}",
    response_model=MenuResponse,
    summary="Get menu item for order",
    description="Retrieve a menu item by ID for order processing."
)
@limiter.limit("3/second")
async def get_menu_item_for_order(
        request: Request,
        menu_item_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_access_manager)
    ):

    return await order_query_service.get_menu_item_for_order(
        db,
        menu_item_id,
    )


@router.get(
    "/all_orders",
    response_model=list[OrderResponse],
    summary="Get all orders",
    description="Retrieve all orders visible to the authenticated user."
)
@limiter.limit("3/second")
async def get_all_orders(
        request: Request,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await order_query_service.get_all_orders(
        db,
        current_user
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Get order by ID",
    description="Retrieve an order by its ID."
)
@limiter.limit("3/second")
async def get_order_by_id(
        request: Request,
        order_id: int,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await order_query_service.get_order_by_id(
        db,
        order_id,
        current_user
    )
