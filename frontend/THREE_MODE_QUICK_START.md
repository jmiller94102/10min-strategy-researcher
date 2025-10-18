# 3-Mode API Configuration - Quick Start Guide

**Status:** ✅ Ready
**Updated:** 2025-10-18

---

## 🎯 Three Development Modes

The frontend now supports **3 modes** for maximum flexibility:

| Mode | When to Use | Backend Required | HTTP Requests |
|------|-------------|------------------|---------------|
| **CLIENT_MOCK** | Early development | ❌ No | ❌ No (simulated) |
| **BACKEND_MOCK** | Integration testing | ✅ Yes (mock endpoints) | ✅ Yes (to `/mock/*`) |
| **REAL** | Production | ✅ Yes (full pipeline) | ✅ Yes (to real endpoints) |

---

## 📝 How to Switch Modes

### Mode 1: CLIENT_MOCK (Current - Default)

**What it does:** Client-side simulation, no backend needed

**.env Configuration:**
```bash
VITE_API_MODE=CLIENT_MOCK
VITE_API_BASE_URL=http://localhost:8000/api/v1  # Not used in this mode
```

**Start Dev Server:**
```bash
npm run dev
```

**Console Output:**
```
🎭 API Client: CLIENT_MOCK mode (client-side simulation)
🎭 WebSocket Client: Mock mode enabled
```

**Use Case:**
- ✅ UI/UX development
- ✅ Component development
- ✅ Learning the codebase
- ✅ Offline development
- ❌ Not for testing HTTP/CORS

**Data Source:** `src/mocks/mockData.ts`

---

### Mode 2: BACKEND_MOCK (Next - Integration Testing)

**What it does:** Real HTTP requests to backend's `/mock/*` endpoints

**Prerequisites:**
- Backend must implement `/mock/*` endpoints (see `BACKEND_MOCK_ENDPOINTS_SPEC.md`)
- Backend server running on `localhost:8000`

**.env Configuration:**
```bash
VITE_API_MODE=BACKEND_MOCK
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
```

