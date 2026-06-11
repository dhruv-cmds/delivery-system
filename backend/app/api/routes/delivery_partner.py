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
    description=(
        "Create a new delivery partner profile. "
        "Accessible only to authenticated users and administrators."
    )
)
@limiter.limit("5/minute")
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
    summary="Get delivery partner by user ID",
    description=(
        "Retrieve a delivery partner profile using the associated user ID. "
        "Accessible only to administrators."
    )
)
@limiter.limit("60/minute")
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
    "/{partner_id}",
    response_model=DeliveryPartnerResponse,
    summary="Get delivery partner by ID",
    description=(
        "Retrieve a delivery partner profile by its unique partner ID. "
        "Accessible to all users."
    )
)
@limiter.limit("60/minute")
async def get_delivery_partner_by_id(
        request: Request,
        partner_id: int,
        db: AsyncSession = Depends(get_db),
    ):

    return await delivery_partner_service.get_delivery_partner_by_id(
        db,
        partner_id
    )



@router.put(
    "/{partner_id}",
    response_model=DeliveryPartnerResponse,
    summary="Update delivery partner vehicle",
    description=(
        "Update the vehicle information and status of a delivery partner. "
        "Accessible to the assigned delivery partner and administrators."
    )
)
@limiter.limit("20/minute")
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


@router.get(
    "/all",
    response_model=list[DeliveryPartnerResponse],
    summary="Get all delivery partners",
    description=(
        "Retrieve a list of all registered delivery partners. "
        "Accessible only to administrators."
    )
)
@limiter.limit("30/minute")
async def get_all_delivery_partners(
        request: Request,
        current_user = Depends(require_admin_access),
        db: AsyncSession = Depends(get_db)
    ):

    return await delivery_partner_service.get_all_delivery_partners(
        db
    )


@router.put(
    "/{partner_id}/location",
    response_model=DeliveryPartnerResponse,
    summary="Update delivery partner location",
    description=(
        "Update the current location coordinates of a delivery partner. "
        "Accessible to the assigned delivery partner and administrators."
    )
)
@limiter.limit("120/minute")
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
    summary="Delete a delivery partner",
    description=(
        "Remove a delivery partner profile. "
        "Accessible to the assigned delivery partner and administrators."
    )
)
@limiter.limit("10/minute")
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
