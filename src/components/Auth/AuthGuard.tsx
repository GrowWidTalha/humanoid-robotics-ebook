/**
 * AuthGuard Higher-Order Component for route protection
 *
 * Redirects unauthenticated users to login page.
 * Shows loading state while checking authentication.
 * T058-T060: Enhanced with timeout safeguard and verified behavior for chatbot use case
 */
import React, { useEffect, useState } from 'react';
import { useHistory } from '@docusaurus/router';
import { useAuth } from '../../hooks/useAuth';
import styles from './Auth.module.css';

export function AuthGuard({ children, redirectTo = '/auth/login', showLoading = true }) {
  const { isAuthenticated, isLoading } = useAuth();
  const history = useHistory();
  // T058: Add timeout state to prevent infinite loading
  const [timedOut, setTimedOut] = useState(false);

  useEffect(() => {
    if (!isLoading && !isAuthenticated && redirectTo) {
      history.push(redirectTo);
    }
  }, [isAuthenticated, isLoading, history, redirectTo]);

  // T058: Add 10-second timeout safeguard to prevent infinite loading state
  useEffect(() => {
    const timeout = setTimeout(() => {
      if (isLoading) {
        console.warn('[AuthGuard] Auth check timeout after 10 seconds, treating as not authenticated');
        setTimedOut(true);
      }
    }, 10000);

    return () => clearTimeout(timeout);
  }, [isLoading]);

  // T060: For chatbot use case (showLoading=false, redirectTo=null), return null immediately
  // This ensures no flash of content and chatbot only renders when authenticated
  if (showLoading && (isLoading && !timedOut)) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.loadingSpinner}></div>
        <p className={styles.loadingText}>Checking authentication...</p>
      </div>
    );
  }

  // T059: Return null immediately when not authenticated (no flash of content)
  if (!isAuthenticated || timedOut) {
    return null;
  }

  return <>{children}</>;
}
