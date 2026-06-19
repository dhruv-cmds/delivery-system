from time import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.core import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time()

        response = await call_next(request)

        duration = round(
            (time() - start_time) * 1000,
            2
        )

        logger.info(
            "[user=%s role=%s] %s %s -> %s (%sms)",
            getattr(
                request.state,
                "user_id",
                None
            ),
            getattr(
                request.state,
                "role",
                None
            ),
            request.method,
            request.url.path,
            response.status_code,
            duration
        )

        return response