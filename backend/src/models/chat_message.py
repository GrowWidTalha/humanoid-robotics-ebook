"""Chat message model for storing conversation history

Represents a single question-answer exchange in the chatbot.
Aligns with data-model.md ChatMessage entity specification.
"""
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy.orm import relationship

from src.config.database import Base


class ChatUserRole(str, Enum):
    """Enum for the role of the chat message sender."""
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(Base):
    """ChatMessage model for storing conversation history

    Attributes:
        id: Unique message identifier (UUID)
        user_id: Foreign key to User
        thread_id: OpenAI Agents SDK thread identifier
        role: Message sender (user or assistant)
        content: Message text content
        metadata: Additional context (JSONB)
        created_at: Message creation timestamp
    """

    __tablename__ = "chat_messages"

    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default="gen_random_uuid()"
    )
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    thread_id = Column(String(255), nullable=False)
    role = Column(String(10), nullable=False) # CHECK (role IN ('user', 'assistant')) will be added in migration
    content = Column(Text, nullable=False)
    message_metadata = Column('metadata', JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, server_default="NOW()")

    # Relationships
    user = relationship("User", back_populates="chat_messages")

    def __repr__(self) -> str:
        return f"<ChatMessage(id={self.id}, role={self.role}, thread_id={self.thread_id})>"