from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from decimal import Decimal

from app.db.models import DeliveryPartner, User

from app.schemas import DeliveryPartnerCreate, DeliveryPartnerResponse

from app.core import (

    logger,
    redis_client,

    UserRole,
    VehicleTypeStatus,

    DatabaseError,

    PermissionDeniedError,

    UserNotFoundError,

    DeliveryPartnerNotFoundError,
    DeliveryPartnerAlreadyExistsError,

    InvalidLatitudeError,
    InvalidLongitudeError
)

from app.repositories import delivery_repository

async def create_delivery_partner(
        db: AsyncSession,
        data: DeliveryPartnerCreate,
        current_user: User,
    ):

    existing = await delivery_repository.get_delivery_partner_user_id(
        db,
        current_user.id
    )

    if existing:

        logger.warning(
            "Delivery partner creation failed: profile already exists for user ID %s",
            current_user.id
        )

        raise DeliveryPartnerAlreadyExistsError()
    
    if current_user.role != UserRole.CUSTOMER:

        logger.warning(
            "Delivery partner creation denied: only customers can become delivery partners (user_id=%s, role=%s)",
            current_user.id,
            current_user.role
        )

        raise PermissionDeniedError()
    
    partner = DeliveryPartner(
        user_id=current_user.id,
        vehicle_type=data.vehicle_type,
    )

    try:

        if current_user.role == UserRole.CUSTOMER:

            logger.info(
                "User role updated from CUSTOMER to DELIVERY_PARTNER (user_id=%s)",
                current_user.id
            )

            current_user.role = UserRole.DELIVERY_PARTNER

        db.add(partner)

        await db.flush()

        await db.commit()

        logger.info(
            "Delivery partner created successfully (user_id=%s)",
            current_user.id
        )

        return partner

    except IntegrityError:

        await db.rollback()

        logger.exception(
            "Database integrity error while creating delivery partner"
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

    cache_key = f"user_id:{user_id}"

    cached = await redis_client.get(cache_key)

    if cached:

        logger.info(
            "Delivery partner ID retrived by user ID (user_id=%s)",
            user_id
        )

        return DeliveryPartnerResponse.model_validate_json(cached)

    partner = await delivery_repository.get_delivery_partner_user_id(
        db,
        user_id
    )

    if not partner:

        logger.warning(
            "Delivery partner not found for user ID %s",
            user_id
        )
        raise DeliveryPartnerNotFoundError()
    
    response = DeliveryPartnerResponse.model_validate(

        # schema has from_attributes so you can only use payment 
        # and can use with from_attributes both works
        # use what every you like
        
        partner,
        from_attributes=True
    )

    await redis_client.set(
        cache_key,
        response.model_dump_json(),
        ex=300
    )

    return response

async def get_delivery_partner_by_id(
        db: AsyncSession,
        partner_id: int,
    ):

    cache_key = f"partner_id:{partner_id}"

    cached = await redis_client.get(cache_key)

    if cached:

        logger.info(
            "Delivery partner ID retrived by user ID (user_id=%s)",
            partner_id
        )

        return DeliveryPartnerResponse.model_validate_json(cached)

    partner = await delivery_repository.get_delivery_partner_by_id(
        db,
        partner_id
    )

    if not partner:

        logger.warning(
            "Delivery partner lookup failed because the profile was not found %s",
            partner_id
        )

        raise DeliveryPartnerNotFoundError()
    
    response = DeliveryPartnerResponse.model_validate(
        
        partner,
        from_attributes=True
    )

    await redis_client.set(
        cache_key,
        response.model_dump_json(),
        ex=300
    )

    return response

async def get_all_delivery_partners(
        db: AsyncSession,
    ):

    return await delivery_repository.get_all_delivery_partners(
        db
    )


async def update_delivery_partner(
        db: AsyncSession,
        partner_id: int,
        vehicle_type: VehicleTypeStatus,
        current_user: User,
    ):

    partner = await delivery_repository.get_delivery_partner_by_id(
        db,
        partner_id,
    )

    if not partner:

        logger.warning(
            "Delivery partner lookup failed because the profile was not found %s",
            partner_id
        )

        raise DeliveryPartnerNotFoundError()

    if (
        current_user.role != UserRole.ADMIN
        and partner.user_id != current_user.id
    ):

        logger.warning(
            "Delivery partner update denied: user ID %s is not authorized",
            current_user.id
        )

        raise PermissionDeniedError()

    partner.vehicle_type = vehicle_type

    try: 

        await db.commit()

        await db.refresh(partner)

        logger.info(
            "Delivery partner update successfully (partner_id=%s)",
            partner_id
        )

        cache_key_partner = f"partner_id:{partner.id}"
        cache_key_user = f"user_id:{partner.user_id}"

        response = DeliveryPartnerResponse.model_validate(
        
            partner,
            from_attributes=True
        )

        await redis_client.set(
            cache_key_partner,
            response.model_dump_json(),
            ex=300
        )

        await redis_client.set(
            cache_key_user,
            response.model_dump_json(),
            ex=300
        )

        return response

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

    partner = await delivery_repository.get_delivery_partner_by_id(
        db,
        partner_id,
    )

    if not partner:

        logger.warning(
            "Delivery partner lookup failed because the profile was not found %s",
            partner_id
        )

        raise DeliveryPartnerNotFoundError()

    if (
        current_user.role != UserRole.ADMIN
        and partner.user_id != current_user.id
    ):

        logger.warning(
            "Location update denied: user ID %s is not authorized",
            current_user.id
        )

        raise PermissionDeniedError()
    
    if latitude < -90 or latitude > 90:
        raise InvalidLatitudeError()

    if longitude < -180 or longitude > 180:
        raise InvalidLongitudeError()
    
    partner.latitude = latitude
    partner.longitude = longitude

    try:

        await db.commit()

        await db.refresh(partner)

        logger.info(
            "Delivery partner location updated successfully (partner_id=%s)",
            partner_id
        )

        cache_key_partner = f"partner_id:{partner.id}"
        cache_key_user = f"user_id:{partner.user_id}"

        response = DeliveryPartnerResponse.model_validate(
        
            partner,
            from_attributes=True
        )

        await redis_client.set(
            cache_key_partner,
            response.model_dump_json(),
            ex=300
        )

        await redis_client.set(
            cache_key_user,
            response.model_dump_json(),
            ex=300
        )

        return response
    
    except Exception:

        await db.rollback()

        logger.exception(
            "Unexpected error while updating delivery partner location"
        )

        raise DatabaseError()
    
    
async def delete_delivery_partner(
        db: AsyncSession,
        partner_id: int,
        current_user: User,
    ):

    partner = await delivery_repository.get_delivery_partner_by_id(
        db,
        partner_id,
    )

    if not partner:

        logger.warning(
            "Delivery partner lookup failed because the profile was not found %s",
            partner_id
        )

        raise DeliveryPartnerNotFoundError()

    if (
        current_user.role != UserRole.ADMIN
        and partner.user_id != current_user.id
    ):

        logger.warning(
            "Delivery partner deletion denied: user ID %s is not authorized",
            current_user.id
        )

        raise PermissionDeniedError()

    try:
         
        partner_owner = await db.get(
            User,
            partner.user_id
        )

        if not partner_owner:

            logger.warning(
                "User not found %s",
                partner.user_id
            )
            
            raise UserNotFoundError()

        partner_owner.role = UserRole.CUSTOMER
                    
        await db.delete(partner)

        await db.commit()

        await db.refresh(partner_owner)


        logger.info(
            "Partner owner role after commit: %s",
            partner_owner.role
        )

        logger.info(
            "Delivery partner deleted successfully (partner_id=%s)",
            partner_id
        )
        
        return partner

    except Exception:

        await db.rollback()

        logger.exception(
            "Unexpected error while deleting delivery partner"
        )

        raise DatabaseError()
