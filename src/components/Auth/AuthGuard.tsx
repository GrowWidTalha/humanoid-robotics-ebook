/**
 * AuthGuard Higher-Order Component for route protection
 *
 * Redirects unauthenticated users to login page.
 * Shows loading state while checking authentication.
 */
import React, { useEffect } from 'react';
import { useHistory } from '@docusaurus/router';
import { useAuth } from '../../hooks/useAuth';
import styles from './Auth.module.css';

export function AuthGuard({ children, redirectTo = '/auth/login', showLoading = true }) {
  const { isAuthenticated, isLoading } = useAuth();
  const history = useHistory();

  useEffect(() => {
    if (!isLoading && !isAuthenticated && redirectTo) {
      history.push(redirectTo);
    }
  }, [isAuthenticated, isLoading, history, redirectTo]);

  if (isLoading && showLoading) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.loadingSpinner}></div>
        <p className={styles.loadingText}>Checking authentication...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
