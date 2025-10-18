// usePipeline Hook - Complete pipeline management with WebSocket support

import { useState, useEffect, useCallback, useRef } from 'react';
import { api } from '@/services/api';
import { createWebSocketClient } from '@/services/websocket';
import type {
  PipelineStatusResponse,
  CompanyProfile,
  WebSocketMessage,
  CompanyStatus,
} from '@/types/api';

// ============================================================================
// TYPES
// ============================================================================

interface UsePipelineReturn {
  // Actions
  startPipeline: (tickers: string[]) => Promise<void>;
  reset: () => void;

  // State
  jobId: string | null;
  status: PipelineStatusResponse | null;
  results: CompanyProfile[];
  progress: number;
  loading: boolean;
  error: string | null;

  // Company-specific progress
  companyStatuses: CompanyStatus[];
}

// ============================================================================
// HOOK
// ============================================================================

export function usePipeline(): UsePipelineReturn {
  // State
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<PipelineStatusResponse | null>(null);
  const [results, setResults] = useState<CompanyProfile[]>([]);
  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [companyStatuses, setCompanyStatuses] = useState<CompanyStatus[]>([]);

  // Refs
  const wsClientRef = useRef(createWebSocketClient());
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const tickersRef = useRef<string[]>([]);

  // ============================================================================
  // START PIPELINE
  // ============================================================================

  const startPipeline = useCallback(async (tickers: string[]) => {
    console.log('🚀 Starting pipeline for tickers:', tickers);

    // Reset state
    setLoading(true);
    setError(null);
    setResults([]);
    setProgress(0);
    setCompanyStatuses(
      tickers.map((ticker) => ({
        ticker,
        status: 'pending',
        stage: null,
      }))
    );

    tickersRef.current = tickers;

    try {
      // Start pipeline via API
      const response = await api.startPipeline({
        company_tickers: tickers,
        skip_enrichment: false,
      });

      console.log('✅ Pipeline started:', response.job_id);

      setJobId(response.job_id);

      // Connect WebSocket for real-time updates
      connectWebSocket(response.job_id, tickers);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to start pipeline';
      console.error('❌ Pipeline start failed:', errorMessage);
      setError(errorMessage);
      setLoading(false);
    }
  }, []);

  // ============================================================================
  // WEBSOCKET CONNECTION
  // ============================================================================

  const connectWebSocket = useCallback((jobId: string, tickers: string[]) => {
    const wsClient = wsClientRef.current;

    // Setup message handler
    const unsubscribe = wsClient.onMessage((message: WebSocketMessage) => {
      handleWebSocketMessage(message);
    });

    // Connect
    wsClient.connect(jobId, tickers);

    // Fallback to polling if WebSocket fails
    setTimeout(() => {
      if (!wsClient.isConnected()) {
        console.warn('⚠️ WebSocket not connected, falling back to polling');
        startPolling(jobId);
      }
    }, 5000);

    return unsubscribe;
  }, []);

  // ============================================================================
  // WEBSOCKET MESSAGE HANDLING
  // ============================================================================

  const handleWebSocketMessage = useCallback((message: WebSocketMessage) => {
    console.log('📨 WebSocket message:', message.type, message.data);

    switch (message.type) {
      case 'progress':
        // Update individual company progress
        setCompanyStatuses((prev) =>
          prev.map((cs) =>
            cs.ticker === message.data.ticker
              ? {
                  ...cs,
                  status: message.data.status as any,
                  stage: message.data.stage,
                  message: message.data.message,
                }
              : cs
          )
        );
        break;

      case 'stage_change':
        // Update company stage
        setCompanyStatuses((prev) =>
          prev.map((cs) =>
            cs.ticker === message.data.ticker
              ? { ...cs, stage: message.data.to_stage as any }
              : cs
          )
        );
        break;

      case 'complete':
        // Company processing complete
        setCompanyStatuses((prev) =>
          prev.map((cs) =>
            cs.ticker === message.data.ticker
              ? { ...cs, status: 'completed', stage: 'finalization' }
              : cs
          )
        );

        // Add to results
        setResults((prev) => [...prev, message.data.profile]);

        // Check if all companies are complete
        setCompanyStatuses((currentStatuses) => {
          const allComplete = currentStatuses.every(
            (cs) => cs.status === 'completed' || cs.ticker === message.data.ticker
          );

          if (allComplete) {
            console.log('✅ All companies processed!');
            setProgress(100);
            setLoading(false);
            wsClientRef.current.disconnect();
            if (pollIntervalRef.current) {
              clearInterval(pollIntervalRef.current);
            }
          }

          return currentStatuses;
        });
        break;

      case 'error':
        // Company processing failed
        setCompanyStatuses((prev) =>
          prev.map((cs) =>
            cs.ticker === message.data.ticker
              ? {
                  ...cs,
                  status: 'failed',
                  error: message.data.error,
                }
              : cs
          )
        );
        break;
    }

    // Update overall progress
    setCompanyStatuses((currentStatuses) => {
      const completed = currentStatuses.filter((cs) => cs.status === 'completed').length;
      const total = currentStatuses.length;
      const newProgress = total > 0 ? Math.floor((completed / total) * 100) : 0;
      setProgress(newProgress);
      return currentStatuses;
    });
  }, []);

  // ============================================================================
  // POLLING FALLBACK
  // ============================================================================

  const startPolling = useCallback((jobId: string) => {
    console.log('🔄 Starting status polling');

    const interval = setInterval(async () => {
      try {
        const statusData = await api.getPipelineStatus(jobId);
        setStatus(statusData);
        setProgress(statusData.progress.percentage);
        setCompanyStatuses(statusData.companies);

        if (statusData.status === 'completed') {
          console.log('✅ Pipeline completed (via polling)');
          clearInterval(interval);
          await fetchResults(jobId);
          setLoading(false);
        } else if (statusData.status === 'failed') {
          console.error('❌ Pipeline failed');
          clearInterval(interval);
          setError('Pipeline processing failed');
          setLoading(false);
        }
      } catch (err) {
        console.error('❌ Polling error:', err);
      }
    }, 2000); // Poll every 2 seconds

    pollIntervalRef.current = interval;
  }, []);

  // ============================================================================
  // FETCH RESULTS
  // ============================================================================

  const fetchResults = useCallback(async (jobId: string) => {
    try {
      console.log('📥 Fetching pipeline results');
      const resultsData = await api.getPipelineResults(jobId);
      setResults(resultsData.results);
      console.log('✅ Results fetched:', resultsData.results.length, 'companies');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch results';
      console.error('❌ Failed to fetch results:', errorMessage);
      setError(errorMessage);
    }
  }, []);

  // ============================================================================
  // RESET
  // ============================================================================

  const reset = useCallback(() => {
    console.log('🔄 Resetting pipeline state');

    setJobId(null);
    setStatus(null);
    setResults([]);
    setProgress(0);
    setLoading(false);
    setError(null);
    setCompanyStatuses([]);

    // Cleanup WebSocket
    wsClientRef.current.disconnect();

    // Cleanup polling
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
  }, []);

  // ============================================================================
  // CLEANUP ON UNMOUNT
  // ============================================================================

  useEffect(() => {
    return () => {
      console.log('🧹 Cleaning up pipeline hook');
      wsClientRef.current.disconnect();
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  // ============================================================================
  // RETURN
  // ============================================================================

  return {
    // Actions
    startPipeline,
    reset,

    // State
    jobId,
    status,
    results,
    progress,
    loading,
    error,
    companyStatuses,
  };
}

// ============================================================================
// USAGE EXAMPLE
// ============================================================================

/*
function PipelineDemo() {
  const {
    startPipeline,
    progress,
    results,
    loading,
    error,
    companyStatuses,
    reset,
  } = usePipeline();

  const handleStart = () => {
    startPipeline(['MSFT', 'AAPL', 'NVDA']);
  };

  return (
    <div>
      <button onClick={handleStart} disabled={loading}>
        {loading ? 'Processing...' : 'Start Pipeline'}
      </button>

      {loading && (
        <div>
          <p>Progress: {progress}%</p>
          <ul>
            {companyStatuses.map((cs) => (
              <li key={cs.ticker}>
                {cs.ticker}: {cs.status} ({cs.stage || 'pending'})
              </li>
            ))}
          </ul>
        </div>
      )}

      {error && <div>Error: {error}</div>}

      {results.length > 0 && (
        <div>
          <h2>Results ({results.length})</h2>
          {results.map((company) => (
            <div key={company.company.ticker}>
              {company.company.name} - Maturity: {company.ai_maturity.total_score}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
*/
