"""Authentication middleware for protecting API endpoints

Provides dependency injection for current user authentication.
Validates JWT tokens from HTTP-only cookies and extracts user information.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db_session
from src.models.user import User
from src.services.auth_service import AuthService
from src.utils.logger import get_logger

logger = get_logger(__name__)

# HTTP Bearer scheme for Authorization header (optional fallback)
security = HTTPBearer(auto_error=False)


async def get_token_from_request(request: Request) -> Optional[str]:
    """Extract JWT token from cookie or Authorization header

    Args:
        request: FastAPI request object

    Returns:
        JWT token string or None
    """
    # First, try to get token from HTTP-only cookie
    token = request.cookies.get("auth_token")
    if token:
        return token

    # Fallback: try Authorization header (for API clients)
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]

    return None


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
) -> User:
    """Dependency to get the current authenticated user

    Validates JWT token from cookie/header and returns the associated user.
    Raises 401 Unauthorized if token is invalid or user not found.

    Args:
        request: FastAPI request object
        db: Database session

    Returns:
        Authenticated User instance

    Raises:
        HTTPException: 401 if authentication fails
    """
    # Extract token from request
    token = await get_token_from_request(request)

    if not token:
        logger.warning("Authentication failed: no token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Decode and validate JWT token
    payload = AuthService.decode_jwt_token(token)
    if not payload:
        logger.warning("Authentication failed: invalid JWT token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from token payload
    user_id_str = payload.get("sub")
    if not user_id_str:
        logger.warning("Authentication failed: no user_id in token payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Validate session still exists in database
    session = await AuthService.validate_session(db, token)
    if not session:
        logger.warning(f"Authentication failed: session not found or expired for token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    from uuid import UUID
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        logger.warning(f"Authentication failed: invalid user_id format: {user_id_str}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identifier",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await AuthService.get_user_by_id(db, user_id)
    if not user:
        logger.warning(f"Authentication failed: user {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.debug(f"User authenticated: {user.id}")
    return user


async def get_current_user_optional(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
) -> Optional[User]:
    """Optional authentication dependency

    Same as get_current_user but returns None instead of raising exception
    when no valid authentication is provided.

    Args:
        request: FastAPI request object
        db: Database session

    Returns:
        Authenticated User instance or None
    """
    try:
        return await get_current_user(request, db)
    except HTTPException:
        return None
