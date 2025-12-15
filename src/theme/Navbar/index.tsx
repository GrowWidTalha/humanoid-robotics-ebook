/**
 * Swizzled Navbar component wrapper
 *
 * T021-T024: Wraps the original Docusaurus Navbar to add auth-aware menu items
 * T022: Import useAuth hook
 * T023: Add conditional rendering logic
 * T024: Preserve all existing Docusaurus navbar functionality
 * T033: Integrate UserDropdown component
 */
import React from 'react';
import Navbar from '@theme-original/Navbar';
import { useAuth } from '@site/src/hooks/useAuth';
import { UserDropdown } from '@site/src/components/Navbar/UserDropdown';
import Link from '@docusaurus/Link';

type Props = any; // Use any for Docusaurus wrapper props to avoid type definition issues

export default function NavbarWrapper(props: Props): JSX.Element {
  const { isAuthenticated, isLoading } = useAuth();

  return (
    <>
      {/* T024: Render original Docusaurus Navbar with all its functionality */}
      <Navbar {...props} />

      {/* T023: Add auth-aware menu items to the right side of navbar */}
      {!isLoading && (
        <div style={{
          position: 'fixed',
          top: '0',
          right: '1rem',
          height: 'var(--ifm-navbar-height)',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
          zIndex: 100,
          pointerEvents: 'none'
        }}>
          <div style={{ pointerEvents: 'auto' }}>
            {!isAuthenticated ? (
              // Show auth links when not authenticated
              <>
                <Link
                  to="/auth/login"
                  style={{
                    padding: '0.375rem 0.875rem',
                    marginRight: '0.5rem',
                    color: 'var(--ifm-navbar-link-color)',
                    textDecoration: 'none',
                    borderRadius: 'var(--ifm-global-radius)',
                    transition: 'all 0.2s ease',
                    display: 'inline-block'
                  }}
                  className="navbar-auth-link"
                >
                  Login
                </Link>
                <Link
                  to="/auth/signup"
                  style={{
                    padding: '0.375rem 0.875rem',
                    backgroundColor: 'var(--ifm-color-primary)',
                    color: 'white',
                    textDecoration: 'none',
                    borderRadius: 'var(--ifm-global-radius)',
                    transition: 'background-color 0.2s ease',
                    display: 'inline-block'
                  }}
                  className="navbar-signup-button"
                >
                  Sign Up
                </Link>
              </>
            ) : (
              // T033: Show UserDropdown when authenticated
              <UserDropdown />
            )}
          </div>
        </div>
      )}
    </>
  );
}
