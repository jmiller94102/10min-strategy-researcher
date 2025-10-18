# API Contract Documentation

**Version:** 1.0.0
**Last Updated:** 2025-10-18
**Purpose:** Define backend/frontend interface for parallel development

---

## Overview

This document defines the REST API contract between the FastAPI backend and React frontend. Both teams can develop independently using this specification.

**Base URL:** `http://localhost:8000/api/v1`

---

## Core Data Models

### Company

```typescript
interface Company {
  name: string;
  ticker: string;
  cik: string;
  domain?: string;
}
```

### CompanyProfile

```typescript
interface CompanyProfile {
  company: Company;
  filing_date: string; // ISO 8601
  fiscal_year: number;
  ai_insights: AIInsights;
  enrichment: EnrichmentData;
  ai_maturity: AIMaturityScore;
  sdr_playbook: SDRPlaybook;
  metadata: ProfileMetadata;
}
```

### AIInsights

```typescript
interface AIInsights {
  investments: AIInvestment[];
  products: AIProduct[];
  risks: AIRisk[];
  timeline: AITimeline;
  competitive_positioning: CompetitivePositioning;
}

interface AIInvestment {
  amount: string; // e.g., "$50M"
  amount_numeric: number;
  purpose: string;
  timeframe: string;
  quote: string;
  confidence: "high" | "medium" | "low";
  source_section: "business" | "risk_factors" | "mda";
}

interface AIProduct {
  product_name: string;
  description: string;
  launch_status: "available" | "beta" | "planned";
  target_market: "enterprise" | "consumer" | "developer";
  quote: string;
  revenue_impact?: "mentioned" | "not_mentioned";
}

interface AIRisk {
  category: "competitive" | "implementation" | "regulatory" | "ethical";
  risk: string;
  severity: "high" | "medium" | "low";
  quote: string;
}

interface AITimeline {
  current_initiatives: string[];
  near_term_plans: string[];
  long_term_vision: string;
  milestones: Milestone[];
}

interface Milestone {
  date: string;
  event: string;
}

interface CompetitivePositioning {
  strengths: string[];
  competitors_mentioned: string[];
  differentiation: string;
  concerns_about_competition: string[];
}
```

### EnrichmentData

```typescript
interface EnrichmentData {
  hiring: HiringData;
  recent_news: NewsItem[];
  enriched_at: string; // ISO 8601
}

interface HiringData {
  total_jobs: number;
  ai_jobs: number;
  ai_job_details: JobPosting[];
  hiring_urgency: "HIGH" | "NORMAL" | "LOW";
  tech_stack: string[];
  scraped_at: string; // ISO 8601
}

interface JobPosting {
  title: string;
  location: string;
  job_url: string;
  tech_stack: string[];
  posted_date: string;
  seniority: "junior" | "mid" | "senior" | "staff" | "principal";
  remote: boolean;
}

interface NewsItem {
  headline: string;
  source: string;
  date: string;
  url: string;
  summary?: string;
  category: "product_launch" | "investment" | "partnership" | "research" | "executive" | "general";
}
```

### AIMaturityScore

```typescript
interface AIMaturityScore {
  total_score: number; // 0-100
  breakdown: {
    investment: number; // 0-25
    product: number; // 0-25
    strategic_importance: number; // 0-25
    organizational_readiness: number; // 0-25
  };
  percentile: number; // vs other companies
  label: "Leader" | "Fast Follower" | "Emerging" | "Laggard";
}
```

### SDRPlaybook

```typescript
interface SDRPlaybook {
  discovery_questions: string[];
  value_propositions: string[];
  objection_handlers: Record<string, string>;
  executive_summary: string;
  talking_points: string[];
}
```

### ProfileMetadata

```typescript
interface ProfileMetadata {
  analyzed_at: string; // ISO 8601
  analysis_time_seconds: number;
  retrieval_time_seconds: number;
  enrichment_time_seconds: number;
  enrichment_completeness: number; // 0-1
  status: "complete" | "partial" | "failed";
}
```

---

## API Endpoints

### 1. Pipeline Management

#### **POST /pipeline/start**

Start full intelligence pipeline for multiple companies.

