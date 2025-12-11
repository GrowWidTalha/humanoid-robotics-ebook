"""Service for managing chat message persistence and retrieval.

Handles saving chat messages to the database and fetching chat history for users.
"""
from typing import List, Dict, Any, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func

from src.models.chat_message import ChatMessage, ChatUserRole
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ChatService:
    """Handles chat message data operations."""

    @staticmethod
    async def save_message(
        db: AsyncSession,
        user_id: UUID,
        thread_id: str,
        role: ChatUserRole,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ChatMessage:
        """
        Saves a chat message to the database.

        Args:
            db: The database session.
            user_id: The ID of the user sending/receiving the message.
            thread_id: The OpenAI thread ID this message belongs to.
            role: The role of the sender (user or assistant).
            content: The content of the message.
            metadata: Optional dictionary for additional message metadata.

        Returns:
            The created ChatMessage object.
        """
        if metadata is None:
            metadata = {}

        message = ChatMessage(
            user_id=user_id,
            thread_id=thread_id,
            role=role.value,  # Store enum value as string
            content=content,
            message_metadata=metadata
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        logger.info(f"Saved chat message (id={message.id}) to thread {thread_id}")
        return message

    @staticmethod
    async def get_chat_history(
        db: AsyncSession,
        user_id: UUID,
        thread_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[ChatMessage]:
        """
        Retrieves chat message history for a specific user and thread.

        Args:
            db: The database session.
            user_id: The ID of the user.
            thread_id: The OpenAI thread ID.
            limit: Maximum number of messages to retrieve.
            offset: Offset for pagination.

        Returns:
            A list of ChatMessage objects, ordered by creation time descending.
        """
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id, ChatMessage.thread_id == thread_id)
            .order_by(desc(ChatMessage.created_at))
            .limit(limit)
            .offset(offset)
        )
        messages = result.scalars().all()
        logger.info(f"Retrieved {len(messages)} messages for user {user_id} in thread {thread_id}")
        return messages

    @staticmethod
    async def get_user_threads(
        db: AsyncSession,
        user_id: UUID
    ) -> List[Dict[str, Any]]:
        """
        Retrieves a list of unique thread IDs for a given user, along with
        the last message timestamp and message count for each thread.

        Args:
            db: The database session.
            user_id: The ID of the user.

        Returns:
            A list of dictionaries, each containing 'thread_id', 'last_message_at',
            and 'message_count' for threads associated with the user.
        """
        # Select distinct thread_id, max(created_at) as last_message_at, count(*) as message_count
        # Group by thread_id
        result = await db.execute(
            select(
                ChatMessage.thread_id,
                func.max(ChatMessage.created_at).label("last_message_at"),
                func.count(ChatMessage.id).label("message_count")
            )
            .where(ChatMessage.user_id == user_id)
            .group_by(ChatMessage.thread_id)
            .order_by(desc(func.max(ChatMessage.created_at)))
        )
        # Convert Row objects to dictionaries
        threads = [
            {"thread_id": r.thread_id, "last_message_at": r.last_message_at, "message_count": r.message_count}
            for r in result.all()
        ]
        logger.info(f"Retrieved {len(threads)} threads for user {user_id}")
        return threads