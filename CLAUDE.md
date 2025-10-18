# Claude Code Project Guide: 10-K AI Intelligence Pipeline

**Project:** Daytona Browser - AI Intelligence from 10-K Filings
**Version:** 1.0.0
**Last Updated:** 2025-10-18
**Status:** Phase 1 - Initial Setup
**Timeline:** 12-hour Hackathon

---

## Project Overview

**10-K AI Intelligence Pipeline** automates the extraction of AI strategy insights from SEC 10-K filings. The system scrapes filings, analyzes them with LLMs, enriches with live data (jobs, news), and generates CRM-ready outputs for sales teams.

**Core Value:** Turn 500+ pages of dense legal documents into actionable sales intelligence in <10 minutes.

**Tech Stack:**
- **Backend:** Python 3.11+, FastAPI, Browser-Use, Daytona.io SDK, Anthropic Claude API
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, shadcn/ui (Lovable.dev starter)
- **Infrastructure:** Daytona.io (parallel execution environments)

---

## Repository Structure

```
daytona-browser/
├── CLAUDE.md                      # THIS FILE - Root guidance
├── backend/
│   ├── CLAUDE.md                  # Backend-specific guidance
│   ├── src/
│   │   ├── api/                   # FastAPI routes
│   │   ├── services/              # Business logic
│   │   │   ├── retrieval/         # PRD 1: 10-K retrieval
│   │   │   ├── analysis/          # PRD 2: AI analysis
│   │   │   └── enrichment/        # PRD 3: Live enrichment
│   │   ├── models/                # Pydantic models
│   │   └── utils/                 # Utilities
│   ├── tests/
│   ├── requirements.txt
│   └── main.py                    # FastAPI entrypoint
├── frontend/
│   ├── CLAUDE.md                  # Frontend-specific guidance
│   ├── src/
│   │   ├── pages/                 # React pages
│   │   ├── components/            # React components
│   │   ├── hooks/                 # Custom hooks
│   │   ├── services/              # API client
│   │   ├── types/                 # TypeScript types
│   │   └── utils/                 # Utilities
│   ├── tests/
│   ├── package.json
│   └── vite.config.ts
├── .claude/
│   └── commands/
│       ├── generate-prp.md        # Generate new PRP
│       ├── execute-prp.md         # Execute PRP with validation
│       ├── recover-context.md     # Restore context after /clear
│       ├── backend-setup.md       # Backend dev environment setup
│       └── frontend-setup.md      # Frontend dev environment setup
├── PRPs/
│   ├── README.md                  # PRP organization guide
│   ├── backend/
│   │   ├── 10k_retrieval.md       # PRD 1: Retrieval pipeline
│   │   ├── ai_engine.md           # PRD 2: AI analysis
│   │   └── crm_enrichment.md      # PRD 3: Enrichment + CRM
│   ├── frontend/
│   │   └── dashboard_ui.md        # Frontend UI architecture
│   └── fullstack/
│       └── (cross-cutting PRPs)
├── docs/
│   ├── architecture/
│   │   ├── API_CONTRACT.md        # ⭐ CRITICAL: Backend/Frontend interface
│   │   ├── data_flow.md           # System data flow
│   │   └── deployment.md          # Deployment architecture
│   └── methodology/
│       ├── prp-methodology.md     # How to use PRPs
│       ├── quality-standards.md   # Testing & validation
│       ├── sub-agent-patterns.md  # When to use sub-agents
│       └── context-management.md  # Context preservation
├── BACKEND_TASKS.md               # Backend progress tracking
├── FRONTEND_TASKS.md              # Frontend progress tracking
└── template_claude_code.md        # Template reference (remove post-setup)
```

---

## Architecture Overview

### System Components

```
┌─────────────┐
│  Frontend   │
│  (React)    │
└──────┬──────┘
       │ REST API + WebSocket
       │
┌──────▼──────┐
│  Backend    │
│  (FastAPI)  │
└──────┬──────┘
       │
   ┌───┴───┬───────┬──────────┐
   │       │       │          │
   ▼       ▼       ▼          ▼
┌──────┐ ┌───┐ ┌────────┐ ┌─────┐
│ SEC  │ │LLM│ │Browser │ │File │
│EDGAR │ │API│ │  -Use  │ │Store│
└──────┘ └───┘ └────────┘ └─────┘
          │         │
          │    ┌────▼─────┐
          │    │ Daytona  │
          │    │10 Envs   │
          │    └──────────┘
          ▼
    ┌──────────┐
    │Anthropic │
    │  Claude  │
    └──────────┘
```

