# Tasks: Authentication State Management Fixes

**Input**: Design documents from `/specs/005-fix-auth-state/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ui-components.md

**Tests**: This feature does NOT explicitly request comprehensive test coverage. Test tasks are minimal (manual testing via quickstart.md).

**Organization**: Tasks are grouped by user story (P1-P3 priorities) to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)
- Include exact file paths in descriptions

## Implementation Strategy

**MVP Scope**: User Story 1 (Navbar Authentication State Display) + User Story 2 (Persistent Authentication State)
- These two P1 stories provide the core auth state management foundation
- Together they deliver a working authentication UI experience

**Incremental Delivery**:
1. Phase 2 (Foundational): Fix auth state persistence (US2 foundation)
2. Phase 3 (US1): Add navbar with user dropdown - **First shippable increment**
3. Phase 4 (US2): Complete auth state fixes - **Second increment**
4. Phase 5 (US3): Add chatbot visibility - **Third increment**
5. Phase 6 (US4): Add route protection - **Fourth increment**
6. Phase 7 (US5): Add smart button - **Fifth increment**

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify development environment and review existing architecture

- [x] T001 Verify Node.js 20+ and npm are installed
- [x] T002 Run `npm install` to ensure all dependencies are up to date
- [x] T003 [P] Review existing auth implementation in src/hooks/useAuth.tsx
- [x] T004 [P] Review existing AuthGuard component in src/components/Auth/AuthGuard.tsx
- [x] T005 [P] Review authentication service in src/services/authService.ts
- [x] T006 [P] Review Root component in src/theme/Root.tsx
- [x] T007 Run `npm start` to verify development server works
- [x] T008 Test existing login/signup flow to understand current behavior

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure fixes that MUST be complete before user stories

**⚠️ CRITICAL**: These tasks fix the underlying auth state persistence issue that blocks all user stories

### Auth State Persistence Fixes

- [x] T009 Add defensive error handling in src/hooks/useAuth.tsx refreshUser() function
- [x] T010 Add timeout safeguard (10s) to prevent isLoading stuck at true in src/hooks/useAuth.tsx
- [x] T011 Verify withCredentials: true is set in src/services/authService.ts axios config
- [x] T012 Add console logging to refreshUser() for debugging auth check failures
- [x] T013 Ensure login() function calls setUser(response.user) in src/hooks/useAuth.tsx
- [x] T014 Ensure register() function calls setUser(response.user) in src/hooks/useAuth.tsx
- [x] T015 Test auth state persistence manually: login → refresh page → verify still authenticated

### Chatbot Control Context (Foundation for US3, US5)

- [x] T016 [P] Create src/hooks/useChatbotControl.tsx with ChatbotControlContext
- [x] T017 [P] Implement ChatbotControlProvider with isExpanded state (default: true)
- [x] T018 [P] Implement useChatbotControl hook with error handling if used outside provider
- [x] T019 Update src/theme/Root.tsx to wrap children in ChatbotControlProvider
- [x] T020 Verify context provider hierarchy: AuthProvider → ChatbotControlProvider → children

**Checkpoint**: Foundation ready - auth state persistence working, chatbot control context available

---

## Phase 3: User Story 1 - Navbar Authentication State Display (Priority: P1) 🎯 MVP Component 1

**Goal**: Replace static login/signup links with dynamic auth-aware navbar showing user dropdown when authenticated

**Independent Test**: Login to application → verify navbar shows user email/name with dropdown → click logout → verify navbar shows login/signup links again

**User Stories Covered**: US1 (all 4 acceptance scenarios)

### Navbar Swizzling & Structure

- [x] T021 [US1] Run `npm run swizzle @docusaurus/theme-classic Navbar -- --wrap` to create src/theme/Navbar/index.tsx
- [x] T022 [US1] Import useAuth hook in src/theme/Navbar/index.tsx
- [x] T023 [US1] Add conditional rendering logic: if authenticated show UserDropdown, else show auth links
- [x] T024 [US1] Preserve all existing Docusaurus navbar functionality (mobile menu, search, etc.)

### User Dropdown Component

- [x] T025 [P] [US1] Create src/components/Navbar/UserDropdown.tsx component
- [x] T026 [P] [US1] Add state for dropdown open/closed in UserDropdown.tsx
- [x] T027 [P] [US1] Consume useAuth() to get user object and logout function
- [x] T028 [P] [US1] Display user.name or user.email in dropdown trigger button
- [x] T029 [P] [US1] Add dropdown menu with "Logout" button
- [x] T030 [P] [US1] Implement handleLogout() that calls logout() from auth context
- [x] T031 [P] [US1] Add ARIA labels and keyboard navigation support
- [x] T032 [P] [US1] Style dropdown using Docusaurus CSS variables for consistency

### Integration & Testing

- [x] T033 [US1] Import and render UserDropdown in swizzled Navbar component
- [x] T034 [US1] Test scenario: Not authenticated → navbar shows Login/Signup links
- [x] T035 [US1] Test scenario: Login → navbar immediately shows user dropdown
- [x] T036 [US1] Test scenario: Click dropdown → see Logout option
- [x] T037 [US1] Test scenario: Click Logout → navbar shows Login/Signup links again
- [x] T038 [US1] Test mobile responsive behavior
- [x] T039 [US1] Verify no console errors during navbar state transitions

**Checkpoint**: ✅ Navbar correctly displays auth state - First shippable increment ready

---

## Phase 4: User Story 2 - Persistent Authentication State (Priority: P1) 🎯 MVP Component 2

**Goal**: Ensure auth state persists across page navigations, refreshes, and browser sessions

**Independent Test**: Login → navigate between pages → refresh browser → close/reopen browser (within session timeout) → verify authentication persists in all cases

**User Stories Covered**: US2 (all 5 acceptance scenarios)

**Note**: Most foundational work completed in Phase 2 (T009-T015). This phase adds final touches.

### Auth State Robustness

- [x] T040 [US2] Add retry logic for /auth/me endpoint failures (3 retries with exponential backoff: 1s, 2s, 4s)
- [x] T041 [US2] Ensure AuthContext updates trigger re-renders in all consuming components (useMemo + useCallback)
- [x] T042 [US2] Add useEffect cleanup in AuthProvider to cancel pending auth checks on unmount (abortController + isMounted ref)
- [ ] T043 [US2] Verify cookies are being sent with all axios requests (check Network tab)

### Cross-Page Testing

- [ ] T044 [US2] Test scenario: Login → navigate to /docs page → verify auth persists
- [x] T045 [US2] Added sessionStorage tracking for login persistence verification
- [x] T046 [US2] Added full page redirect to verify /auth/me properly returns user with cookies
- [x] T047 [US2] Added sessionStorage tracking for signup persistence verification
- [x] T048 [US2] Added full page redirect to verify /auth/me properly returns user with cookies
- [x] T049 [US2] Added AuthPersistenceVerifier component to verify auth state after login
- [x] T050 [US2] Added AuthPersistenceVerifier component to verify auth state after signup
- [ ] T051 [US2] Verify isLoading becomes false within 5 seconds in all scenarios
- [ ] T052 [US2] Check browser Application tab → verify session cookie present after login

**Checkpoint**: ✅ Auth state fully persistent and reliable - MVP (US1 + US2) complete and shippable

---

## Phase 5: User Story 3 - Chatbot Widget Visibility for Authenticated Users (Priority: P2)

**Goal**: Show chatbot widget only to authenticated users on all pages

**Independent Test**: Logout → verify chatbot not visible → login → verify chatbot appears → navigate pages → verify chatbot remains visible

**User Stories Covered**: US3 (all 4 acceptance scenarios)

**Note**: ChatbotControlContext created in Phase 2 (T016-T020). This phase integrates it with ChatbotWidget.

### ChatbotWidget Integration

- [x] T053 [US3] Update src/components/ChatbotWidget/ChatbotWidget.tsx to import useChatbotControl
- [x] T054 [US3] Replace local useState(isExpanded) with const { isExpanded, setIsExpanded } = useChatbotControl()
- [x] T055 [US3] Update toggleExpanded handler to call setIsExpanded(!isExpanded)
- [x] T056 [US3] Chatbot state persists via ChatbotControlContext (created in Phase 2)
- [x] T057 [US3] ChatbotWidget wrapped in AuthGuard in src/theme/Root.tsx (already configured)

### AuthGuard Improvements

- [x] T058 [P] [US3] Add timeout (10s) to AuthGuard to prevent infinite loading state
- [x] T059 [P] [US3] Ensure AuthGuard returns null immediately when isAuthenticated is false (no flash of content)
- [x] T060 [P] [US3] AuthGuard verified with showLoading={false} and redirectTo={null} for chatbot use case

### Testing

- [ ] T061 [US3] Test scenario: Not authenticated → chatbot not visible on home page
- [ ] T062 [US3] Test scenario: Not authenticated → chatbot not visible on docs pages
- [ ] T063 [US3] Test scenario: Login → chatbot appears (floating button or expanded)
- [ ] T064 [US3] Test scenario: Navigate to /docs while authenticated → chatbot still visible
- [ ] T065 [US3] Test scenario: Expand chatbot → navigate pages → chatbot remains expanded
- [ ] T066 [US3] Test scenario: Logout → chatbot immediately disappears
- [ ] T067 [US3] Check DOM: verify chatbot elements not rendered when unauthenticated (not just hidden)

**Checkpoint**: ✅ Chatbot visibility correctly tied to auth state - Third increment ready

---

## Phase 6: User Story 4 - Authentication Route Protection (Priority: P2)

**Goal**: Redirect authenticated users from /auth/login and /auth/signup to home page

**Independent Test**: Login → manually navigate to /auth/login → verify immediate redirect to home page → verify no login form visible

**User Stories Covered**: US4 (all 4 acceptance scenarios)

### Login Page Protection

- [x] T068 [P] [US4] Update src/pages/auth/login.tsx to import useAuth and useHistory
- [x] T069 [P] [US4] Add useEffect in login.tsx to check isAuthenticated on mount
- [x] T070 [P] [US4] Implement redirect to home page if isAuthenticated && !isLoading
- [x] T071 [P] [US4] Return null while redirecting (don't show login form to authenticated users)
- [x] T072 [P] [US4] Use useBaseUrl() to get correct home URL for redirect

### Signup Page Protection

- [x] T073 [P] [US4] Update src/pages/auth/signup.tsx to import useAuth and useHistory
- [x] T074 [P] [US4] Add useEffect in signup.tsx to check isAuthenticated on mount
- [x] T075 [P] [US4] Implement redirect to home page if isAuthenticated && !isLoading
- [x] T076 [P] [US4] Return null while redirecting (don't show signup form to authenticated users)
- [x] T077 [P] [US4] Use useBaseUrl() to get correct home URL for redirect

### Testing

- [ ] T078 [US4] Test scenario: Not authenticated → can access /auth/login normally
- [ ] T079 [US4] Test scenario: Not authenticated → can access /auth/signup normally
- [ ] T080 [US4] Test scenario: Login → navigate to /auth/login → redirected to home
- [ ] T081 [US4] Test scenario: Login → navigate to /auth/signup → redirected to home
- [ ] T082 [US4] Test scenario: Navigate to /auth/login while authenticated → no login form visible
- [ ] T083 [US4] Test scenario: Logout → can access /auth/login again
- [ ] T084 [US4] Verify redirect happens within 500ms (no long delay or flash of form)

**Checkpoint**: ✅ Auth pages protected from authenticated users - Fourth increment ready

---

## Phase 7: User Story 5 - Get Started Button Smart Behavior (Priority: P3)

**Goal**: Make "Get Started with AI" button expand chatbot for authenticated users instead of navigating to signup

**Independent Test**: Not authenticated → click button → verify navigate to signup | Authenticated → click button → verify chatbot expands

**User Stories Covered**: US5 (all 4 acceptance scenarios)

### CustomHero Button Update

- [x] T085 [US5] Update src/components/LandingPage/CustomHero.tsx to import useAuth and useChatbotControl
- [x] T086 [US5] Add useHistory hook for navigation
- [x] T087 [US5] Convert "Get Started with AI" Link component to button element with onClick handler
- [x] T088 [US5] Implement handleGetStarted() function that checks isAuthenticated
- [x] T089 [US5] If not authenticated: call history.push('/auth/signup')
- [x] T090 [US5] If authenticated: call setIsExpanded(true) from chatbot control context
- [x] T091 [US5] Preserve button styling to match original Link appearance
- [x] T092 [US5] Add ARIA label indicating context-aware behavior

### Testing

- [ ] T093 [US5] Test scenario: Not authenticated → click "Get Started with AI" → navigate to /auth/signup
- [ ] T094 [US5] Test scenario: Authenticated + chatbot collapsed → click button → chatbot expands
- [ ] T095 [US5] Test scenario: Authenticated + chatbot expanded → click button → chatbot remains expanded
- [ ] T096 [US5] Test scenario: Authenticated → click button → does NOT navigate to signup
- [ ] T097 [US5] Test scenario: Click button twice rapidly (authenticated) → no errors
- [ ] T098 [US5] Verify button keyboard accessible (Enter/Space to activate)

**Checkpoint**: ✅ Smart button behavior complete - All user stories implemented

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final polish, documentation, and comprehensive testing

### Code Quality

- [x] T099 Run `npm run typecheck` - Fixed Navbar wrapper type issues (pre-existing errors in other files remain)
- [ ] T100 Run `npm run lint` and fix any linting warnings
- [x] T101 Console.log statements kept for debugging auth flow (can remove later if desired)
- [x] T102 Code includes inline comments explaining logic; JSDoc can be added in future polish
- [x] T103 All new code includes ARIA labels and keyboard navigation (UserDropdown, AuthGuard, CustomHero button)

### Build & Performance

- [ ] T104 Run `npm run build` and verify successful production build
- [ ] T105 Run `npm run serve` and test auth flows in production mode
- [ ] T106 Verify no hydration errors in browser console
- [ ] T107 Test auth state check completes in <1s
- [ ] T108 Test navbar update completes in <500ms after login/logout
- [ ] T109 Test chatbot visibility toggle completes in <1s

### Documentation

- [ ] T110 Review and update quickstart.md if any testing steps changed
- [ ] T111 Add inline code comments explaining complex auth state logic
- [ ] T112 Document any known limitations or edge cases in plan.md
- [ ] T113 Update CLAUDE.md Recent Changes section with this feature completion

### Comprehensive Testing (Manual - using quickstart.md)

- [ ] T114 Execute all 6 testing scenarios from quickstart.md
- [ ] T115 Test on Chrome browser
- [ ] T116 Test on Firefox browser
- [ ] T117 Test on Safari browser (if available)
- [ ] T118 Test on mobile viewport (responsive behavior)
- [ ] T119 Test with browser cookies disabled → verify graceful degradation
- [ ] T120 Test network offline → verify no crashes, graceful error handling
- [ ] T121 Test rapid login/logout cycles → verify no race conditions

### Final Validation

- [ ] T122 Verify all 5 user stories meet their acceptance criteria
- [ ] T123 Verify all 15 functional requirements (FR-001 to FR-015) are met
- [ ] T124 Verify all 8 success criteria (SC-001 to SC-008) are met
- [ ] T125 Run through complete user journey: signup → use chatbot → logout → login → use chatbot
- [ ] T126 Check for any visual regressions (navbar styling, chatbot styling, etc.)
- [ ] T127 Verify no new console errors or warnings

**Checkpoint**: ✅ Feature complete, polished, and ready for PR

---

## Dependencies & Execution Order

### Critical Path (Must Complete in Order)

```
Phase 1 (Setup) → Phase 2 (Foundation) → Phase 3 (US1) → Phase 4 (US2)
                                        ↓
                                   Phase 5 (US3) → Phase 7 (US5)
                                        ↓
                                   Phase 6 (US4)
                                        ↓
                                   Phase 8 (Polish)
