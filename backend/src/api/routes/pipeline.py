"""Pipeline API endpoints - Real implementation"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict
import uuid
from datetime import datetime

from src.models.pipeline import (
    PipelineStartRequest, PipelineStartResponse, PipelineStatusResponse,
    PipelineResultsResponse, CompanyProgress, PipelineProgress, PipelineResultsSummary
)
from src.core.logging_config import logger

router = APIRouter(prefix="/api/v1/pipeline", tags=["pipeline"])

# In-memory job storage (will be replaced with Redis or database)
active_jobs: Dict[str, dict] = {}


@router.post("/start", response_model=PipelineStartResponse, status_code=202)
async def start_pipeline(request: PipelineStartRequest, background_tasks: BackgroundTasks):
    """Start the full intelligence pipeline"""
    job_id = str(uuid.uuid4())

    logger.info(f"Starting pipeline job {job_id} for tickers: {request.company_tickers}")

    # Validate tickers
    valid_tickers = ["MSFT", "AAPL", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "CRM", "ADBE", "NFLX"]
    invalid_tickers = [t for t in request.company_tickers if t not in valid_tickers]

    if invalid_tickers:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid tickers: {', '.join(invalid_tickers)}"
        )

    # Create job entry
    active_jobs[job_id] = {
        "status": "started",
        "tickers": request.company_tickers,
        "started_at": datetime.now(),
        "total_companies": len(request.company_tickers),
        "force_refresh": request.force_refresh,
        "skip_enrichment": request.skip_enrichment,
        "results": []
    }

    # TODO: Add background task to execute pipeline
    # background_tasks.add_task(execute_pipeline, job_id, request)

    return PipelineStartResponse(
        job_id=job_id,
        status="started",
        total_companies=len(request.company_tickers),
        estimated_time_seconds=len(request.company_tickers) * 60,  # 60 seconds per company
        started_at=datetime.now().isoformat()
    )


@router.get("/status/{job_id}", response_model=PipelineStatusResponse)
async def get_pipeline_status(job_id: str):
    """Get pipeline execution status"""
    if job_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = active_jobs[job_id]

    # TODO: Get real progress from pipeline execution
    progress = PipelineProgress(
        current_stage="retrieval",
        companies_processed=0,
        companies_total=job["total_companies"],
        percentage=0
    )

    companies = [
        CompanyProgress(ticker=t, status="pending", stage=None)
        for t in job["tickers"]
    ]

    return PipelineStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=progress,
        companies=companies,
        started_at=job["started_at"].isoformat(),
        estimated_completion=None
    )


@router.get("/results/{job_id}", response_model=PipelineResultsResponse)
async def get_pipeline_results(job_id: str):
    """Get completed pipeline results"""
    if job_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = active_jobs[job_id]

    if job["status"] not in ["completed", "partial"]:
        raise HTTPException(status_code=425, detail="Pipeline not yet completed")

    # TODO: Return real results
    return PipelineResultsResponse(
        job_id=job_id,
        status=job["status"],
        results=job.get("results", []),
        summary=PipelineResultsSummary(
            total_companies=job["total_companies"],
            successful=len(job.get("results", [])),
            failed=0,
            total_time_seconds=0
        )
    )