### Data Flow

```
1. User selects companies in UI
2. Frontend → POST /api/v1/pipeline/start
3. Backend creates pipeline job
4. WebSocket connection established for real-time updates

Pipeline Execution (per company):
5. PRD 1: Browser-Use → Daytona → SEC EDGAR → Retrieve 10-K HTML
6. PRD 2: Parse HTML → Extract AI sections → LLM analysis → Generate insights
7. PRD 3: Browser-Use → Scrape jobs/news → Merge with insights
8. Generate CRM CSV + PDF playbooks
9. Return complete profile to frontend

10. Frontend displays results in dashboard
11. User exports to Salesforce or downloads PDFs
```

---

## Critical Constraints

### DO ✅

**Backend:**
- Use async/await for all I/O operations
- Implement proper error handling (try/except with logging)
- Use Pydantic models for all API requests/responses
- Cache 10-K data to avoid re-scraping (file system or Redis)
- Add request timeouts (30s for scraping, 60s for LLM calls)
- Use structured logging (`logging` module with JSON format)

**Frontend:**
- Use TypeScript strictly (`strict: true` in tsconfig.json)
- Implement loading states for all async operations
- Handle WebSocket reconnection logic
- Use React.memo for expensive components
- Follow API contract types exactly (import from `types/api.ts`)

**Both:**
- Follow the API contract in `docs/architecture/API_CONTRACT.md` religiously
- Update `*_TASKS.md` after completing each epic
- Run validation gates after each major change
- Commit frequently with descriptive messages
- Reference PRPs in commit messages (e.g., "PRD 1: Implement SEC navigator")

### DON'T ❌

**Backend:**
- Don't block async functions with synchronous I/O
- Don't skip input validation (always use Pydantic)
- Don't hardcode secrets (use environment variables)
- Don't let Daytona environments run indefinitely (cleanup!)
- Don't exceed Anthropic rate limits (implement backoff)

**Frontend:**
- Don't fetch data in useEffect without cleanup
- Don't mutate state directly (immutable updates only)
- Don't skip TypeScript errors (fix them, don't `@ts-ignore`)
- Don't hardcode API URLs (use env variables)
- Don't forget WebSocket cleanup on unmount

**Both:**
- Don't start implementation without reading the PRP
- Don't skip validation gates before marking epic complete
- Don't forget to update TASKS.md files
- Don't commit untested code
- Don't create PRPs for trivial changes (use for features only)

---

## Parallel Development Strategy

### Backend and Frontend Can Work Simultaneously

**Critical Coordination Point:** `docs/architecture/API_CONTRACT.md`

#### Backend Development Flow
1. Open Claude Code session in `backend/` directory
2. Read `backend/CLAUDE.md` for backend-specific guidance
3. Follow PRPs in `PRPs/backend/`
4. Update `BACKEND_TASKS.md` after each epic
5. Implement API endpoints per contract
6. Provide `/mock/*` endpoints for frontend development

#### Frontend Development Flow
1. Open separate Claude Code session in `frontend/` directory
2. Read `frontend/CLAUDE.md` for frontend-specific guidance
3. Follow PRPs in `PRPs/frontend/`
4. Update `FRONTEND_TASKS.md` after each epic
5. Develop against mock API endpoints initially
6. Switch to real API once backend is ready

#### Integration Points
- **API Contract:** Update `API_CONTRACT.md` if either side needs changes
- **Types:** Backend generates OpenAPI spec → Frontend imports types
- **Testing:** Backend provides mock data → Frontend uses for component tests
- **Communication:** Use `BACKEND_TASKS.md` and `FRONTEND_TASKS.md` to coordinate

---

## Custom Commands

### /generate-prp.md
Generate a new Product Requirements Process document.

**Usage:** `/generate-prp.md "Add user authentication"`

**What it does:**
1. Researches codebase patterns
2. Analyzes requirements
3. Creates implementation plan with epics
4. Defines validation checkpoints
5. Writes PRP to `PRPs/backend/` or `PRPs/frontend/`

### /execute-prp.md
Execute a PRP with systematic validation.

**Usage:** `/execute-prp.md PRPs/backend/10k_retrieval.md`

