/**
 * Root component wrapper for Docusaurus
 *
 * This component wraps the entire app and provides global context providers.
 * It's automatically loaded by Docusaurus as the root of the React tree.
 * Includes the ChatbotWidget for authenticated users.
 */
import React from 'react';
import { AuthProvider } from '../hooks/useAuth';
import { AuthGuard } from '../components/Auth/AuthGuard';
import { ChatbotWidget } from '../components/ChatbotWidget/ChatbotWidget';

export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      {children}
      <AuthGuard redirectTo={null} showLoading={false}>
        <ChatbotWidget />
      </AuthGuard>
    </AuthProvider>
  );
}
