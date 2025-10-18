# API Documentation Package - Ready for Backend Development

**Date:** 2025-10-18
**Status:** ✅ Complete and Ready
**Prepared by:** Frontend Team (Claude Code)

---

## 📋 What's Included

I've created comprehensive API documentation for the **10-K AI Intelligence Pipeline** project. The backend team can now start development immediately using these specifications.

### Documentation Files Created

1. **`docs/architecture/API_CONTRACT_V2.md`** ⭐ **MAIN REFERENCE**
   - Complete REST API specification
   - Full TypeScript and Python type definitions
   - All endpoints with request/response examples
   - WebSocket API specification
   - Error handling guide
   - Backend implementation notes

2. **`docs/architecture/FRONTEND_API_INTEGRATION_GUIDE.md`**
   - Frontend integration patterns
   - Custom React hooks
   - API client implementation
   - WebSocket integration
   - Testing strategies
   - Production checklist

3. **`frontend/anthropic-insight-panel/src/types/api.ts`** (Updated)
   - TypeScript types perfectly matching API contract
   - All models, enums, and utility types
   - Backward compatibility aliases
   - Debug/workflow types for hackathon demo

---

## 🎯 Key Features of the API Documentation

### Comprehensive Coverage

✅ **11 REST API Endpoints:**
- Pipeline Management (3 endpoints)
- Company Intelligence (4 endpoints)
- Comparison & Analytics (1 endpoint)
- Export (2 endpoints)
- Health Check (1 endpoint)

✅ **WebSocket API:**
- Real-time pipeline progress updates
- 4 message types (progress, complete, error, stage_change)
- Reconnection logic
- Fallback to polling

✅ **40+ Type Definitions:**
- Company models
- AI insights models
- Enrichment models
- Pipeline models
- Comparison models
- Export models

### Developer-Friendly

✅ **Request/Response Examples:**
- Every endpoint has complete JSON examples
- Success and error response examples
- HTTP status codes documented

✅ **Python Models (Pydantic):**
- Complete backend model definitions
- Field validation rules
- Type hints and literals

✅ **Frontend Integration Code:**
- Complete API client implementation
- Custom React hooks
- WebSocket client with reconnection
- Error handling patterns

---

## 🚀 Quick Start for Backend Team

### 1. Read the API Contract

```bash
open docs/architecture/API_CONTRACT_V2.md
```

This is your **single source of truth**. It contains:
- All endpoint specifications
- Request/response schemas
- Python Pydantic models (copy-paste ready)
- WebSocket message formats
- Error codes and handling

### 2. Understand the Data Flow

```
Frontend → POST /api/v1/pipeline/start
         ↓
Backend creates pipeline job (UUID)
         ↓
WebSocket connection: ws://localhost:8000/ws/pipeline/{job_id}
         ↓
Backend processes companies in parallel (Daytona + Browser-Use)
         ↓
WebSocket sends real-time progress updates
         ↓
Frontend displays progress in real-time
         ↓
Frontend → GET /api/v1/pipeline/results/{job_id}
         ↓
Frontend displays company intelligence
```

### 3. Implement in This Order

**Phase 1: Core Infrastructure (Hour 1)**
1. FastAPI app setup with CORS
2. Pydantic models (copy from API_CONTRACT_V2.md)
3. Job management system (in-memory or Redis)
4. Health endpoint (`/api/v1/health`)

**Phase 2: Pipeline Endpoints (Hours 2-3)**
5. POST `/api/v1/pipeline/start` - Create pipeline job
6. GET `/api/v1/pipeline/status/{job_id}` - Return job status
7. GET `/api/v1/pipeline/results/{job_id}` - Return results

**Phase 3: WebSocket (Hour 4)**
8. WebSocket handler at `/ws/pipeline/{job_id}`
9. Connection manager for multiple clients
10. Message broadcasting

**Phase 4: Company Endpoints (Hour 5)**
11. GET `/api/v1/companies` - List companies
12. GET `/api/v1/companies/{ticker}` - Get company profile
13. GET `/api/v1/companies/{ticker}/insights`
14. GET `/api/v1/companies/{ticker}/enrichment`

