"""Pydantic schemas for request/response validation

Provides type-safe data validation for API endpoints.
"""
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field, field_validator


# ============================================================================
# User Schemas
# ============================================================================

class UserCreate(BaseModel):
    """Schema for user registration request"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=128, description="User's password")

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets strength requirements"""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserLogin(BaseModel):
    """Schema for user login request"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, max_length=128, description="User's password")


class UserResponse(BaseModel):
    """Schema for user data in responses"""
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    """Schema for authentication response"""
    user: UserResponse
    message: str = "Authentication successful"


# ============================================================================
# Session Schemas
# ============================================================================

class SessionResponse(BaseModel):
    """Schema for session data in responses"""
    id: UUID
    user_id: UUID
    expires_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


# ============================================================================
# Chat Message Schemas
# ============================================================================

class ChatMessageCreate(BaseModel):
    """Schema for creating a new chat message"""
    message: str = Field(..., min_length=1, max_length=10000, description="User's message content")
    thread_id: Optional[str] = Field(None, min_length=1, max_length=255, description="OpenAI thread ID, optional for new threads")
    query_mode: Optional[str] = Field(None, description="Query mode: 'full_book' or 'selection'")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Selected text for context queries")

    @field_validator("query_mode")
    @classmethod
    def validate_query_mode(cls, v: Optional[str]) -> Optional[str]:
        """Validate query mode is one of allowed values"""
        if v is not None and v not in ["full_book", "selection"]:
            raise ValueError("query_mode must be 'full_book' or 'selection'")
        return v

    @field_validator("selected_text")
    @classmethod
    def validate_selected_text(cls, v: Optional[str], info: Any) -> Optional[str]:
        """Validate selected_text is present when query_mode is 'selection'"""
        if info.data.get("query_mode") == "selection" and not v:
            raise ValueError("selected_text is required when query_mode is 'selection'")
        return v


class ChatMessageResponse(BaseModel):
    """Schema for chat message in responses"""
    id: UUID
    user_id: UUID
    thread_id: str
    role: str
    content: str
    metadata: Dict[str, Any] = Field(..., alias="message_metadata") # Use alias for Pydantic V2
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }



class ChatResponse(BaseModel):
    """Schema for chat response with user and assistant messages"""
    user_message: ChatMessageResponse
    assistant_message: ChatMessageResponse
    thread_id: str


class ChatHistoryResponse(BaseModel):
    """Schema for thread history response"""
    messages: list[ChatMessageResponse]
    total: int
    thread_id: str


# ============================================================================
# Generic Response Schemas
# ============================================================================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
