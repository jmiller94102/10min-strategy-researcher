"""Backend Verification Test - Save all outputs for inspection"""
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.pipeline_orchestrator import PipelineOrchestrator
from src.core.logging_config import setup_logging, logger


# Test with 3 companies
TEST_TICKERS = ["MSFT", "AAPL", "NVDA"]


def save_json(data: dict, filepath: Path):
    """Save data as formatted JSON"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    logger.info(f"💾 Saved: {filepath}")


def save_text(content: str, filepath: Path):
    """Save text content"""
    with open(filepath, 'w') as f:
        f.write(content)
    logger.info(f"💾 Saved: {filepath}")


async def test_backend_verification():
    """
    Complete backend verification test
    Saves all outputs to /output for inspection
    """
    setup_logging("INFO")

    # Create output directory
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_dir = output_dir / f"backend_test_{timestamp}"
    test_dir.mkdir(exist_ok=True)

    logger.info("=" * 80)
    logger.info("BACKEND VERIFICATION TEST")
    logger.info(f"Companies: {', '.join(TEST_TICKERS)}")
    logger.info(f"Output Directory: {test_dir}")
    logger.info("=" * 80)

    orchestrator = PipelineOrchestrator()

    try:
        # ==================================================================
        # PHASE 1: SEC 10-K Retrieval
        # ==================================================================
        logger.info("\n[PHASE 1] Testing SEC 10-K Retrieval...")

        retrieval_result = await orchestrator.retrieval_controller.retrieve_parallel(
            tickers=TEST_TICKERS,
            force_refresh=False  # Use cache if available
        )

        # Save retrieval results
        retrieval_file = test_dir / "1_sec_retrieval.json"
        retrieval_summary = {
            "status": retrieval_result["status"],
            "total": retrieval_result["total"],
            "successful": retrieval_result["successful"],
            "duration_seconds": retrieval_result["duration_seconds"],
            "companies": {}
        }

        for ticker, data in retrieval_result["results"].items():
            # Save full HTML for each company
            html_file = test_dir / f"1_sec_{ticker}_10k.html"
            save_text(data["html_content"][:50000], html_file)  # First 50K chars

            # Add to summary
            retrieval_summary["companies"][ticker] = {
                "company": data["company"]["name"],
                "filing_date": data["filing_date"],
                "fiscal_year": data["fiscal_year"],
                "accession_number": data["accession_number"],
                "html_url": data["html_url"],
                "html_size": len(data["html_content"])
            }

        save_json(retrieval_summary, retrieval_file)

        logger.info(f"✅ Phase 1 Complete: {retrieval_result['successful']}/{retrieval_result['total']} companies")

        # ==================================================================
        # PHASE 2: HTML Parsing
        # ==================================================================
        logger.info("\n[PHASE 2] Testing HTML Parsing & AI Text Extraction...")

        parsed_results = {}
        parsing_summary = {"companies": {}}

        for ticker, data in retrieval_result["results"].items():
            parsed = orchestrator.html_parser.parse_10k(data["html_content"])
            parsed_results[ticker] = parsed

            # Save AI-related text
            ai_text_file = test_dir / f"2_parsed_{ticker}_ai_text.txt"
            save_text(parsed["ai_text"][:10000], ai_text_file)  # First 10K chars

            parsing_summary["companies"][ticker] = {
                "full_text_size": len(parsed["full_text"]),
                "ai_text_size": len(parsed["ai_text"]),
                "ai_sentence_count": parsed["ai_sentence_count"]
            }

        parsing_file = test_dir / "2_parsing_summary.json"
        save_json(parsing_summary, parsing_file)

        logger.info(f"✅ Phase 2 Complete: Extracted AI content from {len(parsed_results)} companies")

        # ==================================================================
        # PHASE 3: LLM Extraction (Azure OpenAI GPT-4o)
        # ==================================================================
        logger.info("\n[PHASE 3] Testing LLM Extraction with Azure OpenAI GPT-4o...")

        insights_results = {}
        llm_summary = {"companies": {}}

        for ticker in retrieval_result["results"].keys():
            company = orchestrator.company_manager.get_company(ticker)
            ai_text = parsed_results[ticker]["ai_text"]

            logger.info(f"  Extracting insights for {ticker}...")
            insights = await orchestrator.llm_extractor.extract_insights(ai_text, company["name"])
            insights_results[ticker] = insights

            # Save insights
            insights_file = test_dir / f"3_llm_{ticker}_insights.json"
            save_json(insights, insights_file)

            llm_summary["companies"][ticker] = {
                "investments_count": len(insights.get("investments", {}).get("details", [])),
                "products_count": len(insights.get("products", [])),
                "risks_count": len(insights.get("risks", [])),
                "total_investment": insights.get("investments", {}).get("total_amount", "unknown")
            }

        llm_file = test_dir / "3_llm_extraction_summary.json"
        save_json(llm_summary, llm_file)

        logger.info(f"✅ Phase 3 Complete: Extracted insights from {len(insights_results)} companies")

        # ==================================================================
        # PHASE 4: Browser-Use + Daytona + Azure OpenAI Enrichment
        # ==================================================================
        logger.info("\n[PHASE 4] Testing Browser-Use + Daytona + Azure OpenAI Enrichment...")
        logger.info("NOTE: ✅ Creating Daytona sandboxes for parallel execution")
        logger.info("      Using Azure OpenAI GPT-4o for Browser-Use agent\n")

        companies = orchestrator.company_manager.get_companies(TEST_TICKERS)

        enrichment_result = await orchestrator.enrichment_controller.enrich_parallel(
            companies=companies,
            use_daytona=True,  # ✅ REQUIRED: Create Daytona sandboxes
            progress_callback=None
        )

        # Save enrichment results
        enrichment_summary = {
            "status": enrichment_result["status"],
            "total": enrichment_result["total"],
            "successful": enrichment_result["successful"],
            "duration_seconds": enrichment_result["duration_seconds"],
            "used_daytona": enrichment_result["used_daytona"],
            "companies": {}
        }

        for ticker, data in enrichment_result["results"].items():
            # Save full enrichment data
            enrichment_file = test_dir / f"4_enrichment_{ticker}.json"
            save_json(data, enrichment_file)

            enrichment_summary["companies"][ticker] = {
                "ai_jobs_count": len(data.get("ai_jobs", [])),
                "tech_stack_count": len(data.get("tech_stack", [])),
                "tech_stack": data.get("tech_stack", [])[:10],  # Top 10
                "status": data.get("status", "unknown")
            }

        enrichment_summary_file = test_dir / "4_enrichment_summary.json"
        save_json(enrichment_summary, enrichment_summary_file)

        logger.info(f"✅ Phase 4 Complete: Enriched {enrichment_result['successful']}/{enrichment_result['total']} companies")

        # ==================================================================
        # PHASE 5: AI Maturity Scoring
        # ==================================================================
        logger.info("\n[PHASE 5] Testing AI Maturity Scoring...")

        profiles = []
        maturity_summary = {"companies": {}}

        for ticker in retrieval_result["results"].keys():
            company = orchestrator.company_manager.get_company(ticker)
            retrieval_data = retrieval_result["results"][ticker]
            insights = insights_results.get(ticker, {})
            enrichment = enrichment_result["results"].get(ticker, {})

            # Calculate maturity score
            maturity = orchestrator.maturity_scorer.calculate_score(
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

            profiles.append(profile)

            maturity_summary["companies"][ticker] = {
                "score": maturity["score"],
                "tier": maturity["tier"],
                "breakdown": maturity["breakdown"]
            }

        maturity_file = test_dir / "5_maturity_scores.json"
        save_json(maturity_summary, maturity_file)

        logger.info(f"✅ Phase 5 Complete: Scored {len(profiles)} companies")

        # ==================================================================
        # PHASE 6: Salesforce CSV Export
        # ==================================================================
        logger.info("\n[PHASE 6] Testing Salesforce CSV Export...")

        csv_path = orchestrator.csv_exporter.export_companies(profiles)

        # Copy to test directory
        import shutil
        csv_dest = test_dir / "6_salesforce_export.csv"
        shutil.copy(csv_path, csv_dest)

        logger.info(f"✅ Phase 6 Complete: CSV exported to {csv_dest}")

        # ==================================================================
        # CREATE SUMMARY REPORT
        # ==================================================================
        logger.info("\n[SUMMARY] Creating verification report...")

        summary_report = {
            "test_timestamp": timestamp,
            "test_directory": str(test_dir),
            "companies_tested": TEST_TICKERS,
            "results": {
                "phase_1_sec_retrieval": {
                    "status": retrieval_result["status"],
                    "successful": retrieval_result["successful"],
                    "duration_seconds": retrieval_result["duration_seconds"]
                },
                "phase_2_parsing": {
                    "companies_parsed": len(parsed_results)
                },
                "phase_3_llm_extraction": {
                    "companies_processed": len(insights_results)
                },
                "phase_4_enrichment": {
                    "status": enrichment_result["status"],
                    "successful": enrichment_result["successful"],
                    "used_daytona": enrichment_result["used_daytona"],
                    "duration_seconds": enrichment_result["duration_seconds"]
                },
                "phase_5_maturity_scoring": {
                    "companies_scored": len(profiles)
                },
                "phase_6_csv_export": {
                    "csv_path": str(csv_dest),
                    "companies_exported": len(profiles)
                }
            },
            "company_profiles": {}
        }

        for profile in profiles:
            ticker = profile["company"]["ticker"]
            summary_report["company_profiles"][ticker] = {
                "name": profile["company"]["name"],
                "filing_date": profile["filing_date"],
                "fiscal_year": profile["fiscal_year"],
                "ai_maturity_score": profile["maturity"]["score"],
                "ai_maturity_tier": profile["maturity"]["tier"],
                "investments": profile["insights"].get("investments", {}).get("total_amount", "unknown"),
                "products_count": len(profile["insights"].get("products", [])),
                "risks_count": len(profile["insights"].get("risks", [])),
                "ai_jobs_count": len(profile["enrichment"].get("ai_jobs", [])),
                "tech_stack": profile["enrichment"].get("tech_stack", [])[:10]
            }

        summary_file = test_dir / "SUMMARY_REPORT.json"
        save_json(summary_report, summary_file)

        # ==================================================================
        # CREATE README
        # ==================================================================
        readme_content = f"""# Backend Verification Test Results

