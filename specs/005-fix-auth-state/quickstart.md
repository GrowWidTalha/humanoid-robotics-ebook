# Developer Quickstart: Authentication State Management Fixes

**Feature**: 005-fix-auth-state
**Date**: 2025-12-13
**For**: Developers implementing this feature

## Overview

This guide helps developers quickly set up, test, and verify the authentication state management fixes. It covers local development setup, testing scenarios, and troubleshooting common issues.

## Prerequisites

- Node.js 20+ installed
- Project repository cloned and on branch `005-fix-auth-state`
- Backend API accessible (local or remote)
- Basic understanding of React, TypeScript, and Docusaurus

## Quick Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Backend API URL

The backend API URL is configured in `docusaurus.config.ts` and `src/services/authService.ts`.

**Current Configuration**:
```typescript
// In docusaurus.config.ts
customFields: {
  chatbotApiUrl: process.env.REACT_APP_API_URL || "https://growwithtalha-humanoid-robotics-rag.hf.space/api",
}

// In src/services/authService.ts
const API_URL = "https://growwithtalha-humanoid-robotics-rag.hf.space/api";
```

**For Local Backend Testing**:
```bash
# Set environment variable (optional)
export REACT_APP_API_URL=http://localhost:8000/api

# Or modify src/services/authService.ts temporarily
const API_URL = "http://localhost:8000/api";
```

### 3. Start Development Server

```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Verify Backend Connectivity

Before testing auth features, verify the backend is reachable:

```bash
# Test auth/me endpoint (should return 401 if not authenticated)
curl -v http://localhost:8000/api/auth/me

# Or use the remote backend
curl -v https://growwithtalha-humanoid-robotics-rag.hf.space/api/auth/me
```

Expected response when not authenticated:
```
HTTP/1.1 401 Unauthorized
```

## Testing Scenarios

### Scenario 1: Navbar Shows Auth Links for Unauthenticated Users

**Goal**: Verify navbar displays "Login" and "Sign Up" links when user is not logged in.

**Steps**:
1. Clear browser cookies (or use incognito mode)
2. Navigate to [http://localhost:3000](http://localhost:3000)
3. Wait for page to load

**Expected Behavior**:
- Navbar shows "Login" and "Sign Up" links on the right side
- No user dropdown visible
- No loading indicator (after initial load)

**Verification**:
```typescript
// Check in browser console
window.localStorage.clear();  // Clear any stored state
// Refresh page
// Inspect navbar: should see auth links
```

### Scenario 2: Navbar Shows User Dropdown After Login

**Goal**: Verify navbar displays user information and dropdown after successful login.

**Steps**:
1. Navigate to [http://localhost:3000/auth/login](http://localhost:3000/auth/login)
2. Enter valid credentials (test user or create account)
3. Click "Login"
4. Wait for redirect to home page

**Expected Behavior**:
- After login, navbar replaces "Login"/"Sign Up" with user dropdown
- User dropdown shows email or name
- Dropdown menu includes "Logout" option
- Chatbot widget appears (floating button or expanded)

**Verification**:
```typescript
// Check in browser console after login
// Auth context should show authenticated state
```

### Scenario 3: Chatbot Widget Visibility

**Goal**: Verify chatbot is only visible to authenticated users.

**Steps**:
1. **When Not Authenticated**:
   - Clear cookies, navigate to home page
   - Verify chatbot is NOT visible (no floating button, no expanded widget)

2. **When Authenticated**:
   - Login via `/auth/login`
   - Navigate to any page
   - Verify chatbot IS visible (floating button or expanded)

**Expected Behavior**:
- Unauthenticated: No chatbot anywhere on page
- Authenticated: Chatbot visible on all pages

**Debugging**:
```typescript
// In browser console
// Check auth state
const authState = /* access React DevTools or check network tab */;
console.log('Is Authenticated:', authState.isAuthenticated);
console.log('Is Loading:', authState.isLoading);
```

### Scenario 4: Auth Page Redirect for Authenticated Users

**Goal**: Verify authenticated users are redirected from login/signup pages.

**Steps**:
1. Login to application
2. Manually navigate to [http://localhost:3000/auth/login](http://localhost:3000/auth/login)
3. Observe behavior

**Expected Behavior**:
- Immediately redirected to home page (/)
- Login form does NOT appear
- Brief loading state acceptable

**Alternative Test**:
1. Login to application
2. Try navigating to [http://localhost:3000/auth/signup](http://localhost:3000/auth/signup)
3. Should also redirect to home page

### Scenario 5: Get Started Button Smart Behavior

**Goal**: Verify "Get Started with AI" button behavior changes based on auth state.

**Steps**:
1. **When Not Authenticated**:
   - Navigate to home page
   - Click "Get Started with AI" button
   - Verify redirects to `/auth/signup`

2. **When Authenticated**:
   - Login to application
   - Navigate to home page
   - Chatbot should be collapsed (click minimize if expanded)
   - Click "Get Started with AI" button
   - Verify chatbot expands (does NOT navigate to signup)

**Expected Behavior**:
- Unauthenticated: Button navigates to signup page
- Authenticated: Button expands chatbot widget

### Scenario 6: Logout Flow

**Goal**: Verify logout correctly updates all UI elements.

**Steps**:
1. Login to application
2. Verify navbar shows user dropdown
3. Verify chatbot is visible
4. Click user dropdown
5. Click "Logout"
6. Observe changes

**Expected Behavior**:
- Navbar immediately shows "Login"/"Sign Up" links
- User dropdown disappears
- Chatbot widget disappears
- User is logged out (can verify by checking `/auth/me` in Network tab)

## Browser DevTools Debugging

### React DevTools

Install React DevTools browser extension to inspect component state.

**Useful Checks**:
1. Find `AuthProvider` component:
   - Inspect `user`, `isAuthenticated`, `isLoading` state

2. Find `ChatbotControlProvider` component:
   - Inspect `isExpanded` state

3. Find `Navbar` component:
   - Verify it's consuming auth context
   - Check conditional rendering logic

### Network Tab Monitoring

**Key Endpoints to Monitor**:

1. **POST `/api/auth/login`**:
   - Should return 200 with user object
   - Should set `Set-Cookie` header (HTTP-only cookie)

2. **GET `/api/auth/me`**:
   - Called on app load by `AuthProvider.refreshUser()`
   - Should return 200 with user object if authenticated
   - Should return 401 if not authenticated

3. **POST `/api/auth/logout`**:
   - Should return 200
   - Should clear cookies

**Debugging Tips**:
```bash
# Check if cookies are being sent
# In Network tab, look for "Cookie" header in request
# Should include session cookie

