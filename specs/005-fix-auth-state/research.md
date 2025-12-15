# Research: Authentication State Management Fixes

**Feature**: 005-fix-auth-state
**Date**: 2025-12-13
**Phase**: Phase 0 - Research & Decision Making

## Overview

This document consolidates research findings and architectural decisions for fixing authentication state management issues in the Docusaurus-based textbook application.

## Research Areas

### 1. Docusaurus Navbar Customization

**Research Question**: How to customize the Docusaurus navbar to show dynamic authentication state?

**Decision**: Use Docusaurus theme swizzling to override the Navbar component

**Rationale**:
- Docusaurus provides a "swizzling" mechanism to safely override theme components
- The Navbar component can be swizzled with `npm run swizzle @docusaurus/theme-classic Navbar -- --wrap`
- This approach maintains compatibility with Docusaurus updates while allowing custom React logic
- Can inject authentication context into navbar without modifying core Docusaurus files

**Alternatives Considered**:
1. **Modify docusaurus.config.ts navbar items only**:
   - Rejected: Static configuration cannot conditionally render based on runtime auth state
   - Navbar items in config are evaluated at build time, not client runtime

2. **Create custom navbar from scratch**:
   - Rejected: Loses Docusaurus navbar features (mobile menu, search, version dropdown)
   - Significantly more maintenance overhead

3. **CSS-only approach to hide/show elements**:
   - Rejected: Cannot dynamically change navbar structure or add user dropdown
   - Security issue: elements still in DOM, just hidden

**Implementation Approach**:
- Swizzle the Navbar component to create `src/theme/Navbar/index.tsx`
- Import and use `useAuth()` hook to access authentication state
- Conditionally render auth links vs user dropdown based on `isAuthenticated`
- Create separate `UserDropdown` component for authenticated user menu

**Best Practices**:
- Keep swizzled component minimal - only authentication logic
- Preserve all original Docusaurus navbar functionality
- Use Docusaurus's built-in `useThemeConfig()` to access navbar config
- Follow Docusaurus theming conventions for styling

### 2. React Context Auth State Persistence

**Research Question**: Why does auth state not persist properly across page navigations?

**Current Analysis**:
- Existing `AuthProvider` in `src/hooks/useAuth.tsx` calls `refreshUser()` on mount
- `refreshUser()` calls `authService.getCurrentUser()` which hits `/api/auth/me`
- Issue: The `/auth/me` endpoint returns 401 even after successful login

**Root Cause Hypothesis**:
1. HTTP-only cookies not being sent with `/auth/me` request
2. Backend session not being created properly on login/signup
3. Cookie domain/path mismatch between auth endpoints and /auth/me
4. CORS or credentials configuration issue in axios client

**Decision**: Ensure axios client properly sends credentials with all requests

**Rationale**:
- The `authService.ts` already has `withCredentials: true` in axios config
- This should send HTTP-only cookies with every request
- Issue likely on backend OR cookie not being set properly on login/signup
- Frontend fix: Add defensive error handling and retry logic
- Backend investigation needed (out of scope for this feature, but noted as assumption)

**Implementation Approach**:
- Verify `withCredentials: true` is set in axios config (already present)
- Add error logging to `refreshUser()` to diagnose 401 responses
- Ensure login/signup flows call `refreshUser()` after successful auth
- Add loading states to prevent premature auth state assumptions

