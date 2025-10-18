# Backend Mock Endpoints Specification

**For:** Backend Team
**Purpose:** Implement `/mock/*` endpoints for frontend integration testing
**Estimated Time:** 30-45 minutes
**Priority:** HIGH (unblocks full frontend testing)

---

## Overview

The frontend team has built a complete integration layer with **3 modes**:

1. **CLIENT_MOCK** (current) - Client-side mocks, no backend needed
2. **BACKEND_MOCK** (next) - Real HTTP requests to your `/mock/*` endpoints ⭐ **YOU BUILD THIS**
3. **REAL** (final) - Full production backend

By implementing mock endpoints, you enable the frontend to test:
- ✅ Real HTTP requests
- ✅ CORS configuration
- ✅ Request/response serialization
- ✅ Error handling
- ✅ Network latency
- ✅ Type compatibility

**All while you build the real pipeline in parallel!**

---

## What You Need to Build

### 9 Mock Endpoints

All endpoints should return **realistic fake data instantly** (no actual processing).

| Endpoint | Method | Purpose | Time to Build |
|----------|--------|---------|---------------|
| `/mock/companies/{ticker}` | GET | Return company profile | 5 min |
| `/mock/pipeline/start` | POST | Start fake pipeline | 5 min |
| `/mock/pipeline/status/{job_id}` | GET | Return fake progress | 5 min |
| `/mock/pipeline/results/{job_id}` | GET | Return fake results | 5 min |
| `/mock/companies` | GET | List all companies | 3 min |
| `/mock/comparison?tickers=...` | GET | Compare companies | 5 min |
| `/mock/export/salesforce` | POST | Generate fake CSV | 3 min |
| `/mock/export/playbooks` | POST | Generate fake PDFs | 3 min |
| `/mock/health` | GET | Health check | 2 min |

**Total:** ~35 minutes

---

## Detailed Specifications

### 1. GET /api/v1/mock/companies/{ticker}

**Purpose:** Return a complete company profile.

**Example Request:**
```bash
GET /api/v1/mock/companies/MSFT
```

**Example Response:** `200 OK`
```json
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
        "purpose": "AI infrastructure and OpenAI partnership expansion",
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
        "quote": "GitHub Copilot has been adopted by millions...",
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
        { "date": "2024-Q1", "event": "GPT-4 integration in Azure" }
      ]
    },
    "competitive_positioning": {
      "strengths": ["Azure infrastructure", "OpenAI partnership"],
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
          "job_url": "https://careers.microsoft.com/job/123",
          "tech_stack": ["Python", "TensorFlow", "Azure ML", "PyTorch"],
          "posted_date": "2025-10-13",
          "seniority": "senior",
          "remote": true
        }
      ],
      "hiring_urgency": "HIGH",
      "tech_stack": ["Python", "PyTorch", "TensorFlow", "Azure ML"],
      "scraped_at": "2025-10-18T10:00:00Z"
    },
    "recent_news": [
      {
        "headline": "Microsoft announces new AI features in Office 365",
        "source": "TechCrunch",
        "date": "2025-10-16",
        "url": "https://techcrunch.com/microsoft-ai",
        "summary": "Microsoft unveils Copilot Pro...",
        "category": "product_launch"
      }
    ],
    "enriched_at": "2025-10-18T10:00:00Z"
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
      "Your 10-K mentions competitive pressure from Google AI - how are you differentiating?"
    ],
    "value_propositions": [
      "Help Microsoft-scale organizations leverage similar AI infrastructure"
    ],
    "objection_handlers": {
      "too_expensive": "Microsoft invested $50M in AI last year..."
    },
    "executive_summary": "Microsoft is an AI Leader (85/100) with significant investment...",
    "talking_points": ["Recent $50M AI investment signals aggressive expansion"]
  },
  "metadata": {
    "analyzed_at": "2025-10-18T10:00:00Z",
    "analysis_time_seconds": 15.3,
    "retrieval_time_seconds": 2.1,
    "enrichment_time_seconds": 3.2,
    "enrichment_completeness": 0.95,
    "status": "complete"
  }
}
```

**Implementation Tip:**
```python
# Store mock data in a dict or file
MOCK_PROFILES = {
    "MSFT": {...},  # Full Microsoft profile above
    "AAPL": {...},  # Apple profile
    "NVDA": {...},  # NVIDIA profile
}

@app.get("/api/v1/mock/companies/{ticker}")
def get_mock_company(ticker: str):
    if ticker not in MOCK_PROFILES:
        raise HTTPException(404, detail={"error": {
            "code": "COMPANY_NOT_FOUND",
            "message": f"Company '{ticker}' not found"
        }})
    return MOCK_PROFILES[ticker]
```