**Start Backend:**
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --port 8000
```

**Start Frontend:**
```bash
# Terminal 2: Frontend
cd frontend/anthropic-insight-panel
npm run dev
```

**Console Output:**
```
🧪 API Client: BACKEND_MOCK mode (using /mock/* endpoints)
📡 API Client initialized: Mode: BACKEND_MOCK Base URL: http://localhost:8000/api/v1
```

**API Calls Go To:**
```
GET  http://localhost:8000/api/v1/mock/companies/MSFT
POST http://localhost:8000/api/v1/mock/pipeline/start
GET  http://localhost:8000/api/v1/mock/pipeline/status/abc
```

**Use Case:**
- ✅ Test HTTP requests
- ✅ Test CORS configuration
- ✅ Test request/response serialization
- ✅ Test error handling
- ✅ Realistic latency
- ❌ Not for testing real pipeline

**Data Source:** Backend `/mock/*` endpoints (instant fake data)

---

### Mode 3: REAL (Final - Production)

**What it does:** Real HTTP requests to full backend pipeline

**Prerequisites:**
- Full backend implementation complete
- Daytona integration working
- Anthropic API configured
- Backend server running

**.env Configuration:**
```bash
VITE_API_MODE=REAL
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
```

**Start Backend:**
```bash
# Terminal 1: Backend (full pipeline)
cd backend
uvicorn main:app --reload --port 8000
```

**Start Frontend:**
```bash
# Terminal 2: Frontend
cd frontend/anthropic-insight-panel
npm run dev
```

**Console Output:**
```
🌐 API Client: REAL mode (production endpoints)
📡 API Client initialized: Mode: REAL Base URL: http://localhost:8000/api/v1
```

**API Calls Go To:**
```
GET  http://localhost:8000/api/v1/companies/MSFT  (no /mock prefix!)
POST http://localhost:8000/api/v1/pipeline/start
GET  http://localhost:8000/api/v1/pipeline/status/abc
```

**Use Case:**
- ✅ End-to-end testing
- ✅ Performance testing
- ✅ Real data validation
- ✅ Production deployment
- ⚠️ Requires full backend

**Data Source:** Real 10-K processing pipeline (slow, resource-intensive)

---

## 🔄 Development Workflow

### Week 1: CLIENT_MOCK
```bash
# .env
VITE_API_MODE=CLIENT_MOCK
```

**Team:** Frontend only
**Focus:** Build UI, components, layouts
**Speed:** Instant responses
**Backend:** Not needed

---

### Week 2: BACKEND_MOCK
```bash
# .env
VITE_API_MODE=BACKEND_MOCK
```

**Team:** Both teams in parallel
**Focus:** Integration testing
**Speed:** Fast (instant mock data)
**Backend:** Implements `/mock/*` endpoints (30 min)

**Backend Checklist:**
- [ ] GET `/mock/companies/{ticker}`
- [ ] POST `/mock/pipeline/start`
- [ ] GET `/mock/pipeline/status/{job_id}`
- [ ] GET `/mock/pipeline/results/{job_id}`
- [ ] GET `/mock/companies`
- [ ] GET `/mock/comparison?tickers=...`
- [ ] POST `/mock/export/salesforce`
- [ ] POST `/mock/export/playbooks`
- [ ] GET `/mock/health`

**Test Integration:**
```bash
# Frontend team
curl http://localhost:8000/api/v1/mock/health  # Should work!
```

---

### Week 3: REAL
```bash
# .env
VITE_API_MODE=REAL
```

**Team:** Both teams testing together
**Focus:** End-to-end validation
**Speed:** Realistic (2-7 minutes per company)
**Backend:** Full pipeline implementation

**Test Real Pipeline:**
```bash
# Start pipeline for 3 companies
# Watch real processing via WebSocket
# Validate results against 10-K filings
```

---

## 🧪 Quick Testing Guide

### Test CLIENT_MOCK Mode

```bash
# 1. Set mode
echo "VITE_API_MODE=CLIENT_MOCK" > .env

# 2. Start frontend
npm run dev

# 3. Open browser
open http://localhost:8080

# 4. Check console
# Should see: 🎭 API Client: CLIENT_MOCK mode

# 5. Click "Start Pipeline"
# Should see instant progress simulation
```

---

### Test BACKEND_MOCK Mode

```bash
# 1. Ensure backend /mock/* endpoints are running
curl http://localhost:8000/api/v1/mock/health

# 2. Set mode
echo "VITE_API_MODE=BACKEND_MOCK" > .env
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" >> .env

# 3. Start frontend
npm run dev

# 4. Check console
# Should see: 🧪 API Client: BACKEND_MOCK mode

# 5. Check Network tab
# Should see requests to http://localhost:8000/api/v1/mock/*
```

---

### Test REAL Mode

```bash
# 1. Ensure full backend is running
curl http://localhost:8000/api/v1/health

# 2. Set mode
echo "VITE_API_MODE=REAL" > .env
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" >> .env

# 3. Start frontend
npm run dev

# 4. Check console
# Should see: 🌐 API Client: REAL mode

# 5. Click "Start Pipeline"
# Should see REAL processing (takes several minutes)
```

---

## 🔍 Troubleshooting

### Issue: Still seeing CLIENT_MOCK after changing .env

**Solution:** Restart dev server
```bash
# Stop server (Ctrl+C)
# Restart
npm run dev
```

---

### Issue: CORS errors in BACKEND_MOCK mode

**Solution:** Check backend CORS configuration
```python
# Backend: main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Must match frontend port!
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Issue: 404 errors on `/mock/*` endpoints

**Solution:** Backend hasn't implemented mock endpoints yet
```bash
# Test manually
curl http://localhost:8000/api/v1/mock/health

# If 404, backend team needs to implement (see BACKEND_MOCK_ENDPOINTS_SPEC.md)
```

---

### Issue: Mode not changing

**Solution:** Check `.env` syntax
```bash
# Correct
VITE_API_MODE=BACKEND_MOCK

# Wrong (don't use quotes!)
VITE_API_MODE="BACKEND_MOCK"
```

---

## 📊 Mode Comparison Table

| Feature | CLIENT_MOCK | BACKEND_MOCK | REAL |
|---------|-------------|--------------|------|
| HTTP Requests | ❌ No | ✅ Yes | ✅ Yes |
| CORS Testing | ❌ No | ✅ Yes | ✅ Yes |
| Backend Required | ❌ No | ✅ Yes (mock) | ✅ Yes (full) |
| Response Time | Instant | Instant | Minutes |
| Data Accuracy | Fake | Fake | Real |
| Offline Development | ✅ Yes | ❌ No | ❌ No |
| Network Tab | Empty | Full | Full |
| Demo Ready | ✅ Yes | ✅ Yes | ✅ Yes |
| Production Ready | ❌ No | ❌ No | ✅ Yes |

---

## 🎯 Recommended Path

```
Week 1: CLIENT_MOCK
   ↓
   Frontend builds UI

Week 2: BACKEND_MOCK
   ↓
   Backend implements /mock/* (30 min)
   Frontend tests HTTP integration

Week 3: REAL
   ↓
   Backend implements real pipeline
   End-to-end testing

Production: REAL
   ↓
   Deploy!
```

---

## 📝 Quick Reference

**Change modes:**
```bash
# Edit .env
VITE_API_MODE=CLIENT_MOCK    # or BACKEND_MOCK or REAL
```

**Restart dev server:**
```bash
npm run dev
```

**Check current mode:**
```javascript
// Open browser console
// Look for:
// 🎭 CLIENT_MOCK
// 🧪 BACKEND_MOCK
// 🌐 REAL
```

---

## 🚀 You're Ready!

- ✅ CLIENT_MOCK works today
- ✅ BACKEND_MOCK ready when backend implements `/mock/*`
- ✅ REAL ready when full pipeline complete
- ✅ One line change to switch modes

**Next step:** Wait for backend to implement `/mock/*` endpoints, then test BACKEND_MOCK mode!

---

**Questions?** Check:
- `BACKEND_MOCK_ENDPOINTS_SPEC.md` - Backend implementation guide
- `FRONTEND_INTEGRATION_COMPLETE.md` - Frontend usage guide
- `.env.example` - All configuration options
