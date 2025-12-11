"""Service for RAG operations using OpenAI Agents SDK.

Integrates with OpenAI Agents SDK to create agents and generate
responses using retrieved context chunks from the vector database.
"""
from typing import List, Dict, Any, Optional
import asyncio
from openai import AsyncOpenAI, APIStatusError, APITimeoutError
from agents import Agent, Runner, ModelSettings, set_default_openai_client

from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Retry configuration
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 10  # seconds

# Initialize OpenAI client for Agents SDK
openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
set_default_openai_client(openai_client, use_for_tracing=True)


class RAGService:
    """Handles RAG operations with OpenAI Agents SDK."""

    @staticmethod
    async def _run_with_retry(agent: Agent, prompt: str, max_retries: int = MAX_RETRIES):
        """Run agent with exponential backoff retry logic.

        Args:
            agent: The agent to run
            prompt: The prompt to send
            max_retries: Maximum number of retry attempts

        Returns:
            The agent result

        Raises:
            Exception: If all retries fail
        """
        retry_delay = INITIAL_RETRY_DELAY
        last_exception = None

        for attempt in range(max_retries):
            try:
                result = await Runner.run(agent, prompt)
                if attempt > 0:
                    logger.info(f"OpenAI API call succeeded on attempt {attempt + 1}")
                return result

            except APIStatusError as e:
                last_exception = e
                # Handle rate limits with Retry-After header
                if e.status_code == 429:
                    retry_after = e.response.headers.get('Retry-After')
                    if retry_after:
                        try:
                            retry_delay = int(retry_after)
                        except ValueError:
                            pass

                    if attempt < max_retries - 1:
                        logger.warning(f"Rate limit hit (429), retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, MAX_RETRY_DELAY)
                        continue
                    else:
                        logger.error(f"Rate limit exhausted after {max_retries} attempts")
                        raise
                else:
                    # Non-retryable status error
                    raise

            except APITimeoutError as e:
                last_exception = e
                if attempt < max_retries - 1:
                    logger.warning(f"API timeout, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, MAX_RETRY_DELAY)
                    continue
                else:
                    logger.error(f"API timeout after {max_retries} attempts")
                    raise

            except Exception as e:
                # For other exceptions, don't retry
                logger.error(f"Non-retryable error: {e}")
                raise

        # If we get here, all retries failed
        raise last_exception

    @staticmethod
    def _build_context(context_chunks: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved chunks.

        Args:
            context_chunks: List of chunks with 'content' and metadata

        Returns:
            Formatted context string
        """
        if not context_chunks:
            return "No relevant context found in the book."

        context_parts = []
        for idx, chunk in enumerate(context_chunks, 1):
            content = chunk.get('content', '')
            chapter = chunk.get('chapter', 'Unknown')
            section = chunk.get('section', 'Unknown')
            context_parts.append(
                f"[Source {idx}] {chapter} - {section}:\n{content}\n"
            )

        return "\n".join(context_parts)

    @staticmethod
    def _build_messages(
        user_message: str,
        context: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        query_mode: str = "full_book",
        selected_text: Optional[str] = None
    ) -> str:
        """Build the complete prompt with context and history.

        Args:
            user_message: The user's question
            context: Retrieved context from vector database
            chat_history: Previous messages (list of {"role": ..., "content": ...})
            query_mode: "full_book" or "selection"
            selected_text: Selected text if in selection mode

        Returns:
            Complete prompt string
        """
        if query_mode == 'selection' and selected_text:
            prompt = (
                f"The user has selected the following text from the book:\n"
                f'"""{selected_text}"""\n\n'
                f"User's question about the selected text: {user_message}\n\n"
                f"Additional relevant context from the book:\n{context}\n\n"
                f"Please answer the question based primarily on the selected text, "
                f"using the additional context only if needed for clarification."
            )
        else:
            prompt = (
                f"User's question: {user_message}\n\n"
                f"Relevant context from the Humanoid Robotics book:\n{context}\n\n"
                f"Please provide a comprehensive answer based on the context above. "
                f"If the context doesn't contain enough information to fully answer "
                f"the question, acknowledge this limitation."
            )

        # Add chat history context if available
        if chat_history and len(chat_history) > 0:
            history_str = "\n".join([
                f"{msg['role'].title()}: {msg['content']}"
                for msg in chat_history[-5:]  # Last 5 messages for context
            ])
            prompt = f"Previous conversation:\n{history_str}\n\n{prompt}"

        return prompt

    @staticmethod
    async def generate_response(
        user_message: str,
        context_chunks: List[Dict[str, Any]],
        chat_history: Optional[List[Dict[str, str]]] = None,
        query_mode: str = "full_book",
        selected_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a response using OpenAI Agents SDK.

        Args:
            user_message: The user's question
            context_chunks: Retrieved context chunks from Qdrant
            chat_history: Previous conversation messages
            query_mode: "full_book" or "selection"
            selected_text: Text selected by user (if query_mode is "selection")

        Returns:
            Dictionary with:
                - content: The assistant's response text
                - chunk_ids: List of chunk IDs used for context
                - model_used: The model name
        """
        try:
            # Build context from chunks
            context_text = RAGService._build_context(context_chunks)

            # Build complete prompt
            prompt = RAGService._build_messages(
                user_message=user_message,
                context=context_text,
                chat_history=chat_history,
                query_mode=query_mode,
                selected_text=selected_text
            )

            # Create agent with instructions for answering book questions
            agent = Agent(
                name="Humanoid Robotics Assistant",
                instructions=(
                    "You are a knowledgeable assistant for a humanoid robotics textbook. "
                    "Provide clear, concise answers based on the book content. "
                    "Cite sources when relevant."
                ),
                model=settings.chat_model,
                model_settings=ModelSettings(
                    temperature=0.7,
                    max_tokens=500  # Reduced for faster responses
                )
            )

            # Run the agent with the prompt (with retry logic)
            logger.info(f"Generating response for: '{user_message[:50]}...'")
            result = await RAGService._run_with_retry(agent, prompt)

            # Extract chunk IDs for metadata
            chunk_ids = [
                chunk.get('id', f"chunk_{idx}")
                for idx, chunk in enumerate(context_chunks)
            ]

            response_content = result.final_output if hasattr(result, 'final_output') else str(result)

            logger.info(f"Generated response ({len(response_content)} chars)")

            return {
                "content": response_content,
                "chunk_ids": chunk_ids,
                "model_used": settings.chat_model
            }

        except Exception as e:
            logger.error(f"Error generating RAG response: {e}", exc_info=True)
            raise
