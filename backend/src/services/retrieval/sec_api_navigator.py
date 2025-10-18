"""SEC EDGAR API Navigator (no browser needed)"""
import asyncio
import aiohttp
import re
from datetime import datetime
from typing import Dict, Optional
from bs4 import BeautifulSoup

from src.core.config import settings
from src.core.logging_config import logger
from src.core.exceptions import SECNavigationError


class SECAPINavigator:
    """Navigate SEC EDGAR using official APIs (no browser)"""

    def __init__(self):
        self.user_agent = settings.sec_user_agent
        self.request_delay = settings.sec_request_delay
        # Headers for SEC API - don't set Host, let aiohttp handle it
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'application/json'
        }

    async def retrieve_10k(self, company: dict) -> dict:
        """
        Retrieve 10-K filing for a company using SEC APIs

        Args:
            company: Dict with keys: name, ticker, cik, domain

        Returns:
            Dict with filing data
        """
        logger.info(f"Retrieving 10-K for {company['ticker']} (CIK: {company['cik']})")

        try:
            # Get company submissions data from SEC API
            submissions = await self._get_company_submissions(company['cik'])

            # Find most recent 10-K
            filing_info = self._find_recent_10k_from_submissions(submissions)

            # Download HTML content
            html_content = await self._download_10k_html(filing_info['html_url'])

            # Add delay to respect rate limits
            await asyncio.sleep(self.request_delay)

            result = {
                "company": company,
                "filing_date": filing_info['filing_date'],
                "fiscal_year": filing_info['fiscal_year'],
                "html_url": filing_info['html_url'],
                "html_content": html_content,
                "accession_number": filing_info['accession_number'],
                "status": "success"
            }

            logger.info(
                f"Successfully retrieved 10-K for {company['ticker']}: "
                f"FY{filing_info['fiscal_year']}, {len(html_content)} chars"
            )

            return result

        except Exception as e:
            logger.error(f"Failed to retrieve 10-K for {company['ticker']}: {e}")
            raise SECNavigationError(f"10-K retrieval failed: {e}")

    async def _get_company_submissions(self, cik: str) -> dict:
        """
        Get company submissions from SEC API

        Args:
            cik: Company CIK (with leading zeros)

        Returns:
            Submissions data dict
        """
        # SEC API endpoint
        # Format: https://data.sec.gov/submissions/CIK##########.json
        api_url = f"https://data.sec.gov/submissions/CIK{cik}.json"

        logger.info(f"Fetching submissions from SEC API: {api_url}")

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    raise SECNavigationError(
                        f"SEC API returned status {response.status}"
                    )

                data = await response.json()
                return data

    def _find_recent_10k_from_submissions(self, submissions: dict) -> dict:
        """
        Find most recent 10-K from submissions data

        Args:
            submissions: SEC API submissions response

        Returns:
            Dict with filing_date, fiscal_year, html_url, accession_number
        """
        recent_filings = submissions['filings']['recent']

        # Find 10-K filings
        forms = recent_filings['form']
        filing_dates = recent_filings['filingDate']
        accession_numbers = recent_filings['accessionNumber']
        primary_documents = recent_filings['primaryDocument']

        # Priority: 2024 > 2025 > 2023 > 2022
        for priority_year in [2024, 2025, 2023, 2022]:
            for i, form in enumerate(forms):
                if form != '10-K':
                    continue

                filing_date = filing_dates[i]
                filing_year = int(filing_date.split('-')[0])

                if filing_year == priority_year:
                    accession_number = accession_numbers[i]
                    primary_doc = primary_documents[i]

                    # Construct URL to HTML document
                    # Format: https://www.sec.gov/Archives/edgar/data/CIK/ACCESSION/DOCUMENT
                    cik_no_zeros = submissions['cik']
                    accession_no_dashes = accession_number.replace('-', '')

                    html_url = (
                        f"https://www.sec.gov/Archives/edgar/data/"
                        f"{cik_no_zeros}/{accession_no_dashes}/{primary_doc}"
                    )

                    logger.info(f"Found 10-K: FY{filing_year}, filed {filing_date}")

                    return {
                        "filing_date": filing_date,
                        "fiscal_year": filing_year,
                        "html_url": html_url,
                        "accession_number": accession_number
                    }

        raise SECNavigationError(
            "No suitable 10-K filing found (looked for 2024, 2025, 2023, 2022)"
        )

    async def _download_10k_html(self, html_url: str) -> str:
        """
        Download 10-K HTML content

        Args:
            html_url: Direct URL to HTML document

        Returns:
            HTML content as string
        """
        logger.info(f"Downloading HTML from: {html_url}")

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(html_url) as response:
                if response.status != 200:
                    raise SECNavigationError(
                        f"Failed to download HTML: status {response.status}"
                    )

                html_content = await response.text()

                if len(html_content) < 10000:
                    raise SECNavigationError(
                        f"HTML content too small ({len(html_content)} chars), likely invalid"
                    )

                logger.info(f"Downloaded {len(html_content)} characters of HTML")

                return html_content
