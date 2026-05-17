from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

from core.security import verify_access_token

class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # Allow preflight requests
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path.rstrip("/")

        public_routes = [
            "",
            "/signin",
            "/signup",
            "/auth/google",
            "/health"
        ]

        if path in public_routes:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"}
            )

        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token format"}
            )

        token = auth_header.split(" ")[1]

        id = verify_access_token(token)

        if not id:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"}
            )

        request.state.id = id

        return await call_next(request)