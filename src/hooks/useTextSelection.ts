/**
 * useTextSelection hook
 *
 * This hook detects and debounces text selections in the window,
 * providing the selected text and a method to clear it.
 */
import { useState, useEffect, useCallback } from 'react';
import { debounce } from 'lodash';

const DEBOUNCE_DELAY = 300; // ms

export function useTextSelection() {
  const [selectedText, setSelectedText] = useState('');

  const debouncedSetSelectedText = useCallback(
    debounce((selection) => {
      const text = selection.toString().trim();
      if (text.length > 0) {
        setSelectedText(text);
      }
    }, DEBOUNCE_DELAY),
    []
  );

  useEffect(() => {
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      debouncedSetSelectedText(selection);
    };

    document.addEventListener('selectionchange', handleSelectionChange);

    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
      debouncedSetSelectedText.cancel(); // Clean up debounced calls
    };
  }, [debouncedSetSelectedText]);

  const clearSelection = useCallback(() => {
    setSelectedText('');
    window.getSelection()?.removeAllRanges();
  }, []);

  return { selectedText, clearSelection };
}
