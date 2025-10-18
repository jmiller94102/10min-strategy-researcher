# 10-K AI Intelligence Pipeline

**Automated 10-K analysis pipeline using Browser-Use, Daytona.io, and Azure OpenAI**

---

## Overview

This project automatically:
1. ✅ Retrieves 10-K filings from SEC EDGAR for 10 tech companies
2. 🤖 Extracts AI strategy insights using LLMs (investments, products, risks)
3. 🔍 Enriches with real-time data (job postings, news, tech stack)
4. 📊 Exports to Salesforce CRM + generates PDF playbooks for SDRs

**Timeline:** 12-hour hackathon project
**Tech Stack:** FastAPI, Browser-Use, Daytona.io, Azure OpenAI, React

---

## Quick Start

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run server
uvicorn main:app --reload --port 8010
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev  # Runs on http://localhost:3000
```

---

## Environment Variables

**Backend** (`backend/.env`):
- `AZURE_OPENAI_API_KEY` - Your Azure OpenAI key
- `AZURE_OPENAI_ENDPOINT` - Your Azure endpoint
- `AZURE_OPENAI_CHAT_DEPLOYMENT` - gpt-4o deployment
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` - text-embedding-3-small
- `DAYTONA_API_KEY` - Daytona.io API key
- `DAYTONA_API_URL` - https://app.daytona.io/api

**Frontend** (`frontend/.env`):
- `VITE_API_BASE_URL` - Backend API URL (http://localhost:8010/api/v1)
- `VITE_WS_URL` - WebSocket URL (ws://localhost:8010/ws)

---

## Project Structure

```
daytona-browser/
├── backend/                  # FastAPI backend
│   ├── src/                  # Source code
│   ├── tests/                # Tests
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Environment template
│   └── BACKEND_BUILD_PLAN.md # Development plan
├── frontend/                 # React frontend
│   ├── src/                  # Source code
│   ├── .env.example          # Environment template
│   └── CLAUDE.md             # Frontend guide
├── PRPs/                     # Product Requirements
│   ├── backend/              # Backend PRDs
│   └── frontend/             # Frontend PRDs
├── docs/                     # Documentation
│   └── architecture/         # Architecture docs
├── .claude/                  # Claude Code commands
│   └── commands/             # Project commands
└── README.md                 # This file
```

---

## Development Approach

### Parallel Development
- **Backend:** FastAPI server, LLM extraction, data pipeline
- **Frontend:** React dashboard, real-time updates, visualizations

### Key Features
- 🔄 Parallel processing with Daytona.io (10 companies simultaneously)
- 🌐 Browser automation with Browser-Use for web scraping
- 🤖 Semantic analysis with Azure OpenAI (not just keyword matching)
- 📈 AI maturity scoring and benchmarking
- 💼 CRM-ready exports for Salesforce

---

## Target Companies

1. Microsoft (MSFT)
2. Apple (AAPL)
3. NVIDIA (NVDA)
4. Alphabet (GOOGL)
5. Amazon (AMZN)
6. Meta (META)
7. Tesla (TSLA)
8. Salesforce (CRM)
9. Adobe (ADBE)
10. Netflix (NFLX)

---

## Development Timeline

**Total:** ~12 hours

### Backend (9-10 hours)
- Phase 1: SEC Retrieval (1.5h)
- Phase 2: Parallel Execution (2h)
- Phase 3: Section Extraction (1h)
- Phase 4: AI Content Detection (0.5h)
- Phase 5: LLM Extraction (2.5h)
- Phase 6: Maturity Scoring (1.5h)
- Phase 7: Live Enrichment (2h)
- Phase 8: CRM Export (1.5h)

### Frontend (6 hours)
- UI generation with Lovable.dev (2h)
- Component development (2h)
- API integration (1h)
- Polish + testing (1h)

---

## Tech Stack

### Backend
- **Framework:** FastAPI 0.115+
- **Web Automation:** Browser-Use 0.8+
- **Parallel Execution:** Daytona.io SDK 0.111+
- **LLM:** Azure OpenAI (gpt-4o)
- **HTML Parsing:** BeautifulSoup4 4.13+
- **Testing:** pytest 8.3+

### Frontend
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Styling:** TailwindCSS + shadcn/ui
- **State:** React Context / Zustand
- **Real-time:** WebSocket

---

## API Endpoints

### Pipeline
- `POST /api/v1/pipeline/start` - Start pipeline for companies
- `GET /api/v1/pipeline/status/{job_id}` - Check progress
- `GET /api/v1/pipeline/results/{job_id}` - Get results

### Companies
- `GET /api/v1/companies` - List all companies
- `GET /api/v1/companies/{ticker}` - Get company profile

### Exports
- `POST /api/v1/export/salesforce` - Generate Salesforce CSV
- `POST /api/v1/export/pdf` - Generate PDF playbooks

### Real-time
- `WebSocket /ws/pipeline/{job_id}` - Live progress updates

---

## Output Files

```
output/
├── 10k_retrieval_results.json        # Raw 10-K data
├── ai_insights/                       # AI analysis
│   ├── MSFT_insights.json
│   └── consolidated_insights.json
├── enrichment/                        # Live data
│   └── MSFT_enrichment.json
├── crm/                               # CRM exports
│   └── salesforce_accounts_import.csv
└── playbooks/                         # SDR playbooks
    ├── MSFT_playbook.pdf
    └── ALL_COMPANIES_PLAYBOOK.pdf
```

---

## Claude Code Commands

Custom commands for development workflow:

- `/recover-context` - Restore context after /clear
- `/execute-backend-prp` - Execute backend PRDs
- `/execute-frontend-prp` - Execute frontend PRDs

See `.claude/commands/` for all available commands.

---

## Contributing

This is a hackathon project. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

MIT License - See LICENSE file for details

---

## Credits

**Built with:**
- [Browser-Use](https://github.com/browser-use/browser-use) - Web automation
- [Daytona.io](https://daytona.io) - Parallel execution environments
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) - LLM analysis
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [React](https://react.dev/) - Frontend framework

---

**Last Updated:** October 18, 2025
**Status:** Initial setup complete, ready for development
