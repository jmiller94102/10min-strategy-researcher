# PRPs Directory Organization

**Product Requirements Process (PRP)** documents define systematic implementation plans for features and epics.

---

## Directory Structure

```
PRPs/
├── README.md                  # This file
├── backend/                   # Backend features
│   ├── 10k_retrieval.md       # PRD 1: 10-K retrieval pipeline
│   ├── ai_engine.md           # PRD 2: AI analysis engine
│   └── crm_enrichment.md      # PRD 3: Live enrichment + CRM
├── frontend/                  # Frontend features
│   └── dashboard_ui.md        # Dashboard UI architecture
└── fullstack/                 # Cross-cutting features
    └── (future cross-stack PRPs)
```

---

## What is a PRP?

A **Product Requirements Process** document includes:

1. **Requirements Analysis** - What problem does this solve?
2. **Codebase Research** - What patterns exist? What can we reuse?
3. **Implementation Plan** - Broken into epics and tasks
4. **Validation Gates** - Type checking, tests, coverage targets
5. **Success Criteria** - Clear definition of done

---

## When to Create a PRP

**Create a PRP for:**
- ✅ New features (>1 hour implementation)
- ✅ Major refactorings
- ✅ Significant bug fixes requiring architecture changes
- ✅ Cross-module integrations

**Don't create a PRP for:**
- ❌ Trivial bug fixes (<30 minutes)
- ❌ Documentation updates
- ❌ Minor styling tweaks
- ❌ Simple configuration changes

---

## How to Generate a PRP

### Option 1: Use Command (Recommended)
```bash
/generate-prp.md "feature description"
```

This will:
1. Research existing codebase patterns
2. Analyze requirements
3. Create implementation plan
4. Define validation checkpoints
5. Save to appropriate directory (backend/frontend/fullstack)

### Option 2: Manual Creation

Use the PRP template structure (see example PRPs in this directory).

---

## How to Execute a PRP

```bash
/execute-prp.md PRPs/backend/10k_retrieval.md
```

This will:
1. Read the PRP file
2. Create/update `BACKEND_TASKS.md` or `FRONTEND_TASKS.md`
3. Implement each epic sequentially
4. Run validation after each epic
5. Update task file with results

---

## PRP Lifecycle

1. **Planning Phase** → Generate PRP using `/generate-prp.md`
2. **Review Phase** → Read PRP, ensure it's complete and accurate
3. **Execution Phase** → Execute PRP using `/execute-prp.md`
4. **Validation Phase** → Run validation gates after each epic
5. **Completion Phase** → Mark PRP as complete, archive if needed

---

## Current PRPs

### Backend PRPs

#### 1. 10k_retrieval.md (PRD 1)
**Status:** Ready for execution
**Estimated Time:** 3.5 hours
**Dependencies:** None
**Description:** Automated pipeline to retrieve 10-K filings from SEC EDGAR using Browser-Use and Daytona.io for parallel execution.

**Key Components:**
- Company list manager
- Daytona environment manager
- SEC EDGAR navigator (Browser-Use)
- Parallel execution controller

**Success Criteria:**
- Retrieve 10-Ks for all 10 companies
- Complete in < 3 minutes
- Valid HTML output

---

#### 2. ai_engine.md (PRD 2)
**Status:** Ready for execution (depends on PRD 1)
**Estimated Time:** 3.5 hours
**Dependencies:** PRD 1 (Retrieval)
**Description:** LLM-powered semantic analysis to extract AI strategy intelligence from 10-K filings.

**Key Components:**
- Document section identifier
- AI content detector
- LLM extraction engine (Claude)
- AI maturity scorer
- SDR playbook generator

**Success Criteria:**
- Extract AI investments with 90%+ accuracy
- Generate 5+ actionable insights per company
- Process 10 companies in < 4 minutes

---

#### 3. crm_enrichment.md (PRD 3)
**Status:** Ready for execution (depends on PRD 2)
**Estimated Time:** 3.5 hours
**Dependencies:** PRD 1, PRD 2
**Description:** Live enrichment with job postings and news, plus CRM export generation.