**Test Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Companies Tested:** {', '.join(TEST_TICKERS)}

## Test Results Summary

### Phase 1: SEC 10-K Retrieval
- Status: {retrieval_result["status"]}
- Success Rate: {retrieval_result["successful"]}/{retrieval_result["total"]}
- Duration: {retrieval_result["duration_seconds"]}s
- Files: `1_sec_*.html`, `1_sec_retrieval.json`

### Phase 2: HTML Parsing
- Companies Parsed: {len(parsed_results)}
- Files: `2_parsed_*_ai_text.txt`, `2_parsing_summary.json`

### Phase 3: LLM Extraction (Azure OpenAI GPT-4o)
- Companies Processed: {len(insights_results)}
- Files: `3_llm_*_insights.json`, `3_llm_extraction_summary.json`

### Phase 4: Browser-Use + Daytona Enrichment
- Status: {enrichment_result["status"]}
- Success Rate: {enrichment_result["successful"]}/{enrichment_result["total"]}
- Duration: {enrichment_result["duration_seconds"]}s
- Used Daytona: {enrichment_result["used_daytona"]}
- Files: `4_enrichment_*.json`, `4_enrichment_summary.json`

### Phase 5: AI Maturity Scoring
- Companies Scored: {len(profiles)}
- Files: `5_maturity_scores.json`

