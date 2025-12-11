/**
 * Authentication types shared between frontend and backend
 */

/**
 * User registration request
 */
export interface RegisterRequest {
  email: string;
  password: string;
}

/**
 * User login request
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * User object returned from API
 */
export interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

/**
 * Authentication response with user and session info
 */
export interface AuthResponse {
  user: User;
  message: string;
}

/**
 * Session information
 */
export interface Session {
  id: string;
  user_id: string;
  expires_at: string;
  created_at: string;
}

/**
 * Logout response
 */
export interface LogoutResponse {
  message: string;
}

/**
 * Current user response (for /auth/me endpoint)
 */
export interface CurrentUserResponse {
  user: User;
}
