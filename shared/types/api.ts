/**
 * Generic API types shared between frontend and backend
 */

/**
 * Standard API error response
 */
export interface ApiError {
  error: string;
  message: string;
  details?: any;
}

/**
 * Health check response
 */
export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  environment: string;
  dependencies: {
    [key: string]: 'healthy' | 'unhealthy';
  };
}

/**
 * Pagination parameters
 */
export interface PaginationParams {
  limit?: number;
  offset?: number;
}

/**
 * Paginated response wrapper
 */
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  limit: number;
  offset: number;
}

/**
 * API response wrapper for success cases
 */
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

/**
 * Rate limit error response
 */
export interface RateLimitError extends ApiError {
  retry_after: number;  // Seconds until rate limit resets
}
