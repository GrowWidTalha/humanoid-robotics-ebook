# Quickstart Guide: RAG Chatbot Development

**Feature**: 001-rag-chatbot
**Audience**: Developers implementing the RAG chatbot feature
**Estimated Setup Time**: 30-45 minutes

## Prerequisites

Before starting development, ensure you have:

- **Python 3.11+** installed
- **Node.js 18+** and npm installed
- **Docker** and Docker Compose installed
- **Git** configured with repository access
- **API Keys** for:
  - OpenAI API (Tier 1 or higher recommended)
  - Qdrant Cloud account (Free Tier)
  - Neon Serverless Postgres database (Free Tier)

---

## Environment Setup

### 1. Clone Repository and Create Branch

```bash
# Ensure you're on the correct feature branch
git checkout 001-rag-chatbot

# Verify branch
git branch --show-current
# Output: 001-rag-chatbot
```

### 2. Set Up Backend Environment

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 3. Configure Environment Variables

Edit `backend/.env` with your credentials:

```bash
# Database (Neon Postgres)
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# Vector Database (Qdrant Cloud)
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key

# OpenAI API
OPENAI_API_KEY=sk-your_openai_api_key
OPENAI_ORG_ID=org-your_org_id  # Optional

# Better Auth
BETTER_AUTH_SECRET=your_random_secret_key_here  # Generate with: openssl rand -hex 32
BETTER_AUTH_SESSION_TTL=604800  # 7 days in seconds

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
RATE_LIMIT_PER_MINUTE=20
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 4. Initialize Database

```bash
# Run database migrations
cd backend
alembic upgrade head

# Seed initial data (optional)
python scripts/seed_database.py
```

### 5. Embed Book Content

```bash
# Run one-time script to embed book content into Qdrant
python scripts/embed_book_content.py --book-path ../docs --collection-name humanoid-robotics-book-v1

# Expected output:
# Processing 245 markdown files...
# Created 8,742 chunks (avg 487 words per chunk)
# Embedded and uploaded to Qdrant collection: humanoid-robotics-book-v1
# Total time: 12m 34s
```

### 6. Start Backend Server

```bash
# Option A: Run with Docker Compose (recommended)
docker-compose up -d

# Option B: Run locally without Docker
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Verify backend is running
curl http://localhost:8000/health
# Expected: {"status":"healthy","timestamp":"2025-12-06T...","checks":{...}}
```

---

## Frontend Setup (Docusaurus Integration)

### 1. Install Frontend Dependencies

```bash
# From repository root
cd frontend  # Or wherever your Docusaurus project is located

# Install npm dependencies
npm install

# Install additional chatbot dependencies
npm install @openai/chatkit better-auth-react axios
```

### 2. Configure Docusaurus

Add chatbot configuration to `docusaurus.config.js`:

```javascript
module.exports = {
  // ... existing config

  themeConfig: {
    // ... existing theme config

    // Custom fields for chatbot
    customFields: {
      chatbotApiUrl: process.env.CHATBOT_API_URL || 'http://localhost:8000',
      betterAuthEnabled: true,
    },

    // Dark theme configuration
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },
  },

  // ... rest of config
};
```

### 3. Create Environment Variables

Create `frontend/.env.local`:

```bash
CHATBOT_API_URL=http://localhost:8000
BETTER_AUTH_CLIENT_ID=your_better_auth_client_id
```

### 4. Start Frontend Development Server

```bash
npm start

# Docusaurus will start at http://localhost:3000
```

---

## Quick Verification Checklist

After setup, verify the following:

### Backend Health Checks

- [ ] Backend server running at http://localhost:8000
- [ ] Health endpoint returns `{"status":"healthy"}`: `curl http://localhost:8000/health`
- [ ] Database connection successful (check health endpoint `checks.database`)
- [ ] Qdrant connection successful (check health endpoint `checks.qdrant`)
- [ ] OpenAI connection successful (check health endpoint `checks.openai`)

### Frontend Checks

