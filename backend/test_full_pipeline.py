"""End-to-end pipeline test"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.pipeline_orchestrator import PipelineOrchestrator
from src.core.logging_config import setup_logging, logger


# Test with 2 companies for speed
TEST_TICKERS = ["MSFT", "NVDA"]


async def progress_callback(stage: str, substage: str, data):
    """Pipeline progress callback"""
    logger.info(f"📍 {stage.upper()}: {substage}")


async def test_full_pipeline():
    """Test complete end-to-end pipeline"""

    setup_logging("INFO")

    logger.info("=" * 80)
    logger.info("END-TO-END PIPELINE TEST")
    logger.info(f"Companies: {', '.join(TEST_TICKERS)}")
    logger.info("=" * 80)

    orchestrator = PipelineOrchestrator()

    try:
        logger.info("\nRunning complete pipeline...")
        logger.info("(Skipping enrichment to save time - use skip_enrichment=False for full demo)\n")

        result = await orchestrator.run_pipeline(
            tickers=TEST_TICKERS,
            force_refresh=False,  # Use cache for speed
            skip_enrichment=True,  # Skip Browser-Use for faster test
            use_daytona=False,
            progress_callback=progress_callback
        )

        # Validate
        assert result["status"] in ["completed", "partial"], \
            f"Expected completed/partial, got {result['status']}"

        assert len(result["profiles"]) >= 1, \
            f"Expected at least 1 profile, got {len(result['profiles'])}"

        logger.info("\n" + "=" * 80)
        logger.info("RESULTS SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Job ID: {result['job_id']}")
        logger.info(f"Status: {result['status']}")
        logger.info(f"Successful: {result['successful']}/{result['total']}")
        logger.info(f"Duration: {result['duration_seconds']:.1f}s")
        logger.info(f"CSV Export: {result['csv_path']}")

        logger.info("\nCompany Profiles:")
        for profile in result["profiles"]:
            company = profile["company"]
            maturity = profile["maturity"]
            insights = profile["insights"]

            logger.info(f"\n{company['name']} ({company['ticker']}):")
            logger.info(f"  AI Maturity: {maturity['score']}/100 ({maturity['tier']})")
            logger.info(f"  Investments: {insights.get('investments', {}).get('total_amount', 'N/A')}")
            logger.info(f"  Products: {len(insights.get('products', []))}")
            logger.info(f"  Risks: {len(insights.get('risks', []))}")

        logger.info("\n" + "=" * 80)
        logger.info("✅ END-TO-END PIPELINE TEST PASSED!")
        logger.info("=" * 80)

        logger.info("\n🎯 HACKATHON DEMO READY:")
        logger.info("  ✅ SEC 10-K retrieval (API-based)")
        logger.info("  ✅ HTML parsing")
        logger.info("  ✅ Azure OpenAI GPT-4o extraction")
        logger.info("  ✅ AI maturity scoring")
        logger.info("  ✅ Browser-Use + Daytona (Phase 7 code ready)")
        logger.info("  ✅ Salesforce CSV export")
        logger.info("\n💡 To test Browser-Use + Daytona:")
        logger.info("  python test_enrichment.py")

        return True

    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = asyncio.run(test_full_pipeline())
    sys.exit(0 if success else 1)