**Request:**
```json
{
  "company_tickers": ["MSFT", "AAPL", "NVDA"],
  "skip_enrichment": false // optional, default false
}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "started",
  "total_companies": 3,
  "estimated_time_seconds": 420
}
```

**Status Codes:**
- `202` - Accepted (job started)
- `400` - Invalid request
- `429` - Too many concurrent jobs

---

#### **GET /pipeline/status/{job_id}**

Get pipeline execution status.

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "in_progress" | "completed" | "failed" | "partial",
  "progress": {
    "current_stage": "enrichment",
    "companies_processed": 2,
    "companies_total": 3,
    "percentage": 66
  },
  "companies": [
    {
      "ticker": "MSFT",
      "status": "completed",
      "stage": "enrichment"
    },
    {
      "ticker": "AAPL",
      "status": "in_progress",
      "stage": "analysis"
    },
    {
      "ticker": "NVDA",
      "status": "pending",
      "stage": null
    }
  ],
  "started_at": "2025-10-18T10:00:00Z",
  "estimated_completion": "2025-10-18T10:07:00Z"
}
```

---

#### **GET /pipeline/results/{job_id}**

Get completed pipeline results.

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "completed",
  "results": CompanyProfile[], // Array of full profiles
  "summary": {
    "total_companies": 3,
    "successful": 3,
    "failed": 0,
    "total_time_seconds": 385
  }
}
```

---

### 2. Company Intelligence

#### **GET /companies**

List available companies.

**Response:**
```json
{
  "companies": Company[]
}
```

---

#### **GET /companies/{ticker}**

Get full intelligence profile for a company.

**Response:**
```json
CompanyProfile
```

**Status Codes:**
- `200` - Success
- `404` - Company not found
- `425` - Data not ready (still processing)

---

#### **GET /companies/{ticker}/insights**

Get only AI insights (without enrichment).

**Response:**
```json
{
  "company": Company,
  "ai_insights": AIInsights,
  "ai_maturity": AIMaturityScore,
  "metadata": {
    "analyzed_at": "2025-10-18T10:05:00Z"
  }
}
```

---

#### **GET /companies/{ticker}/enrichment**

Get only live enrichment data.

**Response:**
```json
{
  "company": Company,
  "enrichment": EnrichmentData
}
```

---

### 3. Comparison & Analytics

#### **GET /comparison**

Compare multiple companies.

**Query Params:**
- `tickers` (required): Comma-separated list, e.g., `?tickers=MSFT,AAPL,GOOGL`

**Response:**
```json
{
  "companies": [
    {
      "ticker": "MSFT",
      "name": "Microsoft",
      "ai_maturity_score": 85,
      "total_investment": 50000000,
      "ai_jobs": 23,
      "ai_products_count": 5
    }
  ],
  "rankings": {
    "by_maturity": ["MSFT", "NVDA", "AAPL"],
    "by_investment": ["MSFT", "GOOGL", "AAPL"],
    "by_hiring": ["NVDA", "MSFT", "GOOGL"]
  }
}
```

---

### 4. Export

#### **POST /export/salesforce**

Generate Salesforce CSV.

**Request:**
```json
{
  "job_id": "uuid-string"
}
```

**Response:**
```json
{
  "download_url": "/downloads/salesforce_import_uuid.csv",
  "filename": "salesforce_import_2025-10-18.csv",
  "expires_at": "2025-10-18T12:00:00Z"
}
```

---

#### **POST /export/playbooks**

Generate PDF playbooks.

**Request:**
```json
{
  "job_id": "uuid-string",
  "tickers": ["MSFT", "AAPL"] // optional, defaults to all
}
```

**Response:**
```json
{
  "download_url": "/downloads/playbooks_uuid.zip",
  "filename": "ai_playbooks_2025-10-18.zip",
  "files_included": ["MSFT_playbook.pdf", "AAPL_playbook.pdf", "ALL_COMPANIES.pdf"],
  "expires_at": "2025-10-18T12:00:00Z"
}
```

---

### 5. Health & Utilities

#### **GET /health**

Service health check.

**Response:**
```json
{
  "status": "healthy",
  "daytona": "connected",
  "anthropic_api": "connected",
  "version": "1.0.0"
}
```

