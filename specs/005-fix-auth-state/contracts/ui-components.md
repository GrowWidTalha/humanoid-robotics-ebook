# UI Component Contracts

**Feature**: 005-fix-auth-state
**Date**: 2025-12-13
**Phase**: Phase 1 - Design

## Overview

This document defines the interface contracts for UI components involved in the authentication state management feature. These contracts specify component props, behavior, and integration points.

## Component Contracts

### 1. Navbar Component (Swizzled)

**Location**: `src/theme/Navbar/index.tsx`

**Purpose**: Override Docusaurus default navbar to show authentication-aware menu items

**Props**: None (uses Docusaurus theme context internally)

**Consumes**:
- `useAuth()` from `src/hooks/useAuth.tsx`
- `useThemeConfig()` from `@docusaurus/theme-common`

**Behavior**:
```typescript
interface NavbarBehavior {
  // When user is not authenticated and not loading
  renderAuthLinks(): JSX.Element;  // Show "Login" and "Sign Up" links

  // When user is authenticated and not loading
  renderUserDropdown(): JSX.Element;  // Show UserDropdown component

  // When loading (optional)
  renderLoadingState(): JSX.Element | null;  // Show loading indicator or nothing
}
```

**Contract**:
- MUST check `isLoading` before deciding what to render
- MUST NOT show both auth links and user dropdown simultaneously
- MUST maintain all other Docusaurus navbar functionality (mobile menu, search, etc.)
- MUST use Docusaurus styling classes for consistency

**Example Usage**:
```typescript
export default function Navbar() {
  const { isAuthenticated, isLoading } = useAuth();
  const themeConfig = useThemeConfig();

  return (
    <nav>
      {/* Existing Docusaurus navbar content */}

      {/* Custom auth-aware items */}
      {!isLoading && (
        <>
          {!isAuthenticated && (
            <NavbarAuthLinks />
          )}
          {isAuthenticated && (
            <UserDropdown />
          )}
        </>
      )}
    </nav>
  );
}
```

### 2. UserDropdown Component

**Location**: `src/components/Navbar/UserDropdown.tsx` (new file)

**Purpose**: Display authenticated user information and actions in navbar

**Props**:
```typescript
interface UserDropdownProps {
  // No props - consumes auth state from context
}
```

**Consumes**:
- `useAuth()` from `src/hooks/useAuth.tsx`

**Behavior**:
```typescript
interface UserDropdownBehavior {
  // Display user's name or email
  displayName: string;  // user.name || user.email

  // Handle logout click
  handleLogout(): Promise<void>;

  // Toggle dropdown menu
  isOpen: boolean;
  toggleOpen(): void;
}
```

**Contract**:
- MUST display user's name if available, fallback to email
- MUST include "Logout" option in dropdown menu
- MUST call `logout()` from auth context when logout clicked
- MUST handle logout errors gracefully (log error, close dropdown)
- SHOULD close dropdown after logout initiated
- SHOULD use Docusaurus navbar dropdown styling for consistency

**Visual Requirements**:
- Display format: User icon + name/email + dropdown arrow
- Dropdown menu items: "Logout" (minimum), can include divider and user email display
- Accessible: Keyboard navigable, ARIA labels

**Example Structure**:
```typescript
export function UserDropdown() {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = async () => {
    setIsOpen(false);
    await logout();
    // Redirect handled by useAuth or page component
  };

  return (
    <div className="navbar-user-dropdown">
      <button onClick={() => setIsOpen(!isOpen)}>
        {user?.name || user?.email}
      </button>
      {isOpen && (
        <div className="dropdown-menu">
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}
    </div>
  );
}
```

### 3. AuthGuard Component (Modified)

**Location**: `src/components/Auth/AuthGuard.tsx` (existing, will modify)

**Purpose**: Protect routes requiring authentication, conditionally render content

**Props**:
```typescript
interface AuthGuardProps {
  children: React.ReactNode;       // Content to render if authenticated
  redirectTo?: string | null;      // Where to redirect if not authenticated (null = no redirect)
  showLoading?: boolean;           // Show loading UI while checking auth (default: true)
}
```