# Check Set-Cookie in response headers after login
# Should see HttpOnly, Secure, SameSite attributes
```

## Common Issues & Troubleshooting

### Issue 1: Auth State Stuck in Loading

**Symptom**: `isLoading` stays `true`, UI never updates

**Possible Causes**:
- Backend `/auth/me` endpoint not responding
- Network error during auth check
- Missing error handling in `refreshUser()`

**Solution**:
```typescript
// Check AuthProvider implementation
// Ensure finally block sets isLoading = false

// Add timeout safeguard
useEffect(() => {
  const timeout = setTimeout(() => {
    if (isLoading) {
      console.error('Auth check timeout');
      setIsLoading(false);
    }
  }, 10000);  // 10 second timeout

  return () => clearTimeout(timeout);
}, [isLoading]);
```

### Issue 2: Cookies Not Being Sent

**Symptom**: Login succeeds but `/auth/me` returns 401

**Possible Causes**:
- `withCredentials: true` not set in axios config
- CORS headers not allowing credentials
- Cookie domain mismatch (localhost vs 127.0.0.1)
- SameSite cookie attribute blocking cross-origin requests

**Solution**:
```typescript
// Verify in authService.ts
const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,  // ← Must be present
});

// Check browser Application tab > Cookies
// Verify session cookie is present after login
// Verify Domain and Path match API URL
```

**Backend Requirements** (out of scope but document):
- Backend must send `Access-Control-Allow-Credentials: true`
- Backend must send `Access-Control-Allow-Origin: http://localhost:3000` (not `*`)
- Backend must set cookie with correct domain

### Issue 3: Navbar Not Updating After Login

**Symptom**: After login, navbar still shows "Login"/"Sign Up"

**Possible Causes**:
- Auth state not updating in context
- Login success not calling `setUser()`
- Navbar not re-rendering

**Solution**:
```typescript
// Check AuthProvider.login() function
// Ensure it calls setUser(response.user)

const login = async (email, password) => {
  setIsLoading(true);
  try {
    const response = await authService.login(email, password);
    setUser(response.user);  // ← Must update user state
  } finally {
    setIsLoading(false);
  }
};

// Check if Navbar is consuming auth context
// Should see re-render in React DevTools
```

### Issue 4: Chatbot Not Visible After Login

**Symptom**: User is authenticated but chatbot doesn't appear

