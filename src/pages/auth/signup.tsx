/**
 * Signup page component
 *
 * Renders the registration form and provides navigation to login page.
 * T047-T048: Add auth persistence tracking to verify state persists after signup
 * T073-T077: Add route protection to redirect authenticated users
 */
import React, { useEffect } from 'react';
import { useHistory } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Layout from '@theme/Layout';
import { SignupForm } from '../../components/Auth/SignupForm';
import { useAuth } from '@site/src/hooks/useAuth';

export default function SignupPage() {
  const history = useHistory();
  const baseUrl = useBaseUrl('/');
  console.log('[Signup] baseUrl:', baseUrl);
  // T073-T074: Import useAuth and check authentication status
  const { isAuthenticated, isLoading } = useAuth();

  // T075: Redirect authenticated users to home page
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      console.log('[Signup] User already authenticated, redirecting to home');
      history.push(baseUrl);
    }
  }, [isAuthenticated, isLoading, history, baseUrl]);

  const handleSuccess = () => {
    console.log('[Signup] handleSuccess - user registered');

    // T047: Mark auth state as should-persist before redirect
    sessionStorage.setItem('auth-just-registered', 'true');
    console.log('[Signup] Set auth-just-registered flag, redirecting to:', baseUrl);

    // T048: Full page redirect to home - forces auth state check from scratch
    // This verifies that /auth/me properly returns user data with HTTP-only cookies
    window.location.href = baseUrl;
  };

  const handleSwitchToLogin = () => {
    history.push('/auth/login');
  };

  // T076: Return null while redirecting (don't show signup form to authenticated users)
  if (!isLoading && isAuthenticated) {
    return null;
  }

  return (
    <Layout title="Create Account" description="Create an account to access the chatbot">
      <SignupForm
        onSuccess={handleSuccess}
        onSwitchToLogin={handleSwitchToLogin}
      />
    </Layout>
  );
}
