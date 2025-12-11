/**
 * Signup page component
 *
 * Renders the registration form and provides navigation to login page.
 */
import React from 'react';
import { useHistory } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Layout from '@theme/Layout';
import { SignupForm } from '../../components/Auth/SignupForm';

export default function SignupPage() {
  const history = useHistory();
  const baseUrl = useBaseUrl('/');


  const handleSuccess = () => {
    // Redirect to home page after successful login
    window.location.href = baseUrl;
  };

  const handleSwitchToLogin = () => {
    history.push('/auth/login');
  };

  return (
    <Layout title="Create Account" description="Create an account to access the chatbot">
      <SignupForm
        onSuccess={handleSuccess}
        onSwitchToLogin={handleSwitchToLogin}
      />
    </Layout>
  );
}
