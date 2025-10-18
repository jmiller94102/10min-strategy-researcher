// ============================================================================
// 10-K AI Intelligence Pipeline - TypeScript Type Definitions
// Version: 2.0.0
// Auto-generated from: docs/architecture/API_CONTRACT_V2.md
// Last Updated: 2025-10-18
// ============================================================================

// ============================================================================
// COMPANY MODELS
// ============================================================================

export interface Company {
  name: string;           // e.g., "Microsoft Corporation"
  ticker: string;         // e.g., "MSFT"
  cik: string;           // SEC Central Index Key, e.g., "0000789019"
  domain?: string;       // e.g., "microsoft.com"
}

export interface CompanyProfile {
  company: Company;
  filing_date: string;                  // ISO 8601, e.g., "2024-07-30"
  fiscal_year: number;                  // e.g., 2024
  ai_insights: AIInsights;
  enrichment: EnrichmentData;
  ai_maturity: AIMaturityScore;
  sdr_playbook: SDRPlaybook;
  metadata: ProfileMetadata;
}

// ============================================================================
// AI INSIGHTS MODELS
// ============================================================================

export interface AIInsights {
  investments: AIInvestment[];
  products: AIProduct[];
  risks: AIRisk[];
  timeline: AITimeline;
  competitive_positioning: CompetitivePositioning;
}

export interface AIInvestment {
  amount: string;                       // Human-readable, e.g., "$50M"
  amount_numeric: number;               // Actual number, e.g., 50000000
  purpose: string;                      // e.g., "AI infrastructure and R&D"
  timeframe: string;                    // e.g., "FY2024"
  quote: string;                        // Direct quote from 10-K
  confidence: "high" | "medium" | "low";
  source_section: "business" | "risk_factors" | "mda";  // Management's Discussion & Analysis
}

export interface AIProduct {
  product_name: string;                 // e.g., "GitHub Copilot"
  description: string;                  // Brief description
  launch_status: "available" | "beta" | "planned";
  target_market: "enterprise" | "consumer" | "developer";
  quote: string;                        // Direct quote from 10-K
  revenue_impact?: "mentioned" | "not_mentioned";
}

export interface AIRisk {
  category: "competitive" | "implementation" | "regulatory" | "ethical";
  risk: string;                         // Risk description
  severity: "high" | "medium" | "low";
  quote: string;                        // Direct quote from 10-K
}

export interface AITimeline {
  current_initiatives: string[];        // Ongoing AI projects
  near_term_plans: string[];            // 1-2 year plans
  long_term_vision: string;             // 3-5 year vision statement
  milestones: Milestone[];
}

export interface Milestone {
  date: string;                         // ISO 8601 or description
  event: string;                        // Milestone description
}

export interface CompetitivePositioning {
  strengths: string[];                  // Competitive advantages
  competitors_mentioned: string[];      // List of competitor names
  differentiation: string;              // How they differentiate
  concerns_about_competition: string[]; // Competitive concerns
}

// ============================================================================
// ENRICHMENT MODELS (Live Data)
// ============================================================================

export interface EnrichmentData {
  hiring: HiringData;
  recent_news: NewsItem[];
  enriched_at: string;                  // ISO 8601, when data was scraped
}

export interface HiringData {
  total_jobs: number;                   // Total open positions
  ai_jobs: number;                      // AI-related positions
  ai_job_details: JobPosting[];         // Top 10-20 AI jobs
  hiring_urgency: "HIGH" | "NORMAL" | "LOW";
  tech_stack: string[];                 // Unique technologies across all jobs
  scraped_at: string;                   // ISO 8601
}

export interface JobPosting {
  title: string;                        // e.g., "Senior ML Engineer"
  location: string;                     // e.g., "Seattle, WA (Remote)"
  job_url: string;                      // Link to job posting
  tech_stack: string[];                 // e.g., ["Python", "TensorFlow", "PyTorch"]
  posted_date: string;                  // e.g., "2025-10-10"
  seniority: "junior" | "mid" | "senior" | "staff" | "principal";
  remote: boolean;
}

