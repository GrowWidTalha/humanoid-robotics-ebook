# Research: RAG Chatbot Technical Decisions

**Feature**: 001-rag-chatbot
**Date**: 2025-12-06
**Purpose**: Resolve technical unknowns and document architectural decisions for RAG chatbot implementation

## Research Areas

### 1. OpenAI Agents SDK Integration

**Decision**: Use OpenAI Agents SDK (formerly Assistants API) for RAG orchestration

**Rationale**:
- Native support for retrieval-augmented generation workflows
- Built-in conversation state management
- Function calling for dynamic vector retrieval
- Simplified integration with OpenAI models (GPT-4, GPT-3.5-turbo)
- Official SDK reduces custom orchestration code

**Alternatives Considered**:
- **LangChain**: More flexible but adds complexity; requires custom RAG pipeline construction
- **LlamaIndex**: Excellent for RAG but less mature ecosystem for production deployments
- **Custom orchestration**: Maximum control but significant development overhead

**Best Practices**:
- Use Assistants API with retrieval tool enabled for document-based Q&A
- Implement streaming responses for better UX (show chunks as they arrive)
- Store thread IDs in database to maintain conversation continuity
- Use function calling for dynamic vector search (pass selected text as context)
- Implement retry logic with exponential backoff for API failures

**Integration Pattern**:
```
User Question → FastAPI Endpoint → RAG Service
                                    ↓
                            Create/Resume Thread
                                    ↓
                            Query Qdrant (retrieve top-k chunks)
                                    ↓
                            OpenAI Agents SDK (generate response with context)
                                    ↓
                            Store message in Postgres
                                    ↓
                            Return response to user
```

---

### 2. Better Auth Integration Strategy

**Decision**: Use Better Auth with session-based authentication (JWT tokens in HTTP-only cookies)

**Rationale**:
- Modern, secure authentication library with React + Python support
- Built-in CSRF protection, session management, and token refresh
- Reduces custom auth code (password hashing, token generation, email verification)
- Provides pre-built React components (login, signup, password reset)
- HTTPS-only cookies prevent XSS attacks on tokens

**Alternatives Considered**:
- **Auth0/Clerk**: Third-party services add cost and external dependencies
- **Custom JWT implementation**: High risk of security vulnerabilities
- **OAuth2 only**: Requires external providers (Google, GitHub), limits accessibility

**Best Practices**:
- Store JWT tokens in HTTP-only cookies (not localStorage or sessionStorage)
- Implement CSRF tokens for state-changing operations
- Use short-lived access tokens (15 minutes) with refresh tokens (7 days)
- Validate tokens in FastAPI middleware before processing requests
- Log authentication events (login, logout, failed attempts) for security auditing

**Integration Pattern**:
```
Frontend (Better Auth React)
    ↓
Login/Signup → POST /auth/login or /auth/register
    ↓
Better Auth Python SDK (FastAPI)
    ↓
Verify credentials → Generate JWT → Set HTTP-only cookie
    ↓
Middleware validates JWT on subsequent requests
    ↓
Attach user_id to request context → Proceed to protected endpoint
```

---

### 3. Qdrant Vector Database Configuration

**Decision**: Use Qdrant Cloud Free Tier with cosine similarity and HNSW indexing

**Rationale**:
- Optimized for semantic search with high recall
- HNSW (Hierarchical Navigable Small World) provides fast approximate nearest neighbor search
- Cosine similarity ideal for text embeddings (captures semantic meaning)
- Free tier sufficient for book content (1GB storage, 100K vectors)
- Cloud-hosted reduces infrastructure management

**Alternatives Considered**:
- **Pinecone**: Similar features but more expensive free tier
- **Weaviate**: Open-source but requires self-hosting
- **PostgreSQL pgvector**: Simpler but slower for large-scale vector search

**Best Practices**:
- Chunk book content into 500-word segments with 50-word overlap (prevents context loss at chunk boundaries)
- Use OpenAI `text-embedding-3-small` model (1536 dimensions, cost-effective)
- Store metadata with each vector: `{chapter, section, page_number, heading, content}`
- Create collections per book version (allows A/B testing of chunking strategies)
- Implement caching for frequently queried vectors (reduces API costs)

