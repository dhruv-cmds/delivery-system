from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (

    User,
    Menu,
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

from app.repositories import  menu_repository

async def create_menu_item(
        db: AsyncSession,
        menu: MenuCreate,
        current_user: User
    ):

    restaurant = await menu_repository.get_restaurant_by_id(
        db,
        menu.restaurant_id
    )

    if not restaurant:

        logger.warning(
            "Menu item creation failed: restaurant not found (restaurant_id=%s)",
            menu.restaurant_id
        )

        raise RestaurantNotFoundError()

    if (
        current_user.role != UserRole.ADMIN and
        restaurant.owner_id != current_user.id
    ):

        
        logger.warning(
            "Menu item creation denied: user ID %s is not the restaurant owner",
            current_user.id
        )
        raise PermissionDeniedError()

    
    existing_menu = await menu_repository.get_menu_by_name(
        db,
        menu.restaurant_id,
        menu.item_name
    )

    if existing_menu:

        logger.warning(
            "Menu item already exists (restaurant_id=%s, item_name='%s')",
            menu.restaurant_id,
            menu.item_name
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
        
        await db.flush()

        await db.refresh(new_menu)

        await db.commit()

        logger.info(
            "Menu item created successfully (menu_id=%s)",
            new_menu.id
        )

        return new_menu

    except IntegrityError:

        await db.rollback()

        logger.exception(
            "Database integrity error while creating menu item"
        )

        raise MenuAlreadyExistsError()
    
    except Exception:
        
        await db.rollback()

        logger.exception("Unexpected error while creating menu item")

        raise DatabaseError()
    
    
async def get_menu_item_by_id (
        db: AsyncSession,
        menu_id: int,
    ):

    menu = await menu_repository.get_menu_by_id(
        db,
        menu_id
    )

    if not menu:

        logger.warning(
            "Menu item not found (menu_id=%s)",
            menu_id
        )

        raise MenuNotFoundError()
    
    return menu

async def get_menu_items_by_restaurant_id(
        db: AsyncSession,
        restaurant_id: int
    ):

    return await menu_repository.get_menu_by_restaurant_id(
        db,
        restaurant_id
    )
    

async def update_menu_item(
        db: AsyncSession,
        menu_data: MenuCreate,
        menu_id: int,
        current_user: User
    ):

    menu = await menu_repository.get_menu_by_id(db, menu_id)

    if not menu:

        logger.warning(
            "Menu item not found (menu_id=%s)",
            menu_id
        )

        raise MenuNotFoundError()

    restaurant = await menu_repository.get_restaurant_by_id(db, menu.restaurant_id)

    if not restaurant:

        logger.warning(
            "Menu item update failed: restaurant not found (restaurant_id=%s)",
            menu.restaurant_id
        )

        raise RestaurantNotFoundError()
    
    if (
        current_user.role != UserRole.ADMIN and
        restaurant.owner_id != current_user.id
    ):

        logger.warning(
            "Menu item update denied: user ID %s is not the restaurant owner",
            current_user.id
        )

        raise PermissionDeniedError()
    
    existing_menu = await menu_repository.get_menu_by_name(
        db,
        restaurant.id,
        menu_data.item_name
    )

    if existing_menu and existing_menu.id != menu.id:

        logger.warning(
            "Menu item already exists (restaurant_id=%s, item_name='%s')",
            restaurant.id,
            menu_data.item_name
        )

        raise MenuAlreadyExistsError()
    

    menu.item_name = menu_data.item_name
    menu.description = menu_data.description
    menu.price = menu_data.price


    try:

        await db.commit()

        await db.refresh(menu)

        logger.info(
            "Menu item updated successfully (menu_id=%s)",
            menu.id
        )

        return menu
    
    except IntegrityError:

        await db.rollback()

        logger.exception(
            "Database integrity error while updating menu item"
        )

        raise MenuAlreadyExistsError()
    
    except Exception:

        await db.rollback()

        logger.exception(
            "Unexpected error while updating menu item"
        )

        raise DatabaseError()
    
async def delete_menu_item(
        
        db: AsyncSession,
        menu_id: int,
        current_user: User
    ):

    menu = await menu_repository.get_menu_by_id(db, menu_id)

    if not menu:

        logger.warning(
            "Menu item not found (menu_id=%s)",
            menu_id
        )

        raise MenuNotFoundError()

    restaurant = await menu_repository.get_restaurant_by_id(
        db,
        menu.restaurant_id
    )

    if not restaurant:

        logger.warning(
            "Menu item deletion failed because the restaurant was not found"
        )
        raise RestaurantNotFoundError()
    
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
        
        logger.info(
            "Menu item deleted successfully (menu_id=%s)",
            menu.id
        )

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

    menu = await menu_repository.get_menu_by_id(db, menu_id)

    if not menu:

        logger.warning(
            "Menu item not found (menu_id=%s)",
            menu_id
        )

        raise MenuNotFoundError()
    
    restaurant = await menu_repository.get_restaurant_by_id(
        db,
        menu.restaurant_id
    )

    if not restaurant:

        logger.warning(
            "Menu status update failed: restaurant not found (restaurant_id=%s)",
            menu.restaurant_id
        )

        raise RestaurantNotFoundError()
    
    if (
        current_user.role != UserRole.ADMIN
        and
        restaurant.owner_id != current_user.id
    ):
        logger.warning(
            "Menu status update denied: user ID %s is not the restaurant owner",
            current_user.id
        )

        raise PermissionDeniedError()
    

    menu.status = status

    try:

        await db.commit()

        await db.refresh(menu)

        logger.info(
            "Menu status updated successfully (menu_id=%s, status=%s)",
            menu.id,
            status
        )
        
        return menu
    
    except Exception:

        await db.rollback()

        logger.exception("Unexpected error while changing menu item status")
        raise DatabaseError()
