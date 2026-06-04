from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import (

    OrderItemCreate,
    OrderItemResponse,   
    OrderCreate,
    OrderResponse,
)

from app.db.models import order_item, order, order_tracking

from app.core import limiter

from app.api import (
    get_db,
    get_current_user,
    get_access_manager,
    get_order_manager
)

router = APIRouter(
        tags=["Menu"],
        dependencies=[Depends(get_current_user)]
    )

public_router = APIRouter(tags=["Menu"])

@router.post(
        "/order",
        response_model=OrderResponse,
        summary="Create order",
        description="chat gpt add here"
)
@limiter.limit("3/second")
async def create_order(
        request: Request,
        order_data: OrderCreate,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):