**Chunking Strategy**:
- **Markdown-aware chunking**: Split on headings (`##`, `###`) to preserve logical structure
- **Fallback to word count**: If section >500 words, split into 500-word chunks with 50-word overlap
- **Preserve code blocks**: Keep code examples intact within chunks (don't split mid-code)
- **Metadata enrichment**: Add chapter/section context to each chunk for better retrieval

**Collection Schema**:
```python
{
    "vector": [1536 floats],  # text-embedding-3-small
    "payload": {
        "content": str,       # Original text chunk
        "chapter": str,       # "Module 1: ROS 2"
        "section": str,       # "1.2 Nodes and Topics"
        "page_number": int,   # Approximate page number
        "heading": str,       # Section heading
        "chunk_index": int,   # Position in section (0, 1, 2...)
        "word_count": int,    # Length of chunk
        "doc_version": str    # "v1.0.0"
    }
}
```

---

### 4. OpenAI ChatKit UI Integration

**Decision**: Use OpenAI ChatKit React SDK with custom theming for dark mode

**Rationale**:
- Official OpenAI UI library designed for chat interfaces
- Pre-built components: message list, input box, typing indicators
- Supports streaming responses (displays tokens as they arrive)
- Customizable theming via CSS modules
- Reduces custom UI development time

**Alternatives Considered**:
- **Custom chat UI**: More control but significant development time
- **react-chatbot-kit**: Community library, less maintained
- **Botpress UI**: Heavy-weight, designed for bot builders (overkill)

**Best Practices**:
- Implement text selection detection with `window.getSelection()`
- Show selection mode indicator when text is highlighted
- Use CSS modules for scoped styling (prevents Docusaurus theme conflicts)
- Implement optimistic updates (show user message immediately, update after API confirms)
- Add error boundaries to catch and display chat failures gracefully

**Dark Theme Customization**:
```css
/* ChatbotWidget.module.css */
.chatContainer {
  background-color: #1a1a1a;
  color: #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.messageUser {
  background-color: #2c5aa0;
  color: #ffffff;
}

.messageAssistant {
  background-color: #2a2a2a;
  color: #e0e0e0;
}

.inputBox {
  background-color: #2a2a2a;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
}
```

---

### 5. Neon Serverless Postgres Schema Design

**Decision**: Use normalized schema with separate tables for users, chat_messages, and sessions

**Rationale**:
- Normalized design prevents data duplication and ensures consistency
- Separate sessions table allows Better Auth to manage token lifecycle
- Indexes on frequently queried columns (user_id, created_at) improve performance
- JSONB for metadata allows flexible storage without schema migrations

**Alternatives Considered**:
- **Denormalized schema**: Faster reads but data duplication and update anomalies
- **NoSQL (MongoDB)**: Better Auth requires SQL database for session management
- **Single table design**: Simpler but harder to query and maintain

**Schema**:
```sql
-- Users table (managed by Better Auth)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Sessions table (managed by Better Auth)
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Chat messages table
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    thread_id VARCHAR(255) NOT NULL,  -- OpenAI thread ID
    role VARCHAR(10) CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',  -- {query_mode: 'full_book' | 'selection', selected_text: str, ...}
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX idx_chat_messages_thread_id ON chat_messages(thread_id);
CREATE INDEX idx_chat_messages_created_at ON chat_messages(created_at DESC);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

---

### 6. Docker Containerization Strategy

**Decision**: Use Docker Compose with multi-stage builds for production-ready images

**Rationale**:
- Multi-stage builds reduce image size (separate build and runtime dependencies)
- Docker Compose simplifies local development (backend + Postgres + Qdrant in one command)
- Environment variables for configuration (12-factor app principles)
- Health checks ensure services are ready before accepting traffic

**Alternatives Considered**:
- **Single Dockerfile**: Simpler but larger images and slower builds
- **Kubernetes**: Overkill for <1000 users, adds operational complexity
- **Serverless (AWS Lambda)**: Cold start latency incompatible with <5s response target

**Best Practices**:
- Use `.dockerignore` to exclude unnecessary files (tests, .git, node_modules)
- Pin dependency versions in requirements.txt (prevents unexpected breakages)
- Run as non-root user for security
- Implement health check endpoints (`/health`) for container orchestration

**Dockerfile (multi-stage)**:
```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 7. Text Selection and Context Injection

**Decision**: Use browser's `window.getSelection()` API with custom event listeners

**Rationale**:
- Native browser API, no additional dependencies
- Works across all modern browsers (Chrome, Firefox, Safari)
- Can extract exact text and position on page
- Integrates with React component lifecycle via `useEffect`

**Alternatives Considered**:
- **rangy library**: Adds dependency for minimal benefit
- **Custom text tracking**: Complex to implement and maintain
- **Server-side parsing**: Cannot access client-side selection state

**Best Practices**:
- Debounce selection events (wait 300ms after user stops selecting)
- Clear selection mode when user clicks outside chatbot
- Send selected text to backend as `context` parameter in query
- Display indicator in chat UI showing selection mode is active

**Implementation Pattern**:
```typescript
// useTextSelection.ts
export function useTextSelection() {
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    const handleSelection = debounce(() => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim().length > 0) {
        setSelectedText(selection.toString().trim());
      }
    }, 300);

    document.addEventListener('selectionchange', handleSelection);
    return () => document.removeEventListener('selectionchange', handleSelection);
  }, []);

  return { selectedText, clearSelection: () => setSelectedText('') };
}
```

---

### 8. Rate Limiting and Security

**Decision**: Use FastAPI's SlowAPI for rate limiting with Redis backend (or in-memory for MVP)

**Rationale**:
- Prevents abuse (e.g., scripted attacks, excessive queries)
- Protects OpenAI API quota and costs
- SlowAPI integrates natively with FastAPI decorators
- Redis allows distributed rate limiting across multiple backend instances

**Alternatives Considered**:
- **Nginx rate limiting**: Works but less flexible (cannot rate-limit per user)
- **Custom middleware**: Reinventing the wheel, higher maintenance
- **No rate limiting**: Exposes system to abuse and cost overruns

**Best Practices**:
- Rate limit per user (20 queries/minute) using user_id from JWT
- Global rate limit for unauthenticated endpoints (100 requests/minute per IP)
- Return 429 Too Many Requests with `Retry-After` header
- Log rate limit violations for abuse detection

**Security Checklist**:
- ✅ Input validation: Sanitize all user inputs (questions, selected text)
- ✅ SQL injection prevention: Use parameterized queries (SQLAlchemy/psycopg3)
- ✅ XSS prevention: Escape user-generated content in UI (React handles this by default)
- ✅ CSRF protection: Better Auth provides CSRF tokens
- ✅ HTTPS only: Enforce in production (Better Auth requirement)
- ✅ Secrets management: Use environment variables (never commit to Git)
- ✅ Logging: Log security events (failed logins, rate limit violations)

---

## Summary of Decisions

| Area | Decision | Primary Benefit |
|------|----------|----------------|
| RAG Orchestration | OpenAI Agents SDK | Native RAG support, simplified integration |
| Authentication | Better Auth (session-based JWT) | Security best practices, pre-built components |
| Vector Database | Qdrant Cloud (cosine similarity, HNSW) | Fast semantic search, managed service |
| Chat UI | OpenAI ChatKit with custom dark theme | Pre-built chat components, OpenAI integration |
| Database Schema | Normalized PostgreSQL (users, sessions, messages) | Data consistency, Better Auth compatibility |
| Containerization | Docker Compose with multi-stage builds | Smaller images, local dev simplicity |
| Text Selection | Native `window.getSelection()` API | No dependencies, cross-browser support |
| Rate Limiting | SlowAPI with per-user limits (20 qpm) | Abuse prevention, cost control |

---

## Open Questions for Implementation Phase

1. **Embedding model selection**: Confirm `text-embedding-3-small` (1536d) vs. `text-embedding-3-large` (3072d) based on accuracy benchmarks
2. **Chunking overlap**: Test 50-word vs. 100-word overlap for optimal context preservation
3. **Error handling**: Define user-facing error messages for common failures (API timeout, no results found, session expired)
4. **Monitoring**: Decide on observability stack (Prometheus + Grafana vs. cloud provider metrics)
5. **Deployment**: Confirm hosting environment (AWS, GCP, Azure, DigitalOcean) for Docker containers

These will be addressed during task generation and implementation phases.
