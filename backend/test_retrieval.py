"""Test script for Phase 1: SEC Retrieval"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.retrieval.retrieval_service import RetrievalService
from src.core.logging_config import setup_logging, logger


# Microsoft company info
MICROSOFT = {
    "name": "Microsoft",
    "ticker": "MSFT",
    "cik": "0000789019",
    "domain": "microsoft.com"
}


async def test_retrieval():
    """Test 10-K retrieval for Microsoft"""

    setup_logging("INFO")

    logger.info("=" * 80)
    logger.info("PHASE 1 TEST: SEC 10-K Retrieval for Microsoft (MSFT)")
    logger.info("=" * 80)

    service = RetrievalService()

    try:
        # Test retrieval
        logger.info("\n[1] Testing fresh retrieval from SEC EDGAR...")
        result = await service.retrieve_10k(MICROSOFT, force_refresh=True)

        # Validate result
        logger.info("\n[2] Validating result...")

        assert result['status'] == 'success', "Status should be 'success'"
        assert result['company']['ticker'] == 'MSFT', "Ticker should be MSFT"
        assert len(result['html_content']) > 50000, f"HTML too small: {len(result['html_content'])} chars"
        assert result['filing_date'], "Filing date should exist"
        assert result['fiscal_year'] in [2022, 2023, 2024, 2025], f"Unexpected fiscal year: {result['fiscal_year']}"
        assert result['accession_number'], "Accession number should exist"
        assert result['html_url'], "HTML URL should exist"

        logger.info("✅ All validations passed!")

        logger.info("\n[3] Result Summary:")
        logger.info(f"  Company: {result['company']['name']} ({result['company']['ticker']})")
        logger.info(f"  Filing Date: {result['filing_date']}")
        logger.info(f"  Fiscal Year: {result['fiscal_year']}")
        logger.info(f"  Accession Number: {result['accession_number']}")
        logger.info(f"  HTML URL: {result['html_url']}")
        logger.info(f"  HTML Size: {len(result['html_content']):,} characters")

        # Test caching
        logger.info("\n[4] Testing cache retrieval...")
        cached_result = await service.retrieve_10k(MICROSOFT, force_refresh=False)

        assert cached_result == result, "Cached result should match original"
        logger.info("✅ Cache working correctly!")

        # Check cache info
        cache_info = service.get_cached_info('MSFT')
        if cache_info:
            logger.info("\n[5] Cache Metadata:")
            logger.info(f"  Cached at: {cache_info['cached_at']}")
            logger.info(f"  Ticker: {cache_info['metadata']['ticker']}")
            logger.info(f"  Filing date: {cache_info['metadata']['filing_date']}")
            logger.info(f"  Fiscal year: {cache_info['metadata']['fiscal_year']}")

        logger.info("\n" + "=" * 80)
        logger.info("🎉 PHASE 1 TEST PASSED!")
        logger.info("=" * 80)

        return True

    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = asyncio.run(test_retrieval())
    sys.exit(0 if success else 1)