**Phase 5: Comparison & Export (Hour 6)**
15. GET `/api/v1/comparison?tickers=...`
16. POST `/api/v1/export/salesforce`
17. POST `/api/v1/export/playbooks`

---

## 📝 Backend Implementation Checklist

### FastAPI Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="10-K AI Intelligence Pipeline", version="1.0.0")

# CORS - CRITICAL for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend dev server
        "http://localhost:8080",  # Vite default
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Pydantic Models

All models are in `API_CONTRACT_V2.md` under "Python Models (Backend - Pydantic)" section. Copy-paste ready!

Example:
```python
from pydantic import BaseModel, Field
from typing import List, Literal

class PipelineStartRequest(BaseModel):
    company_tickers: List[str] = Field(..., min_items=1, max_items=50)
    skip_enrichment: bool = False

class PipelineStartResponse(BaseModel):
    job_id: str
    status: Literal["started"]
    total_companies: int
    estimated_time_seconds: int
    started_at: str
```

### Job Management

```python
import uuid
from datetime import datetime
from typing import Dict

# In-memory storage (use Redis for production)
pipeline_jobs: Dict[str, dict] = {}

@app.post("/api/v1/pipeline/start", response_model=PipelineStartResponse)
async def start_pipeline(
    request: PipelineStartRequest,
    background_tasks: BackgroundTasks
):
    job_id = str(uuid.uuid4())

    pipeline_jobs[job_id] = {
        "job_id": job_id,
        "status": "started",
        "companies": [
            {"ticker": t, "status": "pending"}
            for t in request.company_tickers
        ],
        "started_at": datetime.utcnow().isoformat(),
    }

    # Start background processing
    background_tasks.add_task(
        process_pipeline,
        job_id,
        request.company_tickers
    )

    return PipelineStartResponse(
        job_id=job_id,
        status="started",
        total_companies=len(request.company_tickers),
        estimated_time_seconds=len(request.company_tickers) * 140,
        started_at=pipeline_jobs[job_id]["started_at"],
    )
```

