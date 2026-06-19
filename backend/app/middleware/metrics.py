from starlette.middleware.base import BaseHTTPMiddleware

from app.core import logger


REQUEST_COUNT = 0


class MetricsMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        global REQUEST_COUNT

        REQUEST_COUNT += 1

        response = await call_next(request)

        logger.info(
            "Total requests processed: %s",
            REQUEST_COUNT
        )

        return response