export interface NewsItem {
  headline: string;                     // News headline
  source: string;                       // e.g., "TechCrunch"
  date: string;                         // ISO 8601
  url: string;                          // Link to article
  summary?: string;                     // Optional summary
  category: "product_launch" | "investment" | "partnership" | "research" | "executive" | "general";
}

// ============================================================================
// AI MATURITY SCORING
// ============================================================================

export interface AIMaturityScore {
  total_score: number;                  // 0-100
  breakdown: {
    investment: number;                 // 0-25 (based on investment amount)
    product: number;                    // 0-25 (based on product count/maturity)
    strategic_importance: number;       // 0-25 (based on mentions/emphasis)
    organizational_readiness: number;   // 0-25 (based on hiring/structure)
  };
  percentile: number;                   // 0-100, vs other analyzed companies
  label: "Leader" | "Fast Follower" | "Emerging" | "Laggard";
}

// ============================================================================
// SDR PLAYBOOK (Sales Intelligence)
// ============================================================================

export interface SDRPlaybook {
  discovery_questions: string[];        // 5-10 tailored questions
  value_propositions: string[];         // 3-5 value props based on insights
  objection_handlers: Record<string, string>;  // Common objections → responses
  executive_summary: string;            // 2-3 paragraph summary
  talking_points: string[];             // Key conversation starters
}

// ============================================================================
// METADATA
// ============================================================================

export interface ProfileMetadata {
  analyzed_at: string;                  // ISO 8601, when analysis completed
  analysis_time_seconds: number;        // Time taken for AI analysis
  retrieval_time_seconds: number;       // Time taken to retrieve 10-K
  enrichment_time_seconds: number;      // Time taken for enrichment
  enrichment_completeness: number;      // 0-1, % of enrichment successful
  status: "complete" | "partial" | "failed";
}

// ============================================================================
// PIPELINE MODELS
// ============================================================================

export interface PipelineStartRequest {
  company_tickers: string[];            // e.g., ["MSFT", "AAPL", "NVDA"]
  skip_enrichment?: boolean;            // Default: false
}

export interface PipelineStartResponse {
  job_id: string;                       // UUID
  status: "started";
  total_companies: number;
  estimated_time_seconds: number;
  started_at: string;                   // ISO 8601
}

export interface PipelineStatusResponse {
  job_id: string;
  status: "started" | "in_progress" | "completed" | "failed" | "partial";
  progress: PipelineProgress;
  companies: CompanyStatus[];
  started_at: string;                   // ISO 8601
  estimated_completion?: string;        // ISO 8601
  completed_at?: string;                // ISO 8601 (if completed)
}

export interface PipelineProgress {
  current_stage: "retrieval" | "analysis" | "enrichment" | "finalization";
  companies_processed: number;
  companies_total: number;
  percentage: number;                   // 0-100
}

export interface CompanyStatus {
  ticker: string;
  status: "pending" | "retrieving" | "analyzing" | "enriching" | "completed" | "failed";
  stage: "retrieval" | "analysis" | "enrichment" | "finalization" | null;
  message?: string;                     // e.g., "Scraping 10-K from EDGAR..."
  error?: string;                       // Error message if failed
  started_at?: string;                  // ISO 8601
  completed_at?: string;                // ISO 8601
}

export interface PipelineResultsResponse {
  job_id: string;
  status: "completed" | "partial";
  results: CompanyProfile[];
  summary: {
    total_companies: number;
    successful: number;
    failed: number;
    total_time_seconds: number;
  };
}

// ============================================================================
// COMPARISON MODELS
// ============================================================================

export interface ComparisonResponse {
  companies: CompanyComparison[];
  rankings: {
    by_maturity: string[];              // Ticker list sorted by maturity
    by_investment: string[];            // Ticker list sorted by investment
    by_hiring: string[];                // Ticker list sorted by AI hiring
  };
}

export interface CompanyComparison {
  ticker: string;
  name: string;
  ai_maturity_score: number;
  total_investment: number;
  ai_jobs: number;
  ai_products_count: number;
  recent_news_count: number;
  label: "Leader" | "Fast Follower" | "Emerging" | "Laggard";
}

// ============================================================================
// EXPORT MODELS
// ============================================================================

