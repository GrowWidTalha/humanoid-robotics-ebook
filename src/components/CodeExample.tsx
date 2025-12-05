import React, {useState} from 'react';
import CodeBlock from '@theme/CodeBlock';

interface CodeExampleProps {
  language: 'python' | 'javascript' | 'typescript' | 'bash';
  title: string;
  code: string;
  expectedOutput?: string;
  explanation?: string;
}

/**
 * CodeExample component displays code with syntax highlighting,
 * copy button, expected output, and explanation.
 */
export default function CodeExample({
  language,
  title,
  code,
  expectedOutput,
  explanation,
}: CodeExampleProps): JSX.Element {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  return (
    <div className="code-example">
      <div className="code-example-header">
        <span>{title}</span>
        <button
          className="code-example-copy-button"
          onClick={handleCopy}
          aria-label="Copy code to clipboard"
          type="button"
        >
          {copied ? '✓ Copied!' : '📋 Copy'}
        </button>
      </div>
      <CodeBlock language={language} showLineNumbers>
        {code}
      </CodeBlock>
      {expectedOutput && (
        <div style={{marginTop: '1rem'}}>
          <strong>Expected Output:</strong>
          <CodeBlock language="plaintext" title="Output">
            {expectedOutput}
          </CodeBlock>
        </div>
      )}
      {explanation && (
        <div className="code-example-explanation">
          <strong>Explanation:</strong> {explanation}
        </div>
      )}
    </div>
  );
}
