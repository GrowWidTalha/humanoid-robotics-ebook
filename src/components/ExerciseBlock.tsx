import React from 'react';

interface ExerciseBlockProps {
  number: number;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  objective?: string;
  children: React.ReactNode;
}

/**
 * ExerciseBlock component wraps exercises with metadata
 * (number, difficulty, related objective) for structured practice.
 */
export default function ExerciseBlock({
  number,
  difficulty,
  objective,
  children,
}: ExerciseBlockProps): JSX.Element {
  const difficultyColors = {
    beginner: '#4CAF50',
    intermediate: '#FF9800',
    advanced: '#F44336',
  };

  const difficultyColor = difficultyColors[difficulty];

  return (
    <div className="exercise-block">
      <div className="exercise-header">
        <span style={{fontSize: '1.25rem', fontWeight: 'bold'}}>
          Exercise {number}
        </span>
        <span
          className="exercise-difficulty"
          style={{
            backgroundColor: difficultyColor,
            color: 'white',
          }}
        >
          {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
        </span>
      </div>
      {objective && (
        <div style={{marginBottom: '1rem', fontStyle: 'italic', color: 'var(--ifm-color-emphasis-700)'}}>
          <strong>Learning Objective:</strong> {objective}
        </div>
      )}
      <div>{children}</div>
    </div>
  );
}
