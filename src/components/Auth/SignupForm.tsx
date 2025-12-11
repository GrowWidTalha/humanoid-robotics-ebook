/**
 * SignupForm component for user registration
 *
 * Provides email/password registration form with password strength validation.
 * Uses dark theme styling for consistency with the application.
 */
import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import styles from './Auth.module.css';

/**
 * Validate password strength
 */
function validatePasswordStrength(password) {
  if (password.length < 8) {
    return 'Password must be at least 8 characters long';
  }
  if (!/[A-Z]/.test(password)) {
    return 'Password must contain at least one uppercase letter';
  }
  if (!/[a-z]/.test(password)) {
    return 'Password must contain at least one lowercase letter';
  }
  if (!/\d/.test(password)) {
    return 'Password must contain at least one digit';
  }
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    return 'Password must contain at least one special character';
  }
  return null;
}

export function SignupForm({ onSuccess, onSwitchToLogin }) {
  const { register } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    const passwordError = validatePasswordStrength(password);
    if (passwordError) {
      setError(passwordError);
      return;
    }

    setIsLoading(true);

    try {
      await register(email, password);
      if (onSuccess) {
        onSuccess();
      }
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Registration failed. Please try again.';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <h2 className={styles.authTitle}>Create Account</h2>
        <p className={styles.authSubtitle}>Join us to start learning</p>

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
              placeholder="Create a strong password"
              required
              autoComplete="new-password"
              disabled={isLoading}
              minLength={8}
            />
            <p className={styles.formHint}>
              Must be 8+ characters with uppercase, lowercase, number, and special character
            </p>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="confirmPassword" className={styles.formLabel}>
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className={styles.formInput}
              placeholder="Re-enter your password"
              required
              autoComplete="new-password"
              disabled={isLoading}
              minLength={8}
            />
          </div>

          <button
            type="submit"
            className={styles.submitButton}
            disabled={isLoading}
          >
            {isLoading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>

        {onSwitchToLogin && (
          <p className={styles.switchPrompt}>
            Already have an account?{' '}
            <button
              type="button"
              onClick={onSwitchToLogin}
              className={styles.switchButton}
            >
              Sign in
            </button>
          </p>
        )}
      </div>
    </div>
  );
}
