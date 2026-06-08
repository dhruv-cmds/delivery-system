from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import MenuStatus, limiter

from app.schemas import MenuResponse, MenuCreate
from app.services import menu_service

from app.api import get_db
from app.api import (
    get_current_user,
    get_access_manager,
)

router = APIRouter(
        prefix="/meuns",
        tags=["MENU"],
        dependencies=[Depends(get_current_user)]
    )

public_router = APIRouter(tags=["PUBLIC MENU"])


@router.post(
    "/",
    response_model=MenuResponse,
    summary="Create a menu item",
    description=(
        "Create a new menu item for a restaurant. "
        "Accessible to administrators and restaurant owners."
    )
)
@limiter.limit("20/minute")
async def create_menu_item(
    request: Request,
    menu: MenuCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_access_manager)
):
    return await menu_service.create_menu_item(
        db,
        menu,
        current_user
    )


@public_router.get(
    "/{menu_id}",
    response_model=MenuResponse,
    summary="Get menu item by ID",
    description="Retrieve a menu item by its unique ID."
)
@limiter.limit("120/minute")
async def get_menu_item_by_id(
        request: Request,
        menu_id: int,
        db: AsyncSession = Depends(get_db),
    ):

    return await menu_service.get_menu_item_by_id(
        db,
        menu_id
    )


@public_router.get(
    "/restaurants/{restaurant_id}/menus",
    response_model=list[MenuResponse],
    summary="Get restaurant menu items",
    description="Retrieve all menu items for a specific restaurant."
)
@limiter.limit("120/minute")
async def get_menu_items_by_restaurant_id(
        request: Request,
        restaurant_id: int,
        db: AsyncSession = Depends(get_db),
    ):

    return await menu_service.get_menu_items_by_restaurant_id(
        db,
        restaurant_id,
    )


@router.put(
    "/{menu_id}",
    response_model=MenuResponse,
    summary="Update a menu item",
    description=(
        "Update menu item details. "
        "Accessible to administrators and the restaurant owner."
    )
)
@limiter.limit("30/minute")
async def update_menu_item(
        request: Request,
        menu_data: MenuCreate,
        menu_id: int,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_access_manager)
    ):

    return await menu_service.update_menu_item(
        db,
        menu_data,
        menu_id,
        current_user
    )


@router.delete(
    "/{menu_id}",
    response_model=MenuResponse,
    summary="Delete a menu item",
    description=(
        "Delete a menu item by ID. "
        "Accessible to administrators and the restaurant owner."
    )
)
@limiter.limit("20/minute")
async def delete_menu_item(
        request: Request,
        menu_id: int,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_access_manager)
    ):

    return await menu_service.delete_menu_item(
        db,
        menu_id,
        current_user
    )


@router.patch(
    "/{menu_id}/status",
    response_model=MenuResponse,
    summary="Update menu item status",
    description=(
        "Update the availability status of a menu item. "
        "Accessible to administrators and the restaurant owner."
    )
)
@limiter.limit("30/minute")
async def change_menu_status(
        request: Request,
        menu_id: int,
        status: MenuStatus,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_access_manager)
    ):

    return await menu_service.change_menu_status(
        db,
        menu_id,
        status,
        current_user
    )
