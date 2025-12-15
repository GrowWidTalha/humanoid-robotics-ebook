/**
 * CustomHero component for the landing page.
 *
 * This component displays the main hero section with a title, subtitle,
 * and call-to-action buttons.
 * T085-T092: Smart "Get Started with AI" button that expands chatbot for authenticated users
 */
import React from 'react';
import Link from '@docusaurus/Link';
import { useHistory } from '@docusaurus/router';
import { useAuth } from '../../hooks/useAuth';
import { useChatbotControl } from '../../hooks/useChatbotControl';
import styles from './LandingPage.module.css';

export function CustomHero() {
  // T085-T086: Import hooks for auth state and chatbot control
  const { isAuthenticated } = useAuth();
  const { setIsExpanded } = useChatbotControl();
  const history = useHistory();

  // T088: Handle "Get Started with AI" button click with context-aware behavior
  const handleGetStarted = () => {
    if (!isAuthenticated) {
      // T089: Not authenticated → navigate to signup
      history.push('/auth/signup');
    } else {
      // T090: Authenticated → expand chatbot
      setIsExpanded(true);
    }
  };

  return (
    <div className={styles.heroBanner}>
      <div className={styles.heroContainer}>
        <h1 className={styles.heroTitle}>The Future of AI is Embodied</h1>
        <p className={styles.heroSubtitle}>
          An open-source textbook on the software and hardware for building, training, and deploying
          the next generation of autonomous humanoid robots.
        </p>
        <div className={styles.buttons}>
          <Link
            className={`button button--primary button--lg ${styles.heroButton}`}
            to="/humanoid-robotics-ebook/module1-ros2/chapter1-introduction">
            Start Reading
          </Link>
          {/* T087: Convert Link to button with onClick handler */}
          {/* T091: Preserve button styling to match original Link appearance */}
          <button
            className={`button button--secondary button--lg ${styles.heroButton}`}
            onClick={handleGetStarted}
            aria-label={isAuthenticated ? "Open AI chatbot assistant" : "Sign up to access AI chatbot"}
            type="button">
            Get Started with AI
          </button>
        </div>
      </div>
    </div>
  );
}
