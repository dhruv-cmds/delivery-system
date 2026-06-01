from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from decimal import Decimal

from app.db.models import DeliveryPartner, User

from app.schemas import DeliveryPartnerCreate

from app.core import (

    logger,

    UserRole,

    DatabaseError,

    PermissionDeniedError,

    DeliveryPartnerNotFoundError,
    DeliveryPartnerAlreadyExistsError,
)


async def create_delivery_partner(
        db: AsyncSession,
        data: DeliveryPartnerCreate,
        current_user: User,
    ):

    existing = await db.execute(
        select(DeliveryPartner)
        .where(
            DeliveryPartner.user_id == current_user.id
        )
    )

    if existing.scalar_one_or_none():

        logger.warning(
            "Delivery partner profile already exists"
        )

        raise DeliveryPartnerAlreadyExistsError()

    partner = DeliveryPartner(
        user_id=current_user.id,
        vehicle_type=data.vehicle_type,
    )

    current_user.role = UserRole.DELIVERY_PARTNER.value

    try:

        db.add(partner)

        await db.commit()

        await db.refresh(partner)

        return partner

    except IntegrityError:

        await db.rollback()

        logger.exception(
            "Integrity error while creating delivery partner"
        )

        raise DeliveryPartnerAlreadyExistsError()

    except Exception:

        await db.rollback()

        logger.exception(
            "Unexpected error while creating delivery partner"
        )

        raise DatabaseError()
    

async def get_delivery_partner_by_user_id(
        db: AsyncSession,
        user_id: int,
    ):

    result = await db.execute(
        select(DeliveryPartner)
        .where(
            DeliveryPartner.user_id == user_id
        )
    )

    partner = result.scalar_one_or_none()

    if not partner:

        logger.warning(
            "Delivery partner not found"
        )

        raise DeliveryPartnerNotFoundError()

    return partner


async def get_delivery_partner_by_id(
        db: AsyncSession,
        partner_id: int,
    ):

    result = await db.execute(
        select(DeliveryPartner)
        .where(
            DeliveryPartner.id == partner_id
        )
    )

    partner = result.scalar_one_or_none()

    if not partner:

        logger.warning(
            "Delivery partner not found"
        )

        raise DeliveryPartnerNotFoundError()

    return partner



async def get_all_delivery_partners(
        db: AsyncSession,
        current_user: User
    ):

    if current_user.role != UserRole.ADMIN.value:

        logger.warning(
            "Non-admin attempted to access all delivery partners"
        )

        raise PermissionDeniedError()

    result = await db.execute(
        select(DeliveryPartner)
        .order_by(
            DeliveryPartner.created_at.desc()
        )
    )

    return result.scalars().all()


async def update_delivery_partner(
        db: AsyncSession,
        partner_id: int,
        data: DeliveryPartnerCreate,
        current_user: User,
    ):

    partner = await get_delivery_partner_by_id(
        db,
        partner_id,
    )

    if (
        current_user.role != UserRole.ADMIN.value
        and partner.user_id != current_user.id
    ):

        logger.warning(
            "Unauthorized delivery partner update attempt"
        )

        raise PermissionDeniedError()

    partner.vehicle_type = data.vehicle_type

    try:

        await db.commit()

        await db.refresh(partner)

        return partner

    except Exception:

        await db.rollback()

        logger.exception(
            "Unexpected error while updating delivery partner"
        )

        raise DatabaseError()


async def update_location(
        db: AsyncSession,
        partner_id: int,
        latitude: Decimal,
        longitude: Decimal,
        current_user: User,
    ):

    partner = await get_delivery_partner_by_id(
        db,
        partner_id,
    )

    if (
        current_user.role != UserRole.ADMIN.value
        and partner.user_id != current_user.id
    ):

        logger.warning(
            "Unauthorized location update attempt"
        )

        raise PermissionDeniedError()

    partner.latitude = latitude
    partner.longitude = longitude

    try:

        await db.commit()

        await db.refresh(partner)

        return partner

    except Exception:

        await db.rollback()

        logger.exception(
            "Unexpected error while updating location"
        )

        raise DatabaseError()
    
    
async def delete_delivery_partner(
        db: AsyncSession,
        partner_id: int,
        current_user: User,
    ):

    partner = await get_delivery_partner_by_id(
        db,
        partner_id,
    )

    if (
        current_user.role != UserRole.ADMIN.value
        and partner.user_id != current_user.id
    ):

        logger.warning(
            "Unauthorized delivery partner delete attempt"
        )

        raise PermissionDeniedError()

    try:

        await db.delete(partner)

        await db.commit()

        return True

    except Exception:

        await db.rollback()

        logger.exception(
            "Unexpected error while deleting delivery partner"
        )

        raise DatabaseError()