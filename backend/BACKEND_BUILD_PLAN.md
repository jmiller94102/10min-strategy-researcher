# Backend Build Plan: 10-K AI Intelligence Pipeline

**Consolidated from 3 PRDs - Optimized for Claude Code**
**Total Estimated Time:** 10-11 hours
**Port:** 8010

---

## Project Overview

Build an automated pipeline that:
1. Retrieves 10-K filings from SEC EDGAR for 10 tech companies
2. Extracts AI strategy insights using LLMs (investments, products, risks)
3. Enriches with real-time data (job postings, news)
4. Exports to Salesforce CRM + PDF playbooks

**Tech Stack:** FastAPI, Browser-Use, Daytona.io, Azure OpenAI, BeautifulSoup4

---

## Target Companies (Hardcoded List)

```python
COMPANIES = [
    {"name": "Microsoft", "ticker": "MSFT", "cik": "0000789019", "domain": "microsoft.com"},
    {"name": "Apple", "ticker": "AAPL", "cik": "0000320193", "domain": "apple.com"},
    {"name": "NVIDIA", "ticker": "NVDA", "cik": "0001045810", "domain": "nvidia.com"},
    {"name": "Alphabet", "ticker": "GOOGL", "cik": "0001652044", "domain": "google.com"},
    {"name": "Amazon", "ticker": "AMZN", "cik": "0001018724", "domain": "amazon.com"},
    {"name": "Meta", "ticker": "META", "cik": "0001326801", "domain": "meta.com"},
    {"name": "Tesla", "ticker": "TSLA", "cik": "0001318605", "domain": "tesla.com"},
    {"name": "Salesforce", "ticker": "CRM", "cik": "0001108524", "domain": "salesforce.com"},
    {"name": "Adobe", "ticker": "ADBE", "cik": "0000796343", "domain": "adobe.com"},
    {"name": "Netflix", "ticker": "NFLX", "cik": "0001065280", "domain": "netflix.com"}
]
```

---

## Phase 1: SEC Retrieval - Single Company (1.5 hours)

**Objective:** Retrieve and cache 10-K HTML for one company using Browser-Use

### Components to Build

**1. `src/sec_navigator.py` - SECNavigator class**
- Navigate to https://www.sec.gov/cgi-bin/browse-edgar
- Search by CIK number
- Filter to "10-K" filing type
- Select most recent 10-K (prefer 2024, fallback 2023)
- Extract HTML document URL (not PDF)
- Download full HTML content
- Return structured result with filing date, accession number, HTML content

**2. `src/cache.py` - FileCache class**
- Cache 10-K HTML by ticker (key: "10k:{ticker}")
- 30-day TTL for cache entries
- Store in `./cache/` directory
- Return cached if exists and not expired

### Success Criteria
- [ ] Successfully retrieve Microsoft 10-K HTML
- [ ] HTML content > 50,000 characters
- [ ] Cached result can be retrieved on second call
- [ ] Filing date extracted correctly (format: YYYY-MM-DD)
- [ ] Accession number present

### Validation
```python
# Test with Microsoft first
result = await retrieve_10k(COMPANIES[0])
assert result['status'] == 'success'
assert len(result['html_content']) > 50000
assert result['filing_date'] matches YYYY-MM-DD format
```

---

## Phase 2: Parallel Execution with Daytona (2 hours)

**Objective:** Execute 10 retrievals in parallel across Daytona environments

### Components to Build

**1. `src/daytona_manager.py` - DaytonaEnvironmentManager class**
- Create isolated environment per company
- Spec: Python 3.11+, Browser-Use installed, Chromium browser
- 2GB RAM minimum per environment
- Create 10 environments in parallel
- Cleanup all environments after completion

**2. `src/parallel_controller.py` - ParallelRetrievalController class**
- Orchestrate 10 parallel SEC retrievals
- Use asyncio.gather() for concurrency
- Retry logic: max 2 retries per company with exponential backoff
- Handle partial failures gracefully (return results for successful ones)
- Log progress for each company
- Add 1-second delay per request to respect SEC rate limits

### Success Criteria
- [ ] All 10 companies retrieved successfully
- [ ] Total execution time < 3 minutes
- [ ] No rate limiting errors from SEC
- [ ] Environments cleaned up after completion
- [ ] Results saved to `output/10k_retrieval_results.json`