---

## WebSocket: Real-time Updates

**Endpoint:** `ws://localhost:8000/ws/pipeline/{job_id}`

Subscribe to real-time pipeline progress updates.

**Messages:**
```json
{
  "type": "progress",
  "data": {
    "ticker": "MSFT",
    "stage": "enrichment",
    "status": "in_progress",
    "message": "Scraping career page..."
  }
}

{
  "type": "complete",
  "data": {
    "ticker": "MSFT",
    "profile": CompanyProfile
  }
}

{
  "type": "error",
  "data": {
    "ticker": "AAPL",
    "stage": "retrieval",
    "error": "SEC rate limit exceeded"
  }
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "INVALID_TICKER",
    "message": "Ticker 'INVALID' not found in supported companies",
    "details": {
      "valid_tickers": ["MSFT", "AAPL", ...]
    }
  }
}
```

### Common Error Codes

- `INVALID_TICKER` - Unknown company ticker
- `JOB_NOT_FOUND` - Pipeline job doesn't exist
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `DAYTONA_UNAVAILABLE` - Daytona service down
- `LLM_API_ERROR` - Anthropic API error
- `PARSING_ERROR` - 10-K parsing failed

---

## Mock Data Strategy

For parallel development, backend provides mock endpoints:

**GET /mock/companies/{ticker}**

Returns realistic mock data instantly (no processing).

Frontend can develop against `/mock/*` endpoints while backend implements real pipeline.

---

## Authentication (Future)

Currently no auth required (hackathon MVP).

Post-hackathon: Add JWT Bearer tokens.

---

## Rate Limiting

- Pipeline: Max 1 concurrent job per client
- API calls: 100 requests/minute per IP

---

## Versioning

API is versioned via URL path: `/api/v1/`

Breaking changes will increment version: `/api/v2/`

---

## Frontend Integration Example

```typescript
// Start pipeline
const response = await fetch('/api/v1/pipeline/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    company_tickers: ['MSFT', 'AAPL', 'NVDA']
  })
});

const { job_id } = await response.json();

// Connect WebSocket for real-time updates
const ws = new WebSocket(`ws://localhost:8000/ws/pipeline/${job_id}`);

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'progress') {
    updateProgressUI(message.data);
  }
};

// Poll status (alternative to WebSocket)
const checkStatus = setInterval(async () => {
  const status = await fetch(`/api/v1/pipeline/status/${job_id}`);
  const data = await status.json();

  if (data.status === 'completed') {
    clearInterval(checkStatus);
    fetchResults(job_id);
  }
}, 2000);
```

---

## Backend Implementation Notes

**FastAPI Structure:**
```python
# backend/src/api/routes/
- pipeline.py  # Pipeline management endpoints
- companies.py # Company intelligence endpoints
- comparison.py # Comparison endpoints
- export.py    # Export endpoints
- websocket.py # WebSocket handlers
```

**Background Jobs:**
- Use `asyncio` + `BackgroundTasks` for pipeline execution
- Store job status in Redis or in-memory dict (hackathon MVP)
- Cleanup completed jobs after 1 hour

**CORS Configuration:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing Strategy

### Backend Tests
```python
# test_api.py
async def test_start_pipeline():
    response = client.post("/api/v1/pipeline/start", json={
        "company_tickers": ["MSFT"]
    })
    assert response.status_code == 202
    assert "job_id" in response.json()
```

### Frontend Tests
```typescript
// Mock API responses for component tests
import { rest } from 'msw';

const handlers = [
  rest.get('/api/v1/companies/:ticker', (req, res, ctx) => {
    return res(ctx.json(mockCompanyProfile));
  }),
];
```

---

## Questions for Clarification

1. **Caching:** Should we cache 10-K data to avoid re-scraping?
2. **Persistence:** Store results in database or file system?
3. **Auth:** Needed for hackathon demo?
4. **Deployment:** Single server or separate backend/frontend hosts?

---

**Next Steps:**
1. Backend: Implement pipeline orchestration and job management
2. Frontend: Build UI components using mock data
3. Integration: Connect real API once backend is ready
