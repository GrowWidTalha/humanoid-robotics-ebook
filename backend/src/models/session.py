"""Session model for authentication token management

Represents an active authentication session with JWT tokens and expiration.
Aligns with data-model.md Session entity specification.
"""
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from src.config.database import Base


class Session(Base):
    """Session model for JWT token management

    Attributes:
        id: Unique session identifier (UUID)
        user_id: Foreign key to User
        token_hash: Hashed JWT token (unique)
        expires_at: Session expiration timestamp
        created_at: Session creation timestamp
    """

    __tablename__ = "sessions"

    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default="gen_random_uuid()"
    )
    user_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    token_hash = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(TIMESTAMP, nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, server_default="NOW()")

    # Relationships
    user = relationship("User", back_populates="sessions")

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})>"

    @property
    def is_expired(self) -> bool:
        """Check if session has expired"""
        return datetime.utcnow() > self.expires_at