- [ ] Frontend server running at http://localhost:3000
- [ ] Landing page displays (no Docusaurus default template)
- [ ] Dark theme applied by default
- [ ] Login/signup pages accessible at `/auth/login` and `/auth/signup`

### Integration Tests

```bash
# Test authentication flow
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'
# Expected: 201 Created with user object

# Test chatbot query (requires authentication cookie)
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -H "Cookie: auth_token=YOUR_TOKEN_HERE" \
  -d '{"message":"What is a ROS 2 node?","query_mode":"full_book"}'
# Expected: 200 OK with chatbot response
```

---

## Development Workflow

### Running Tests

```bash
# Backend unit tests
cd backend
pytest tests/unit

# Backend integration tests
pytest tests/integration

# Frontend component tests
cd frontend
npm test

# E2E tests (Playwright)
npm run test:e2e
```

### Code Quality Checks

```bash
# Backend linting and formatting
cd backend
black src/ tests/
flake8 src/ tests/
mypy src/

# Frontend linting
cd frontend
npm run lint
npm run format
```

### Database Management

```bash
# Create new migration
cd backend
alembic revision --autogenerate -m "Add new column to users"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

### Debugging Tips

**Backend Debugging**:
- Enable debug logs: Set `LOG_LEVEL=DEBUG` in `.env`
- Use FastAPI's interactive docs: http://localhost:8000/docs
- Check logs: `docker-compose logs -f backend`

**Frontend Debugging**:
- Open browser DevTools → Network tab to inspect API calls
- Check console for React errors
- Use React DevTools browser extension

**Vector Search Debugging**:
- Access Qdrant dashboard: https://your-cluster.qdrant.io
- Test queries directly in Qdrant UI
- Check embedding dimensions: Should be 1536 for `text-embedding-3-small`

---

## Common Issues and Solutions

### Issue: Database connection refused

**Solution**:
```bash
# Verify Neon database is accessible
psql $DATABASE_URL -c "SELECT 1"

# Check if DATABASE_URL is correctly set
echo $DATABASE_URL
```

### Issue: Qdrant returns 401 Unauthorized

**Solution**:
- Verify `QDRANT_API_KEY` is correct
- Check API key permissions in Qdrant Cloud console
- Ensure collection name matches embedded content

### Issue: OpenAI API rate limit errors

**Solution**:
- Check your OpenAI usage dashboard
- Reduce `RATE_LIMIT_PER_MINUTE` in `.env`
- Upgrade to higher OpenAI tier if needed

### Issue: Frontend can't connect to backend

**Solution**:
```bash
# Check CORS configuration in backend/.env
# Add frontend URL to ALLOWED_ORIGINS
ALLOWED_ORIGINS=http://localhost:3000

# Restart backend after changes
docker-compose restart backend
```

---

## Next Steps

After completing the quickstart:

1. **Review Architecture**: Read `plan.md` for detailed system design
2. **Understand Data Model**: Read `data-model.md` for database schema
3. **API Reference**: Review `contracts/api-spec.yaml` for endpoint details
4. **Start Development**: Follow tasks in `tasks.md` (generated by `/sp.tasks`)

---

## Useful Commands Reference

```bash
# Backend
docker-compose up -d          # Start all services
docker-compose logs -f        # View logs
docker-compose down           # Stop all services
pytest --cov                  # Run tests with coverage
alembic upgrade head          # Apply migrations

# Frontend
npm start                     # Start dev server
npm run build                 # Build for production
npm test                      # Run tests
npm run lint                  # Lint code

# Database
psql $DATABASE_URL            # Connect to Postgres
python scripts/seed_database.py  # Reset database

# Vector Database
python scripts/embed_book_content.py  # Re-embed content
```

---

## Support and Resources

- **API Documentation**: http://localhost:8000/docs (FastAPI interactive docs)
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **OpenAI Agents SDK**: https://platform.openai.com/docs/assistants/overview
- **Better Auth**: https://better-auth.com/docs
- **Docusaurus**: https://docusaurus.io/docs

For issues specific to this feature, refer to the planning documents in `specs/001-rag-chatbot/`.
