"""Input validation and sanitization utilities

Provides functions for validating and sanitizing user input to prevent
security vulnerabilities like XSS, SQL injection, and invalid data.
"""
import re
from typing import Optional
import bleach
from email_validator import validate_email, EmailNotValidError


# Allowed HTML tags and attributes for sanitized content
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote', 'code', 'pre', 'ul', 'ol', 'li', 'a'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'code': ['class'],
}


def sanitize_html(text: str, strip: bool = False) -> str:
    """Sanitize HTML content to prevent XSS attacks

    Args:
        text: Input text that may contain HTML
        strip: If True, strip all HTML tags instead of sanitizing

    Returns:
        Sanitized text safe for rendering
    """
    if strip:
        return bleach.clean(text, tags=[], strip=True)

    return bleach.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )


def validate_email_address(email: str) -> tuple[bool, Optional[str]]:
    """Validate email address format

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, normalized_email or None)
    """
    try:
        # Validate and normalize email
        email_info = validate_email(email, check_deliverability=False)
        return True, email_info.normalized
    except EmailNotValidError:
        return False, None


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """Validate password strength

    Requirements:
    - At least 8 characters
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message or None)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"

    return True, None


def sanitize_thread_id(thread_id: str) -> str:
    """Sanitize thread ID to prevent injection attacks

    Args:
        thread_id: Thread ID from user input

    Returns:
        Sanitized thread ID (alphanumeric, hyphens, underscores only)
    """
    # Remove any characters that aren't alphanumeric, hyphens, or underscores
    sanitized = re.sub(r"[^a-zA-Z0-9\-_]", "", thread_id)

    # Limit length to 255 characters
    return sanitized[:255]


def validate_content_length(content: str, max_length: int = 10000) -> tuple[bool, Optional[str]]:
    """Validate content length

    Args:
        content: Content to validate
        max_length: Maximum allowed length

    Returns:
        Tuple of (is_valid, error_message or None)
    """
    if not content or len(content.strip()) == 0:
        return False, "Content cannot be empty"

    if len(content) > max_length:
        return False, f"Content exceeds maximum length of {max_length} characters"

    return True, None