**Possible Causes**:
- `AuthGuard` still thinks user is unauthenticated
- `isLoading` never becomes `false`
- CSS hiding chatbot

**Solution**:
```typescript
// Check AuthGuard component
// Verify it checks isLoading before hiding content

if (isLoading && showLoading) {
  return <LoadingState />;
}

if (!isAuthenticated) {
  return null;  // ← Should only reach if isLoading is false
}

return <>{children}</>;

// Inspect DOM: search for chatbot elements
// Check if hidden by CSS or not rendered at all
```

### Issue 5: Get Started Button Not Expanding Chatbot

**Symptom**: Button still navigates to signup when authenticated

**Possible Causes**:
- CustomHero not consuming auth context
- Button still using `Link` component instead of `button` with `onClick`
- Chatbot control context not working

**Solution**:
```typescript
// Verify CustomHero implementation
const { isAuthenticated } = useAuth();
const { setIsExpanded } = useChatbotControl();

const handleGetStarted = () => {
  if (isAuthenticated) {
    setIsExpanded(true);  // ← Expand chatbot
  } else {
    history.push('/auth/signup');
  }
};

// Must use button, not Link component
<button onClick={handleGetStarted}>Get Started with AI</button>
```

## Running Tests

### Unit Tests

```bash
# Run all tests
npm test

# Run tests for specific component
npm test -- AuthGuard.test.tsx

# Run tests in watch mode
npm test -- --watch
```

### Test Coverage

```bash
# Generate coverage report
npm test -- --coverage

# View coverage report
open coverage/lcov-report/index.html
```

**Expected Coverage**:
- AuthGuard: 100% (all branches)
- UserDropdown: >90%
- Navbar: >80% (Docusaurus integration makes 100% difficult)
- Auth pages: >90%

## Manual Testing Checklist

Before marking feature as complete, verify:

- [ ] Navbar shows auth links when not authenticated
- [ ] Navbar shows user dropdown when authenticated
- [ ] User dropdown displays email/name correctly
- [ ] Logout button works and updates navbar immediately
- [ ] Chatbot is hidden when not authenticated
- [ ] Chatbot is visible when authenticated
- [ ] Chatbot expands/collapses correctly
- [ ] Login page redirects authenticated users
- [ ] Signup page redirects authenticated users
- [ ] Get Started button navigates to signup (not authenticated)
- [ ] Get Started button expands chatbot (authenticated)
- [ ] Auth state persists across page navigations
- [ ] Auth state persists across page refresh
- [ ] All tests pass (`npm test`)
- [ ] No console errors during normal flows
- [ ] Build succeeds (`npm run build`)

## Build and Deploy

### Build for Production

```bash
# Create production build
npm run build

# Serve production build locally
npm run serve
```

Open [http://localhost:3000](http://localhost:3000) and test in production mode.

### Verify Production Build

Production builds are static, but client-side auth should still work:

- [ ] Auth state checks work (calls `/auth/me`)
- [ ] Login/logout flows work
- [ ] Navbar updates correctly
- [ ] Chatbot visibility works
- [ ] No hydration errors in console

## Backend API Requirements (Reference)

This feature assumes the backend provides:

1. **POST `/api/auth/login`**:
   - Accepts: `{ email: string, password: string }`
   - Returns: `{ user: { id, email, name? } }`
   - Sets HTTP-only session cookie

2. **POST `/api/auth/register`**:
   - Accepts: `{ email: string, password: string }`
   - Returns: `{ user: { id, email, name? } }`
   - Sets HTTP-only session cookie

3. **GET `/api/auth/me`**:
   - Returns: `{ id, email, name? }` if authenticated (200)
   - Returns: `{ detail: "Unauthorized" }` if not (401)
   - Requires session cookie

4. **POST `/api/auth/logout`**:
   - Returns: `{ message: "Logged out" }` (200)
   - Clears session cookie

**CORS Configuration** (required):
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

## Next Steps

After completing quickstart verification:

1. Run full test suite: `npm test`
2. Run type checking: `npm run typecheck`
3. Run build: `npm run build`
4. Create pull request with detailed testing notes
5. Request code review focusing on:
   - Auth state management correctness
   - UI component integration
   - Error handling
   - Accessibility

## Additional Resources

- [Docusaurus Swizzling Guide](https://docusaurus.io/docs/swizzling)
- [React Context Best Practices](https://react.dev/learn/passing-data-deeply-with-context)
- [Axios withCredentials Documentation](https://axios-http.com/docs/req_config)
- [HTTP-only Cookies Security](https://owasp.org/www-community/HttpOnly)
