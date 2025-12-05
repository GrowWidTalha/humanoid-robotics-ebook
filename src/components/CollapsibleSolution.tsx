import React, {useState} from 'react';

interface CollapsibleSolutionProps {
  children: React.ReactNode;
}

/**
 * CollapsibleSolution component hides exercise solutions by default
 * to prevent accidental spoilers. Readers click to reveal.
 */
export default function CollapsibleSolution({
  children,
}: CollapsibleSolutionProps): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSolution = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="collapsible-solution">
      <button
        className="collapsible-solution-button"
        onClick={toggleSolution}
        aria-expanded={isOpen}
        aria-controls="solution-content"
        type="button"
      >
        <span>{isOpen ? '▼' : '▶'}</span>
        <span>{isOpen ? 'Hide Solution' : 'Show Solution'}</span>
      </button>
      {isOpen && (
        <div
          id="solution-content"
          className="collapsible-solution-content"
          role="region"
          aria-label="Exercise solution"
        >
          {children}
        </div>
      )}
    </div>
  );
}
