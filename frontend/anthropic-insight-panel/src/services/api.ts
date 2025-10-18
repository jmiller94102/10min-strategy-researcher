// API Client with 3-Mode Support
// Modes:
//   1. CLIENT_MOCK: Client-side mocks (no HTTP requests)
//   2. BACKEND_MOCK: Backend /mock/* endpoints (real HTTP to mock data)
//   3. REAL: Real backend endpoints (production)

import type {
  Company,
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

import {
  mockProfiles,
  mockCompanies,
  getMockCompanyProfile,
  getAllMockCompanies,
} from '@/mocks/mockData';

// ============================================================================
// CONFIGURATION
// ============================================================================

// ⚠️ HARDCODED FOR BACKEND INTEGRATION (Vite .env not loading)
const API_BASE_URL = 'http://localhost:8010';

// API Mode: CLIENT_MOCK | BACKEND_MOCK | REAL
type APIMode = 'CLIENT_MOCK' | 'BACKEND_MOCK' | 'REAL';

const getAPIMode = (): APIMode => {
  const mode = import.meta.env.VITE_API_MODE || 'CLIENT_MOCK';

  // Legacy support: VITE_ENABLE_MOCK_DATA=true → CLIENT_MOCK
  if (import.meta.env.VITE_ENABLE_MOCK_DATA === 'true') {
    return 'CLIENT_MOCK';
  }

  return mode as APIMode;
};

// ⚠️ HARDCODED FOR BACKEND INTEGRATION (Vite .env not loading)
const API_MODE: APIMode = 'BACKEND_MOCK';

// Mock delays (milliseconds) for realistic simulation
const MOCK_DELAYS = {
  fast: 200,
  medium: 500,
  slow: 1000,
};

// ============================================================================
// ERROR HANDLING
// ============================================================================

export class APIError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// ============================================================================
// MOCK HELPERS
// ============================================================================

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

// Store mock pipeline jobs
const mockPipelineJobs: Record<string, any> = {};

// ============================================================================
// API CLIENT
// ============================================================================

class APIClient {
  private baseURL: string;
  private mode: APIMode;

  constructor(baseURL: string, mode: APIMode) {
    this.baseURL = baseURL;
    this.mode = mode;

    this.logMode();
  }

  private logMode() {
    switch (this.mode) {
      case 'CLIENT_MOCK':
        console.log('🎭 API Client: CLIENT_MOCK mode (client-side simulation)');
        break;
      case 'BACKEND_MOCK':
        console.log('🧪 API Client: BACKEND_MOCK mode (using /mock/* endpoints)');
        break;
      case 'REAL':
        console.log('🌐 API Client: REAL mode (production endpoints)');
        break;
    }
  }

  private shouldUseClientMock(): boolean {
    return this.mode === 'CLIENT_MOCK';
  }

  private getEndpointPath(path: string): string {
    if (this.mode === 'BACKEND_MOCK') {
      // Prepend /mock to the path
      return `/mock${path}`;
    }
    return path;
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    if (this.shouldUseClientMock()) {
      throw new Error('request() should not be called in CLIENT_MOCK mode');
    }

    // Apply mock prefix if in BACKEND_MOCK mode
    const finalEndpoint = this.getEndpointPath(endpoint);
    const url = `${this.baseURL}${finalEndpoint}`;

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
    if (this.shouldUseClientMock()) {
      await delay(MOCK_DELAYS.medium);

      const jobId = `mock-job-${Date.now()}`;
      const startedAt = new Date().toISOString();

      // Store mock job state
      mockPipelineJobs[jobId] = {
        job_id: jobId,
        status: 'in_progress',
        progress: {
          current_stage: 'retrieval',
          companies_processed: 0,
          companies_total: request.company_tickers.length,
          percentage: 0,
        },
        companies: request.company_tickers.map((ticker) => ({
          ticker,
          status: 'pending',
          stage: null,
        })),
        started_at: startedAt,
        request,
      };

      // Simulate pipeline progress
      this.simulatePipelineProgress(jobId, request.company_tickers);

      return {
        job_id: jobId,
        status: 'started',
        total_companies: request.company_tickers.length,
        estimated_time_seconds: request.company_tickers.length * 140,
        started_at: startedAt,
      };
    }

    return this.request('/pipeline/start', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getPipelineStatus(jobId: string): Promise<PipelineStatusResponse> {
    if (this.shouldUseClientMock()) {
      await delay(MOCK_DELAYS.fast);

      const job = mockPipelineJobs[jobId];
      if (!job) {
        throw new APIError(
          `Pipeline job '${jobId}' not found`,
          'JOB_NOT_FOUND',
          { job_id: jobId }
        );
      }

      return {
        job_id: job.job_id,
        status: job.status,
        progress: job.progress,
        companies: job.companies,
        started_at: job.started_at,
        estimated_completion: job.estimated_completion,
        completed_at: job.completed_at,
      };
    }

    return this.request(`/pipeline/status/${jobId}`);
  }

  async getPipelineResults(jobId: string): Promise<PipelineResultsResponse> {
    if (this.shouldUseClientMock()) {
      await delay(MOCK_DELAYS.medium);

      const job = mockPipelineJobs[jobId];
      if (!job) {
        throw new APIError(
          `Pipeline job '${jobId}' not found`,
          'JOB_NOT_FOUND',
          { job_id: jobId }
        );
      }

      if (job.status !== 'completed') {
        throw new APIError(
          'Pipeline job is still processing',
          'PROCESSING_IN_PROGRESS',
          { status: job.status, percentage: job.progress.percentage }
        );
      }

      const results = job.request.company_tickers
        .map((ticker: string) => getMockCompanyProfile(ticker))
        .filter(Boolean) as CompanyProfile[];

      return {
        job_id: jobId,
        status: 'completed',
        results,
        summary: {
          total_companies: job.request.company_tickers.length,
          successful: results.length,
          failed: 0,
          total_time_seconds: job.request.company_tickers.length * 15,
        },
      };
    }

    return this.request(`/pipeline/results/${jobId}`);
  }

  // Simulate realistic pipeline progress for mock mode
  private simulatePipelineProgress(jobId: string, tickers: string[]) {
    const job = mockPipelineJobs[jobId];
    if (!job) return;

    const stages: Array<'retrieval' | 'analysis' | 'enrichment' | 'finalization'> = [
      'retrieval',
      'analysis',
      'enrichment',
      'finalization',
    ];

    let currentCompanyIndex = 0;
    let currentStageIndex = 0;

    const progressInterval = setInterval(() => {
      if (currentCompanyIndex >= tickers.length) {
        // Pipeline complete
        clearInterval(progressInterval);
        job.status = 'completed';
        job.progress.percentage = 100;
        job.progress.current_stage = 'finalization';
        job.completed_at = new Date().toISOString();
        return;
      }

      const ticker = tickers[currentCompanyIndex];
      const stage = stages[currentStageIndex];

      // Update company status
      const companyStatus = job.companies.find((c: any) => c.ticker === ticker);
      if (companyStatus) {
        companyStatus.stage = stage;
        companyStatus.status = currentStageIndex === 3 ? 'completed' :
                               stage === 'retrieval' ? 'retrieving' :
                               stage === 'analysis' ? 'analyzing' :
                               stage === 'enrichment' ? 'enriching' : 'completed';
      }

      // Update overall progress
      const totalSteps = tickers.length * stages.length;
      const completedSteps = currentCompanyIndex * stages.length + currentStageIndex + 1;
      job.progress.percentage = Math.floor((completedSteps / totalSteps) * 100);
      job.progress.current_stage = stage;
      job.progress.companies_processed = currentCompanyIndex;

      // Move to next stage
      currentStageIndex++;
      if (currentStageIndex >= stages.length) {
        currentStageIndex = 0;
        currentCompanyIndex++;
        job.progress.companies_processed = currentCompanyIndex;
      }
    }, 2000); // Update every 2 seconds
  }

  // ============================================================================
  // COMPANY ENDPOINTS
  // ============================================================================

  async getCompany(ticker: string): Promise<CompanyProfile> {
    if (this.shouldUseClientMock()) {
      await delay(MOCK_DELAYS.medium);

      const profile = getMockCompanyProfile(ticker);
      if (!profile) {
        throw new APIError(
          `Company '${ticker}' not found`,
          'COMPANY_NOT_FOUND',
          { ticker, available_tickers: Object.keys(mockProfiles) }
        );
      }

      return profile;
    }

    return this.request(`/companies/${ticker}`);
  }

  async getAllCompanies(): Promise<{ companies: Company[] }> {
    if (this.shouldUseClientMock()) {
      await delay(MOCK_DELAYS.fast);
      return { companies: getAllMockCompanies() };
    }

    return this.request('/companies');
  }

  async getCompanyInsights(ticker: string): Promise<{
    company: Company;
    ai_insights: any;
    ai_maturity: any;
    metadata: { analyzed_at: string };
  }> {
    if (this.shouldUseClientMock()) {
      await delay(MOCK_DELAYS.medium);

      const profile = getMockCompanyProfile(ticker);
      if (!profile) {
        throw new APIError(
          `Company '${ticker}' not found`,
          'COMPANY_NOT_FOUND',
          { ticker }
        );
      }

      return {
        company: profile.company,
        ai_insights: profile.ai_insights,
        ai_maturity: profile.ai_maturity,
        metadata: { analyzed_at: profile.metadata.analyzed_at },
      };
    }

    return this.request(`/companies/${ticker}/insights`);
  }

  async getCompanyEnrichment(ticker: string): Promise<{
    company: Company;
    enrichment: any;
  }> {
    if (this.shouldUseClientMock()) {
      await delay(MOCK_DELAYS.medium);

      const profile = getMockCompanyProfile(ticker);
      if (!profile) {
        throw new APIError(
          `Company '${ticker}' not found`,
          'COMPANY_NOT_FOUND',
          { ticker }
        );
      }

      return {
        company: profile.company,
        enrichment: profile.enrichment,
      };
    }

    return this.request(`/companies/${ticker}/enrichment`);
  }

  // ============================================================================
  // COMPARISON ENDPOINT
  // ============================================================================

  async compareCompanies(tickers: string[]): Promise<ComparisonResponse> {
    if (this.shouldUseClientMock()) {
      await delay(MOCK_DELAYS.medium);

      const companies = tickers
        .map((ticker) => {
          const profile = getMockCompanyProfile(ticker);
          if (!profile) return null;

          return {
            ticker: profile.company.ticker,
            name: profile.company.name,
            ai_maturity_score: profile.ai_maturity.total_score,
            total_investment:
              profile.ai_insights.investments.reduce(
                (sum, inv) => sum + inv.amount_numeric,
                0
              ),
            ai_jobs: profile.enrichment.hiring.ai_jobs,
            ai_products_count: profile.ai_insights.products.length,
            recent_news_count: profile.enrichment.recent_news.length,
            label: profile.ai_maturity.label,
          };
        })
        .filter(Boolean);

      // Sort for rankings
      const byMaturity = [...companies].sort(
        (a, b) => (b?.ai_maturity_score || 0) - (a?.ai_maturity_score || 0)
      );
      const byInvestment = [...companies].sort(
        (a, b) => (b?.total_investment || 0) - (a?.total_investment || 0)
      );
      const byHiring = [...companies].sort(
        (a, b) => (b?.ai_jobs || 0) - (a?.ai_jobs || 0)
      );

      return {
        companies: companies as any,
        rankings: {
          by_maturity: byMaturity.map((c) => c!.ticker),
          by_investment: byInvestment.map((c) => c!.ticker),
          by_hiring: byHiring.map((c) => c!.ticker),
        },
      };
    }

    const tickerParam = tickers.join(',');
    return this.request(`/comparison?tickers=${tickerParam}`);
  }

  // ============================================================================
  // EXPORT ENDPOINTS
  // ============================================================================

  async exportSalesforce(
    request: ExportSalesforceRequest
  ): Promise<ExportSalesforceResponse> {
    if (this.shouldUseClientMock()) {
      await delay(MOCK_DELAYS.slow);

      return {
        download_url: `/downloads/salesforce_${request.job_id}.csv`,
        filename: `salesforce_import_${new Date().toISOString().split('T')[0]}.csv`,
        expires_at: new Date(Date.now() + 3600000).toISOString(), // 1 hour
      };
    }

    return this.request('/export/salesforce', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async exportPlaybooks(
    request: ExportPlaybooksRequest
  ): Promise<ExportPlaybooksResponse> {
    if (this.shouldUseClientMock()) {
      await delay(MOCK_DELAYS.slow);

      const tickers = request.tickers || ['MSFT', 'AAPL', 'NVDA'];

      return {
        download_url: `/downloads/playbooks_${request.job_id}.zip`,
        filename: `ai_playbooks_${new Date().toISOString().split('T')[0]}.zip`,
        files_included: [
          ...tickers.map((t) => `${t}_playbook.pdf`),
          'ALL_COMPANIES_comparison.pdf',
        ],
        expires_at: new Date(Date.now() + 3600000).toISOString(), // 1 hour
      };
    }

    return this.request('/export/playbooks', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // ============================================================================
  // HEALTH ENDPOINT
  // ============================================================================

  async getHealth(): Promise<HealthResponse> {
    if (this.shouldUseClientMock()) {
      await delay(MOCK_DELAYS.fast);

      return {
        status: 'healthy',
        daytona: 'connected',
        anthropic_api: 'connected',
        version: '1.0.0-mock',
        uptime_seconds: Math.floor(Math.random() * 100000),
      };
    }

    return this.request('/health');
  }
}

// ============================================================================
// EXPORT SINGLETON
// ============================================================================

export const api = new APIClient(API_BASE_URL, API_MODE);
// Note: APIError is already exported at line 63 (inline export)

// Log current configuration
console.log(
  `📡 API Client initialized:`,
  `Mode: ${API_MODE}`,
  `Base URL: ${API_BASE_URL}`
);