**Best Practices**:
- Always handle authentication errors gracefully (treat as unauthenticated)
- Use React Context to share auth state globally
- Minimize auth check frequency (cache state, don't re-check on every render)
- Handle race conditions (multiple components checking auth simultaneously)

### 3. Chatbot Widget Visibility Logic

**Research Question**: How to conditionally render the ChatbotWidget based on auth state?

**Current Implementation**:
- `Root.tsx` wraps `ChatbotWidget` in `<AuthGuard>`
- `AuthGuard` has `redirectTo={null}` and `showLoading={false}`
- This should hide chatbot for non-authenticated users

**Issue Analysis**:
- AuthGuard returns `null` when `!isAuthenticated`
- If `isLoading` is stuck at `true`, chatbot never shows
- If auth check fails, `isAuthenticated` stays `false`

**Decision**: Keep existing AuthGuard approach but fix the auth state issue

**Rationale**:
- The pattern is sound: conditional rendering based on auth state
- Problem is upstream in auth state management, not the widget
- Once auth state is fixed, chatbot visibility will work automatically
- No changes needed to ChatbotWidget component itself

**Implementation Approach**:
- Fix the auth state persistence issue (see Research Area 2)
- Ensure `isLoading` eventually becomes `false` after auth check
- Add timeout to auth check to prevent infinite loading state
- Verify AuthGuard logic handles all states correctly (loading, authenticated, unauthenticated)

**Best Practices**:
- Use composition (wrapping with AuthGuard) for conditional rendering
- Keep auth-dependent components unaware of auth logic
- Handle loading, success, and error states explicitly
- Provide visual feedback during auth state checks

### 4. Route Protection for Auth Pages

**Research Question**: How to redirect authenticated users from /auth/login and /auth/signup?

**Decision**: Add `useEffect` with redirect logic in login.tsx and signup.tsx pages

**Rationale**:
- Docusaurus pages are React components, can use hooks
- Check auth state on mount and redirect if authenticated
- Simple, maintainable approach that doesn't require routing middleware
- Consistent with Docusaurus patterns (client-side React logic)

**Alternatives Considered**:
1. **Create auth routing middleware**:
   - Rejected: Docusaurus doesn't support custom routing middleware
   - Would require ejecting from Docusaurus or complex workarounds

2. **Use AuthGuard with reverse logic**:
   - Rejected: AuthGuard is designed for protecting authenticated routes
   - Creating "reverse" auth guard adds confusion and complexity

3. **Server-side redirect**:
   - Rejected: Docusaurus is a static site generator, no server-side routing
   - All routing is client-side

**Implementation Approach**:
- In login.tsx and signup.tsx, add `useEffect` that checks `isAuthenticated`
- If authenticated, use `history.push('/')` to redirect to home page
- Wait for `isLoading` to be false before making redirect decision
- Don't show auth form while redirecting (show loading state)

**Best Practices**:
- Check `isLoading` before making redirect decision
- Use Docusaurus router (`@docusaurus/router`) for navigation
- Provide visual feedback during redirect
- Prevent flash of auth form before redirect

### 5. Get Started Button Context-Aware Behavior

**Research Question**: How to make "Get Started with AI" button open chatbot for authenticated users?

**Decision**: Use `useAuth()` hook in CustomHero component to conditionally handle button click

**Rationale**:
- CustomHero component already exists in `src/components/LandingPage/`
- Can import `useAuth()` to check authentication state
- Button can call different handlers based on auth state
- For authenticated users, trigger chatbot expand programmatically

**Challenge**: How to programmatically expand the chatbot?

**Solution**: Create a global chatbot control context or use event system

**Alternatives Considered**:
1. **Direct DOM manipulation**:
   - Rejected: Not the React way, fragile

2. **Chatbot control context**:
   - Option: Create `ChatbotContext` with `expandChatbot()` method
   - Wrap app in ChatbotContext provider
   - CustomHero calls `expandChatbot()` when authenticated

3. **Event-based approach**:
   - Option: Dispatch custom event from button
   - ChatbotWidget listens for event and expands
   - Simpler than context, but less type-safe

**Decision**: Use Chatbot control context (ChatbotContext)

**Rationale**:
- More maintainable and testable than events
- Type-safe with TypeScript
- Follows React patterns (context for cross-component communication)
- Can add more chatbot controls in future (close, minimize, etc.)

**Implementation Approach**:
- Create `src/hooks/useChatbotControl.tsx` with ChatbotContext
- Provide `isExpanded` state and `setIsExpanded` function
- Wrap app in ChatbotControlProvider (in Root.tsx)
- ChatbotWidget consumes context to control its expanded state
- CustomHero button calls `setIsExpanded(true)` for authenticated users

**Best Practices**:
- Use React Context for cross-component communication
- Keep context focused (chatbot control only)
- Provide type-safe context API
- Handle edge cases (chatbot not mounted, rapid toggling)

## Technology Stack Summary

**Core Technologies**:
- React 19.0.0 - UI library
- TypeScript 5.6.2 - Type safety
- Docusaurus 3.9.2 - Static site generator
- Axios 1.6.2 - HTTP client
- @docusaurus/router - Client-side routing

**Authentication**:
- React Context API - Auth state management
- HTTP-only cookies - Session storage
- Axios withCredentials - Cookie transmission

**Testing**:
- Jest 29.7.0 - Test runner
- React Testing Library 14.1.2 - Component testing
- @testing-library/jest-dom 6.1.5 - DOM matchers

**Build & Development**:
- Node.js 20+ - Runtime
- npm - Package manager
- TypeScript compiler - Type checking
- ESLint - Linting

## Key Architectural Decisions

### Decision 1: Minimal Backend Assumptions

**Context**: The `/api/auth/me` returning 401 might be a backend issue

**Decision**: Implement frontend fixes assuming backend will be corrected separately

**Impact**:
- Frontend will be robust to backend auth issues
- Can test frontend changes independently
- May need backend fix to fully resolve issue

**Documentation**: Add note in quickstart.md about backend requirements

### Decision 2: No LocalStorage for Auth State

**Context**: HTTP-only cookies are secure but harder to debug

**Decision**: Stick with HTTP-only cookies, no localStorage fallback

**Impact**:
- More secure (XSS protection)
- Auth state fully managed by backend session
- Frontend is stateless for auth (relies on cookie presence)

**Rationale**: Security best practice, already implemented

### Decision 3: Chatbot Control via Context

**Context**: Need cross-component communication between button and chatbot

**Decision**: Create dedicated ChatbotControlContext

**Impact**:
- Adds new context provider to app
- Requires wrapping app in additional provider
- Provides type-safe, testable chatbot control

**Alternatives**: Event-based system (simpler but less maintainable)

### Decision 4: Docusaurus Theme Swizzling

**Context**: Need to customize navbar while maintaining Docusaurus compatibility

**Decision**: Use official swizzling mechanism for Navbar

**Impact**:
- Creates `src/theme/Navbar/` directory
- Overrides default Docusaurus navbar
- Requires maintaining swizzled component on Docusaurus upgrades

**Mitigation**: Keep swizzled component minimal, document customizations

## Open Questions & Assumptions

### Assumptions:
1. Backend `/api/auth/me` endpoint will be fixed or is already working (spec says issue exists)
2. HTTP-only cookies are set correctly by backend on login/signup success
3. Cookie domain/path configuration matches between all auth endpoints
4. Existing AuthProvider/useAuth implementation is fundamentally sound

### Open Questions (for Implementation):
1. Should we add auth state debug logging for troubleshooting?
2. What timeout should we use for auth check to prevent infinite loading?
3. Should navbar show "Loading..." state during auth check or assume unauthenticated?
4. Should chatbot have smooth animation when expanding programmatically?

### Deferred Decisions:
- Specific loading state UX (will decide during implementation)
- Error message wording for auth failures (will decide during implementation)
- Navbar user dropdown menu items beyond Logout (out of scope, can add later)

## Next Steps

Phase 1 will generate:
1. **data-model.md**: Define auth state structure, user entity, chatbot state
2. **contracts/ui-components.md**: Interface contracts for Navbar, UserDropdown, ChatbotWidget
3. **quickstart.md**: Developer guide for testing auth changes locally
