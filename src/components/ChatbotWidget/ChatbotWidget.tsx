/**
 * ChatbotWidget component
 *
 * Main chatbot interface with message list, input, and RAG-powered responses.
 */
import React, { useState, useRef, useEffect } from 'react';
import { useChatbot } from '../../hooks/useChatbot';
import { useTextSelection } from '../../hooks/useTextSelection';
import { SelectionModeIndicator } from './SelectionModeIndicator';
import styles from './ChatbotWidget.module.css';

export function ChatbotWidget() {
  const [inputValue, setInputValue] = useState('');
  const [isExpanded, setIsExpanded] = useState(true);
  const messagesEndRef = useRef(null);

  const {
    messages,
    isLoading,
    error,
    sendMessage,
    clearChat
  } = useChatbot();

  const { selectedText, clearSelection } = useTextSelection();

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const queryMode = selectedText ? 'selection' : 'full_book';
    await sendMessage(inputValue.trim(), queryMode, selectedText);
    
    setInputValue('');
    if (queryMode === 'selection') {
      clearSelection();
    }
  };

  const handleClearSelection = () => {
    clearSelection();
  };

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  if (!isExpanded) {
    // Collapsed state - floating button
    return (
      <button
        className={styles.floatingButton}
        onClick={toggleExpanded}
        aria-label="Open AI Assistant chatbot"
        aria-expanded={false}>
        <span className={styles.chatIcon} aria-hidden="true">💬</span>
        <span className={styles.buttonText}>Ask AI</span>
      </button>
    );
  }

  return (
    <div className={styles.chatbotContainer} role="complementary" aria-label="AI Assistant">
      <div className={styles.chatbotHeader}>
        <h3 className={styles.chatbotTitle} id="chatbot-title">Robotics AI Assistant</h3>
        <div className={styles.headerButtons}>
          <button
            onClick={() => {
              clearChat();
              clearSelection();
            }}
            className={styles.clearButton}
            aria-label="Start new conversation"
            title="New conversation"
          >
            <span aria-hidden="true">✨</span>
          </button>
          <button
            onClick={toggleExpanded}
            className={styles.closeButton}
            aria-label="Minimize chatbot"
            title="Minimize"
          >
            ✕
          </button>
        </div>
      </div>

      {selectedText && (
        <SelectionModeIndicator
          selectedText={selectedText}
          onClear={handleClearSelection}
        />
      )}

      <div
        className={styles.messagesContainer}
        role="log"
        aria-live="polite"
        aria-atomic="false"
        aria-relevant="additions"
        aria-label="Chat conversation"
      >
        {messages.length === 0 && !selectedText && (
          <div className={styles.emptyState} role="status">
            <p>👋 Hi! I'm your AI assistant for humanoid robotics.</p>
            <p>Ask me anything about ROS 2, digital twins, AI, or robotics, or select text on any page to ask a question about it.</p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`${styles.message} ${styles[message.role]}`}
            role="article"
            aria-label={`Chat message from ${message.role === 'user' ? 'you' : 'AI assistant'}`}
          >
            <div className={styles.messageContent}>
              {message.content}
            </div>
            {message.metadata?.query_mode === 'selection' && (
              <div className={styles.selectionBadge} aria-label="This was a selection-based query">
                <span aria-hidden="true">📌</span> Selection query
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className={`${styles.message} ${styles.assistant}`} role="status" aria-label="AI assistant is typing">
            <div className={styles.typingIndicator} aria-hidden="true">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        {error && (
          <div className={styles.errorMessage} role="alert" aria-live="assertive">
            <span aria-hidden="true">⚠️</span> {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className={styles.inputForm} role="search">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={selectedText ? "Ask about the selected text..." : "Ask a question..."}
          className={styles.input}
          disabled={isLoading}
          aria-label={selectedText ? "Ask a question about the selected text" : "Ask a question about robotics"}
          aria-describedby="chatbot-title"
        />
        <button
          type="submit"
          className={styles.sendButton}
          disabled={!inputValue.trim() || isLoading}
          aria-label={isLoading ? "Sending message..." : "Send message"}
        >
          <span aria-hidden="true">{isLoading ? '⏳' : '➤'}</span>
        </button>
      </form>
    </div>
  );
}
