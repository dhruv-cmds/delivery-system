from sqlalchemy import select, or_

from app.db.models import User

from app.schemas import UserCreate

from sqlalchemy.ext.asyncio import AsyncSession


async def find_existing_user(
        db: AsyncSession, 
        user: UserCreate
    ):

    result = await db.execute(
        select(User)
        .where(
            or_(
                User.username == user.username.lower(),
                User.phone == user.phone,
                User.email == user.email.lower()
            ),
        )
    )

    return result.scalar_one_or_none()
    
async def get_user_by_id(
        db: AsyncSession,
        user_id: int,
    ):

    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )

    return result.scalar_one_or_none()
    

async def get_all_users(
        db: AsyncSession
    ):

    result = await db.execute(
        select(User)
    )
    
    return result.scalars().all()
    
async def get_user_by_email(
        db: AsyncSession,
        user_email: str,
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
