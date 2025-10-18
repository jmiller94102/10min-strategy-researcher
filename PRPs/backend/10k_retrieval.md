# Product Requirements Document: 10-K Retrieval Pipeline

**Version:** 1.0.0  
**Date:** October 18, 2025  
**Hackathon Timeline:** 12 hours  
**Primary Vendors:** Browser-Use, Daytona.io

---

## Executive Summary

Build an automated pipeline to retrieve and extract 10-K filings from 10 public companies using Browser-Use for web navigation and Daytona.io for parallel execution environments.

---

## Objectives

### Primary Goals
1. Retrieve 10-K HTML documents from SEC EDGAR for 10 Fortune 500 tech companies
2. Execute retrievals in parallel using Daytona.io isolated environments
3. Extract clean text content for downstream analysis
4. Complete retrieval phase in < 3 minutes for all 10 companies

### Success Metrics
- **Speed:** All 10 companies processed in parallel < 3 minutes
- **Accuracy:** 100% successful retrieval rate
- **Format:** Clean HTML/text output ready for Docling processing

---

## Technical Architecture

### Component 1: Company List Manager
```python
# File: src/company_manager.py

COMPANIES = [
    {"name": "Microsoft", "ticker": "MSFT", "cik": "0000789019"},
    {"name": "Apple", "ticker": "AAPL", "cik": "0000320193"},
    {"name": "NVIDIA", "ticker": "NVDA", "cik": "0001045810"},
    {"name": "Alphabet", "ticker": "GOOGL", "cik": "0001652044"},
    {"name": "Amazon", "ticker": "AMZN", "cik": "0001018724"},
    {"name": "Meta", "ticker": "META", "cik": "0001326801"},
    {"name": "Tesla", "ticker": "TSLA", "cik": "0001318605"},
    {"name": "Salesforce", "ticker": "CRM", "cik": "0001108524"},
    {"name": "Adobe", "ticker": "ADBE", "cik": "0000796343"},
    {"name": "Netflix", "ticker": "NFLX", "cik": "0001065280"}
]
```

**Requirements:**
- Store company metadata (name, ticker, CIK number)
- Validate CIK format (10-digit with leading zeros)
- Export to JSON for pipeline consumption

---

### Component 2: Daytona Environment Manager
```python
# File: src/daytona_manager.py

class DaytonaEnvironmentManager:
    """
    Manages isolated Daytona environments for parallel Browser-Use execution
    """
    
    async def create_environment(self, company_ticker: str) -> DaytonaEnvironment:
        """
        Create isolated environment for single company retrieval
        
        Environment specs:
        - Python 3.11+
        - Browser-Use installed
        - Chromium browser
        - 2GB RAM minimum
        """
        pass
    
    async def create_all_environments(self, companies: list) -> dict:
        """
        Create 10 parallel environments
        Return: {ticker: environment_id}
        """
        pass
    
    async def cleanup_environments(self, env_ids: list):
        """
        Cleanup all environments after completion
        """
        pass
```

**Requirements:**
- Create 10 isolated Daytona workspaces
- Each workspace must have Browser-Use pre-installed
- Include Chromium/Chrome browser capability
- 2-minute timeout per environment creation
- Automatic cleanup on completion or failure

---

### Component 3: SEC EDGAR Navigator (Browser-Use)
```python
# File: src/sec_navigator.py

class SECNavigator:
    """
    Browser-Use agent to navigate SEC EDGAR and retrieve 10-K
    """
    
    async def retrieve_10k(self, company: dict, env: DaytonaEnvironment) -> dict:
        """
        Navigate SEC EDGAR and retrieve latest 10-K
        
        Steps:
        1. Navigate to https://www.sec.gov/cgi-bin/browse-edgar
        2. Search by CIK number
        3. Filter for "10-K" filing type
        4. Select most recent 10-K (2024 or 2023)
        5. Click into filing details
        6. Locate HTML document (usually .htm file)
        7. Download/extract HTML content
        8. Return structured data
        
        Returns:
        {
            'company': company_dict,
            'filing_date': 'YYYY-MM-DD',
            'html_url': 'full_url',
            'html_content': 'raw_html',
            'accession_number': 'xxxx-xx-xxxxxx',
            'retrieved_at': timestamp
        }
        """
        pass
    
    async def navigate_to_edgar(self, agent):
        """Use Browser-Use to navigate to EDGAR search"""
        await agent.navigate("https://www.sec.gov/cgi-bin/browse-edgar")
        
    async def search_by_cik(self, agent, cik: str):
        """Enter CIK and search"""
        await agent.fill("input[name='CIK']", cik)
        await agent.click("input[name='Find']")
        
    async def filter_to_10k(self, agent):
        """Filter results to 10-K only"""
        await agent.select("select[name='type']", "10-K")
        
    async def get_latest_10k_url(self, agent) -> str:
        """Extract URL of most recent 10-K HTML document"""
        # Find first "Documents" button
        # Click into filing
        # Find .htm file (not .pdf)
        # Return full URL
        pass
```

