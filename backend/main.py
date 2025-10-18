"""10-K AI Intelligence Pipeline - Main FastAPI Application"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.core.config import settings
from src.core.logging_config import setup_logging, logger
from src.core.exceptions import (
    InvalidTickerError, DaytonaUnavailableError, LLMAPIError,
    RateLimitExceededError, PipelineException
)
from src.api.routes import mock, pipeline, companies, health


# Setup logging
setup_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    logger.info("Starting 10-K AI Intelligence Pipeline API")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Port: {settings.port}")
    logger.info(f"Cache enabled: {settings.enable_caching}")
    logger.info(f"Max Daytona environments: {settings.daytona_max_environments}")
    yield
    logger.info("Shutting down API")


# Create FastAPI app
app = FastAPI(
    title="10-K AI Intelligence Pipeline API",
    description="Extract AI strategy insights from SEC 10-K filings",
    version="1.0.0",
    lifespan=lifespan
)


# CORS middleware - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # Alternative React port
        "http://localhost:8083",  # Lovable.dev frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(InvalidTickerError)
async def invalid_ticker_handler(request: Request, exc: InvalidTickerError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": {
                "code": "INVALID_TICKER",
                "message": str(exc),
                "details": {"ticker": exc.ticker}
            }
        }
    )


@app.exception_handler(DaytonaUnavailableError)
async def daytona_unavailable_handler(request: Request, exc: DaytonaUnavailableError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": {
                "code": "DAYTONA_UNAVAILABLE",
                "message": "Daytona service is currently unavailable",
                "details": {}
            }
        }
    )


@app.exception_handler(LLMAPIError)
async def llm_api_error_handler(request: Request, exc: LLMAPIError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": {
                "code": "LLM_API_ERROR",
                "message": "AI analysis service error",
                "details": {"message": str(exc)}
            }
        }
    )


@app.exception_handler(RateLimitExceededError)
async def rate_limit_handler(request: Request, exc: RateLimitExceededError):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": {
                "code": "RATE_LIMIT_EXCEEDED",
                "message": "Too many requests. Please try again later.",
                "details": {}
            }
        }
    )


@app.exception_handler(PipelineException)
async def pipeline_exception_handler(request: Request, exc: PipelineException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "PIPELINE_ERROR",
                "message": str(exc),
                "details": {}
            }
        }
    )


# Include routers
app.include_router(mock.router)  # Mock endpoints for frontend development
app.include_router(pipeline.router)  # Real pipeline endpoints
app.include_router(companies.router)  # Company intelligence endpoints
app.include_router(health.router)  # Health check


# Root endpoint
@app.get("/")
async def root():
    """API root"""
    return {
        "name": "10-K AI Intelligence Pipeline API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "mock_endpoints": "/mock",
        "message": "Use /mock/* endpoints for frontend development with instant responses"
    }


# Development info endpoint
@app.get("/info")
async def info():
    """Development information"""
    return {
        "environment": settings.environment,
        "port": settings.port,
        "cache_enabled": settings.enable_caching,
        "daytona_max_environments": settings.daytona_max_environments,
        "endpoints": {
            "mock": "/mock/*",
            "real": "/api/v1/*",
            "docs": "/docs",
            "health": "/api/v1/health"
        },
        "frontend_development": {
            "use_mock_endpoints": True,
            "base_url": f"http://localhost:{settings.port}/mock",
            "note": "Mock endpoints return realistic data instantly without backend processing"
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower()
    )
