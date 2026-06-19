from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError

from app.core import setting


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        request.state.user_id = None
        request.state.role = None
        request.state.email = None

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):

            try:

                token = auth_header.replace(
                    "Bearer ",
                    ""
                )

                payload = jwt.decode(
                    token,
                    setting.SECRET_KEY,
                    algorithms=[setting.ALGORITHM],
                    issuer="delivery_api"
                )

                request.state.user_id = int(
                    payload.get("sub")
                )

                request.state.role = payload.get("role")

                request.state.email = payload.get("email")

            except JWTError:
                pass

        return await call_next(request)