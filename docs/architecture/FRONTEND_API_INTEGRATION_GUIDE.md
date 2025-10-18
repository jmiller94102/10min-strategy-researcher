# Frontend API Integration Guide

**Version:** 1.0.0
**Last Updated:** 2025-10-18
**Target Audience:** Frontend developers integrating with the 10-K AI Intelligence Pipeline API

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [API Client Setup](#api-client-setup)
3. [Core Workflows](#core-workflows)
4. [Custom Hooks](#custom-hooks)
5. [WebSocket Integration](#websocket-integration)
6. [Error Handling](#error-handling)
7. [Testing](#testing)
8. [Production Checklist](#production-checklist)

---

## Quick Start

### 1. Install Dependencies

```bash
cd frontend/anthropic-insight-panel
npm install
```

Required dependencies (already in package.json):
- `@tanstack/react-query` - For API data fetching
- `date-fns` - For date formatting
- `zod` - For runtime type validation

### 2. Configure Environment

Create `.env` file:

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENABLE_MOCK_DATA=false  # Set to true for dev without backend
VITE_ENABLE_DEBUG=true
```

### 3. Import Types

```typescript
import type {
  CompanyProfile,
  PipelineStartRequest,
  PipelineStartResponse,
  WebSocketMessage,
} from '@/types/api';
```

---

## API Client Setup

### Create API Client (`services/api.ts`)

```typescript
// src/services/api.ts

import type {
  CompanyProfile,
  PipelineStartRequest,
  PipelineStartResponse,
  PipelineStatusResponse,
  PipelineResultsResponse,
  ComparisonResponse,
  ExportSalesforceRequest,
  ExportSalesforceResponse,
  ExportPlaybooksRequest,
  ExportPlaybooksResponse,
  HealthResponse,
  ErrorResponse,
} from '@/types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

class APIError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = 'APIError';
  }
}

class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      if (!response.ok) {
        const errorData: ErrorResponse = await response.json();
        throw new APIError(
          errorData.error.message,
          errorData.error.code,
          errorData.error.details
        );
      }

      return response.json();
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError(
        'Network request failed',
        'NETWORK_ERROR',
        { originalError: error }
      );
    }
  }

  // ============================================================================
  // PIPELINE ENDPOINTS
  // ============================================================================

  async startPipeline(request: PipelineStartRequest): Promise<PipelineStartResponse> {
    return this.request('/pipeline/start', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getPipelineStatus(jobId: string): Promise<PipelineStatusResponse> {
    return this.request(`/pipeline/status/${jobId}`);
  }

  async getPipelineResults(jobId: string): Promise<PipelineResultsResponse> {
    return this.request(`/pipeline/results/${jobId}`);
  }

  // ============================================================================
  // COMPANY ENDPOINTS
  // ============================================================================

  async getCompany(ticker: string): Promise<CompanyProfile> {
    return this.request(`/companies/${ticker}`);
  }

  async getAllCompanies(): Promise<{ companies: Company[] }> {
    return this.request('/companies');
  }

  async getCompanyInsights(ticker: string): Promise<{
    company: Company;
    ai_insights: AIInsights;
    ai_maturity: AIMaturityScore;
    metadata: { analyzed_at: string };
  }> {
    return this.request(`/companies/${ticker}/insights`);
  }

  async getCompanyEnrichment(ticker: string): Promise<{
    company: Company;
    enrichment: EnrichmentData;
  }> {
    return this.request(`/companies/${ticker}/enrichment`);
  }

  // ============================================================================
  // COMPARISON ENDPOINT
  // ============================================================================

  async compareCompanies(tickers: string[]): Promise<ComparisonResponse> {
    const tickerParam = tickers.join(',');
    return this.request(`/comparison?tickers=${tickerParam}`);
  }

  // ============================================================================
  // EXPORT ENDPOINTS
  // ============================================================================

  async exportSalesforce(request: ExportSalesforceRequest): Promise<ExportSalesforceResponse> {
    return this.request('/export/salesforce', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async exportPlaybooks(request: ExportPlaybooksRequest): Promise<ExportPlaybooksResponse> {
    return this.request('/export/playbooks', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // ============================================================================
  // HEALTH ENDPOINT
  // ============================================================================

  async getHealth(): Promise<HealthResponse> {
    return this.request('/health');
  }
}

export const api = new APIClient(API_BASE_URL);
export { APIError };
```

---

## Core Workflows

### Workflow 1: Start Pipeline and Monitor Progress

```typescript
// Example component using the pipeline

import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import type { PipelineStatusResponse } from '@/types/api';

export function PipelineDemo() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<PipelineStatusResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const startPipeline = async () => {
    setLoading(true);
    try {
      const response = await api.startPipeline({
        company_tickers: ['MSFT', 'AAPL', 'NVDA'],
        skip_enrichment: false,
      });

      setJobId(response.job_id);

      // Start polling status
      pollStatus(response.job_id);
    } catch (error) {
      console.error('Failed to start pipeline:', error);
    } finally {
      setLoading(false);
    }
  };

  const pollStatus = async (jobId: string) => {
    const interval = setInterval(async () => {
      try {
        const statusData = await api.getPipelineStatus(jobId);
        setStatus(statusData);

        if (statusData.status === 'completed' || statusData.status === 'failed') {
          clearInterval(interval);

          if (statusData.status === 'completed') {
            fetchResults(jobId);
          }
        }
      } catch (error) {
        console.error('Failed to fetch status:', error);
        clearInterval(interval);
      }
    }, 2000); // Poll every 2 seconds
  };

  const fetchResults = async (jobId: string) => {
    try {
      const results = await api.getPipelineResults(jobId);
      console.log('Pipeline completed:', results);
      // Handle results (update state, show in UI, etc.)
    } catch (error) {
      console.error('Failed to fetch results:', error);
    }
  };

  return (
    <div>
      <button onClick={startPipeline} disabled={loading}>
        {loading ? 'Starting...' : 'Start Pipeline'}
      </button>

      {status && (
        <div>
          <p>Status: {status.status}</p>
          <p>Progress: {status.progress.percentage}%</p>
          <ul>
            {status.companies.map((company) => (
              <li key={company.ticker}>
                {company.ticker}: {company.status}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

### Workflow 2: Fetch Company Data

```typescript
import { useEffect, useState } from 'react';
import { api } from '@/services/api';
import type { CompanyProfile } from '@/types/api';

export function CompanyViewer({ ticker }: { ticker: string }) {
  const [company, setCompany] = useState<CompanyProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCompany = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await api.getCompany(ticker);
        setCompany(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch company');
      } finally {
        setLoading(false);
      }
    };

    fetchCompany();
  }, [ticker]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!company) return null;

  return (
    <div>
      <h1>{company.company.name} ({company.company.ticker})</h1>
      <p>AI Maturity: {company.ai_maturity.total_score}/100</p>
      <p>Label: {company.ai_maturity.label}</p>

      <h2>Investments</h2>
      <ul>
        {company.ai_insights.investments.map((inv, idx) => (
          <li key={idx}>
            {inv.amount} - {inv.purpose}
          </li>
        ))}
      </ul>

      <h2>Products</h2>
      <ul>
        {company.ai_insights.products.map((product, idx) => (
          <li key={idx}>
            {product.product_name} ({product.launch_status})
          </li>
        ))}
      </ul>

      <h2>Hiring ({company.enrichment.hiring.ai_jobs} AI jobs)</h2>
      <ul>
        {company.enrichment.hiring.ai_job_details.slice(0, 5).map((job, idx) => (
          <li key={idx}>
            {job.title} - {job.location}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Workflow 3: Compare Companies

```typescript
import { useEffect, useState } from 'react';
import { api } from '@/services/api';
import type { ComparisonResponse } from '@/types/api';

export function ComparisonView() {
  const [comparison, setComparison] = useState<ComparisonResponse | null>(null);

  useEffect(() => {
    const fetchComparison = async () => {
      const data = await api.compareCompanies(['MSFT', 'AAPL', 'NVDA']);
      setComparison(data);
    };

    fetchComparison();
  }, []);

  if (!comparison) return <div>Loading...</div>;

  return (
    <table>
      <thead>
        <tr>
          <th>Company</th>
          <th>Maturity Score</th>
          <th>Investment</th>
          <th>AI Jobs</th>
          <th>Products</th>
        </tr>
      </thead>
      <tbody>
        {comparison.companies.map((company) => (
          <tr key={company.ticker}>
            <td>{company.name}</td>
            <td>{company.ai_maturity_score}</td>
            <td>${(company.total_investment / 1000000).toFixed(1)}M</td>
            <td>{company.ai_jobs}</td>
            <td>{company.ai_products_count}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### Workflow 4: Export to Salesforce

```typescript
async function exportToSalesforce(jobId: string) {
  try {
    const response = await api.exportSalesforce({ job_id: jobId });

    // Create download link
    const link = document.createElement('a');
    link.href = `${import.meta.env.VITE_API_BASE_URL}${response.download_url}`;
    link.download = response.filename;
    link.click();

    console.log(`CSV will expire at: ${response.expires_at}`);
  } catch (error) {
    console.error('Export failed:', error);
  }
}
```

---

## Custom Hooks

### Hook 1: `usePipeline`

Complete pipeline management hook with WebSocket support.

```typescript
// src/hooks/usePipeline.ts

import { useState, useEffect, useCallback, useRef } from 'react';
import { api } from '@/services/api';
import type {
  PipelineStatusResponse,
  CompanyProfile,
  WebSocketMessage,
} from '@/types/api';

interface UsePipelineReturn {
  startPipeline: (tickers: string[]) => Promise<void>;
  jobId: string | null;
  status: PipelineStatusResponse | null;
  results: CompanyProfile[];
  progress: number;
  loading: boolean;
  error: string | null;
  reset: () => void;
}

export function usePipeline(): UsePipelineReturn {
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<PipelineStatusResponse | null>(null);
  const [results, setResults] = useState<CompanyProfile[]>([]);
  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const startPipeline = useCallback(async (tickers: string[]) => {
    setLoading(true);
    setError(null);
    setResults([]);
    setProgress(0);

    try {
      const response = await api.startPipeline({
        company_tickers: tickers,
        skip_enrichment: false,
      });

      setJobId(response.job_id);

      // Try WebSocket first, fallback to polling
      connectWebSocket(response.job_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start pipeline');
      setLoading(false);
    }
  }, []);

  const connectWebSocket = useCallback((jobId: string) => {
    const wsUrl = `${import.meta.env.VITE_WS_URL}/pipeline/${jobId}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const message: WebSocketMessage = JSON.parse(event.data);

      if (message.type === 'progress') {
        setProgress(message.data.percentage);
      } else if (message.type === 'complete') {
        setResults((prev) => [...prev, message.data.profile]);
      } else if (message.type === 'error') {
        setError(message.data.error);
      }
    };

    ws.onerror = () => {
      console.warn('WebSocket error, falling back to polling');
      ws.close();
      startPolling(jobId);
    };

    ws.onclose = () => {
      console.log('WebSocket closed');
    };

    wsRef.current = ws;
  }, []);

  const startPolling = useCallback((jobId: string) => {
    const interval = setInterval(async () => {
      try {
        const statusData = await api.getPipelineStatus(jobId);
        setStatus(statusData);
        setProgress(statusData.progress.percentage);

        if (statusData.status === 'completed') {
          clearInterval(interval);
          const resultsData = await api.getPipelineResults(jobId);
          setResults(resultsData.results);
          setLoading(false);
        } else if (statusData.status === 'failed') {
          clearInterval(interval);
          setError('Pipeline failed');
          setLoading(false);
        }
      } catch (err) {
        console.error('Polling error:', err);
      }
    }, 2000);

    pollIntervalRef.current = interval;
  }, []);

  const reset = useCallback(() => {
    setJobId(null);
    setStatus(null);
    setResults([]);
    setProgress(0);
    setLoading(false);
    setError(null);

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  return {
    startPipeline,
    jobId,
    status,
    results,
    progress,
    loading,
    error,
    reset,
  };
}

// Usage:
// const { startPipeline, progress, results, loading, error } = usePipeline();
```

### Hook 2: `useCompanies`

Fetch company data with caching.

```typescript
// src/hooks/useCompanies.ts

import { useQuery } from '@tanstack/react-query';
import { api } from '@/services/api';
import type { CompanyProfile } from '@/types/api';

export function useCompany(ticker: string) {
  return useQuery({
    queryKey: ['company', ticker],
    queryFn: () => api.getCompany(ticker),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
  });
}

export function useCompanies(tickers: string[]) {
  return useQuery({
    queryKey: ['companies', tickers],
    queryFn: async () => {
      const promises = tickers.map((ticker) => api.getCompany(ticker));
      return Promise.all(promises);
    },
    enabled: tickers.length > 0,
    staleTime: 5 * 60 * 1000,
  });
}

// Usage:
// const { data: company, isLoading, error } = useCompany('MSFT');
```

### Hook 3: `useComparison`

Compare multiple companies.

```typescript
// src/hooks/useComparison.ts

import { useQuery } from '@tanstack/react-query';
import { api } from '@/services/api';

export function useComparison(tickers: string[]) {
  return useQuery({
    queryKey: ['comparison', tickers],
    queryFn: () => api.compareCompanies(tickers),
    enabled: tickers.length >= 2,
    staleTime: 5 * 60 * 1000,
  });
}

// Usage:
// const { data: comparison, isLoading } = useComparison(['MSFT', 'AAPL', 'NVDA']);
```

---

## WebSocket Integration

### WebSocket Client

```typescript
// src/services/websocket.ts

import type { WebSocketMessage } from '@/types/api';

type MessageHandler = (message: WebSocketMessage) => void;

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private handlers: Set<MessageHandler> = new Set();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private jobId: string | null = null;

  connect(jobId: string) {
    this.jobId = jobId;
    const wsUrl = `${import.meta.env.VITE_WS_URL}/pipeline/${jobId}`;

    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log(`WebSocket connected for job ${jobId}`);
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        this.handlers.forEach((handler) => handler(message));
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket closed');
      this.attemptReconnect();
    };
  }

  private attemptReconnect() {
    if (
      this.reconnectAttempts < this.maxReconnectAttempts &&
      this.jobId
    ) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

      console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

      setTimeout(() => {
        if (this.jobId) {
          this.connect(this.jobId);
        }
      }, delay);
    }
  }

  onMessage(handler: MessageHandler) {
    this.handlers.add(handler);
    return () => this.handlers.delete(handler); // Return cleanup function
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.handlers.clear();
    this.jobId = null;
    this.reconnectAttempts = 0;
  }

  getReadyState(): number | null {
    return this.ws?.readyState ?? null;
  }
}

// Usage:
// const wsClient = new WebSocketClient();
// wsClient.connect('job-id');
// const unsubscribe = wsClient.onMessage((message) => {
//   console.log('Received:', message);
// });
// // Later: unsubscribe();
```

---

## Error Handling

### Global Error Handler

```typescript
// src/utils/errorHandler.ts

import { APIError } from '@/services/api';
import type { ErrorResponse } from '@/types/api';

export function handleAPIError(error: unknown): string {
  if (error instanceof APIError) {
    switch (error.code) {
      case 'INVALID_TICKER':
        return `Invalid company ticker. Please check the ticker symbol.`;
      case 'JOB_NOT_FOUND':
        return `Pipeline job not found. It may have expired.`;
      case 'RATE_LIMIT_EXCEEDED':
        return `Too many requests. Please wait and try again.`;
      case 'DAYTONA_UNAVAILABLE':
        return `Service temporarily unavailable. Please try again later.`;
      case 'LLM_API_ERROR':
        return `AI analysis service error. Please try again.`;
      case 'PARSING_ERROR':
        return `Failed to process 10-K filing. Please contact support.`;
      default:
        return error.message || 'An unexpected error occurred';
    }
  }

  if (error instanceof Error) {
    return error.message;
  }

  return 'An unknown error occurred';
}
```

### Error Boundary Component

```typescript
// src/components/ErrorBoundary.tsx

import React, { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error boundary caught error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="error-container">
            <h2>Something went wrong</h2>
            <p>{this.state.error?.message}</p>
            <button onClick={() => this.setState({ hasError: false, error: null })}>
              Try again
            </button>
          </div>
        )
      );
    }

    return this.props.children;
  }
}
```

---

## Testing

### Mock API for Tests

```typescript
// src/mocks/handlers.ts

import { rest } from 'msw';
import { mockCompanyProfile } from './mockData';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const handlers = [
  // Start pipeline
  rest.post(`${API_BASE_URL}/pipeline/start`, (req, res, ctx) => {
    return res(
      ctx.status(202),
      ctx.json({
        job_id: 'test-job-id-123',
        status: 'started',
        total_companies: 3,
        estimated_time_seconds: 420,
        started_at: new Date().toISOString(),
      })
    );
  }),

  // Get pipeline status
  rest.get(`${API_BASE_URL}/pipeline/status/:jobId`, (req, res, ctx) => {
    return res(
      ctx.json({
        job_id: req.params.jobId,
        status: 'completed',
        progress: {
          current_stage: 'finalization',
          companies_processed: 3,
          companies_total: 3,
          percentage: 100,
        },
        companies: [
          {
            ticker: 'MSFT',
            status: 'completed',
            stage: 'finalization',
          },
        ],
        started_at: new Date().toISOString(),
      })
    );
  }),

  // Get company
  rest.get(`${API_BASE_URL}/companies/:ticker`, (req, res, ctx) => {
    return res(ctx.json(mockCompanyProfile));
  }),
];
```

### Component Test Example

```typescript
// src/components/CompanyCard.test.tsx

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CompanyCard } from './CompanyCard';
import { mockCompanyProfile } from '@/mocks/mockData';

describe('CompanyCard', () => {
  it('renders company name', () => {
    render(<CompanyCard company={mockCompanyProfile} />);
    expect(screen.getByText(/Microsoft/i)).toBeInTheDocument();
  });

  it('displays maturity score', () => {
    render(<CompanyCard company={mockCompanyProfile} />);
    expect(screen.getByText('85/100')).toBeInTheDocument();
  });

  it('shows maturity label', () => {
    render(<CompanyCard company={mockCompanyProfile} />);
    expect(screen.getByText('Leader')).toBeInTheDocument();
  });
});
```

---

## Production Checklist

### Before Deployment

- [ ] **Environment Variables**
  - [ ] Update `VITE_API_BASE_URL` to production API URL
  - [ ] Update `VITE_WS_URL` to production WebSocket URL
  - [ ] Set `VITE_ENABLE_MOCK_DATA=false`
  - [ ] Set `VITE_ENABLE_DEBUG=false`

- [ ] **Error Handling**
  - [ ] All API calls wrapped in try-catch
  - [ ] Error boundary components in place
  - [ ] User-friendly error messages
  - [ ] Logging configured

- [ ] **Performance**
  - [ ] React Query cache configured
  - [ ] WebSocket reconnection logic tested
  - [ ] Large lists virtualized
  - [ ] Images optimized

- [ ] **Testing**
  - [ ] All critical paths have unit tests
  - [ ] Integration tests pass
  - [ ] E2E tests pass (if applicable)

- [ ] **Security**
  - [ ] No API keys in client code
  - [ ] CORS properly configured
  - [ ] Input validation on forms

- [ ] **UX**
  - [ ] Loading states for all async operations
  - [ ] Proper error messages
  - [ ] Success confirmations
  - [ ] Responsive design tested

---

## Common Patterns

### Pattern 1: Loading State

```typescript
function DataComponent() {
  const { data, isLoading, error } = useCompany('MSFT');

  if (isLoading) {
    return <LoadingSkeleton />;
  }

  if (error) {
    return <ErrorMessage error={error} />;
  }

  if (!data) {
    return <EmptyState />;
  }

  return <DataDisplay data={data} />;
}
```

### Pattern 2: Optimistic Updates

```typescript
async function updateCompany(ticker: string, updates: Partial<CompanyProfile>) {
  // Optimistically update UI
  setCompany((prev) => prev ? { ...prev, ...updates } : null);

  try {
    // Make API call
    const updated = await api.updateCompany(ticker, updates);
    setCompany(updated);
  } catch (error) {
    // Revert on error
    setCompany(originalCompany);
    showError(error);
  }
}
```

### Pattern 3: Debounced Search

```typescript
import { useMemo } from 'react';
import debounce from 'lodash.debounce';

function SearchComponent() {
  const [query, setQuery] = useState('');

  const debouncedSearch = useMemo(
    () =>
      debounce(async (searchTerm: string) => {
        const results = await api.searchCompanies(searchTerm);
        setResults(results);
      }, 300),
    []
  );

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    debouncedSearch(value);
  };

  return <input value={query} onChange={handleSearch} />;
}
```

---

## Troubleshooting

### Issue: WebSocket not connecting

**Solution:**
1. Check if backend WebSocket server is running
2. Verify `VITE_WS_URL` in `.env`
3. Check browser console for CORS errors
4. Ensure job_id is valid

### Issue: API requests failing with CORS errors

**Solution:**
1. Verify backend CORS configuration allows frontend origin
2. Check that `VITE_API_BASE_URL` matches backend URL
3. Ensure cookies/credentials are handled correctly

### Issue: TypeScript errors after updating types

**Solution:**
```bash
# Clear TypeScript cache
rm -rf node_modules/.vite
rm -rf dist

# Restart dev server
npm run dev
```

### Issue: Stale data in UI

**Solution:**
```typescript
// Invalidate React Query cache
import { useQueryClient } from '@tanstack/react-query';

const queryClient = useQueryClient();
queryClient.invalidateQueries({ queryKey: ['companies'] });
```

---

## Support

For issues or questions:
1. Check API contract: `docs/architecture/API_CONTRACT_V2.md`
2. Review backend logs for errors
3. Test endpoints with curl or Postman
4. Contact backend team for API issues
5. File bug reports with reproducible examples

---

**Version:** 1.0.0
**Last Updated:** 2025-10-18
