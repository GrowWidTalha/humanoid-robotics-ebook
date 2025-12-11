/**
 * CustomHero component for the landing page.
 *
 * This component displays the main hero section with a title, subtitle,
 * and call-to-action buttons.
 */
import React from 'react';
import Link from '@docusaurus/Link';
import styles from './LandingPage.module.css';

export function CustomHero() {
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
          <Link
            className={`button button--secondary button--lg ${styles.heroButton}`}
            to="/auth/signup">
            Get Started with AI
          </Link>
        </div>
      </div>
    </div>
  );
}
