# Frontend Guide: 10-K AI Intelligence Dashboard

**Module:** Frontend (React)
**Tech Stack:** React 18, TypeScript, Vite, TailwindCSS, shadcn/ui
**Last Updated:** 2025-10-18

---

## Quick Start

```bash
# Setup
cd frontend
npm install

# Development server
npm run dev  # Runs on http://localhost:3000

# Testing
npm run test         # Run tests
npm run test:watch   # Watch mode
npm run test:coverage

# Linting
npm run lint
npm run lint:fix

# Type checking
npm run typecheck  # tsc --noEmit

# Build for production
npm run build
npm run preview  # Preview production build
```

---

## Frontend Architecture

### Directory Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Dashboard.tsx          # Main dashboard view
│   │   ├── CompanyDetail.tsx      # Company detail modal/page
│   │   └── Comparison.tsx         # Side-by-side comparison
│   ├── components/
│   │   ├── ui/                    # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── progress.tsx
│   │   │   └── tabs.tsx
│   │   ├── CompanyCard.tsx        # Company summary card
│   │   ├── MaturityGauge.tsx      # AI maturity visualization
│   │   ├── InsightsPanel.tsx      # AI insights display
│   │   ├── EnrichmentPanel.tsx    # Jobs/news display
│   │   ├── PlaybookViewer.tsx     # SDR playbook
│   │   ├── ProgressTracker.tsx    # Pipeline progress modal
│   │   ├── CompanySelector.tsx    # Multi-select picker
│   │   ├── ExportButtons.tsx      # Export functionality
│   │   └── ComparisonTable.tsx    # Comparison table
│   ├── hooks/
│   │   ├── usePipeline.ts         # Pipeline management
│   │   ├── useCompanies.ts        # Company data
│   │   ├── useWebSocket.ts        # Real-time updates
│   │   └── useExport.ts           # Export functionality
│   ├── services/
│   │   ├── api.ts                 # API client
│   │   └── websocket.ts           # WebSocket client
│   ├── types/
│   │   └── api.ts                 # TypeScript types (from API contract)
│   ├── utils/
│   │   ├── formatters.ts          # Data formatters
│   │   └── validators.ts          # Input validators
│   ├── lib/
│   │   └── utils.ts               # Utility functions (cn, etc.)
│   ├── App.tsx                    # Root component
│   └── main.tsx                   # Entry point
├── public/
│   └── assets/
├── tests/
│   ├── unit/
│   │   ├── CompanyCard.test.tsx
│   │   └── MaturityGauge.test.tsx
│   ├── integration/
│   │   └── Dashboard.integration.test.tsx
│   └── setup.ts                   # Test setup
├── .env                           # Environment variables
├── .env.example                   # Environment template
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

---

## Core Technologies

### React Patterns

**Functional Components + Hooks:**
```typescript
// Good ✅
import { useState, useEffect } from 'react';

export function CompanyCard({ company }: { company: CompanyProfile }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div onClick={() => setExpanded(!expanded)}>
      {/* ... */}
    </div>
  );
}

// Bad ❌ (class components)
class CompanyCard extends React.Component {
  // Don't use class components
}
```

**Custom Hooks:**
```typescript
// hooks/useCompanies.ts
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import type { CompanyProfile } from '@/types/api';

export function useCompanies(tickers?: string[]) {
  const [companies, setCompanies] = useState<CompanyProfile[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCompanies = async (tickerList: string[]) => {
    setLoading(true);
    setError(null);
    try {
      const promises = tickerList.map(ticker => api.getCompany(ticker));
      const results = await Promise.all(promises);
      setCompanies(results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch companies');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (tickers && tickers.length > 0) {
      fetchCompanies(tickers);
    }
  }, [tickers]);

  return { companies, loading, error, refetch: fetchCompanies };
}
```

**Component Composition:**
```typescript
// Good ✅ - Composable components
function CompanyDetail({ ticker }: { ticker: string }) {
  const { company, loading } = useCompanies([ticker]);

  if (loading) return <LoadingSkeleton />;
  if (!company) return <ErrorMessage />;

  return (
    <div>
      <CompanyHeader company={company} />
      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="products">Products</TabsTrigger>
        </TabsList>
        <TabsContent value="overview">
          <InsightsPanel insights={company.ai_insights} />
        </TabsContent>
        <TabsContent value="products">
          <ProductsPanel products={company.ai_insights.products} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
```

---

### TypeScript Best Practices

**Strict Type Safety:**
```typescript
// Good ✅
interface CompanyCardProps {
  company: CompanyProfile;
  onClick: (ticker: string) => void;
  className?: string;
}

export function CompanyCard({ company, onClick, className }: CompanyCardProps) {
  // TypeScript knows exact types
  const handleClick = () => onClick(company.company.ticker);

  return <div className={className} onClick={handleClick}>...</div>;
}

// Bad ❌
export function CompanyCard(props: any) {  // Don't use any!
  // ...
}
```

