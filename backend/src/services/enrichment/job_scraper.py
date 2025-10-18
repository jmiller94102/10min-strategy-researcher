"""Job scraping using Browser-Use Cloud API"""
import asyncio
from typing import List
from browser_use import Agent, ChatBrowserUse
from dotenv import load_dotenv

from src.core.config import settings
from src.core.logging_config import logger

# Load environment variables
load_dotenv()


class AIJobScraper:
    """Scrape job postings using Browser-Use Cloud API"""

    def __init__(self):
        """Initialize job scraper with Browser-Use cloud"""
        # Use Browser-Use Cloud API (handles browser infrastructure)
        try:
            # Create Browser-Use cloud LLM (manages browser automatically)
            self.llm = ChatBrowserUse()

            # No browser object needed - Browser-Use cloud handles it
            self.browser = None

            logger.info("AIJobScraper initialized with Browser-Use Cloud API")
            logger.info(f"API Key configured: {bool(settings.browser_use_api_key)}")
        except Exception as e:
            self.llm = None
            self.browser = None
            logger.warning(f"AIJobScraper: Failed to initialize Browser-Use Cloud: {e}")

    async def scrape_ai_jobs(self, company: dict) -> dict:
        """
        Scrape ALL job postings from company career page

        Args:
            company: Company dict with name, domain, ticker

        Returns:
            Dict with all jobs and tech stack matching frontend interface
        """
        company_name = company["name"]
        domain = company["domain"]
        ticker = company["ticker"]

        logger.info(f"Starting Browser-Use job scrape for {company_name}")

        # If no LLM, return empty data
        if not self.llm:
            logger.warning(f"Skipping Browser-Use for {ticker} - Browser-Use not configured")
            return {
                "company": company,
                "ai_jobs": [],
                "tech_stack": [],
                "source": f"careers.{domain}",
                "status": "skipped",
                "note": "Browser-Use not configured"
            }

        try:
            # Create Browser-Use agent to find jobs
            task = f"""
            Go to {company_name}'s career page and find job openings.

            Try these URLs:
            - https://{domain}/careers
            - https://careers.{domain}

            Find 3 job postings.

            For each job you find, extract:
            - Job title
            - Location (city, state/country, remote/hybrid/onsite)
            - Direct URL to the job posting
            - Any technologies or skills mentioned (Python, Java, AWS, React, etc.)
            - Job category (Engineering, Sales, Marketing, etc.)

            Return the 3 job titles with their details.
            """

            # Browser-Use Cloud handles browser automatically - no browser param needed
            agent = Agent(
                task=task,
                llm=self.llm,
                max_actions=15,  # Limit actions for faster execution (3 jobs),
                use_vision=True
            )

            # Run the agent
            logger.info(f"Running Browser-Use agent for {ticker}")
            result = await agent.run()

            # Parse agent output into structured format
            jobs_data = self._parse_agent_output(result, company_name, domain)

            logger.info(
                f"Scraped {len(jobs_data.get('jobs', []))} jobs for {company_name}, "
                f"tech stack: {len(jobs_data.get('tech_stack', []))} items"
            )

            return {
                "company": company,
                "ai_jobs": jobs_data.get("jobs", []),
                "tech_stack": jobs_data.get("tech_stack", []),
                "total_jobs": jobs_data.get("total_jobs_found", 0),
                "ai_jobs_count": jobs_data.get("ai_jobs_found", 0),
                "source": f"careers.{domain}",
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Job scraping failed for {company_name}: {e}")
            return {
                "company": company,
                "ai_jobs": [],
                "tech_stack": [],
                "total_jobs": 0,
                "ai_jobs_count": 0,
                "source": f"careers.{domain}",
                "status": "failed",
                "error": str(e)
            }

    def _parse_agent_output(self, result, company_name: str, domain: str) -> dict:
        """
        Parse Browser-Use agent output into structured data

        Args:
            result: Agent result object from Browser-Use (AgentHistoryList)
            company_name: Company name for fallback URL construction
            domain: Company domain for fallback URL construction

        Returns:
            Dict with jobs and tech_stack matching frontend JobPosting interface
        """
        import re
        from datetime import datetime

        jobs = []
        tech_stack_set = set()

        # Common tech keywords to extract
        tech_keywords = [
            "Python", "TensorFlow", "PyTorch", "Kubernetes", "Docker",
            "AWS", "Azure", "GCP", "React", "Node.js", "Go", "Rust",
            "LangChain", "LlamaIndex", "Hugging Face", "OpenAI", "Anthropic",
            "Java", "C++", "Scala", "Spark", "Hadoop", "MLflow", "Airflow",
            "VMware", "ESXi", "vCenter", "NSX", "vSAN", "CompTIA"
        ]

        # Browser-Use Cloud returns AgentHistoryList with extracted content in ActionResults
        if hasattr(result, 'action_results'):
            action_results = result.action_results()
            logger.info(f"Parsing Browser-Use AgentHistoryList with {len(action_results)} action results")

            for i, action_result in enumerate(action_results):
                # Look for extracted content from the agent
                if hasattr(action_result, 'extracted_content') and action_result.extracted_content:
                    content = action_result.extracted_content

                    # Check if this is an extracted job posting (contains <url> from a job posting)
                    # Skip navigation/non-job URLs
                    has_url = '<url>' in content
                    has_job_url = 'jobs.careers' in content
                    is_long_enough = len(content) > 200

                    logger.info(f"ActionResult {i}: has_url={has_url}, has_job_url={has_job_url}, len={len(content)}")

                    if has_url and has_job_url and is_long_enough:
                        logger.info(f"Found potential job posting in ActionResult {i}")
                        job_data = self._parse_extracted_job(content, tech_keywords)
                        if job_data:
                            logger.info(f"Successfully parsed job: {job_data['title']}")
                            jobs.append(job_data)
                            tech_stack_set.update(job_data["tech_stack"])
                        else:
                            logger.warning(f"Failed to parse job from ActionResult {i}")

        # If we found jobs via extracted content, return them
        if jobs:
            logger.info(f"Successfully parsed {len(jobs)} jobs from Browser-Use extracted content")
            return {
                "jobs": jobs,
                "tech_stack": sorted(list(tech_stack_set)),
                "total_jobs_found": len(jobs),
                "ai_jobs_found": len(jobs)
            }

        # Fallback: Try to parse as text
        logger.info("Using fallback text parsing for job data")
        output_text = str(result)
        lines = output_text.split('\n')
        current_job = None

        for line in lines:
            line = line.strip()

            # Look for job titles in plain text
            if any(kw in line.lower() for kw in ["engineer", "scientist", "researcher", "developer", "architect", "technician", "manager"]):
                if current_job:
                    jobs.append(current_job)

                current_job = {
                    "title": line,
                    "location": "Location not specified",
                    "job_url": f"https://careers.{domain}",
                    "tech_stack": [],
                    "seniority": self._infer_seniority(line, ""),
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "remote": False
                }

            # Look for tech stack mentions
            if current_job:
                for tech in tech_keywords:
                    if tech.lower() in line.lower() and tech not in current_job["tech_stack"]:
                        current_job["tech_stack"].append(tech)
                        tech_stack_set.add(tech)

        # Add last job
        if current_job:
            jobs.append(current_job)

        return {
            "jobs": jobs[:3],  # Limit to 3 jobs
            "tech_stack": sorted(list(tech_stack_set)),
            "total_jobs_found": len(jobs),
            "ai_jobs_found": len(jobs)
        }

    def _parse_extracted_job(self, content: str, tech_keywords: list) -> dict:
        """
        Parse a single extracted job posting from Browser-Use

        Args:
            content: Extracted content string with structured job data
            tech_keywords: List of technology keywords to search for

        Returns:
            Dict with job details, or None if parsing fails
        """
        from datetime import datetime
        import re

        try:
            # Extract URL from <url> tags
            url_match = re.search(r'<url>\s*(\S+)\s*</url>', content)
            job_url = url_match.group(1) if url_match else None

            # Try to extract title from the URL as fallback
            title_from_url = None
            if job_url:
                # URL format: .../job/1234567/Job-Title-With-Dashes
                url_title_match = re.search(r'/job/\d+/([^/\?]+)', job_url)
                if url_title_match:
                    title_from_url = url_title_match.group(1).replace('-', ' ')

            # Extract Job Title (case insensitive, multiple patterns)
            title = None

            # Pattern 1: Key-value format "Job title: ..."
            title_match = re.search(r'Job [Tt]itle:\s*(.+?)(?:\n|$)', content)
            if title_match:
                title = title_match.group(1).strip()

            # Pattern 2: Table format "| Job title | ... |" (first row after headers)
            if not title and '| Job' in content:
                table_match = re.search(r'\|\s*([^|]+?)\s*\|', content)
                if table_match:
                    title = table_match.group(1).strip()

            # Fallback to URL-derived title
            if not title or title == "Unavailable":
                title = title_from_url or "Unknown Position"

            # Extract Location (case insensitive, handle multi-line format)
            # Look for patterns like "Location: City, State, Country" or nested "City, State/Country: ..."
            location = "Location not specified"

            # Pattern 1: Direct "Location: City, State..."
            location_match = re.search(r'Location[:\s]+([^:\n]+(?:,\s*[^:\n]+)*)', content, re.IGNORECASE)
            if location_match:
                potential_location = location_match.group(1).strip()
                # Filter out bullet points and "City, State/Country:" headers
                if not potential_location.startswith('*') and 'City, State' not in potential_location:
                    location = potential_location

            # Pattern 2: Nested format "City, State/Country: Actual Location"
            if location == "Location not specified" or 'City, State' in location:
                nested_match = re.search(r'City,\s*State/Country:\s*([^\n*]+)', content, re.IGNORECASE)
                if nested_match:
                    location = nested_match.group(1).strip()

            # Find all tech keywords in the entire content
            found_tech = set()
            for tech in tech_keywords:
                if tech.lower() in content.lower():
                    found_tech.add(tech)

            # Extract posted date if available
            date_match = re.search(r'Date posted:\s*(.+)', content, re.IGNORECASE)
            if date_match:
                posted_date = date_match.group(1).strip()
            else:
                posted_date = datetime.now().strftime("%Y-%m-%d")

            # Determine if remote
            remote = self._infer_remote(location) or 'remote' in content.lower() or 'hybrid' in content.lower()

            return {
                "title": title,
                "location": location,
                "job_url": job_url or "URL not available",
                "tech_stack": sorted(list(found_tech)),
                "seniority": self._infer_seniority(title, ""),
                "posted_date": posted_date,
                "remote": remote
            }

        except Exception as e:
            logger.warning(f"Failed to parse extracted job: {e}")
            return None

    def _infer_seniority(self, title: str, explicit_seniority: str) -> str:
        """Infer seniority level from job title"""
        if explicit_seniority and explicit_seniority in ["junior", "mid", "senior", "staff", "principal"]:
            return explicit_seniority

        title_lower = title.lower()

        if any(kw in title_lower for kw in ["principal", "distinguished", "fellow"]):
            return "principal"
        elif any(kw in title_lower for kw in ["staff", "lead", "architect"]):
            return "staff"
        elif any(kw in title_lower for kw in ["senior", "sr"]):
            return "senior"
        elif any(kw in title_lower for kw in ["junior", "jr", "associate", "entry"]):
            return "junior"
        else:
            return "mid"

    def _infer_remote(self, location: str) -> bool:
        """Infer if job is remote from location string"""
        location_lower = location.lower()
        return any(kw in location_lower for kw in ["remote", "work from home", "wfh", "anywhere"])

    async def scrape_jobs_with_retry(
        self,
        company: dict,
        max_retries: int = 2
    ) -> dict:
        """
        Scrape jobs with retry logic

        Args:
            company: Company dict
            max_retries: Maximum retry attempts

        Returns:
            Scraping result dict
        """
        for attempt in range(max_retries):
            try:
                result = await self.scrape_ai_jobs(company)
                if result["status"] == "success":
                    return result

                # Retry if failed
                logger.warning(
                    f"Attempt {attempt + 1} failed for {company['ticker']}, retrying..."
                )
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"All retries failed for {company['ticker']}: {e}")
                    return {
                        "company": company,
                        "ai_jobs": [],
                        "tech_stack": [],
                        "status": "failed",
                        "error": str(e)
                    }

        return result
