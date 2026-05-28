from app.core import (
    
    logger,

    DatabaseError,
    UserNotFoundError,
    UserAlreadyExistsError,

    hash_password
)

from sqlalchemy.exc  import IntegrityError

from sqlalchemy import select, func

from app.db.models import User

from app.schemas import UserCreate

from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(
        db: AsyncSession, 
        user: UserCreate
    ):
    
    result = await db.execute(
        select(User)
        .where(
            (User.username == user.username.lower()) |
            (User.phone == user.phone) |
            (User.email == user.email)
        )
    )

    exist = result.scalar_one_or_none()

    if exist:

        logger.warning("User already exists")
        raise UserAlreadyExistsError()
    
    
    new_user = User(
        username=user.username.lower(),
        name=user.name,
        phone=user.phone,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    try:

        db.add(new_user)

        await db.commit()

        await db.refresh(new_user)

        return new_user

    except IntegrityError:

        await db.rollback()

        logger.exception("Integrity error while creating user")
        raise UserAlreadyExistsError()
    
    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while creating user")
        raise DatabaseError()
    

async def get_user_by_id (
        db:AsyncSession,
        user_id:int
    ):

    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if not user:

        logger.warning("User not found")
        raise UserNotFoundError()
    
    return user

async def get_user_by_email(
        db:AsyncSession,
        user_email: str
    ):

    result = await db.execute(
        select(User)
        .where(User.email == user_email)
    )

    return result.scalar_one_or_none()

async def get_user_by_username(
        db: AsyncSession,
        username: str
    ):

    result = await db.execute(
        select(User)
        .where(User.username == username)
    )
    
    return result.scalar_one_or_none()