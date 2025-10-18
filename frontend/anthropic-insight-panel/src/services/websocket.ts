// WebSocket Client with Mock/Real Mode Support
// Simulates WebSocket behavior in mock mode, uses real WebSocket in production

import type { WebSocketMessage } from '@/types/api';
import { getMockCompanyProfile } from '@/mocks/mockData';

// ============================================================================
// CONFIGURATION
// ============================================================================

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8010/ws';
const ENABLE_MOCK_DATA = import.meta.env.VITE_ENABLE_MOCK_DATA === 'true';

type MessageHandler = (message: WebSocketMessage) => void;

// ============================================================================
// WEBSOCKET CLIENT
// ============================================================================

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private handlers: Set<MessageHandler> = new Set();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private jobId: string | null = null;
  private useMockData: boolean;

  // Mock simulation
  private mockInterval: NodeJS.Timeout | null = null;
  private mockTickers: string[] = [];
  private mockCurrentIndex = 0;
  private mockCurrentStage = 0;

  constructor(useMockData: boolean = ENABLE_MOCK_DATA) {
    this.useMockData = useMockData;

    if (useMockData) {
      console.log('🎭 WebSocket Client: Mock mode enabled');
    } else {
      console.log('🌐 WebSocket Client: Real WebSocket mode enabled');
    }
  }

  connect(jobId: string, tickers?: string[]) {
    this.jobId = jobId;

    if (this.useMockData) {
      this.mockTickers = tickers || [];
      this.connectMock();
    } else {
      this.connectReal(jobId);
    }
  }

  // ============================================================================
  // REAL WEBSOCKET CONNECTION
  // ============================================================================

  private connectReal(jobId: string) {
    const wsUrl = `${WS_URL}/pipeline/${jobId}`;

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log(`✅ WebSocket connected for job ${jobId}`);
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          this.notifyHandlers(message);
        } catch (error) {
          console.error('❌ Failed to parse WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
      };

      this.ws.onclose = (event) => {
        console.log('🔌 WebSocket closed:', event.code, event.reason);
        this.attemptReconnect();
      };
    } catch (error) {
      console.error('❌ Failed to create WebSocket connection:', error);
      this.attemptReconnect();
    }
  }

  private attemptReconnect() {
    if (
      this.reconnectAttempts < this.maxReconnectAttempts &&
      this.jobId &&
      !this.useMockData
    ) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

      console.log(
        `🔄 Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`
      );

      setTimeout(() => {
        if (this.jobId) {
          this.connectReal(this.jobId);
        }
      }, delay);
    } else if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('❌ Max reconnection attempts reached. Giving up.');
    }
  }

  // ============================================================================
  // MOCK WEBSOCKET SIMULATION
  // ============================================================================

  private connectMock() {
    console.log('🎭 Starting mock WebSocket simulation');

    // Simulate connection success
    setTimeout(() => {
      console.log(`✅ Mock WebSocket connected for job ${this.jobId}`);
    }, 100);

    // Simulate pipeline progress
    if (this.mockTickers.length > 0) {
      this.simulateProgress();
    }
  }

  private simulateProgress() {
    const stages: Array<'retrieval' | 'analysis' | 'enrichment'> = [
      'retrieval',
      'analysis',
      'enrichment',
    ];

    const stageMessages: Record<string, string> = {
      retrieval: 'Retrieving 10-K from SEC EDGAR...',
      analysis: 'Analyzing with Claude AI...',
      enrichment: 'Enriching with live job and news data...',
    };

    this.mockInterval = setInterval(() => {
      if (this.mockCurrentIndex >= this.mockTickers.length) {
        // All companies processed
        this.stopMockSimulation();
        return;
      }

      const ticker = this.mockTickers[this.mockCurrentIndex];
      const stage = stages[this.mockCurrentStage];

      // Send progress message
      const progressMessage: WebSocketMessage = {
        type: 'progress',
        data: {
          ticker,
          stage,
          status: 'in_progress',
          message: stageMessages[stage],
          percentage: ((this.mockCurrentStage + 1) / stages.length) * 100,
        },
      };
      this.notifyHandlers(progressMessage);

      // Send stage change message
      if (this.mockCurrentStage > 0) {
        const stageChangeMessage: WebSocketMessage = {
          type: 'stage_change',
          data: {
            ticker,
            from_stage: stages[this.mockCurrentStage - 1],
            to_stage: stage,
          },
        };
        this.notifyHandlers(stageChangeMessage);
      }

      // Move to next stage
      this.mockCurrentStage++;

      if (this.mockCurrentStage >= stages.length) {
        // Company complete
        const profile = getMockCompanyProfile(ticker);
        if (profile) {
          const completeMessage: WebSocketMessage = {
            type: 'complete',
            data: {
              ticker,
              profile,
            },
          };
          this.notifyHandlers(completeMessage);
        }

        // Move to next company
        this.mockCurrentIndex++;
        this.mockCurrentStage = 0;
      }
    }, 2500); // Update every 2.5 seconds
  }

  private stopMockSimulation() {
    if (this.mockInterval) {
      clearInterval(this.mockInterval);
      this.mockInterval = null;
    }
    console.log('✅ Mock WebSocket simulation complete');
  }

  // ============================================================================
  // HANDLER MANAGEMENT
  // ============================================================================

  onMessage(handler: MessageHandler): () => void {
    this.handlers.add(handler);
    return () => this.handlers.delete(handler); // Return cleanup function
  }

  private notifyHandlers(message: WebSocketMessage) {
    this.handlers.forEach((handler) => {
      try {
        handler(message);
      } catch (error) {
        console.error('❌ Error in WebSocket message handler:', error);
      }
    });
  }

  // ============================================================================
  // CONNECTION MANAGEMENT
  // ============================================================================

  disconnect() {
    if (this.useMockData) {
      this.stopMockSimulation();
    } else if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    this.handlers.clear();
    this.jobId = null;
    this.reconnectAttempts = 0;
    this.mockCurrentIndex = 0;
    this.mockCurrentStage = 0;

    console.log('🔌 WebSocket disconnected');
  }

  getReadyState(): number | null {
    if (this.useMockData) {
      // Simulate OPEN state in mock mode
      return 1; // WebSocket.OPEN
    }
    return this.ws?.readyState ?? null;
  }

  isConnected(): boolean {
    if (this.useMockData) {
      return this.mockInterval !== null || this.jobId !== null;
    }
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

// ============================================================================
// EXPORT
// ============================================================================

export function createWebSocketClient(): WebSocketClient {
  // ⚠️ HARDCODED: Use real WebSocket for backend integration
  return new WebSocketClient(false);  // false = REAL mode (not mock)
}

// Log current mode (hardcoded to REAL for backend integration)
console.log(
  `🔌 WebSocket Client module loaded:`,
  '🌐 Real WebSocket Mode (hardcoded for backend integration)'
);
