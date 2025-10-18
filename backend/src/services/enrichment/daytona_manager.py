"""Daytona.io environment management for parallel browser execution"""
import asyncio
from typing import Dict, List, Optional
from daytona_sdk import Daytona, DaytonaConfig, CreateSandboxFromImageParams

from src.core.config import settings
from src.core.logging_config import logger


class DaytonaEnvironmentManager:
    """Manages Daytona dev environments for parallel enrichment"""

    def __init__(self):
        # Daytona SDK uses environment variables:
        # DAYTONA_API_KEY, DAYTONA_API_URL, DAYTONA_TARGET
        try:
            # Use environment variables (recommended)
            self.client = Daytona()
            self.active_sandboxes: Dict[str, any] = {}
            logger.info("DaytonaEnvironmentManager initialized")
        except Exception as e:
            logger.warning(f"Daytona client initialization failed: {e}")
            self.client = None
            self.active_sandboxes: Dict[str, any] = {}

    async def create_workspace(self, company_ticker: str) -> dict:
        """
        Create Daytona sandbox for a company

        Args:
            company_ticker: Company ticker symbol

        Returns:
            Sandbox info dict
        """
        sandbox_name = f"{settings.daytona_workspace_prefix}-{company_ticker.lower()}"

        if not self.client:
            return {
                "ticker": company_ticker,
                "sandbox_id": None,
                "name": sandbox_name,
                "status": "skipped",
                "note": "Daytona client not initialized"
            }

        try:
            logger.info(f"Creating Daytona sandbox: {sandbox_name}")

            # Create sandbox using CreateSandboxFromImageParams
            params = CreateSandboxFromImageParams(
                image="ubuntu:22.04",  # Base image
                # Note: Packages installed via execute commands after creation
            )

            # Create the sandbox (runs async in thread to avoid blocking)
            sandbox = await asyncio.to_thread(
                self.client.create,
                params=params,
                timeout=120  # 2 minutes for sandbox creation
            )

            self.active_sandboxes[company_ticker] = sandbox

            logger.info(f"✅ Created Daytona sandbox for {company_ticker}: {sandbox.id}")

            # Install Chrome and get CDP URL
            cdp_url = await self._setup_sandbox_dependencies(sandbox)

            return {
                "ticker": company_ticker,
                "sandbox_id": sandbox.id,
                "name": sandbox_name,
                "status": "ready",
                "sandbox": sandbox,
                "cdp_url": cdp_url  # ← Chrome CDP URL for Browser-Use
            }

        except Exception as e:
            logger.error(f"Failed to create sandbox for {company_ticker}: {e}")
            return {
                "ticker": company_ticker,
                "sandbox_id": None,
                "name": sandbox_name,
                "status": "failed",
                "error": str(e)
            }

    async def _setup_sandbox_dependencies(self, sandbox):
        """Install Chrome and start it with remote debugging in sandbox"""
        try:
            logger.info(f"Installing Chrome with remote debugging in sandbox {sandbox.id}")

            # Install Chrome/Chromium and dependencies
            install_commands = [
                "apt-get update -y",
                "apt-get install -y chromium-browser chromium-chromedriver xvfb",
                "apt-get install -y fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 libnspr4 libnss3 libwayland-client0 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils"
            ]

            for cmd in install_commands:
                result = await asyncio.to_thread(
                    sandbox.process.exec,
                    cmd,
                    timeout=180  # 3 minutes per command
                )
                logger.debug(f"Command: {cmd[:50]}... Exit code: {result.exit_code}")

            # Start Xvfb (virtual display for headless Chrome)
            await asyncio.to_thread(
                sandbox.process.exec,
                "Xvfb :99 -screen 0 1280x1024x24 &",
                env={"DISPLAY": ":99"},
                timeout=10
            )

            # Start Chrome with remote debugging on port 9222
            chrome_cmd = (
                "chromium-browser "
                "--remote-debugging-port=9222 "
                "--remote-debugging-address=0.0.0.0 "
                "--user-data-dir=/tmp/chrome-debug "
                "--no-first-run "
                "--no-default-browser-check "
                "--disable-dev-shm-usage "
                "--no-sandbox "
                "--disable-gpu "
                "--headless &"
            )

            result = await asyncio.to_thread(
                sandbox.process.exec,
                chrome_cmd,
                env={"DISPLAY": ":99"},
                timeout=30
            )

            logger.info(f"✅ Chrome started with remote debugging in sandbox {sandbox.id}")
            logger.info(f"   Chrome start result: exit_code={result.exit_code}")

            # Wait for Chrome to start
            await asyncio.sleep(3)

            # Get CDP URL for the Chrome instance
            cdp_url = await self._get_chrome_cdp_url(sandbox)
            logger.info(f"✅ Chrome CDP URL: {cdp_url}")

            return cdp_url

        except Exception as e:
            logger.warning(f"Failed to setup Chrome in sandbox {sandbox.id}: {e}")
            return None

    async def _get_chrome_cdp_url(self, sandbox) -> str:
        """Get the CDP URL for Chrome running in the sandbox"""
        try:
            # Get preview link for port 9222
            preview_link = await asyncio.to_thread(
                sandbox.get_preview_link,
                9222
            )

            # Convert HTTP URL to WebSocket URL for CDP
            # Daytona returns http://... but CDP needs ws://...
            http_url = preview_link.url

            # Replace http:// with ws:// for CDP connection
            if http_url.startswith("https://"):
                ws_url = http_url.replace("https://", "wss://")
            else:
                ws_url = http_url.replace("http://", "ws://")

            logger.info(f"Chrome CDP URL: {ws_url}")
            return ws_url

        except Exception as e:
            logger.error(f"Failed to get CDP URL for sandbox {sandbox.id}: {e}")
            return None

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

    async def execute_in_sandbox(
        self,
        sandbox_id: str,
        script: str,
        timeout: int = 60
    ) -> dict:
        """
        Execute Python script in Daytona sandbox

        Args:
            sandbox_id: Sandbox ID
            script: Python code to execute
            timeout: Execution timeout in seconds

        Returns:
            Execution result dict
        """
        try:
            logger.info(f"Executing script in sandbox {sandbox_id}")

            # Get sandbox object
            sandbox = await asyncio.to_thread(self.client.get, sandbox_id)

            # Execute command using sandbox.process
            result = await asyncio.to_thread(
                sandbox.process.execute_command,
                f"python3 -c '{script}'",
                timeout=timeout
            )

            return {
                "status": "success",
                "output": str(result),
                "error": None
            }

        except Exception as e:
            logger.error(f"Execution failed in sandbox {sandbox_id}: {e}")
            return {
                "status": "failed",
                "output": "",
                "error": str(e)
            }

    async def cleanup_sandbox(self, sandbox_id: str):
        """Delete a Daytona sandbox"""
        try:
            logger.info(f"Cleaning up sandbox {sandbox_id}")
            await asyncio.to_thread(self.client.delete, sandbox_id)
            logger.info(f"✅ Deleted sandbox {sandbox_id}")
        except Exception as e:
            logger.error(f"Failed to cleanup sandbox {sandbox_id}: {e}")

    async def cleanup_all(self):
        """Cleanup all active sandboxes"""
        logger.info(f"Cleaning up {len(self.active_sandboxes)} sandboxes")

        cleanup_tasks = []
        for ticker, sandbox in self.active_sandboxes.items():
            if sandbox and hasattr(sandbox, 'id'):
                cleanup_tasks.append(self.cleanup_sandbox(sandbox.id))

        await asyncio.gather(*cleanup_tasks, return_exceptions=True)

        self.active_sandboxes.clear()
        logger.info("All sandboxes cleaned up")

    def get_sandbox(self, ticker: str) -> Optional[dict]:
        """Get sandbox info for a ticker"""
        return self.active_sandboxes.get(ticker)
