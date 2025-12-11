/**
 * ChatbotFeatureShowcase component
 *
 * This component showcases the key features of the RAG chatbot.
 */
import React from 'react';
import styles from './LandingPage.module.css';

const features = [
  {
    title: 'Interactive Learning',
    description: 'Ask questions in natural language and get instant, context-aware answers from the book content.',
    icon: '💬',
  },
  {
    title: 'Deep Content Understanding',
    description: 'Our RAG-powered chatbot understands the nuances of the book, providing accurate and relevant information.',
    icon: '🧠',
  },
  {
    title: 'Query Selected Text',
    description: 'Highlight any text on the page to ask focused questions and get explanations on specific concepts.',
    icon: '📌',
  },
];

export function ChatbotFeatureShowcase() {
  return (
    <div className={styles.featureShowcase}>
      <div className={styles.featureContainer}>
        <div className={styles.featureGrid}>
          {features.map((feature, idx) => (
            <div key={idx} className={styles.featureCard}>
              <div className={styles.featureIcon}>{feature.icon}</div>
              <h3 className={styles.featureTitle}>{feature.title}</h3>
              <p className={styles.featureDescription}>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
