"""Health check endpoint

Provides health status for the application and its dependencies.
"""
from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

from sqlalchemy import text

from src.config.database import get_engine, get_qdrant_client
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    environment: str
    dependencies: Dict[str, str]


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check the health status of the application and its dependencies"
)
async def health_check() -> HealthResponse:
    """Perform health check on application and dependencies

    Returns:
        HealthResponse with status and dependency information
    """
    dependencies: Dict[str, str] = {}

    # Check database connection
    try:
        engine = get_engine()
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        dependencies["database"] = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        dependencies["database"] = "unhealthy"

    # Check Qdrant connection
    try:
        client = get_qdrant_client()
        await client.get_collections()
        dependencies["qdrant"] = "healthy"
    except Exception as e:
        logger.error(f"Qdrant health check failed: {e}")
        dependencies["qdrant"] = "unhealthy"

    # Overall status
    overall_status = "healthy" if all(
        dep_status == "healthy" for dep_status in dependencies.values()
    ) else "degraded"

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat(),
        environment=settings.environment,
        dependencies=dependencies
    )
