from fastapi import APIRouter
from sqlalchemy import text

from app.db import engine
from app.core.logger import logger

router = APIRouter(tags=["HEALTH"])


@router.get(
    "/health",
    summary="Application health check",
    description=(
        "Verify application availability and database connectivity. "
        "Returns the current health status of the service."
    )
)
async def health_check():

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "message": "Service and database are operational"
        }

    except Exception as exc:
        logger.warning(
            "Health check failed: database connectivity unavailable (%s)",
            str(exc)
        )

        return {
            "status": "unhealthy",
            "database": "disconnected",
            "message": "Service is running but database connectivity failed"
        }