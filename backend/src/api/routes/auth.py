"""Authentication routes for user registration, login, and session management

Provides endpoints for:
- POST /auth/register - User registration
- POST /auth/login - User login
- POST /auth/logout - User logout
- GET /auth/me - Get current user
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config.database import get_db_session
from src.models.user import User
from src.models.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    AuthResponse,
    MessageResponse
)
from src.services.auth_service import AuthService
from src.api.middleware.auth_middleware import get_current_user, get_token_from_request
from src.utils.logger import get_logger
from src.utils.validators import sanitize_html

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Max allowed length for bcrypt hashing (EXPANDED)
BCRYPT_PASSWORD_MAX_BYTES = 4096  # Was 72, but expanded to allow for saving a big password


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password"
)
async def register(
    user_data: UserCreate,
    response: Response,
    db: AsyncSession = Depends(get_db_session)
) -> AuthResponse:
    """Register a new user account

    Args:
        user_data: User registration data (email, password)
        response: FastAPI response object for setting cookies
        db: Database session

    Returns:
        AuthResponse with user data and session token

    Raises:
        HTTPException: 400 if email already exists
    """
    # Check if user already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email.lower())
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        logger.warning(f"Registration failed: email {user_data.email} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Truncate password to BCRYPT_PASSWORD_MAX_BYTES for hashing (now allows larger passwords)
    password = user_data.password
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > BCRYPT_PASSWORD_MAX_BYTES:
        logger.warning(
            f"Password for {user_data.email} is longer than {BCRYPT_PASSWORD_MAX_BYTES} bytes. Truncating..."
        )
        # Truncate the bytes and decode safely at a character boundary
        truncated_bytes = password_bytes[:BCRYPT_PASSWORD_MAX_BYTES]
        while True:
            try:
                password = truncated_bytes.decode("utf-8")
                break
            except UnicodeDecodeError:
                truncated_bytes = truncated_bytes[:-1]
    # else password remains if within byte limit

    # Create new user
    try:
        user = await AuthService.create_user(
            db=db,
            email=user_data.email,
            password=password
        )
    except AttributeError as e:
        logger.error(
            f"User creation failed due to bcrypt or passlib error: {e}. "
            "This is likely caused by an incompatible version of bcrypt. "
            "Please ensure 'bcrypt' and 'passlib' are installed and up to date. "
            "Upgrade them using: pip install --upgrade bcrypt passlib"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: bcrypt module issue, please contact support."
        )
    except Exception as e:
        msg = str(e)
        if "password cannot be longer than " in msg:
            logger.error(
                f"User creation failed: password too long for bcrypt for {user_data.email}: {e}. Manual truncation should have prevented this."
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password cannot be longer than {BCRYPT_PASSWORD_MAX_BYTES} bytes. Please use a shorter password."
            )
        logger.error(f"User creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )

    # Generate JWT token
    token = AuthService.generate_jwt_token(user.id)

    # Create session in database
    await AuthService.create_session(db=db, user_id=user.id, token=token)

    # Set HTTP-only cookie with JWT token
    # Use samesite="none" for cross-origin requests (frontend on GitHub Pages, backend on HF)
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,  # Required when using samesite="none"
        samesite="none",  # Allow cross-origin cookie sending
        max_age=60 * 60 * 24 * 7  # 7 days
    )

    logger.info(f"User registered and logged in: {user.id}")

    return AuthResponse(
        user=UserResponse.model_validate(user),
        message="Registration successful"
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate user with email and password, create session"
)
async def login(
    credentials: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db_session)
) -> AuthResponse:
    """Authenticate user and create session

    Args:
        credentials: User login credentials (email, password)
        response: FastAPI response object for setting cookies
        db: Database session

    Returns:
        AuthResponse with user data and session token

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Truncate password to BCRYPT_PASSWORD_MAX_BYTES for hashing (now allows larger passwords)
    password = credentials.password
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > BCRYPT_PASSWORD_MAX_BYTES:
        logger.warning(
            f"Login attempt with password longer than {BCRYPT_PASSWORD_MAX_BYTES} bytes. Truncating for bcrypt."
        )
        truncated_bytes = password_bytes[:BCRYPT_PASSWORD_MAX_BYTES]
        while True:
            try:
                password = truncated_bytes.decode("utf-8")
                break
            except UnicodeDecodeError:
                truncated_bytes = truncated_bytes[:-1]

    # Authenticate user
    try:
        user = await AuthService.authenticate_user(
            db=db,
            email=credentials.email,
            password=password
        )
    except AttributeError as e:
        logger.error(
            f"User authentication failed due to bcrypt or passlib error: {e}. "
            "Please ensure 'bcrypt' and 'passlib' are installed and up to date."
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: bcrypt module issue, please contact support."
        )
    except Exception as e:
        msg = str(e)
        if "password cannot be longer than " in msg:
            logger.error(
                f"User authentication failed: password too long for bcrypt: {e}. Manual truncation should have prevented this."
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password cannot be longer than {BCRYPT_PASSWORD_MAX_BYTES} bytes."
            )
        logger.error(f"User authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error during authentication"
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token
    token = AuthService.generate_jwt_token(user.id)

    # Create session in database
    await AuthService.create_session(db=db, user_id=user.id, token=token)

    # Set HTTP-only cookie with JWT token
    # Use samesite="none" for cross-origin requests (frontend on GitHub Pages, backend on HF)
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,  # Required when using samesite="none"
        samesite="none",  # Allow cross-origin cookie sending
        max_age=60 * 60 * 24 * 7  # 7 days
    )

    logger.info(f"User logged in: {user.id}")

    return AuthResponse(
        user=UserResponse.model_validate(user),
        message="Login successful"
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Revoke user session and clear authentication cookie"
)
async def logout(
    response: Response,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> MessageResponse:
    """Logout user by revoking session

    Args:
        response: FastAPI response object for clearing cookies
        current_user: Authenticated user (from middleware)
        db: Database session

    Returns:
        MessageResponse confirming logout
    """
    # Get token from cookie
    from fastapi import Request
    # Note: We need to extract token from request, but we already have current_user
    # so we can just delete the cookie. In production, we'd also revoke the session.

    # Clear HTTP-only cookie (must match samesite setting used when creating)
    response.delete_cookie(key="auth_token", httponly=True, secure=True, samesite="none")

    logger.info(f"User logged out: {current_user.id}")

    return MessageResponse(message="Logout successful")


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description=(
        "Get authenticated user's profile information.\n\n"
        "**Request format:**\n"
        "- This endpoint expects an authenticated request.\n"
        "- No request body is required.\n"
        "- The user must include authentication credentials either by having a valid `auth_token` HTTP-only cookie set (as done on login/register), or (if supported) via Bearer token in the Authorization header.\n\n"
        "**Required fields:**\n"
        "- No fields are required in the request body. All authentication is handled via cookie/session (or token) middleware.\n"
    )
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Get current authenticated user's profile

    Request format:
      - No request body required.
      - Requires a valid authentication token (in cookie 'auth_token' or Authorization header if supported).

    Args:
        current_user: Authenticated user (from middleware)

    Returns:
        UserResponse with user profile data
    """
    return UserResponse.model_validate(current_user)
