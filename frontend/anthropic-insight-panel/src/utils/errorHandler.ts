// Error Handling Utilities
// Centralized error handling and user-friendly error messages

import { APIError } from '@/services/api';
import type { ErrorResponse } from '@/types/api';

// ============================================================================
// ERROR TYPES
// ============================================================================

export interface UserFriendlyError {
  title: string;
  message: string;
  action?: string;
  code?: string;
  details?: Record<string, any>;
}

// ============================================================================
// ERROR HANDLERS
// ============================================================================

export function handleAPIError(error: unknown): UserFriendlyError {
  console.error('API Error:', error);

  if (error instanceof APIError) {
    return {
      title: getErrorTitle(error.code),
      message: getErrorMessage(error.code, error.message, error.details),
      action: getErrorAction(error.code),
      code: error.code,
      details: error.details,
    };
  }

  if (error instanceof Error) {
    return {
      title: 'An error occurred',
      message: error.message,
      action: 'Please try again.',
    };
  }

  return {
    title: 'Unknown error',
    message: 'An unexpected error occurred. Please try again.',
    action: 'Contact support if the problem persists.',
  };
}

// ============================================================================
// ERROR TITLES
// ============================================================================

function getErrorTitle(code: string): string {
  const titles: Record<string, string> = {
    INVALID_REQUEST: 'Invalid Request',
    INVALID_TICKER: 'Company Not Found',
    JOB_NOT_FOUND: 'Pipeline Job Not Found',
    COMPANY_NOT_FOUND: 'Company Not Found',
    PROCESSING_IN_PROGRESS: 'Processing Not Complete',
    RATE_LIMIT_EXCEEDED: 'Too Many Requests',
    DAYTONA_UNAVAILABLE: 'Service Temporarily Unavailable',
    LLM_API_ERROR: 'AI Analysis Error',
    PARSING_ERROR: '10-K Processing Error',
    NETWORK_ERROR: 'Connection Error',
  };

  return titles[code] || 'Error';
}

// ============================================================================
// ERROR MESSAGES
// ============================================================================

function getErrorMessage(
  code: string,
  defaultMessage: string,
  details?: Record<string, any>
): string {
  const messages: Record<string, (details?: Record<string, any>) => string> = {
    INVALID_TICKER: (details) => {
      const ticker = details?.ticker || 'Unknown';
      const available = details?.valid_tickers
        ? ` Available tickers: ${details.valid_tickers.slice(0, 5).join(', ')}...`
        : '';
      return `The company ticker "${ticker}" was not found.${available}`;
    },

    JOB_NOT_FOUND: (details) => {
      const jobId = details?.job_id || 'Unknown';
      return `Pipeline job "${jobId}" not found. It may have expired or been deleted.`;
    },

    COMPANY_NOT_FOUND: (details) => {
      const ticker = details?.ticker || 'Unknown';
      return `No data available for "${ticker}". Please run the pipeline first.`;
    },

    PROCESSING_IN_PROGRESS: (details) => {
      const percentage = details?.percentage || 0;
      return `The pipeline is still processing (${percentage}% complete). Please wait for it to finish.`;
    },

    RATE_LIMIT_EXCEEDED: (details) => {
      const retryAfter = details?.retry_after_seconds || 60;
      return `You've made too many requests. Please wait ${retryAfter} seconds before trying again.`;
    },

    DAYTONA_UNAVAILABLE: () =>
      'The processing service is temporarily unavailable. Our team has been notified.',

    LLM_API_ERROR: () =>
      'The AI analysis service encountered an error. This is usually temporary.',

    PARSING_ERROR: (details) => {
      const ticker = details?.ticker || 'the company';
      return `Failed to process the 10-K filing for ${ticker}. The file may be corrupted or in an unsupported format.`;
    },

    NETWORK_ERROR: () =>
      'Unable to connect to the server. Please check your internet connection.',

    INVALID_REQUEST: () =>
      'The request contains invalid data. Please check your input and try again.',
  };

  const messageFunc = messages[code];
  return messageFunc ? messageFunc(details) : defaultMessage;
}

// ============================================================================
// ERROR ACTIONS
// ============================================================================

function getErrorAction(code: string): string | undefined {
  const actions: Record<string, string> = {
    INVALID_TICKER: 'Please check the ticker symbol and try again.',
    JOB_NOT_FOUND: 'Start a new pipeline or check your recent jobs.',
    COMPANY_NOT_FOUND: 'Run the pipeline for this company first.',
    PROCESSING_IN_PROGRESS: 'Wait for the current pipeline to complete.',
    RATE_LIMIT_EXCEEDED: 'Please wait a moment before trying again.',
    DAYTONA_UNAVAILABLE: 'Try again in a few minutes.',
    LLM_API_ERROR: 'Try again in a moment.',
    PARSING_ERROR: 'Try a different company or contact support.',
    NETWORK_ERROR: 'Check your connection and try again.',
  };

  return actions[code];
}

