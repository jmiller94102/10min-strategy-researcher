# Backend Guide: 10-K AI Intelligence Pipeline

**Module:** Backend (FastAPI)
**Tech Stack:** Python 3.11+, FastAPI, Browser-Use, Daytona.io, Azure OpenAI
**Last Updated:** 2025-10-18

---

## Quick Start

```bash
# Setup environment
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Run development server
uvicorn main:app --reload --port 8000

# In another terminal: Run tests
pytest tests/ -v
```

---

## Backend Architecture

### Directory Structure

```
backend/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── pipeline.py       # Pipeline management endpoints
│   │   │   ├── companies.py      # Company intelligence endpoints
│   │   │   ├── comparison.py     # Comparison endpoints
│   │   │   ├── export.py         # Export endpoints (CSV, PDF)
│   │   │   └── websocket.py      # WebSocket handlers
│   │   ├── dependencies.py       # FastAPI dependencies
│   │   └── middleware.py         # Custom middleware
│   ├── services/
│   │   ├── retrieval/
│   │   │   ├── company_manager.py        # Company list management
│   │   │   ├── daytona_manager.py        # Daytona environment manager
│   │   │   ├── sec_navigator.py          # SEC EDGAR navigation
│   │   │   └── parallel_controller.py    # Parallel retrieval orchestration
│   │   ├── analysis/
│   │   │   ├── section_identifier.py     # 10-K section extraction
│   │   │   ├── ai_content_detector.py    # AI content filtering
│   │   │   ├── llm_extractor.py          # LLM-powered extraction
│   │   │   ├── ai_maturity_scorer.py     # Maturity scoring
│   │   │   └── sdr_playbook_generator.py # SDR playbook generation
│   │   ├── enrichment/
│   │   │   ├── job_scraper.py            # AI job scraping
│   │   │   ├── news_aggregator.py        # News scraping
│   │   │   └── enrichment_controller.py  # Parallel enrichment
│   │   └── export/
│   │       ├── salesforce_generator.py   # Salesforce CSV
│   │       └── pdf_generator.py          # PDF playbooks
│   ├── models/
│   │   ├── company.py            # Company Pydantic models
│   │   ├── pipeline.py           # Pipeline models
│   │   ├── insights.py           # AI insights models
│   │   ├── enrichment.py         # Enrichment models
│   │   └── export_models.py      # Export models
│   ├── core/
│   │   ├── config.py             # Configuration management
│   │   ├── logging.py            # Logging setup
│   │   └── exceptions.py         # Custom exceptions
│   └── utils/
│       ├── cache.py              # Caching utilities
│       ├── validators.py         # Input validators
│       └── formatters.py         # Data formatters
├── tests/
│   ├── unit/
│   │   ├── test_sec_navigator.py
│   │   ├── test_llm_extractor.py
│   │   └── test_job_scraper.py
│   ├── integration/
│   │   ├── test_api_endpoints.py
│   │   └── test_pipeline_flow.py
│   └── fixtures/
│       ├── mock_10k.html
│       └── mock_company_data.json
├── main.py                       # FastAPI app entrypoint
├── requirements.txt              # Python dependencies
└── .env.example                  # Environment variables template
```

---

## Core Technologies

### FastAPI Patterns

**Async Everywhere:**
```python
# Good ✅
@router.get("/companies/{ticker}")
async def get_company(ticker: str) -> CompanyProfile:
    profile = await company_service.get_profile(ticker)
    return profile

# Bad ❌ (blocking I/O)
@router.get("/companies/{ticker}")
def get_company(ticker: str) -> CompanyProfile:
    profile = company_service.get_profile_sync(ticker)  # Blocks event loop!
    return profile
```

**Dependency Injection:**
```python
# dependencies.py
async def get_daytona_client():
    client = DaytonaClient(api_key=settings.DAYTONA_API_KEY)
    try:
        yield client
    finally:
        await client.close()

# routes/pipeline.py
@router.post("/pipeline/start")
async def start_pipeline(
    request: PipelineStartRequest,
    daytona: DaytonaClient = Depends(get_daytona_client)
):
    # Use daytona client
    job = await pipeline_service.start(request.company_tickers, daytona)
    return job
```

**Background Tasks:**
```python
from fastapi import BackgroundTasks

@router.post("/pipeline/start")
async def start_pipeline(
    request: PipelineStartRequest,
    background_tasks: BackgroundTasks
):
    job_id = str(uuid.uuid4())

    # Run pipeline in background
    background_tasks.add_task(
        execute_pipeline,
        job_id=job_id,
        tickers=request.company_tickers
    )

    return {"job_id": job_id, "status": "started"}
```