### Data Contract - Retrieval Output
```python
{
    "retrieval_metadata": {
        "total_companies": 10,
        "successful": 10,
        "failed": 0,
        "total_time_seconds": 145
    },
    "results": [
        {
            "company": {"name": "Microsoft", "ticker": "MSFT", "cik": "..."},
            "filing_date": "2024-07-30",
            "fiscal_year": 2024,
            "html_url": "https://...",
            "html_content": "<!DOCTYPE html>...",
            "accession_number": "...",
            "status": "success"
        }
    ]
}
```

---

## Phase 3: HTML Parsing & Section Extraction (1 hour)

**Objective:** Parse 10-K HTML and extract critical sections

### Components to Build

**1. `src/section_identifier.py` - TenKSectionIdentifier class**
- Identify section boundaries in HTML (Item 1, Item 1A, Item 7)
- Extract clean text from each section
- Remove HTML tags, tables artifacts, page headers/footers
- Preserve paragraph structure for context

**Target Sections:**
- Item 1: Business
- Item 1A: Risk Factors
- Item 7: Management's Discussion and Analysis

### Success Criteria
- [ ] Extract all 3 sections for Microsoft
- [ ] Each section has > 1,000 characters
- [ ] No HTML tags in extracted text
- [ ] Paragraph boundaries preserved

### Data Contract - Section Output
```python
{
    "company": {"ticker": "MSFT"},
    "sections": {
        "business": "Item 1 clean text...",
        "risk_factors": "Item 1A clean text...",
        "mda": "Item 7 clean text..."
    }
}
```

---

## Phase 4: AI Content Detection & Filtering (30 minutes)

**Objective:** Identify AI-relevant paragraphs to reduce LLM context usage

### Components to Build

**1. `src/ai_content_detector.py` - AIContentDetector class**
- Score paragraphs 0-1 on AI relevance
- Keywords: "artificial intelligence", "AI", "machine learning", "ML", "deep learning", "neural network", "generative AI", "GenAI", "copilot", "LLM", "foundation model"
- Filter paragraphs above 0.3 threshold
- Preserve surrounding context (include 1 paragraph before/after)

### Success Criteria
- [ ] Reduce section text by 50-70%
- [ ] All AI-relevant content captured
- [ ] Test: Microsoft Copilot mentions preserved

---

## Phase 5: LLM Extraction Engine (2.5 hours)

**Objective:** Extract structured insights using Azure OpenAI

### Components to Build

**1. `src/llm_extractor.py` - AIInsightExtractor class**

Implement 5 extraction methods:

**a) `extract_ai_investments()` - Investment Extraction**
- Prompt: Extract specific dollar amounts for AI initiatives
- Look for: "invested $X in AI", "allocated $Y for machine learning"
- Return: amount, amount_numeric, purpose, timeframe, quote, confidence
- Use gpt-4o deployment

**b) `extract_ai_products()` - Product Extraction**
- Prompt: Extract AI products, features, services mentioned
- Look for: Product names (Copilot, Firefly), AI features in existing products
- Return: product_name, description, launch_status, target_market, quote

**c) `extract_ai_risks()` - Risk Extraction**
- Prompt: Extract AI-related risks from Risk Factors section
- Categories: competitive, implementation, regulatory, ethical
- Return: category, risk, severity, quote

**d) `extract_ai_timeline()` - Timeline Extraction**
- Prompt: Extract temporal information about AI initiatives
- Return: current_initiatives, near_term_plans, long_term_vision, milestones

**e) `extract_competitive_positioning()` - Competitive Analysis**
- Prompt: How company positions itself vs competitors on AI
- Return: strengths_claimed, competitors_mentioned, differentiation

### Key Implementation Details
- Use Azure OpenAI client with gpt-4o deployment
- Implement rate limiting (max 50 calls/minute)
- Return structured JSON validated with Pydantic models
- Handle malformed responses with retry logic
- Log all LLM calls for debugging

### Success Criteria
- [ ] Extract investments with 90%+ accuracy (manual validation on 3 companies)
- [ ] At least 5 insights per company
- [ ] Process all 10 companies in < 4 minutes
- [ ] All JSON outputs valid

---

## Phase 6: Maturity Scoring & SDR Playbook (1.5 hours)

**Objective:** Calculate AI maturity scores and generate sales intelligence

### Components to Build

**1. `src/ai_maturity_scorer.py` - AIMaturityScorer class**

Calculate 0-100 score with 4 components (25 points each):
- **Investment Score:** Dollar amount invested, % of revenue
- **Product Score:** Number of AI products, market availability
- **Strategic Importance:** Frequency of AI mentions, executive quotes
- **Organizational Readiness:** AI infrastructure, partnerships

