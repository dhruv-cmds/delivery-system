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

app = FastAPI(
    title="Food Delivery Management API",
    description=('''
        A complete food delivery backend system with authentication, restaurant management,
        menu management, order processing, payments, delivery tracking, notifications,
        and role-based access control.

        **Roles:** Admin, Customer, Restaurant Owner, Delivery Partner.
        '''
    ),
    
    version="1.0.0",

    # docs_url=None,
    # redoc_url=None,
    # openapi_url=None,

    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "AUTHENTICATION",
            "description": "User registration, login, and JWT authentication."
        },
        {
            "name": "USER",
            "description": "User profile lookup and user management endpoints."
        },
        {
            "name": "RESTAURANT",
            "description": "Restaurant creation, updates, status management, and deletion."
        },
        {
            "name": "PUBLIC RESTAURANT",
            "description": "Public restaurant information and restaurant discovery."
        },
        {
            "name": "MENU",
            "description": "Menu item creation, updates, availability management, and deletion."
        },
        {
            "name": "PUBLIC MENU",
            "description": "Public menu browsing and restaurant menu retrieval."
        },
        {
            "name": "ORDER",
            "description": "Order creation, status updates, retrieval, and cancellation."
        },
        {
            "name": "PAYMENT",
            "description": "Payment processing, payment lookup, and payment status management."
        },
        {
            "name": "MAKE PAYMENT",
            "description": "Payment creation."
        },
        {
            "name": "DELIVERY PARTNER",
            "description": "Delivery partner registration, profile management, and location updates."
        },
        {
            "name": "DELIVERY PARTNER PUBLIC",
            "description": "Public delivery partner information endpoints."
        },
        {
            "name": "NOTIFICATION",
            "description": "User notifications, read status management, and notification deletion."
        },
        {
            "name": "ADMIN NOTIFICATIONS",
            "description": "Administrative notification monitoring and user notification access."
        },
        {
            "name": "HEALTH",
            "description": "Application and database health monitoring endpoints."
        }
    ]

)

app.include_router(auth.router, prefix="/api")

app.include_router(delivery_partner.public_router, prefix="/api")
app.include_router(delivery_partner.router, prefix="/api")

app.include_router(health.router, prefix="/api")

app.include_router(menu.public_router, prefix="/api")
app.include_router(menu.router, prefix="/api")

app.include_router(notifications.routes, prefix="/api")
app.include_router(notifications.admin, prefix="/api")

app.include_router(orders.router, prefix="/api")

app.include_router(payment.make_payment_router, prefix="/api")
app.include_router(payment.router, prefix="/api")


app.include_router(restaurants.public_router, prefix="/api")
app.include_router(restaurants.router, prefix="/api")

app.include_router(users.router, prefix="/api")