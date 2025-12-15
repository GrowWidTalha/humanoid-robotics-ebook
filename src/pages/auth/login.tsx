/**
 * Login page component
 *
 * Renders the login form and provides navigation to signup page.
 * T045-T046: Add auth persistence tracking to verify state persists after login
 * T068-T072: Add route protection to redirect authenticated users
 */
import React, { useEffect } from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useHistory } from '@docusaurus/router';
import Layout from '@theme/Layout';
import { LoginForm } from '@site/src/components/Auth/LoginForm';
import { useAuth } from '@site/src/hooks/useAuth';

export default function LoginPage() {
  const history = useHistory();
  const baseUrl = useBaseUrl("/");
  // T068-T069: Import useAuth and check authentication status
  const { isAuthenticated, isLoading } = useAuth();

  // T070: Redirect authenticated users to home page
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      console.log('[Login] User already authenticated, redirecting to home');
      history.push(baseUrl);
    }
  }, [isAuthenticated, isLoading, history, baseUrl]);

  const handleSuccess = () => {
    console.log('[Login] handleSuccess - user logged in');
    console.log('[Login] baseUrl:', baseUrl);

    // T045: Mark auth state as should-persist before redirect
    sessionStorage.setItem('auth-just-logged-in', 'true');
    console.log('[Login] Set auth-just-logged-in flag, redirecting to:', baseUrl);

    // T046: Full page redirect to home - forces auth state check from scratch
    // This verifies that /auth/me properly returns user data with HTTP-only cookies
    window.location.href = baseUrl;
  };

  const handleSwitchToSignup = () => {
    history.push('/auth/signup');
  };

  // T071: Return null while redirecting (don't show login form to authenticated users)
  if (!isLoading && isAuthenticated) {
    return null;
  }

  return (
    <Layout title="Sign In" description="Sign in to access the chatbot">
      <LoginForm
        onSuccess={handleSuccess}
        onSwitchToSignup={handleSwitchToSignup}
      />
    </Layout>
  );
}
