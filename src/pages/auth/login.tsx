/**
 * Login page component
 *
 * Renders the login form and provides navigation to signup page.
 */
import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useHistory } from '@docusaurus/router';
import Layout from '@theme/Layout';
import { LoginForm } from '@site/src/components/Auth/LoginForm';

export default function LoginPage() {
  const history = useHistory();
  const baseUrl = useBaseUrl();

  const handleSuccess = () => {
    // Redirect to home page after successful login
    window.location.href = baseUrl;
  };

  const handleSwitchToSignup = () => {
    history.push('/auth/signup');
  };

  return (
    <Layout title="Sign In" description="Sign in to access the chatbot">
      <LoginForm
        onSuccess={handleSuccess}
        onSwitchToSignup={handleSwitchToSignup}
      />
    </Layout>
  );
}
