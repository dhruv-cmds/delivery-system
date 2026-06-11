from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Payment, Order, User

from app.repositories.order_repository import (
    apply_order_visibility,
)


async def save_payment(
        db: AsyncSession,
        payment: Payment,
    ):

    if payment.id is None:
        db.add(payment)

        await db.flush()


async def get_payment_by_order_id(
        db: AsyncSession,
        order_id: int,
    ):

    result = await db.execute(
        select(Payment)
        .where(Payment.order_id == order_id)
    )

    return result.scalar_one_or_none()

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

    return payment


async def get_all_payments(
        db: AsyncSession,
        current_user: User,
    ):

    statement = (
        select(Payment)
        .join(Order)
        .order_by(Payment.created_at.desc())
    )

    statement = apply_order_visibility(
        statement,
        current_user
    )

    result = await db.execute(statement)

    payments = result.scalars().all()

    return payments


async def get_payment_for_status_update(
        db: AsyncSession,
        payment_id: int,
    ):

    result = await db.execute(
        select(Payment)
        .options(selectinload(Payment.order))
        .join(Order, Payment.order_id == Order.id)
        .where(Payment.id == payment_id)
    )

    return result.scalar_one_or_none()
