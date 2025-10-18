# START NOW - Quick Setup Guide

**You're starting the hackathon RIGHT NOW!** ⏱️

This guide gets you from zero to coding in **10 minutes**.

---

## ⚡ 1-Minute Overview

**What You're Building:**
- 🔍 Scrape 10-K filings from SEC
- 🤖 Extract AI insights with LLMs
- 📊 Display in beautiful dashboard
- 💾 Export to Salesforce

**How Long:**
- Backend: ~9 hours (3 PRDs)
- Frontend: ~6 hours (UI + integration)
- **Total: 12-hour hackathon**

**Strategy: Frontend-First**
- Hours 0-2: Generate UI with Lovable.dev
- Hour 2: Define API contract together
- Hours 2-12: Parallel backend + frontend work

---

## 🚀 Quick Setup (10 Minutes)

### Step 1: API Keys (3 min)

**1. Azure OpenAI** (for backend AI analysis)
```bash
# Open backend/.env
cd backend
nano .env  # or use your editor

# Add these lines:
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4  # or your deployment name
```

**Get Azure OpenAI Keys:**
- Portal: https://portal.azure.com
- Create Azure OpenAI resource (or use existing)
- Keys: Resource → Keys and Endpoint

**Alternative: Use OpenAI**
```bash
# If you have OpenAI (not Azure):
OPENAI_API_KEY=sk-...
# Comment out all AZURE_OPENAI_* variables
```

**2. Daytona** (for parallel execution)
```bash
# Still in backend/.env, add:
DAYTONA_API_KEY=your-daytona-key-here
```

**Get Daytona Key:**
- Go to: https://app.daytona.io
- Sign up / Login
- Settings → API Keys → Create New
- Copy key

**3. Browser-Use** (no key needed!)
- Browser-Use runs locally, no API key required

---

### Step 2: Frontend Setup (5 min)

**Generate with Lovable.dev:**

```bash
# 1. Open Lovable.dev in browser
open https://lovable.dev

# 2. Copy the prompt
cat LOVABLE_PROMPT.md | pbcopy  # macOS
# Or manually copy LOVABLE_PROMPT.md contents

# 3. Paste into Lovable.dev project creator

# 4. Wait ~2 minutes for generation

# 5. Download generated code

# 6. Move to frontend directory
# (Unzip download, copy contents to frontend/)
```

**Install Frontend Dependencies:**
```bash
cd frontend
npm install
```

**Start Frontend:**
```bash
npm run dev
# Opens on http://localhost:3000
```

**✅ Frontend running with mock data!**

---

### Step 3: Backend Setup (2 min)

**Install Dependencies:**
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Create requirements.txt:**
```bash
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
browser-use>=0.1.0
daytona-sdk>=1.0.0
openai==1.3.0  # For Azure OpenAI
beautifulsoup4==4.12.2
aiohttp==3.9.0
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
mypy==1.7.0
ruff==0.1.6
black==23.11.0
EOF
```

**Reinstall:**
```bash
pip install -r requirements.txt
```

---

## 📋 Verify Setup

**Frontend Check:**
```bash
cd frontend
npm run dev
# Open http://localhost:3000
# Should see dashboard with mock companies
```

**Backend Check:**
```bash
cd backend
source venv/bin/activate

# Check Python version
python --version  # Should be 3.11+

# Check imports work
python -c "from openai import AsyncAzureOpenAI; print('✅ Azure OpenAI OK')"
python -c "from browser_use import Agent; print('✅ Browser-Use OK')"
python -c "from daytona_sdk import Daytona; print('✅ Daytona OK')"
```

**Environment Variables Check:**
```bash
cd backend
cat .env | grep -v "^#" | grep "="

# Should see:
# AZURE_OPENAI_API_KEY=...
# DAYTONA_API_KEY=...
# etc.
```

---

## 🎯 What to Do Next

### Recommended: Frontend-First Approach

**Hour 0-2: Frontend Development**

```bash
# Terminal/Windsurf Window 1
cd frontend
# Start Windsurf HERE

# Your tasks:
# 1. Integrate Lovable code (done above)
# 2. Build CompanyCard component
# 3. Build MaturityGauge component
# 4. Build CompanyDetail modal
# 5. Polish with mock data
```