**Type Guards:**
```typescript
// Type guard for API responses
function isCompanyProfile(data: unknown): data is CompanyProfile {
  return (
    typeof data === 'object' &&
    data !== null &&
    'company' in data &&
    'ai_insights' in data
  );
}

// Usage
const response = await fetch('/api/companies/MSFT');
const data = await response.json();

if (isCompanyProfile(data)) {
  // TypeScript knows data is CompanyProfile
  console.log(data.ai_insights.investments);
}
```

**Enums and Unions:**
```typescript
// Use string literal unions
type PipelineStatus = 'started' | 'in_progress' | 'completed' | 'failed';

// Or enums for more structure
enum MaturityLabel {
  Leader = 'Leader',
  FastFollower = 'Fast Follower',
  Emerging = 'Emerging',
  Laggard = 'Laggard'
}
```

---

### State Management

**React Context for Global State:**
```typescript
// context/AppContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react';
import type { CompanyProfile, PipelineJob } from '@/types/api';

interface AppState {
  companies: CompanyProfile[];
  pipelineJob: PipelineJob | null;
  selectedTickers: string[];
}

interface AppContextType extends AppState {
  setCompanies: (companies: CompanyProfile[]) => void;
  setPipelineJob: (job: PipelineJob | null) => void;
  setSelectedTickers: (tickers: string[]) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [companies, setCompanies] = useState<CompanyProfile[]>([]);
  const [pipelineJob, setPipelineJob] = useState<PipelineJob | null>(null);
  const [selectedTickers, setSelectedTickers] = useState<string[]>([]);

  return (
    <AppContext.Provider value={{
      companies,
      pipelineJob,
      selectedTickers,
      setCompanies,
      setPipelineJob,
      setSelectedTickers
    }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
}
```

---

### API Integration

**API Client:**
```typescript
// services/api.ts
import type { CompanyProfile, PipelineStartRequest, PipelineStartResponse } from '@/types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error?.message || 'API request failed');
    }

    return response.json();
  }

  // Pipeline
  async startPipeline(request: PipelineStartRequest): Promise<PipelineStartResponse> {
    return this.request('/pipeline/start', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getPipelineStatus(jobId: string) {
    return this.request(`/pipeline/status/${jobId}`);
  }

  async getPipelineResults(jobId: string) {
    return this.request(`/pipeline/results/${jobId}`);
  }

  // Companies
  async getCompany(ticker: string): Promise<CompanyProfile> {
    return this.request(`/companies/${ticker}`);
  }

  async getAllCompanies() {
    return this.request('/companies');
  }

  // Export
  async exportSalesforce(jobId: string) {
    return this.request('/export/salesforce', {
      method: 'POST',
      body: JSON.stringify({ job_id: jobId }),
    });
  }
}

export const api = new APIClient(API_BASE_URL);
```

**WebSocket Client:**
```typescript
// services/websocket.ts
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

type MessageHandler = (message: WebSocketMessage) => void;

interface WebSocketMessage {
  type: 'progress' | 'complete' | 'error';
  data: any;
}

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private handlers: MessageHandler[] = [];
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  connect(jobId: string) {
    this.ws = new WebSocket(`${WS_URL}/pipeline/${jobId}`);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      const message: WebSocketMessage = JSON.parse(event.data);
      this.handlers.forEach(handler => handler(message));
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket closed');
      this.attemptReconnect(jobId);
    };
  }

  private attemptReconnect(jobId: string) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      console.log(`Reconnecting in ${delay}ms...`);
      setTimeout(() => this.connect(jobId), delay);
    }
  }

  onMessage(handler: MessageHandler) {
    this.handlers.push(handler);
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.handlers = [];
  }
}
```

---

### Hook Examples

**usePipeline Hook:**
```typescript
// hooks/usePipeline.ts
import { useState, useCallback } from 'react';
import { api } from '@/services/api';
import { WebSocketClient } from '@/services/websocket';
import type { PipelineStatus } from '@/types/api';

export function usePipeline() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<PipelineStatus | null>(null);
  const [progress, setProgress] = useState(0);
  const [wsClient] = useState(() => new WebSocketClient());

  const startPipeline = useCallback(async (tickers: string[]) => {
    const response = await api.startPipeline({ company_tickers: tickers });
    setJobId(response.job_id);
    setStatus('started');

    // Connect WebSocket
    wsClient.connect(response.job_id);
    wsClient.onMessage((message) => {
      if (message.type === 'progress') {
        setProgress(message.data.percentage);
      } else if (message.type === 'complete') {
        setStatus('completed');
        wsClient.disconnect();
      }
    });
  }, [wsClient]);

  const cleanup = useCallback(() => {
    wsClient.disconnect();
  }, [wsClient]);

  return {
    jobId,
    status,
    progress,
    startPipeline,
    cleanup
  };
}
```

