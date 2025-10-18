# Execute Frontend PRP - 10-K Dashboard UI

## PRP file: $ARGUMENTS

Execute a frontend PRP for the 10-K intelligence dashboard.

---

## Pre-Flight Checklist

- [ ] Read entire PRP file: `cat $ARGUMENTS`
- [ ] Read `frontend/CLAUDE.md` for patterns
- [ ] Lovable.dev code integrated (if applicable)
- [ ] Node.js 18+ installed
- [ ] Dependencies installed (`npm install`)

---

## Execution Process

### Step 1: Load Context (5 min)

```bash
# Read PRP
cat $ARGUMENTS

# Read frontend guide
cat frontend/CLAUDE.md

# Read API contract
cat docs/architecture/API_CONTRACT.md
```

### Step 2: Create Task List

Use TodoWrite tool to create tasks from PRP epics.

### Step 3: Epic-by-Epic Implementation

For each epic in the PRP:

#### A. Plan Epic
- Read epic requirements
- Identify components to build
- List validation criteria

#### B. Implement Epic

**Follow this pattern:**

```typescript
// 1. Define TypeScript types
interface CompanyProfile {
  company: Company;
  ai_maturity: AIMaturityScore;
  // ...
}

// 2. Create custom hook
export function useCompanies(tickers?: string[]) {
  const [data, setData] = useState<CompanyProfile[]>([]);
  const [loading, setLoading] = useState(false);

  // Implementation
  return { data, loading };
}

// 3. Build component
export function CompanyCard({ company }: { company: CompanyProfile }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{company.company.name}</CardTitle>
      </CardHeader>
      {/* ... */}
    </Card>
  );
}

// 4. Write tests
describe('CompanyCard', () => {
  it('renders company name', () => {
    render(<CompanyCard company={mockCompany} />);
    expect(screen.getByText('Microsoft')).toBeInTheDocument();
  });
});
```

#### C. Continuous Validation

After each component:

```bash
# Type checking
npm run typecheck

# Linting
npm run lint

# Tests
npm run test
```

#### D. Epic Validation Gate

**Level 1: Type Checking** ❌ BLOCKING
```bash
npm run typecheck  # tsc --noEmit
# Must pass with 0 errors
```

**Level 2: Linting** ❌ BLOCKING
```bash
npm run lint
npm run lint:fix  # Auto-fix what you can
```

**Level 3: Unit Tests** ❌ BLOCKING
```bash
npm run test
npm run test:coverage
# Coverage: ≥70%
```

**Level 4: Visual Testing** ⚠️ RECOMMENDED
```bash
npm run dev
# Open http://localhost:3000
# Manually test in browser
```

#### E. Update Task List

Mark epic as completed in TodoWrite and FRONTEND_TASKS.md

```bash
git add .
git commit -m "[Frontend] Complete Epic Y: Description

- Implemented components
- Tests: XX% coverage
- Validation: PASSED"
```

---

## Technology-Specific Patterns

### shadcn/ui Components

```bash
# Install components as needed
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
```

### Custom Hooks

```typescript
// hooks/usePipeline.ts
import { useState, useCallback } from 'react';
import { api } from '@/services/api';

export function usePipeline() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<PipelineStatus>('pending');

  const startPipeline = useCallback(async (tickers: string[]) => {
    const response = await api.startPipeline({ company_tickers: tickers });
    setJobId(response.job_id);
    setStatus('in_progress');
  }, []);

  return { jobId, status, startPipeline };
}
```

### API Integration

```typescript
// services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const api = {
  async getCompany(ticker: string): Promise<CompanyProfile> {
    const response = await fetch(`${API_BASE_URL}/companies/${ticker}`);
    if (!response.ok) throw new Error('Failed to fetch company');
    return response.json();
  },

  async startPipeline(request: PipelineStartRequest) {
    const response = await fetch(`${API_BASE_URL}/pipeline/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });
    return response.json();
  },
};
```

### Mock Data (Until Backend Ready)

```typescript
// hooks/useCompanies.ts
const USE_MOCK_DATA = true;  // Toggle this

const MOCK_DATA: CompanyProfile[] = [
  {
    company: { name: 'Microsoft', ticker: 'MSFT' },
    ai_maturity: { total_score: 85, label: 'Leader' },
    // ... more mock data
  },
];

export function useCompanies() {
  if (USE_MOCK_DATA) {
    return { data: MOCK_DATA, loading: false };
  }

  // Real API call
  // ...
}
```

---

## Lovable.dev Integration

If using Lovable.dev generated code:

```bash
# 1. Copy Lovable output to frontend/
cp -r lovable-output/* frontend/

# 2. Install dependencies
cd frontend
npm install

# 3. Verify it works
npm run dev

# 4. Start customizing
# - Replace mock data with API calls
# - Add TypeScript types from API contract
# - Enhance components per PRP requirements
```

---

## Validation Gates

### Level 1: Type Checking ❌ BLOCKING
```bash
npm run typecheck
# TypeScript strict mode must pass
```

### Level 2: Linting ❌ BLOCKING
```bash
npm run lint
npm run lint:fix
```

### Level 3: Unit Tests ❌ BLOCKING
```bash
npm run test
npm run test:coverage
# Coverage: ≥70%
```

### Level 4: Browser Testing ⚠️ RECOMMENDED
- Open in Chrome, Firefox, Safari
- Test responsive design (mobile, tablet, desktop)
- Verify keyboard navigation
- Check accessibility (axe DevTools)

---

## Error Handling

### Type Errors
```bash
npm run typecheck
# Read error messages
# Fix type annotations
# Re-run
```

### Lint Errors
```bash
npm run lint:fix  # Auto-fix
# Manually fix remaining issues
npm run lint  # Verify
```

### Test Failures
```bash
npm run test -- --watch
# Read failure message
# Fix component logic
# Re-run
```

### Runtime Errors
```bash
# Check browser console
# Check Network tab for API calls
# Verify environment variables (.env)
```

---

## Success Criteria

Before marking PRP complete:

- [ ] All type checking passes
- [ ] All linting passes
- [ ] All tests passing (≥70% coverage)
- [ ] Components render correctly
- [ ] Responsive design works
- [ ] Accessibility verified
- [ ] FRONTEND_TASKS.md updated
- [ ] Code committed

---

## Deliverables

- [ ] Working frontend implementation
- [ ] All components built
- [ ] Tests with coverage
- [ ] Responsive design
- [ ] Integration with backend (or mock data)

---

## Frontend-Specific Tips

**Component Design:**
- Keep components small and focused
- Use composition over large monolithic components
- Separate presentational and container components

**State Management:**
- Use React Context for global state
- Keep component state local when possible
- Use custom hooks for reusable logic

**Performance:**
- Use React.memo for expensive components
- Lazy load routes and heavy components
- Optimize images (WebP, lazy loading)

**Accessibility:**
- Semantic HTML (button, nav, main)
- ARIA labels for icons
- Keyboard navigation (Tab, Enter, Escape)
- Color contrast (WCAG AA)

---

**Remember:**
- Validate after each component
- Update task file regularly
- Test in browser frequently
- Commit working code

---

**Last Updated:** 2025-10-18
