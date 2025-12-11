# Implementation Plan: Integrated RAG Chatbot for Book Content

**Branch**: `001-rag-chatbot` | **Date**: 2025-12-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an authenticated RAG chatbot embedded within the Docusaurus-published humanoid robotics textbook. The chatbot enables readers to ask natural language questions about book content, with support for both full-book queries and selected-text-only queries. The system uses OpenAI Agents SDK for orchestration, Qdrant for vector search, Neon Postgres for user/chat data, Better Auth for authentication, and OpenAI ChatKit for the UI. Backend services are containerized with Docker and feature a dark, minimalistic theme consistent with the book's design.

## Technical Context

**Language/Version**: Python 3.11+ (backend), JavaScript/TypeScript ES2022+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI 0.104+, OpenAI Python SDK, Qdrant Client, psycopg3, Better Auth Python SDK
- Frontend: React 18+, OpenAI ChatKit SDK, Better Auth React components, Docusaurus 3.x
**Storage**: Neon Serverless Postgres (user accounts, chat history), Qdrant Cloud Free Tier (vector embeddings)
**Testing**: pytest (backend), Jest + React Testing Library (frontend), Playwright (e2e)
**Target Platform**: Linux server (Docker containers), modern web browsers (Chrome, Firefox, Safari)
**Project Type**: Web application (backend API + frontend integration)
**Performance Goals**:
- Chatbot response: <5s p95 latency
- Vector search: <2s query time
- Landing page load: <3s
- Support 50 concurrent users
**Constraints**:
- Qdrant Free Tier: 1GB storage, 100K vectors max
- Neon Free Tier: 0.5GB storage, 1 database
- OpenAI API rate limits: Tier-dependent (assume Tier 1: 500 RPM)
- Better Auth: HTTPS required
**Scale/Scope**:
- Book content: ~300-500 pages (estimated 150K-250K words)
- Expected users: <1000 initial users
- Chat history: ~100 messages per user average
- Vector embeddings: ~5K-10K chunks (assuming 500-word chunks)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Accessibility First ✅ PASS
- Chatbot UI uses clear, simple language for prompts and error messages
- Authentication flows use Better Auth UI components (designed for accessibility)
- Dark theme with high contrast for readability
- No complex jargon in user-facing interfaces

### Principle II: Systems Understanding Over Implementation ✅ PASS
- Feature enhances the textbook (an informational resource) without requiring coding
- Chatbot provides explanations of book content, not labs or exercises
- Focus on understanding humanoid robotics concepts through conversational AI

### Principle III: Modular Structure ⚠️ NOT APPLICABLE
- This feature is infrastructure (chatbot), not textbook content
- Does not add or modify book modules/chapters
- Supports existing modular content structure

### Principle IV: Visual and Narrative Clarity ✅ PASS
- Landing page includes visual descriptions of chatbot capabilities
- ChatKit UI provides clear visual feedback (typing indicators, message history)
- Dark, minimalistic theme consistent with book design

### Principle V: Consistency and Terminology Standards ✅ PASS
- Chatbot responses reference book terminology consistently
- Vector search retrieves exact book sections (preserves original terminology)
- No new technical terms introduced to readers

### Principle VI: Practical Connection to Physical AI ✅ PASS
- Chatbot helps readers understand Physical AI concepts from the textbook
- Queries about ROS 2, Gazebo, NVIDIA Isaac, VLA answered from book content
- Direct connection: assists learning of humanoid robotics material

### Principle VII: Docusaurus and MDX Compliance ✅ PASS
- Chatbot UI embedded as React component in Docusaurus pages
- Landing page created as custom MDX page
- No breaking changes to Docusaurus build process
- Uses Docusaurus theming system for dark mode

