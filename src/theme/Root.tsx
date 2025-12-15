/**
 * Root component wrapper for Docusaurus
 *
 * This component wraps the entire app and provides global context providers.
 * It's automatically loaded by Docusaurus as the root of the React tree.
 * Includes the ChatbotWidget for authenticated users.
 *
 * T019: Added ChatbotControlProvider to enable programmatic chatbot control
 * T049-T050: Added AuthPersistenceVerifier to verify auth state persists after login/signup
 * Provider hierarchy: AuthProvider → ChatbotControlProvider → children
 */
import React, { useEffect } from 'react';
import { AuthProvider, useAuth } from '../hooks/useAuth';
import { ChatbotControlProvider } from '../hooks/useChatbotControl';
import { AuthGuard } from '../components/Auth/AuthGuard';
import { ChatbotWidget } from '../components/ChatbotWidget/ChatbotWidget';

/**
 * T049-T050: Component to verify auth state persistence after login/signup
 * Checks sessionStorage flags set by login/signup pages and verifies user is authenticated
 */
function AuthPersistenceVerifier() {
  const { isAuthenticated, isLoading, user } = useAuth();

  useEffect(() => {
    // Only run verification once loading completes
    if (isLoading) return;

    const justLoggedIn = sessionStorage.getItem('auth-just-logged-in');
    const justRegistered = sessionStorage.getItem('auth-just-registered');

    if (justLoggedIn) {
      sessionStorage.removeItem('auth-just-logged-in');
      if (isAuthenticated) {
        console.log('[AuthVerify] ✓ Login persistence verified - user authenticated:', user?.email);
      } else {
        console.error('[AuthVerify] ✗ Login persistence FAILED - expected authenticated user but got null');
      }
    }

    if (justRegistered) {
      sessionStorage.removeItem('auth-just-registered');
      if (isAuthenticated) {
        console.log('[AuthVerify] ✓ Signup persistence verified - user authenticated:', user?.email);
      } else {
        console.error('[AuthVerify] ✗ Signup persistence FAILED - expected authenticated user but got null');
      }
    }
  }, [isLoading, isAuthenticated, user]);

  return null; // This component doesn't render anything
}

export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <ChatbotControlProvider>
        <AuthPersistenceVerifier />
        {children}
        <AuthGuard redirectTo={null} showLoading={false}>
          <ChatbotWidget />
        </AuthGuard>
      </ChatbotControlProvider>
    </AuthProvider>
  );
}
