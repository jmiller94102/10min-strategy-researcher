# Daytona + Chrome CDP Architecture

**Status:** Implemented, Ready for Testing
**Date:** 2025-10-18

---

## Architecture Overview

Browser-Use runs on the **backend** but connects to Chrome instances running **inside Daytona sandboxes** via Chrome DevTools Protocol (CDP) URLs.

```
┌─────────────────────────────────────────────┐
│         Backend (Your Machine)              │
│                                             │
│  ┌───────────────────────────────┐         │
│  │  Job Scraper 1 (MSFT)         │         │
│  │  Browser-Use Agent             │         │
│  │  ├─ Anthropic Claude API      │         │
│  │  └─ CDP: ws://daytona-1:9222/ │─────┐   │
│  └───────────────────────────────┘     │   │
│                                         │   │
│  ┌───────────────────────────────┐     │   │
│  │  Job Scraper 2 (AAPL)         │     │   │
│  │  Browser-Use Agent             │     │   │
│  │  ├─ Anthropic Claude API      │     │   │
│  │  └─ CDP: ws://daytona-2:9222/ │─────┤   │
│  └───────────────────────────────┘     │   │
│                                         │   │
│  ┌───────────────────────────────┐     │   │
│  │  Job Scraper 3 (NVDA)         │     │   │
│  │  Browser-Use Agent             │     │   │
│  │  ├─ Anthropic Claude API      │     │   │
│  │  └─ CDP: ws://daytona-3:9222/ │─────┤   │
│  └───────────────────────────────┘     │   │
└─────────────────────────────────────────┼───┘
                                          │
              ┌───────────────────────────┼────────────────────┐
              │         Daytona Cloud     ▼                    │
              │                                                │
              │  ┌──────────────────────────────────┐         │
              │  │ Sandbox 1 (MSFT)                 │         │
              │  │                                  │         │
              │  │  ┌────────────────────────────┐ │         │
              │  │  │ Chrome (Chromium)          │ │         │
              │  │  │ --remote-debugging-port    │ │         │
              │  │  │   =9222                    │ │         │
              │  │  │ --remote-debugging-address │ │         │
              │  │  │   =0.0.0.0                 │ │         │
              │  │  └────────────────────────────┘ │         │
              │  │  Port 9222 exposed via CDP      │         │
              │  └──────────────────────────────────┘         │
              │                                                │
              │  ┌──────────────────────────────────┐         │
              │  │ Sandbox 2 (AAPL)                 │         │
              │  │  [Same Chrome setup...]          │         │
              │  └──────────────────────────────────┘         │
              │                                                │
              │  ┌──────────────────────────────────┐         │
              │  │ Sandbox 3 (NVDA)                 │         │
              │  │  [Same Chrome setup...]          │         │
              │  └──────────────────────────────────┘         │
              └────────────────────────────────────────────────┘
```

---

## Key Components

### 1. Daytona Sandbox Setup

Each sandbox gets:
- **Ubuntu 22.04** base image
- **Chromium browser** + dependencies
- **Xvfb** (virtual display for headless mode)
- **Chrome running with remote debugging** on port 9222

**Chrome command:**
```bash
chromium-browser \
  --remote-debugging-port=9222 \
  --remote-debugging-address=0.0.0.0 \
  --user-data-dir=/tmp/chrome-debug \
  --no-first-run \
  --no-default-browser-check \
  --disable-dev-shm-usage \
  --no-sandbox \
  --disable-gpu \
  --headless &
```

### 2. CDP URL Generation

Daytona's `sandbox.get_preview_link(9222)` returns:
- **HTTP URL:** `http://sandbox-id.daytona.io:9222/`
- **Token:** For private sandbox access

We convert HTTP to WebSocket:
- `http://` → `ws://`
- `https://` → `wss://`

**Result:** CDP URL like `ws://sandbox-id.daytona.io:9222/`

### 3. Job Scraper Connection

```python
# Create scraper with Daytona CDP URL
scraper = AIJobScraper(
    cdp_url="ws://sandbox-id.daytona.io:9222/"
)

# Browser-Use connects to Daytona Chrome
browser = Browser(cdp_url=cdp_url)

# Scrape jobs
result = await scraper.scrape_ai_jobs(company)
```

---

## Benefits

### ✅ Parallel Execution
- 10 scrapers running simultaneously
- Each with isolated Chrome instance
- 10x faster than sequential

### ✅ Different IPs
- Each Daytona sandbox has unique IP
- Avoids rate limiting from career sites
- Better than all requests from single machine

### ✅ Isolation
- Each company gets own environment
- Crashes don't affect other scrapers
- Clean slate for each scraping session

### ✅ Scalability
- Easy to scale to 20, 50, 100 companies
- Daytona handles resource management
- No local resource constraints

---

## Implementation Details

### Modified Files

#### 1. `daytona_manager.py`

**Changes:**
- `_setup_sandbox_dependencies()` now installs Chrome instead of Python packages
- Starts Chrome with remote debugging
- Added `_get_chrome_cdp_url()` method to get CDP URL via `sandbox.get_preview_link(9222)`
- `create_workspace()` returns `cdp_url` in result dict

