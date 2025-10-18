"""Configuration management"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    environment: str = "development"
    log_level: str = "INFO"
    debug: bool = True
    api_port: int = 8010
    api_host: str = "0.0.0.0"

    # Azure OpenAI
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_deployment_name: str = "gpt-4"
    azure_openai_chat_deployment: str = "gpt-4o"
    azure_openai_embedding_deployment: str = "text-embedding-3-small"

    # Anthropic (for Browser-Use agent)
    anthropic_api_key: Optional[str] = None

    # Browser-Use Cloud API
    browser_use_api_key: Optional[str] = None

    # Daytona
    daytona_api_key: str
    daytona_workspace_prefix: str = "10k-pipeline"
    daytona_api_url: str = "https://app.daytona.io/api"
    daytona_max_environments: int = 3  # Start with 3 for testing

    # Browser-Use
    browser_headless: bool = True
    browser_timeout: int = 30000
    sec_request_delay: int = 1

    # Caching
    enable_caching: bool = True
    cache_dir: str = "./cache"
    cache_ttl_days: int = 30

    # CORS
    frontend_url: str = "http://localhost:5173"  # Vite default port

    # Rate Limiting
    llm_calls_per_minute: int = 50
    sec_requests_per_second: int = 10

    # SEC EDGAR
    sec_user_agent: str = "10K-Pipeline-Hackathon research@hackathon.dev"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"  # Allow extra fields from .env

    @property
    def port(self) -> int:
        """Alias for api_port"""
        return self.api_port


settings = Settings()
