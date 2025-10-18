"""Mock API endpoints for frontend development"""
from fastapi import APIRouter, HTTPException
from typing import Dict
import uuid
from datetime import datetime, timedelta

from src.models.company import CompanyProfile
from src.models.pipeline import (
    PipelineStartRequest, PipelineStartResponse, PipelineStatusResponse,
    CompanyProgress, PipelineProgress
)
from src.utils.mock_data import get_mock_company_profile

router = APIRouter(prefix="/mock", tags=["mock"])

# In-memory storage for mock jobs
mock_jobs: Dict[str, dict] = {}


@router.post("/pipeline/start", response_model=PipelineStartResponse)
async def start_mock_pipeline(request: PipelineStartRequest):
    """Start a mock pipeline - returns immediately with fake job ID"""
    job_id = str(uuid.uuid4())

    mock_jobs[job_id] = {
        "status": "in_progress",
        "tickers": request.company_tickers,
        "started_at": datetime.now(),
        "total_companies": len(request.company_tickers)
    }

    return PipelineStartResponse(
        job_id=job_id,
        status="started",
        total_companies=len(request.company_tickers),
        estimated_time_seconds=len(request.company_tickers) * 30,
        started_at=datetime.now().isoformat()
    )


@router.get("/pipeline/status/{job_id}", response_model=PipelineStatusResponse)
async def get_mock_pipeline_status(job_id: str):
    """Get mock pipeline status - simulates progress"""
    if job_id not in mock_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = mock_jobs[job_id]
    elapsed_seconds = (datetime.now() - job["started_at"]).total_seconds()

    # Simulate progress (10 seconds per company)
    simulated_progress = min(int((elapsed_seconds / 10) * 100), 100)
    companies_processed = int((simulated_progress / 100) * job["total_companies"])

    # Update status
    if simulated_progress >= 100:
        job["status"] = "completed"
        status = "completed"
    else:
        status = "in_progress"

    # Generate company progress
    companies = []
    for i, ticker in enumerate(job["tickers"]):
        if i < companies_processed:
            companies.append(CompanyProgress(
                ticker=ticker,
                status="completed",
                stage="enrichment"
            ))
        elif i == companies_processed:
            companies.append(CompanyProgress(
                ticker=ticker,
                status="in_progress",
                stage="analysis"
            ))
        else:
            companies.append(CompanyProgress(
                ticker=ticker,
                status="pending",
                stage=None
            ))

    progress = PipelineProgress(
        current_stage="enrichment" if simulated_progress < 100 else "finalization",
        companies_processed=companies_processed,
        companies_total=job["total_companies"],
        percentage=simulated_progress
    )

    return PipelineStatusResponse(
        job_id=job_id,
        status=status,
        progress=progress,
        companies=companies,
        started_at=job["started_at"].isoformat(),
        estimated_completion=(job["started_at"] + timedelta(seconds=job["total_companies"] * 10)).isoformat()
    )


@router.get("/companies/{ticker}", response_model=CompanyProfile)
async def get_mock_company(ticker: str):
    """Get mock company profile"""
    valid_tickers = ["MSFT", "AAPL", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "CRM", "ADBE", "NFLX"]

    if ticker not in valid_tickers:
        raise HTTPException(
            status_code=404,
            detail=f"Ticker '{ticker}' not found. Valid tickers: {', '.join(valid_tickers)}"
        )

    return get_mock_company_profile(ticker)


@router.get("/health")
async def mock_health():
    """Mock health endpoint"""
    return {
        "status": "healthy",
        "daytona": "connected",
        "azure_openai": "connected",
        "version": "1.0.0-mock"
    }
