from fastapi import FastAPI

from contextlib import asynccontextmanager

from sqlalchemy import text

from app.db import Base,engine

from app.api.routes import (
    auth,
    delivery_partner,
    health,
    menu,
    notifications,
    orders,
    payment,
    restaurants,
    users,
)

from app.db.models import (
    User, 
    Restaurant, 
    Payment, 
    Order, 
    OrderTracking, 
    OrderItem, 
    Notification, 
    Menu, 
    DeliveryPartner
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:

        # Create all tables again
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/api")

app.include_router(health.router, prefix="/api")

app.include_router(menu.router, prefix="/api")
app.include_router(menu.public_router, prefix="/api")

app.include_router(orders.router, prefix="/api")

app.include_router(restaurants.router, prefix="/api")

app.include_router(users.router, prefix="/api")