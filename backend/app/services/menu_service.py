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

    DatabaseError,
    PermissionDeniedError,
    MenuAlreadyExistsError,
    MenuNotFoundError,
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

        logger.warning("Restaurant not found while creating menu item")
        raise MenuNotFoundError()
    
    if restaurant.owner_id != current_user.id:

        logger.warning("User tried to create menu item for another restaurant")
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

        logger.warning("Menu item already exists")
        raise MenuAlreadyExistError()
    

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

        logger.exception("Integrity error while creating menu")
        raise MenuAlreadyExistError()
    
    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while creating menu")
        raise DatabaseError()
    
    
async def get_menu_item_by_id (
        db: AsyncSession,
        menu_id: int
    ):

    result = await db.execute(
        select(Menu)
        .where(Menu.id == menu_id)
    )

    menu = result.scalar_one_or_none()

    if not menu:

        logger.warning("Menu item not found")
        raise MenuNotFoundError()
    
    return menu

async def get_menu_items_by_restaurant(
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

    if not restaurant or restaurant.owner_id != current_user.id:

        logger.warning("User tried to update menu item without permission")
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

        logger.warning("Integrity error while updating menu")
        raise MenuAlreadyExistError()
    
    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while updating menu item")
        raise DatabaseError()
    
async def detele_menu_item(
        
        db: AsyncSession,
        menu_id: int,
        current_id: User
    ):

    menu = await get_menu_item_by_id(db, menu_id)

    restaurant_result = await db.execute (
        select(Restaurant)
        .where(Restaurant.id == menu.restaurant_id)
    )

    restaurant = restaurant_result.scalar_one_or_none()

    if not restaurant or restaurant.owner_id != current_id.id:

        logger.warning("User tried to delete menu item without permission")
        raise PermissionDeniedError()
    
    try:

        await db.delete(menu)

        await db.commit()

        return{
            "message": "Menu item deleted successfully"
        }
    
    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while updating menu item")
        raise DatabaseError()

async def change_menu_status(
        db: AsyncSession,
        menu_id: int,
        status: str,
        current_user: User
    ):

    menu = await get_menu_item_by_id(db, menu_id)

    restaurant_result = await db.execute(
        select(Restaurant)
        .where(Restaurant.id == menu.restaurant_id)
    )

    restaurant = restaurant_result.scalar_one_or_none()

    if not restaurant or restaurant.owner_id != current_user.id:

        logger.warning("User tried to change menu status without permission")
        raise PermissionDeniedError()

    menu.status = status

    try:

        await db.commit()

        await db.refresh(menu)

        return menu
    
    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while changing menu status")
        raise DatabaseError()