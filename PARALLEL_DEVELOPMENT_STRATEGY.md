# Parallel Development Strategy: Backend + Frontend

**Last Updated:** 2025-10-18
**Status:** Recommended Approach for 12-Hour Hackathon

---

## 🎯 Core Philosophy

**"Build Independently, Integrate Frequently, Pivot Easily"**

- Backend and frontend work in parallel with minimal dependencies
- API contract is a **living document**, not rigid spec
- Integration checkpoints every 2-3 hours
- Easy to pivot based on what works

---

## 📋 Recommended Approach

### Option A: Frontend-First (RECOMMENDED for Hackathon)

**Why:** Fastest path to a working demo, backend fills in gaps

**Timeline:**

**Hour 0-2: Frontend Only**
- Generate UI with Lovable.dev
- Build with mock data
- Perfect the UX/design
- No backend dependency

**Hour 2-4: Backend Starts, Frontend Continues**
- Backend: Build PRD 1 (10-K retrieval)
- Frontend: Polish components, add features
- **No integration yet**

**Hour 4-6: First Integration Point**
- Backend: PRD 1 complete, basic API endpoints
- Frontend: Create API client, test with real data
- **Quick sync:** Does the API match frontend needs?
- **Pivot if needed:** Adjust API or frontend

**Hour 6-9: Parallel Development**
- Backend: PRD 2 (Analysis) + PRD 3 (Enrichment)
- Frontend: Dashboard polish, comparison view
- **Integration:** Connect real-time progress (WebSocket)

**Hour 9-11: Final Integration**
- Backend: Export generation (CSV, PDF)
- Frontend: Export buttons functional
- **Full E2E test:** Click button → download file

**Hour 11-12: Demo Prep**
- Polish UI
- Test full flow
- Record backup video

**Pros:**
- ✅ Working UI from day 1
- ✅ Easy to demo progress
- ✅ Backend knows exactly what to build
- ✅ Less risk of integration mismatches

**Cons:**
- ⚠️ Backend may need to adapt to frontend needs
- ⚠️ API might change during development

---

### Option B: Parallel from Start

**Why:** Maximum parallelization, but needs tight coordination

**Timeline:**

**Hour 0-3: Both Start Simultaneously**
- Backend: PRD 1 (Retrieval)
- Frontend: Lovable.dev + component building
- **Coordination:** Quick API contract draft (30 min collaboration)

**Hour 3-6: Continued Parallel**
- Backend: PRD 2 (Analysis)
- Frontend: Dashboard + detail views
- **Sync at Hour 4.5:** Check API compatibility

**Hour 6-9: Integration Phase**
- Backend: PRD 3 (Enrichment + exports)
- Frontend: Connect real API, replace mocks
- **Continuous testing:** Backend provides `/mock` endpoints

**Hour 9-12: Polish + Demo**
- Both teams: Bug fixes, polish, demo prep

**Pros:**
- ✅ Fastest total time (if coordination is good)
- ✅ Both teams productive from start

**Cons:**
- ⚠️ Requires strong API contract upfront
- ⚠️ Integration issues can cascade
- ⚠️ Harder to pivot

---

## 🔧 Technical Setup

### Workspace Organization

**Backend Developer:**
```bash
# Terminal 1 - Backend Windsurf session
cd /path/to/daytona-browser/backend
# Open Windsurf HERE

# Your context:
# - backend/CLAUDE.md
# - PRPs/backend/*.md
# - BACKEND_TASKS.md
```

**Frontend Developer:**
```bash
# Terminal 2 - Frontend Windsurf session
cd /path/to/daytona-browser/frontend
# Open Windsurf HERE

# Your context:
# - frontend/CLAUDE.md
# - PRPs/frontend/*.md
# - FRONTEND_TASKS.md
```

**Shared Reference:**
- Both read: `docs/architecture/API_CONTRACT.md`
- Update it together as needed (via git commits or shared doc)

---

## 📡 Communication & Coordination

### Integration Checkpoints

**Every 2-3 hours, both teams sync:**

1. **What's working?**
   - Backend: Which endpoints are ready?
   - Frontend: Which features need API?

2. **What's changed?**
   - API shape different than expected?
   - New requirements discovered?

3. **What's next?**
   - Priorities aligned?
   - Any blockers?

**Format:** 5-10 minute quick sync (Slack, in-person, or commit messages)

---

### Git Workflow

**Branches:**
```bash
main           # Stable, working code
backend-dev    # Backend work-in-progress
frontend-dev   # Frontend work-in-progress
```

**Commit Message Convention:**
```
[Backend] feat: Implement SEC navigator for 10-K retrieval
[Frontend] feat: Add company detail modal with tabs
[API Contract] Update endpoint /companies/{ticker} to include enrichment
[Integration] Connect frontend to backend pipeline API
```

**Integration:**
```bash
# Merge to main when both sides are ready
git checkout main
git merge backend-dev
git merge frontend-dev
# Test integration
# If works: continue. If breaks: fix before proceeding.
```

