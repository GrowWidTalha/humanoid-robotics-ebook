/**
 * useChatbotControl hook for chatbot expansion state management
 *
 * Provides global chatbot control state for programmatic expansion/collapse.
 * Allows components like CustomHero button to expand the chatbot.
 */
import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';

const ChatbotControlContext = createContext<ChatbotControlContextType | undefined>(undefined);

export type ChatbotControlContextType = {
  isExpanded: boolean;
  setIsExpanded: (expanded: boolean) => void;
  toggleExpanded: () => void;
};

/**
 * T017: ChatbotControlProvider component
 * Provides chatbot expansion state to the entire application
 */
export function ChatbotControlProvider({ children }: { children: React.ReactNode }) {
  const [isExpanded, setIsExpanded] = useState(true); // Default: expanded

  const toggleExpanded = useCallback(() => {
    setIsExpanded(prev => !prev);
  }, []);

  const value = useMemo(
    () => ({ isExpanded, setIsExpanded, toggleExpanded }),
    [isExpanded, toggleExpanded]
  );

  return (
    <ChatbotControlContext.Provider value={value}>
      {children}
    </ChatbotControlContext.Provider>
  );
}

/**
 * T018: useChatbotControl hook
 * Access chatbot control state from any component
 * Throws error if used outside ChatbotControlProvider
 */
export function useChatbotControl() {
  const context = useContext(ChatbotControlContext);
  if (context === undefined) {
    throw new Error('useChatbotControl must be used within a ChatbotControlProvider');
  }
  return context;
}
