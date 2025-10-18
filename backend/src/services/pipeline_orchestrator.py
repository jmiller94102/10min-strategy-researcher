"""End-to-end pipeline orchestrator for 10-K AI intelligence"""
import asyncio
from datetime import datetime
from typing import List, Callable, Optional
import uuid

from src.core.logging_config import logger
from src.services.retrieval.parallel_controller import ParallelRetrievalController
from src.services.retrieval.company_manager import CompanyManager
from src.services.analysis.html_parser import TenKHTMLParser
from src.services.analysis.llm_extractor import AIInsightExtractor
from src.services.analysis.maturity_scorer import AIMaturityScorer
from src.services.enrichment.parallel_enrichment import ParallelEnrichmentController
from src.services.export.salesforce_exporter import SalesforceCSVExporter


class PipelineOrchestrator:
    """Orchestrate complete 10-K AI intelligence pipeline"""

    def __init__(self):
        self.company_manager = CompanyManager()
        self.retrieval_controller = ParallelRetrievalController()
        self.html_parser = TenKHTMLParser()
        self.llm_extractor = AIInsightExtractor()
        self.maturity_scorer = AIMaturityScorer()
        self.enrichment_controller = ParallelEnrichmentController()
        self.csv_exporter = SalesforceCSVExporter()

        self.active_jobs = {}
        logger.info("PipelineOrchestrator initialized")

    async def run_pipeline(
        self,
        tickers: List[str],
        force_refresh: bool = False,
        skip_enrichment: bool = False,
        use_daytona: bool = False,
        progress_callback: Optional[Callable] = None
    ) -> dict:
        """
        Run complete pipeline for multiple companies

        Args:
            tickers: Company ticker symbols
            force_refresh: Bypass 10-K cache
            skip_enrichment: Skip Browser-Use enrichment (faster)
            use_daytona: Use Daytona environments for enrichment
            progress_callback: Progress update callback

        Returns:
            Pipeline result dict with all company profiles
        """
        job_id = str(uuid.uuid4())
        started_at = datetime.now()

        logger.info("=" * 80)
        logger.info(f"PIPELINE START - Job {job_id}")
        logger.info(f"Companies: {', '.join(tickers)}")
        logger.info(f"Options: force_refresh={force_refresh}, skip_enrichment={skip_enrichment}, use_daytona={use_daytona}")
        logger.info("=" * 80)

        results = []
        errors = {}

        try:
            # Step 1: Validate companies
            logger.info("\n[Step 1/6] Validating companies...")
            companies = self.company_manager.get_companies(tickers)
            logger.info(f"✅ Validated {len(companies)} companies")

            if progress_callback:
                await progress_callback("pipeline", "validation_complete", {
                    "total": len(companies)
                })

            # Step 2: Retrieve 10-Ks in parallel
            logger.info("\n[Step 2/6] Retrieving 10-K filings from SEC...")
            retrieval_result = await self.retrieval_controller.retrieve_parallel(
                tickers=tickers,
                force_refresh=force_refresh
            )

            logger.info(
                f"✅ Retrieved {retrieval_result['successful']}/{retrieval_result['total']} 10-Ks "
                f"in {retrieval_result['duration_seconds']:.1f}s"
            )

            if progress_callback:
                await progress_callback("pipeline", "retrieval_complete", retrieval_result)

            # Step 3: Parse HTML and extract AI text
            logger.info("\n[Step 3/6] Parsing HTML and extracting AI content...")
            parsed_results = {}
            for ticker, retrieval_data in retrieval_result["results"].items():
                html_content = retrieval_data.get("html_content", "")
                parsed = self.html_parser.parse_10k(html_content)
                parsed_results[ticker] = parsed

            logger.info(f"✅ Parsed {len(parsed_results)} 10-K filings")

            # Step 4: LLM extraction (in parallel)
            logger.info("\n[Step 4/6] Extracting AI insights with Azure OpenAI GPT-4o...")
            extraction_tasks = []
            for ticker in retrieval_result["results"].keys():
                company = self.company_manager.get_company(ticker)
                ai_text = parsed_results[ticker]["ai_text"]
                task = self.llm_extractor.extract_insights(ai_text, company["name"])
                extraction_tasks.append((ticker, task))

            # Execute LLM extractions in parallel
            insights_results = {}
            for ticker, task in extraction_tasks:
                insights = await task
                insights_results[ticker] = insights

            logger.info(f"✅ Extracted insights for {len(insights_results)} companies")

            if progress_callback:
                await progress_callback("pipeline", "extraction_complete", {
                    "count": len(insights_results)
                })

            # Step 5: Live enrichment (optional, with Browser-Use + Daytona)
            enrichment_results = {}
            if not skip_enrichment:
                logger.info(f"\n[Step 5/6] Live enrichment with Browser-Use (use_daytona={use_daytona})...")
                enrichment_result = await self.enrichment_controller.enrich_parallel(
                    companies=companies,
                    use_daytona=use_daytona,
                    progress_callback=None
                )

                enrichment_results = enrichment_result.get("results", {})
                logger.info(
                    f"✅ Enriched {enrichment_result['successful']}/{enrichment_result['total']} companies "
                    f"in {enrichment_result['duration_seconds']:.1f}s"
                )

                if progress_callback:
                    await progress_callback("pipeline", "enrichment_complete", enrichment_result)
            else:
                logger.info("\n[Step 5/6] Skipping enrichment (skip_enrichment=True)")

            # Step 6: Calculate maturity scores and assemble profiles
            logger.info("\n[Step 6/6] Calculating AI maturity scores...")
            for ticker in retrieval_result["results"].keys():
                try:
                    company = self.company_manager.get_company(ticker)
                    retrieval_data = retrieval_result["results"][ticker]
                    insights = insights_results.get(ticker, {})
                    enrichment = enrichment_results.get(ticker, {})

                    # Calculate maturity score
                    maturity = self.maturity_scorer.calculate_score(
                        insights=insights,
                        enrichment=enrichment if enrichment else None
                    )

                    # Assemble complete profile
                    profile = {
                        "company": company,
                        "filing_date": retrieval_data.get("filing_date"),
                        "fiscal_year": retrieval_data.get("fiscal_year"),
                        "insights": insights,
                        "enrichment": enrichment,
                        "maturity": maturity
                    }

                    results.append(profile)

                except Exception as e:
                    logger.error(f"Failed to process {ticker}: {e}")
                    errors[ticker] = str(e)

            logger.info(f"✅ Generated {len(results)} complete profiles")

            # Step 7: Export to CSV
            logger.info("\n[Step 7/7] Exporting to Salesforce CSV...")
            csv_path = self.csv_exporter.export_companies(results)
            logger.info(f"✅ Exported to {csv_path}")

            if progress_callback:
                await progress_callback("pipeline", "export_complete", {
                    "csv_path": csv_path
                })

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            errors["pipeline"] = str(e)

        completed_at = datetime.now()
        duration = (completed_at - started_at).total_seconds()

        # Determine overall status
        total = len(tickers)
        successful = len(results)
        failed = len(errors)

        if successful == total:
            status = "completed"
        elif successful > 0:
            status = "partial"
        else:
            status = "failed"

        pipeline_result = {
            "job_id": job_id,
            "status": status,
            "total": total,
            "successful": successful,
            "failed": failed,
            "profiles": results,
            "errors": errors,
            "csv_path": csv_path if results else None,
            "started_at": started_at.isoformat(),
            "completed_at": completed_at.isoformat(),
            "duration_seconds": round(duration, 2)
        }

        logger.info("\n" + "=" * 80)
        logger.info(f"PIPELINE COMPLETE - Job {job_id}")
        logger.info(f"Status: {status} ({successful}/{total} successful)")
        logger.info(f"Duration: {duration:.1f}s")
        logger.info("=" * 80)

        # Store job
        self.active_jobs[job_id] = pipeline_result

        return pipeline_result

    def get_job_status(self, job_id: str) -> Optional[dict]:
        """Get pipeline job status"""
        return self.active_jobs.get(job_id)
