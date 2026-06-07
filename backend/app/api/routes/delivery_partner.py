from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import VehicleTypeStatus, limiter

from decimal import Decimal

from app.schemas import DeliveryPartnerCreate, DeliveryPartnerResponse
from app.services import delivery_partner_service

from app.api import get_db
from app.api import (
    get_current_user,
    require_admin_access,
    get_access_manager
)

router = APIRouter(
    prefix="/delivery_partner",
    tags=["DELIVERY PARTNER"]
)

public_router = APIRouter(
    prefix="/delivery_partner",
    tags=["DELIVERY PARTNER PUBLIC"]
)

@router.post(
    "/",
    response_model=DeliveryPartnerResponse,
    summary="Create a delivery partner",
    description="Create a delivery partner only authorised user and admin can access it"
)   
@limiter.limit("3/second")
async def create_delivery_partner(
        request: Request,
        data: DeliveryPartnerCreate,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await delivery_partner_service.create_delivery_partner(
        db,
        data,
        current_user
    )

@router.get(
    "/user/{user_id}",
    response_model=DeliveryPartnerResponse,
    summary="Get delivery partner by user id",
    description="Only admin can access this routes"
)
@limiter.limit("3/second")
async def get_delivery_partner_by_user_id(
        request: Request,
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_access_manager)
    ):

    return await delivery_partner_service.get_delivery_partner_by_user_id(
        db,
        user_id
    )


@public_router.get(
    "/id/{partner_id}",
    response_model=DeliveryPartnerResponse,
    summary="Get delivery partner by delivery partner id",
    description="Any buddy can access this routes"
)
@limiter.limit("3/second")
async def get_delivery_partner_by_id(
        request: Request,
        partner_id: int,
        db: AsyncSession = Depends(get_db),
    ):

    return await delivery_partner_service.get_delivery_partner_by_id(
        db,
        partner_id
    )


@router.get(
    "/all",
    response_model=list[DeliveryPartnerResponse],
    summary="Get all the delivery partners",
    description="Only admin can get all delivery partners"
)
@limiter.limit("3/second")
async def get_all_delivery_partners(
        request: Request,
        current_user = Depends(require_admin_access),
        db: AsyncSession = Depends(get_db)
    ):

    return await delivery_partner_service.get_all_delivery_partners(
        db
    )


@router.put(
    "/{partner_id}",
    response_model=DeliveryPartnerResponse,
    summary="Update delivery partners vehical",
    description="Only admin and delivery partner can Update vehical"
)
@limiter.limit("3/second")
async def update_delivery_partner(
        request: Request,
        partner_id: int,
        data: VehicleTypeStatus,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await delivery_partner_service.update_delivery_partner(
        db,
        partner_id,
        data,
        current_user
    )


@router.put(
    "/{partner_id}/location",
    response_model=DeliveryPartnerResponse,
    summary="Update delivery partners location",
    description="Only admin and delivery partner can Update location"
)
@limiter.limit("3/second")
async def update_location(
        request: Request,
        partner_id: int,
        latitude: Decimal,
        longitude: Decimal,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await delivery_partner_service.update_location(
        db,
        partner_id,
        latitude,
        longitude,
        current_user
    )


@router.delete(
    "/{partner_id}",
    response_model=DeliveryPartnerResponse,
    summary="Delete delivery partners",
    description="Only admin and delivery partner can delete"
)
@limiter.limit("3/second")
async def delete_delivery_partner(
        request: Request,
        partner_id: int,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await delivery_partner_service.delete_delivery_partner(
        db,
        partner_id,
        current_user
    )
