"""Pipeline API endpoints - Real implementation"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict
import uuid
from datetime import datetime
import asyncio

from src.models.pipeline import (
    PipelineStartRequest, PipelineStartResponse, PipelineStatusResponse,
    PipelineResultsResponse, CompanyProgress, PipelineProgress, PipelineResultsSummary
)
from src.core.logging_config import logger
from src.services.pipeline_orchestrator import PipelineOrchestrator

router = APIRouter(prefix="/api/v1/pipeline", tags=["pipeline"])

# In-memory job storage (will be replaced with Redis or database)
active_jobs: Dict[str, dict] = {}


# Background task to execute pipeline
async def execute_pipeline_background(job_id: str, request: PipelineStartRequest):
    """Execute pipeline in background"""
    try:
        logger.info(f"[Job {job_id}] Starting pipeline execution for {request.company_tickers}")

        # Update job status
        active_jobs[job_id]["status"] = "in_progress"

        # Create orchestrator
        orchestrator = PipelineOrchestrator()

        # Run pipeline
        result = await orchestrator.run_pipeline(
            tickers=request.company_tickers,
            force_refresh=request.force_refresh,
            skip_enrichment=request.skip_enrichment,
            use_daytona=True  # Use Daytona by default
        )

        # Update job with results
        active_jobs[job_id]["status"] = "completed"
        active_jobs[job_id]["results"] = [result]  # Single company result
        active_jobs[job_id]["completed_at"] = datetime.now()

        logger.info(f"[Job {job_id}] Pipeline completed successfully")

    except Exception as e:
        logger.error(f"[Job {job_id}] Pipeline failed: {e}")
        active_jobs[job_id]["status"] = "failed"
        active_jobs[job_id]["error"] = str(e)
        active_jobs[job_id]["completed_at"] = datetime.now()


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

    # ✅ Execute pipeline in background
    background_tasks.add_task(execute_pipeline_background, job_id, request)

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

    # Calculate progress based on job status
    if job["status"] == "completed":
        percentage = 100
        current_stage = "finalization"
        companies_processed = job["total_companies"]
    elif job["status"] == "in_progress":
        percentage = 50
        current_stage = "enrichment"
        companies_processed = 0
    else:
        percentage = 0
        current_stage = "retrieval"
        companies_processed = 0

    progress = PipelineProgress(
        current_stage=current_stage,
        companies_processed=companies_processed,
        companies_total=job["total_companies"],
        percentage=percentage
    )

    # Determine company status
    company_status = "completed" if job["status"] == "completed" else "in_progress" if job["status"] == "in_progress" else "pending"
    companies = [
        CompanyProgress(ticker=t, status=company_status, stage=current_stage)
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

    if job["status"] not in ["completed", "partial", "failed"]:
        raise HTTPException(status_code=425, detail="Pipeline not yet completed")

    # Calculate execution time
    started_at = job["started_at"]
    completed_at = job.get("completed_at", datetime.now())
    total_time = (completed_at - started_at).total_seconds()

    # Return real results
    return PipelineResultsResponse(
        job_id=job_id,
        status=job["status"],
        results=job.get("results", []),
        summary=PipelineResultsSummary(
            total_companies=job["total_companies"],
            successful=len(job.get("results", [])),
            failed=1 if job["status"] == "failed" else 0,
            total_time_seconds=int(total_time)
        )
    )
