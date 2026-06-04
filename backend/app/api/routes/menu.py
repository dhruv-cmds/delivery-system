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
        tags=["Menu"],
        dependencies=[Depends(get_current_user)]
    )

public_router = APIRouter(tags=["Menu_Public"])


@router.post(
    "/menus",
    response_model=MenuResponse,
    summary="Create a menu item",
    description=(
        "Create a menu item for a restaurant. Only admins and restaurant owners "
        "can create menu items."
    )
)
@limiter.limit("3/second")
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
    "/menus/{menu_id}",
    response_model=MenuResponse,
    summary="Get a menu item by ID",
    description="Return the details for a specific menu item."
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


@public_router.get(
    "/restaurants/{restaurant_id}/menus",
    response_model=list[MenuResponse],
    summary="List menu items by restaurant",
    description="Return all menu items that belong to the given restaurant."
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


@router.put(
    "/menus/{menu_id}",
    response_model=MenuResponse,
    summary="Update a menu item",
    description=(
        "Update a menu item's details. Only admins and the restaurant owner "
        "can update the item."
    )
)
@limiter.limit("3/second")
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
    "/menus/{menu_id}",
    response_model=MenuResponse,
    summary="Delete a menu item",
    description=(
        "Delete a menu item by ID. Only admins and the restaurant owner can "
        "delete the item."
    )
)
@limiter.limit("3/second")
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
    "/menus/{menu_id}/status",
    response_model=MenuResponse,
    summary="Change a menu item's status",
    description=(
        "Update the availability status for a menu item. Only admins and the "
        "restaurant owner can change the status."
    )
)
@limiter.limit("3/second")
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
