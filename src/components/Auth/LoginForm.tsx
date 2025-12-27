/**
 * LoginForm component for user authentication
 *
 * Provides email/password login form with validation and error handling.
 * Uses dark theme styling for consistency with the application.
 */
import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import styles from './Auth.module.css';

export function LoginForm({ onSuccess, onSwitchToSignup }) {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(email, password);
      if (onSuccess) {
        onSuccess();
      }
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Invalid email or password';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUseTestCredentials = () => {
    setEmail('test@example.com');
    setPassword('Test123!');
    setError('');
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <h2 className={styles.authTitle}>Welcome Back</h2>
        <p className={styles.authSubtitle}>Sign in to continue learning</p>

        <form onSubmit={handleSubmit} className={styles.authForm}>
          {error && (
            <div className={styles.errorMessage} role="alert">
              {error}
            </div>
          )}

          <div className={styles.formGroup}>
            <label htmlFor="email" className={styles.formLabel}>
              Email Address
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={styles.formInput}
              placeholder="you@example.com"
              required
              autoComplete="email"
              disabled={isLoading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="password" className={styles.formLabel}>
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={styles.formInput}
              placeholder="Enter your password"
              required
              autoComplete="current-password"
              disabled={isLoading}
              minLength={8}
            />
          </div>

          <button
            type="button"
            onClick={handleUseTestCredentials}
            className={styles.testCredentialsButton}
            disabled={isLoading}
          >
            Use Test Credentials
          </button>

          <button
            type="submit"
            className={styles.submitButton}
            disabled={isLoading}
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        {onSwitchToSignup && (
          <p className={styles.switchPrompt}>
            Don't have an account?{' '}
            <button
              type="button"
              onClick={onSwitchToSignup}
              className={styles.switchButton}
            >
              Sign up
            </button>
          </p>
        )}
      </div>
    </div>
  );
}
