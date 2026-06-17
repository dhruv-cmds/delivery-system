import json

from app.core import redis_client

from app.core import (
    
    logger,

    DatabaseError,
    UserNotFoundError,
    UserAlreadyExistsError,

    hash_password
)

from sqlalchemy.exc  import IntegrityError

from app.db.models import User

from app.schemas import UserCreate

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user_repository

async def create_user(
    db: AsyncSession,
    user: UserCreate
):
    try:


        existing_user = await user_repository.find_existing_user(
            db,
            user
        )

        if existing_user:
            logger.warning(
                "User already exists (email=%s)",
                user.email.lower()
            )
            raise UserAlreadyExistsError()

        new_user = User(
            username=user.username.lower(),
            name=user.name,
            phone=user.phone,
            email=user.email.lower(),
            hashed_password=hash_password(user.password)
        )

        db.add(new_user)

        await db.flush()

        logger.info(
            "User created successfully (user_id=%s)",
            new_user.id
        )

        return new_user

    except IntegrityError:

        await db.rollback()

        logger.exception(
            "Database integrity error while creating user"
        )
        raise UserAlreadyExistsError()

    except Exception:

        await db.rollback()
        
        logger.exception(
            "Unexpected error while creating user account"
        )
        raise DatabaseError()
    

async def get_user_by_id(
        db: AsyncSession,
        user_id: int,
    ):

    cache_key = f"user:id:{user_id}"

    cached_user = await redis_client.get(cache_key)

    if cached_user:

        logger.info(
            "User retriedved from Redis (user_id=%s)",
            user_id
        )

        return json.loads(cached_user)

    user = await user_repository.get_user_by_id(
        db,
        user_id
    )

    if not user:

        logger.warning(
            "User not found (user_id=%s)",
            user_id
        )

        raise UserNotFoundError()
    
    user_data = {

        "id": user.id,
        "username":user.username,
        "name":user.name,
        "phone":user.phone,
        "email":user.email,
        "role": user.role,
        "status": user.status,
    }

    await redis_client.set(
        cache_key,
        json.dumps(
            user_data,
            default=str
        ),
        ex=300
    )
    
    logger.info(
        "User retrieved from DB and cached successfully (user_id=%s)",
        user.id
    )

    return user

async def get_all_users(
        db: AsyncSession,
    ):
    
    result = await user_repository.get_all_users(
        db
    )

    logger.info(
        "All users retrieved successfully"
    )
    
    return result
    
async def get_user_by_email(
        db,
        user_email: str,
    ):  

    cache_key = f"user:email:{user_email}"

    cache_user = await redis_client.get(cache_key)

    if cache_user:

        logger.info(
            "User retrived from Redis (user_email=%s)",
            user_email
        )

        return json.loads(cache_user)
    
    user = await user_repository.get_user_by_email(
        db,
        user_email 
    )

    if not user:

        logger.warning(
            "User not found (email=%s)",
            user_email
        )

        raise UserNotFoundError()
    
    user_data = {

        "id": user.id,
        "username":user.username,
        "name":user.name,
        "phone":user.phone,
        "email": user.email,
        "role": user.role,
        "status": user.status,
    }

    await redis_client.set(
        cache_key,
        json.dumps(
            user_data,
            default=str
        ),
        ex=300      # cach for 5 min or waht every you like
    )
    
    logger.info(

        "User retrieved from DB and cached successfully (email=%s)",
        user.email
    )

    return user

async def get_user_by_username(
        db: AsyncSession,
        username: str
    ):

    cache_key = f"user:username:{username}"

    cache_user = await redis_client.get(cache_key)

    if cache_user:

        logger.info(
            "User retrived from Redis (username=%s)",
            username
        )

        return json.loads(cache_user)
    
    user = await user_repository.get_user_by_username(
        db,
        username
    )

    if not user:

        logger.warning(
            "User not found (username=%s)",
            username
        )
        
        raise UserNotFoundError()
    
    user_data = {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "phone": user.phone,
        "email": user.email,
        "role": user.role,
        "status": user.status,
    }

    await redis_client.set(
        cache_key,
        json.dumps(
            user_data,
            default=str
        ),
        ex=300
    )

    logger.info(
        "User retrieved from DB and cached successfully (username=%s)",
        user.username
    )

    return user