**Key Components:**
- Job posting scraper (Browser-Use)
- News aggregator
- Parallel enrichment controller
- Salesforce CSV generator
- PDF playbook generator

**Success Criteria:**
- Scrape AI jobs for 10/10 companies
- Extract tech stack for 8/10 companies
- Generate valid Salesforce CSV
- Create readable PDF playbooks

---

### Frontend PRPs

#### 1. dashboard_ui.md
**Status:** Ready for execution
**Estimated Time:** 5.5 hours
**Dependencies:** API Contract
**Description:** Intuitive dashboard to visualize AI intelligence, display insights, and enable CRM exports.

**Key Components:**
- Dashboard page with company cards
- Company detail modal
- Progress tracker (real-time WebSocket)
- Comparison table
- Export functionality

**Success Criteria:**
- Pipeline progress visible in real-time
- All company data displayed accurately
- Export generates valid Salesforce CSV
- UI is polished and demo-ready

---

### Fullstack PRPs

_(No fullstack PRPs yet - add here when cross-cutting features are needed)_

---

## Parallel Development Strategy

**Backend and Frontend can work simultaneously!**

### Critical Coordination Point
All parallel development is coordinated through:
**`docs/architecture/API_CONTRACT.md`**

This document defines:
- REST API endpoints
- Data models (TypeScript interfaces)
- Request/response formats
- WebSocket messages
- Error handling

### Backend Team Workflow
1. Open session in `backend/` directory
2. Read `backend/CLAUDE.md`
3. Execute backend PRPs in order (PRD 1 → 2 → 3)
4. Implement API per contract
5. Provide `/mock/*` endpoints for frontend

### Frontend Team Workflow
1. Open session in `frontend/` directory
2. Read `frontend/CLAUDE.md`
3. Execute frontend PRPs
4. Develop against mock API initially
5. Switch to real API once backend ready

---

## Validation Gates

All PRPs must define validation gates:

### Level 1: Type Checking ❌ BLOCKING
Must pass before proceeding.

**Backend:** `mypy src/ --strict`
**Frontend:** `npm run typecheck`

### Level 2: Linting ❌ BLOCKING
Must pass before proceeding.

**Backend:** `ruff check src/` + `black src/`
**Frontend:** `npm run lint`

### Level 3: Unit Tests ❌ BLOCKING
Must pass with coverage targets.

**Backend:** `pytest tests/ --cov=src` (≥70% coverage)
**Frontend:** `npm run test` (≥70% coverage)

### Level 4: Integration Tests ⚠️ STRONGLY RECOMMENDED
Should pass before demo.

### Level 5: E2E Tests ⚠️ RECOMMENDED
Nice to have for production.

---

## Versioning

PRPs are versioned documents:
- **1.0.0** - Initial version
- **1.1.0** - Minor updates (add context, clarify requirements)
- **2.0.0** - Major changes (different approach, new architecture)

---

## Archive Policy

After completion:
- Keep PRP in place (don't delete)
- Add completion date to header
- Move to `PRPs/archive/` if PRP is no longer relevant
- Reference in git commits: `[PRD 1] feat: Implement SEC navigator`

---

## Best Practices

1. **Read Before Execute** - Always read the PRP thoroughly before executing
2. **Update Task Files** - Keep `*_TASKS.md` files updated after each epic
3. **Run Validation** - Don't skip validation gates
4. **Reference in Commits** - Use `[PRD X]` prefix in commit messages
5. **Ask Questions** - If PRP is unclear, ask before implementing

---

## Questions?

- Check `docs/methodology/prp-methodology.md` for detailed methodology
- Read `CLAUDE.md` for project overview
- Use `/recover-context.md` if you lose context

---

**Last Updated:** 2025-10-18
**Total Backend PRPs:** 3
**Total Frontend PRPs:** 1
**Total Fullstack PRPs:** 0
