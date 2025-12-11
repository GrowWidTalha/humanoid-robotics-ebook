"""Application settings and configuration

Loads environment variables and provides type-safe configuration.
"""
from typing import List, Union, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from openai import AsyncOpenAI


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Database
    database_url: str

    # Qdrant Vector Database
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "humanoid-robotics-book-v1"
    vector_size: int = 1536  # OpenAI text-embedding-3-small dimension

    # OpenAI
    openai_api_key: str
    openai_embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"  # Fast, cost-effective model for chat (was gpt-4-turbo-preview)

    # Authentication
    better_auth_secret: str
    session_expiry_days: int = 7

    # Rate Limiting
    rate_limit_per_minute: int = 20
    redis_url: str = "redis://localhost:6379"

    # CORS
    allowed_origins: Union[str, List[str]] = "http://localhost:3000,http://localhost:8000"

    # Application
    environment: str = "development"
    log_level: str = "INFO"

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "production"

    @property
    def async_database_url(self) -> str:
        """Get async database URL for SQLAlchemy

        Converts postgresql:// to postgresql+asyncpg:// and removes sslmode and
        channel_binding parameters since asyncpg uses different SSL configuration.
        """
        url = self.database_url

        # Replace postgresql:// with postgresql+asyncpg://
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

        # Remove sslmode and channel_binding parameters that asyncpg doesn't support
        # asyncpg will handle SSL automatically
        if "sslmode=" in url or "channel_binding=" in url:
            from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            # Remove sslmode and channel_binding
            query_params.pop('sslmode', None)
            query_params.pop('channel_binding', None)
            # Reconstruct the query string
            new_query = urlencode(query_params, doseq=True)
            url = urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment
            ))

        return url


# Global settings instance
settings = Settings()

# Global OpenAI client instance (only if API key is provided)
openai_client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