**Overall Status**: ✅ PASS - No violations. Feature supports textbook mission without compromising principles.

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── api-spec.yaml    # OpenAPI specification for FastAPI backend
│   └── events.md        # Event schemas (if applicable)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py                 # FastAPI application entry
│   ├── config/
│   │   ├── settings.py         # Environment configuration
│   │   └── database.py         # Postgres + Qdrant connection setup
│   ├── models/
│   │   ├── user.py             # User model (Better Auth integration)
│   │   ├── chat_message.py     # Chat message model
│   │   └── schemas.py          # Pydantic request/response schemas
│   ├── services/
│   │   ├── auth_service.py     # Better Auth integration
│   │   ├── rag_service.py      # RAG orchestration (OpenAI Agents SDK)
│   │   ├── vector_service.py   # Qdrant vector operations
│   │   └── chat_service.py     # Chat history management
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py         # Authentication endpoints
│   │   │   ├── chat.py         # Chat endpoints
│   │   │   └── health.py       # Health check
│   │   └── middleware/
│   │       ├── auth_middleware.py    # JWT verification
│   │       └── rate_limit.py         # Rate limiting
│   └── utils/
│       ├── embedding.py        # Text chunking + embedding logic
│       ├── validators.py       # Input validation/sanitization
│       └── logger.py           # Logging configuration
├── tests/
│   ├── unit/
│   │   ├── test_rag_service.py
│   │   ├── test_vector_service.py
│   │   └── test_validators.py
│   ├── integration/
│   │   ├── test_auth_flow.py
│   │   ├── test_chat_flow.py
│   │   └── test_vector_search.py
│   └── contract/
│       └── test_api_spec.py
├── scripts/
│   ├── embed_book_content.py  # One-time script to embed book content
│   └── seed_database.py       # Database initialization
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example

frontend/ (integrated into existing Docusaurus site)
├── src/
│   ├── components/
│   │   ├── ChatbotWidget/
│   │   │   ├── ChatbotWidget.tsx        # Main chatbot component (ChatKit wrapper)
│   │   │   ├── SelectionModeIndicator.tsx  # Shows when in selection mode
│   │   │   └── ChatbotWidget.module.css    # Dark theme styles
│   │   ├── Auth/
│   │   │   ├── LoginForm.tsx            # Better Auth login component
│   │   │   ├── SignupForm.tsx           # Better Auth signup component
│   │   │   └── AuthGuard.tsx            # HOC for protected routes
│   │   └── LandingPage/
│   │       ├── CustomHero.tsx           # Custom landing page hero section
│   │       ├── ChatbotFeatureShowcase.tsx  # Feature description
│   │       └── LandingPage.module.css      # Dark theme styles
│   ├── hooks/
│   │   ├── useAuth.ts                   # Better Auth hook
│   │   ├── useChatbot.ts                # Chatbot API integration
│   │   └── useTextSelection.ts          # Text selection handling
│   ├── services/
│   │   ├── apiClient.ts                 # Axios/Fetch wrapper for backend
│   │   └── authService.ts               # Better Auth service
│   ├── pages/
│   │   ├── index.mdx                    # Custom landing page (replaces default)
│   │   └── auth/
│   │       ├── login.tsx                # Login page
│   │       └── signup.tsx               # Signup page
│   └── theme/
│       └── custom.css                   # Dark, minimalistic theme overrides
├── tests/
│   ├── components/
│   │   ├── ChatbotWidget.test.tsx
│   │   └── AuthGuard.test.tsx
│   └── e2e/
│       ├── auth-flow.spec.ts
│       └── chatbot-interaction.spec.ts
└── docusaurus.config.js                # Updated configuration

shared/
└── types/
    ├── user.ts                          # Shared TypeScript types
    ├── chat.ts
    └── api.ts
```

**Structure Decision**: Web application structure selected due to separate backend (FastAPI) and frontend (Docusaurus/React) requirements. Backend containerized with Docker; frontend integrated into existing Docusaurus site. Shared TypeScript types ensure consistency between frontend and API contracts.

## Complexity Tracking

> **No Constitution violations - this section is not needed.**