---

### Browser-Use Integration

**Basic Navigation:**
```python
from browser_use import Agent

async def navigate_sec_edgar(company: dict):
    agent = Agent(task="Navigate to SEC EDGAR")

    # Navigate to EDGAR
    await agent.navigate("https://www.sec.gov/cgi-bin/browse-edgar")

    # Search by CIK
    await agent.fill("input[name='CIK']", company['cik'])
    await agent.click("input[name='Find']")

    # Filter to 10-K
    await agent.select("select[name='type']", "10-K")

    # Extract results
    results = await agent.extract_all(".tableFile2")

    return results
```

**Error Handling:**
```python
from browser_use.exceptions import NavigationError, TimeoutError

async def scrape_with_retry(agent, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = await agent.navigate(url)
            return result
        except TimeoutError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
        except NavigationError as e:
            logger.error(f"Navigation failed: {e}")
            raise
```

---

### Daytona.io Patterns

**Environment Creation:**
```python
from daytona_sdk import Daytona

class DaytonaEnvironmentManager:
    def __init__(self):
        self.client = Daytona(api_key=settings.DAYTONA_API_KEY)

    async def create_environment(self, ticker: str):
        """Create isolated environment for company processing"""
        env = await self.client.create_workspace(
            name=f"10k-{ticker.lower()}",
            image="python:3.11-slim",
            packages=["browser-use", "beautifulsoup4"]
        )
        return env

    async def create_all_environments(self, companies: list):
        """Create 10 environments in parallel"""
        tasks = [
            self.create_environment(c['ticker'])
            for c in companies
        ]
        environments = await asyncio.gather(*tasks)
        return {c['ticker']: env for c, env in zip(companies, environments)}

    async def cleanup_environments(self, env_ids: list):
        """Clean up all environments"""
        cleanup_tasks = [
            self.client.delete_workspace(env_id)
            for env_id in env_ids
        ]
        await asyncio.gather(*cleanup_tasks, return_exceptions=True)
```

---

### Azure OpenAI Integration

**LLM Extraction:**
```python
from openai import AsyncAzureOpenAI
import os

class AIInsightExtractor:
    def __init__(self):
        self.client = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")

    async def extract_investments(self, text_chunks: list) -> dict:
        """Extract AI investments with structured output"""

        system_prompt = """You are an expert financial analyst. Extract AI investments from 10-K filings.
        Return valid JSON only, no additional text."""

        user_prompt = f"""
        Analyze this 10-K section for AI investments. Extract:

        1. SPECIFIC DOLLAR AMOUNTS mentioned for AI initiatives
        2. INVESTMENT AREAS (what the money is for)
        3. TIMEFRAME (when investment was made/planned)

        Return valid JSON:
        {{
            "investments": [
                {{
                    "amount": "$50M",
                    "amount_numeric": 50000000,
                    "purpose": "AI research and development",
                    "timeframe": "fiscal year 2024",
                    "quote": "direct quote from text",
                    "confidence": "high|medium|low"
                }}
            ]
        }}

        Text to analyze:
        {"\n\n".join(text_chunks)}
        """

        response = await self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,  # Low temperature for consistency
            max_tokens=4096
        )

        # Parse JSON from response
        import json
        result = json.loads(response.choices[0].message.content)

        return result
```

**Batch Processing (Cost Optimization):**
```python
# For multiple companies, batch requests when possible
async def extract_all_companies(self, companies_data: list) -> list:
    """Process multiple companies efficiently"""
    tasks = [
        self.extract_investments(company['text_chunks'])
        for company in companies_data
    ]

    # Process in parallel with rate limiting
    results = []
    batch_size = 5  # Process 5 at a time
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i+batch_size]
        batch_results = await asyncio.gather(*batch)
        results.extend(batch_results)
        await asyncio.sleep(1)  # Rate limiting pause

    return results
```

**Rate Limiting:**
```python
import asyncio
from collections import deque
from time import time

class RateLimiter:
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()

    async def acquire(self):
        """Wait if necessary to respect rate limit"""
        now = time()

        # Remove old calls outside the period
        while self.calls and self.calls[0] < now - self.period:
            self.calls.popleft()

        # Wait if at limit
        if len(self.calls) >= self.max_calls:
            sleep_time = self.calls[0] + self.period - now
            await asyncio.sleep(sleep_time)
            await self.acquire()  # Recursive retry

        self.calls.append(now)

# Usage
llm_limiter = RateLimiter(max_calls=50, period=60)  # 50 calls per minute

async def call_llm(prompt):
    await llm_limiter.acquire()
    response = await client.messages.create(...)
    return response
```