**Key Methods:**
```python
async def _setup_sandbox_dependencies(self, sandbox):
    # Install Chrome/Chromium
    # Start Xvfb (virtual display)
    # Start Chrome with --remote-debugging-port=9222
    # Get CDP URL
    return cdp_url

async def _get_chrome_cdp_url(self, sandbox) -> str:
    preview_link = sandbox.get_preview_link(9222)
    ws_url = preview_link.url.replace("http://", "ws://")
    return ws_url
```

#### 2. `job_scraper.py`

**Changes:**
- `__init__()` now accepts `cdp_url` parameter
- Defaults to `"http://localhost:9222/"` for local development
- Logs which CDP URL it's connecting to

**Key Change:**
```python
class AIJobScraper:
    def __init__(self, cdp_url: str = "http://localhost:9222/"):
        self.browser = Browser(cdp_url=cdp_url)
```

---

## Testing

### Test File: `test_daytona_chrome.py`

This test will:
1. ✅ Create Daytona sandbox
2. ✅ Install Chrome in sandbox
3. ✅ Start Chrome with remote debugging
4. ✅ Get CDP URL
5. ✅ Connect Browser-Use to Daytona Chrome
6. ✅ Scrape jobs via Daytona
7. ✅ Cleanup sandbox

**Run test:**
```bash
python test_daytona_chrome.py
```

**Expected output:**
```
✅ Sandbox created: <sandbox-id>
✅ CDP URL: ws://sandbox-id.daytona.io:9222/
✅ Job scraper created
✅ Browser-Use successfully connected to Daytona Chrome!
✅ Job scraping via Daytona working!
```

---

## Usage Pattern

### Local Development (Fast)

```python
# Use local Chrome (already running on :9222)
scraper = AIJobScraper()  # Uses default localhost
result = await scraper.scrape_ai_jobs(company)
```

### Production (Parallel + Isolated)

```python
# Create Daytona sandboxes
manager = DaytonaEnvironmentManager()
sandboxes = await manager.create_all_workspaces(["MSFT", "AAPL", "NVDA"])

# Create scrapers pointing to Daytona Chrome instances
scrapers = []
for ticker, sandbox in sandboxes.items():
    scraper = AIJobScraper(cdp_url=sandbox['cdp_url'])
    scrapers.append((ticker, scraper))

# Run all scrapers in parallel
tasks = [
    scraper.scrape_ai_jobs(companies[ticker])
    for ticker, scraper in scrapers
]
results = await asyncio.gather(*tasks)
```

---

## Environment Variables Required

```bash
# Daytona (for sandbox creation)
DAYTONA_API_KEY=your-daytona-key
DAYTONA_API_URL=https://app.daytona.io/api
DAYTONA_TARGET=us

# Anthropic (for Browser-Use LLM)
ANTHROPIC_API_KEY=sk-ant-your-key
```

---

## Troubleshooting

### Issue: CDP connection fails

**Error:** `Failed to connect to CDP endpoint`

**Possible causes:**
1. Chrome not started in sandbox
2. Port 9222 not exposed
3. Incorrect CDP URL format

**Solution:**
```python
# Check sandbox logs
result = await sandbox.process.exec("ps aux | grep chromium")
print(result.artifacts.stdout)

# Verify port is open
result = await sandbox.process.exec("netstat -tuln | grep 9222")
print(result.artifacts.stdout)

# Test CDP connection
result = await sandbox.process.exec("curl http://localhost:9222/json/version")
print(result.artifacts.stdout)
```

### Issue: Chrome installation fails

**Error:** Package not found or timeout

**Solution:**
- Increase timeout for `apt-get install`
- Check sandbox has internet access
- Try alternate package: `chromium` instead of `chromium-browser`

### Issue: Headless Chrome crashes

**Error:** Chrome exits immediately

**Solution:**
- Verify Xvfb is running
- Check `DISPLAY` environment variable is set
- Increase shared memory: `--disable-dev-shm-usage`
- Check logs: `ps aux | grep Xvfb`

---

## Performance Expectations

| Metric | Local (Sequential) | Daytona (Parallel) |
|--------|-------------------|-------------------|
| 10 companies | ~150 seconds | ~15 seconds |
| Setup time | 0s (Chrome already running) | ~60s per sandbox |
| Per-company scraping | ~15s | ~15s (but parallel) |
| Total time (cold start) | ~150s | ~75s (setup + scrape) |
| Total time (warm start) | ~150s | ~15s |

**Cold start:** First run, need to create sandboxes
**Warm start:** Sandboxes already exist, just scrape

---

## Next Steps

1. ✅ Test with single sandbox: `python test_daytona_chrome.py`
2. ⏳ Test with 3 sandboxes in parallel
3. ⏳ Update enrichment controller to use Daytona CDP URLs
4. ⏳ Test full pipeline with 10 companies
5. ⏳ Add error handling and retry logic
6. ⏳ Implement sandbox pooling (reuse sandboxes)

---

## Future Improvements

### Sandbox Pooling
- Create sandboxes once, reuse many times
- Keep Chrome running between scraping sessions
- Reduce setup time from ~60s to ~0s

### Health Checks
- Ping CDP endpoint before scraping
- Restart Chrome if unresponsive
- Auto-recover from Chrome crashes

### Resource Optimization
- Stop Chrome when not in use
- Set auto-archive interval for inactive sandboxes
- Cleanup old sandboxes automatically

---

**Status:** Ready for testing!
**Last Updated:** 2025-10-18
