# src/api/middleware/rate_limit.py
from typing import Callable
from fastapi import Request
from fastapi.responses import JSONResponse
import inspect

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

def get_user_identifier(request: Request) -> str:
    user = getattr(request.state, "user", None)
    if user:
        return f"user:{user.id}"
    return f"ip:{get_remote_address(request)}"

# Create limiter instance (single authoritative limiter in this module)
limiter = Limiter(
    key_func=get_user_identifier,
    default_limits=[f"{settings.rate_limit_per_minute}/minute"],
    storage_uri=settings.redis_url,
    strategy="fixed-window"
)

async def rate_limit_dependency(request: Request):
    """
    FastAPI dependency to apply default rate limiting.

    This wraps a small noop handler with the limiter decorator and calls it.
    That keeps the decorator semantics without passing Request into the decorator.
    """
    # decorator that would normally be used on a route
    decorator = limiter.limit(f"{settings.rate_limit_per_minute}/minute")

    # a tiny handler the decorator can wrap
    async def _noop(req: Request):
        return None

    wrapped = decorator(_noop)  # now wrapped is a callable handler

    # call the wrapped handler with the request; handle whether it is awaitable
    result = wrapped(request)
    if inspect.isawaitable(result):
        await result

    # dependency returns truthy so route proceeds
    return True


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    identifier = get_user_identifier(request)
    logger.warning(f"Rate limit exceeded for {identifier}")

    # Try to parse retry after defensively
    retry_after = 60
    try:
        # exc.detail sometimes contains text like "Retry after 60 seconds"
        if isinstance(exc.detail, str) and "Retry after" in exc.detail:
            parts = exc.detail.split("Retry after")
            if len(parts) > 1:
                retry_after = int(''.join(filter(str.isdigit, parts[1])) or 60)
    except Exception:
        retry_after = 60

    payload = {
        "error": "rate_limit_exceeded",
        "message": f"Too many requests. Please try again in {retry_after} seconds.",
        "retry_after": int(retry_after)
    }

    return JSONResponse(status_code=429, content=payload, headers={"Retry-After": str(retry_after)})