**What it does:**
1. Reads PRP file
2. Creates/updates `*_TASKS.md` with epics
3. Implements each epic sequentially
4. Runs validation after each epic
5. Updates task file with results

### /recover-context.md
Restore context after `/clear` or context loss.

**Usage:** `/recover-context.md`

**What it does:**
1. Reads `CLAUDE.md` files (root + module)
2. Reads active `*_TASKS.md` files
3. Checks recent git commits
4. Summarizes current state and next actions

### /backend-setup.md
Setup backend development environment.

**Usage:** `/backend-setup.md`

### /frontend-setup.md
Setup frontend development environment.

**Usage:** `/frontend-setup.md`

---

## Task Tracking Files

### BACKEND_TASKS.md
Tracks backend implementation progress.

**When to update:**
- After completing each epic in backend PRPs
- After running validation gates
- When blocked on a task
- Before switching Claude Code sessions

### FRONTEND_TASKS.md
Tracks frontend implementation progress.

**When to update:**
- After completing each epic in frontend PRPs
- After integrating with backend API
- When blocked on a task
- Before switching Claude Code sessions

### Task File Format
```markdown
# Backend Tasks

**Status:** In Progress
**Last Updated:** 2025-10-18 10:30
**Current Epic:** PRD 1 - SEC Navigator Implementation

---

## Epic 1: 10-K Retrieval Pipeline

**Status:** 🔄 In Progress

### Tasks
- [x] Task 1.1: Create company manager
- [x] Task 1.2: Implement Daytona environment manager
- [ ] Task 1.3: Build SEC navigator ← CURRENT
- [ ] Task 1.4: Test parallel retrieval

### Validation
- [x] mypy type checking passes
- [ ] pytest unit tests pass
- [ ] Integration test with 1 company

### Notes
- Started: 2025-10-18
- Daytona API key configured
- SEC EDGAR navigation tested manually

---

## Backlog
- [ ] Epic 2: AI Analysis Engine
- [ ] Epic 3: Live Enrichment
```

---

## Validation Gates

### Level 1: Type Checking ❌ BLOCKING

**Backend:**
```bash
cd backend
mypy src/ --strict
```

**Frontend:**
```bash
cd frontend
npm run typecheck  # tsc --noEmit
```

**Must pass before proceeding to next epic.**

---

### Level 2: Linting ❌ BLOCKING

**Backend:**
```bash
cd backend
ruff check src/
black src/ --check
```

**Frontend:**
```bash
cd frontend
npm run lint  # eslint
```

**Must pass before proceeding.**

---

### Level 3: Unit Tests ❌ BLOCKING

**Backend:**
```bash
cd backend
pytest tests/ --cov=src --cov-report=term-missing
# Coverage: ≥70% overall, ≥90% critical paths
```

**Frontend:**
```bash
cd frontend
npm run test  # vitest
# Coverage: ≥70%
```

**Must pass before marking epic complete.**

---

### Level 4: Integration Tests ⚠️ STRONGLY RECOMMENDED

**Backend:**
```bash
cd backend
pytest tests/integration/ -v
```

**Frontend:**
```bash
cd frontend
npm run test:integration
```

**Should pass before demo.**

---

### Level 5: E2E Tests ⚠️ RECOMMENDED

```bash
# Full pipeline test
npm run test:e2e  # Playwright
```

**Nice to have for production readiness.**

---

## Sub-Agent Usage

### ✅ EXCELLENT Use Cases

**Backend:**
- Comprehensive testing of retrieval pipeline
- Code review of LLM prompt engineering
- Security audit of API endpoints
- Bulk creation of Pydantic models

**Frontend:**
- Component testing across multiple files
- Accessibility audit
- Performance optimization analysis
- Documentation generation

**Both:**
- Updating all task files simultaneously
- Research and pattern analysis (codebase exploration)
- Repetitive operations (10+ similar changes)

### ❌ AVOID For

- Reading a specific file (use Read tool)
- Single file search (use Grep tool)
- Quick 2-3 file edits
- Trivial changes

### Sub-Agent Invocation Pattern

```markdown
Launch [general-purpose] sub-agent to test all API endpoints:

1. Read API contract from docs/architecture/API_CONTRACT.md
2. Generate pytest tests for each endpoint
3. Test happy path + error cases
4. Run tests and report results
5. Update BACKEND_TASKS.md with test coverage

Return:
- Test files created (paths)
- Coverage percentage
- Any failing tests
- Confidence score (1-10)
```

