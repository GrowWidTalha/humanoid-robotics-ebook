/**
 * UserDropdown component for authenticated user menu
 *
 * T025-T032: Displays user information and provides logout functionality
 * Shows user's name or email with a dropdown menu
 */
import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import styles from './UserDropdown.module.css';

export function UserDropdown() {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // T028: Display user.name or user.email
  const displayName = user?.name || user?.email || 'User';

  // T030: Handle logout
  const handleLogout = async () => {
    setIsOpen(false);
    try {
      await logout();
      // Redirect will be handled by navbar update or page component
    } catch (error) {
      console.error('[UserDropdown] Logout failed:', error);
    }
  };

  // T026: Toggle dropdown open/closed
  const toggleDropdown = () => {
    setIsOpen(prev => !prev);
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  // T031: Keyboard navigation support
  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Escape') {
      setIsOpen(false);
    } else if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      toggleDropdown();
    }
  };

  return (
    <div className={styles.userDropdown} ref={dropdownRef}>
      {/* T028: Dropdown trigger button */}
      <button
        className={styles.userButton}
        onClick={toggleDropdown}
        onKeyDown={handleKeyDown}
        aria-expanded={isOpen}
        aria-haspopup="true"
        aria-label={`User menu for ${displayName}`}
      >
        <span className={styles.userIcon} aria-hidden="true">👤</span>
        <span className={styles.userName}>{displayName}</span>
        <span className={styles.dropdownArrow} aria-hidden="true">▼</span>
      </button>

      {/* T029: Dropdown menu */}
      {isOpen && (
        <div
          className={styles.dropdownMenu}
          role="menu"
          aria-label="User menu"
        >
          <div className={styles.userInfo}>
            <span className={styles.userEmail}>{user?.email}</span>
          </div>
          <div className={styles.divider} />
          <button
            className={styles.logoutButton}
            onClick={handleLogout}
            role="menuitem"
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
}
