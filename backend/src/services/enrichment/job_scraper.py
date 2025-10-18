"""AI job scraping using Browser-Use"""
import asyncio
from typing import List
from browser_use import Agent
from langchain_anthropic import ChatAnthropic

from src.core.config import settings
from src.core.logging_config import logger


class AIJobScraper:
    """Scrape AI job postings using Browser-Use agent"""

    def __init__(self):
        # Use Anthropic Claude for browser agent
        if settings.anthropic_api_key:
            self.llm = ChatAnthropic(
                model_name="claude-3-5-sonnet-20241022",
                api_key=settings.anthropic_api_key
            )
            logger.info("AIJobScraper initialized with Browser-Use + Claude")
        else:
            self.llm = None
            logger.warning("AIJobScraper: ANTHROPIC_API_KEY not set - Browser-Use disabled")

    async def scrape_ai_jobs(self, company: dict) -> dict:
        """
        Scrape AI-related jobs from company career page

        Args:
            company: Company dict with name, domain, ticker

        Returns:
            Dict with AI jobs and tech stack
        """
        company_name = company["name"]
        domain = company["domain"]
        ticker = company["ticker"]

        logger.info(f"Starting Browser-Use job scrape for {company_name}")

        # If no API key, return mock data
        if not self.llm:
            logger.warning(f"Skipping Browser-Use for {ticker} - no API key")
            return {
                "company": company,
                "ai_jobs": [],
                "tech_stack": [],
                "source": f"careers.{domain}",
                "status": "skipped",
                "note": "ANTHROPIC_API_KEY not configured"
            }

        try:
            # Create Browser-Use agent with task
            task = f"""
            Navigate to {company_name}'s career page (likely at https://{domain}/careers or https://careers.{domain}).

            Search for AI-related jobs using keywords: "AI", "Machine Learning", "Artificial Intelligence", "ML Engineer", "Data Scientist".

            Extract up to 10 AI-related job postings and return the following information:
            - Job title
            - Location (if available)
            - Required tech stack/skills mentioned

            Also identify what AI technologies the company is using based on job requirements.

            Return results as a structured list.
            """

            agent = Agent(
                task=task,
                llm=self.llm,
                max_actions=15  # Limit actions for speed
            )

            # Run the agent
            logger.info(f"Running Browser-Use agent for {ticker}")
            result = await agent.run()

            # Parse agent output
            jobs = self._parse_agent_output(result)

            logger.info(
                f"Scraped {len(jobs.get('jobs', []))} AI jobs for {company_name}, "
                f"tech stack: {len(jobs.get('tech_stack', []))} items"
            )

            return {
                "company": company,
                "ai_jobs": jobs.get("jobs", []),
                "tech_stack": jobs.get("tech_stack", []),
                "source": f"careers.{domain}",
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Job scraping failed for {company_name}: {e}")
            return {
                "company": company,
                "ai_jobs": [],
                "tech_stack": [],
                "source": f"careers.{domain}",
                "status": "failed",
                "error": str(e)
            }

    def _parse_agent_output(self, result) -> dict:
        """
        Parse Browser-Use agent output into structured data

        Args:
            result: Agent result object

        Returns:
            Dict with jobs and tech_stack
        """
        # Get the agent's final answer
        output_text = str(result)

        # Simple parsing - extract job info from text
        # In production, would use LLM to structure this better
        jobs = []
        tech_stack = set()

        # Common tech keywords to look for
        tech_keywords = [
            "Python", "TensorFlow", "PyTorch", "Kubernetes", "Docker",
            "AWS", "Azure", "GCP", "React", "Node.js", "Go", "Rust",
            "LangChain", "LlamaIndex", "Hugging Face", "OpenAI", "Anthropic"
        ]

        lines = output_text.split('\n')
        current_job = {}

        for line in lines:
            line = line.strip()

            # Look for job titles (usually have keywords)
            if any(kw in line.lower() for kw in ["engineer", "scientist", "researcher", "developer"]):
                if current_job:
                    jobs.append(current_job)
                current_job = {"title": line}

            # Look for tech stack mentions
            for tech in tech_keywords:
                if tech.lower() in line.lower():
                    tech_stack.add(tech)
                    if current_job and "tech" not in current_job:
                        current_job["tech"] = []
                    if current_job:
                        current_job["tech"].append(tech)

        # Add last job
        if current_job:
            jobs.append(current_job)

        # Limit to 10 jobs
        jobs = jobs[:10]

        return {
            "jobs": jobs,
            "tech_stack": sorted(list(tech_stack))
        }

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
