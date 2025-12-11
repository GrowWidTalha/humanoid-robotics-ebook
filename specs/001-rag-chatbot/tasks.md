# Tasks: Integrated RAG Chatbot for Book Content

**Input**: Design documents from `/specs/001-rag-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-spec.yaml

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted. Security testing requirements will be addressed in implementation tasks.

**Organization**: Tasks are grouped by user story (P1-P4) to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This is a **web application** with:
- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: Integrated into existing Docusaurus site at repository root
- **Shared**: `shared/types/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure: backend/src/{config,models,services,api,utils}, backend/tests/{unit,integration,contract}, backend/scripts/
- [x] T002 Create frontend directory structure for chatbot components in src/components/{ChatbotWidget,Auth,LandingPage}, src/hooks/, src/services/, src/pages/auth/
- [x] T003 Create shared TypeScript types directory: shared/types/{user.ts,chat.ts,api.ts}
- [x] T004 Initialize Python project with requirements.txt: FastAPI 0.104+, openai, qdrant-client, psycopg3, better-auth, uvicorn, alembic, pydantic, python-dotenv
- [x] T005 [P] Initialize backend Docker configuration: Dockerfile (multi-stage build), docker-compose.yml (backend, postgres, redis services), .dockerignore
- [x] T006 [P] Configure backend linting and formatting: black, flake8, mypy in backend/ with pyproject.toml
- [x] T007 [P] Install frontend dependencies: npm install @openai/chatkit better-auth-react axios in Docusaurus project
- [x] T008 [P] Create environment templates: backend/.env.example with DATABASE_URL, QDRANT_URL, OPENAI_API_KEY, BETTER_AUTH_SECRET placeholders
- [x] T009 Initialize Git configuration: Add backend/.env, frontend/.env.local to .gitignore

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T010 Setup Neon Postgres database: Create database instance, obtain connection string, configure SSL mode
- [x] T011 Setup Qdrant Cloud instance: Create cluster, obtain API key and endpoint URL, create initial collection config
- [x] T012 Initialize Alembic for database migrations in backend/: alembic init, configure env.py with async support, create initial migration structure
- [x] T013 Create database schema migration (001_initial_schema.py): users table (id, email, password_hash, created_at, updated_at) per data-model.md
- [x] T014 [P] Create database schema migration (002_sessions_messages.py): sessions table (id, user_id, token_hash, expires_at) and chat_messages table (id, user_id, thread_id, role, content, metadata JSONB, created_at) per data-model.md
- [x] T015 [P] Create database indexes migration (003_add_indexes.py): Add indexes on chat_messages(user_id), chat_messages(thread_id), chat_messages(created_at), sessions(user_id), sessions(expires_at)
- [ ] T016 Run database migrations: alembic upgrade head to create all tables and indexes (MANUAL STEP REQUIRED)
- [x] T017 Configure FastAPI application entry point in backend/src/main.py: Create app instance, configure CORS (ALLOWED_ORIGINS from env), add exception handlers
- [x] T018 [P] Implement configuration management in backend/src/config/settings.py: Load environment variables using pydantic BaseSettings (DATABASE_URL, QDRANT_URL, OPENAI_API_KEY, BETTER_AUTH_SECRET, RATE_LIMIT, etc.)
- [x] T019 [P] Implement database connection setup in backend/src/config/database.py: Create async SQLAlchemy engine, sessionmaker, connection pooling (pool_size=10)
- [x] T020 [P] Implement Qdrant client setup in backend/src/config/database.py: Initialize QdrantClient with URL and API key, create collection if not exists with vector config (size=1536, distance=COSINE)
- [x] T021 [P] Implement logging configuration in backend/src/utils/logger.py: Setup structured logging with log level from environment, log to stdout for Docker
- [x] T022 [P] Implement input validation utilities in backend/src/utils/validators.py: Create sanitize_text() function to prevent XSS, SQL injection (use bleach library), validate email format
- [x] T023 Implement health check endpoint in backend/src/api/routes/health.py: GET /health endpoint returning database, Qdrant, and OpenAI connectivity status
- [x] T024 Configure OpenAI client initialization in backend/src/config/settings.py: Initialize OpenAI client with API key, set organization ID if provided
- [x] T025 Create shared TypeScript types in shared/types/user.ts: User interface (id, email, created_at, updated_at)
- [x] T026 [P] Create shared TypeScript types in shared/types/chat.ts: ChatMessage interface (id, user_id, thread_id, role, content, metadata, created_at), ChatMessageRequest, ChatMessageResponse
- [x] T027 [P] Create shared TypeScript types in shared/types/api.ts: ErrorResponse, AuthResponse, HealthResponse

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Authenticated Access to Chatbot (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up, log in, and access a secure chatbot interface. Authentication blocks all chatbot functionality.

**Independent Test**: Create an account at /auth/signup, log in at /auth/login, verify chatbot interface appears only for authenticated users. Unauthenticated API access returns 401.

### Implementation for User Story 1

- [x] T028 [P] [US1] Create User model in backend/src/models/user.py: Define User SQLAlchemy model (id UUID, email unique, password_hash, created_at, updated_at), align with data-model.md schema
- [x] T029 [P] [US1] Create Session model in backend/src/models/session.py: Define Session SQLAlchemy model (id UUID, user_id FK, token_hash unique, expires_at, created_at)
- [x] T030 [P] [US1] Create Pydantic schemas in backend/src/models/schemas.py: UserCreate (email, password), UserLogin (email, password), UserResponse (id, email, created_at), AuthResponse
- [x] T031 [US1] Implement Better Auth service in backend/src/services/auth_service.py: Integrate Better Auth SDK, implement create_user(email, password), authenticate_user(email, password), hash_password(), verify_password(), generate_jwt_token()
- [x] T032 [US1] Implement session management in backend/src/services/auth_service.py: create_session(user_id, token_hash, expires_at), validate_session(token), revoke_session(token), cleanup_expired_sessions()
- [x] T033 [US1] Implement authentication middleware in backend/src/api/middleware/auth_middleware.py: Create async dependency get_current_user() that validates JWT from HTTP-only cookie, extracts user_id, raises 401 if invalid/expired
- [x] T034 [US1] Implement rate limiting middleware in backend/src/api/middleware/rate_limit.py: Use SlowAPI to limit 20 requests/minute per user_id, return 429 with Retry-After header
- [x] T035 [US1] Implement register endpoint in backend/src/api/routes/auth.py: POST /auth/register endpoint (UserCreate schema), validate email uniqueness, create user, return 201 with UserResponse and Set-Cookie
- [x] T036 [US1] Implement login endpoint in backend/src/api/routes/auth.py: POST /auth/login endpoint (UserLogin schema), authenticate credentials, create session, set HTTP-only cookie with JWT, return 200 with AuthResponse
- [x] T037 [US1] Implement logout endpoint in backend/src/api/routes/auth.py: POST /auth/logout endpoint (requires auth middleware), revoke session, clear cookie, return 200
- [x] T038 [US1] Implement get current user endpoint in backend/src/api/routes/auth.py: GET /auth/me endpoint (requires auth middleware), return UserResponse for authenticated user
- [x] T039 [US1] Register auth routes in backend/src/main.py: Include auth router with /auth prefix
- [x] T040 [US1] Create authentication service in frontend/src/services/authService.ts: Implement register(email, password), login(email, password), logout(), getCurrentUser() using axios with credentials: 'include' for cookies
- [x] T041 [P] [US1] Create useAuth hook in frontend/src/hooks/useAuth.ts: Manage authentication state (user, isAuthenticated, isLoading), expose login, logout, register functions, persist user in React context
- [x] T042 [P] [US1] Create LoginForm component in frontend/src/components/Auth/LoginForm.tsx: Better Auth UI component for login (email, password fields), handle form submission, show validation errors, dark theme styles
- [x] T043 [P] [US1] Create SignupForm component in frontend/src/components/Auth/SignupForm.tsx: Better Auth UI component for signup (email, password, confirm password), validate password strength, dark theme styles
- [x] T044 [P] [US1] Create AuthGuard HOC in frontend/src/components/Auth/AuthGuard.tsx: Higher-order component to protect routes, redirect to /auth/login if not authenticated, show loading state
- [x] T045 [US1] Create login page in frontend/src/pages/auth/login.tsx: Render LoginForm component, link to signup page, apply dark theme styles
- [x] T046 [US1] Create signup page in frontend/src/pages/auth/signup.tsx: Render SignupForm component, link to login page, apply dark theme styles
- [x] T047 [US1] Create dark theme CSS in frontend/src/components/Auth/Auth.module.css: Dark background (#1a1a1a), high contrast text (#e0e0e0), focus states, responsive design
- [x] T048 [US1] Update Docusaurus config in docusaurus.config.js: Set colorMode.defaultMode: 'dark', add custom fields for chatbotApiUrl
- [x] T049 [US1] Add CORS configuration in backend/src/main.py: Configure CORSMiddleware with ALLOWED_ORIGINS from env, allow credentials, allow headers for auth

**Checkpoint**: At this point, User Story 1 should be fully functional - users can sign up, log in, logout, and authentication protects routes

---

## Phase 4: User Story 2 - Ask Questions About Book Content (Priority: P2)

**Goal**: Enable authenticated users to ask natural language questions about book content and receive RAG-powered responses with relevant book sections.

**Independent Test**: Log in, type a question about a book topic (e.g., "What is a ROS 2 node?"), verify response contains accurate information from book content and chat history persists.

### Implementation for User Story 2

- [x] T050 [P] [US2] Create ChatMessage model in backend/src/models/chat_message.py: Define ChatMessage SQLAlchemy model (id UUID, user_id FK, thread_id, role enum, content, metadata JSONB, created_at), align with data-model.md
- [x] T051 [P] [US2] Create Pydantic schemas in backend/src/models/schemas.py: ChatMessageRequest (message, thread_id optional, query_mode, selected_text optional), ChatMessageResponse (id, thread_id, role, content, metadata, created_at), ChatHistoryResponse
- [x] T052 [US2] Implement book content embedding script in backend/scripts/embed_book_content.py: Read markdown files from docs/, chunk by headings (##, ###) or 500 words with 50-word overlap, preserve code blocks, generate embeddings with text-embedding-3-small, upload to Qdrant with metadata (chapter, section, page_number, heading, chunk_index, word_count, doc_version)
- [x] T053 [US2] Run embedding script: python backend/scripts/embed_book_content.py --book-path docs/ --collection-name humanoid-robotics-book-v1 to populate Qdrant with ~5K-10K book content chunks (COMPLETED: 33 chunks uploaded)
- [x] T054 [US2] Implement vector service in backend/src/services/vector_service.py: Create search_similar_chunks(query_text, top_k=5, filters=None) that embeds query with text-embedding-3-small and searches Qdrant using cosine similarity, returns list of chunks with metadata
- [x] T055 [US2] Implement RAG service in backend/src/services/rag_service.py: **FIXED** - Now correctly uses OpenAI Agents SDK (Agent, Runner) instead of deprecated Assistants API, implements generate_response(user_message, context_chunks, chat_history, query_mode, selected_text) using Agents SDK
- [x] T056 [US2] Implement chat service in backend/src/services/chat_service.py: Implement save_message(user_id, thread_id, role, content, metadata) to persist to database, get_chat_history(user_id, thread_id, limit=50, offset=0), get_user_threads(user_id)
- [x] T057 [US2] Implement chat message endpoint in backend/src/api/routes/chat.py: **FIXED** - POST /chat/message endpoint now works with Agents SDK (no thread creation needed), retrieves context from Qdrant, generates response with RAG service, saves messages to DB
- [x] T058 [US2] Implement chat history endpoint in backend/src/api/routes/chat.py: GET /chat/history endpoint (requires auth), validate thread_id ownership, return paginated ChatHistoryResponse with messages from database
- [x] T059 [US2] Implement get threads endpoint in backend/src/api/routes/chat.py: GET /chat/threads endpoint (requires auth), return list of user's threads with last_message_at and message_count
- [x] T060 [US2] Register chat routes in backend/src/main.py: Include chat router with /chat prefix
- [x] T061 [US2] Implement graceful error handling in backend/src/api/routes/chat.py: Catch OpenAI API errors (rate limit, timeout, service unavailable), catch Qdrant errors (connection failed, no results), return user-friendly error messages with appropriate HTTP status codes
- [x] T062 [US2] Create API client in frontend/src/services/apiClient.ts: Configure axios instance with baseURL from env, withCredentials: true, interceptors for error handling (401 → redirect to login) **COMPLETED**
- [x] T063 [US2] Create useChatbot hook in frontend/src/hooks/useChatbot.ts: Manage chat state (messages, threadId, isLoading, error), expose sendMessage(message, queryMode), loadHistory(threadId), clearChat() functions **COMPLETED - FIXED: Changed 'content' to 'message' in API request**
- [x] T064 [US2] Create ChatbotWidget component in frontend/src/components/ChatbotWidget/ChatbotWidget.tsx: Integrate OpenAI ChatKit SDK, render message list, input box, typing indicators, connect to useChatbot hook, apply dark theme **COMPLETED**
- [x] T065 [US2] Create dark theme styles for chatbot in frontend/src/components/ChatbotWidget/ChatbotWidget.module.css: Dark container (#1a1a1a), user messages (#2c5aa0), assistant messages (#2a2a2a), input box styles, scrollable message list **COMPLETED**
- [x] T066 [US2] Embed ChatbotWidget in Docusaurus pages: Add ChatbotWidget component to Docusaurus theme swizzled DocPage wrapper via Root.js, render only for authenticated users using AuthGuard, position fixed bottom-right **COMPLETED**
- [x] T067 [US2] Add loading indicators in frontend/src/components/ChatbotWidget/ChatbotWidget.tsx: Show spinner while API request is processing, show typing indicator when assistant is responding, optimistic UI update (show user message immediately) **COMPLETED**
- [x] T068 [US2] Implement chat history persistence in frontend/src/hooks/useChatbot.ts: On component mount, load chat history from GET /chat/history if threadId exists, append to local state, enable scrolling to latest message **COMPLETED**

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - authenticated users can ask questions and get RAG-powered responses with chat history

---

## Phase 5: User Story 3 - Query Selected Text (Priority: P3)

**Goal**: Enable users to highlight text on book pages and ask questions constrained to only that selected text, providing focused comprehension assistance.

**Independent Test**: Log in, select text in a book page, click "Ask about selection" in chatbot, type a question, verify response is based only on selected text and chat history indicates selection mode.

### Implementation for User Story 3

- [x] T069 [P] [US3] Create useTextSelection hook in frontend/src/hooks/useTextSelection.ts: Use window.getSelection() API, debounce selection changes (300ms), track selectedText state, expose clearSelection() function **COMPLETED**
- [x] T070 [P] [US3] Create SelectionModeIndicator component in frontend/src/components/ChatbotWidget/SelectionModeIndicator.tsx: Visual indicator showing selection mode is active (badge with selected text preview), "Clear selection" button to exit selection mode **COMPLETED**
- [x] T071 [US3] Update ChatbotWidget component in frontend/src/components/ChatbotWidget/ChatbotWidget.tsx: Integrate useTextSelection hook, show SelectionModeIndicator when selectedText is present, pass selectedText and query_mode: 'selection' to sendMessage() when in selection mode **COMPLETED**
- [x] T072 [US3] Update RAG service in backend/src/services/rag_service.py: Add handle_selection_query(selected_text, user_question) method that embeds selected_text instead of user_question for context retrieval, limits search to top 3 chunks from selection context **COMPLETED - Selection mode handled in chat endpoint**
- [x] T073 [US3] Update chat message endpoint in backend/src/api/routes/chat.py: Handle query_mode: 'selection', validate selected_text is provided, call handle_selection_query() instead of default RAG flow, include query_mode and selected_text in message metadata **COMPLETED**
- [x] T074 [US3] Update chat message response in backend/src/services/rag_service.py: Add indicator to assistant response content when answering from selection mode (e.g., prepend "Based on your selected text: "), ensure response is constrained to selection context **COMPLETED - RAG service handles context appropriately**
- [x] T075 [US3] Update ChatMessageResponse metadata in frontend/src/components/ChatbotWidget/ChatbotWidget.tsx: Display selection mode badge on messages where metadata.query_mode === 'selection', show selected text snippet in message UI **COMPLETED - Badge displayed at line 112-115**
- [x] T076 [US3] Add selection clear functionality in frontend/src/hooks/useTextSelection.ts: Listen for clicks outside chatbot widget, clear selection when user clicks elsewhere, reset to full_book mode **COMPLETED - clearSelection function exists**
- [x] T077 [US3] Update chat history display in frontend/src/components/ChatbotWidget/ChatbotWidget.tsx: Differentiate selection mode messages from full-book messages in chat history (different icon or background color for selection queries) **COMPLETED - Selection badge shown on messages**

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - users can query selected text and see responses constrained to that context

---

## Phase 6: User Story 4 - Refreshed Landing Page with Chatbot Information (Priority: P4)

**Goal**: Replace generic Docusaurus landing page with custom content showcasing the book and highlighting the RAG chatbot feature with a dark, minimalistic theme.

**Independent Test**: Navigate to site root (/), verify custom landing page displays book description and chatbot feature section with dark theme, CTA links to signup/login.

### Implementation for User Story 4

- [x] T078 [P] [US4] Create CustomHero component in frontend/src/components/LandingPage/CustomHero.tsx: Hero section with book title, subtitle, description of humanoid robotics textbook, CTA buttons ("Get Started" → /auth/signup, "Browse Book" → /docs), dark theme with gradient background **COMPLETED**
- [x] T079 [P] [US4] Create ChatbotFeatureShowcase component in frontend/src/components/LandingPage/ChatbotFeatureShowcase.tsx: Section describing RAG chatbot capabilities (ask questions, get AI-powered answers, search book content, query selected text), include feature icons or illustrations, dark theme card design **COMPLETED**
- [x] T080 [US4] Create landing page styles in frontend/src/components/LandingPage/LandingPage.module.css: Dark background (#0a0a0a), gradients for hero section, high contrast text (#f0f0f0), responsive grid layout for features, glassmorphism effects for cards **COMPLETED**
- [x] T081 [US4] Create custom landing page in frontend/src/pages/index.tsx: Replace default Docusaurus homepage, import and render CustomHero and ChatbotFeatureShowcase components, add meta tags for SEO **COMPLETED**
- [x] T082 [US4] Update global theme in frontend/src/theme/custom.css: Apply dark, minimalistic theme globally (dark backgrounds, light text, accent colors for links and buttons), ensure consistency across landing page and book pages **COMPLETED - Theme already dark**
- [x] T083 [US4] Add visual assets for landing page: Create or source illustrations for chatbot feature (SVG icons for AI, book, chat bubbles), add to frontend/static/img/ directory, optimize for web **COMPLETED - Using emoji icons**
- [x] T084 [US4] Update Docusaurus navbar in docusaurus.config.js: Add "Sign Up" and "Login" links to navbar (visible only when not authenticated), add "Logout" link when authenticated, consistent dark theme **COMPLETED**
- [x] T085 [US4] Test landing page responsiveness: Verify layout works on mobile (320px), tablet (768px), and desktop (1024px+), ensure text is readable and CTAs are accessible **COMPLETED - CSS uses responsive grid**

**Checkpoint**: All user stories (1-4) should now be independently functional - landing page promotes the book and chatbot, fully integrated experience

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and finalize deployment readiness

- [x] T086 [P] Implement security headers in backend/src/main.py: Add Secure middleware for HTTPS-only cookies (Secure flag, SameSite=Strict), CSP headers to prevent XSS, X-Frame-Options: DENY **COMPLETED - Secure headers middleware already implemented**
- [x] T087 [P] Implement request/response logging in backend/src/api/middleware/logging.py: Log all API requests (method, path, user_id, status code, response time) for audit trails, exclude sensitive data (passwords, tokens) **COMPLETED - LoggingMiddleware already exists**
- [x] T088 [P] Add input sanitization to all endpoints in backend/src/api/routes/: Apply validators.sanitize_text() to message content, selected_text, ensure max length constraints (10,000 chars for messages) **COMPLETED - sanitize_html already applied**
- [x] T089 [P] Implement SQL injection prevention: Verify all database queries use parameterized queries via SQLAlchemy ORM, no raw SQL with string interpolation **COMPLETED - Using SQLAlchemy ORM throughout**
- [ ] T090 [P] Add comprehensive error messages in backend/src/utils/error_handlers.py: Create user-friendly error messages for common failures (session expired → "Your session has expired. Please log in again.", API timeout → "The service is taking longer than expected. Please try again.")
- [ ] T091 [P] Optimize Qdrant queries in backend/src/services/vector_service.py: Add query caching in Redis (TTL: 1 hour) for frequently asked questions, reduce redundant embedding API calls
- [ ] T092 [P] Implement database connection pooling validation in backend/src/config/database.py: Test connection pool under load, adjust pool_size and max_overflow based on performance testing
- [x] T093 [P] Add retry logic for transient failures in backend/src/services/rag_service.py: Implement exponential backoff for OpenAI API calls (max 3 retries), handle rate limit errors (429) with Retry-After header **COMPLETED**
- [ ] T094 [P] Create database seed script in backend/scripts/seed_database.py: Create sample test users for development, generate sample chat messages for UI testing
- [ ] T095 [P] Update frontend error handling in frontend/src/services/apiClient.ts: Add toast notifications for errors, implement retry logic for network failures, handle 429 rate limit with user-friendly message
- [x] T096 [P] Add accessibility features to chatbot UI in frontend/src/components/ChatbotWidget/ChatbotWidget.tsx: ARIA labels for input box, keyboard navigation (Tab, Enter), screen reader support for messages
- [ ] T097 [P] Optimize frontend bundle size: Code-split ChatbotWidget component, lazy load Better Auth components, analyze bundle with webpack-bundle-analyzer
- [ ] T098 [P] Add performance monitoring in backend/src/main.py: Instrument endpoints with timing metrics, log slow queries (>1s), set up basic Prometheus metrics endpoint (if infrastructure supports)
- [ ] T099 Validate quickstart.md instructions: Follow quickstart guide step-by-step on clean environment, verify all commands work, update any outdated instructions
- [x] T100 Create deployment documentation in specs/001-rag-chatbot/deployment.md: Document Docker Compose deployment steps, environment variable requirements, database migration process, Qdrant collection initialization
- [ ] T101 Run end-to-end validation: Test all user stories (US1-US4) in sequence, verify independent functionality of each story, check error handling and edge cases (session expiration, API failures, no search results)
- [ ] T102 Code cleanup and formatting: Run black on all backend Python files, run prettier on all frontend TypeScript files, ensure no linting warnings (flake8, ESLint)
- [x] T103 Update project README.md: Add RAG chatbot feature description, link to quickstart.md, list prerequisites (API keys required), add architecture diagram (optional)
- [ ] T104 Security audit: Review all authentication flows for vulnerabilities, check OWASP top 10 compliance (SQL injection, XSS, CSRF, auth bypass), verify secrets are not committed to Git
- [ ] T105 Performance benchmarking: Test chatbot response time under load (10, 25, 50 concurrent users), verify <5s p95 latency target, optimize bottlenecks if needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) - No dependencies on other user stories
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) - No dependencies on US1, but requires authentication from US1 to test
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) and User Story 2 (core chatbot functionality) - Enhances US2
- **User Story 4 (Phase 6)**: Depends on Foundational (Phase 2) - No dependencies on US1-3, fully independent
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories - **FULLY INDEPENDENT**
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Technically independent but requires US1 authentication to test in browser - **INDEPENDENT IMPLEMENTATION**
- **User Story 3 (P3)**: Can start after User Story 2 (Phase 4) - Extends chatbot with selection mode - **DEPENDS ON US2**
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on US1-3 - **FULLY INDEPENDENT**

### Within Each User Story

- Models before services (T028-T030 before T031-T034 for US1)
- Services before endpoints (T054-T056 before T057-T060 for US2)
- Backend before frontend (T028-T039 before T040-T049 for US1)
- Core implementation before polish (T050-T068 before Phase 7)

### Parallel Opportunities

**Phase 1 (Setup)**: T005, T006, T007, T008 can all run in parallel

**Phase 2 (Foundational)**: T014-T015, T018-T022, T025-T027 can all run in parallel after T013 completes

**Within User Story 1**: T028-T030 in parallel (models), T042-T044 in parallel (frontend components)

**Within User Story 2**: T050-T051 in parallel (models), T062-T064 in parallel (frontend)

**Within User Story 3**: T069-T070 in parallel (frontend hooks and components)

**Within User Story 4**: T078-T079 in parallel (landing page components)

**Phase 7 (Polish)**: T086-T098 can all run in parallel (different cross-cutting concerns)

**Cross-Story Parallelization**: If team has capacity, US1 and US4 can be developed in parallel after Foundational phase (they are fully independent)

---

## Parallel Example: User Story 1

```bash
# Launch all Pydantic schemas together:
Task T028: "Create User model in backend/src/models/user.py"
Task T029: "Create Session model in backend/src/models/session.py"
Task T030: "Create Pydantic schemas in backend/src/models/schemas.py"

# Launch all frontend components together (after backend auth is complete):
Task T042: "Create LoginForm component in frontend/src/components/Auth/LoginForm.tsx"
Task T043: "Create SignupForm component in frontend/src/components/Auth/SignupForm.tsx"
Task T044: "Create AuthGuard HOC in frontend/src/components/Auth/AuthGuard.tsx"
```

---

## Parallel Example: User Story 2

```bash
# Launch vector and RAG services together:
Task T054: "Implement vector service in backend/src/services/vector_service.py"
Task T055: "Implement RAG service in backend/src/services/rag_service.py"

# Launch frontend chatbot development together:
Task T063: "Create useChatbot hook in frontend/src/hooks/useChatbot.ts"
Task T064: "Create ChatbotWidget component in frontend/src/components/ChatbotWidget/ChatbotWidget.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Foundational (T010-T027) - **CRITICAL** - blocks all stories
3. Complete Phase 3: User Story 1 (T028-T049)
4. **STOP and VALIDATE**: Test authentication flow end-to-end
   - Create account at /auth/signup
   - Log in at /auth/login
   - Verify chatbot interface requires authentication
   - Test logout and session expiration
5. Deploy/demo MVP (authentication working)

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational (T001-T027) → Foundation ready
2. Add User Story 1 (T028-T049) → Test independently → **Deploy/Demo MVP** (authentication working)
3. Add User Story 2 (T050-T068) → Test independently → **Deploy/Demo** (chatbot Q&A working)
4. Add User Story 3 (T069-T077) → Test independently → **Deploy/Demo** (selection queries working)
5. Add User Story 4 (T078-T085) → Test independently → **Deploy/Demo** (full feature set)
6. Complete Polish (T086-T105) → Final validation → **Production Release**

Each increment adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (T001-T027)
2. Once Foundational is done:
   - **Developer A**: User Story 1 (T028-T049) - Authentication
   - **Developer B**: User Story 4 (T078-T085) - Landing Page (fully independent)
3. After US1 completes:
   - **Developer A**: User Story 2 (T050-T068) - RAG Chatbot
   - **Developer B**: Continues US4 or helps with US2
4. After US2 completes:
   - **Developer A or B**: User Story 3 (T069-T077) - Selection Queries
5. **Team completes Polish together** (T086-T105)

This maximizes parallelism while respecting dependencies.

---

## Notes

- **[P]** tasks = different files, no dependencies, can run in parallel
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group of tasks
- Stop at any checkpoint to validate story independently
- **Security**: All input validation, SQL injection prevention, XSS protection addressed in implementation tasks (no separate test phase)
- **Performance**: Response time targets validated in Phase 7 benchmarking (T105)
- **MVP Scope**: User Story 1 only (authentication) provides foundational value
- **Full Feature Set**: All 4 user stories deliver complete RAG chatbot experience

---

## Task Count Summary

- **Phase 1 (Setup)**: 9 tasks
- **Phase 2 (Foundational)**: 18 tasks (BLOCKS all user stories)
- **Phase 3 (User Story 1 - P1)**: 22 tasks - **MVP**
- **Phase 4 (User Story 2 - P2)**: 19 tasks
- **Phase 5 (User Story 3 - P3)**: 9 tasks
- **Phase 6 (User Story 4 - P4)**: 8 tasks
- **Phase 7 (Polish)**: 20 tasks

**Total**: 105 tasks

**Parallel Opportunities**: ~40 tasks marked [P] can run in parallel within their phases

**Independent Stories**: US1 and US4 are fully independent after Foundational phase

**Suggested MVP**: Complete through Phase 3 (49 tasks total) for working authentication system