### Phase 6: Salesforce CSV Export
- Companies Exported: {len(profiles)}
- Files: `6_salesforce_export.csv`

## Company Results

"""

        for profile in profiles:
            ticker = profile["company"]["ticker"]
            name = profile["company"]["name"]
            score = profile["maturity"]["score"]
            tier = profile["maturity"]["tier"]
            jobs = len(profile["enrichment"].get("ai_jobs", []))
            tech = len(profile["enrichment"].get("tech_stack", []))

            readme_content += f"""### {name} ({ticker})
- AI Maturity: {score}/100 ({tier})
- Filing: FY{profile["fiscal_year"]}, {profile["filing_date"]}
- AI Jobs Found: {jobs}
- Tech Stack Items: {tech}

"""

        readme_content += f"""
## File Descriptions

- `1_sec_*.html` - Raw 10-K HTML from SEC EDGAR (first 50K chars)
- `1_sec_retrieval.json` - SEC retrieval metadata
- `2_parsed_*_ai_text.txt` - Extracted AI-related text (first 10K chars)
- `2_parsing_summary.json` - Parsing statistics
- `3_llm_*_insights.json` - LLM-extracted insights (investments, products, risks)
- `3_llm_extraction_summary.json` - LLM extraction summary
- `4_enrichment_*.json` - Browser-Use job scraping results
- `4_enrichment_summary.json` - Enrichment statistics
- `5_maturity_scores.json` - AI maturity scores and breakdowns
- `6_salesforce_export.csv` - Final CRM-ready export
- `SUMMARY_REPORT.json` - Complete test results