**Consumes**:
- `useAuth()` from `src/hooks/useAuth.tsx`
- `useHistory()` from `@docusaurus/router`

**Behavior**:
```typescript
interface AuthGuardBehavior {
  // When isLoading === true and showLoading === true
  renderLoadingState(): JSX.Element;

  // When isLoading === false and isAuthenticated === false
  handleUnauthenticated(): JSX.Element | null;
  // - If redirectTo is set: redirect to that path, return null
  // - If redirectTo is null: return null (hide content)

  // When isLoading === false and isAuthenticated === true
  renderChildren(): JSX.Element;  // Render children
}
```

**Contract**:
- MUST wait for `isLoading` to be `false` before making auth decision
- MUST NOT redirect if `redirectTo` is `null`
- MUST redirect using `history.push()` if `redirectTo` is a string
- MUST NOT render children if user is not authenticated
- SHOULD show loading state if `showLoading` is true

**Current Usage** (keep compatible):
```typescript
// In Root.tsx - showing chatbot only to authenticated users
<AuthGuard redirectTo={null} showLoading={false}>
  <ChatbotWidget />
</AuthGuard>
```

**Modifications Needed**:
- Ensure `isLoading` handling is correct
- Add timeout to prevent infinite loading state

### 4. ChatbotWidget Component (Modified)

**Location**: `src/components/ChatbotWidget/ChatbotWidget.tsx` (existing, will modify)

**Purpose**: AI chatbot interface, only visible to authenticated users

**Props**: None (existing component has no props)

**Consumes** (NEW):
- `useChatbotControl()` from `src/hooks/useChatbotControl.tsx`

**Behavior** (NEW):
```typescript
interface ChatbotWidgetBehavior {
  // Existing behavior
  isExpanded: boolean;        // Currently from local state
  toggleExpanded(): void;     // Currently local function

  // NEW: Consume from context instead of local state
  // isExpanded and setIsExpanded now come from useChatbotControl()
}
```

**Contract**:
- MUST use `isExpanded` from `useChatbotControl()` instead of local `useState`
- MUST call `setIsExpanded()` when user clicks minimize/expand
- MUST maintain all existing chatbot functionality (messaging, RAG, etc.)
- MUST remain wrapped in `AuthGuard` in `Root.tsx` (no changes to visibility logic)

**Modifications Needed**:
```typescript
// BEFORE (current implementation)
const [isExpanded, setIsExpanded] = useState(true);

// AFTER (new implementation)
const { isExpanded, setIsExpanded } = useChatbotControl();
```

### 5. Login/Signup Pages (Modified)

**Location**:
- `src/pages/auth/login.tsx` (existing, will modify)
- `src/pages/auth/signup.tsx` (existing, will modify)

**Purpose**: Authentication pages that redirect authenticated users

**Props**: None (Docusaurus page components)

**Consumes**:
- `useAuth()` from `src/hooks/useAuth.tsx`
- `useHistory()` from `@docusaurus/router`
- `useBaseUrl()` from `@docusaurus/useBaseUrl`

**Behavior** (NEW):
```typescript
interface AuthPageBehavior {
  // On component mount
  checkAuthAndRedirect(): void;
  // If isAuthenticated === true and isLoading === false:
  //   - Redirect to home page
  //   - Do not show auth form

  // While checking or redirecting
  showLoadingState(): JSX.Element | null;

  // If not authenticated
  showAuthForm(): JSX.Element;
}
```

**Contract**:
- MUST check authentication status on mount
- MUST redirect to home page if user is authenticated
- MUST NOT show auth form while redirecting
- SHOULD show loading indicator while checking auth
- MUST use `useHistory().push()` or `window.location.href` for redirect

**Implementation Pattern**:
```typescript
export default function LoginPage() {
  const { isAuthenticated, isLoading } = useAuth();
  const history = useHistory();
  const baseUrl = useBaseUrl('/');

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      history.push(baseUrl);
    }
  }, [isAuthenticated, isLoading, history, baseUrl]);

  if (isLoading) {
    return <LoadingIndicator />;
  }

  if (isAuthenticated) {
    return null;  // Will redirect via useEffect
  }

  return <LoginForm />;
}
```

