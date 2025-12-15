# Data Model: Authentication State Management

**Feature**: 005-fix-auth-state
**Date**: 2025-12-13
**Phase**: Phase 1 - Design

## Overview

This document defines the data structures and state models for the authentication state management feature. Since this is a frontend-focused fix working with existing backend APIs, the data models focus on client-side state representation and UI component state.

## Entity Definitions

### 1. User Entity

Represents an authenticated user in the system.

**Source**: Returned from `/api/auth/me`, `/api/auth/login`, `/api/auth/register` endpoints

**Structure**:
```typescript
interface User {
  id: string;           // Unique user identifier
  email: string;        // User's email address (used for display)
  name?: string;        // Optional display name
  createdAt?: string;   // ISO 8601 timestamp of account creation
}
```

**Validation Rules**:
- `id` must be non-empty string
- `email` must be valid email format
- `name` is optional, defaults to email for display if not provided

**State Transitions**:
- `null` → `User` object: On successful login/signup or auth check
- `User` object → `null`: On logout or auth check failure

**Usage**:
- Stored in AuthContext state
- Displayed in navbar user dropdown
- Used to determine authenticated status

### 2. AuthContextState

Represents the global authentication state in React Context.

**Source**: Managed by `AuthProvider` in `src/hooks/useAuth.tsx`

**Structure**:
```typescript
interface AuthContextState {
  user: User | null;                                    // Current user or null if not authenticated
  isAuthenticated: boolean;                             // Computed: user !== null
  isLoading: boolean;                                   // True during auth check/login/logout
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;                    // Re-check auth status
}
```

**State Transitions**:

```
Initial State:
{ user: null, isAuthenticated: false, isLoading: true }
                    ↓
            [Auth Check Triggered]
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
[Auth Success]            [Auth Failure]
{ user: User,            { user: null,
  isAuthenticated: true,   isAuthenticated: false,
  isLoading: false }       isLoading: false }
        ↓                       ↓
[User Logs Out]           [User Logs In]
        ↓                       ↓
{ user: null,            { user: User,
  isAuthenticated: false,  isAuthenticated: true,
  isLoading: false }       isLoading: false }
```

**Validation Rules**:
- `isAuthenticated` must always equal `user !== null`
- `isLoading` must transition to `false` after auth operations complete
- `isLoading` must become `false` within 5 seconds (timeout safeguard)

**Usage**:
- Consumed by all components needing auth state (Navbar, AuthGuard, ChatbotWidget, etc.)
- Provided at app root in `Root.tsx`

### 3. ChatbotControlState

Represents the chatbot widget control state.

**Source**: Managed by new `ChatbotControlProvider` in `src/hooks/useChatbotControl.tsx`

**Structure**:
```typescript
interface ChatbotControlState {
  isExpanded: boolean;                   // True if chatbot is expanded, false if minimized
  setIsExpanded: (expanded: boolean) => void;  // Function to control chatbot expansion
  toggleExpanded: () => void;            // Toggle function for convenience
}
```

**State Transitions**:
```
Initial State: { isExpanded: true }  // Default to expanded for authenticated users
                    ↓
        [User Clicks Minimize]
                    ↓
        { isExpanded: false }
                    ↓
    [User Clicks "Ask AI" or Floating Button]
                    ↓
        { isExpanded: true }
```

**Validation Rules**:
- `isExpanded` is boolean only
- State persists across page navigations (stored in React Context)
- State resets to `true` on login (optional enhancement)

**Usage**:
- Consumed by `ChatbotWidget` to control its display state
- Consumed by `CustomHero` "Get Started with AI" button
- Provided at app root in `Root.tsx`

### 4. NavbarState (UI State)

Represents the computed state for navbar rendering.

**Source**: Derived from AuthContextState in swizzled Navbar component

**Structure**:
```typescript
interface NavbarState {
  showAuthLinks: boolean;        // Show Login/Signup links
  showUserDropdown: boolean;     // Show user dropdown menu
  displayName: string | null;    // Name to display in dropdown
  isLoading: boolean;            // Show loading indicator
}
```

**Computation Logic**:
```typescript
function computeNavbarState(authState: AuthContextState): NavbarState {
  return {
    showAuthLinks: !authState.isAuthenticated && !authState.isLoading,
    showUserDropdown: authState.isAuthenticated && !authState.isLoading,
    displayName: authState.user?.name || authState.user?.email || null,
    isLoading: authState.isLoading
  };
}
```

**State Transitions**:
```
Loading → Auth Links → User Dropdown → Auth Links
                ↑                           ↓
                └─────[Logout/Session Expire]
```

**Usage**:
- Computed within Navbar component
- Determines which navbar items to render

