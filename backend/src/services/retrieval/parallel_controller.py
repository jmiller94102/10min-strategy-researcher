"""Parallel 10-K retrieval controller"""
import asyncio
from datetime import datetime
from typing import Callable, Optional
import uuid

from src.core.logging_config import logger
from src.services.retrieval.retrieval_service import RetrievalService
from src.services.retrieval.company_manager import CompanyManager


class ParallelRetrievalController:
    """Orchestrates parallel 10-K retrieval for multiple companies"""

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.company_manager = CompanyManager()
        self.active_jobs = {}

    async def retrieve_parallel(
        self,
        tickers: list[str],
        force_refresh: bool = False,
        progress_callback: Optional[Callable] = None
    ) -> dict:
        """
        Retrieve 10-Ks for multiple companies in parallel

        Args:
            tickers: List of company ticker symbols
            force_refresh: If True, bypass cache
            progress_callback: Optional callback(ticker, stage, result) for progress updates

        Returns:
            Dict with job results:
            {
                "job_id": "uuid",
                "status": "completed|partial|failed",
                "total": 10,
                "successful": 8,
                "failed": 2,
                "results": {
                    "MSFT": {...},
                    "AAPL": {...},
                    ...
                },
                "errors": {
                    "TSLA": "error message",
                    ...
                },
                "started_at": "2025-10-18T13:00:00",
                "completed_at": "2025-10-18T13:02:30",
                "duration_seconds": 150
            }
        """
        job_id = str(uuid.uuid4())
        started_at = datetime.now()

        logger.info(f"Starting parallel retrieval job {job_id} for {len(tickers)} companies")

        # Validate all tickers first
        companies = []
        for ticker in tickers:
            try:
                company = self.company_manager.get_company(ticker)
                companies.append(company)
            except Exception as e:
                logger.error(f"Invalid ticker {ticker}: {e}")
                # For invalid tickers, fail fast
                return {
                    "job_id": job_id,
                    "status": "failed",
                    "error": f"Invalid ticker: {ticker}",
                    "started_at": started_at.isoformat(),
                }

        # Create tasks for parallel execution
        tasks = []
        for company in companies:
            task = self._retrieve_with_progress(
                company,
                force_refresh,
                progress_callback
            )
            tasks.append(task)

        # Execute in parallel with asyncio.gather (return_exceptions=True for partial success)
        logger.info(f"Executing {len(tasks)} retrieval tasks in parallel")
        task_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        results = {}
        errors = {}

        for company, result in zip(companies, task_results):
            ticker = company["ticker"]

            if isinstance(result, Exception):
                logger.error(f"Failed to retrieve {ticker}: {result}")
                errors[ticker] = str(result)
            else:
                logger.info(f"Successfully retrieved {ticker}")
                results[ticker] = result

        completed_at = datetime.now()
        duration = (completed_at - started_at).total_seconds()

        # Determine overall status
        total = len(companies)
        successful = len(results)
        failed = len(errors)

        if successful == total:
            status = "completed"
        elif successful > 0:
            status = "partial"
        else:
            status = "failed"

        job_result = {
            "job_id": job_id,
            "status": status,
            "total": total,
            "successful": successful,
            "failed": failed,
            "results": results,
            "errors": errors,
            "started_at": started_at.isoformat(),
            "completed_at": completed_at.isoformat(),
            "duration_seconds": round(duration, 2)
        }

        logger.info(
            f"Job {job_id} {status}: {successful}/{total} successful "
            f"in {duration:.1f}s"
        )

        # Store job for later retrieval
        self.active_jobs[job_id] = job_result

        return job_result

    async def _retrieve_with_progress(
        self,
        company: dict,
        force_refresh: bool,
        progress_callback: Optional[Callable]
    ) -> dict:
        """
        Retrieve 10-K for single company with progress tracking

        Args:
            company: Company dict
            force_refresh: Bypass cache
            progress_callback: Progress update callback

        Returns:
            10-K result dict
        """
        ticker = company["ticker"]

        try:
            # Send "started" progress
            if progress_callback:
                await progress_callback(ticker, "started", None)

            # Retrieve 10-K
            logger.info(f"Retrieving 10-K for {ticker}")
            result = await self.retrieval_service.retrieve_10k(company, force_refresh)

            # Send "completed" progress
            if progress_callback:
                await progress_callback(ticker, "completed", result)

            return result

        except Exception as e:
            # Send "failed" progress
            if progress_callback:
                await progress_callback(ticker, "failed", {"error": str(e)})

            raise

    def get_job_status(self, job_id: str) -> Optional[dict]:
        """Get job results by ID"""
        return self.active_jobs.get(job_id)
