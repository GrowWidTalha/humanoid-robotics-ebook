/**
 * useAuth hook for authentication state management
 *
 * Provides authentication context and functions for login, logout, and registration.
 * Persists user state across the application using React Context.
 *
 * T040-T044: Enhanced with retry logic and persistence improvements
 */
import React, { createContext, useContext, useState, useEffect, useRef, useCallback, useMemo } from 'react';
import * as authService from '../services/authService';
import { User } from '@auth/core/types';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export type AuthContextType = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  // T043: Track pending auth checks for cleanup
  const abortControllerRef = useRef<AbortController | null>(null);
  const isMountedRef = useRef(true);

  // T043: Cleanup on unmount
  useEffect(() => {
    return () => {
      isMountedRef.current = false;
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  // Check authentication status on mount
  useEffect(() => {
    refreshUser();
  }, []);

  // T010: Add timeout safeguard to prevent isLoading stuck at true
  useEffect(() => {
    const timeout = setTimeout(() => {
      if (isLoading) {
        console.warn('[Auth] Auth check timeout after 10 seconds, forcing isLoading = false');
        setIsLoading(false);
      }
    }, 10000);

    return () => clearTimeout(timeout);
  }, [isLoading]);

  // T040-T041: Add retry logic for /auth/me failures with exponential backoff
  const refreshUser = useCallback(async (retryCount = 0) => {
    const MAX_RETRIES = 3;
    const RETRY_DELAYS = [1000, 2000, 4000]; // exponential backoff: 1s, 2s, 4s

    // T043: Cancel any pending auth check
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    setIsLoading(true);
    try {
      const currentUser = await authService.getCurrentUser();
      // T012: Add debug logging
      console.log('[Auth] refreshUser result:', currentUser ? 'authenticated' : 'not authenticated');

      // T042: Only update state if component is still mounted
      if (isMountedRef.current) {
        setUser(currentUser);
      }
    } catch (error) {
      // T009: Enhanced error handling with more context
      console.error('[Auth] Failed to get current user:', error);
      console.error('[Auth] Error details:', {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        retryAttempt: retryCount + 1
      });

      // T040: Retry logic for network errors (not 401/403)
      const isNetworkError = !error.response || (error.response.status >= 500);
      const shouldRetry = isNetworkError && retryCount < MAX_RETRIES;

      if (shouldRetry && isMountedRef.current) {
        const delay = RETRY_DELAYS[retryCount];
        console.log(`[Auth] Retrying in ${delay}ms (attempt ${retryCount + 1}/${MAX_RETRIES})`);

        setTimeout(() => {
          if (isMountedRef.current) {
            refreshUser(retryCount + 1);
          }
        }, delay);
        return; // Don't set user to null yet, keep retrying
      }

      // T042: Only update state if component is still mounted
      if (isMountedRef.current) {
        setUser(null);
      }
    } finally {
      // T042: Only update loading state if component is still mounted
      if (isMountedRef.current) {
        setIsLoading(false);
      }
      abortControllerRef.current = null;
    }
  }, []);

  const login = useCallback(async (email, password) => {
    setIsLoading(true);
    try {
      const response = await authService.login(email, password);
      setUser(response.user);
    } catch (error) {
      setIsLoading(false);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const register = useCallback(async (email, password) => {
    setIsLoading(true);
    try {
      const response = await authService.register(email, password);
      setUser(response.user);
    } catch (error) {
      setIsLoading(false);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    setIsLoading(true);
    try {
      await authService.logout();
      setUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // T044: Use useMemo to ensure AuthContext updates trigger re-renders
  // This guarantees that any consumer component will re-render when auth state changes
  const value = useMemo(
    () => ({
      user,
      isAuthenticated: user !== null,
      isLoading,
      login,
      register,
      logout,
      refreshUser,
    }),
    [user, isLoading, login, register, logout, refreshUser]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