### 6. CustomHero Component (Modified)

**Location**: `src/components/LandingPage/CustomHero.tsx` (existing, will modify)

**Purpose**: Landing page hero section with "Get Started with AI" button

**Props**: None (existing component has no props)

**Consumes** (NEW):
- `useAuth()` from `src/hooks/useAuth.tsx`
- `useChatbotControl()` from `src/hooks/useChatbotControl.tsx`

**Behavior** (MODIFIED):
```typescript
interface GetStartedButtonBehavior {
  // When user is NOT authenticated
  redirectToSignup(): void;  // Existing behavior: navigate to /auth/signup

  // When user IS authenticated (NEW)
  expandChatbot(): void;     // NEW behavior: call setIsExpanded(true)
}
```

**Contract**:
- MUST check `isAuthenticated` from `useAuth()`
- IF authenticated: call `setIsExpanded(true)` from `useChatbotControl()`
- IF NOT authenticated: navigate to `/auth/signup` (existing behavior)
- MUST NOT navigate to signup if user is authenticated

**Modifications Needed**:
```typescript
// BEFORE (current implementation)
<Link to="/auth/signup">Get Started with AI</Link>

// AFTER (new implementation)
const { isAuthenticated } = useAuth();
const { setIsExpanded } = useChatbotControl();

const handleGetStarted = () => {
  if (isAuthenticated) {
    setIsExpanded(true);
  } else {
    history.push('/auth/signup');
  }
};

<button onClick={handleGetStarted}>Get Started with AI</button>
```

## New Component/Hook Contracts

### 7. useChatbotControl Hook (NEW)

**Location**: `src/hooks/useChatbotControl.tsx` (new file)

**Purpose**: Provide global chatbot control state

**Exports**:
```typescript
// Context
export const ChatbotControlContext = createContext<ChatbotControlContextType | undefined>(undefined);

// Provider component
export function ChatbotControlProvider({ children }: { children: React.ReactNode }): JSX.Element;

// Hook
export function useChatbotControl(): ChatbotControlContextType;

// Types
interface ChatbotControlContextType {
  isExpanded: boolean;
  setIsExpanded: (expanded: boolean) => void;
  toggleExpanded: () => void;
}
```

**Provider Behavior**:
- Maintains `isExpanded` state (default: `true`)
- Provides `setIsExpanded` and `toggleExpanded` functions
- Wraps entire app in `Root.tsx`

**Hook Behavior**:
- Returns current chatbot control state
- Throws error if used outside `ChatbotControlProvider`

**Contract**:
- MUST be provided at app root (in `Root.tsx`)
- MUST initialize with `isExpanded: true`
- State MUST be boolean only
- Provider MUST NOT cause unnecessary re-renders

**Implementation**:
```typescript
export function ChatbotControlProvider({ children }) {
  const [isExpanded, setIsExpanded] = useState(true);

  const toggleExpanded = useCallback(() => {
    setIsExpanded(prev => !prev);
  }, []);

  const value = useMemo(
    () => ({ isExpanded, setIsExpanded, toggleExpanded }),
    [isExpanded, toggleExpanded]
  );

  return (
    <ChatbotControlContext.Provider value={value}>
      {children}
    </ChatbotControlContext.Provider>
  );
}
```

### 8. Root Component (Modified)

**Location**: `src/theme/Root.tsx` (existing, will modify)

**Purpose**: Global app wrapper, provides all context providers

**Current Structure**:
```typescript
export default function Root({ children }) {
  return (
    <AuthProvider>
      {children}
      <AuthGuard redirectTo={null} showLoading={false}>
        <ChatbotWidget />
      </AuthGuard>
    </AuthProvider>
  );
}
```

**NEW Structure**:
```typescript
export default function Root({ children }) {
  return (
    <AuthProvider>
      <ChatbotControlProvider>
        {children}
        <AuthGuard redirectTo={null} showLoading={false}>
          <ChatbotWidget />
        </AuthGuard>
      </ChatbotControlProvider>
    </AuthProvider>
  );
}
```