---

## Styling with TailwindCSS

**Utility Classes:**
```typescript
// Good ✅
<div className="flex flex-col gap-4 p-6 rounded-lg border border-gray-200 shadow-sm">
  <h2 className="text-2xl font-bold text-gray-900">Microsoft (MSFT)</h2>
  <p className="text-sm text-gray-600">AI Maturity: 85/100</p>
</div>

// Component-specific styles with cn() utility
import { cn } from '@/lib/utils';

<div className={cn(
  "rounded-lg border p-4",
  isSelected && "border-blue-500 bg-blue-50",
  isDisabled && "opacity-50 cursor-not-allowed"
)}>
  {/* ... */}
</div>
```

**Custom Theme (tailwind.config.js):**
```javascript
export default {
  theme: {
    extend: {
      colors: {
        maturity: {
          leader: '#10b981',      // Green
          follower: '#3b82f6',    // Blue
          emerging: '#f59e0b',    // Yellow
          laggard: '#ef4444',     // Red
        }
      }
    }
  }
}

// Usage
<span className="text-maturity-leader">Leader</span>
```

---

## Component Examples

### CompanyCard Component

```typescript
// components/CompanyCard.tsx
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { CompanyProfile } from '@/types/api';

interface CompanyCardProps {
  company: CompanyProfile;
  onClick: () => void;
}

export function CompanyCard({ company, onClick }: CompanyCardProps) {
  const { company: companyInfo, ai_maturity, enrichment } = company;

  const getMaturityColor = (score: number) => {
    if (score >= 80) return 'text-maturity-leader';
    if (score >= 60) return 'text-maturity-follower';
    if (score >= 40) return 'text-maturity-emerging';
    return 'text-maturity-laggard';
  };

  return (
    <Card
      className="cursor-pointer hover:shadow-lg transition-shadow"
      onClick={onClick}
    >
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>{companyInfo.name} ({companyInfo.ticker})</span>
          <Badge>{ai_maturity.label}</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-600">AI Maturity:</span>
          <span className={`font-bold ${getMaturityColor(ai_maturity.total_score)}`}>
            {ai_maturity.total_score}/100
          </span>
        </div>

        <div className="grid grid-cols-2 gap-2 text-sm">
          <div>💰 ${(company.ai_insights.investments[0]?.amount_numeric / 1000000)}M</div>
          <div>🚀 {company.ai_insights.products.length} products</div>
          <div>🔥 {enrichment.hiring.ai_jobs} AI jobs</div>
          <div>📰 {enrichment.recent_news.length} news items</div>
        </div>
      </CardContent>
    </Card>
  );
}
```

### MaturityGauge Component

```typescript
// components/MaturityGauge.tsx
import { Progress } from '@/components/ui/progress';

interface MaturityGaugeProps {
  score: number;
  breakdown: {
    investment: number;
    product: number;
    strategic_importance: number;
    organizational_readiness: number;
  };
}

export function MaturityGauge({ score, breakdown }: MaturityGaugeProps) {
  return (
    <div className="space-y-4">
      <div className="text-center">
        <div className="text-5xl font-bold text-gray-900">{score}/100</div>
        <p className="text-sm text-gray-600 mt-1">AI Maturity Score</p>
      </div>

      <div className="space-y-3">
        {Object.entries(breakdown).map(([key, value]) => (
          <div key={key} className="space-y-1">
            <div className="flex justify-between text-sm">
              <span className="capitalize">{key.replace(/_/g, ' ')}</span>
              <span className="font-semibold">{value}/25</span>
            </div>
            <Progress value={(value / 25) * 100} className="h-2" />
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Validation Standards

### Type Checking (Level 1) ❌ BLOCKING

```bash
# Must pass before proceeding
npm run typecheck  # tsc --noEmit

# tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

---

### Linting (Level 2) ❌ BLOCKING

```bash
# ESLint
npm run lint
npm run lint:fix
```

**ESLint Config (.eslintrc.cjs):**
```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  rules: {
    '@typescript-eslint/no-explicit-any': 'error',
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
  }
};
```

---

### Testing (Level 3) ❌ BLOCKING

**Unit Tests (Vitest):**
```typescript
// tests/unit/CompanyCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { CompanyCard } from '@/components/CompanyCard';
import { mockCompanyProfile } from '../fixtures/mockData';

describe('CompanyCard', () => {
  it('renders company name and ticker', () => {
    const onClick = vi.fn();
    render(<CompanyCard company={mockCompanyProfile} onClick={onClick} />);

    expect(screen.getByText(/Microsoft/)).toBeInTheDocument();
    expect(screen.getByText(/MSFT/)).toBeInTheDocument();
  });

  it('displays AI maturity score', () => {
    const onClick = vi.fn();
    render(<CompanyCard company={mockCompanyProfile} onClick={onClick} />);

    expect(screen.getByText('85/100')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const onClick = vi.fn();
    const { container } = render(<CompanyCard company={mockCompanyProfile} onClick={onClick} />);

    fireEvent.click(container.firstChild!);
    expect(onClick).toHaveBeenCalledTimes(1);
  });
});
```

