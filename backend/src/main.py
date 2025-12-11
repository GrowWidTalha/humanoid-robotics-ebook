"""FastAPI application entry point

Main application setup with middleware, CORS, and route configuration.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
# Temporarily disabled for debugging
from secure import Secure

# Secure middleware configuration
# Temporarily disabled for debugging
secure_headers = Secure()
from fastapi.responses import JSONResponse
# Temporarily disabled for debugging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.config.settings import settings
from src.config.database import init_qdrant_collection, close_database_connections
from src.utils.logger import setup_logging, get_logger
from src.api.routes import health, auth, chat

# Setup logging
setup_logging(
    level=settings.log_level,
    use_json=settings.is_production
)

logger = get_logger(__name__)


# Rate limiter configuration (using the one from rate_limit middleware)
# limiter = Limiter(
#     key_func=get_remote_address,
#     default_limits=[f"{settings.rate_limit_per_minute}/minute"]
# )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting up application...")
    logger.info(f"Environment: {settings.environment}")

    # Initialize Qdrant collection
    try:
        await init_qdrant_collection()
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant collection: {e}")

    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Shutting down application...")
    await close_database_connections()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot for humanoid robotics textbook",
    version="1.0.0",
    docs_url="/api/docs" if not settings.is_production else None,
    redoc_url="/api/redoc" if not settings.is_production else None,
    lifespan=lifespan
)

# Temporarily disabled for debugging
from src.api.middleware.logging_middleware import LoggingMiddleware
from src.api.middleware.rate_limit import limiter, rate_limit_exceeded_handler

# Add rate limiter to app state
# Temporarily disabled for debugging
# app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Add logging middleware
# Temporarily disabled due to middleware stack build error
app.add_middleware(LoggingMiddleware)

# Add secure headers middleware
# Temporarily disabled for debugging
@app.middleware("http")
async def secure_headers_middleware(request: Request, call_next):
    response = await call_next(request)

    try:
        # If the Secure instance exposes an integration helper named "framework"
        # that supports FastAPI/Starlette, use it.
        if getattr(secure_headers, "framework", None) is not None:
            fw = secure_headers.framework
            # defensive: some versions expose attributes differently
            if hasattr(fw, "fastapi"):
                fw.fastapi(response)
            elif hasattr(fw, "starlette"):
                fw.starlette(response)
            else:
                # fallback to a generic method if one exists
                if hasattr(secure_headers, "apply"):
                    secure_headers.apply(response)
                elif hasattr(secure_headers, "add"):
                    secure_headers.add(response)
                else:
                    raise AttributeError("Secure instance has no recognized integration methods")
        else:
            # library not integrated or missing; apply safe default headers manually
            # These are conservative, common security headers.
            response.headers.setdefault("X-Content-Type-Options", "nosniff")
            response.headers.setdefault("X-Frame-Options", "DENY")
            response.headers.setdefault("Referrer-Policy", "no-referrer")
            response.headers.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
            response.headers.setdefault("Permissions-Policy", "geolocation=()")
            response.headers.setdefault("X-XSS-Protection", "1; mode=block")
    except Exception:
        # log the failure but do not crash the request pipeline
        logger.exception("Failed to apply secure headers")

    return response

# CORS middleware configuration
# Temporarily disabled for debugging
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled errors

    Args:
        request: FastAPI request
        exc: Exception that was raised

    Returns:
        JSONResponse with error details
    """
    logger.error(
        f"Unhandled exception: {exc}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "client": request.client.host if request.client else "unknown"
        }
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred" if settings.is_production else str(exc)
        }
    )


# Include routers
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


# Root endpoint
@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """Root endpoint

    Returns:
        Welcome message
    """
    return {
        "message": "RAG Chatbot API",
        "status": "running",
        "docs": "/api/docs" if not settings.is_production else "disabled"
    }
