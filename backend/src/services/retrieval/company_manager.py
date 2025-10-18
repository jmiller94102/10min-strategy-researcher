"""Company list management and validation"""
from typing import Optional

from src.core.exceptions import InvalidTickerError
from src.core.logging_config import logger


# 10 tech companies for AI intelligence analysis
COMPANIES = [
    {"name": "Microsoft", "ticker": "MSFT", "cik": "0000789019", "domain": "microsoft.com"},
    {"name": "Apple", "ticker": "AAPL", "cik": "0000320193", "domain": "apple.com"},
    {"name": "NVIDIA", "ticker": "NVDA", "cik": "0001045810", "domain": "nvidia.com"},
    {"name": "Alphabet", "ticker": "GOOGL", "cik": "0001652044", "domain": "google.com"},
    {"name": "Amazon", "ticker": "AMZN", "cik": "0001018724", "domain": "amazon.com"},
    {"name": "Meta", "ticker": "META", "cik": "0001326801", "domain": "meta.com"},
    {"name": "Tesla", "ticker": "TSLA", "cik": "0001318605", "domain": "tesla.com"},
    {"name": "Salesforce", "ticker": "CRM", "cik": "0001108524", "domain": "salesforce.com"},
    {"name": "Adobe", "ticker": "ADBE", "cik": "0000796343", "domain": "adobe.com"},
    {"name": "Netflix", "ticker": "NFLX", "cik": "0001065280", "domain": "netflix.com"}
]


class CompanyManager:
    """Manages company list and validation"""

    def __init__(self):
        self.companies_by_ticker = {c["ticker"]: c for c in COMPANIES}
        logger.info(f"CompanyManager initialized with {len(COMPANIES)} companies")

    def get_company(self, ticker: str) -> dict:
        """
        Get company by ticker (case-insensitive)

        Args:
            ticker: Company ticker symbol

        Returns:
            Company dict with name, ticker, cik, domain

        Raises:
            InvalidTickerError: If ticker not found
        """
        ticker_upper = ticker.upper()

        if ticker_upper not in self.companies_by_ticker:
            logger.error(f"Invalid ticker: {ticker}")
            raise InvalidTickerError(ticker)

        return self.companies_by_ticker[ticker_upper]

    def get_companies(self, tickers: list[str]) -> list[dict]:
        """
        Get multiple companies by tickers

        Args:
            tickers: List of ticker symbols

        Returns:
            List of company dicts

        Raises:
            InvalidTickerError: If any ticker not found
        """
        return [self.get_company(ticker) for ticker in tickers]

    def get_all_companies(self) -> list[dict]:
        """Get all supported companies"""
        return COMPANIES.copy()

    def get_all_tickers(self) -> list[str]:
        """Get all supported ticker symbols"""
        return [c["ticker"] for c in COMPANIES]

    def is_valid_ticker(self, ticker: str) -> bool:
        """Check if ticker is supported"""
        return ticker.upper() in self.companies_by_ticker

    def get_company_name(self, ticker: str) -> Optional[str]:
        """Get company name by ticker (returns None if not found)"""
        try:
            return self.get_company(ticker)["name"]
        except InvalidTickerError:
            return None
