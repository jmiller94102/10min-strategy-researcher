// useCompanies Hooks - Company data fetching with React Query

import { useQuery, useQueries } from '@tanstack/react-query';
import { api } from '@/services/api';
import type { CompanyProfile, Company } from '@/types/api';

// ============================================================================
// QUERY KEYS
// ============================================================================

export const companyKeys = {
  all: ['companies'] as const,
  lists: () => [...companyKeys.all, 'list'] as const,
  list: (filters?: string) => [...companyKeys.lists(), { filters }] as const,
  details: () => [...companyKeys.all, 'detail'] as const,
  detail: (ticker: string) => [...companyKeys.details(), ticker] as const,
  insights: (ticker: string) => [...companyKeys.detail(ticker), 'insights'] as const,
  enrichment: (ticker: string) => [...companyKeys.detail(ticker), 'enrichment'] as const,
};

// ============================================================================
// SINGLE COMPANY HOOK
// ============================================================================

export interface UseCompanyOptions {
  enabled?: boolean;
  staleTime?: number;
  refetchInterval?: number;
}

export function useCompany(ticker: string, options?: UseCompanyOptions) {
  return useQuery({
    queryKey: companyKeys.detail(ticker),
    queryFn: () => api.getCompany(ticker),
    enabled: options?.enabled ?? true,
    staleTime: options?.staleTime ?? 5 * 60 * 1000, // 5 minutes default
    refetchInterval: options?.refetchInterval,
    retry: 2,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}

// ============================================================================
// MULTIPLE COMPANIES HOOK
// ============================================================================

export function useCompanies(tickers: string[], options?: UseCompanyOptions) {
  return useQuery({
    queryKey: companyKeys.list(tickers.join(',')),
    queryFn: async () => {
      if (tickers.length === 0) return [];

      const promises = tickers.map((ticker) => api.getCompany(ticker));
      return Promise.all(promises);
    },
    enabled: (options?.enabled ?? true) && tickers.length > 0,
    staleTime: options?.staleTime ?? 5 * 60 * 1000,
    retry: 2,
  });
}

// ============================================================================
// PARALLEL COMPANIES HOOK (returns individual query states)
// ============================================================================

export function useCompaniesParallel(tickers: string[], options?: UseCompanyOptions) {
  return useQueries({
    queries: tickers.map((ticker) => ({
      queryKey: companyKeys.detail(ticker),
      queryFn: () => api.getCompany(ticker),
      enabled: options?.enabled ?? true,
      staleTime: options?.staleTime ?? 5 * 60 * 1000,
      retry: 2,
    })),
  });
}

// ============================================================================
// ALL COMPANIES LIST HOOK
// ============================================================================

export function useAllCompanies(options?: UseCompanyOptions) {
  return useQuery({
    queryKey: companyKeys.lists(),
    queryFn: async () => {
      const response = await api.getAllCompanies();
      return response.companies;
    },
    enabled: options?.enabled ?? true,
    staleTime: options?.staleTime ?? 10 * 60 * 1000, // 10 minutes for list
    retry: 2,
  });
}

// ============================================================================
// COMPANY INSIGHTS ONLY HOOK
// ============================================================================

export function useCompanyInsights(ticker: string, options?: UseCompanyOptions) {
  return useQuery({
    queryKey: companyKeys.insights(ticker),
    queryFn: () => api.getCompanyInsights(ticker),
    enabled: options?.enabled ?? true,
    staleTime: options?.staleTime ?? 5 * 60 * 1000,
    retry: 2,
  });
}

// ============================================================================
// COMPANY ENRICHMENT ONLY HOOK
// ============================================================================

export function useCompanyEnrichment(ticker: string, options?: UseCompanyOptions) {
  return useQuery({
    queryKey: companyKeys.enrichment(ticker),
    queryFn: () => api.getCompanyEnrichment(ticker),
    enabled: options?.enabled ?? true,
    staleTime: options?.staleTime ?? 2 * 60 * 1000, // 2 minutes for live data
    retry: 2,
    refetchInterval: options?.refetchInterval,
  });
}

// ============================================================================
// COMPARISON HOOK
// ============================================================================

export function useComparison(tickers: string[], options?: UseCompanyOptions) {
  return useQuery({
    queryKey: [...companyKeys.all, 'comparison', tickers.join(',')],
    queryFn: () => api.compareCompanies(tickers),
    enabled: (options?.enabled ?? true) && tickers.length >= 2,
    staleTime: options?.staleTime ?? 5 * 60 * 1000,
    retry: 2,
  });
}

// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/*
// Example 1: Single company
function CompanyDetailPage({ ticker }: { ticker: string }) {
  const { data: company, isLoading, error } = useCompany(ticker);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!company) return <div>Company not found</div>;

  return (
    <div>
      <h1>{company.company.name}</h1>
      <p>AI Maturity: {company.ai_maturity.total_score}/100</p>
    </div>
  );
}

// Example 2: Multiple companies
function ComparisonPage() {
  const {
    data: companies,
    isLoading,
    error,
  } = useCompanies(['MSFT', 'AAPL', 'NVDA']);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {companies?.map((company) => (
        <div key={company.company.ticker}>{company.company.name}</div>
      ))}
    </div>
  );
}

// Example 3: Parallel loading with individual states
function DashboardGrid() {
  const queries = useCompaniesParallel(['MSFT', 'AAPL', 'NVDA']);

  return (
    <div className="grid grid-cols-3 gap-4">
      {queries.map((query, index) => {
        if (query.isLoading) return <Skeleton key={index} />;
        if (query.error) return <ErrorCard key={index} />;
        if (!query.data) return null;

        return (
          <CompanyCard key={query.data.company.ticker} company={query.data} />
        );
      })}
    </div>
  );
}

// Example 4: Comparison
function ComparisonView() {
  const { data, isLoading } = useComparison(['MSFT', 'AAPL', 'NVDA']);

  if (isLoading) return <div>Loading comparison...</div>;

  return (
    <table>
      <thead>
        <tr>
          <th>Company</th>
          <th>Maturity</th>
          <th>Investment</th>
        </tr>
      </thead>
      <tbody>
        {data?.companies.map((company) => (
          <tr key={company.ticker}>
            <td>{company.name}</td>
            <td>{company.ai_maturity_score}</td>
            <td>${company.total_investment / 1000000}M</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Example 5: Auto-refresh enrichment data
function LiveEnrichmentPanel({ ticker }: { ticker: string }) {
  const { data, isLoading } = useCompanyEnrichment(ticker, {
    refetchInterval: 60000, // Refresh every minute
  });

  return (
    <div>
      <h3>Live Signals</h3>
      <p>AI Jobs: {data?.enrichment.hiring.ai_jobs}</p>
      <p>Recent News: {data?.enrichment.recent_news.length}</p>
    </div>
  );
}

// Example 6: Conditional fetching
function CompanyDetails({ ticker, shouldFetch }: { ticker: string; shouldFetch: boolean }) {
  const { data, isLoading } = useCompany(ticker, {
    enabled: shouldFetch, // Only fetch when modal is open
  });

  if (!shouldFetch) return null;
  if (isLoading) return <div>Loading...</div>;

  return <div>{data?.company.name}</div>;
}
*/
