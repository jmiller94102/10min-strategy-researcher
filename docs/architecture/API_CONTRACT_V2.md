# API Contract Documentation v2.0

**Version:** 2.0.0
**Last Updated:** 2025-10-18
**Status:** Production-Ready Specification
**Purpose:** Complete backend/frontend interface for 10-K AI Intelligence Pipeline

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Base Configuration](#base-configuration)
3. [TypeScript/Python Type Definitions](#type-definitions)
4. [REST API Endpoints](#rest-api-endpoints)
5. [WebSocket API](#websocket-api)
6. [Error Handling](#error-handling)
7. [Frontend Integration Examples](#frontend-integration-examples)
8. [Backend Implementation Guide](#backend-implementation-guide)
9. [Testing & Validation](#testing--validation)

---

## Overview

This API enables a React frontend to orchestrate AI intelligence extraction from SEC 10-K filings through a FastAPI backend.

**Architecture Flow:**
```
Frontend → POST /pipeline/start → Backend creates job
       ↓
   WebSocket connection established
       ↓
Backend → Processes companies in parallel
       ↓
Frontend ← Receives real-time progress updates
       ↓
Frontend → GET /companies/{ticker} → Fetch results
```

---

## Base Configuration

### Environment Variables

**Backend (.env):**
```bash
# API Configuration
API_VERSION=v1
API_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# External Services
ANTHROPIC_API_KEY=sk-ant-...
DAYTONA_API_KEY=dyt-...

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
MAX_CONCURRENT_JOBS=3
JOB_RETENTION_HOURS=24
```

**Frontend (.env):**
```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENABLE_MOCK_DATA=false  # Set to true for development without backend
```

### URLs

| Environment | Backend Base URL | WebSocket URL |
|-------------|------------------|---------------|
| Development | `http://localhost:8000/api/v1` | `ws://localhost:8000/ws` |
| Production | `https://api.yourdomain.com/api/v1` | `wss://api.yourdomain.com/ws` |

---

## Type Definitions

### Core Models (TypeScript)

```typescript
// ============================================================================
// COMPANY MODELS
// ============================================================================

export interface Company {
  name: string;           // e.g., "Microsoft Corporation"
  ticker: string;         // e.g., "MSFT"
  cik: string;           // SEC Central Index Key, e.g., "0000789019"
  domain?: string;       // e.g., "microsoft.com"
}

export interface CompanyProfile {
  company: Company;
  filing_date: string;                  // ISO 8601, e.g., "2024-07-30"
  fiscal_year: number;                  // e.g., 2024
  ai_insights: AIInsights;
  enrichment: EnrichmentData;
  ai_maturity: AIMaturityScore;
  sdr_playbook: SDRPlaybook;
  metadata: ProfileMetadata;
}

// ============================================================================
// AI INSIGHTS MODELS
// ============================================================================

export interface AIInsights {
  investments: AIInvestment[];
  products: AIProduct[];
  risks: AIRisk[];
  timeline: AITimeline;
  competitive_positioning: CompetitivePositioning;
}

export interface AIInvestment {
  amount: string;                       // Human-readable, e.g., "$50M"
  amount_numeric: number;               // Actual number, e.g., 50000000
  purpose: string;                      // e.g., "AI infrastructure and R&D"
  timeframe: string;                    // e.g., "FY2024"
  quote: string;                        // Direct quote from 10-K
  confidence: "high" | "medium" | "low";
  source_section: "business" | "risk_factors" | "mda";  // Management's Discussion & Analysis
}

export interface AIProduct {
  product_name: string;                 // e.g., "GitHub Copilot"
  description: string;                  // Brief description
  launch_status: "available" | "beta" | "planned";
  target_market: "enterprise" | "consumer" | "developer";
  quote: string;                        // Direct quote from 10-K
  revenue_impact?: "mentioned" | "not_mentioned";
}

export interface AIRisk {
  category: "competitive" | "implementation" | "regulatory" | "ethical";
  risk: string;                         // Risk description
  severity: "high" | "medium" | "low";
  quote: string;                        // Direct quote from 10-K
}

export interface AITimeline {
  current_initiatives: string[];        // Ongoing AI projects
  near_term_plans: string[];            // 1-2 year plans
  long_term_vision: string;             // 3-5 year vision statement
  milestones: Milestone[];
}

export interface Milestone {
  date: string;                         // ISO 8601 or description
  event: string;                        // Milestone description
}

export interface CompetitivePositioning {
  strengths: string[];                  // Competitive advantages
  competitors_mentioned: string[];      // List of competitor names
  differentiation: string;              // How they differentiate
  concerns_about_competition: string[]; // Competitive concerns
}

// ============================================================================
// ENRICHMENT MODELS (Live Data)
// ============================================================================

export interface EnrichmentData {
  hiring: HiringData;
  recent_news: NewsItem[];
  enriched_at: string;                  // ISO 8601, when data was scraped
}

export interface HiringData {
  total_jobs: number;                   // Total open positions
  ai_jobs: number;                      // AI-related positions
  ai_job_details: JobPosting[];         // Top 10-20 AI jobs
  hiring_urgency: "HIGH" | "NORMAL" | "LOW";
  tech_stack: string[];                 // Unique technologies across all jobs
  scraped_at: string;                   // ISO 8601
}

export interface JobPosting {
  title: string;                        // e.g., "Senior ML Engineer"
  location: string;                     // e.g., "Seattle, WA (Remote)"
  job_url: string;                      // Link to job posting
  tech_stack: string[];                 // e.g., ["Python", "TensorFlow", "PyTorch"]
  posted_date: string;                  // e.g., "2025-10-10"
  seniority: "junior" | "mid" | "senior" | "staff" | "principal";
  remote: boolean;
}

export interface NewsItem {
  headline: string;                     // News headline
  source: string;                       // e.g., "TechCrunch"
  date: string;                         // ISO 8601
  url: string;                          // Link to article
  summary?: string;                     // Optional summary
  category: "product_launch" | "investment" | "partnership" | "research" | "executive" | "general";
}

// ============================================================================
// AI MATURITY SCORING
// ============================================================================

export interface AIMaturityScore {
  total_score: number;                  // 0-100
  breakdown: {
    investment: number;                 // 0-25 (based on investment amount)
    product: number;                    // 0-25 (based on product count/maturity)
    strategic_importance: number;       // 0-25 (based on mentions/emphasis)
    organizational_readiness: number;   // 0-25 (based on hiring/structure)
  };
  percentile: number;                   // 0-100, vs other analyzed companies
  label: "Leader" | "Fast Follower" | "Emerging" | "Laggard";
}

// ============================================================================
// SDR PLAYBOOK (Sales Intelligence)
// ============================================================================

export interface SDRPlaybook {
  discovery_questions: string[];        // 5-10 tailored questions
  value_propositions: string[];         // 3-5 value props based on insights
  objection_handlers: Record<string, string>;  // Common objections → responses
  executive_summary: string;            // 2-3 paragraph summary
  talking_points: string[];             // Key conversation starters
}

// ============================================================================
// METADATA
// ============================================================================

export interface ProfileMetadata {
  analyzed_at: string;                  // ISO 8601, when analysis completed
  analysis_time_seconds: number;        // Time taken for AI analysis
  retrieval_time_seconds: number;       // Time taken to retrieve 10-K
  enrichment_time_seconds: number;      // Time taken for enrichment
  enrichment_completeness: number;      // 0-1, % of enrichment successful
  status: "complete" | "partial" | "failed";
}

// ============================================================================
// PIPELINE MODELS
// ============================================================================

export interface PipelineStartRequest {
  company_tickers: string[];            // e.g., ["MSFT", "AAPL", "NVDA"]
  skip_enrichment?: boolean;            // Default: false
}

export interface PipelineStartResponse {
  job_id: string;                       // UUID
  status: "started";
  total_companies: number;
  estimated_time_seconds: number;
  started_at: string;                   // ISO 8601
}

export interface PipelineStatusResponse {
  job_id: string;
  status: "started" | "in_progress" | "completed" | "failed" | "partial";
  progress: PipelineProgress;
  companies: CompanyStatus[];
  started_at: string;                   // ISO 8601
  estimated_completion?: string;        // ISO 8601
  completed_at?: string;                // ISO 8601 (if completed)
}

export interface PipelineProgress {
  current_stage: "retrieval" | "analysis" | "enrichment" | "finalization";
  companies_processed: number;
  companies_total: number;
  percentage: number;                   // 0-100
}

export interface CompanyStatus {
  ticker: string;
  status: "pending" | "retrieving" | "analyzing" | "enriching" | "completed" | "failed";
  stage: "retrieval" | "analysis" | "enrichment" | "finalization" | null;
  message?: string;                     // e.g., "Scraping 10-K from EDGAR..."
  error?: string;                       // Error message if failed
  started_at?: string;                  // ISO 8601
  completed_at?: string;                // ISO 8601
}

export interface PipelineResultsResponse {
  job_id: string;
  status: "completed" | "partial";
  results: CompanyProfile[];
  summary: {
    total_companies: number;
    successful: number;
    failed: number;
    total_time_seconds: number;
  };
}

// ============================================================================
// COMPARISON MODELS
// ============================================================================

export interface ComparisonResponse {
  companies: CompanyComparison[];
  rankings: {
    by_maturity: string[];              // Ticker list sorted by maturity
    by_investment: string[];            // Ticker list sorted by investment
    by_hiring: string[];                // Ticker list sorted by AI hiring
  };
}

export interface CompanyComparison {
  ticker: string;
  name: string;
  ai_maturity_score: number;
  total_investment: number;
  ai_jobs: number;
  ai_products_count: number;
  recent_news_count: number;
  label: "Leader" | "Fast Follower" | "Emerging" | "Laggard";
}

// ============================================================================
// EXPORT MODELS
// ============================================================================

export interface ExportSalesforceRequest {
  job_id: string;
}

export interface ExportSalesforceResponse {
  download_url: string;                 // e.g., "/downloads/salesforce_uuid.csv"
  filename: string;                     // e.g., "salesforce_import_2025-10-18.csv"
  expires_at: string;                   // ISO 8601
}

export interface ExportPlaybooksRequest {
  job_id: string;
  tickers?: string[];                   // Optional, defaults to all
}

export interface ExportPlaybooksResponse {
  download_url: string;                 // e.g., "/downloads/playbooks_uuid.zip"
  filename: string;                     // e.g., "ai_playbooks_2025-10-18.zip"
  files_included: string[];             // e.g., ["MSFT_playbook.pdf", "AAPL_playbook.pdf"]
  expires_at: string;                   // ISO 8601
}

// ============================================================================
// HEALTH & UTILITY MODELS
// ============================================================================

export interface HealthResponse {
  status: "healthy" | "degraded" | "unhealthy";
  daytona: "connected" | "disconnected";
  anthropic_api: "connected" | "disconnected";
  version: string;
  uptime_seconds: number;
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
}

// ============================================================================
// WEBSOCKET MESSAGE TYPES
// ============================================================================

export type WebSocketMessage =
  | ProgressMessage
  | CompleteMessage
  | ErrorMessage
  | StageChangeMessage;

export interface ProgressMessage {
  type: "progress";
  data: {
    ticker: string;
    stage: "retrieval" | "analysis" | "enrichment";
    status: "in_progress";
    message: string;                    // e.g., "Scraping career page..."
    percentage: number;                 // Company-specific progress 0-100
  };
}

export interface CompleteMessage {
  type: "complete";
  data: {
    ticker: string;
    profile: CompanyProfile;
  };
}

export interface ErrorMessage {
  type: "error";
  data: {
    ticker: string;
    stage: "retrieval" | "analysis" | "enrichment";
    error: string;
  };
}

export interface StageChangeMessage {
  type: "stage_change";
  data: {
    ticker: string;
    from_stage: string;
    to_stage: string;
  };
}
```

### Python Models (Backend - Pydantic)

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict
from datetime import datetime

# ============================================================================
# COMPANY MODELS
# ============================================================================

class Company(BaseModel):
    name: str
    ticker: str
    cik: str
    domain: Optional[str] = None

class AIInvestment(BaseModel):
    amount: str
    amount_numeric: float
    purpose: str
    timeframe: str
    quote: str
    confidence: Literal["high", "medium", "low"]
    source_section: Literal["business", "risk_factors", "mda"]

class AIProduct(BaseModel):
    product_name: str
    description: str
    launch_status: Literal["available", "beta", "planned"]
    target_market: Literal["enterprise", "consumer", "developer"]
    quote: str
    revenue_impact: Optional[Literal["mentioned", "not_mentioned"]] = None

class AIRisk(BaseModel):
    category: Literal["competitive", "implementation", "regulatory", "ethical"]
    risk: str
    severity: Literal["high", "medium", "low"]
    quote: str

class Milestone(BaseModel):
    date: str
    event: str

class AITimeline(BaseModel):
    current_initiatives: List[str]
    near_term_plans: List[str]
    long_term_vision: str
    milestones: List[Milestone]

class CompetitivePositioning(BaseModel):
    strengths: List[str]
    competitors_mentioned: List[str]
    differentiation: str
    concerns_about_competition: List[str]

class AIInsights(BaseModel):
    investments: List[AIInvestment]
    products: List[AIProduct]
    risks: List[AIRisk]
    timeline: AITimeline
    competitive_positioning: CompetitivePositioning

class JobPosting(BaseModel):
    title: str
    location: str
    job_url: str
    tech_stack: List[str]
    posted_date: str
    seniority: Literal["junior", "mid", "senior", "staff", "principal"]
    remote: bool

class HiringData(BaseModel):
    total_jobs: int
    ai_jobs: int
    ai_job_details: List[JobPosting]
    hiring_urgency: Literal["HIGH", "NORMAL", "LOW"]
    tech_stack: List[str]
    scraped_at: str

class NewsItem(BaseModel):
    headline: str
    source: str
    date: str
    url: str
    summary: Optional[str] = None
    category: Literal["product_launch", "investment", "partnership", "research", "executive", "general"]

class EnrichmentData(BaseModel):
    hiring: HiringData
    recent_news: List[NewsItem]
    enriched_at: str

class AIMaturityScore(BaseModel):
    total_score: int = Field(..., ge=0, le=100)
    breakdown: Dict[str, int]  # investment, product, strategic_importance, organizational_readiness
    percentile: int = Field(..., ge=0, le=100)
    label: Literal["Leader", "Fast Follower", "Emerging", "Laggard"]

class SDRPlaybook(BaseModel):
    discovery_questions: List[str]
    value_propositions: List[str]
    objection_handlers: Dict[str, str]
    executive_summary: str
    talking_points: List[str]

class ProfileMetadata(BaseModel):
    analyzed_at: str
    analysis_time_seconds: float
    retrieval_time_seconds: float
    enrichment_time_seconds: float
    enrichment_completeness: float = Field(..., ge=0, le=1)
    status: Literal["complete", "partial", "failed"]

class CompanyProfile(BaseModel):
    company: Company
    filing_date: str
    fiscal_year: int
    ai_insights: AIInsights
    enrichment: EnrichmentData
    ai_maturity: AIMaturityScore
    sdr_playbook: SDRPlaybook
    metadata: ProfileMetadata

# ============================================================================
# PIPELINE MODELS
# ============================================================================

class PipelineStartRequest(BaseModel):
    company_tickers: List[str] = Field(..., min_items=1, max_items=50)
    skip_enrichment: bool = False

class PipelineStartResponse(BaseModel):
    job_id: str
    status: Literal["started"]
    total_companies: int
    estimated_time_seconds: int
    started_at: str

# ... (remaining models similar to TypeScript)
```

---

## REST API Endpoints

### 1. Pipeline Management

#### **POST /api/v1/pipeline/start**

Start the intelligence pipeline for multiple companies.

**Request:**
```json
{
  "company_tickers": ["MSFT", "AAPL", "NVDA"],
  "skip_enrichment": false
}
```

**Response: 202 Accepted**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "started",
  "total_companies": 3,
  "estimated_time_seconds": 420,
  "started_at": "2025-10-18T14:30:00Z"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid tickers or too many companies
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid company tickers provided",
    "details": {
      "invalid_tickers": ["INVALID"],
      "valid_tickers": ["MSFT", "AAPL", "NVDA", ...]
    }
  }
}
```

- `429 Too Many Requests` - Concurrent job limit exceeded
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Maximum concurrent jobs (3) exceeded",
    "details": {
      "active_jobs": 3,
      "retry_after_seconds": 120
    }
  }
}
```

---

#### **GET /api/v1/pipeline/status/{job_id}**

Get current pipeline execution status.

**Response: 200 OK**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_progress",
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
      "stage": "finalization",
      "started_at": "2025-10-18T14:30:01Z",
      "completed_at": "2025-10-18T14:30:19Z"
    },
    {
      "ticker": "AAPL",
      "status": "enriching",
      "stage": "enrichment",
      "message": "Scraping career page for AI job postings...",
      "started_at": "2025-10-18T14:30:02Z"
    },
    {
      "ticker": "NVDA",
      "status": "pending",
      "stage": null
    }
  ],
  "started_at": "2025-10-18T14:30:00Z",
  "estimated_completion": "2025-10-18T14:37:00Z"
}
```

**Error: 404 Not Found**
```json
{
  "error": {
    "code": "JOB_NOT_FOUND",
    "message": "Pipeline job '550e8400-...' not found",
    "details": {
      "job_id": "550e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

---

#### **GET /api/v1/pipeline/results/{job_id}**

Get completed pipeline results.

**Response: 200 OK**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "results": [
    {
      "company": {
        "name": "Microsoft Corporation",
        "ticker": "MSFT",
        "cik": "0000789019",
        "domain": "microsoft.com"
      },
      "filing_date": "2024-07-30",
      "fiscal_year": 2024,
      "ai_insights": {
        "investments": [
          {
            "amount": "$50M",
            "amount_numeric": 50000000,
            "purpose": "AI infrastructure and OpenAI partnership",
            "timeframe": "FY2024",
            "quote": "We continue to invest heavily in AI capabilities...",
            "confidence": "high",
            "source_section": "mda"
          }
        ],
        "products": [
          {
            "product_name": "GitHub Copilot",
            "description": "AI-powered code completion tool",
            "launch_status": "available",
            "target_market": "developer",
            "quote": "GitHub Copilot has been adopted by millions of developers...",
            "revenue_impact": "mentioned"
          }
        ],
        "risks": [
          {
            "category": "competitive",
            "risk": "Intense competition from Google and Amazon in AI",
            "severity": "high",
            "quote": "We face intense competition in the AI and cloud markets..."
          }
        ],
        "timeline": {
          "current_initiatives": ["Azure OpenAI Service expansion", "Copilot integration"],
          "near_term_plans": ["AI model optimization", "Edge AI deployment"],
          "long_term_vision": "Democratize AI access through Azure platform",
          "milestones": [
            {
              "date": "2024-Q1",
              "event": "Launch of GPT-4 integration in Azure"
            }
          ]
        },
        "competitive_positioning": {
          "strengths": ["Azure cloud infrastructure", "OpenAI partnership"],
          "competitors_mentioned": ["Google", "Amazon", "Meta"],
          "differentiation": "Enterprise-focused AI with strong security",
          "concerns_about_competition": ["Google's AI research capabilities"]
        }
      },
      "enrichment": {
        "hiring": {
          "total_jobs": 150,
          "ai_jobs": 23,
          "ai_job_details": [
            {
              "title": "Senior ML Engineer",
              "location": "Seattle, WA (Remote)",
              "job_url": "https://careers.microsoft.com/...",
              "tech_stack": ["Python", "TensorFlow", "Azure ML"],
              "posted_date": "2025-10-10",
              "seniority": "senior",
              "remote": true
            }
          ],
          "hiring_urgency": "HIGH",
          "tech_stack": ["Python", "PyTorch", "TensorFlow", "Azure ML", "CUDA"],
          "scraped_at": "2025-10-18T14:30:15Z"
        },
        "recent_news": [
          {
            "headline": "Microsoft announces new AI features in Office 365",
            "source": "TechCrunch",
            "date": "2025-10-15",
            "url": "https://techcrunch.com/...",
            "summary": "Microsoft unveils Copilot Pro with advanced AI capabilities",
            "category": "product_launch"
          }
        ],
        "enriched_at": "2025-10-18T14:30:18Z"
      },
      "ai_maturity": {
        "total_score": 85,
        "breakdown": {
          "investment": 23,
          "product": 22,
          "strategic_importance": 21,
          "organizational_readiness": 19
        },
        "percentile": 92,
        "label": "Leader"
      },
      "sdr_playbook": {
        "discovery_questions": [
          "I noticed you invested $50M in AI infrastructure last year - what's been the ROI?",
          "Your 10-K mentions competitive pressure from Google AI - how are you differentiating?",
          "You have 23 open AI roles - what capabilities are you building?"
        ],
        "value_propositions": [
          "Help Microsoft-scale organizations leverage similar AI infrastructure",
          "Proven expertise in enterprise AI deployment (23 active AI hiring roles)",
          "Understanding of regulatory concerns around AI ethics"
        ],
        "objection_handlers": {
          "too_expensive": "Microsoft invested $50M in AI last year - this represents 0.1% of that scale",
          "already_have_solution": "With 23 open AI roles, you're clearly scaling - we can accelerate that"
        },
        "executive_summary": "Microsoft is an AI Leader (85/100) with significant investment ($50M in FY2024) across infrastructure, R&D, and strategic partnerships like OpenAI. They're actively hiring 23 AI roles (HIGH urgency) focusing on PyTorch/TensorFlow/Azure ML stack. Recent product launches (Copilot Pro) show execution capability. Primary competitive concern: Google's AI research. Key conversation angles: enterprise AI security, Azure integration, developer tools.",
        "talking_points": [
          "Recent $50M AI investment signals aggressive expansion",
          "23 active AI hiring roles indicate scaling phase",
          "OpenAI partnership creates unique positioning",
          "Competitive pressure from Google mentioned 3x in 10-K"
        ]
      },
      "metadata": {
        "analyzed_at": "2025-10-18T14:30:19Z",
        "analysis_time_seconds": 15.3,
        "retrieval_time_seconds": 2.1,
        "enrichment_time_seconds": 3.2,
        "enrichment_completeness": 0.95,
        "status": "complete"
      }
    }
  ],
  "summary": {
    "total_companies": 3,
    "successful": 3,
    "failed": 0,
    "total_time_seconds": 385
  }
}
```

**Error: 425 Too Early**
```json
{
  "error": {
    "code": "PROCESSING_IN_PROGRESS",
    "message": "Pipeline job is still processing",
    "details": {
      "status": "in_progress",
      "percentage": 67
    }
  }
}
```

---

### 2. Company Intelligence

#### **GET /api/v1/companies**

List all available/processed companies.

**Response: 200 OK**
```json
{
  "companies": [
    {
      "name": "Microsoft Corporation",
      "ticker": "MSFT",
      "cik": "0000789019",
      "domain": "microsoft.com"
    },
    {
      "name": "Apple Inc.",
      "ticker": "AAPL",
      "cik": "0000320193",
      "domain": "apple.com"
    }
  ]
}
```

---

#### **GET /api/v1/companies/{ticker}**

Get full intelligence profile for a specific company.

**Example: GET /api/v1/companies/MSFT**

**Response: 200 OK**
```json
{
  // Full CompanyProfile object (same structure as in pipeline results)
}
```

**Error: 404 Not Found**
```json
{
  "error": {
    "code": "COMPANY_NOT_FOUND",
    "message": "Company 'INVALID' not found",
    "details": {
      "ticker": "INVALID",
      "available_tickers": ["MSFT", "AAPL", "NVDA", ...]
    }
  }
}
```

---

#### **GET /api/v1/companies/{ticker}/insights**

Get only AI insights (without enrichment data).

**Response: 200 OK**
```json
{
  "company": {
    "name": "Microsoft Corporation",
    "ticker": "MSFT",
    "cik": "0000789019"
  },
  "ai_insights": {
    // Full AIInsights object
  },
  "ai_maturity": {
    // Full AIMaturityScore object
  },
  "metadata": {
    "analyzed_at": "2025-10-18T14:30:19Z"
  }
}
```

---

#### **GET /api/v1/companies/{ticker}/enrichment**

Get only live enrichment data (jobs, news).

**Response: 200 OK**
```json
{
  "company": {
    "name": "Microsoft Corporation",
    "ticker": "MSFT"
  },
  "enrichment": {
    // Full EnrichmentData object
  }
}
```

---

### 3. Comparison & Analytics

#### **GET /api/v1/comparison**

Compare multiple companies side-by-side.

**Query Parameters:**
- `tickers` (required): Comma-separated ticker list, e.g., `?tickers=MSFT,AAPL,NVDA`

**Example: GET /api/v1/comparison?tickers=MSFT,AAPL,NVDA**

**Response: 200 OK**
```json
{
  "companies": [
    {
      "ticker": "MSFT",
      "name": "Microsoft Corporation",
      "ai_maturity_score": 85,
      "total_investment": 50000000,
      "ai_jobs": 23,
      "ai_products_count": 5,
      "recent_news_count": 3,
      "label": "Leader"
    },
    {
      "ticker": "NVDA",
      "name": "NVIDIA Corporation",
      "ai_maturity_score": 92,
      "total_investment": 75000000,
      "ai_jobs": 47,
      "ai_products_count": 8,
      "recent_news_count": 6,
      "label": "Leader"
    },
    {
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "ai_maturity_score": 78,
      "total_investment": 35000000,
      "ai_jobs": 15,
      "ai_products_count": 4,
      "recent_news_count": 2,
      "label": "Fast Follower"
    }
  ],
  "rankings": {
    "by_maturity": ["NVDA", "MSFT", "AAPL"],
    "by_investment": ["NVDA", "MSFT", "AAPL"],
    "by_hiring": ["NVDA", "MSFT", "AAPL"]
  }
}
```

---

### 4. Export

#### **POST /api/v1/export/salesforce**

Generate Salesforce-ready CSV export.

**Request:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response: 200 OK**
```json
{
  "download_url": "/downloads/salesforce_550e8400-e29b-41d4.csv",
  "filename": "salesforce_import_2025-10-18.csv",
  "expires_at": "2025-10-18T18:30:00Z"
}
```

**CSV Format:**
```csv
Company Name,Ticker,AI Maturity Score,Label,Total Investment,AI Products,AI Jobs,Executive Summary,Discovery Questions
"Microsoft Corporation","MSFT",85,"Leader",50000000,5,23,"Microsoft is an AI Leader...","Q1: I noticed you invested $50M..."
```

---

#### **POST /api/v1/export/playbooks**

Generate PDF playbooks for sales teams.

**Request:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "tickers": ["MSFT", "AAPL"]  // Optional, defaults to all
}
```

**Response: 200 OK**
```json
{
  "download_url": "/downloads/playbooks_550e8400-e29b-41d4.zip",
  "filename": "ai_playbooks_2025-10-18.zip",
  "files_included": [
    "MSFT_playbook.pdf",
    "AAPL_playbook.pdf",
    "ALL_COMPANIES_comparison.pdf"
  ],
  "expires_at": "2025-10-18T18:30:00Z"
}
```

---

### 5. Health & Utilities

#### **GET /api/v1/health**

Service health check.

**Response: 200 OK**
```json
{
  "status": "healthy",
  "daytona": "connected",
  "anthropic_api": "connected",
  "version": "1.0.0",
  "uptime_seconds": 86400
}
```

**Response: 503 Service Unavailable** (if degraded)
```json
{
  "status": "degraded",
  "daytona": "disconnected",
  "anthropic_api": "connected",
  "version": "1.0.0",
  "uptime_seconds": 86400
}
```

---

## WebSocket API

### Connection

**Endpoint:** `ws://localhost:8000/ws/pipeline/{job_id}`

**Example:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/pipeline/550e8400-e29b-41d4-a716-446655440000');
```

### Message Types

#### 1. Progress Update

```json
{
  "type": "progress",
  "data": {
    "ticker": "MSFT",
    "stage": "enrichment",
    "status": "in_progress",
    "message": "Scraping career page for AI job postings...",
    "percentage": 45
  }
}
```

#### 2. Stage Change

```json
{
  "type": "stage_change",
  "data": {
    "ticker": "MSFT",
    "from_stage": "analysis",
    "to_stage": "enrichment"
  }
}
```

#### 3. Company Complete

```json
{
  "type": "complete",
  "data": {
    "ticker": "MSFT",
    "profile": {
      // Full CompanyProfile object
    }
  }
}
```

#### 4. Error

```json
{
  "type": "error",
  "data": {
    "ticker": "AAPL",
    "stage": "retrieval",
    "error": "SEC EDGAR rate limit exceeded, retrying in 30s..."
  }
}
```

---

## Error Handling

### Error Response Format

All errors follow this structure:

```typescript
interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
}
```

### Error Codes

| Code | HTTP Status | Description | Solution |
|------|-------------|-------------|----------|
| `INVALID_REQUEST` | 400 | Invalid request data | Check request schema |
| `INVALID_TICKER` | 400 | Unknown company ticker | Use valid ticker from `/companies` |
| `JOB_NOT_FOUND` | 404 | Pipeline job doesn't exist | Verify job_id from `/pipeline/start` |
| `COMPANY_NOT_FOUND` | 404 | Company not processed | Run pipeline first |
| `PROCESSING_IN_PROGRESS` | 425 | Data not ready yet | Wait for completion or use WebSocket |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests | Implement exponential backoff |
| `DAYTONA_UNAVAILABLE` | 503 | Daytona service down | Check backend logs, retry later |
| `LLM_API_ERROR` | 503 | Anthropic API error | Check API key, rate limits |
| `PARSING_ERROR` | 500 | 10-K parsing failed | File an issue with ticker |

---

## Frontend Integration Examples

### Complete Pipeline Flow (TypeScript)

```typescript
import { useState, useEffect } from 'react';

// API client setup
const API_BASE = import.meta.env.VITE_API_BASE_URL;
const WS_URL = import.meta.env.VITE_WS_URL;

interface PipelineManager {
  startPipeline: (tickers: string[]) => Promise<void>;
  jobId: string | null;
  progress: number;
  companies: CompanyStatus[];
  results: CompanyProfile[];
  error: string | null;
}

export function usePipeline(): PipelineManager {
  const [jobId, setJobId] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [companies, setCompanies] = useState<CompanyStatus[]>([]);
  const [results, setResults] = useState<CompanyProfile[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [ws, setWs] = useState<WebSocket | null>(null);

  const startPipeline = async (tickers: string[]) => {
    try {
      const response = await fetch(`${API_BASE}/pipeline/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company_tickers: tickers }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error.message);
      }

      const data: PipelineStartResponse = await response.json();
      setJobId(data.job_id);

      // Connect WebSocket
      const websocket = new WebSocket(`${WS_URL}/pipeline/${data.job_id}`);

      websocket.onmessage = (event) => {
        const message: WebSocketMessage = JSON.parse(event.data);

        if (message.type === 'progress') {
          // Update progress UI
          setProgress(message.data.percentage);
        } else if (message.type === 'complete') {
          // Add to results
          setResults((prev) => [...prev, message.data.profile]);
        } else if (message.type === 'error') {
          setError(message.data.error);
        }
      };

      websocket.onerror = () => {
        // Fallback to polling if WebSocket fails
        pollStatus(data.job_id);
      };

      setWs(websocket);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Pipeline failed');
    }
  };

  const pollStatus = async (jobId: string) => {
    const interval = setInterval(async () => {
      const response = await fetch(`${API_BASE}/pipeline/status/${jobId}`);
      const data: PipelineStatusResponse = await response.json();

      setProgress(data.progress.percentage);
      setCompanies(data.companies);

      if (data.status === 'completed') {
        clearInterval(interval);
        fetchResults(jobId);
      }
    }, 2000);
  };

  const fetchResults = async (jobId: string) => {
    const response = await fetch(`${API_BASE}/pipeline/results/${jobId}`);
    const data: PipelineResultsResponse = await response.json();
    setResults(data.results);
  };

  // Cleanup WebSocket on unmount
  useEffect(() => {
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [ws]);

  return {
    startPipeline,
    jobId,
    progress,
    companies,
    results,
    error,
  };
}

// Usage in component
function Dashboard() {
  const { startPipeline, progress, results, error } = usePipeline();

  const handleStart = () => {
    startPipeline(['MSFT', 'AAPL', 'NVDA']);
  };

  return (
    <div>
      <button onClick={handleStart}>Start Pipeline</button>
      {progress > 0 && <ProgressBar value={progress} />}
      {results.map((company) => (
        <CompanyCard key={company.company.ticker} profile={company} />
      ))}
      {error && <ErrorMessage message={error} />}
    </div>
  );
}
```

### Export Functionality

```typescript
async function exportToSalesforce(jobId: string) {
  const response = await fetch(`${API_BASE}/export/salesforce`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ job_id: jobId }),
  });

  const data: ExportSalesforceResponse = await response.json();

  // Download file
  const link = document.createElement('a');
  link.href = `${API_BASE}${data.download_url}`;
  link.download = data.filename;
  link.click();
}
```

---

## Backend Implementation Guide

### FastAPI Project Structure

```
backend/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── pipeline.py       # Pipeline endpoints
│   │   │   ├── companies.py      # Company endpoints
│   │   │   ├── comparison.py     # Comparison endpoint
│   │   │   ├── export.py         # Export endpoints
│   │   │   └── websocket.py      # WebSocket handler
│   │   └── dependencies.py       # Shared dependencies
│   ├── services/
│   │   ├── retrieval/            # 10-K retrieval logic
│   │   ├── analysis/             # AI analysis logic
│   │   └── enrichment/           # Live enrichment logic
│   ├── models/
│   │   ├── api.py               # Pydantic request/response models
│   │   └── domain.py            # Domain models
│   ├── core/
│   │   ├── config.py            # Configuration
│   │   └── job_manager.py       # Pipeline job management
│   └── utils/
│       ├── sec_edgar.py         # SEC EDGAR utilities
│       └── llm_client.py        # Anthropic API client
└── main.py                      # FastAPI app entry point
```

### Key Implementation Notes

#### 1. CORS Configuration

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2. Pipeline Job Management

```python
from fastapi import BackgroundTasks
import asyncio

# In-memory job store (use Redis in production)
pipeline_jobs: Dict[str, PipelineJob] = {}

@app.post("/api/v1/pipeline/start")
async def start_pipeline(
    request: PipelineStartRequest,
    background_tasks: BackgroundTasks
):
    job_id = str(uuid.uuid4())

    # Create job
    pipeline_jobs[job_id] = {
        "job_id": job_id,
        "status": "started",
        "companies": [{"ticker": t, "status": "pending"} for t in request.company_tickers],
        "started_at": datetime.utcnow().isoformat(),
    }

    # Start background processing
    background_tasks.add_task(process_pipeline, job_id, request.company_tickers)

    return {
        "job_id": job_id,
        "status": "started",
        "total_companies": len(request.company_tickers),
        "estimated_time_seconds": len(request.company_tickers) * 140,
        "started_at": pipeline_jobs[job_id]["started_at"],
    }
```

#### 3. WebSocket Connection Manager

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, job_id: str):
        await websocket.accept()
        if job_id not in self.active_connections:
            self.active_connections[job_id] = set()
        self.active_connections[job_id].add(websocket)

    def disconnect(self, websocket: WebSocket, job_id: str):
        self.active_connections[job_id].remove(websocket)

    async def send_message(self, message: dict, job_id: str):
        if job_id in self.active_connections:
            for connection in self.active_connections[job_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/pipeline/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await manager.connect(websocket, job_id)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket, job_id)
```

---

## Testing & Validation

### Backend Tests (pytest)

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_start_pipeline():
    response = client.post("/api/v1/pipeline/start", json={
        "company_tickers": ["MSFT"]
    })
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "started"

def test_get_company():
    response = client.get("/api/v1/companies/MSFT")
    assert response.status_code == 200
    data = response.json()
    assert data["company"]["ticker"] == "MSFT"
```

### Frontend Tests (Vitest)

```typescript
import { describe, it, expect, vi } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { usePipeline } from './usePipeline';
import { server } from '../mocks/server';
import { rest } from 'msw';

describe('usePipeline', () => {
  it('starts pipeline and receives results', async () => {
    const { result } = renderHook(() => usePipeline());

    await result.current.startPipeline(['MSFT']);

    await waitFor(() => {
      expect(result.current.jobId).not.toBeNull();
      expect(result.current.progress).toBeGreaterThan(0);
    });
  });
});
```

---

## Appendix: Mock Data for Development

### Frontend Mock Service

```typescript
// services/mockApi.ts
export const mockCompanyProfile: CompanyProfile = {
  company: {
    name: "Microsoft Corporation",
    ticker: "MSFT",
    cik: "0000789019",
    domain: "microsoft.com"
  },
  filing_date: "2024-07-30",
  fiscal_year: 2024,
  ai_insights: {
    investments: [
      {
        amount: "$50M",
        amount_numeric: 50000000,
        purpose: "AI infrastructure",
        timeframe: "FY2024",
        quote: "We continue to invest...",
        confidence: "high",
        source_section: "mda"
      }
    ],
    products: [
      {
        product_name: "GitHub Copilot",
        description: "AI code completion",
        launch_status: "available",
        target_market: "developer",
        quote: "Copilot has been adopted...",
        revenue_impact: "mentioned"
      }
    ],
    risks: [],
    timeline: {
      current_initiatives: ["Azure OpenAI"],
      near_term_plans: ["Edge AI"],
      long_term_vision: "Democratize AI",
      milestones: []
    },
    competitive_positioning: {
      strengths: ["Azure infrastructure"],
      competitors_mentioned: ["Google", "Amazon"],
      differentiation: "Enterprise focus",
      concerns_about_competition: ["Google's AI research"]
    }
  },
  enrichment: {
    hiring: {
      total_jobs: 150,
      ai_jobs: 23,
      ai_job_details: [],
      hiring_urgency: "HIGH",
      tech_stack: ["Python", "PyTorch"],
      scraped_at: new Date().toISOString()
    },
    recent_news: [],
    enriched_at: new Date().toISOString()
  },
  ai_maturity: {
    total_score: 85,
    breakdown: {
      investment: 23,
      product: 22,
      strategic_importance: 21,
      organizational_readiness: 19
    },
    percentile: 92,
    label: "Leader"
  },
  sdr_playbook: {
    discovery_questions: ["Q1", "Q2"],
    value_propositions: ["VP1"],
    objection_handlers: {},
    executive_summary: "Microsoft is a leader...",
    talking_points: ["Point 1"]
  },
  metadata: {
    analyzed_at: new Date().toISOString(),
    analysis_time_seconds: 15.3,
    retrieval_time_seconds: 2.1,
    enrichment_time_seconds: 3.2,
    enrichment_completeness: 0.95,
    status: "complete"
  }
};
```

---

**Version:** 2.0.0
**Status:** Ready for Implementation
**Last Updated:** 2025-10-18

**Questions?** Contact frontend or backend teams for clarifications.
