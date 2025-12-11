"""Database and vector store configuration

Provides async database engine, session management, and Qdrant client setup.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams

from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

# SQLAlchemy Base for models
Base = declarative_base()

# Global engine instance
_engine: AsyncEngine | None = None

# Global session maker
_async_session_maker: async_sessionmaker[AsyncSession] | None = None

# Global Qdrant client
_qdrant_client: AsyncQdrantClient | None = None


def get_engine() -> AsyncEngine:
    """Get or create the async database engine

    Returns:
        AsyncEngine instance
    """
    global _engine

    if _engine is None:
        # AsyncPG connection arguments for SSL
        connect_args = {}
        if "neon.tech" in settings.database_url or settings.is_production:
            # Enable SSL for Neon and production databases
            connect_args["ssl"] = "require"

        _engine = create_async_engine(
            settings.async_database_url,
            echo=not settings.is_production,  # Log SQL in development
            pool_pre_ping=True,  # Verify connections before using
            pool_size=5,
            max_overflow=10,
            connect_args=connect_args,
        )
        logger.info("Database engine created")

    return _engine


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    """Get or create the async session maker

    Returns:
        async_sessionmaker instance
    """
    global _async_session_maker

    if _async_session_maker is None:
        engine = get_engine()
        _async_session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        logger.info("Session maker created")

    return _async_session_maker


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database sessions

    Yields:
        AsyncSession instance
    """
    session_maker = get_session_maker()
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


def get_qdrant_client() -> AsyncQdrantClient:
    """Get or create the Qdrant client

    Returns:
        AsyncQdrantClient instance
    """
    global _qdrant_client

    if _qdrant_client is None:
        _qdrant_client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            timeout=30.0,
        )
        logger.info("Qdrant client created")

    return _qdrant_client


async def init_qdrant_collection() -> None:
    """Initialize Qdrant collection if it doesn't exist

    Creates the collection with appropriate vector configuration.
    """
    client = get_qdrant_client()

    # Check if collection exists
    collections = await client.get_collections()
    collection_names = [col.name for col in collections.collections]

    if settings.qdrant_collection_name not in collection_names:
        # Create collection with vector configuration
        await client.create_collection(
            collection_name=settings.qdrant_collection_name,
            vectors_config=VectorParams(
                size=settings.vector_size,
                distance=Distance.COSINE,
            ),
        )
        logger.info(f"Created Qdrant collection: {settings.qdrant_collection_name}")
    else:
        logger.info(f"Qdrant collection already exists: {settings.qdrant_collection_name}")


async def close_database_connections() -> None:
    """Close all database connections gracefully"""
    global _engine, _qdrant_client

    if _engine is not None:
        await _engine.dispose()
        logger.info("Database engine disposed")
        _engine = None

    if _qdrant_client is not None:
        await _qdrant_client.close()
        logger.info("Qdrant client closed")
        _qdrant_client = None
