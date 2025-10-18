"""Test script for Phase 2: Parallel Retrieval"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.retrieval.parallel_controller import ParallelRetrievalController
from src.core.logging_config import setup_logging, logger


# Test with 3 companies
TEST_TICKERS = ["MSFT", "AAPL", "NVDA"]


async def progress_callback(ticker: str, stage: str, result):
    """Progress update callback"""
    if stage == "started":
        logger.info(f"  [{ticker}] Started retrieval...")
    elif stage == "completed":
        filing_date = result.get("filing_date", "unknown")
        html_size = len(result.get("html_content", ""))
        logger.info(f"  [{ticker}] ✅ Completed! Filing: {filing_date}, Size: {html_size:,} chars")
    elif stage == "failed":
        error = result.get("error", "unknown error")
        logger.error(f"  [{ticker}] ❌ Failed: {error}")


async def test_parallel_retrieval():
    """Test parallel retrieval for 3 companies"""

    setup_logging("INFO")

    logger.info("=" * 80)
    logger.info("PHASE 2 TEST: Parallel 10-K Retrieval")
    logger.info(f"Companies: {', '.join(TEST_TICKERS)}")
    logger.info("=" * 80)

    controller = ParallelRetrievalController()

    try:
        # Test parallel retrieval (force fresh to ensure real SEC calls)
        logger.info(f"\n[1] Testing parallel retrieval for {len(TEST_TICKERS)} companies...")
        logger.info("Note: This will make real SEC API calls\n")

        result = await controller.retrieve_parallel(
            tickers=TEST_TICKERS,
            force_refresh=True,  # Force fresh retrieval
            progress_callback=progress_callback
        )

        # Validate result
        logger.info("\n[2] Validating results...")

        assert result["status"] in ["completed", "partial"], \
            f"Expected completed/partial, got {result['status']}"

        assert result["total"] == len(TEST_TICKERS), \
            f"Expected {len(TEST_TICKERS)} total, got {result['total']}"

        assert result["successful"] >= 2, \
            f"Expected at least 2 successful, got {result['successful']}"

        assert result["duration_seconds"] < 180, \
            f"Expected < 180s, took {result['duration_seconds']}s"

        logger.info("✅ All validations passed!")

        # Print summary
        logger.info("\n[3] Results Summary:")
        logger.info(f"  Job ID: {result['job_id']}")
        logger.info(f"  Status: {result['status']}")
        logger.info(f"  Total: {result['total']}")
        logger.info(f"  Successful: {result['successful']}")
        logger.info(f"  Failed: {result['failed']}")
        logger.info(f"  Duration: {result['duration_seconds']:.1f}s")

        logger.info("\n[4] Per-Company Results:")
        for ticker, company_result in result["results"].items():
            filing_date = company_result.get("filing_date", "N/A")
            fiscal_year = company_result.get("fiscal_year", "N/A")
            html_size = len(company_result.get("html_content", ""))
            logger.info(
                f"  {ticker}: FY{fiscal_year}, filed {filing_date}, "
                f"{html_size:,} chars"
            )

        if result["errors"]:
            logger.info("\n[5] Errors:")
            for ticker, error in result["errors"].items():
                logger.error(f"  {ticker}: {error}")

        # Test cache (should be fast)
        logger.info("\n[6] Testing cache retrieval...")
        cached_result = await controller.retrieve_parallel(
            tickers=TEST_TICKERS,
            force_refresh=False  # Use cache
        )

        assert cached_result["duration_seconds"] < 2, \
            f"Cached retrieval should be <2s, took {cached_result['duration_seconds']}s"

        logger.info(f"✅ Cache working! Retrieved in {cached_result['duration_seconds']:.2f}s")

        logger.info("\n" + "=" * 80)
        logger.info("🎉 PHASE 2 TEST PASSED!")
        logger.info("=" * 80)

        return True

    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = asyncio.run(test_parallel_retrieval())
    sys.exit(0 if success else 1)
