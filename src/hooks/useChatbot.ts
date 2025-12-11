/**
 * useChatbot hook for chat state management
 *
 * Manages chat messages, thread state, and communication with the backend API.
 */
import { useState, useCallback, useEffect } from 'react';
import apiClient from '../services/apiClient';

export function useChatbot() {
  const [messages, setMessages] = useState([]);
  const [threadId, setThreadId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Send a message to the chatbot
   */
  const sendMessage = useCallback(async (messageContent, queryMode = 'full_book', selectedText = null) => {
    setIsLoading(true);
    setError(null);

    // Optimistically add user message
    const tempUserMessage = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: messageContent,
      created_at: new Date().toISOString(),
      metadata: {
        query_mode: queryMode,
        selected_text: selectedText
      }
    };
    setMessages(prev => [...prev, tempUserMessage]);

    try {
      const response = await apiClient.post('/chat/message', {
        message: messageContent,
        thread_id: threadId,
        query_mode: queryMode,
        selected_text: selectedText
      });

      const { user_message, assistant_message, thread_id: newThreadId } = response.data;

      // Update thread ID if new
      if (!threadId) {
        setThreadId(newThreadId);
      }

      // Replace temp message with actual messages
      setMessages(prev => {
        const withoutTemp = prev.filter(msg => msg.id !== tempUserMessage.id);
        return [...withoutTemp, user_message, assistant_message];
      });

    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send message');
      // Remove optimistic message on error
      setMessages(prev => prev.filter(msg => msg.id !== tempUserMessage.id));
    } finally {
      setIsLoading(false);
    }
  }, [threadId]);

  /**
   * Load chat history for a thread
   */
  const loadHistory = useCallback(async (loadThreadId) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await apiClient.get(`/chat/history/${loadThreadId}`);
      setMessages(response.data.messages);
      setThreadId(loadThreadId);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load history');
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Clear current chat and start fresh
   */
  const clearChat = useCallback(() => {
    setMessages([]);
    setThreadId(null);
    setError(null);
  }, []);

  // Effect to load history on initial mount if a threadId is available
  useEffect(() => {
    // TODO: Implement logic to get initial threadId (e.g., from URL or local storage)
    const initialThreadId = null; 
    if (initialThreadId) {
      loadHistory(initialThreadId);
    }
  }, [loadHistory]);


  return {
    messages,
    threadId,
    isLoading,
    error,
    sendMessage,
    loadHistory,
    clearChat
  };
}