### WebSocket Handler

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
        if job_id in self.active_connections:
            self.active_connections[job_id].discard(websocket)

    async def broadcast(self, message: dict, job_id: str):
        if job_id in self.active_connections:
            for connection in self.active_connections[job_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/pipeline/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await manager.connect(websocket, job_id)
    try:
        while True:
            await websocket.receive_text()  # Keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket, job_id)

# When you want to send updates:
# await manager.broadcast({
#     "type": "progress",
#     "data": {
#         "ticker": "MSFT",
#         "stage": "analysis",
#         "status": "in_progress",
#         "message": "Analyzing 10-K with Claude...",
#         "percentage": 45
#     }
# }, job_id)
```

---

## 🔗 Integration Points

### Frontend Expectations

The frontend is **already built** and waiting for these endpoints to work:

1. **Dashboard Page** expects:
   - POST `/api/v1/pipeline/start` to return job_id
   - WebSocket connection for real-time updates
   - GET `/api/v1/companies/{ticker}` for company details

2. **Company Detail Modal** expects:
   - Full `CompanyProfile` object with nested structure
   - `company.company.name` (nested, not flat!)
   - `ai_insights.investments[]` array
   - `enrichment.hiring.ai_jobs` number

3. **Comparison View** expects:
   - GET `/api/v1/comparison?tickers=MSFT,AAPL,NVDA`
   - Returns `ComparisonResponse` type

4. **Export Buttons** expect:
   - POST `/api/v1/export/salesforce` returns download URL
   - POST `/api/v1/export/playbooks` returns ZIP file URL

### Critical: Type Matching

The frontend types at `frontend/anthropic-insight-panel/src/types/api.ts` **MUST MATCH** the backend responses exactly. I've already ensured this alignment in the API contract.

**Important Structure Notes:**
```typescript
// ✅ CORRECT (nested structure)
{
  "company": {
    "name": "Microsoft Corporation",
    "ticker": "MSFT",
    "cik": "0000789019"
  },
  "ai_insights": {
    "investments": [...],
    "products": [...]
  }
}

// ❌ WRONG (flat structure)
{
  "company_name": "Microsoft Corporation",
  "ticker": "MSFT",
  "investments": [...]
}
```

---

## 🧪 Testing Your API

### Quick Test with curl

```bash
# 1. Health check
curl http://localhost:8000/api/v1/health

# 2. Start pipeline
curl -X POST http://localhost:8000/api/v1/pipeline/start \
  -H "Content-Type: application/json" \
  -d '{"company_tickers": ["MSFT"]}'

# Should return: {"job_id": "...", "status": "started", ...}

# 3. Check status (use job_id from above)
curl http://localhost:8000/api/v1/pipeline/status/YOUR_JOB_ID

# 4. Get company
curl http://localhost:8000/api/v1/companies/MSFT
```

### Frontend Integration Test

Once your endpoints are running:

```bash
# Start backend
cd backend
uvicorn main:app --reload --port 8000

# Start frontend (in another terminal)
cd frontend/anthropic-insight-panel
npm run dev

# Visit: http://localhost:8080
# Click "Start Pipeline" button
# Should see real-time progress updates
```

---

## 📊 API Endpoints Summary

### Pipeline Management

| Method | Endpoint | Purpose | Status Code |
|--------|----------|---------|-------------|
| POST | `/api/v1/pipeline/start` | Start processing | 202 Accepted |
| GET | `/api/v1/pipeline/status/{job_id}` | Get progress | 200 OK |
| GET | `/api/v1/pipeline/results/{job_id}` | Get results | 200 OK |

### Company Intelligence

| Method | Endpoint | Purpose | Status Code |
|--------|----------|---------|-------------|
| GET | `/api/v1/companies` | List all | 200 OK |
| GET | `/api/v1/companies/{ticker}` | Get profile | 200 OK |
| GET | `/api/v1/companies/{ticker}/insights` | Get AI insights only | 200 OK |
| GET | `/api/v1/companies/{ticker}/enrichment` | Get live data only | 200 OK |

### Comparison & Export

| Method | Endpoint | Purpose | Status Code |
|--------|----------|---------|-------------|
| GET | `/api/v1/comparison?tickers=...` | Compare companies | 200 OK |
| POST | `/api/v1/export/salesforce` | Generate CSV | 200 OK |
| POST | `/api/v1/export/playbooks` | Generate PDFs | 200 OK |

### Utilities

| Method | Endpoint | Purpose | Status Code |
|--------|----------|---------|-------------|
| GET | `/api/v1/health` | Health check | 200 OK |

---

## 🎨 Frontend Current State

The frontend team has already built:

✅ **Complete UI:**
- Dashboard with company grid
- Company detail modal with tabs
- Maturity gauge visualization
- Progress tracker modal
- 48+ shadcn/ui components

✅ **TypeScript Types:**
- All API types defined
- Matches API contract exactly

❌ **Missing (waiting for backend):**
- API client implementation (`services/api.ts`)
- WebSocket client (`services/websocket.ts`)
- Custom hooks (`usePipeline`, `useCompanies`)

Once backend is ready, frontend team will implement the integration layer in ~2 hours.

---

## 📚 Reference Documents

### For Backend Team

1. **API_CONTRACT_V2.md** - Start here!
   - Complete API specification
   - Python models ready to copy
   - Request/response examples
   - WebSocket specification

2. **BACKEND_TASKS.md** - Track your progress
   - Epic-by-epic checklist
   - Validation gates

### For Frontend Team

1. **FRONTEND_API_INTEGRATION_GUIDE.md** - Start here!
   - API client implementation
   - Custom hooks
   - WebSocket integration
   - Testing patterns

2. **FRONTEND_TASKS.md** - Track your progress

### For Both Teams

1. **CLAUDE.md** (root) - Project overview
2. **backend/CLAUDE.md** - Backend guidance
3. **frontend/CLAUDE.md** - Frontend guidance

---

## 🔄 Coordination Process

### Daily Sync Points

1. **Morning:** Check BACKEND_TASKS.md and FRONTEND_TASKS.md
2. **Midday:** Test integration if any endpoints are ready
3. **Evening:** Update task files, commit progress

### When Backend Completes an Endpoint

1. Update `BACKEND_TASKS.md` with ✅
2. Test with curl or Postman
3. Notify frontend team
4. Frontend integrates and tests

### If API Contract Needs Changes

1. **Backend team:** Open discussion with frontend
2. **Update:** `API_CONTRACT_V2.md` with versioning
3. **Update:** Frontend types in `types/api.ts`
4. **Update:** Both `BACKEND_TASKS.md` and `FRONTEND_TASKS.md`
5. **Commit:** Changes with clear message

---

## ⚡ Quick Wins for Backend Team

### Start with Mock Data

Implement endpoints that return mock data first, then add real processing:

```python
@app.get("/api/v1/companies/MSFT")
async def get_company_mock():
    return {
        "company": {"name": "Microsoft Corporation", "ticker": "MSFT", "cik": "0000789019"},
        "filing_date": "2024-07-30",
        "fiscal_year": 2024,
        "ai_insights": {
            "investments": [{
                "amount": "$50M",
                "amount_numeric": 50000000,
                "purpose": "AI infrastructure",
                "timeframe": "FY2024",
                "quote": "We continue to invest...",
                "confidence": "high",
                "source_section": "mda"
            }],
            "products": [],
            "risks": [],
            "timeline": {...},
            "competitive_positioning": {...}
        },
        # ... rest of mock data
    }
```

This lets frontend integrate immediately while you build real processing.

---

## 🐛 Common Issues & Solutions

### Issue: Frontend gets CORS errors

**Solution:** Ensure CORS middleware is configured:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: WebSocket connection fails

**Solution:**
- Check WebSocket endpoint is at `/ws/pipeline/{job_id}` (no `/api/v1` prefix)
- Verify frontend uses `ws://localhost:8000` not `http://`

### Issue: Type mismatches

**Solution:**
- Compare backend response with types in `frontend/src/types/api.ts`
- Ensure nested structure: `company.company.name` not `company.name`

---

## 📞 Support

### For Backend Questions
- Check: `docs/architecture/API_CONTRACT_V2.md`
- Review: Python models in API contract
- Test: Use curl examples provided

### For Frontend Questions
- Check: `docs/architecture/FRONTEND_API_INTEGRATION_GUIDE.md`
- Review: TypeScript types in `types/api.ts`
- Test: Use mock data in frontend

### For Integration Issues
- Compare: Request/response in browser Network tab vs API contract
- Validate: Types match exactly
- Test: With minimal example first

---

## 🎯 Success Criteria

### Backend Complete When:
- [ ] All 11 endpoints return correct data
- [ ] WebSocket sends real-time updates
- [ ] Mock data works (frontend can integrate)
- [ ] Real processing works (Daytona + Browser-Use)
- [ ] Error handling follows error codes in contract
- [ ] CORS configured for localhost:8080

### Frontend Complete When:
- [ ] Can start pipeline and see progress
- [ ] Company cards display correctly
- [ ] Company detail modal works
- [ ] Comparison view functional
- [ ] Export buttons download files
- [ ] Error handling graceful

### Integration Complete When:
- [ ] End-to-end flow works without errors
- [ ] Real-time updates display correctly
- [ ] All 3 PRDs (retrieval, analysis, enrichment) working
- [ ] Demo-ready polish applied

---

## 🚀 Let's Build!

**Backend Team:** Start with `docs/architecture/API_CONTRACT_V2.md`

**Frontend Team:** Review `docs/architecture/FRONTEND_API_INTEGRATION_GUIDE.md`

**Both Teams:** Update your respective `TASKS.md` files as you progress!

**Questions?** Check the docs first, then coordinate via task files and git commits.

---

**Created:** 2025-10-18
**Status:** ✅ Ready for Development
**Next Step:** Backend team implement endpoints, frontend team prepare integration code