---

## 📝 API Contract Strategy

### Flexible API Contract Approach

**Initial State (Hour 0):**
```markdown
# API_CONTRACT.md

## Status: DRAFT v0.1 - Will Evolve

### Known Endpoints

POST /pipeline/start
- Request: { company_tickers: string[] }
- Response: { job_id: string, status: string }

GET /companies/{ticker}
- Response: TBD (depends on frontend design)

### TBD Sections
- Export endpoints (format TBD)
- WebSocket protocol (may use polling instead)
- Error handling (will define after integration)
```

**After Frontend Design (Hour 2):**
```markdown
## Status: v0.2 - Based on Frontend Needs

GET /companies/{ticker}
- Response: CompanyProfile (full type definition)

# Frontend discovered they need comparison view:
GET /comparison?tickers=MSFT,AAPL
- Response: ComparisonData
```

**After Backend Build (Hour 6):**
```markdown
## Status: v0.9 - Implemented & Tested

# All endpoints implemented
# Types match actual backend models
# Integration tested
```

**Key Principle:**
- API contract **evolves with the project**
- Not a rigid spec written upfront
- Updated via git commits (both teams can modify)

---

## 🔀 Pivot Strategies

### If Backend is Slower Than Expected

**Frontend Strategies:**
1. **Keep using mock data longer** - Polish UI to perfection
2. **Build more features** - Comparison view, filters, search
3. **Improve UX** - Animations, loading states, error handling
4. **Help backend** - Test endpoints manually, report bugs

### If Frontend is Slower Than Expected

**Backend Strategies:**
1. **Build more exports** - Additional CRM formats, Excel export
2. **Improve data quality** - Better LLM prompts, more validation
3. **Add features** - Historical data, caching, performance optimization
4. **Create better mock endpoints** - So frontend can develop when ready

### If Integration is Hard

**Strategies:**
1. **Add adapter layer** - Transform backend response to frontend's expected shape
2. **Use mock API server** - Tools like json-server or MSW
3. **Simplify** - Remove complex features, focus on core flow
4. **Pair up** - Both developers work together on integration

---

## 🚀 Development Commands

### Backend

```bash
# Setup (once)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with API keys

# Development
uvicorn main:app --reload --port 8000

# Testing
pytest tests/ -v
pytest tests/ --cov=src

# Validation
mypy src/
ruff check src/
```

### Frontend

```bash
# Setup (once)
cd frontend
npm install
cp .env.example .env
# Edit .env

# Development
npm run dev  # Runs on http://localhost:3000

# Testing
npm run test
npm run typecheck
npm run lint
```

### Both Running

**Terminal 1 (Backend):**
```bash
cd backend && uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend && npm run dev
```

**Open:** http://localhost:3000 (frontend calls http://localhost:8000/api/v1)

---

## 📊 Progress Tracking

### Task Files

**Backend:** `BACKEND_TASKS.md`
```markdown
# Backend Tasks

**Current:** PRD 1 - 10-K Retrieval
**Status:** Epic 2/5 complete

## PRD 1: 10-K Retrieval
- [x] Epic 1: Setup
- [x] Epic 2: Single company retrieval
- [ ] Epic 3: Daytona integration ← CURRENT
- [ ] Epic 4: Parallelization
- [ ] Epic 5: Testing

**Blockers:** None
**Next:** Implement Daytona environment manager
```

**Frontend:** `FRONTEND_TASKS.md`
```markdown
# Frontend Tasks

**Current:** Dashboard UI
**Status:** Lovable code integrated, building components

## Dashboard UI
- [x] Lovable.dev generation
- [x] Component integration
- [ ] Company card component ← CURRENT
- [ ] Company detail modal
- [ ] Progress tracker

**Blockers:** Waiting for API contract finalization
**Next:** Build MaturityGauge component
```

**Update frequency:** After each epic completion (every 30-60 min)

---

## 🎬 Demo Preparation

### Hour 11: Demo Checklist

**Both Teams:**
- [ ] Full E2E flow works (start pipeline → see results → export)
- [ ] No console errors (backend logs, frontend console)
- [ ] API responds quickly (< 2s for most requests)
- [ ] UI is polished (no broken layouts, good loading states)
- [ ] Data looks realistic (not placeholder text)

**Backup Plan:**
- [ ] Record video of working flow (in case live demo fails)
- [ ] Screenshot key screens
- [ ] Prepare slides explaining architecture

---

## 💡 Pro Tips

### Backend Tips

1. **Start simple** - Get one company working E2E before parallelizing
2. **Mock early** - Provide `/mock` endpoints so frontend can develop
3. **Log everything** - Use structured logging (JSON) for debugging
4. **Test with curl** - Verify endpoints work before frontend integration
5. **Handle errors** - Return proper HTTP status codes and error messages

### Frontend Tips

