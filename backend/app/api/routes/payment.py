from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import (

    PaymentCreate,
    PaymentResponse
)

from app.services import payment_service

from app.core import limiter, PaymentStatus

from app.api import (
    get_db,
    get_current_user,
    require_admin_access,
)

router = APIRouter(
    tags=["PAYMENT"]
)

make_payment_router = APIRouter(
    tags=["MAKE PAYMENT"]
)


@make_payment_router.post(
    "/order/{order_id}/payment",
    response_model=PaymentResponse,
    summary="Make a payment for an created order",
    description=(
        "Only authenticate user can make payment after creating order"
    )
)
@limiter.limit("5/minute")
async def make_payment(
        request: Request,
        order_id: int,
        payment: PaymentCreate,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await payment_service.make_payment(
        db,
        order_id,
        payment,
        current_user
    )


@router.get(
    "/payment/all",
    response_model=list[PaymentResponse],
    summary=(
        "Get all payments information"
    ),
    description=(
        "Only authenticate user can get only their payment details order id"
    )
)
@limiter.limit("30/minute")
async def get_all_payments(
        request: Request,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await payment_service.get_all_payments(
        db,
        current_user
    )


@router.get(
    "/payment/{payment_id}",
    response_model=PaymentResponse,
    summary=(
        "Get a payment information for any specific order by payment ID"
    ),
    description=(
        "Only admin can get payment details by payment ID"
    )
)
@limiter.limit("60/minute")
async def get_payment_by_id(
        request: Request,
        payment_id: int,
        current_user=Depends(require_admin_access),
        db: AsyncSession = Depends(get_db)
    ):

    return await payment_service.get_payment_by_id(
        db,
        payment_id,
        current_user
    )


@router.get(
    "/order/{order_id}/payment",
    response_model=PaymentResponse,
    summary=(
        "Get a payment information for specific order by order ID"
    ),
    description=(
        "Only authenticate user can get only their payment details by order ID"
    )
)
@limiter.limit("60/minute")
async def get_payment_by_order_id(
        request: Request,
        order_id: int,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    return await payment_service.get_payment_by_order_id(
        db,
        order_id,
        current_user
    )


@router.patch(
    "/payment/{payment_id}/status",
    response_model=PaymentResponse,
    summary=(
        "Get all payments information"
    ),
    description=(
        "Only authenticate user can get only their payment details order id"
    )
)
@limiter.limit("20/minute")
async def update_payment_status(
        request: Request,
        payment_id: int,
        status: PaymentStatus,
        current_user=Depends(require_admin_access),
        db: AsyncSession = Depends(get_db)
    ):

    return await payment_service.update_payment_status(
        db,
        payment_id,
        status,
        current_user
    )