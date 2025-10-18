"""SEC EDGAR Navigator for 10-K retrieval"""
import asyncio
import re
from datetime import datetime
from typing import Dict, Optional
from playwright.async_api import async_playwright, Browser, Page
from bs4 import BeautifulSoup

from src.core.config import settings
from src.core.logging_config import logger
from src.core.exceptions import SECNavigationError


class SECNavigator:
    """Navigate SEC EDGAR and retrieve 10-K filings"""

    def __init__(self):
        self.user_agent = settings.sec_user_agent
        self.request_delay = settings.sec_request_delay
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    async def start(self):
        """Start browser instance with stealth settings"""
        playwright = await async_playwright().start()

        # Launch browser with args to avoid detection
        self.browser = await playwright.chromium.launch(
            headless=settings.browser_headless,
            args=[
                '--disable-blink-features=AutomationControlled',  # Hide automation
            ]
        )

        # Create context with realistic settings
        context = await self.browser.new_context(
            user_agent=self.user_agent,
            viewport={'width': 1920, 'height': 1080},
            # Add extra HTTP headers
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
            }
        )

        self.page = await context.new_page()

        # Override navigator.webdriver property
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        logger.info("Browser started for SEC navigation with stealth mode")


    async def close(self):
        """Close browser instance"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        logger.info("Browser closed")

    async def retrieve_10k(self, company: dict) -> dict:
        """
        Retrieve 10-K filing for a company

        Args:
            company: Dict with keys: name, ticker, cik, domain

        Returns:
            Dict with filing data:
            {
                "company": company,
                "filing_date": "2024-07-30",
                "fiscal_year": 2024,
                "html_url": "https://...",
                "html_content": "<!DOCTYPE html>...",
                "accession_number": "0000789019-24-000123",
                "status": "success"
            }
        """
        logger.info(f"Retrieving 10-K for {company['ticker']} (CIK: {company['cik']})")

        try:
            # Navigate to company's EDGAR page
            filings_url = await self._navigate_to_company_filings(company['cik'])

            # Find most recent 10-K
            filing_info = await self._find_recent_10k(filings_url)

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

    async def _navigate_to_company_filings(self, cik: str) -> str:
        """
        Navigate to company's EDGAR filings page

        Args:
            cik: Company CIK number (e.g., "0000789019")

        Returns:
            URL of company's filings page
        """
        # Clean CIK (remove leading zeros for URL)
        clean_cik = cik.lstrip('0')

        # Construct EDGAR filings URL
        # New EDGAR format: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-K&dateb=&owner=exclude&count=100
        filings_url = (
            f"https://www.sec.gov/cgi-bin/browse-edgar?"
            f"action=getcompany&CIK={cik}&type=10-K&dateb=&owner=exclude&count=40"
        )

        logger.info(f"Navigating to EDGAR: {filings_url}")

        await self.page.goto(filings_url, wait_until="networkidle", timeout=30000)

        # Wait for the table to be present
        try:
            await self.page.wait_for_selector("table.tableFile2", timeout=10000)
        except:
            logger.warning("Table not found with wait_for_selector, continuing anyway")

        # Wait a bit more for full render
        await asyncio.sleep(3)

        return filings_url

    async def _find_recent_10k(self, filings_url: str) -> dict:
        """
        Find most recent 10-K filing from EDGAR page

        Returns:
            Dict with filing_date, fiscal_year, html_url, accession_number
        """
        logger.info("Searching for most recent 10-K filing")

        # Get page content
        content = await self.page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # DEBUG: Save HTML for inspection
        with open('sec_filings_page.html', 'w') as f:
            f.write(content)
        logger.info(f"Saved page HTML to sec_filings_page.html ({len(content)} chars)")

        # Find all 10-K filings in the table
        # EDGAR uses a table with class "tableFile2"
        filing_table = soup.find('table', class_='tableFile2')

        # DEBUG: Try finding with find_all
        if not filing_table:
            all_tables = soup.find_all('table')
            logger.info(f"Found {len(all_tables)} tables total")
            for i, t in enumerate(all_tables):
                logger.info(f"  Table {i}: class={t.get('class')}")

            # Try to find by searching all tables
            for table in all_tables:
                table_class = table.get('class')
                if table_class and 'tableFile2' in table_class:
                    filing_table = table
                    logger.info("Found tableFile2 using manual search")
                    break

        if not filing_table:
            raise SECNavigationError("Could not find filings table on EDGAR page")

        rows = filing_table.find_all('tr')[1:]  # Skip header row

        if not rows:
            raise SECNavigationError("No 10-K filings found")

        # Priority: 2024 > 2025 > 2023
        for priority_year in [2024, 2025, 2023, 2022]:
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 4:
                    continue

                filing_type = cols[0].text.strip()
                filing_date = cols[3].text.strip()

                # Check if this is a 10-K (not 10-K/A amendment)
                if filing_type != '10-K':
                    continue

                # Parse filing date
                try:
                    filing_dt = datetime.strptime(filing_date, '%Y-%m-%d')
                    filing_year = filing_dt.year
                except:
                    continue

                # Check if this matches our priority year
                if filing_year == priority_year:
                    # Get documents link
                    documents_link = cols[1].find('a', id='documentsbutton')
                    if not documents_link:
                        continue

                    documents_href = documents_link.get('href')
                    if not documents_href:
                        continue

                    # Get accession number from the link
                    # Format: /cgi-bin/viewer?action=view&cik=789019&accession_number=0000789019-24-000105&xbrl_type=v
                    accession_match = re.search(r'accession_number=([\d-]+)', documents_href)
                    if not accession_match:
                        continue

                    accession_number = accession_match.group(1)

                    # Construct full URL
                    if not documents_href.startswith('http'):
                        documents_url = f"https://www.sec.gov{documents_href}"
                    else:
                        documents_url = documents_href

                    logger.info(f"Found 10-K: FY{filing_year}, filed {filing_date}")

                    # Now navigate to documents page to find HTML file
                    html_url = await self._find_html_document(documents_url, accession_number)

                    return {
                        "filing_date": filing_date,
                        "fiscal_year": filing_year,
                        "html_url": html_url,
                        "accession_number": accession_number
                    }

        raise SECNavigationError("No suitable 10-K filing found (looked for 2024, 2025, 2023, 2022)")

    async def _find_html_document(self, documents_url: str, accession_number: str) -> str:
        """
        Find HTML document URL from documents page

        Args:
            documents_url: URL of EDGAR documents page
            accession_number: Filing accession number

        Returns:
            Direct URL to HTML document
        """
        logger.info(f"Navigating to documents page: {documents_url}")

        await self.page.goto(documents_url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(2)

        content = await self.page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Find the document table
        doc_table = soup.find('table', class_='tableFile')

        if not doc_table:
            raise SECNavigationError("Could not find documents table")

        rows = doc_table.find_all('tr')[1:]  # Skip header

        # Look for the main HTML document
        # Typically named like "d12345d10k.htm" or similar
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 3:
                continue

            doc_type = cols[3].text.strip() if len(cols) > 3 else ''
            filename = cols[2].text.strip()

            # Look for 10-K document (not exhibits)
            if '10-K' in doc_type or 'd10k' in filename.lower():
                doc_link = cols[2].find('a')
                if not doc_link:
                    continue

                doc_href = doc_link.get('href')
                if not doc_href:
                    continue

                # Construct full URL
                if not doc_href.startswith('http'):
                    html_url = f"https://www.sec.gov{doc_href}"
                else:
                    html_url = doc_href

                logger.info(f"Found HTML document: {html_url}")
                return html_url

        raise SECNavigationError("Could not find HTML document on documents page")

    async def _download_10k_html(self, html_url: str) -> str:
        """
        Download 10-K HTML content

        Args:
            html_url: Direct URL to HTML document

        Returns:
            HTML content as string
        """
        logger.info(f"Downloading HTML from: {html_url}")

        await self.page.goto(html_url, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(2)

        html_content = await self.page.content()

        if len(html_content) < 10000:
            raise SECNavigationError(f"HTML content too small ({len(html_content)} chars), likely invalid")

        logger.info(f"Downloaded {len(html_content)} characters of HTML")

        return html_content