---

## Validation Standards

### Type Checking (Level 1) ❌ BLOCKING

```bash
# Must pass before proceeding
mypy src/ --strict

# Configuration: mypy.ini
[mypy]
python_version = 3.11
strict = True
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

**Example:**
```python
# Good ✅
async def get_company(ticker: str) -> CompanyProfile:
    profile: CompanyProfile = await db.fetch_one(ticker)
    return profile

# Bad ❌ (missing type hints)
async def get_company(ticker):
    profile = await db.fetch_one(ticker)
    return profile
```

---

### Linting (Level 2) ❌ BLOCKING

```bash
# Ruff (fast Python linter)
ruff check src/

# Black (code formatter)
black src/ --check

# Fix issues automatically
ruff check src/ --fix
black src/
```

**Ruff Configuration (pyproject.toml):**
```toml
[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]  # Line too long (handled by black)

[tool.black]
line-length = 100
target-version = ['py311']
```

---

### Testing (Level 3) ❌ BLOCKING

**Unit Tests:**
```python
# tests/unit/test_sec_navigator.py
import pytest
from src.services.retrieval.sec_navigator import SECNavigator

@pytest.mark.asyncio
async def test_navigate_to_edgar():
    """Test navigation to SEC EDGAR"""
    navigator = SECNavigator()
    agent = MockAgent()

    await navigator.navigate_to_edgar(agent)

    assert agent.navigated_to == "https://www.sec.gov/cgi-bin/browse-edgar"

@pytest.mark.asyncio
async def test_search_by_cik():
    """Test CIK search"""
    navigator = SECNavigator()
    agent = MockAgent()

    await navigator.search_by_cik(agent, "0000789019")

    assert agent.filled_fields["input[name='CIK']"] == "0000789019"
    assert agent.clicked == "input[name='Find']"
```

**Integration Tests:**
```python
# tests/integration/test_api_endpoints.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_start_pipeline():
    """Test pipeline start endpoint"""
    response = client.post("/api/v1/pipeline/start", json={
        "company_tickers": ["MSFT", "AAPL"]
    })

    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "started"

def test_get_company_not_found():
    """Test 404 for unknown company"""
    response = client.get("/api/v1/companies/INVALID")
    assert response.status_code == 404
```

**Coverage Requirements:**
```bash
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Required coverage:
# - Overall: ≥70%
# - Critical paths (API routes, core services): ≥90%
```

---

## Pydantic Models

### Company Models

```python
# src/models/company.py
from pydantic import BaseModel, Field, validator

class Company(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    ticker: str = Field(..., min_length=1, max_length=10)
    cik: str = Field(..., regex=r"^\d{10}$")  # 10-digit CIK
    domain: str | None = None

    @validator('ticker')
    def uppercase_ticker(cls, v):
        return v.upper()

class CompanyProfile(BaseModel):
    company: Company
    filing_date: str  # ISO 8601
    fiscal_year: int
    ai_insights: AIInsights
    enrichment: EnrichmentData
    ai_maturity: AIMaturityScore
    sdr_playbook: SDRPlaybook
    metadata: ProfileMetadata

    class Config:
        json_schema_extra = {
            "example": {
                "company": {
                    "name": "Microsoft",
                    "ticker": "MSFT",
                    "cik": "0000789019"
                },
                # ... example data
            }
        }
```

### Pipeline Models

```python
# src/models/pipeline.py
from enum import Enum
from pydantic import BaseModel, UUID4

class PipelineStatus(str, Enum):
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"

class PipelineStartRequest(BaseModel):
    company_tickers: list[str] = Field(..., min_items=1, max_items=10)
    skip_enrichment: bool = False

class PipelineStartResponse(BaseModel):
    job_id: UUID4
    status: PipelineStatus
    total_companies: int
    estimated_time_seconds: int

class CompanyProgress(BaseModel):
    ticker: str
    status: PipelineStatus
    stage: str | None
    error: str | None = None

class PipelineStatusResponse(BaseModel):
    job_id: UUID4
    status: PipelineStatus
    progress: dict
    companies: list[CompanyProgress]
    started_at: str
    estimated_completion: str | None
```

---

## Error Handling

### Custom Exceptions

```python
# src/core/exceptions.py
class PipelineException(Exception):
    """Base exception for pipeline errors"""
    pass

class InvalidTickerError(PipelineException):
    """Unknown company ticker"""
    def __init__(self, ticker: str):
        self.ticker = ticker
        super().__init__(f"Ticker '{ticker}' not found")

class DaytonaUnavailableError(PipelineException):
    """Daytona service unavailable"""
    pass

class LLMAPIError(PipelineException):
    """Anthropic API error"""
    pass

class RateLimitExceededError(PipelineException):
    """Rate limit exceeded"""
    pass
```

### Exception Handlers

```python
# src/api/middleware.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.core.exceptions import InvalidTickerError, DaytonaUnavailableError

@app.exception_handler(InvalidTickerError)
async def invalid_ticker_handler(request: Request, exc: InvalidTickerError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": {
                "code": "INVALID_TICKER",
                "message": str(exc),
                "details": {
                    "ticker": exc.ticker,
                    "valid_tickers": SUPPORTED_TICKERS
                }
            }
        }
    )