Return: total_score, breakdown, percentile (vs other 9 companies), maturity_label (Leader/Fast Follower/Emerging/Laggard)

**2. `src/sdr_playbook_generator.py` - SDRPlaybookGenerator class**

Generate:
- **Discovery Questions (5-7):** Specific questions based on 10-K findings
  - Template: "I saw in your 10-K that you invested {amount} in {area} - how is that progressing?"
- **Value Propositions (3-5):** Aligned to their AI strategy
- **Objection Handlers:** Anticipate objections based on 10-K
- **Executive Summary:** One-page brief with strategy, opportunities, talking points

### Success Criteria
- [ ] Maturity scores range from 40-90 (realistic distribution)
- [ ] Discovery questions include direct 10-K quotes
- [ ] SDR playbooks pass "would I use this?" test

---

## Phase 7: Live Enrichment - Jobs & News (2 hours)

**Objective:** Scrape real-time data using Browser-Use

### Components to Build

**1. `src/job_scraper.py` - AIJobScraper class**
- Navigate to company careers page (try {domain}/careers, fallback Google search)
- Filter jobs for AI keywords: "ai", "machine learning", "ml engineer", "data scientist", "deep learning", "nlp"
- Extract: title, location, job_url, posted_date
- Click into 3-5 job descriptions to extract tech stack
- Tech patterns: Python, TensorFlow, PyTorch, AWS, Azure, GCP, Kubernetes
- Calculate hiring urgency (>10 AI jobs = HIGH)

**2. `src/news_aggregator.py` - AINewsAggregator class**
- Search Google News for "{company} artificial intelligence OR AI"
- Filter: Past 30 days
- Extract first 5 results: headline, source, date, url
- Categorize: product_launch, investment, research, executive

**3. `src/enrichment_controller.py` - ParallelEnrichmentController class**
- Run job scraping + news aggregation in parallel via Daytona
- Merge with AI insights from Phase 6
- Calculate enrichment completeness score (0-1)

### Success Criteria
- [ ] AI jobs found for 8+ companies
- [ ] Tech stack extracted for 8+ companies
- [ ] Recent news found for 8+ companies
- [ ] Complete enrichment in < 3 minutes

### Data Contract - Enrichment Output
```python
{
    "enrichment": {
        "hiring": {
            "total_jobs": 247,
            "ai_jobs": 23,
            "tech_stack": ["Python", "TensorFlow", "Azure ML"],
            "hiring_urgency": "HIGH"
        },
        "recent_news": [
            {
                "headline": "Microsoft announces Copilot for Sales",
                "source": "TechCrunch",
                "date": "2025-09-15",
                "url": "...",
                "category": "product_launch"
            }
        ]
    }
}
```

---

## Phase 8: CRM Export - CSV & PDF (1.5 hours)

**Objective:** Generate Salesforce CSV and PDF playbooks

### Components to Build

**1. `src/crm_generator.py` - SalesforceCRMGenerator class**

Generate CSV with columns:
- Standard: Name, Ticker__c, Website, Industry
- Custom AI fields:
  - AI_Investment__c (currency)
  - AI_Maturity_Score__c (0-100)
  - AI_Products__c (semicolon-separated)
  - AI_Hiring_Count__c (number)
  - AI_Tech_Stack__c (semicolon-separated)
  - AI_Recent_News__c (formatted headlines)
  - SDR_Talking_Points__c (newline-separated)
  - Discovery_Questions__c (newline-separated)
  - Value_Propositions__c (newline-separated)
  - Last_Intelligence_Update__c (date)

Handle:
- CSV special characters (commas, quotes)
- Salesforce field limits (255/1000/32000 chars)
- Proper escaping

**2. `src/playbook_pdf_generator.py` - SDRPlaybookPDFGenerator class**
- Use reportlab for PDF generation
- Create one-page brief per company
- Layout: Company name, AI maturity score, strategy bullets, current signals, discovery questions, value props
- Generate individual PDFs + master PDF with all companies

### Success Criteria
- [ ] Valid CSV generated (10 rows)
- [ ] All fields populated
- [ ] CSV imports to Salesforce without errors (test in sandbox if available)
- [ ] PDFs readable and well-formatted

### Output Files
```
output/
├── 10k_retrieval_results.json
├── ai_insights/
│   ├── MSFT_insights.json (x10)
│   └── consolidated_insights.json
├── enrichment/
│   └── MSFT_enrichment.json (x10)
├── crm/
│   ├── salesforce_accounts_import.csv
│   └── import_instructions.md
└── playbooks/
    ├── MSFT_playbook.pdf (x10)
    └── ALL_COMPANIES_PLAYBOOK.pdf
```

