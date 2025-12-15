# Implementation Plan: Authentication State Management Fixes

**Branch**: `005-fix-auth-state` | **Date**: 2025-12-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-fix-auth-state/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Fix authentication state management across the Docusaurus-based textbook application to ensure proper navbar display, chatbot widget visibility, and route protection for authenticated users. The implementation will enhance the existing React Context-based authentication system to properly reflect auth state in UI components and prevent authenticated users from accessing login/signup pages.

## Technical Context

**Language/Version**: TypeScript 5.6.2, React 19.0.0, Node.js 20+
**Primary Dependencies**: Docusaurus 3.9.2, React Router (via @docusaurus/router), Axios 1.6.2, @auth/core 0.18.6
**Storage**: HTTP-only cookies for session management (backend), no frontend local storage for auth tokens
**Testing**: Jest 29.7.0, @testing-library/react 14.1.2, @testing-library/jest-dom 6.1.5
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari - last 3-5 versions), Static site with client-side authentication
**Project Type**: Web application (Docusaurus static site generator with React components)
**Performance Goals**: Auth state checks <1s, navbar updates <500ms, chatbot visibility toggle <1s
**Constraints**: Must work with Docusaurus theming system, maintain static site generation compatibility, HTTP-only cookies only (no localStorage for tokens)
**Scale/Scope**: Single-user concurrent sessions, ~10 UI components affected (Navbar, ChatbotWidget, AuthGuard, auth pages, landing page), small educational site

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

This feature involves authentication bug fixes and UI state management improvements - NOT educational content creation. Therefore, the constitution's content-focused principles (I-VII) do not apply to this implementation work.

**Applicability Assessment**:
- ✅ **N/A - Principle I (Accessibility First)**: Not creating content; fixing authentication UX
- ✅ **N/A - Principle II (Systems Understanding)**: Not creating educational materials
- ✅ **N/A - Principle III (Modular Structure)**: Not creating book modules
- ✅ **N/A - Principle IV (Visual Clarity)**: Not creating educational diagrams
- ✅ **N/A - Principle V (Terminology Standards)**: Not creating educational terminology
- ✅ **N/A - Principle VI (Physical AI Connection)**: Not creating educational content
- ✅ **N/A - Principle VII (Docusaurus/MDX Compliance)**: Applies only to docs, not React components

**Relevant Development Standards**:
- ✅ **Code Quality**: Follow existing TypeScript/React patterns in the codebase
- ✅ **Testing**: Use existing Jest/React Testing Library setup
- ✅ **Simplicity**: Minimal changes to existing authentication architecture
- ✅ **Compatibility**: Maintain Docusaurus SSG compatibility

**Gate Status**: ✅ PASS - Constitution principles do not block this implementation work. Standard software development practices apply.

## Project Structure

### Documentation (this feature)

```text
specs/005-fix-auth-state/
├── spec.md              # Feature specification
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── ui-components.md # UI component interface contracts
├── checklists/
│   └── requirements.md  # Spec quality checklist (already created)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── components/
│   ├── Auth/
│   │   ├── AuthGuard.tsx           # Route protection (MODIFY)
│   │   ├── LoginForm.tsx           # Login form component
│   │   └── SignupForm.tsx          # Signup form component
│   ├── ChatbotWidget/
│   │   └── ChatbotWidget.tsx       # Chatbot UI (visibility logic - MODIFY)
│   ├── LandingPage/
│   │   └── CustomHero.tsx          # Get Started button (MODIFY)
│   └── Navbar/                     # (CREATE - Docusaurus swizzle)
│       └── UserDropdown.tsx        # (CREATE - new component)
├── hooks/
│   └── useAuth.tsx                 # Auth context provider (MODIFY)
├── pages/
│   └── auth/
│       ├── login.tsx               # Login page (ADD redirect logic)
│       └── signup.tsx              # Signup page (ADD redirect logic)
├── services/
│   └── authService.ts              # API client for auth (REVIEW for /auth/me)
└── theme/
    ├── Root.tsx                    # Global wrapper (REVIEW)
    └── Navbar/                     # (CREATE via swizzle if needed)
        └── index.tsx               # Custom navbar (CREATE)

tests/
└── components/
    ├── Auth/
    │   └── AuthGuard.test.tsx      # (CREATE - test auth guard)
    ├── Navbar/
    │   └── UserDropdown.test.tsx   # (CREATE - test user dropdown)
    └── ChatbotWidget/
        └── ChatbotWidget.test.tsx  # (MODIFY - add visibility tests)
```

**Structure Decision**: This is a Docusaurus web application with custom React components in `src/`. The feature will modify existing authentication components (`useAuth`, `AuthGuard`, `ChatbotWidget`) and create new UI components for the navbar user dropdown. Docusaurus theme swizzling may be required to customize the navbar. Tests will be added/modified in the `tests/` directory following the existing Jest + React Testing Library setup.

## Complexity Tracking

No constitutional violations detected - this section is not applicable.
