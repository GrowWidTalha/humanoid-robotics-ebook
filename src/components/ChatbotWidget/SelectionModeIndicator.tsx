/**
 * SelectionModeIndicator component
 *
 * Displays a visual indicator when chatbot is in text selection mode.
 */
import React from 'react';
import styles from './ChatbotWidget.module.css'; // Assuming styles are in the main widget CSS

interface SelectionModeIndicatorProps {
  selectedText: string;
  onClear: () => void;
}

export function SelectionModeIndicator({ selectedText, onClear }: SelectionModeIndicatorProps) {
  return (
    <div className={styles.selectionIndicator}>
      <div className={styles.selectionInfo}>
        <span className={styles.selectionIcon}>📌</span>
        <span className={styles.selectionText}>
          Querying selected text: "<em>{selectedText.substring(0, 50)}...</em>"
        </span>
      </div>
      <button onClick={onClear} className={styles.clearSelectionButton} title="Clear selection">
        ✕
      </button>
    </div>
  );
}
