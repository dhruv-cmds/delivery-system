from fastapi import FastAPI

from contextlib import asynccontextmanager

from sqlalchemy import text

from app.db import Base,engine

from app.api.routes import auth, users, health

from app.db.models import User,Restaurant,Payment,Order,OrderTracking,OrderItem,Notification,Menu,DeliveryPartner

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)

        # Create all tables again
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(health.router, tags=["Health"])