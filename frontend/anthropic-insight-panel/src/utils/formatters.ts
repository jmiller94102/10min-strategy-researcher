// Formatting Utilities
// Consistent data formatting across the application

import { formatDistanceToNow, format, parseISO } from 'date-fns';

// ============================================================================
// CURRENCY FORMATTING
// ============================================================================

export function formatCurrency(amount: number, compact: boolean = false): string {
  if (compact) {
    if (amount >= 1_000_000_000) {
      return `$${(amount / 1_000_000_000).toFixed(1)}B`;
    }
    if (amount >= 1_000_000) {
      return `$${(amount / 1_000_000).toFixed(1)}M`;
    }
    if (amount >= 1_000) {
      return `$${(amount / 1_000).toFixed(1)}K`;
    }
    return `$${amount}`;
  }

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

// ============================================================================
// NUMBER FORMATTING
// ============================================================================

export function formatNumber(num: number, compact: boolean = false): string {
  if (compact) {
    if (num >= 1_000_000) {
      return `${(num / 1_000_000).toFixed(1)}M`;
    }
    if (num >= 1_000) {
      return `${(num / 1_000).toFixed(1)}K`;
    }
    return num.toString();
  }

  return new Intl.NumberFormat('en-US').format(num);
}

export function formatPercentage(
  value: number,
  total: number,
  decimals: number = 0
): string {
  if (total === 0) return '0%';
  const percentage = (value / total) * 100;
  return `${percentage.toFixed(decimals)}%`;
}

// ============================================================================
// DATE FORMATTING
// ============================================================================

export function formatDate(dateString: string, formatStr: string = 'MMM d, yyyy'): string {
  try {
    const date = parseISO(dateString);
    return format(date, formatStr);
  } catch (error) {
    console.error('Invalid date string:', dateString);
    return dateString;
  }
}

export function formatRelativeTime(dateString: string): string {
  try {
    const date = parseISO(dateString);
    return formatDistanceToNow(date, { addSuffix: true });
  } catch (error) {
    console.error('Invalid date string:', dateString);
    return dateString;
  }
}

export function formatDateTime(dateString: string): string {
  return formatDate(dateString, 'MMM d, yyyy h:mm a');
}

// ============================================================================
// TIME DURATION FORMATTING
// ============================================================================

export function formatDuration(seconds: number): string {
  if (seconds < 60) {
    return `${Math.floor(seconds)}s`;
  }

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);

  if (minutes < 60) {
    return remainingSeconds > 0 ? `${minutes}m ${remainingSeconds}s` : `${minutes}m`;
  }

  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;

  return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
}

// ============================================================================
// TEXT FORMATTING
// ============================================================================

export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength - 3)}...`;
}

export function capitalize(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

export function titleCase(text: string): string {
  return text
    .split('_')
    .map((word) => capitalize(word))
    .join(' ');
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^\w-]+/g, '')
    .replace(/--+/g, '-')
    .replace(/^-+/, '')
    .replace(/-+$/, '');
}

// ============================================================================
// LIST FORMATTING
// ============================================================================

export function formatList(items: string[], maxItems: number = 3): string {
  if (items.length === 0) return 'None';
  if (items.length <= maxItems) {
    return items.join(', ');
  }

  const displayedItems = items.slice(0, maxItems);
  const remaining = items.length - maxItems;
  return `${displayedItems.join(', ')} +${remaining} more`;
}

// ============================================================================
// AI MATURITY LABEL FORMATTING
// ============================================================================

export type MaturityLabel = 'Leader' | 'Fast Follower' | 'Emerging' | 'Laggard';

export function getMaturityColor(label: MaturityLabel): string {
  const colors: Record<MaturityLabel, string> = {
    Leader: 'text-green-600 bg-green-50 border-green-200',
    'Fast Follower': 'text-blue-600 bg-blue-50 border-blue-200',
    Emerging: 'text-yellow-600 bg-yellow-50 border-yellow-200',
    Laggard: 'text-red-600 bg-red-50 border-red-200',
  };
  return colors[label] || 'text-gray-600 bg-gray-50 border-gray-200';
}

export function getMaturityIcon(label: MaturityLabel): string {
  const icons: Record<MaturityLabel, string> = {
    Leader: '🏆',
    'Fast Follower': '🚀',
    Emerging: '🌱',
    Laggard: '⏳',
  };
  return icons[label] || '📊';
}

// ============================================================================
// SCORE FORMATTING
// ============================================================================

export function formatScore(score: number, maxScore: number = 100): string {
  return `${score}/${maxScore}`;
}

export function getScoreColor(score: number, maxScore: number = 100): string {
  const percentage = (score / maxScore) * 100;

  if (percentage >= 80) return 'text-green-600';
  if (percentage >= 60) return 'text-blue-600';
  if (percentage >= 40) return 'text-yellow-600';
  return 'text-red-600';
}

// ============================================================================
// FILE SIZE FORMATTING
// ============================================================================

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
}

// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/*
// Currency
formatCurrency(50000000, true) // "$50.0M"
formatCurrency(50000000, false) // "$50,000,000"

// Numbers
formatNumber(1234567, true) // "1.2M"
formatPercentage(75, 100) // "75%"

// Dates
formatDate("2024-07-30") // "Jul 30, 2024"
formatRelativeTime("2024-07-30T10:00:00Z") // "2 days ago"
formatDuration(185) // "3m 5s"

// Text
truncate("Long text here...", 10) // "Long te..."
titleCase("ai_maturity_score") // "Ai Maturity Score"
formatList(["Python", "Java", "C++", "Go", "Rust"], 3) // "Python, Java, C++ +2 more"

// Maturity
getMaturityColor("Leader") // "text-green-600 bg-green-50 border-green-200"
getMaturityIcon("Leader") // "🏆"
*/
