from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserCreate

from app.services.user_service import (
    create_user,
    get_user_by_email
)

from app.core import (

    create_access_token,
    verify_password,

    InvalidCredentialsError,
    logger
)

async def sign_up(db, user: UserCreate):

    return await create_user(db, user)
    
async def login(
        db,
        email: str,
        password: str,
    ):

    user = await get_user_by_email(
        db,
        email,
    )

    if not user:

        logger.warning(
            "Login failed: user not found for email '%s'",
            email
        )
        raise InvalidCredentialsError()

    if not verify_password(password, user.hashed_password):

        logger.warning(
            "Login failed: invalid password for user ID %s",
            user.id
        )
        raise InvalidCredentialsError()

    token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    logger.info(
        "User authenticated successfully (user_id=%s)",
        user.id
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