**Contract**:
- MUST wrap app in `AuthProvider` first (outer)
- MUST wrap app in `ChatbotControlProvider` second (inner)
- MUST maintain `AuthGuard` wrapping of `ChatbotWidget`
- Provider order matters: Auth → ChatbotControl → children

## Integration Points

### Context Provider Hierarchy

```
Root
 └─ AuthProvider
     └─ ChatbotControlProvider
         ├─ {children} (entire app)
         │   ├─ Navbar (uses auth)
         │   ├─ Pages (uses auth)
         │   └─ CustomHero (uses auth + chatbot control)
         └─ AuthGuard
             └─ ChatbotWidget (uses chatbot control)
```

### Data Flow

```
User Action: Click "Get Started with AI"
    ↓
CustomHero.handleGetStarted()
    ↓
Check isAuthenticated from useAuth()
    ↓
┌─────────────────┬─────────────────┐
│ Authenticated   │ Not Authenticated│
↓                 ↓
useChatbotControl() Navigate to
.setIsExpanded(true) /auth/signup
    ↓
ChatbotWidget re-renders
    ↓
Chatbot expands
```

### Component Dependencies

| Component | Depends On | Provides |
|-----------|------------|----------|
| AuthProvider | Backend API | AuthContext |
| ChatbotControlProvider | - | ChatbotControlContext |
| Navbar | AuthContext | UI |
| UserDropdown | AuthContext | UI |
| AuthGuard | AuthContext | Conditional rendering |
| ChatbotWidget | ChatbotControlContext | UI |
| CustomHero | AuthContext, ChatbotControlContext | UI |
| Login/Signup Pages | AuthContext | UI |

## Testing Contracts

### Unit Test Requirements

Each component must have tests covering:

1. **Navbar**:
   - Renders auth links when not authenticated
   - Renders user dropdown when authenticated
   - Does not render both simultaneously
   - Handles loading state

2. **UserDropdown**:
   - Displays user name/email
   - Logout button calls logout function
   - Dropdown toggles open/closed

3. **AuthGuard**:
   - Redirects when not authenticated and redirectTo is set
   - Does not redirect when redirectTo is null
   - Renders children when authenticated
   - Shows loading state when isLoading is true

4. **ChatbotWidget**:
   - Uses isExpanded from context
   - Calls setIsExpanded when toggling

5. **Login/Signup Pages**:
   - Redirects when authenticated
   - Shows form when not authenticated
   - Handles loading state

6. **CustomHero**:
   - Expands chatbot when authenticated
   - Navigates to signup when not authenticated

### Integration Test Requirements

1. Full auth flow: Login → Navbar updates → Chatbot visible
2. Logout flow: Logout → Navbar updates → Chatbot hidden
3. Get Started flow: Authenticated user → Click button → Chatbot expands

## Error Handling Contracts

### Component Error Boundaries

All components must handle:

1. **Missing Context**:
   - `useAuth()` called outside `AuthProvider`: Throw descriptive error
   - `useChatbotControl()` called outside provider: Throw descriptive error

2. **Network Errors**:
   - Auth check fails: Treat as unauthenticated
   - Logout fails: Clear local state anyway

3. **Invalid State**:
   - User object missing required fields: Fallback to email display
   - isLoading stuck true: Timeout after 10 seconds

### User-Facing Errors

- Login/signup errors: Display in form
- Logout errors: Log to console, clear state
- Auth check errors: Silent (treat as unauthenticated)

## Accessibility Contracts

All components must:
- Use semantic HTML elements
- Include ARIA labels where appropriate
- Support keyboard navigation
- Maintain sufficient color contrast
- Announce state changes to screen readers

**Specific Requirements**:
- UserDropdown: `role="menu"`, keyboard navigation
- AuthGuard loading: `role="status"`, screen reader announcement
- ChatbotWidget: Maintain existing ARIA labels
- Get Started button: Clear label indicating auth-dependent behavior
