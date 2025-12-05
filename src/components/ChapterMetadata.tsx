import React from 'react';

interface ChapterMetadataProps {
  lastUpdated: string;
  chapter: number;
  readingTime?: number;
}

/**
 * ChapterMetadata component displays last updated date and reading time
 * at the top of each chapter for content freshness transparency.
 */
export default function ChapterMetadata({
  lastUpdated,
  chapter,
  readingTime,
}: ChapterMetadataProps): JSX.Element {
  return (
    <div className="chapter-metadata">
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem'}}>
        <div>
          <strong>Chapter {chapter}</strong>
          {readingTime && (
            <span style={{marginLeft: '1rem', color: 'var(--ifm-color-emphasis-700)'}}>
              📖 ~{readingTime} min read
            </span>
          )}
        </div>
        <div style={{color: 'var(--ifm-color-emphasis-700)', fontSize: '0.9rem'}}>
          Last updated: <time dateTime={lastUpdated}>{lastUpdated}</time>
        </div>
      </div>
    </div>
  );
}