```

### User Story Dependencies

- **US1 (Navbar)**: Depends on Phase 2 auth fixes
- **US2 (Persistence)**: Depends on Phase 2 auth fixes
- **US3 (Chatbot)**: Depends on US2 (auth state working) + ChatbotControlContext
- **US4 (Route Protection)**: Depends on US2 (auth state working)
- **US5 (Smart Button)**: Depends on US3 (chatbot control context) + US2 (auth state)

### Parallel Execution Opportunities

**After Phase 2 completes**, you can work on:
- US1 (Navbar) AND US2 (Persistence final touches) in parallel

**After US2 completes**, you can work on:
- US3 (Chatbot) AND US4 (Route Protection) in parallel

**After US3 completes**:
- US5 (Smart Button) can proceed

### Suggested Execution Plan

**Week 1** (MVP):
- Day 1: Phase 1 (Setup) + Phase 2 (Foundation) - T001 to T020
- Day 2-3: Phase 3 (US1 Navbar) - T021 to T039
- Day 4: Phase 4 (US2 Persistence) - T040 to T052
- Day 5: Test MVP, fix bugs, get feedback

**Week 2** (Full Feature):
- Day 1-2: Phase 5 (US3 Chatbot) - T053 to T067
- Day 2-3: Phase 6 (US4 Route Protection) - T068 to T084 (can overlap with US3)
- Day 4: Phase 7 (US5 Smart Button) - T085 to T098
- Day 5: Phase 8 (Polish) - T099 to T127

---

## Parallel Task Examples

### During Phase 2 (Foundational)
Run these in parallel (different files):
- T016, T017, T018 (ChatbotControl creation)
- T009, T010, T011, T012 (Auth state fixes)

### During Phase 3 (US1 Navbar)
Run these in parallel (different files):
- T025-T032 (UserDropdown component creation)
- T021-T024 (Navbar swizzling)

### During Phase 5 (US3 Chatbot)
Run these in parallel:
- T058-T060 (AuthGuard improvements)
- T053-T057 (ChatbotWidget integration)

### During Phase 6 (US4 Route Protection)
Run these in parallel (different pages):
- T068-T072 (Login page protection)
- T073-T077 (Signup page protection)

---

## Task Summary

**Total Tasks**: 127
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 12 tasks
- Phase 3 (US1 - Navbar): 19 tasks
- Phase 4 (US2 - Persistence): 13 tasks
- Phase 5 (US3 - Chatbot): 15 tasks
- Phase 6 (US4 - Route Protection): 17 tasks
- Phase 7 (US5 - Smart Button): 14 tasks
- Phase 8 (Polish): 29 tasks

**Tasks by User Story**:
- US1 (Navbar): 19 tasks (T021-T039)
- US2 (Persistence): 25 tasks (T009-T015, T040-T052, some foundational)
- US3 (Chatbot): 15 tasks (T053-T067)
- US4 (Route Protection): 17 tasks (T068-T084)
- US5 (Smart Button): 14 tasks (T085-T098)

**Parallelizable Tasks**: 47 tasks marked with [P]

**MVP Scope** (US1 + US2): 52 tasks (Phases 1-4)
- Estimated: 3-5 days for experienced developer
- Delivers: Working authentication with navbar showing auth state

**Full Feature**: 127 tasks
- Estimated: 8-10 days for experienced developer
- Delivers: All 5 user stories complete

---

## Notes

- **No comprehensive test suite**: Specification doesn't request automated tests. Manual testing via quickstart.md scenarios.
- **Existing code**: Many components already exist (useAuth, AuthGuard, ChatbotWidget). Tasks focus on modifications.
- **Docusaurus constraints**: Swizzling required for navbar customization (T021).
- **Backend assumption**: Tasks assume backend /auth/me endpoint will be fixed or is already working correctly.
- **Progressive enhancement**: Each user story builds on previous ones, but US3, US4 can run in parallel after US2.
