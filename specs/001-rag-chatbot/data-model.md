# Data Model: RAG Chatbot

**Feature**: 001-rag-chatbot
**Date**: 2025-12-06
**Source**: Extracted from spec.md functional requirements and research decisions

## Entities

### 1. User

**Purpose**: Represents an authenticated reader with account credentials and session information.

**Attributes**:
- `id` (UUID): Unique user identifier (primary key)
- `email` (String, 255 chars): User's email address (unique, required)
- `password_hash` (String, 255 chars): Hashed password (managed by Better Auth, required)
- `created_at` (Timestamp): Account creation time
- `updated_at` (Timestamp): Last account modification time

**Relationships**:
- One-to-many with `ChatMessage` (a user has many messages)
- One-to-many with `Session` (a user can have multiple active sessions)

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Email must be unique across all users
- Password must meet minimum strength requirements (handled by Better Auth: min 8 chars, 1 uppercase, 1 number, 1 special char)

**State Transitions**: None (static entity, no state machine)

---

### 2. Session

**Purpose**: Represents an active authentication session with JWT tokens and expiration.

**Attributes**:
- `id` (UUID): Unique session identifier (primary key)
- `user_id` (UUID): Foreign key to User (required)
- `token_hash` (String, 255 chars): Hashed JWT token (unique, required)
- `expires_at` (Timestamp): Session expiration time (required)
- `created_at` (Timestamp): Session creation time

**Relationships**:
- Many-to-one with `User` (a session belongs to one user)

**Validation Rules**:
- `expires_at` must be in the future when session is created
- Token hash must be unique across all sessions
- Sessions automatically expire when `expires_at` is reached (handled by Better Auth)

**State Transitions**: None (sessions are created and deleted, no intermediate states)

---

### 3. ChatMessage

**Purpose**: Represents a single question-answer exchange in the chatbot, linked to a user and OpenAI thread.

**Attributes**:
- `id` (UUID): Unique message identifier (primary key)
- `user_id` (UUID): Foreign key to User (required)
- `thread_id` (String, 255 chars): OpenAI Agents SDK thread identifier (required)
- `role` (Enum: 'user' | 'assistant'): Message sender (required)
- `content` (Text): Message text content (required)
- `metadata` (JSONB): Additional context (optional, default: `{}`)
  - `query_mode` (String): 'full_book' or 'selection'
  - `selected_text` (String): User-selected text (if `query_mode` is 'selection')
  - `chunk_ids` (Array of Strings): Qdrant vector IDs used for response (assistant messages only)
  - `response_time_ms` (Integer): Time to generate response (assistant messages only)
- `created_at` (Timestamp): Message creation time

**Relationships**:
- Many-to-one with `User` (a message belongs to one user)
- Many-to-one with `Thread` (logical grouping by `thread_id`, not enforced by FK)

**Validation Rules**:
- `role` must be either 'user' or 'assistant'
- `content` must not be empty (min 1 character)
- `content` max length: 10,000 characters (prevents abuse)
- `thread_id` must match OpenAI thread format (e.g., `thread_abc123`)
- If `role` is 'user' and `metadata.query_mode` is 'selection', `metadata.selected_text` must be present

**State Transitions**: None (messages are immutable once created)

---

### 4. BookContentChunk (Qdrant Collection)

**Purpose**: Represents a section of book content stored as a vector embedding for semantic search.

**Attributes** (Qdrant Payload):
- `vector` (Array of Floats, 1536 dimensions): Embedding from `text-embedding-3-small`
- `content` (String): Original text chunk (required)
- `chapter` (String): Chapter name (e.g., "Module 1: ROS 2", required)
- `section` (String): Section heading (e.g., "1.2 Nodes and Topics", required)
- `page_number` (Integer): Approximate page number (optional)
- `heading` (String): Section/subsection heading (required)
- `chunk_index` (Integer): Position in section (0-indexed, required)
- `word_count` (Integer): Number of words in chunk (required)
- `doc_version` (String): Book version identifier (e.g., "v1.0.0", required)

**Relationships**: None (stored in Qdrant, no relational database links)

**Validation Rules**:
- `content` must not be empty
- `content` max length: 2,000 characters (enforced by chunking strategy)
- `word_count` should be approximately 500 ± 200 words
- `chunk_index` must be >= 0
- `vector` must have exactly 1536 dimensions

**Indexing**:
- HNSW index on vector field for fast approximate nearest neighbor search
- No additional indexes (Qdrant optimized for vector similarity)

---

## Entity Relationships Diagram

```
┌─────────────────┐
│     User        │
│─────────────────│
│ id (PK)         │
│ email           │
│ password_hash   │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────┴────────┐        ┌──────────────────────┐
│    Session      │        │    ChatMessage       │
│─────────────────│        │──────────────────────│
│ id (PK)         │        │ id (PK)              │
│ user_id (FK)    │        │ user_id (FK)         │
│ token_hash      │        │ thread_id            │
│ expires_at      │        │ role                 │
│ created_at      │        │ content              │
└─────────────────┘        │ metadata (JSONB)     │
                           │ created_at           │
                           └──────────────────────┘
                                    │
                                    │ Logical grouping by thread_id
                                    │ (no FK enforcement)
                                    ▼
                           ┌──────────────────────┐
                           │ OpenAI Thread        │
                           │ (External, not in DB)│
                           └──────────────────────┘

┌─────────────────────────────────┐
│  BookContentChunk (Qdrant)      │
│─────────────────────────────────│
│ vector (1536 floats)            │
│ content                         │
│ chapter                         │
│ section                         │
│ page_number                     │
│ heading                         │
│ chunk_index                     │
│ word_count                      │
│ doc_version                     │
└─────────────────────────────────┘
(No relational links - queried via similarity search)
```