---

### 2. POST /api/v1/mock/pipeline/start

**Purpose:** Start a fake pipeline job.

**Example Request:**
```json
POST /api/v1/mock/pipeline/start
{
  "company_tickers": ["MSFT", "AAPL", "NVDA"],
  "skip_enrichment": false
}
```

**Example Response:** `202 Accepted`
```json
{
  "job_id": "mock-job-1729260000000",
  "status": "started",
  "total_companies": 3,
  "estimated_time_seconds": 420,
  "started_at": "2025-10-18T10:00:00Z"
}
```

**Implementation Tip:**
```python
import uuid
from datetime import datetime

@app.post("/api/v1/mock/pipeline/start")
def start_mock_pipeline(request: PipelineStartRequest):
    job_id = f"mock-job-{uuid.uuid4()}"

    return {
        "job_id": job_id,
        "status": "started",
        "total_companies": len(request.company_tickers),
        "estimated_time_seconds": len(request.company_tickers) * 140,
        "started_at": datetime.utcnow().isoformat() + "Z"
    }
```

---

### 3. GET /api/v1/mock/pipeline/status/{job_id}

**Purpose:** Return fake pipeline progress.

**Example Request:**
```bash
GET /api/v1/mock/pipeline/status/mock-job-123
```

**Example Response:** `200 OK`
```json
{
  "job_id": "mock-job-123",
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
      "started_at": "2025-10-18T10:00:01Z",
      "completed_at": "2025-10-18T10:00:19Z"
    },
    {
      "ticker": "AAPL",
      "status": "enriching",
      "stage": "enrichment",
      "message": "Scraping career page for AI job postings...",
      "started_at": "2025-10-18T10:00:02Z"
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

**Implementation Tip:**
```python
# Simple approach: Always return "completed" after 5 seconds
@app.get("/api/v1/mock/pipeline/status/{job_id}")
def get_mock_status(job_id: str):
    # Check if job exists (you could store in-memory dict)
    if not job_id.startswith("mock-job-"):
        raise HTTPException(404, detail={"error": {
            "code": "JOB_NOT_FOUND",
            "message": f"Pipeline job '{job_id}' not found"
        }})

    # For simplicity, always return "completed"
    return {
        "job_id": job_id,
        "status": "completed",
        "progress": {
            "current_stage": "finalization",
            "companies_processed": 3,
            "companies_total": 3,
            "percentage": 100
        },
        "companies": [
            {"ticker": "MSFT", "status": "completed", "stage": "finalization"},
            {"ticker": "AAPL", "status": "completed", "stage": "finalization"},
            {"ticker": "NVDA", "status": "completed", "stage": "finalization"}
        ],
        "started_at": "2025-10-18T10:00:00Z",
        "completed_at": "2025-10-18T10:00:30Z"
    }
```

---

### 4. GET /api/v1/mock/pipeline/results/{job_id}

**Purpose:** Return fake pipeline results.

**Example Response:** `200 OK`
```json
{
  "job_id": "mock-job-123",
  "status": "completed",
  "results": [
    {
      // Full CompanyProfile for MSFT (same as GET /companies/MSFT)
    },
    {
      // Full CompanyProfile for AAPL
    },
    {
      // Full CompanyProfile for NVDA
    }
  ],
  "summary": {
    "total_companies": 3,
    "successful": 3,
    "failed": 0,
    "total_time_seconds": 45
  }
}
```

**Implementation Tip:**
```python
@app.get("/api/v1/mock/pipeline/results/{job_id}")
def get_mock_results(job_id: str):
    return {
        "job_id": job_id,
        "status": "completed",
        "results": [
            MOCK_PROFILES["MSFT"],
            MOCK_PROFILES["AAPL"],
            MOCK_PROFILES["NVDA"]
        ],
        "summary": {
            "total_companies": 3,
            "successful": 3,
            "failed": 0,
            "total_time_seconds": 45
        }
    }
```

---

### 5-9. Remaining Endpoints (Quick Implementation)

```python
# 5. GET /mock/companies
@app.get("/api/v1/mock/companies")
def list_mock_companies():
    return {
        "companies": [
            {"name": "Microsoft Corporation", "ticker": "MSFT", "cik": "0000789019"},
            {"name": "Apple Inc.", "ticker": "AAPL", "cik": "0000320193"},
            {"name": "NVIDIA Corporation", "ticker": "NVDA", "cik": "0001045810"}
        ]
    }

