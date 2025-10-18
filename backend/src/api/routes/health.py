"""Health check endpoints"""
from fastapi import APIRouter
from src.models.pipeline import HealthResponse
from src.core.config import settings

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Service health check"""
    # TODO: Add actual health checks for Daytona and Azure OpenAI
    return HealthResponse(
        status="healthy",
        daytona="unknown",  # Will check connection
        azure_openai="unknown",  # Will check connection
        version="1.0.0"
    )