---

## Database Schema (PostgreSQL - Neon)

```sql
-- Users table (managed by Better Auth)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

-- Sessions table (managed by Better Auth)
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_expiration CHECK (expires_at > created_at)
);

-- Chat messages table
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    thread_id VARCHAR(255) NOT NULL,
    role VARCHAR(10) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL CHECK (char_length(content) > 0 AND char_length(content) <= 10000),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX idx_chat_messages_thread_id ON chat_messages(thread_id);
CREATE INDEX idx_chat_messages_created_at ON chat_messages(created_at DESC);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update updated_at on user modifications
CREATE TRIGGER update_user_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

---

## Vector Database Schema (Qdrant)

**Collection Name**: `humanoid-robotics-book-v1`

**Vector Configuration**:
```python
from qdrant_client.models import Distance, VectorParams

collection_config = VectorParams(
    size=1536,  # text-embedding-3-small dimensions
    distance=Distance.COSINE  # Cosine similarity for semantic search
)
```

**Payload Schema** (TypeScript representation):
```typescript
interface BookContentChunkPayload {
    content: string;          // Original text chunk
    chapter: string;          // "Module 1: ROS 2"
    section: string;          // "1.2 Nodes and Topics"
    page_number?: number;     // Approximate page number
    heading: string;          // Section heading
    chunk_index: number;      // Position in section (0, 1, 2, ...)
    word_count: number;       // Number of words in chunk
    doc_version: string;      // "v1.0.0"
}
```

**Example Qdrant Point**:
```json
{
    "id": "chunk_001_001_000",
    "vector": [0.123, -0.456, 0.789, ...],  // 1536 floats
    "payload": {
        "content": "ROS 2 is the Robot Operating System version 2, a framework for building robot applications...",
        "chapter": "Module 1: ROS 2",
        "section": "1.1 Introduction to ROS 2",
        "page_number": 12,
        "heading": "What is ROS 2?",
        "chunk_index": 0,
        "word_count": 487,
        "doc_version": "v1.0.0"
    }
}
```

---

## Data Flow: User Query to Response

```
1. User submits question
   ↓
2. Frontend sends POST /api/chat with:
   {
       "message": "What is a ROS 2 node?",
       "thread_id": "thread_abc123" (optional, for continuing conversation),
       "query_mode": "full_book" | "selection",
       "selected_text": "..." (if query_mode is selection)
   }
   ↓
3. Backend (FastAPI):
   a. Validate JWT token (middleware)
   b. Extract user_id from token
   c. Validate input (sanitize message, check length)
   d. Rate limit check (20 queries/minute per user)
   ↓
4. RAG Service:
   a. Create/resume OpenAI thread
   b. If query_mode == "full_book":
      - Embed user message with text-embedding-3-small
      - Query Qdrant: retrieve top 5 similar chunks (cosine similarity)
   c. If query_mode == "selection":
      - Embed selected_text with text-embedding-3-small
      - Query Qdrant: retrieve top 3 chunks from selected text context
   d. Construct context from retrieved chunks
   e. Send message + context to OpenAI Agents SDK
   f. Receive response from OpenAI
   ↓
5. Chat Service:
   a. Store user message in chat_messages table:
      {user_id, thread_id, role: 'user', content, metadata: {query_mode, selected_text}}
   b. Store assistant response in chat_messages table:
      {user_id, thread_id, role: 'assistant', content, metadata: {chunk_ids, response_time_ms}}
   ↓
6. Return response to frontend
   ↓
7. Frontend displays message in chat UI
```

---

## Migrations and Versioning

### Database Migrations (PostgreSQL)
- Use Alembic for schema migrations
- Migration files stored in `backend/migrations/`
- Initial migration: `001_create_users_sessions_messages_tables.sql`
- Version control all migrations in Git

### Vector Database Versioning (Qdrant)
- Create new collections for major book updates: `humanoid-robotics-book-v2`
- Allows A/B testing of different chunking strategies
- Old collections can be deleted after migration is complete

### Data Retention Policy
- Chat messages: Retain indefinitely (user conversation history)
- Sessions: Auto-expire after 7 days (handled by Better Auth)
- Vector embeddings: Retain all versions for rollback capability

---

## Performance Considerations

### Database Indexes
- Composite index on `(user_id, created_at DESC)` for efficient chat history retrieval
- Partial index on `sessions.expires_at` for active sessions: `WHERE expires_at > NOW()`

### Query Optimization
- Limit chat history queries to last 100 messages per thread (pagination for older messages)
- Cache frequently queried vector results in Redis (TTL: 1 hour)
- Use connection pooling for Postgres (SQLAlchemy with pool size: 10)

### Scaling Limits (Free Tier Constraints)
- **Neon Postgres**: 0.5GB storage → ~50K chat messages (estimated 10KB per message with metadata)
- **Qdrant Free Tier**: 1GB storage → ~10K vector chunks (1536 floats × 4 bytes + payload ~= 100KB per chunk)
- If limits exceeded: Implement data archival (move old messages to S3) or upgrade to paid tier
