"""10-K Retrieval Service with caching"""
from datetime import timedelta
from typing import Dict, Optional

from src.core.config import settings
from src.core.logging_config import logger
from src.utils.cache import FileCache
from src.services.retrieval.sec_api_navigator import SECAPINavigator


class RetrievalService:
    """Service for retrieving 10-K filings with caching"""

    def __init__(self):
        self.cache = FileCache(cache_dir=settings.cache_dir)
        self.cache_ttl = timedelta(days=settings.cache_ttl_days)

    async def retrieve_10k(
        self,
        company: dict,
        force_refresh: bool = False
    ) -> dict:
        """
        Retrieve 10-K filing for a company (with caching)

        Args:
            company: Dict with name, ticker, cik, domain
            force_refresh: If True, bypass cache and fetch fresh data

        Returns:
            Dict with filing data including HTML content
        """
        ticker = company['ticker']
        cache_key = f"10k:{ticker}"

        logger.info(f"Retrieving 10-K for {ticker} (force_refresh={force_refresh})")

        # Check cache first (unless force_refresh)
        if not force_refresh and settings.enable_caching:
            cached_data = self.cache.get(cache_key, max_age=self.cache_ttl)

            if cached_data:
                logger.info(f"Using cached 10-K for {ticker}")
                return cached_data

        # Cache miss or force refresh - retrieve from SEC
        logger.info(f"Fetching fresh 10-K from SEC for {ticker}")

        navigator = SECAPINavigator()
        result = await navigator.retrieve_10k(company)

        # Cache the result
        if settings.enable_caching:
            self.cache.set(
                cache_key,
                result,
                metadata={
                    "ticker": ticker,
                    "filing_date": result['filing_date'],
                    "fiscal_year": result['fiscal_year']
                }
            )

        return result

    def get_cached_info(self, ticker: str) -> Optional[dict]:
        """Get cache metadata without loading full data"""
        cache_key = f"10k:{ticker}"
        return self.cache.get_info(cache_key)

    def clear_cache(self, ticker: Optional[str] = None):
        """Clear cache for specific ticker or all"""
        if ticker:
            cache_key = f"10k:{ticker}"
            self.cache.delete(cache_key)
            logger.info(f"Cleared cache for {ticker}")
        else:
            self.cache.clear()
            logger.info("Cleared all cache")
