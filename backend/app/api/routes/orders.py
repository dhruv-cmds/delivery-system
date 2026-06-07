from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import (

    MenuResponse,
    OrderItemCreate,
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
    tags=["Orders"]
)

@router.post(
    "/",
    response_model=OrderResponse,
    summary="Create order",
    description="Only current user can make a order"
)
@limiter.limit("3/second")
async def create_order(
        request: Request,
        order_data: OrderCreate,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):

    return await order_service.create_order(
        db,
        order_data,
        current_user
    )

@router.put(
    "/update/{order_id}",
    response_model=OrderResponse,
    summary="Update inforamtion about order",
    description="Update Order filed by order id such as restaurant id total price etc",
)


@router.patch(
    "/status/{order_id}",
    response_model=OrderResponse,
    summary="Update status of order",
    description="Update Order status by order id such as ACTIVE or CLOSE",
)
@limiter.limit("3/second")
async def update_order_status(
        request: Request,
        order_id: int,
        status: OrderStatus,
        current_user = Depends(get_access_manager),
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
    description="Delete Order by order id",
)
@limiter.limit("3/second")
async def delete_order_by_id(
        request: Request,
        order_id: int,
        current_user = Depends(get_access_manager),
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
    summary="Get menu iten for  order",
    description="Get Order by menu item only admin and restaturant owner can access this",
)
@limiter.limit("3/second")
async def get_menu_item_for_order(
        request: Request,
        menu_item_id: int,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_access_manager)
    ):

    return await order_query_service.get_menu_item_for_order(
        db,
        menu_item_id,
    )


@router.get(
    "/all_orders",
    response_model=list[OrderResponse],
    summary="Get all order",
    description="Get all orders visible to the authenticated user.",
)
@limiter.limit("3/second")
async def get_all_orders(
        request: Request,
        current_user = Depends(get_current_user),
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
    description="Return a single order visible to the authenticated user.",
)
@limiter.limit("3/second")
async def get_order_by_id(
        request: Request,
        order_id: int,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await order_query_service.get_order_by_id(
        db,
        order_id,
        current_user
    )