---

## Key Pydantic Models

**Create in `src/models/`**

```python
# company.py
class Company(BaseModel):
    name: str
    ticker: str
    cik: str
    domain: str

# insights.py
class AIInvestment(BaseModel):
    amount: str
    amount_numeric: int
    purpose: str
    timeframe: str
    quote: str
    confidence: Literal["high", "medium", "low"]

class AIProduct(BaseModel):
    product_name: str
    description: str
    launch_status: Literal["available", "beta", "planned"]
    target_market: str
    quote: str

class AIInsights(BaseModel):
    investments: list[AIInvestment]
    products: list[AIProduct]
    risks: list[dict]
    timeline: dict
    competitive_positioning: dict

# maturity.py
class AIMaturityScore(BaseModel):
    total_score: int
    breakdown: dict
    percentile: int
    label: Literal["Leader", "Fast Follower", "Emerging", "Laggard"]

# enrichment.py
class JobPosting(BaseModel):
    title: str
    location: str
    job_url: str
    tech_stack: list[str]
    posted_date: str

class Enrichment(BaseModel):
    hiring: dict
    recent_news: list[dict]
    enriched_at: str
```

---

## FastAPI Endpoints (Optional - for demo)

**Create in `src/api/routes/`**

```python
# GET /companies - List all companies
# GET /companies/{ticker} - Get full profile
# POST /pipeline/start - Trigger full pipeline
# GET /pipeline/status/{job_id} - Check progress
# WebSocket /ws/pipeline/{job_id} - Real-time updates
```

---

## Error Handling Patterns

### Retry Logic
```python
@retry(max_attempts=3, delay=1, backoff=2)
async def scrape_with_retry(func):
    # Exponential backoff for network errors
```

### Graceful Degradation
- If 10-K retrieval fails for 1 company → Continue with other 9
- If job scraping fails → Mark enrichment as partial
- If LLM returns malformed JSON → Retry once, then skip that extraction

### Rate Limiting
- SEC EDGAR: 1 second delay between requests per environment
- Azure OpenAI: 50 calls/minute max (track with deque)
- Career pages: Random 1-3 second delays

---

## Validation Gates Between Phases

**After Phase 1:** Verify one 10-K retrieved successfully
**After Phase 2:** Verify all 10 companies retrieved
**After Phase 3:** Verify sections extracted correctly
**After Phase 5:** Manual spot-check 3 companies' insights
**After Phase 7:** Verify enrichment data quality
**After Phase 8:** Test CSV import in Salesforce

---

## Testing Strategy

### Unit Tests (pytest)
- `test_sec_navigator.py` - Test CIK search, 10-K filtering
- `test_section_identifier.py` - Test HTML parsing
- `test_llm_extractor.py` - Test with known Microsoft data
- `test_job_scraper.py` - Test career page navigation

### Integration Tests
- `test_full_pipeline.py` - End-to-end with 1 company
- `test_parallel_execution.py` - Test Daytona orchestration

### Manual Validation
- Compare extracted investments to known public data
- Review SDR questions for quality
- Check maturity scores against intuition (MSFT, NVDA should be high)

---

## Development Order Recommendations

1. **Start with Microsoft only** - Get Phase 1-6 working for MSFT first
2. **Validate quality** - Manual review before scaling to 10 companies
3. **Add parallelization** - Once single company works, add Daytona
4. **Enrichment last** - Can demo without enrichment if time runs short
5. **PDF is optional** - CSV is critical, PDF is nice-to-have

---

## Critical Dependencies

- **Daytona quota:** Need 10+ concurrent environments
- **Azure OpenAI credits:** ~100 LLM calls total ($5-10 cost)
- **SEC EDGAR:** Public, but respect rate limits
- **Career pages:** Some companies use third-party systems (fallback to Google)

---

## Success Definition

**Minimum Viable:**
- 10 companies' 10-Ks retrieved ✓
- AI investments extracted for 7+ companies ✓
- Salesforce CSV generated ✓

**Strong Demo:**
- All above ✓
- Job postings for 8+ companies ✓
- PDF playbooks generated ✓
- Sub-10-minute end-to-end ✓

**Winning Demo:**
- All above ✓
- 90%+ extraction accuracy ✓
- Polished presentation ✓

---

**Ready to build. Start with Phase 1 after /recover-context.**
