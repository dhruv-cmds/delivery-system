from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import limiter

from app.schemas import TrackingCreate, TrackingResponse
from app.services import tracking_service

from app.api import get_db
from app.api import (
    get_current_user,
    get_access_manager
)

router = APIRouter(
    prefix="/traking",
    tags=["ORDER TRACKING"]
)

@router.post(
    "/",
    response_model=TrackingResponse,
    summary="Create a delivery partner",
    description=(
        "Create a new tracking profile for order."
        "Accessible only to restaurant owner and administrators."
    )
)
@limiter.limit("5/minute")
async def create_tracking(
        request: Request,
        tracking: TrackingCreate,
        current_user = Depends(get_access_manager),
        db: AsyncSession = Depends(get_db)
    ):

    return await tracking_service.create_tracking(
        db,
        tracking
    )

@router.get(
    "/order/{order_id}",
    response_model=TrackingResponse,
    summary="Get order tracking by order ID",
    description=(
        "Retrieve a order tracking using the associated order ID. "
        "Accessible to order owner."
    )
)
@limiter.limit("60/minute")
async def get_tracking_by_order(
        request: Request,
        order_id: int,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
    ):

    return await tracking_service.get_tracking_by_order(
        db,
        order_id,
        current_user
    )

@router.get(
    "/all",
    response_model=list[TrackingResponse],
    summary="Get order tracking by order ID",
    description=(
        "Retrieve a order tracking using the associated order ID. "
        "Accessible to order owner."
    )
)
@limiter.limit("60/minute")
async def get_tracking_by_order(
        request: Request,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_access_manager)
    ):

    return await tracking_service.get_all_tracking(
        db,
    )