1. **Mock data first** - Don't wait for backend, use realistic mocks
2. **Build components small** - Easy to swap in real data later
3. **TypeScript strictly** - Catches integration bugs early
4. **Loading states** - Skeletons for every async operation
5. **Test keyboard nav** - Tab through the UI, ensure accessible

### Integration Tips

1. **Test frequently** - Don't wait until hour 11 to connect
2. **Use browser DevTools** - Network tab shows API calls
3. **CORS issues?** - Backend needs to allow `http://localhost:3000`
4. **Type mismatches?** - Use TypeScript to catch them
5. **Performance issues?** - Profile and optimize hot paths

---

## 🛠 Troubleshooting

### "Frontend can't connect to backend"

**Check:**
```bash
# Backend running?
curl http://localhost:8000/health

# CORS configured?
# In backend main.py:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### "API response shape doesn't match frontend types"

**Fix:**
1. Check `API_CONTRACT.md` - is it up to date?
2. Backend: Print actual response: `print(response.dict())`
3. Frontend: Console log response: `console.log(data)`
4. Update types or response to match

### "WebSocket connection keeps failing"

**Fallback:**
```typescript
// Use polling instead
useEffect(() => {
  const interval = setInterval(async () => {
    const status = await api.getPipelineStatus(jobId);
    setProgress(status.progress);
  }, 2000); // Poll every 2 seconds

  return () => clearInterval(interval);
}, [jobId]);
```

---

## 🎯 Success Metrics

**Minimum Success:**
- ✅ Backend retrieves 10-Ks and analyzes them
- ✅ Frontend displays results in dashboard
- ✅ One export format works (CSV or PDF)
- ✅ No major errors during demo

**Strong Success:**
- ✅ All of above
- ✅ Real-time progress updates working
- ✅ Both export formats work
- ✅ UI is polished and responsive
- ✅ Full E2E flow < 10 minutes

**Exceptional Success:**
- ✅ All of above
- ✅ Comparison view functional
- ✅ Excellent error handling
- ✅ Production-ready code quality
- ✅ Video demo recorded as backup

---

## 📅 Recommended Timeline

**Recommended: Option A (Frontend-First)**

| Time | Backend | Frontend | Integration |
|------|---------|----------|-------------|
| 0-2h | Setup, planning | Lovable.dev UI | API contract v0.1 |
| 2-4h | PRD 1 (Retrieval) | Component building | Mock data |
| 4-6h | PRD 2 (Analysis) | Dashboard polish | First integration test |
| 6-8h | PRD 3 (Enrichment) | Detail views | Real-time updates |
| 8-10h | Export generation | Export UI | Full integration |
| 10-11h | Bug fixes | Polish | E2E testing |
| 11-12h | Demo prep | Demo prep | Video recording |

**Sync Points:** Hours 2, 4, 6, 8, 10 (5-10 min quick checks)

---

## ❓ FAQs

**Q: Do we need the API contract upfront?**
A: No! Start with a minimal draft, evolve it as you go. Frontend-first approach means frontend drives the API design.

**Q: What if we want to pivot mid-hackathon?**
A: Easy! Update `API_CONTRACT.md` via git commit, both teams adjust. The contract is flexible by design.

**Q: How do we coordinate without constant meetings?**
A: Use task files (BACKEND_TASKS.md, FRONTEND_TASKS.md) to communicate status. Sync every 2-3 hours for 5-10 minutes.

**Q: What if one team finishes early?**
A: Help the other team! Pair up on integration, testing, or polish. Or build bonus features.

**Q: Should we merge to main frequently?**
A: Merge when integration points work. Don't merge broken code. It's okay to stay on separate branches until hour 8-9.

---

## 🎉 Final Recommendations

**My Strong Recommendation: Option A (Frontend-First)**

**Why:**
1. **Visible progress** - Working UI from hour 2
2. **Clear requirements** - Backend knows exactly what to build
3. **Lower risk** - If backend is slow, at least you have UI to demo
4. **Easier pivots** - Frontend can adjust quickly, backend follows
5. **Better demo** - Polish the UI while backend cooks

**How to Start:**

**Frontend (Hour 0):**
```bash
cd frontend
# Copy LOVABLE_PROMPT.md content
# Paste into Lovable.dev
# Generate project
# Download and integrate
# Start building!
```

**Backend (Hour 0-1):**
```bash
# Read backend/CLAUDE.md
# Read PRPs/backend/10k_retrieval.md
# Set up environment (Python, venv, dependencies)
# Wait for frontend to define API needs (or start with minimal endpoints)
```

**Both (Hour 2):**
```bash
# Quick 10-min sync
# Frontend shows UI mockups
# Backend understands what endpoints to build
# Update API_CONTRACT.md together
# Continue parallel development
```

---

**Good luck! This strategy is designed for maximum flexibility and minimum risk. You can pivot at any checkpoint.** 🚀

---

**Last Updated:** 2025-10-18
**Version:** 1.0.0