**Hour 2: Define API Contract**

```bash
# Quick sync between frontend/backend
# Look at frontend's data needs
# Update docs/architecture/API_CONTRACT.md
# Keep it minimal!
```

**Hour 2-9: Backend Development**

```bash
# Terminal/Windsurf Window 2
cd backend
# Start Windsurf HERE (separate window!)

# Execute PRDs in order:
/execute-backend-prp.md PRPs/backend/10k_retrieval.md
# Then PRD 2 (ai_engine.md)
# Then PRD 3 (crm_enrichment.md)
```

---

## 🔧 Commands Reference

**Frontend Commands:**
```bash
cd frontend
npm run dev          # Start dev server
npm run typecheck    # Type checking
npm run lint         # Linting
npm run test         # Tests
npm run build        # Production build
```

**Backend Commands:**
```bash
cd backend
source venv/bin/activate

# Development
uvicorn main:app --reload --port 8000

# Validation
mypy src/
ruff check src/
pytest tests/ -v

# Type check + lint + test
mypy src/ && ruff check src/ && pytest tests/
```

---

## 📂 Open Two Windsurf Windows

**Window 1 - Frontend:**
```bash
cd /Users/johnney-fivemiller/PythonLearning/hackathons/10-2025-project/daytona-browser/frontend
# Start Windsurf/Claude Code HERE
```

**Window 2 - Backend:**
```bash
cd /Users/johnney-fivemiller/PythonLearning/hackathons/10-2025-project/daytona-browser/backend
# Start Windsurf/Claude Code HERE (separate window)
```

**Why two windows?**
- ✅ Focused context (only relevant files)
- ✅ Faster searches
- ✅ Less token usage
- ✅ Clear separation

---

## 🆘 Quick Troubleshooting

**"pip install failing"**
```bash
# Upgrade pip
pip install --upgrade pip

# Try again
pip install -r requirements.txt
```

**"npm install failing"**
```bash
# Clear cache
npm cache clean --force

# Delete node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

**"Can't find Azure OpenAI"**
```bash
# Check installation
pip show openai

# If missing:
pip install openai==1.3.0
```

**"Browser-Use not working"**
```bash
# Install browser binary
# Browser-Use will auto-download on first use
# Or install Chromium manually:
# brew install chromium  # macOS
```

**"Daytona API not working"**
```bash
# Test API key
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Daytona Key:', os.getenv('DAYTONA_API_KEY')[:10] + '...')
"
```

---

## 📊 Timeline

| Hour | Frontend | Backend |
|------|----------|---------|
| 0-2 | Lovable → UI building | Setup, env config |
| 2 | **SYNC: Define API** | **SYNC: Define API** |
| 2-4 | Components + mock data | PRD 1: Retrieval |
| 4-6 | Dashboard polish | PRD 2: AI Analysis |
| 6-8 | Detail views | PRD 3: Enrichment |
| 8-10 | Integration + exports | Exports + integration |
| 10-11 | Polish + testing | Bug fixes |
| 11-12 | **Demo prep** | **Demo prep** |

**Sync Points:** Hours 2, 4, 6, 8, 10 (quick 5-min checks)

---

## 🎉 You're Ready!

**Checklist:**
- [x] API keys configured (backend/.env)
- [x] Frontend running (http://localhost:3000)
- [x] Backend environment ready
- [x] Two Windsurf windows open
- [x] LOVABLE_PROMPT.md ready to use
- [x] PRPs ready to execute

**Next Step:**
```bash
# Frontend Window:
cd frontend
cat LOVABLE_PROMPT.md
# Copy to Lovable.dev → Generate → Download → Integrate

# Backend Window:
cd backend
source venv/bin/activate
# Wait for frontend to define API needs (Hour 2)
```

---

**START BUILDING! ⚡**

**Questions?**
- Context lost? → `/recover-context.md`
- Backend help? → `cat backend/CLAUDE.md`
- Frontend help? → `cat frontend/CLAUDE.md`
- Strategy? → `cat PARALLEL_DEVELOPMENT_STRATEGY.md`

---

**Last Updated:** 2025-10-18
**Status:** READY TO START! 🚀
