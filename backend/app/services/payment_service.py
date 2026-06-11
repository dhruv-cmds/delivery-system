from datetime import datetime
from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Payment, User
from app.schemas import PaymentCreate
from app.repositories import payment_repository

from app.repositories import order_repository
from app.core import (

    logger,

    UserRole,
    PaymentStatus,

    DatabaseError,

    PaymentNotFoundError,
    PaymentAlreadyCompletedError,
    PermissionDeniedError,

    OrderNotFoundError,
)


ONLINE_PAYMENT_METHODS = {
    "UPI",
    "CARD",
    "ONLINE",
}

def build_payment_metadata(payment_method):

    status = PaymentStatus.PENDING
    paid_at = None
    transaction_reference = None

    # TODO:
    # Replace with gateway callback flow
    if payment_method in ONLINE_PAYMENT_METHODS:

        status = PaymentStatus.SUCCESS
        paid_at = datetime.utcnow()
        transaction_reference = f"txn_{uuid4().hex}"

    return status, paid_at, transaction_reference


async def make_payment(
    db: AsyncSession,
    order_id: int,
    payment: PaymentCreate,
    current_user: User,
):

    if current_user.role != UserRole.CUSTOMER:

        logger.warning(
            "Payment creation denied: user ID %s is not a customer",
            current_user.id
        )

        raise PermissionDeniedError()

    order = await order_repository.get_order_by_id(
        db,
        order_id,
        current_user,
    )

    if not order:

        logger.warning(
            "order not found by order ID %s",
            order_id
        )

        raise OrderNotFoundError()

    existing_payment = await payment_repository.get_payment_by_order_id(
        db,
        order.id,
    )

    if (
        existing_payment and
        existing_payment.status == PaymentStatus.SUCCESS
    ):

        logger.warning(
            "Payment already completed for order ID %s",
            order.id
        )

        raise PaymentAlreadyCompletedError()

    status, paid_at, transaction_reference = build_payment_metadata(
        payment.payment_method
    )

    if existing_payment:

        existing_payment.amount = order.total_price
        existing_payment.payment_method = payment.payment_method
        existing_payment.status = status
        existing_payment.paid_at = paid_at
        existing_payment.transaction_reference = transaction_reference

        payment_record = existing_payment

    else:

        payment_record = Payment(
            order_id=order.id,
            amount=order.total_price,
            payment_method=payment.payment_method,
            status=status,
            paid_at=paid_at,
            transaction_reference=transaction_reference,
        )

    order.payment_status = status

    try:

        async with db.begin():

            payment_record = await payment_repository.save_payment(
                db,
                payment_record,
            )

        logger.info(
            "Payment processed successfully "
            "(payment_id=%s, order_id=%s)",
            payment_record.id,
            order.id,
        )

        return payment_record

    except IntegrityError:

        logger.exception(
            "Database integrity error while processing payment"
        )

        raise DatabaseError()

    except Exception:

        logger.exception(
            "Unexpected error while processing payment"
        )

        raise DatabaseError()
    

async def get_payment_by_id(
        db: AsyncSession,
        payment_id: int,
        current_user: User,
    ):

    payment = await payment_repository.get_payment_by_id(
        db,
        payment_id,
        current_user
    )

    if not payment:

        logger.warning(
            "Payment not found (payment_id=%s)",
            payment_id
        )
        raise PaymentNotFoundError()

    logger.info(
        "Payment retrieved successfully (payment_id=%s)",
        payment.id
    )

    return payment


async def get_payment_by_order_id(
        db: AsyncSession,
        order_id: int,
        current_user: User
    ):

    order = await order_repository.get_order_by_id(
        db,
        order_id,
        current_user,
    )
    
    if not order:

        logger.warning(
            "order not found by order ID %s",
            order_id
        )

        raise OrderNotFoundError()

    payment = await payment_repository.get_payment_by_order_id(
        db,
        order_id,
    )

    if not payment:

        logger.warning(
            "Payment not found for order ID %s",
            order_id
        )
        raise PaymentNotFoundError()

    logger.info(
        "Payment retrieved successfully for order ID %s",
        order_id
    )

    return payment


async def get_all_payments(
        db: AsyncSession,
        current_user: User,
    ):

    payments = await payment_repository.get_all_payments(

        db,
        current_user
    )

    logger.info(
        "Retrieved %s payments for user ID %s",
        len(payments),
        current_user.id
    )

    return payments


async def update_payment_status(
        db: AsyncSession,
        payment_id: int,
        status: PaymentStatus,
        current_user: User,
   ):

    if current_user.role != UserRole.ADMIN:

        logger.warning(
            "Payment status update denied: user ID %s is not an administrator",
            current_user.id
        )
        
        raise PermissionDeniedError()

    payment = await payment_repository.get_payment_for_status_update(
        db,
        payment_id
    )

    if not payment:

        logger.warning(
            "Payment status update failed: payment not found (payment_id=%s)",
            payment_id
        )

        raise PaymentNotFoundError()

    if (
        payment.status == PaymentStatus.SUCCESS
        and status == PaymentStatus.SUCCESS
    ):

        logger.warning(
            "Payment status update skipped: payment already completed (payment_id=%s)",
            payment_id
        )

        raise PaymentAlreadyCompletedError()

    payment.status = status
    payment.order.payment_status = status

    if status == PaymentStatus.SUCCESS:

        if not payment.paid_at:

            payment.paid_at = datetime.utcnow()

        if not payment.transaction_reference:

            payment.transaction_reference = f"txn_{uuid4().hex}"

    try:

        async with db.begin():

            await payment_repository.save_payment(
                db,
                payment,
            )

            await db.refresh(payment)
            
        logger.info(
            "Payment status updated successfully (payment_id=%s, status=%s)",
            payment_id,
            status
        )

        return payment

    except Exception:

        logger.exception("Unexpected error while updating payment status")

        raise DatabaseError()