"""Chat message endpoints for interacting with the RAG chatbot.

Provides endpoints for:
- POST /chat/message - Send a new message to the chatbot, get a RAG-powered response
- GET /chat/history - Get chat history for a specific thread
- GET /chat/threads - Get a list of user's chat threads
"""
from typing import List, Dict, Any
from uuid import UUID, uuid4
import time
import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from openai import OpenAIError, APITimeoutError, APIConnectionError, APIStatusError

from src.api.middleware.auth_middleware import get_current_user
# from src.api.middleware.rate_limit import rate_limit_dependency
from src.config.database import get_db_session
from src.models.user import User
from src.models.schemas import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatResponse,
    ChatHistoryResponse
)
from src.models.chat_message import ChatUserRole, ChatMessage
from src.services.chat_service import ChatService
from src.services.rag_service import RAGService
from src.services.vector_service import VectorService
from src.utils.validators import sanitize_html
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.post(
    "/message",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Send message to chatbot",
    description="Send a message to the RAG chatbot and get a response based on book content"
)
async def send_message(
    chat_message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
    # rate_limit_status: Dict[str, Any] = Depends(rate_limit_dependency)
) -> ChatResponse:
    """Send a message to the RAG chatbot.

    Handles full-book queries and selected-text queries.
    Retrieves context from Qdrant, generates response using RAG service,
    and persists both user and assistant messages to the database.
    """
    start_time = time.time()
    user_id = current_user.id
    query_mode = chat_message_data.query_mode or "full_book"
    user_message_content = sanitize_html(chat_message_data.message, strip=True)
    selected_text_content = sanitize_html(chat_message_data.selected_text, strip=True) if chat_message_data.selected_text else None

    # Determine thread_id: create new if not provided (simple UUID for conversation grouping)
    thread_id = chat_message_data.thread_id if chat_message_data.thread_id else str(uuid4())
    logger.info(f"Processing message for user {user_id}, thread {thread_id}")

    # 1. Save user message to DB
    user_message_db = await ChatService.save_message(
        db=db,
        user_id=user_id,
        thread_id=thread_id,
        role=ChatUserRole.USER,
        content=user_message_content,
        metadata={
            "query_mode": query_mode,
            "selected_text": selected_text_content
        }
    )

    # 2 & 3. Run vector search and chat history retrieval in parallel for speed
    try:
        # Prepare vector search task
        if query_mode == "selection" and not selected_text_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="selected_text is required for 'selection' query mode"
            )

        # Determine search parameters
        search_text = selected_text_content if query_mode == "selection" else user_message_content
        top_k = 3 if query_mode == "selection" else 5

        # Run both operations in parallel
        context_chunks, chat_history = await asyncio.gather(
            VectorService.search_similar_chunks(query_text=search_text, top_k=top_k),
            ChatService.get_chat_history(db=db, user_id=user_id, thread_id=thread_id, limit=10)
        )

        # Convert history to dict format for RAG service
        history_dicts = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(chat_history)  # Reverse to chronological order
        ]

    except HTTPException:
        raise  # Re-raise validation errors
    except Exception as e:
        logger.error(f"Error retrieving context or history: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve relevant book content. Please try again."
        )

    # 4. Generate response using RAG service with Agents SDK
    try:
        rag_response = await RAGService.generate_response(
            user_message=user_message_content,
            context_chunks=context_chunks,
            chat_history=history_dicts,
            query_mode=query_mode,
            selected_text=selected_text_content
        )
        assistant_message_content = rag_response["content"]
        chunk_ids = rag_response["chunk_ids"]
        model_used = rag_response["model_used"]

    except APIStatusError as e:
        logger.error(f"OpenAI API error (status: {e.status_code}): {e.message}")
        if e.status_code == 429:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="OpenAI API rate limit exceeded. Please try again shortly."
            )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OpenAI API error: {e.message}"
        )
    except APITimeoutError as e:
        logger.error(f"OpenAI API timeout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="OpenAI API timed out. Please try again."
        )
    except APIConnectionError as e:
        logger.error(f"OpenAI API connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not connect to OpenAI API. Please check your internet connection or try again later."
        )
    except Exception as e:
        logger.error(f"Generic error from RAG service: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate response from chatbot. Please try again."
        )

    # Calculate response time
    response_time_ms = int((time.time() - start_time) * 1000)

    # 5. Save assistant message to DB
    assistant_message_db = await ChatService.save_message(
        db=db,
        user_id=user_id,
        thread_id=thread_id,
        role=ChatUserRole.ASSISTANT,
        content=assistant_message_content,
        metadata={
            "query_mode": query_mode,
            "selected_text_context": selected_text_content if query_mode == "selection" else None,
            "chunk_ids": chunk_ids,
            "model_used": model_used,
            "response_time_ms": response_time_ms
        }
    )

    logger.info(f"Chat response generated for user {user_id} in thread {thread_id} ({response_time_ms}ms)")

    return ChatResponse(
        user_message=ChatMessageResponse.model_validate(user_message_db),
        assistant_message=ChatMessageResponse.model_validate(assistant_message_db),
        thread_id=thread_id
    )


@router.get(
    "/history",
    response_model=ChatHistoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get chat history",
    description="Retrieve paginated chat message history for a specific thread"
)
async def get_chat_history(
    thread_id: str,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> ChatHistoryResponse:
    """Retrieve chat history for a specific thread.

    Args:
        thread_id: The ID of the conversation thread.
        limit: The maximum number of messages to return.
        offset: The number of messages to skip for pagination.
        current_user: The authenticated user.
        db: The database session.

    Returns:
        ChatHistoryResponse containing messages and total count.
    """
    user_id = current_user.id

    messages_db = await ChatService.get_chat_history(
        db=db,
        user_id=user_id,
        thread_id=thread_id,
        limit=limit,
        offset=offset
    )

    # Convert to Pydantic models
    messages_response = [ChatMessageResponse.model_validate(msg) for msg in messages_db]

    # Get total count for pagination metadata
    total_messages = await db.scalar(
        select(func.count(ChatMessage.id))
        .where(ChatMessage.user_id == user_id, ChatMessage.thread_id == thread_id)
    )

    logger.info(f"Retrieved chat history for user {user_id}, thread {thread_id}")

    return ChatHistoryResponse(
        messages=messages_response,
        total=total_messages if total_messages is not None else 0,
        thread_id=thread_id
    )


@router.get(
    "/threads",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Get user chat threads",
    description="Retrieve a list of all chat threads for the authenticated user"
)
async def get_user_chat_threads(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> List[Dict[str, Any]]:
    """Retrieve a list of chat threads for the authenticated user.

    Args:
        current_user: The authenticated user.
        db: The database session.

    Returns:
        A list of dictionaries, each representing a thread summary.
    """
    user_id = current_user.id
    threads = await ChatService.get_user_threads(db=db, user_id=user_id)
    logger.info(f"Retrieved {len(threads)} chat threads for user {user_id}")
    return threads
