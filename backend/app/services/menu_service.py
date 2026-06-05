from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (

    User,
    Menu,
    Restaurant
)

from app.schemas import MenuCreate

from sqlalchemy.exc  import IntegrityError

from app.core import (

    logger,

    UserRole,

    MenuStatus,

    DatabaseError,
    PermissionDeniedError,
    MenuAlreadyExistsError,
    MenuNotFoundError,

    RestaurantNotFoundError
)


async def create_menu_item(
        db: AsyncSession,
        menu: MenuCreate,
        current_user: User
    ):

    restaurant_result = await db.execute(
        select(Restaurant)
        .where(Restaurant.id == menu.restaurant_id)
    )

    restaurant = restaurant_result.scalar_one_or_none()

    if not restaurant:

        logger.warning(
            "Menu item creation failed because the restaurant was not found"
        )
        raise RestaurantNotFoundError()
    
    if current_user.role not in (
        UserRole.ADMIN,
        UserRole.RESTAURANT_OWNER,
    ):
        logger.warning(
            "Menu item creation denied because the user is not an admin or restaurant owner"
        )
        raise PermissionDeniedError()

    if (
        current_user.role != UserRole.ADMIN and
        restaurant.owner_id != current_user.id
    ):

        logger.warning(
            "Menu item creation denied because the restaurant belongs to another owner"
        )
        raise PermissionDeniedError()

    
    result = await db.execute(

        select(Menu)
        .where(
            (Menu.restaurant_id == menu.restaurant_id),
            (Menu.item_name == menu.item_name),
        )
    )

    existing_menu = result.scalar_one_or_none()

    if existing_menu:

        logger.warning(
            "Menu item creation skipped because the item already exists"
        )
        raise MenuAlreadyExistsError()
    

    new_menu = Menu(

        restaurant_id=menu.restaurant_id,
        item_name=menu.item_name,
        price=menu.price,
        description=menu.description
    )

    try:

        db.add(new_menu)

        await db.commit()

        await db.refresh(new_menu)

        return new_menu

    except IntegrityError:

        await db.rollback()

        logger.exception("Database integrity error while creating menu item")
        raise MenuAlreadyExistsError()
    
    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while creating menu item")
        raise DatabaseError()
    
    
async def get_menu_item_by_id (
        db: AsyncSession,
        menu_id: int,
    ):

    result = await db.execute(
        select(Menu)
        .where(Menu.id == menu_id)
    )

    menu = result.scalar_one_or_none()

    if not menu:

        logger.warning(
            "Menu item lookup failed because the item was not found"
        )
        raise MenuNotFoundError()
    
    return menu

async def get_menu_items_by_restaurant_id(
        db: AsyncSession,
        restaurant_id: int
    ):

    result = await db.execute(

        select(Menu)
        .where(Menu.restaurant_id == restaurant_id)
    )

    return result.scalars().all()
    

async def update_menu_item(
        db: AsyncSession,
        menu_data: MenuCreate,
        menu_id: int,
        current_user: User
    ):

    menu = await get_menu_item_by_id(db, menu_id)

    restaurant_result = await db.execute(

        select(Restaurant)
        .where(Restaurant.id == menu.restaurant_id)
    )

    restaurant = restaurant_result.scalar_one_or_none()

    if not restaurant:

        logger.warning(
            "Menu item update failed because the restaurant was not found"
        )
        raise PermissionDeniedError()
    

    if current_user.role not in (

        UserRole.ADMIN,
        UserRole.RESTAURANT_OWNER,
    ):
        
        logger.warning(
            "Menu item update denied because the user is not an admin or restaurant owner"
        )
        raise PermissionDeniedError()
    
    if (
        current_user.role != UserRole.ADMIN and
        restaurant.owner_id != current_user.id
    ):

        logger.warning(
            "Menu item update denied because the restaurant belongs to another owner"
        )
        raise PermissionDeniedError()
    

    menu.restaurant_id = menu_data.restaurant_id
    menu.item_name = menu_data.item_name
    menu.description = menu_data.description
    menu.price = menu_data.price


    try:

        await db.commit()

        await db.refresh(menu)

        return menu
    
    except IntegrityError:

        await db.rollback()

        logger.warning("Database integrity error while updating menu item")
        raise MenuAlreadyExistsError()
    
    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while updating menu item")
        raise DatabaseError()
    
async def delete_menu_item(
        
        db: AsyncSession,
        menu_id: int,
        current_user: User
    ):

    menu = await get_menu_item_by_id(db, menu_id)

    restaurant_result = await db.execute (
        select(Restaurant)
        .where(Restaurant.id == menu.restaurant_id)
    )

    restaurant = restaurant_result.scalar_one_or_none()

    if not restaurant:

        logger.warning(
            "Menu item deletion failed because the restaurant was not found"
        )
        raise PermissionDeniedError()
    
    if current_user.role not in (
        
        UserRole.ADMIN,
        UserRole.RESTAURANT_OWNER
    ):
        
        logger.warning(
            "Menu item deletion denied because the user is not an admin or restaurant owner"
        )
        raise PermissionDeniedError()
    
    if (
        current_user.role != UserRole.ADMIN and
        restaurant.owner_id != current_user.id
    ):
        
        logger.warning(
            "Menu item deletion denied because the restaurant belongs to another owner"
        )
        raise PermissionDeniedError()
    

    try:

        await db.delete(menu)

        await db.commit()

        return menu
    
    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while deleting menu item")
        raise DatabaseError()



async def change_menu_status(
        db: AsyncSession,
        menu_id: int,
        status: MenuStatus,
        current_user: User
    ):

    menu = await get_menu_item_by_id(db, menu_id)

    restaurant_result = await db.execute(
        select(Restaurant)
        .where(Restaurant.id == menu.restaurant_id)
    )

    restaurant = restaurant_result.scalar_one_or_none()

    if not restaurant:

        logger.warning(
            "Menu status update failed because the restaurant was not found"
        )
        raise PermissionDeniedError()
    
    if current_user.role not in (

        UserRole.ADMIN,
        UserRole.RESTAURANT_OWNER
    ):
        
        logger.warning(
            "Menu status update denied because the user is not an admin or restaurant owner"
        )
        raise PermissionDeniedError()
    
    if (
        current_user.role != UserRole.ADMIN
        and
        restaurant.owner_id != current_user.id
    ):
        logger.warning(
            "Menu status update denied because the restaurant belongs to another owner"
        )
        raise PermissionDeniedError()
    

    menu.status = status

    try:

        await db.commit()

        await db.refresh(menu)

        return menu
    
    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while changing menu item status")
        raise DatabaseError()