@app.exception_handler(DaytonaUnavailableError)
async def daytona_unavailable_handler(request: Request, exc: DaytonaUnavailableError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": {
                "code": "DAYTONA_UNAVAILABLE",
                "message": "Daytona service is currently unavailable",
                "details": {}
            }
        }
    )
```

---

## Caching Strategy

### File-based Cache

```python
# src/utils/cache.py
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

class FileCache:
    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Generate cache file path from key"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"

    def get(self, key: str, max_age: timedelta | None = None):
        """Get cached value if exists and not expired"""
        cache_file = self._get_cache_path(key)

        if not cache_file.exists():
            return None

        with open(cache_file) as f:
            cached = json.load(f)

        # Check expiration
        if max_age:
            cached_at = datetime.fromisoformat(cached["cached_at"])
            if datetime.now() - cached_at > max_age:
                return None

        return cached["value"]

    def set(self, key: str, value):
        """Cache value"""
        cache_file = self._get_cache_path(key)

        with open(cache_file, 'w') as f:
            json.dump({
                "value": value,
                "cached_at": datetime.now().isoformat()
            }, f)

# Usage
cache = FileCache()

async def retrieve_10k(company: dict):
    cache_key = f"10k:{company['ticker']}"

    # Check cache (30-day expiration for 10-Ks)
    cached = cache.get(cache_key, max_age=timedelta(days=30))
    if cached:
        logger.info(f"Cache hit for {company['ticker']}")
        return cached

    # Not cached, retrieve from SEC
    result = await sec_navigator.retrieve_10k(company)

    # Cache result
    cache.set(cache_key, result)

    return result
```

---

## Logging

### Structured Logging

```python
# src/core/logging.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, 'extra'):
            log_data.update(record.extra)

        return json.dumps(log_data)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

# Usage
logger = logging.getLogger(__name__)

