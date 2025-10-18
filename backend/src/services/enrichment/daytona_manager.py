"""Daytona.io environment management for parallel browser execution"""
import asyncio
from typing import Dict, List, Optional
from daytona_sdk import Daytona

from src.core.config import settings
from src.core.logging_config import logger


class DaytonaEnvironmentManager:
    """Manages Daytona dev environments for parallel enrichment"""

    def __init__(self):
        # Daytona SDK uses environment variable DAYTONA_API_KEY
        # or pass configuration directly
        try:
            self.client = Daytona()
            self.active_workspaces: Dict[str, any] = {}
            logger.info("DaytonaEnvironmentManager initialized")
        except Exception as e:
            logger.warning(f"Daytona client initialization failed: {e}")
            self.client = None
            self.active_workspaces: Dict[str, any] = {}

    async def create_workspace(self, company_ticker: str) -> dict:
        """
        Create Daytona workspace for a company

        Args:
            company_ticker: Company ticker symbol

        Returns:
            Workspace info dict
        """
        workspace_name = f"{settings.daytona_workspace_prefix}-{company_ticker.lower()}"

        if not self.client:
            return {
                "ticker": company_ticker,
                "workspace_id": None,
                "name": workspace_name,
                "status": "skipped",
                "note": "Daytona client not initialized"
            }

        try:
            logger.info(f"Creating Daytona workspace: {workspace_name}")

            # Create workspace with browser dependencies
            workspace = await asyncio.to_thread(
                self.client.create_workspace,
                name=workspace_name,
                image="python:3.11-slim",
                packages=[
                    "browser-use",
                    "playwright",
                    "beautifulsoup4",
                    "aiohttp"
                ]
            )

            self.active_workspaces[company_ticker] = workspace

            logger.info(f"Created workspace {workspace_name}: {workspace.get('id', 'N/A')}")

            return {
                "ticker": company_ticker,
                "workspace_id": workspace.get("id"),
                "name": workspace_name,
                "status": "ready"
            }

        except Exception as e:
            logger.error(f"Failed to create workspace for {company_ticker}: {e}")
            return {
                "ticker": company_ticker,
                "workspace_id": None,
                "name": workspace_name,
                "status": "failed",
                "error": str(e)
            }

    async def create_all_workspaces(self, tickers: List[str]) -> Dict[str, dict]:
        """
        Create workspaces for multiple companies in parallel

        Args:
            tickers: List of company tickers

        Returns:
            Dict mapping ticker to workspace info
        """
        logger.info(f"Creating {len(tickers)} Daytona workspaces in parallel")

        tasks = [self.create_workspace(ticker) for ticker in tickers]
        results = await asyncio.gather(*tasks)

        workspaces = {result["ticker"]: result for result in results}

        successful = sum(1 for r in results if r["status"] == "ready")
        logger.info(f"Created {successful}/{len(tickers)} workspaces successfully")

        return workspaces

    async def execute_in_workspace(
        self,
        workspace_id: str,
        script: str,
        timeout: int = 60
    ) -> dict:
        """
        Execute Python script in Daytona workspace

        Args:
            workspace_id: Workspace ID
            script: Python code to execute
            timeout: Execution timeout in seconds

        Returns:
            Execution result dict
        """
        try:
            logger.info(f"Executing script in workspace {workspace_id}")

            result = await asyncio.to_thread(
                self.client.execute,
                workspace_id=workspace_id,
                command=f"python -c '{script}'",
                timeout=timeout
            )

            return {
                "status": "success",
                "output": result.get("output", ""),
                "error": result.get("error")
            }

        except Exception as e:
            logger.error(f"Execution failed in workspace {workspace_id}: {e}")
            return {
                "status": "failed",
                "output": "",
                "error": str(e)
            }

    async def cleanup_workspace(self, workspace_id: str):
        """Delete a Daytona workspace"""
        try:
            logger.info(f"Cleaning up workspace {workspace_id}")
            await asyncio.to_thread(self.client.delete_workspace, workspace_id)
            logger.info(f"Deleted workspace {workspace_id}")
        except Exception as e:
            logger.error(f"Failed to cleanup workspace {workspace_id}: {e}")

    async def cleanup_all(self):
        """Cleanup all active workspaces"""
        logger.info(f"Cleaning up {len(self.active_workspaces)} workspaces")

        cleanup_tasks = []
        for ticker, workspace in self.active_workspaces.items():
            if workspace and workspace.get("id"):
                cleanup_tasks.append(self.cleanup_workspace(workspace["id"]))

        await asyncio.gather(*cleanup_tasks, return_exceptions=True)

        self.active_workspaces.clear()
        logger.info("All workspaces cleaned up")

    def get_workspace(self, ticker: str) -> Optional[dict]:
        """Get workspace info for a ticker"""
        return self.active_workspaces.get(ticker)
