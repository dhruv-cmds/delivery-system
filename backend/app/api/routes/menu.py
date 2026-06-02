from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import limiter 

from app.schemas import MenuResponse, MenuCreate
from app.services import menu_service

from app.api import get_db
from app.api import (
    get_current_user,
    get_menu_manager,
    get_admin
)

router = APIRouter(
        tags=["Menu"],
        dependencies=[Depends(get_current_user)]
    )


@router.post(
    "/create_menu",
    response_model=MenuResponse,
    summary="Create a menu for restaurant",
    description="Menu that provice list of time that restaurant has"
)
@limiter.limit("3/second")
async def create_menu_item(
    request: Request,
    menu: MenuCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_menu_manager)
):
    return await menu_service.create_menu_item(
        db,
        menu,
        current_user
    )



@router.get(
    "/id/{menu_id}",
    response_model=MenuResponse,
    summary="Get menu item by id",
    description="Recive a detail of a specifi menu item"
)
@limiter.limit("3/second")
async def get_menu_item_by_id(
        request: Request,
        menu_id: int,
        db: AsyncSession = Depends(get_db),
    ):

    return await menu_service.get_menu_item_by_id(
        db,
        menu_id
    )


@router.get(
    "/id/{restaurant_id}",
    response_model=list[MenuResponse],
    summary="Get menu item by id",
    description="Recive a detail of menu items by restaurant id"
)
@limiter.limit("3/second")
async def get_menu_items_by_restaurant_id(
        request: Request,
        restaurant_id: int,
        db: AsyncSession = Depends(get_db),
    ):

    return await menu_service.get_menu_items_by_restaurant_id(
        db,
        restaurant_id,
    )


@router.post(
    "/update_menu/{menu_id}",
    response_model=MenuResponse,
    summary="Update menu item by id",
    description="Update a details of menu items by menu id"
)
@limiter.limit("3/second")
async def update_menu_item(
        request: Request,
        menu_data: MenuCreate,
        menu_id: int,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_menu_manager)
    ):

    return await menu_service.update_menu_item(
        db,
        menu_data,
        menu_id,
        current_user
    )


@router.delete(
    "/delete_menu/{menu_id}",
    response_model=MenuResponse,
    summary="Delete menu item by id",
    description="Delete a menu by menu id"
)
@limiter.limit("3/second")
async def delete_menu_item(
        request: Request,
        menu_id: int,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_menu_manager)
    ):

    return await menu_service.delete_menu_item(
        db,
        menu_id,
        current_user
    )


@router.post(
    "/change_status/{menu_id}",
    response_model=MenuResponse,
    summary="Change menu status by id",
    description="Change a menu status by menu id"
)
@limiter.limit("3/second")
async def change_menu_status(
        request: Request,
        menu_id: int,
        status: str,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_menu_manager)
    ):

    return await menu_service.change_menu_status(
        db,
        menu_id,
        status,
        current_user
    )
