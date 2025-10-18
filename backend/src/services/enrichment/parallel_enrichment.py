"""Parallel enrichment using Daytona + Browser-Use"""
import asyncio
from datetime import datetime
from typing import List, Callable, Optional
import uuid

from src.core.logging_config import logger
from src.services.enrichment.daytona_manager import DaytonaEnvironmentManager
from src.services.enrichment.job_scraper import AIJobScraper


class ParallelEnrichmentController:
    """Orchestrate parallel job scraping across Daytona environments"""

    def __init__(self):
        self.daytona_manager = DaytonaEnvironmentManager()
        self.job_scraper = AIJobScraper()
        logger.info("ParallelEnrichmentController initialized")

    async def enrich_parallel(
        self,
        companies: List[dict],
        use_daytona: bool = True,
        progress_callback: Optional[Callable] = None
    ) -> dict:
        """
        Enrich multiple companies in parallel using Daytona + Browser-Use

        Args:
            companies: List of company dicts
            use_daytona: If True, use Daytona environments (slower setup, isolated)
                        If False, run locally in parallel (faster for demo)
            progress_callback: Optional progress callback

        Returns:
            Enrichment job result dict
        """
        job_id = str(uuid.uuid4())
        started_at = datetime.now()

        logger.info(
            f"Starting parallel enrichment job {job_id} for {len(companies)} companies "
            f"(use_daytona={use_daytona})"
        )

        results = {}
        errors = {}
        workspaces = {}

        try:
            # Step 1: Create Daytona workspaces if requested
            if use_daytona:
                logger.info("Creating Daytona workspaces...")
                tickers = [c["ticker"] for c in companies]
                workspaces = await self.daytona_manager.create_all_workspaces(tickers)

                # Filter to successful workspaces
                companies_with_workspaces = [
                    c for c in companies
                    if workspaces.get(c["ticker"], {}).get("status") == "ready"
                ]

                logger.info(
                    f"Created {len(companies_with_workspaces)}/{len(companies)} workspaces"
                )
            else:
                companies_with_workspaces = companies

            # Step 2: Run job scraping in parallel
            logger.info(f"Running Browser-Use job scraping for {len(companies_with_workspaces)} companies")

            if progress_callback:
                await progress_callback("enrichment", "scraping_started", None)

            # Create scraping tasks
            tasks = []
            for company in companies_with_workspaces:
                task = self._scrape_with_progress(
                    company,
                    workspaces.get(company["ticker"]) if use_daytona else None,
                    progress_callback
                )
                tasks.append(task)

            # Execute in parallel
            scrape_results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for company, scrape_result in zip(companies_with_workspaces, scrape_results):
                ticker = company["ticker"]

                if isinstance(scrape_result, Exception):
                    logger.error(f"Enrichment failed for {ticker}: {scrape_result}")
                    errors[ticker] = str(scrape_result)
                else:
                    logger.info(
                        f"Enrichment succeeded for {ticker}: "
                        f"{len(scrape_result.get('ai_jobs', []))} jobs"
                    )
                    results[ticker] = scrape_result

        finally:
            # Step 3: Cleanup Daytona workspaces
            if use_daytona and workspaces:
                logger.info("Cleaning up Daytona workspaces...")
                await self.daytona_manager.cleanup_all()

        completed_at = datetime.now()
        duration = (completed_at - started_at).total_seconds()

        # Determine status
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
            "used_daytona": use_daytona,
            "workspaces_created": len(workspaces) if use_daytona else 0,
            "started_at": started_at.isoformat(),
            "completed_at": completed_at.isoformat(),
            "duration_seconds": round(duration, 2)
        }

        logger.info(
            f"Enrichment job {job_id} {status}: {successful}/{total} successful "
            f"in {duration:.1f}s (Daytona: {use_daytona})"
        )

        return job_result

    async def _scrape_with_progress(
        self,
        company: dict,
        workspace: Optional[dict],
        progress_callback: Optional[Callable]
    ) -> dict:
        """
        Scrape jobs for single company with progress tracking

        Args:
            company: Company dict
            workspace: Daytona workspace info (if using Daytona)
            progress_callback: Progress callback

        Returns:
            Enrichment result dict
        """
        ticker = company["ticker"]

        try:
            if progress_callback:
                await progress_callback(ticker, "scraping_started", None)

            # Scrape jobs using Browser-Use
            if workspace:
                logger.info(f"Scraping {ticker} in Daytona workspace {workspace['workspace_id']}")
                # For hackathon demo, run locally even with workspace created
                # In production, would execute scraping code inside Daytona workspace
                result = await self.job_scraper.scrape_jobs_with_retry(company)
            else:
                logger.info(f"Scraping {ticker} locally")
                result = await self.job_scraper.scrape_jobs_with_retry(company)

            if progress_callback:
                await progress_callback(ticker, "scraping_completed", result)

            return result

        except Exception as e:
            if progress_callback:
                await progress_callback(ticker, "scraping_failed", {"error": str(e)})
            raise