---

## Context Recovery

### After /clear or Context Loss

**Quick Recovery:**
```bash
/recover-context.md
```

**Manual Recovery:**
```bash
# Read guidance
cat CLAUDE.md
cat backend/CLAUDE.md  # or frontend/CLAUDE.md

# Check progress
cat BACKEND_TASKS.md
cat FRONTEND_TASKS.md

# Review recent work
git log -10 --oneline

# Check current PRPs
ls PRPs/backend/
ls PRPs/frontend/
```

---

## Environment Variables

### Backend (.env)

```bash
# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Daytona
DAYTONA_API_KEY=dyt-...
DAYTONA_WORKSPACE_PREFIX=10k-pipeline

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
ENABLE_CACHING=true
CACHE_DIR=./cache

# CORS
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENVIRONMENT=development
```

---

## Essential Commands

### Backend

```bash
# Setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Development
uvicorn main:app --reload --port 8000

# Testing
pytest tests/ -v
pytest tests/ --cov=src

# Linting
ruff check src/
mypy src/

# Format
black src/
```

### Frontend

```bash
# Setup
cd frontend
npm install

# Development
npm run dev  # Starts Vite dev server on :3000

# Testing
npm run test         # Vitest
npm run test:watch   # Watch mode
npm run test:coverage

# Linting
npm run lint
npm run lint:fix

# Build
npm run build
npm run preview  # Preview production build
```

### Both

```bash
# From root: Start both simultaneously
npm run dev:all  # (if we create a root package.json script)

# Or use separate terminals:
# Terminal 1: cd backend && uvicorn main:app --reload
# Terminal 2: cd frontend && npm run dev
```

---

## Service Management

### When to Restart Backend

✅ **YES, restart:**
- Dependency changes (`requirements.txt`)
- Environment variable changes
- Non-hot-reloadable changes (middleware, CORS config)

❌ **NO restart needed (FastAPI auto-reloads):**
- Route changes
- Business logic changes
- Pydantic model changes

### When to Restart Frontend

✅ **YES, restart:**
- Dependency changes (`package.json`)
- Vite config changes
- Environment variable changes (`.env`)

❌ **NO restart needed (Vite HMR):**
- Component changes
- Style changes
- Most code changes

---

## Documentation

### Essential Reading (Start Here)

1. **API Contract:** `docs/architecture/API_CONTRACT.md` ⭐ READ FIRST
2. **Backend PRDs:**
   - `PRPs/backend/10k_retrieval.md`
   - `PRPs/backend/ai_engine.md`
   - `PRPs/backend/crm_enrichment.md`
3. **Frontend PRD:** `PRPs/frontend/dashboard_ui.md`
4. **Module Guides:**
   - `backend/CLAUDE.md`
   - `frontend/CLAUDE.md`

### Methodology Docs

- `docs/methodology/prp-methodology.md` - How PRPs work
- `docs/methodology/quality-standards.md` - Testing standards
- `docs/methodology/sub-agent-patterns.md` - When to use sub-agents
- `docs/methodology/context-management.md` - Context preservation

### Architecture Docs

- `docs/architecture/API_CONTRACT.md` - Backend/Frontend interface ⭐
- `docs/architecture/data_flow.md` - System data flow
- `docs/architecture/deployment.md` - Deployment strategy

---

## Project Phases

### Phase 1: Setup (Current)
- [x] Project structure created
- [x] Documentation scaffolded
- [ ] Backend environment setup
- [ ] Frontend environment setup
- [ ] API contract finalized

### Phase 2: Backend Development (Hours 0-6)
- [ ] PRD 1: 10-K Retrieval (Browser-Use + Daytona)
- [ ] PRD 2: AI Analysis Engine (LLM extraction)
- [ ] PRD 3: Live Enrichment (Jobs + News scraping)
- [ ] API endpoints implementation
- [ ] Mock endpoints for frontend

### Phase 3: Frontend Development (Hours 0-6, Parallel)
- [ ] Lovable.dev integration
- [ ] Dashboard UI implementation
- [ ] Company detail views
- [ ] Progress tracking
- [ ] Export functionality

### Phase 4: Integration (Hours 6-9)
- [ ] Connect frontend to real backend API
- [ ] End-to-end testing
- [ ] Bug fixes
- [ ] Performance optimization

### Phase 5: Demo Preparation (Hours 9-12)
- [ ] Demo script finalized
- [ ] Practice runs
- [ ] Backup video recording
- [ ] Presentation slides