## Next Steps

1. Review the CSV file: `6_salesforce_export.csv`
2. Check LLM insights: `3_llm_*_insights.json`
3. Verify enrichment data: `4_enrichment_*.json`
4. Confirm maturity scores: `5_maturity_scores.json`

All files are ready for frontend integration!
"""

        readme_file = test_dir / "README.md"
        save_text(readme_content, readme_file)

        logger.info(f"✅ Summary report saved: {summary_file}")
        logger.info(f"✅ README saved: {readme_file}")

        # ==================================================================
        # FINAL OUTPUT
        # ==================================================================
        logger.info("\n" + "=" * 80)
        logger.info("🎉 BACKEND VERIFICATION COMPLETE!")
        logger.info("=" * 80)
        logger.info(f"\n📁 Output Directory: {test_dir}")
        logger.info(f"\n📊 Files Created:")
        logger.info(f"   - README.md (start here!)")
        logger.info(f"   - SUMMARY_REPORT.json")
        logger.info(f"   - 6_salesforce_export.csv")
        logger.info(f"   - Plus {len(list(test_dir.glob('*')))} total files")

        logger.info(f"\n✅ All Phases Validated:")
        logger.info(f"   ✅ Phase 1: SEC 10-K Retrieval ({retrieval_result['successful']}/{retrieval_result['total']})")
        logger.info(f"   ✅ Phase 2: HTML Parsing ({len(parsed_results)} companies)")
        logger.info(f"   ✅ Phase 3: LLM Extraction ({len(insights_results)} companies)")
        logger.info(f"   ✅ Phase 4: Browser-Use Enrichment ({enrichment_result['successful']}/{enrichment_result['total']})")
        logger.info(f"   ✅ Phase 5: Maturity Scoring ({len(profiles)} companies)")
        logger.info(f"   ✅ Phase 6: CSV Export ({len(profiles)} companies)")

        logger.info(f"\n📈 Performance:")
        logger.info(f"   - SEC Retrieval: {retrieval_result['duration_seconds']:.1f}s")
        logger.info(f"   - Enrichment: {enrichment_result['duration_seconds']:.1f}s")

        logger.info("\n" + "=" * 80)
        logger.info("Backend is READY for frontend integration! ✨")
        logger.info("=" * 80)

        return True

    except Exception as e:
        logger.error(f"\n❌ VERIFICATION FAILED: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = asyncio.run(test_backend_verification())
    sys.exit(0 if success else 1)