# 6. GET /mock/comparison?tickers=MSFT,AAPL
@app.get("/api/v1/mock/comparison")
def mock_comparison(tickers: str):
    ticker_list = tickers.split(',')
    return {
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
            }
        ],
        "rankings": {
            "by_maturity": ["MSFT", "NVDA", "AAPL"],
            "by_investment": ["MSFT", "NVDA", "AAPL"],
            "by_hiring": ["NVDA", "MSFT", "AAPL"]
        }
    }

# 7. POST /mock/export/salesforce
@app.post("/api/v1/mock/export/salesforce")
def mock_salesforce_export(request: ExportSalesforceRequest):
    return {
        "download_url": f"/downloads/salesforce_{request.job_id}.csv",
        "filename": f"salesforce_import_{datetime.now().date()}.csv",
        "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
    }

# 8. POST /mock/export/playbooks
@app.post("/api/v1/mock/export/playbooks")
def mock_playbooks_export(request: ExportPlaybooksRequest):
    tickers = request.tickers or ["MSFT", "AAPL", "NVDA"]
    return {
        "download_url": f"/downloads/playbooks_{request.job_id}.zip",
        "filename": f"ai_playbooks_{datetime.now().date()}.zip",
        "files_included": [f"{t}_playbook.pdf" for t in tickers] + ["ALL_COMPANIES.pdf"],
        "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
    }

# 9. GET /mock/health
@app.get("/api/v1/mock/health")
def mock_health():
    return {
        "status": "healthy",
        "daytona": "connected",
        "anthropic_api": "connected",
        "version": "1.0.0-mock",
        "uptime_seconds": 12345
    }
```

---

## Complete FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import uuid

app = FastAPI(title="10-K Pipeline Mock API")

# CORS - CRITICAL!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data (copy from frontend/src/mocks/mockData.ts or docs)
MOCK_PROFILES = {
    "MSFT": {
        "company": {"name": "Microsoft Corporation", "ticker": "MSFT", "cik": "0000789019"},
        "ai_maturity": {"total_score": 85, "label": "Leader", ...},
        # ... rest of profile
    },
    # Add AAPL, NVDA, etc.
}

# Request models
class PipelineStartRequest(BaseModel):
    company_tickers: List[str]
    skip_enrichment: bool = False

class ExportSalesforceRequest(BaseModel):
    job_id: str

# ... (Implement endpoints from above)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Testing Your Mock Endpoints

### Step 1: Start Your Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Step 2: Test with curl

```bash
# Test health
curl http://localhost:8000/api/v1/mock/health

# Test company
curl http://localhost:8000/api/v1/mock/companies/MSFT

# Test pipeline start
curl -X POST http://localhost:8000/api/v1/mock/pipeline/start \
  -H "Content-Type: application/json" \
  -d '{"company_tickers": ["MSFT"]}'
```

### Step 3: Connect Frontend

```bash
# In frontend/.env
VITE_API_MODE=BACKEND_MOCK
VITE_API_BASE_URL=http://localhost:8000/api/v1

# Start frontend
cd frontend/anthropic-insight-panel
npm run dev
```

### Step 4: Verify in Browser

1. Open `http://localhost:8080`
2. Check console for: `🧪 API Client: BACKEND_MOCK mode`
3. Click "Start Pipeline"
4. Check Network tab - should see requests to `/mock/*`

---

## Benefits of Mock Endpoints

1. **Frontend can test real HTTP** - CORS, headers, serialization
2. **Backend can develop in parallel** - No blocking
3. **Integration testing** - Catch issues early
4. **Fast iteration** - No waiting for pipeline processing
5. **Reliable demos** - Instant responses, no failures

---

## Timeline

**Total Time:** 30-45 minutes

- [ ] Copy CompanyProfile mock data (10 min)
- [ ] Implement 9 endpoints (25 min)
- [ ] Test with curl (5 min)
- [ ] Test with frontend (5 min)

---

## Questions?

**Frontend ready to test:** Yes! Just flip `VITE_API_MODE=BACKEND_MOCK`

**Full contract:** See `docs/architecture/API_CONTRACT_V2.md`

**Mock data examples:** See `frontend/src/mocks/mockData.ts`

---

**Next:** Implement these mock endpoints, notify frontend team, and continue building real pipeline! 🚀