---

## Hackathon Timeline

### Recommended Schedule

**Hours 0-1:** Setup
- Both teams: Environment setup, read docs

**Hours 1-4:** Core Implementation
- Backend: PRD 1 (Retrieval)
- Frontend: Dashboard UI

**Hours 4-7:** Advanced Features
- Backend: PRD 2 (Analysis) + PRD 3 (Enrichment)
- Frontend: Detail views + Export

**Hours 7-9:** Integration
- Connect real API
- End-to-end testing
- Bug fixes

**Hours 9-11:** Polish
- UI/UX refinement
- Error handling
- Performance optimization

**Hours 11-12:** Demo Prep
- Practice demo
- Record backup video
- Finalize presentation

---

## Git Workflow

### Commit Message Format

```
[MODULE] TYPE: Description

Example:
[Backend] feat: Implement SEC navigator for 10-K retrieval
[Frontend] fix: Resolve WebSocket reconnection issue
[Docs] chore: Update API contract with new endpoints
[PRD 1] test: Add integration tests for retrieval pipeline
```

### Branch Strategy (Hackathon - Simple)

- `main` - stable code
- Work directly on `main` (solo/pair) OR
- `backend-dev` and `frontend-dev` branches (larger team)

### When to Commit

- After completing each epic
- After passing validation gates
- Before switching focus areas
- Before `/clear` (save context)

---

## Troubleshooting

### Backend Issues

**Daytona connection fails:**
```bash
# Check API key
echo $DAYTONA_API_KEY

# Test connection
daytona info

# Re-authenticate
daytona auth login
```

**Anthropic rate limit:**
```python
# Add exponential backoff
import tenacity

@tenacity.retry(
    wait=tenacity.wait_exponential(min=1, max=60),
    stop=tenacity.stop_after_attempt(3)
)
async def call_llm(prompt):
    # LLM call here
```

**SEC rate limiting:**
- Add delays between requests (1 second minimum)
- Use Daytona's different IPs per environment

### Frontend Issues

**TypeScript errors:**
```bash
# Regenerate types from API
npm run generate:types

# Check tsconfig
cat tsconfig.json
```

**WebSocket connection fails:**
- Check backend WebSocket endpoint is running
- Verify URL in `.env` matches backend
- Check browser console for CORS errors

---

## Success Criteria

### Minimum Viable Demo (Must Have)
- ✅ Backend retrieves 10-Ks for 10 companies
- ✅ Backend extracts AI insights with LLM
- ✅ Frontend displays company cards with maturity scores
- ✅ Pipeline progress visible in real-time
- ✅ Salesforce CSV exports successfully

### Strong Demo (Should Have)
- ✅ All of above
- ✅ Live enrichment (jobs/news) working for 8+ companies
- ✅ PDF playbooks generate
- ✅ Comparison view functional
- ✅ Error handling graceful

### Winning Demo (Nice to Have)
- ✅ All of above
- ✅ Sub-10-minute end-to-end execution
- ✅ Polished UI/UX
- ✅ Manual validation of accuracy shown
- ✅ Clear roadmap presented

---

## Questions & Support

### If Things Go Wrong

**Browser-Use issues:**
- Check GitHub issues: https://github.com/browser-use/browser-use
- Community Discord

**Daytona issues:**
- Support: support@daytona.io
- Docs: https://daytona.io/docs

**Anthropic API:**
- Status: status.anthropic.com
- Docs: https://docs.anthropic.com

**Context lost?**
```bash
/recover-context.md
```

---

## Next Steps

### Backend Team
1. Run `/backend-setup.md` command
2. Read `backend/CLAUDE.md`
3. Execute `/execute-prp.md PRPs/backend/10k_retrieval.md`
4. Update `BACKEND_TASKS.md` as you progress

### Frontend Team
1. Run `/frontend-setup.md` command
2. Read `frontend/CLAUDE.md`
3. Execute `/execute-prp.md PRPs/frontend/dashboard_ui.md`
4. Update `FRONTEND_TASKS.md` as you progress

### Both Teams
1. Read `docs/architecture/API_CONTRACT.md` ⭐
2. Coordinate on any API contract changes
3. Update task files regularly
4. Communicate via task files and git commits

---

**Let's build something amazing! 🚀**

**Last Updated:** 2025-10-18
**Version:** 1.0.0