logger.info("Processing company", extra={
    "ticker": "MSFT",
    "stage": "retrieval",
    "job_id": job_id
})
```

---

## WebSocket Implementation

```python
# src/api/routes/websocket.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, job_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[job_id] = websocket

    def disconnect(self, job_id: str):
        if job_id in self.active_connections:
            del self.active_connections[job_id]

    async def send_message(self, job_id: str, message: dict):
        if job_id in self.active_connections:
            await self.active_connections[job_id].send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/pipeline/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await manager.connect(job_id, websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(job_id)

# Send updates from pipeline
async def process_company(job_id: str, ticker: str):
    await manager.send_message(job_id, {
        "type": "progress",
        "data": {
            "ticker": ticker,
            "stage": "retrieval",
            "status": "in_progress"
        }
    })

    # ... processing ...

    await manager.send_message(job_id, {
        "type": "complete",
        "data": {
            "ticker": ticker,
            "profile": company_profile
        }
    })
```

---

## Environment Configuration

### .env.example

```bash
# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG=true

# API Keys
ANTHROPIC_API_KEY=sk-ant-api03-...
DAYTONA_API_KEY=dyt-...

# Daytona Configuration
DAYTONA_WORKSPACE_PREFIX=10k-pipeline
DAYTONA_MAX_ENVIRONMENTS=10

# Caching
ENABLE_CACHING=true
CACHE_DIR=./cache
CACHE_TTL_DAYS=30

# CORS
FRONTEND_URL=http://localhost:3000

# Rate Limiting
LLM_CALLS_PER_MINUTE=50
SEC_REQUESTS_PER_SECOND=10

# Database (if using)
# DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Configuration Management

```python
# src/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application
    environment: str = "development"
    log_level: str = "INFO"
    debug: bool = False

    # API Keys
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str = "2024-02-15-preview"
    azure_openai_deployment_name: str = "gpt-4"
    daytona_api_key: str

    # Daytona
    daytona_workspace_prefix: str = "10k-pipeline"
    daytona_max_environments: int = 10

    # Caching
    enable_caching: bool = True
    cache_dir: str = "./cache"
    cache_ttl_days: int = 30

    # CORS
    frontend_url: str = "http://localhost:3000"

    # Rate Limiting
    llm_calls_per_minute: int = 50
    sec_requests_per_second: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

---

## PRD Execution Order

### 1. PRD 1: 10-K Retrieval (Hours 0-3)

**Files:**
- `src/services/retrieval/company_manager.py`
- `src/services/retrieval/daytona_manager.py`
- `src/services/retrieval/sec_navigator.py`
- `src/services/retrieval/parallel_controller.py`

**Validation:**
```bash
# Test retrieval for 1 company
pytest tests/unit/test_sec_navigator.py -v

# Test parallel retrieval
pytest tests/integration/test_retrieval_pipeline.py -v

# Verify output
ls cache/*.json  # Should see MSFT_10k.json, etc.
```

---

### 2. PRD 2: AI Analysis (Hours 3-6)

**Files:**
- `src/services/analysis/section_identifier.py`
- `src/services/analysis/ai_content_detector.py`
- `src/services/analysis/llm_extractor.py`
- `src/services/analysis/ai_maturity_scorer.py`
- `src/services/analysis/sdr_playbook_generator.py`

**Validation:**
```bash
# Test LLM extraction
pytest tests/unit/test_llm_extractor.py -v

# Test full analysis
pytest tests/integration/test_analysis_pipeline.py -v

# Check output quality
python scripts/validate_insights.py  # Manual validation script
```

---

### 3. PRD 3: Live Enrichment (Hours 6-9)

**Files:**
- `src/services/enrichment/job_scraper.py`
- `src/services/enrichment/news_aggregator.py`
- `src/services/enrichment/enrichment_controller.py`
- `src/services/export/salesforce_generator.py`
- `src/services/export/pdf_generator.py`

**Validation:**
```bash
# Test job scraping
pytest tests/unit/test_job_scraper.py -v

# Test full pipeline
pytest tests/integration/test_full_pipeline.py -v

# Verify exports
ls output/crm/*.csv
ls output/playbooks/*.pdf
```

---

## Common Patterns

### Retry Logic

```python
import asyncio
from functools import wraps

def async_retry(max_attempts=3, delay=1, backoff=2):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    wait_time = delay * (backoff ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
        return wrapper
    return decorator

# Usage
@async_retry(max_attempts=3, delay=2)
async def scrape_career_page(company):
    # May fail due to network issues
    return await browser_use.navigate(url)
```

---

## Testing Utilities

### Mock Factories

```python
# tests/fixtures/factories.py
from src.models.company import Company, CompanyProfile

def create_mock_company(ticker="MSFT") -> Company:
    return Company(
        name="Microsoft" if ticker == "MSFT" else f"Company {ticker}",
        ticker=ticker,
        cik="0000789019" if ticker == "MSFT" else f"000078{ticker[:4]}"
    )

def create_mock_profile(ticker="MSFT") -> CompanyProfile:
    return CompanyProfile(
        company=create_mock_company(ticker),
        filing_date="2024-07-30",
        fiscal_year=2024,
        # ... rest of mock data
    )
```

---

## Deployment Checklist

- [ ] Environment variables configured
- [ ] API keys validated
- [ ] Daytona quota sufficient (10+ environments)
- [ ] All tests passing (`pytest tests/ -v`)
- [ ] Type checking passes (`mypy src/`)
- [ ] Linting passes (`ruff check src/`)
- [ ] CORS configured for frontend URL
- [ ] Logging configured appropriately
- [ ] Rate limiting tested
- [ ] Cache directory created and writable
- [ ] WebSocket connection tested

---

## Troubleshooting

### "Daytona API key invalid"
```bash
# Verify key format
echo $DAYTONA_API_KEY

# Test connection
python -c "from daytona_sdk import Daytona; print(Daytona(api_key='$DAYTONA_API_KEY').info())"
```

### "Azure OpenAI rate limit exceeded"
- Implement rate limiter (see RateLimiter class above)
- Batch requests (process 5 at a time)
- Add delays between batches (1-2 seconds)
- Check Azure portal for quota limits

### "SEC EDGAR blocking requests"
- Add delays between requests (1 second minimum)
- Use different IPs via Daytona environments
- Check SEC User-Agent requirements

---

**Last Updated:** 2025-10-18
**Next Steps:** Execute `/execute-prp.md PRPs/backend/10k_retrieval.md`