export interface ExportSalesforceRequest {
  job_id: string;
}

export interface ExportSalesforceResponse {
  download_url: string;                 // e.g., "/downloads/salesforce_uuid.csv"
  filename: string;                     // e.g., "salesforce_import_2025-10-18.csv"
  expires_at: string;                   // ISO 8601
}

export interface ExportPlaybooksRequest {
  job_id: string;
  tickers?: string[];                   // Optional, defaults to all
}

export interface ExportPlaybooksResponse {
  download_url: string;                 // e.g., "/downloads/playbooks_uuid.zip"
  filename: string;                     // e.g., "ai_playbooks_2025-10-18.zip"
  files_included: string[];             // e.g., ["MSFT_playbook.pdf", "AAPL_playbook.pdf"]
  expires_at: string;                   // ISO 8601
}

// ============================================================================
// HEALTH & UTILITY MODELS
// ============================================================================

export interface HealthResponse {
  status: "healthy" | "degraded" | "unhealthy";
  daytona: "connected" | "disconnected";
  anthropic_api: "connected" | "disconnected";
  version: string;
  uptime_seconds: number;
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
}

// ============================================================================
// WEBSOCKET MESSAGE TYPES
// ============================================================================

export type WebSocketMessage =
  | ProgressMessage
  | CompleteMessage
  | ErrorMessage
  | StageChangeMessage;

export interface ProgressMessage {
  type: "progress";
  data: {
    ticker: string;
    stage: "retrieval" | "analysis" | "enrichment";
    status: "in_progress";
    message: string;                    // e.g., "Scraping career page..."
    percentage: number;                 // Company-specific progress 0-100
  };
}

export interface CompleteMessage {
  type: "complete";
  data: {
    ticker: string;
    profile: CompanyProfile;
  };
}

export interface ErrorMessage {
  type: "error";
  data: {
    ticker: string;
    stage: "retrieval" | "analysis" | "enrichment";
    error: string;
  };
}

export interface StageChangeMessage {
  type: "stage_change";
  data: {
    ticker: string;
    from_stage: string;
    to_stage: string;
  };
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type PipelineStage = "retrieval" | "analysis" | "enrichment" | "finalization";
export type PipelineStatus = "started" | "in_progress" | "completed" | "failed" | "partial";
export type CompanyStatusType = "pending" | "retrieving" | "analyzing" | "enriching" | "completed" | "failed";
export type MaturityLabel = "Leader" | "Fast Follower" | "Emerging" | "Laggard";
export type HiringUrgency = "HIGH" | "NORMAL" | "LOW";
export type Confidence = "high" | "medium" | "low";
export type Severity = "high" | "medium" | "low";
export type LaunchStatus = "available" | "beta" | "planned";
export type TargetMarket = "enterprise" | "consumer" | "developer";
export type Seniority = "junior" | "mid" | "senior" | "staff" | "principal";
export type NewsCategory = "product_launch" | "investment" | "partnership" | "research" | "executive" | "general";

// ============================================================================
// DEPRECATED TYPES (for backward compatibility - remove after migration)
// ============================================================================

/**
 * @deprecated Use CompanyProfile instead
 */
export interface LegacyCompanyProfile {
  ticker: string;
  company_name: string;
  filing_date: string;
  analyzed_at: string;
  ai_maturity: AIMaturityScore;
  investments: AIInvestment[];
  products: string[];
  risk_factors: string[];
  enrichment: EnrichmentData;
  sdr_playbook: SDRPlaybook;
}

// ============================================================================
// DEBUG/WORKFLOW TYPES (for hackathon demo panel)
// ============================================================================

export interface WorkflowStep {
  id: string;
  name: string;
  tool: 'Browser Use' | 'Daytona' | 'Agent' | 'System';
  status: 'pending' | 'running' | 'complete' | 'error';
  startTime?: number;
  endTime?: number;
  details?: string;
}

export interface WorkflowState {
  currentCompany?: string;
  steps: WorkflowStep[];
  activeStepId?: string;
}

// Alias for backward compatibility
export interface PipelineJob extends PipelineStatusResponse {}
