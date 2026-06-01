from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Payment, Order, User
from app.schemas import PaymentCreate

from app.services.order_query_service import (
    apply_order_visibility,
    get_order_by_id
)

from app.core import (

    logger,

    UserRole,
    PaymentStatus,

    DatabaseError,
    InvalidOperationError,

    PaymentNotFoundError,
    PaymentAlreadyCompletedError,
    InsufficientBalanceError,
    PermissionDeniedError,
)


ONLINE_PAYMENT_METHODS = {
    "UPI",
    "CARD",
    "ONLINE",
}


async def make_payment(
        db: AsyncSession,
        order_id: int,
        payment: PaymentCreate,
        current_user: User,
    ):

    if current_user.role != UserRole.CUSTOMER.value:

        logger.warning("Non-customer attempted to make payment")
        raise PermissionDeniedError()
    
    order = await get_order_by_id(
        db,
        order_id,
        current_user,
    )

    result = await db.execute(
        select(Payment)
        .where(Payment.order_id == order.id)
    )

    existing_payment = result.scalar_one_or_none()

    if existing_payment and existing_payment.status == PaymentStatus.SUCCESS.value:

        logger.warning("Completed payment attempted again")
        raise PaymentAlreadyCompletedError()

    status = PaymentStatus.PENDING.value
    paid_at = None
    transaction_reference = None

    if payment.payment_method in ONLINE_PAYMENT_METHODS:

        status = PaymentStatus.SUCCESS.value
        paid_at = datetime.utcnow()
        transaction_reference = f"txn_{uuid4().hex}"

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

        db.add(payment_record)

    order.payment_status = status

    try:

        await db.commit()

        await db.refresh(payment_record)

        return payment_record

    except IntegrityError:

        await db.rollback()

        logger.exception("Integrity error while creating payment")
        raise PaymentNotFoundError()

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while creating payment")
        raise DatabaseError()


async def get_payment_by_id(
        db: AsyncSession,
        payment_id: int,
        current_user: User,
    ):

    statement = (
        select(Payment)
        .join(Order, Payment.order_id == Order.id)
        .where(Payment.id == payment_id)
    )

    statement = apply_order_visibility(statement, current_user)

    result = await db.execute(statement)

    payment = result.scalar_one_or_none()

    if not payment:

        logger.warning("Payment not found")
        raise PaymentNotFoundError()

    return payment


async def get_payment_by_order_id(
        db: AsyncSession,
        order_id: int,
        current_user: User,
    ):

    order = await get_order_by_id(
        db,
        order_id,
        current_user,
    )

    result = await db.execute(
        select(Payment)
        .where(Payment.order_id == order.id)
    )

    payment = result.scalar_one_or_none()

    if not payment:

        logger.warning("Payment not found for order")
        raise PaymentNotFoundError()

    return payment


async def update_payment_status(
        db: AsyncSession,
        payment_id: int,
        status: str,
        current_user: User,
    ):

    if current_user.role != UserRole.ADMIN.value:

        logger.warning("Non-admin attempted to update payment status")
        raise PermissionDeniedError()

    valid_statuses = {payment_status.value for payment_status in PaymentStatus}

    if status not in valid_statuses:

        logger.warning("Invalid payment status update attempted")
        raise InvalidOperationError(f"Invalid payment status '{status}'")

    result = await db.execute(
        select(Payment)
        .options(selectinload(Payment.order))
        .join(Order, Payment.order_id == Order.id)
        .where(Payment.id == payment_id)
    )

    payment = result.scalar_one_or_none()

    if not payment:

        logger.warning("Payment not found")
        raise PaymentNotFoundError()

    if (
        payment.status == PaymentStatus.SUCCESS.value
        and status == PaymentStatus.SUCCESS.value
    ):

        logger.warning("Completed payment marked successful again")
        raise PaymentAlreadyCompletedError()

    payment.status = status
    payment.order.payment_status = status

    if status == PaymentStatus.SUCCESS.value:

        if not payment.paid_at:

            payment.paid_at = datetime.utcnow()

        if not payment.transaction_reference:

            payment.transaction_reference = f"txn_{uuid4().hex}"

    try:

        await db.commit()

        await db.refresh(payment)

        return payment

    except IntegrityError:

        await db.rollback()

        logger.exception("Integrity error while updating payment status")
        raise PaymentNotFoundError()

    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while updating payment status")
        raise DatabaseError()
