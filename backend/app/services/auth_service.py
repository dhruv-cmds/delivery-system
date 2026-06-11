from app.schemas import UserCreate

from app.services.user_service import create_user


from app.core import (

    create_access_token,
    verify_password,

    UserNotFoundError,
    InvalidCredentialsError,

    logger
)

from app.repositories import user_repository


async def sign_up(db, user: UserCreate):

    return await create_user(db, user)
    
async def login(
        db,
        email: str,
        password: str,
    ):

    try:

        user = await user_repository.get_user_by_email(db,email)

    except UserNotFoundError:

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
            "email": user.email,
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