## Relationships

```
┌─────────────────────────────────────────┐
│         Root Component (App)            │
│  ┌─────────────────────────────────┐   │
│  │      AuthProvider               │   │
│  │  (AuthContextState)             │   │
│  │  - user: User | null            │   │
│  │  - isAuthenticated: boolean     │   │
│  │  - isLoading: boolean           │   │
│  └────────────┬────────────────────┘   │
│               │                         │
│  ┌────────────┴────────────────────┐   │
│  │  ChatbotControlProvider         │   │
│  │  (ChatbotControlState)          │   │
│  │  - isExpanded: boolean          │   │
│  └────────────┬────────────────────┘   │
└───────────────┼─────────────────────────┘
                │
    ┌───────────┼───────────┐
    ↓           ↓           ↓
┌─────────┐ ┌─────────┐ ┌────────────┐
│ Navbar  │ │Chatbot  │ │ CustomHero │
│         │ │Widget   │ │            │
│Consumes:│ │         │ │ Consumes:  │
│- Auth   │ │Consumes:│ │ - Auth     │
│         │ │- Auth   │ │ - Chatbot  │
│Computes:│ │- Chatbot│ │            │
│- Navbar │ │         │ │ Actions:   │
│  State  │ │Actions: │ │ - Expand   │
│         │ │- Toggle │ │   chatbot  │
└─────────┘ └─────────┘ └────────────┘
```

## State Persistence

### Session Persistence

**Auth State**:
- Persisted server-side via HTTP-only cookies
- Frontend re-checks auth on app load (`refreshUser()` in AuthProvider)
- No localStorage or sessionStorage used for auth tokens
- Session timeout managed by backend

**Chatbot State**:
- Persisted client-side in React Context (in-memory)
- Resets to default on page refresh
- Optional enhancement: Use sessionStorage to persist expanded state across refreshes

## Error States

### AuthContext Error Handling

**Error Scenarios**:

1. **Network Error During Auth Check**:
   ```typescript
   // Auth check fails due to network
   { user: null, isAuthenticated: false, isLoading: false }
   // Treat as unauthenticated
   ```

2. **401 Unauthorized from /auth/me**:
   ```typescript
   // Valid response indicating not authenticated
   { user: null, isAuthenticated: false, isLoading: false }
   ```

3. **500 Server Error**:
   ```typescript
   // Server error during auth check
   { user: null, isAuthenticated: false, isLoading: false }
   // Log error, treat as unauthenticated for UX
   ```

4. **Login/Signup Failure**:
   ```typescript
   // User remains unauthenticated
   { user: null, isAuthenticated: false, isLoading: false }
   // Error message displayed in form
   ```

**Error Recovery**:
- All auth errors default to unauthenticated state
- User can retry login manually
- No automatic retry (to avoid infinite loops)
- Errors logged to console for debugging

## Validation & Constraints

### Type Constraints

All state objects must match TypeScript interfaces exactly:
- `User` must have `id` and `email` at minimum
- `isAuthenticated` must be boolean derived from `user !== null`
- `isLoading` must be boolean
- `isExpanded` must be boolean

### Business Rules

1. **Auth State**:
   - User cannot be partially authenticated (either fully authenticated or not)
   - `isLoading` must eventually become `false` (timeout after 10 seconds)
   - Logout always succeeds (even if backend call fails, clear local state)

2. **Chatbot Visibility**:
   - Chatbot MUST NOT render for unauthenticated users
   - Chatbot state (expanded/collapsed) only matters when authenticated

3. **Navbar**:
   - Cannot show both auth links AND user dropdown simultaneously
   - During loading, can show loading indicator OR hide both (implementation choice)

## Migration Notes

**Existing State Structure**:
- Current `useAuth.tsx` already defines most of this structure
- `User` type imported from `@auth/core/types` (may need to verify structure matches)
- No migration needed for auth state

**New Additions**:
- `ChatbotControlState` is new (requires creating `useChatbotControl.tsx`)
- `NavbarState` is new (computed in swizzled Navbar component)

**Breaking Changes**:
- None - extending existing state, not modifying

## Future Considerations

**Potential Enhancements** (Out of scope for this feature):
1. Add `lastLoginAt` timestamp to User entity
2. Add user profile picture/avatar URL
3. Add role-based permissions to User
4. Persist chatbot expanded state in sessionStorage
5. Add user preferences to AuthContext (theme, language, etc.)
6. Add "Remember Me" functionality (longer session cookies)

**Scalability**:
- Current model supports single-user sessions
- If multi-device support needed, backend session management required
- If offline support needed, service worker + IndexedDB required (significant change)
