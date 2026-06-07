from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import limiter, RestaurantStatus

from app.api import (

    get_db,
    get_current_user,
    get_access_manager,
    require_restaurant_access
)

from app.services import restaurant_service

from app.schemas import RestaurantCreate, RestaurantResponse 


router = APIRouter(
    prefix="/restaurant",
    tags=["RESTAURANT"]
)

public_router = APIRouter(
    prefix="/restaurant",
    tags=["PUBLIC RESTAURANT"]
)

@router.post(
    "/",
    response_model=RestaurantResponse,
    summary="Create a restaurant owner",
    description="Restaurant owner create only admin and current user can create resaurant owner"
)
@limiter.limit("3/second")
async def create_restaurant(
        request: Request,
        restaurant: RestaurantCreate,
        current_user = Depends(require_restaurant_access),
        db: AsyncSession = Depends(get_db)
    ):

    return await restaurant_service.create_restaurant(
        db,
        restaurant,
        current_user
    )


@public_router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
    summary="Get a restaurant by resaurant id",
    description="Any one can get restaurant by restaurant id"
)
@limiter.limit("3/second")
async def get_restaurant_by_id(
        request: Request,
        restaurant_id: int,
        db: AsyncSession = Depends(get_db)
    ):

    return await restaurant_service.get_restaurant_by_id(
        db,
        restaurant_id,
    )


@router.put(
    "/update/{restaurant_id}",
    response_model=RestaurantResponse,
    summary="Update restaurant by resaurant id",
    description="Only restaurant owner and admin can change the restaurant by restaurant id"
)
@limiter.limit("3/second")
async def update_restaurant(
        request: Request,
        restaurant_id: int,
        restaurant_data: RestaurantCreate,
        current_user = Depends(get_access_manager),
        db: AsyncSession = Depends(get_db)
    ):

    return await restaurant_service.update_restaurant(
        db,
        restaurant_id,
        restaurant_data,
        current_user
    )


@router.patch(
    "/status/{restaurant_id}",
    response_model=RestaurantResponse,
    summary="Update restaurant status by resaurant id",
    description="Only restaurant owner and admin can change the restaurant status restaurant id"
)
@limiter.limit("3/second")
async def update_restaurant_status(
        request: Request,
        restaurant_id: int,
        status: RestaurantStatus,
        current_user = Depends(get_access_manager),
        db: AsyncSession = Depends(get_db)
    ):

    return await restaurant_service.update_restaurant_status(
        db,
        restaurant_id,
        status,
        current_user
    )


@router.delete(
    "/delete/{restaurant_id}",
    response_model=RestaurantResponse,
    summary="Delete restaurant by resaurant id",
    description="Only restaurant owner and admin can delete the restaurant restaurant id"
)
@limiter.limit("3/second")
async def delete_restaurant_by_id(
        request: Request,
        restaurant_id: int,
        current_user = Depends(get_access_manager),
        db: AsyncSession = Depends(get_db)
    ):

    return await restaurant_service.delete_restaurant_by_id(
        db,
        restaurant_id,
        current_user
    )