**Integration Tests:**
```typescript
// tests/integration/Dashboard.integration.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { Dashboard } from '@/pages/Dashboard';

const server = setupServer(
  rest.post('/api/v1/pipeline/start', (req, res, ctx) => {
    return res(ctx.json({ job_id: 'test-job-id', status: 'started' }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Dashboard Integration', () => {
  it('starts pipeline and shows progress', async () => {
    render(<Dashboard />);

    // Interact with UI
    fireEvent.click(screen.getByText('Start Pipeline'));

    await waitFor(() => {
      expect(screen.getByText(/Processing/)).toBeInTheDocument();
    });
  });
});
```

---

## Performance Optimization

**React.memo for Expensive Components:**
```typescript
import { memo } from 'react';

export const CompanyCard = memo(function CompanyCard({ company, onClick }: CompanyCardProps) {
  // Component will only re-render if company or onClick changes
  return <div>...</div>;
});
```

**Lazy Loading:**
```typescript
import { lazy, Suspense } from 'react';

const CompanyDetail = lazy(() => import('./pages/CompanyDetail'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <CompanyDetail ticker="MSFT" />
    </Suspense>
  );
}
```

**Virtualized Lists (for large datasets):**
```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function JobsList({ jobs }: { jobs: JobPosting[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: jobs.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 80,
  });

  return (
    <div ref={parentRef} className="h-96 overflow-auto">
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div key={virtualItem.key} style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: `${virtualItem.size}px`,
            transform: `translateY(${virtualItem.start}px)`,
          }}>
            <JobListItem job={jobs[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Lovable.dev Integration

### What Lovable Provides
- Vite + React setup
- TailwindCSS configured
- Basic routing (React Router)
- Component scaffolding

### What to Add
1. **API Integration Layer:**
   - Create `services/api.ts` and `services/websocket.ts`
   - Add environment variables

2. **TypeScript Types:**
   - Import types from `docs/architecture/API_CONTRACT.md`
   - Create `types/api.ts`

3. **Business Components:**
   - Replace Lovable placeholders with real components
   - Add custom hooks for data fetching

4. **State Management:**
   - Add React Context or state library

### Migration Strategy
```bash
# 1. Copy Lovable base code to frontend/
cp -r lovable-output/* frontend/

# 2. Install additional dependencies
npm install @tanstack/react-query zustand date-fns

# 3. Add API types
# Copy types from API_CONTRACT.md to types/api.ts

# 4. Integrate API client
# Create services/api.ts using patterns above

# 5. Replace placeholder components
# Keep layout, replace data with real API calls
```

---

## Environment Variables

### .env.example

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws

# Application
VITE_ENVIRONMENT=development
VITE_APP_NAME="10-K AI Intelligence Dashboard"

# Feature Flags (optional)
VITE_ENABLE_MOCK_DATA=false
VITE_ENABLE_DEBUG=true
```

---

## Accessibility

**Semantic HTML:**
```typescript
// Good ✅
<button onClick={handleClick} aria-label="Start pipeline">
  Start Pipeline
</button>

// Bad ❌
<div onClick={handleClick}>Start Pipeline</div>
```

**Keyboard Navigation:**
```typescript
function CompanyCard({ company, onClick }: CompanyCardProps) {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      onClick();
    }
  };

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyPress={handleKeyPress}
      aria-label={`View details for ${company.company.name}`}
    >
      {/* ... */}
    </div>
  );
}
```

---

## Troubleshooting

### "Module not found" errors
```bash
# Check import paths use @/ alias
# tsconfig.json should have:
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}

# vite.config.ts should have:
import path from "path"
export default {
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}
```

### WebSocket connection fails
- Check backend is running on correct port
- Verify `VITE_WS_URL` in `.env`
- Check browser console for CORS errors

### TypeScript errors in shadcn/ui
```bash
# Regenerate component types
npx shadcn-ui@latest add button --overwrite
```

---

## Demo Checklist

- [ ] All companies display correctly
- [ ] Pipeline progress shows in real-time
- [ ] Company detail modal opens and displays data
- [ ] Comparison view works
- [ ] Export buttons functional
- [ ] Loading states work
- [ ] Error handling graceful
- [ ] Responsive on different screen sizes

---

**Last Updated:** 2025-10-18
**Next Steps:** Execute `/execute-prp.md PRPs/frontend/dashboard_ui.md`
