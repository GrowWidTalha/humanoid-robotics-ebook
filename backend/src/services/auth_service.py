"""Authentication service for user management and session handling

Provides user registration, authentication, password hashing,
JWT token generation, and session management.
"""
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
import hashlib
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.models.user import User
from src.models.session import Session
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Password hashing configuration
# Using Argon2 (modern, memory-hard algorithm) with bcrypt fallback for existing passwords
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# JWT configuration
ALGORITHM = "HS256"


class AuthService:
    """Authentication service for user and session management"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plain text password using Argon2

        Args:
            password: Plain text password (no length limitations with Argon2)

        Returns:
            Hashed password
        """
        # Argon2 is a modern, memory-hard hashing algorithm with no password length limits
        return pwd_context.hash(password, scheme="argon2")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to compare against

        Returns:
            True if password matches, False otherwise
        """
        # Passlib automatically handles both Argon2 and bcrypt hashes
        # Works with the hash that was used (supports password migration)
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def generate_jwt_token(user_id: UUID) -> str:
        """Generate a JWT token for a user

        Args:
            user_id: User's UUID

        Returns:
            JWT token string
        """
        expires_delta = timedelta(days=settings.session_expiry_days)
        expire = datetime.utcnow() + expires_delta

        to_encode = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.utcnow()
        }

        encoded_jwt = jwt.encode(
            to_encode,
            settings.better_auth_secret,
            algorithm=ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_jwt_token(token: str) -> Optional[dict]:
        """Decode and validate a JWT token

        Args:
            token: JWT token string

        Returns:
            Decoded token payload or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                settings.better_auth_secret,
                algorithms=[ALGORITHM]
            )
            return payload
        except JWTError as e:
            logger.warning(f"JWT decode error: {e}")
            return None

    @staticmethod
    def hash_token(token: str) -> str:
        """Create SHA-256 hash of a token for storage

        Args:
            token: Token to hash

        Returns:
            Hex digest of token hash
        """
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    async def create_user(
        db: AsyncSession,
        email: str,
        password: str
    ) -> User:
        """Create a new user account

        Args:
            db: Database session
            email: User's email address
            password: Plain text password

        Returns:
            Created User instance
        """
        password_hash = AuthService.hash_password(password)

        user = User(
            email=email.lower(),  # Normalize email to lowercase
            password_hash=password_hash
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        logger.info(f"User created: {user.id}")
        return user

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """Authenticate a user by email and password

        Args:
            db: Database session
            email: User's email address
            password: Plain text password

        Returns:
            User instance if authenticated, None otherwise
        """
        # Query user by email
        result = await db.execute(
            select(User).where(User.email == email.lower())
        )
        user = result.scalar_one_or_none()

        if user is None:
            logger.warning(f"Authentication failed: user not found for email {email}")
            return None

        if not AuthService.verify_password(password, user.password_hash):
            logger.warning(f"Authentication failed: invalid password for user {user.id}")
            return None

        logger.info(f"User authenticated: {user.id}")
        return user

    @staticmethod
    async def create_session(
        db: AsyncSession,
        user_id: UUID,
        token: str
    ) -> Session:
        """Create a new session for a user

        Args:
            db: Database session
            user_id: User's UUID
            token: JWT token string

        Returns:
            Created Session instance
        """
        token_hash = AuthService.hash_token(token)
        expires_at = datetime.utcnow() + timedelta(days=settings.session_expiry_days)

        session = Session(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at
        )

        db.add(session)
        await db.commit()
        await db.refresh(session)

        logger.info(f"Session created: {session.id} for user {user_id}")
        return session

    @staticmethod
    async def validate_session(
        db: AsyncSession,
        token: str
    ) -> Optional[Session]:
        """Validate a session token

        Args:
            db: Database session
            token: JWT token string

        Returns:
            Session instance if valid, None otherwise
        """
        token_hash = AuthService.hash_token(token)

        # Query session by token hash
        result = await db.execute(
            select(Session).where(Session.token_hash == token_hash)
        )
        session = result.scalar_one_or_none()

        if session is None:
            logger.warning("Session validation failed: session not found")
            return None

        if session.is_expired:
            logger.warning(f"Session validation failed: session {session.id} expired")
            return None

        return session

    @staticmethod
    async def revoke_session(
        db: AsyncSession,
        token: str
    ) -> bool:
        """Revoke a session by token

        Args:
            db: Database session
            token: JWT token string

        Returns:
            True if session was revoked, False otherwise
        """
        token_hash = AuthService.hash_token(token)

        result = await db.execute(
            delete(Session).where(Session.token_hash == token_hash)
        )
        await db.commit()

        revoked = result.rowcount > 0
        if revoked:
            logger.info(f"Session revoked for token hash {token_hash[:16]}...")

        return revoked

    @staticmethod
    async def cleanup_expired_sessions(db: AsyncSession) -> int:
        """Remove all expired sessions from database

        Args:
            db: Database session

        Returns:
            Number of sessions deleted
        """
        result = await db.execute(
            delete(Session).where(Session.expires_at < datetime.utcnow())
        )
        await db.commit()

        count = result.rowcount
        if count > 0:
            logger.info(f"Cleaned up {count} expired sessions")

        return count

    @staticmethod
    async def get_user_by_id(
        db: AsyncSession,
        user_id: UUID
    ) -> Optional[User]:
        """Get a user by ID

        Args:
            db: Database session
            user_id: User's UUID

        Returns:
            User instance if found, None otherwise
        """
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
