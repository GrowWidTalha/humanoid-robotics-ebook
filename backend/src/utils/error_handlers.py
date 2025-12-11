"""Custom error handlers for user-friendly error messages.

Provides consistent, helpful error messages for common failure scenarios.
"""
from typing import Dict, Any, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from openai import APIStatusError, APITimeoutError, APIConnectionError
from qdrant_client.http.exceptions import UnexpectedResponse

from src.utils.logger import get_logger

logger = get_logger(__name__)


class ErrorMessages:
    """Centralized error message templates for user-friendly responses"""

    # Authentication errors
    SESSION_EXPIRED = "Your session has expired. Please log in again."
    INVALID_CREDENTIALS = "Invalid email or password. Please try again."
    UNAUTHORIZED = "You must be logged in to access this resource."
    ACCOUNT_EXISTS = "An account with this email already exists."

    # API errors
    API_TIMEOUT = "The service is taking longer than expected. Please try again."
    API_UNAVAILABLE = "The AI service is temporarily unavailable. Please try again in a few moments."
    API_RATE_LIMIT = "Too many requests. Please wait a moment before trying again."

    # Vector database errors
    VECTOR_DB_ERROR = "Unable to search book content. Please try again."
    NO_RESULTS = "No relevant content found for your question. Try rephrasing or asking something else."

    # Validation errors
    INVALID_INPUT = "Invalid input provided. Please check your data and try again."
    MESSAGE_TOO_LONG = "Your message is too long. Please keep it under 10,000 characters."
    SELECTED_TEXT_REQUIRED = "Please select some text first before asking a question about it."

    # Database errors
    DATABASE_ERROR = "A database error occurred. Please try again."
    CONNECTION_ERROR = "Unable to connect to the database. Please try again later."

    # Generic errors
    INTERNAL_ERROR = "An unexpected error occurred. Our team has been notified."
    NOT_FOUND = "The requested resource was not found."


def create_error_response(
    message: str,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """Create a standardized error response.

    Args:
        message: User-friendly error message
        status_code: HTTP status code
        details: Optional additional error details (for debugging)

    Returns:
        JSONResponse with error information
    """
    content = {
        "error": True,
        "message": message,
        "status_code": status_code
    }

    if details:
        content["details"] = details

    return JSONResponse(
        status_code=status_code,
        content=content
    )


async def openai_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle OpenAI API errors with user-friendly messages.

    Args:
        request: The request that caused the error
        exc: The exception that was raised

    Returns:
        JSONResponse with user-friendly error
    """
    if isinstance(exc, APIStatusError):
        if exc.status_code == 429:
            logger.warning(f"OpenAI rate limit hit for {request.url.path}")
            return create_error_response(
                ErrorMessages.API_RATE_LIMIT,
                status.HTTP_429_TOO_MANY_REQUESTS,
                {"retry_after": exc.response.headers.get("Retry-After", "60")}
            )
        elif exc.status_code >= 500:
            logger.error(f"OpenAI server error: {exc.message}")
            return create_error_response(
                ErrorMessages.API_UNAVAILABLE,
                status.HTTP_503_SERVICE_UNAVAILABLE
            )
        else:
            logger.error(f"OpenAI API error ({exc.status_code}): {exc.message}")
            return create_error_response(
                ErrorMessages.API_UNAVAILABLE,
                status.HTTP_502_BAD_GATEWAY
            )

    elif isinstance(exc, APITimeoutError):
        logger.warning(f"OpenAI API timeout for {request.url.path}")
        return create_error_response(
            ErrorMessages.API_TIMEOUT,
            status.HTTP_504_GATEWAY_TIMEOUT
        )

    elif isinstance(exc, APIConnectionError):
        logger.error(f"OpenAI connection error: {exc}")
        return create_error_response(
            ErrorMessages.API_UNAVAILABLE,
            status.HTTP_503_SERVICE_UNAVAILABLE
        )

    # Default OpenAI error
    logger.error(f"Unexpected OpenAI error: {exc}")
    return create_error_response(
        ErrorMessages.INTERNAL_ERROR,
        status.HTTP_500_INTERNAL_SERVER_ERROR
    )


async def qdrant_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle Qdrant errors with user-friendly messages.

    Args:
        request: The request that caused the error
        exc: The exception that was raised

    Returns:
        JSONResponse with user-friendly error
    """
    if isinstance(exc, UnexpectedResponse):
        logger.error(f"Qdrant error for {request.url.path}: {exc}")
        return create_error_response(
            ErrorMessages.VECTOR_DB_ERROR,
            status.HTTP_503_SERVICE_UNAVAILABLE
        )

    logger.error(f"Unexpected Qdrant error: {exc}")
    return create_error_response(
        ErrorMessages.VECTOR_DB_ERROR,
        status.HTTP_500_INTERNAL_SERVER_ERROR
    )


async def validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle validation errors with user-friendly messages.

    Args:
        request: The request that caused the error
        exc: The exception that was raised

    Returns:
        JSONResponse with user-friendly error
    """
    from pydantic import ValidationError

    if isinstance(exc, ValidationError):
        # Extract field-specific errors
        errors = []
        for error in exc.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            errors.append(f"{field}: {message}")

        logger.warning(f"Validation error for {request.url.path}: {errors}")
        return create_error_response(
            ErrorMessages.INVALID_INPUT,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {"validation_errors": errors}
        )

    return create_error_response(
        ErrorMessages.INVALID_INPUT,
        status.HTTP_400_BAD_REQUEST
    )