**Requirements:**
- Use Browser-Use Agent class
- Implement robust error handling for missing filings
- Capture full HTML content (not PDF)
- Handle SEC rate limiting (10 requests/second max)
- Add 1-second delay between requests per environment
- Log all navigation steps for debugging

---

### Component 4: Parallel Execution Controller
```python
# File: src/parallel_controller.py

class ParallelRetrievalController:
    """
    Orchestrates parallel 10-K retrieval across Daytona environments
    """
    
    async def run_parallel_retrieval(self, companies: list) -> list:
        """
        Execute 10 parallel retrievals
        
        Process:
        1. Create 10 Daytona environments
        2. Launch Browser-Use agent in each
        3. Execute retrieve_10k() concurrently
        4. Collect all results
        5. Cleanup environments
        
        Returns: List of retrieval results
        """
        
        # Create environments
        env_manager = DaytonaEnvironmentManager()
        environments = await env_manager.create_all_environments(companies)
        
        # Launch parallel retrievals
        tasks = []
        for company in companies:
            env = environments[company['ticker']]
            navigator = SECNavigator()
            task = navigator.retrieve_10k(company, env)
            tasks.append(task)
        
        # Await all
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Cleanup
        await env_manager.cleanup_environments(list(environments.values()))
        
        return results
```

**Requirements:**
- Use Python asyncio for concurrency
- Handle partial failures gracefully
- Return results even if some retrievals fail
- Include retry logic (max 2 retries per company)
- Log progress for each company

---

## Data Structures

### Input Format
```json
{
  "companies": [
    {
      "name": "Microsoft",
      "ticker": "MSFT",
      "cik": "0000789019"
    }
  ]
}
```

### Output Format
```json
{
  "retrieval_metadata": {
    "total_companies": 10,
    "successful": 10,
    "failed": 0,
    "total_time_seconds": 145,
    "retrieved_at": "2025-10-18T10:30:00Z"
  },
  "results": [
    {
      "company": {
        "name": "Microsoft",
        "ticker": "MSFT",
        "cik": "0000789019"
      },
      "filing_date": "2024-07-30",
      "fiscal_year": 2024,
      "html_url": "https://www.sec.gov/Archives/edgar/data/789019/...",
      "html_content": "<!DOCTYPE html>...",
      "accession_number": "0000789019-24-000074",
      "retrieved_at": "2025-10-18T10:28:32Z",
      "retrieval_time_seconds": 12.4,
      "status": "success"
    }
  ]
}
```

---

## Implementation Phases

### Phase 1: Setup (30 minutes)
- [ ] Install Browser-Use in development environment
- [ ] Setup Daytona CLI and authenticate
- [ ] Create base Python project structure
- [ ] Test single Browser-Use navigation to SEC EDGAR
- [ ] Verify Daytona environment creation

### Phase 2: Single Company Retrieval (60 minutes)
- [ ] Implement SECNavigator for one company
- [ ] Test full navigation flow: search → filter → download
- [ ] Extract HTML content successfully
- [ ] Validate HTML structure
- [ ] Handle errors (missing filings, timeouts)

### Phase 3: Daytona Integration (45 minutes)
- [ ] Implement DaytonaEnvironmentManager
- [ ] Test environment creation
- [ ] Deploy Browser-Use script to Daytona environment
- [ ] Execute remote retrieval
- [ ] Verify HTML content retrieval from remote environment

### Phase 4: Parallelization (45 minutes)
- [ ] Implement ParallelRetrievalController
- [ ] Test with 2 companies first
- [ ] Scale to 10 companies
- [ ] Add progress logging
- [ ] Implement cleanup logic

### Phase 5: Testing & Refinement (30 minutes)
- [ ] Run full pipeline end-to-end
- [ ] Measure total execution time
- [ ] Verify all 10 companies successful
- [ ] Test failure scenarios
- [ ] Document any manual steps needed

