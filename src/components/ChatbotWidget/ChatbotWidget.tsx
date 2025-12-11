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
      <div className={styles.floatingButton} onClick={toggleExpanded}>
        <span className={styles.chatIcon}>💬</span>
        <span className={styles.buttonText}>Ask AI</span>
      </div>
    );
  }

  return (
    <div className={styles.chatbotContainer}>
      <div className={styles.chatbotHeader}>
        <h3 className={styles.chatbotTitle}>Robotics AI Assistant</h3>
        <div className={styles.headerButtons}>
          <button
            onClick={() => {
              clearChat();
              clearSelection();
            }}
            className={styles.clearButton}
            title="New conversation"
          >
            ✨
          </button>
          <button
            onClick={toggleExpanded}
            className={styles.closeButton}
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

      <div className={styles.messagesContainer}>
        {messages.length === 0 && !selectedText && (
          <div className={styles.emptyState}>
            <p>👋 Hi! I'm your AI assistant for humanoid robotics.</p>
            <p>Ask me anything about ROS 2, digital twins, AI, or robotics, or select text on any page to ask a question about it.</p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`${styles.message} ${styles[message.role]}`}
          >
            <div className={styles.messageContent}>
              {message.content}
            </div>
            {message.metadata?.query_mode === 'selection' && (
              <div className={styles.selectionBadge}>
                📌 Selection query
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className={`${styles.message} ${styles.assistant}`}>
            <div className={styles.typingIndicator}>
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        {error && (
          <div className={styles.errorMessage}>
            ⚠️ {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className={styles.inputForm}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={selectedText ? "Ask about the selected text..." : "Ask a question..."}
          className={styles.input}
          disabled={isLoading}
        />
        <button
          type="submit"
          className={styles.sendButton}
          disabled={!inputValue.trim() || isLoading}
        >
          {isLoading ? '⏳' : '➤'}
        </button>
      </form>
    </div>
  );
}
