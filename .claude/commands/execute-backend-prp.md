# Execute Backend PRP - 10-K Intelligence Pipeline

## PRP file: $ARGUMENTS

Execute a backend PRP for the 10-K AI intelligence extraction system.

---

## Pre-Flight Checklist

- [ ] Read entire PRP file: `cat $ARGUMENTS`
- [ ] Read `backend/CLAUDE.md` for patterns
- [ ] Verify environment variables set (`.env` file)
- [ ] Check Daytona API key configured
- [ ] Python 3.11+ installed
- [ ] Virtual environment activated

---

## Execution Process

### Step 1: Load Context (5 min)

```bash
# Read PRP
cat $ARGUMENTS

# Read backend guide
cat backend/CLAUDE.md

# Read API contract (if exists)
cat docs/architecture/API_CONTRACT.md
```

### Step 2: Create Task List

Use TodoWrite tool to create tasks from PRP epics.

### Step 3: Epic-by-Epic Implementation

For each epic in the PRP:

#### A. Plan Epic
- Read epic requirements
- Identify validation criteria
- Estimate time

#### B. Implement Epic

**Follow this pattern:**

```python
# 1. Start with Pydantic models
from pydantic import BaseModel

class Company(BaseModel):
    name: str
    ticker: str
    cik: str

# 2. Create service layer
async def retrieve_10k(company: Company):
    # Implementation
    pass

# 3. Add API endpoint
@app.get("/companies/{ticker}")
async def get_company(ticker: str):
    # Implementation
    pass

# 4. Write tests
def test_retrieve_10k():
    # Test implementation
    pass
```

#### C. Continuous Validation

After each major component:

```bash
# Type checking
mypy src/

# Linting
ruff check src/
black src/ --check

# Tests
pytest tests/ -v
```

#### D. Epic Validation Gate

**Level 1: Code Quality** ❌ BLOCKING
```bash
mypy src/  # Must pass
ruff check src/  # Must pass
black src/ --check  # Must pass
```

**Level 2: Testing** ❌ BLOCKING
```bash
pytest tests/ -v  # All tests pass
pytest --cov=src --cov-report=term-missing  # ≥70% coverage
```

**Level 3: Manual Testing** ⚠️ RECOMMENDED
```bash
# Start server
uvicorn main:app --reload

# Test endpoint
curl http://localhost:8000/health
```

#### E. Update Task List

Mark epic as completed in TodoWrite and BACKEND_TASKS.md

```bash
git add .
git commit -m "[PRD X] Complete Epic Y: Description

- Implemented features
- Tests: XX% coverage
- Validation: PASSED"
```

---

## Technology-Specific Patterns

### Browser-Use Integration

```python
from browser_use import Agent

async def scrape_with_browser_use(url: str):
    agent = Agent(task="Navigate and extract")

    await agent.navigate(url)
    await agent.fill("input[name='search']", "value")
    await agent.click("button[type='submit']")

    result = await agent.extract_text(".result")
    return result
```

### Daytona Environment Management

```python
from daytona_sdk import Daytona

async def create_environment(company_ticker: str):
    client = Daytona(api_key=os.getenv("DAYTONA_API_KEY"))

    env = await client.create_workspace(
        name=f"10k-{company_ticker.lower()}",
        image="python:3.11-slim"
    )
    return env
```

### Azure OpenAI Integration

```python
from openai import AsyncAzureOpenAI

client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

async def extract_insights(text: str):
    response = await client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": "Extract AI insights from 10-K"},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content
```

---

## Validation Gates

### Level 1: Type Checking ❌ BLOCKING
```bash
mypy src/ --strict
```

### Level 2: Linting ❌ BLOCKING
```bash
ruff check src/
black src/
```

### Level 3: Unit Tests ❌ BLOCKING
```bash
pytest tests/ --cov=src
# Coverage: ≥70% overall, ≥90% critical paths
```

### Level 4: Integration Tests ⚠️ RECOMMENDED
```bash
# Test with real Daytona environment
pytest tests/integration/ -v
```

---

## Error Handling

### Type Errors
```bash
mypy src/  # Read errors carefully
# Fix type hints, re-run
```

### Test Failures
```bash
pytest -v --tb=long  # See full traceback
# Fix implementation, re-run
```

### Browser-Use Issues
- Check browser binary installed
- Verify network connectivity
- Add delays for slow sites

### Daytona Issues
- Check API key valid
- Verify quota not exceeded
- Check workspace creation logs

---

## Success Criteria

Before marking PRP complete:

- [ ] All type checking passes
- [ ] All linting passes
- [ ] All tests passing
- [ ] Test coverage ≥70%
- [ ] Manual testing successful
- [ ] BACKEND_TASKS.md updated
- [ ] Code committed with good messages

---

## Deliverables

- [ ] Working backend implementation
- [ ] All API endpoints functional
- [ ] Test suite with coverage
- [ ] Documentation updated
- [ ] BACKEND_TASKS.md current

---

**Remember:**
- Validate after each epic
- Update task file regularly
- Commit frequently
- Test integration points early

---

**Last Updated:** 2025-10-18