**Total Estimated Time:** 3.5 hours

---

## Error Handling

### Critical Errors (Stop Execution)
- Daytona authentication failure
- Browser-Use installation failure
- SEC EDGAR site completely down

### Recoverable Errors (Retry)
- Individual company retrieval timeout → Retry 2x
- Browser navigation failure → Retry with fresh browser
- Rate limiting → Wait 5 seconds and retry

### Acceptable Failures (Continue)
- Company has no 10-K filed yet → Mark as "no_filing"
- HTML parsing issues → Save raw content, flag for manual review

---

## Testing Strategy

### Unit Tests
```python
# test_sec_navigator.py
async def test_search_by_cik():
    """Test CIK search returns results"""
    pass

async def test_filter_to_10k():
    """Test 10-K filtering works"""
    pass
```

### Integration Tests
```python
# test_integration.py
async def test_full_retrieval_microsoft():
    """Test complete retrieval for MSFT"""
    result = await retrieve_10k(COMPANIES[0])
    assert result['status'] == 'success'
    assert 'html_content' in result
    assert len(result['html_content']) > 10000  # 10-K should be substantial
```

### Manual Validation
- [ ] Visually inspect 2 retrieved HTML files
- [ ] Verify filing dates are 2023/2024
- [ ] Check HTML contains financial tables
- [ ] Confirm accession numbers are valid

---

## Dependencies

### Python Packages
```
browser-use>=0.1.0
daytona-sdk>=1.0.0
asyncio
aiohttp
beautifulsoup4  # For HTML validation
```

### External Services
- SEC EDGAR (public, no API key needed)
- Daytona.io account with workspace quota for 10+ environments
- Chromium browser binary

---

## Deliverables

1. **Code Repository**
   - `/src/company_manager.py`
   - `/src/daytona_manager.py`
   - `/src/sec_navigator.py`
   - `/src/parallel_controller.py`
   - `/src/main.py` (entry point)
   - `/tests/`

2. **Output Data**
   - `/output/10k_retrieval_results.json`
   - `/output/html_files/MSFT_10k.html` (10 files)

3. **Documentation**
   - `README.md` with setup instructions
   - `DEMO.md` with demo script

---

## Demo Script

```bash
# Terminal output during demo:

$ python src/main.py

🚀 10-K Intelligence Pipeline - Phase 1: Retrieval
═══════════════════════════════════════════════════

📊 Target Companies:
   MSFT, AAPL, NVDA, GOOGL, AMZN, META, TSLA, CRM, ADBE, NFLX

⚙️  Creating 10 Daytona environments... [00:45]
✅ All environments ready

🌐 Launching parallel Browser-Use retrievals...
   ├─ MSFT: Navigating SEC EDGAR... ✓
   ├─ AAPL: Searching CIK 0000320193... ✓
   ├─ NVDA: Filtering to 10-K... ✓
   ├─ GOOGL: Downloading HTML... ✓
   [... progress for all 10 ...]

📥 Retrieval Results:
   ✅ 10/10 successful
   ⏱️  Total time: 2m 34s
   📄 Total content: 4.2MB

💾 Saved to: output/10k_retrieval_results.json
```

---

## Known Limitations

1. **SEC Rate Limiting:** If all 10 hit SEC simultaneously, may get rate limited
   - Mitigation: Built-in delays per environment
   
2. **Daytona Quota:** Free tier may limit concurrent environments
   - Mitigation: Document paid tier requirement

3. **10-K Availability:** Some companies may not have 2024 10-K yet
   - Mitigation: Fall back to 2023 filing

4. **HTML Structure Variance:** SEC HTML format varies by company
   - Mitigation: Save raw HTML for next pipeline stage (Docling)

---

## Future Enhancements (Post-Hackathon)

- PDF fallback if HTML not available
- Automatic CIK lookup from ticker symbol
- Caching to avoid re-downloading same filings
- Support for quarterly 10-Q filings
- Historical filing retrieval (multiple years)

---

## Success Criteria

✅ Pipeline retrieves 10-K for all 10 companies  
✅ Execution completes in < 3 minutes  
✅ HTML content is valid and parseable  
✅ Results saved in structured JSON format  
✅ Demo runs smoothly without manual intervention  

**Sign-off Required:** Technical lead approval before proceeding to PRD 2 (Document Extraction)