// ============================================================================
// ERROR LOGGING
// ============================================================================

export function logError(
  error: unknown,
  context?: {
    component?: string;
    action?: string;
    metadata?: Record<string, any>;
  }
) {
  const timestamp = new Date().toISOString();

  console.group(`🔴 Error [${timestamp}]`);

  if (context?.component) {
    console.log('Component:', context.component);
  }

  if (context?.action) {
    console.log('Action:', context.action);
  }

  if (context?.metadata) {
    console.log('Metadata:', context.metadata);
  }

  if (error instanceof APIError) {
    console.log('API Error Code:', error.code);
    console.log('Message:', error.message);
    console.log('Details:', error.details);
  } else if (error instanceof Error) {
    console.log('Error Type:', error.name);
    console.log('Message:', error.message);
    console.log('Stack:', error.stack);
  } else {
    console.log('Unknown Error:', error);
  }

  console.groupEnd();

  // In production, you might send this to a logging service like Sentry
  if (import.meta.env.PROD) {
    // Example: Sentry.captureException(error, { contexts: { custom: context } });
  }
}

// ============================================================================
// ERROR BOUNDARY HELPERS
// ============================================================================

export function isRetryableError(error: unknown): boolean {
  if (error instanceof APIError) {
    const retryableCodes = [
      'NETWORK_ERROR',
      'RATE_LIMIT_EXCEEDED',
      'DAYTONA_UNAVAILABLE',
      'LLM_API_ERROR',
    ];
    return retryableCodes.includes(error.code);
  }

  return false;
}

export function getRetryDelay(error: unknown, attempt: number = 1): number {
  if (error instanceof APIError && error.code === 'RATE_LIMIT_EXCEEDED') {
    return (error.details?.retry_after_seconds || 60) * 1000;
  }

  // Exponential backoff: 1s, 2s, 4s, 8s, 16s (max)
  return Math.min(1000 * Math.pow(2, attempt - 1), 16000);
}

// ============================================================================
// VALIDATION ERROR FORMATTING
// ============================================================================

export function formatValidationErrors(errors: Record<string, string[]>): string {
  const messages = Object.entries(errors).map(([field, fieldErrors]) => {
    return `${field}: ${fieldErrors.join(', ')}`;
  });

  return messages.join('; ');
}

// ============================================================================
// TOAST NOTIFICATION HELPERS
// ============================================================================

export interface ToastOptions {
  title: string;
  description?: string;
  variant?: 'default' | 'destructive' | 'success';
  duration?: number;
}

export function errorToToast(error: unknown): ToastOptions {
  const friendlyError = handleAPIError(error);

  return {
    title: friendlyError.title,
    description: friendlyError.message,
    variant: 'destructive',
    duration: 5000,
  };
}

// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/*
// Example 1: Handle API error in component
async function fetchCompany(ticker: string) {
  try {
    const company = await api.getCompany(ticker);
    return company;
  } catch (error) {
    const userError = handleAPIError(error);
    toast({
      title: userError.title,
      description: userError.message,
      variant: "destructive",
    });

    logError(error, {
      component: "CompanyDetail",
      action: "fetchCompany",
      metadata: { ticker },
    });
  }
}

// Example 2: With toast helper
async function startPipeline(tickers: string[]) {
  try {
    await api.startPipeline({ company_tickers: tickers });
  } catch (error) {
    toast(errorToToast(error));
  }
}

// Example 3: Retry logic
async function fetchWithRetry(ticker: string, maxAttempts = 3) {
  let attempt = 1;

  while (attempt <= maxAttempts) {
    try {
      return await api.getCompany(ticker);
    } catch (error) {
      if (!isRetryableError(error) || attempt === maxAttempts) {
        throw error;
      }

      const delay = getRetryDelay(error, attempt);
      console.log(`Retry attempt ${attempt} after ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
      attempt++;
    }
  }
}

// Example 4: Validation errors
const validationErrors = {
  tickers: ["At least one ticker is required", "INVALID is not a valid ticker"],
  email: ["Email format is invalid"],
};

const errorMessage = formatValidationErrors(validationErrors);
// "tickers: At least one ticker is required, INVALID is not a valid ticker; email: Email format is invalid"
*/
