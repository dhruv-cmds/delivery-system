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

    try:

        async with db.begin():

            db.add(new_user)

        await db.refresh(new_user)

        logger.info(
            "User created successfully (user_id=%s)",
            new_user.id
        )

        return new_user
    
    except IntegrityError:

        logger.exception("Database integrity error while creating user")

        raise UserAlreadyExistsError()
    
    except Exception:

        logger.exception("Unexpected error while creating user account")

        raise DatabaseError()
    

async def get_user_by_id(
        db: AsyncSession,
        user_id: int,
    ):

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
    
    logger.info(
        "User retrieved successfully (user_id=%s)",
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
    
    logger.info(

        "User retrieved successfully (email=%s)",
        user.email
    )

    return user

async def get_user_by_username(
        db: AsyncSession,
        username: str
    ):

    user = await user_repository.get_user_by_username(
        db,
        username
    )

    if not user:

        logger.warning(
            "User not found (username=%s)",
            username
        )
        
        return UserNotFoundError()

    logger.info(
        "User retrieved successfully (username=%s)",
        user.username
    )

    return user