# RAG Chatbot Deployment Guide

This guide covers deploying the Humanoid Robotics Book platform with the RAG chatbot feature.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Setup](#database-setup)
4. [Vector Database Setup](#vector-database-setup)
5. [Backend Deployment](#backend-deployment)
6. [Frontend Deployment](#frontend-deployment)
7. [Docker Compose Deployment](#docker-compose-deployment)
8. [Post-Deployment Tasks](#post-deployment-tasks)
9. [Monitoring and Maintenance](#monitoring-and-maintenance)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Services

- **Neon Serverless Postgres** (free tier available)
  - Sign up at https://neon.tech
  - Create a new project and database
  - Note the connection string

- **Qdrant Cloud** (free tier: 1GB storage)
  - Sign up at https://cloud.qdrant.io
  - Create a cluster
  - Generate API key
  - Note the cluster URL

- **OpenAI API** (paid service)
  - Sign up at https://platform.openai.com
  - Add payment method
  - Generate API key
  - Note: Estimated cost ~$5-10/month for moderate usage

### Development Tools

- Docker 20.10+ and Docker Compose 2.0+
- Node.js 18+ and npm 8+
- Python 3.11+
- Git

### Cost Estimates

- **Neon Postgres**: Free tier (3 GiB storage, 1 compute unit)
- **Qdrant Cloud**: Free tier (1GB vector storage, ~40k vectors)
- **OpenAI API**:
  - Embeddings: ~$0.02 per 1M tokens (~$0.50 for full book)
  - Chat (GPT-4o-mini): ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
  - Estimated monthly cost: $5-10 for 100-500 queries/day

**Total monthly cost**: $5-10 (assuming free tiers for Neon and Qdrant)

---

## Environment Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd humanoid-robots-book
```

### 2. Backend Environment Variables

Create `backend/.env`:

```bash
# Database (Neon Postgres)
DATABASE_URL=postgresql://user:password@ep-example.us-east-2.aws.neon.tech/neondb?sslmode=require

# Qdrant Vector Database
QDRANT_URL=https://your-cluster-id.us-east-1-0.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_COLLECTION_NAME=humanoid-robotics-book-v1
VECTOR_SIZE=1536

# OpenAI API
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini

# Authentication
# Generate with: openssl rand -base64 32
BETTER_AUTH_SECRET=your-random-secret-key-minimum-32-characters-long
SESSION_EXPIRY_DAYS=7

# Rate Limiting
RATE_LIMIT_PER_MINUTE=20
REDIS_URL=redis://localhost:6379

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Application
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### 3. Frontend Environment Variables

Create `.env.local` (or `.env.production` for production builds):

```bash
REACT_APP_API_URL=https://api.yourdomain.com
```

---

## Database Setup

### 1. Apply Migrations

Using the Neon Postgres connection:

```bash
cd backend
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial_schema
INFO  [alembic.runtime.migration] Running upgrade 001_initial_schema -> 002_sessions_messages
INFO  [alembic.runtime.migration] Running upgrade 002_sessions_messages -> 003_add_indexes
```

### 2. Verify Database Schema

```bash
# Connect to Neon Postgres
psql $DATABASE_URL

# List tables
\dt

# Expected tables:
# - users
# - sessions
# - chat_messages
```

### 3. Database Indexes

The migrations automatically create these indexes:
- `idx_chat_messages_user_id` on `chat_messages(user_id)`
- `idx_chat_messages_thread_id` on `chat_messages(thread_id)`
- `idx_chat_messages_created_at` on `chat_messages(created_at)`

---

## Vector Database Setup

### 1. Create Qdrant Collection

The embedding script automatically creates the collection, but you can verify:

```bash
# Check collection exists
curl -X GET "https://your-cluster.qdrant.io:6333/collections/humanoid-robotics-book-v1" \
  -H "api-key: your-api-key"
```

### 2. Generate Book Embeddings

**IMPORTANT**: Run this before deploying the chatbot feature.

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Generate embeddings for all book content
python scripts/embed_book_content.py \
  --book-path ../docs/ \
  --collection-name humanoid-robotics-book-v1 \
  --doc-version v1.0.0
```

**Expected output:**
```
INFO: Found 18 markdown files (.md and .mdx) recursively in all subdirectories
INFO: Processing: docs/module-1-ros2/overview.mdx
INFO:   -> Generated 12 chunks
INFO: Processing: docs/module-2-digital-twin/overview.mdx
INFO:   -> Generated 15 chunks
...
INFO: Total chunks: 245
INFO: Uploading 245 chunks to Qdrant...
INFO: Uploaded batch 1 (100 points)
INFO: Uploaded batch 2 (100 points)
INFO: Uploaded final batch (45 points)
INFO: ✅ Embedding complete!
```

**Embedding time**: ~5-10 minutes for full book
**Cost**: ~$0.50 (one-time)

### 3. Verify Embeddings

```bash
# Check collection info
curl -X GET "https://your-cluster.qdrant.io:6333/collections/humanoid-robotics-book-v1" \
  -H "api-key: your-api-key"

# Expected response:
# {
#   "result": {
#     "status": "green",
#     "vectors_count": 245,
#     "indexed_vectors_count": 245,
#     ...
#   }
# }
```

---

## Backend Deployment

### Option 1: Docker Deployment (Recommended)

#### 1. Build Docker Image

```bash
cd backend
docker build -t humanoid-robotics-backend:latest .
```

#### 2. Run with Docker Compose

```bash
cd backend
docker-compose up -d
```

**docker-compose.yml** should include:
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

#### 3. Verify Deployment

```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs -f backend

# Test health endpoint
curl http://localhost:8000/health
```

### Option 2: Direct Deployment

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run with uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

For production, use a process manager like **systemd** or **supervisor**.

#### Example systemd service (`/etc/systemd/system/humanoid-backend.service`):

```ini
[Unit]
Description=Humanoid Robotics Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/humanoid-robots-book/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable humanoid-backend
sudo systemctl start humanoid-backend
sudo systemctl status humanoid-backend
```

---

## Frontend Deployment

### Option 1: Static Build (Recommended)

```bash
# Install dependencies
npm install

# Build for production
npm run build

# Output in: build/
# Deploy these static files to any static hosting:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
# - GitHub Pages
# - Nginx
```

#### Deploy to Vercel (Easiest)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

#### Deploy to Nginx

```bash
# Copy build files
sudo cp -r build/* /var/www/humanoid-robotics/

# Nginx config (/etc/nginx/sites-available/humanoid-robotics)
server {
    listen 80;
    server_name yourdomain.com;

    root /var/www/humanoid-robotics;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/humanoid-robotics /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Option 2: Development Server (Not Recommended for Production)

```bash
npm start
```

---

## Docker Compose Deployment

Full-stack deployment with one command:

### 1. Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  # Backend API
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - QDRANT_URL=${QDRANT_URL}
      - QDRANT_API_KEY=${QDRANT_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - REDIS_URL=redis://redis:6379
      - ALLOWED_ORIGINS=http://localhost:3000
    depends_on:
      - redis
    restart: unless-stopped

  # Redis for rate limiting
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  # Frontend (optional, use static build instead)
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend
    restart: unless-stopped
```

### 2. Deploy

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

---

## Post-Deployment Tasks

### 1. Verify Health Endpoints

```bash
# Backend health
curl https://api.yourdomain.com/health

# Expected: {"status": "healthy", "timestamp": "2025-12-11T..."}
```

### 2. Test Authentication

```bash
# Signup
curl -X POST https://api.yourdomain.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123", "name": "Test User"}'

# Login
curl -X POST https://api.yourdomain.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}' \
  -c cookies.txt

# Session check (with cookies)
curl -X GET https://api.yourdomain.com/auth/session \
  -b cookies.txt
```

### 3. Test Chatbot

```bash
# Send message
curl -X POST https://api.yourdomain.com/chat/message \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "message": "What is ROS 2?",
    "query_mode": "full_book"
  }'

# Expected: Response with AI-generated answer and sources
```

### 4. Monitor Initial Usage

```bash
# Check logs for errors
docker-compose logs -f backend | grep ERROR

# Monitor response times
docker-compose logs -f backend | grep "response_time"
```

---

## Monitoring and Maintenance

### Health Checks

Set up monitoring for:
- `GET /health` - Backend health
- `GET /docs` - API documentation availability
- Database connection pool status
- Qdrant cluster status
- Redis connection

**Recommended tools:**
- UptimeRobot (free tier)
- Pingdom
- StatusCake
- Custom script with cron

### Log Aggregation

Backend logs include:
- Request/response timing
- Error stack traces
- Authentication events
- Rate limit hits
- Database query performance

**Log locations:**
- Docker: `docker-compose logs backend`
- Systemd: `journalctl -u humanoid-backend -f`

### Backup Strategy

**Database (Neon)**:
- Automatic daily backups (included with free tier)
- Manual backups before major updates
- Export: `pg_dump $DATABASE_URL > backup.sql`

**Vector Database (Qdrant)**:
- Snapshot before re-embedding
- Export collection if needed
- Keep embedding script and book content in Git

**Application Code**:
- Git repository (remote backup)
- Tag releases: `git tag v1.0.0`

### Performance Monitoring

Key metrics to track:
- **Chatbot response time**: Target <3s p95
- **Vector search time**: Target <200ms
- **Database query time**: Target <100ms
- **API error rate**: Target <1%
- **Rate limit hits**: Monitor for abuse

### Updating Embeddings

When book content changes:

```bash
# Re-run embedding script
cd backend
python scripts/embed_book_content.py \
  --book-path ../docs/ \
  --collection-name humanoid-robotics-book-v1 \
  --doc-version v1.1.0

# This will upsert (update or insert) embeddings
# Old embeddings are automatically replaced
```

**Frequency**:
- After content updates
- Monthly for minor updates
- Major version bumps for significant changes

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors

**Symptom**: `could not connect to server` or `FATAL: password authentication failed`

**Solution**:
```bash
# Verify DATABASE_URL format
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1;"

# Check Neon dashboard for database status
# Ensure IP is whitelisted (if applicable)
```

#### 2. Qdrant Connection Errors

**Symptom**: `Connection refused` or `Unauthorized`

**Solution**:
```bash
# Verify Qdrant URL and API key
curl -X GET "$QDRANT_URL/collections" \
  -H "api-key: $QDRANT_API_KEY"

# Check Qdrant Cloud console for cluster status
# Verify API key is active
```

#### 3. OpenAI API Errors

**Symptom**: `401 Unauthorized` or `429 Rate Limit Exceeded`

**Solution**:
```bash
# Verify API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check billing at https://platform.openai.com/account/billing
# Increase rate limits if needed
# Implement retry logic (already included in rag_service.py)
```

#### 4. CORS Errors

**Symptom**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution**:
```bash
# Update ALLOWED_ORIGINS in backend/.env
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Restart backend
docker-compose restart backend
```

#### 5. Session/Authentication Issues

**Symptom**: `401 Unauthorized` or `Session expired`

**Solution**:
```bash
# Verify BETTER_AUTH_SECRET is set and consistent
echo $BETTER_AUTH_SECRET

# Check cookie settings (SameSite, Secure, HttpOnly)
# Clear browser cookies and re-login
# Check backend logs for authentication errors
```

#### 6. Slow Chatbot Responses

**Symptom**: Response time >10s

**Solution**:
```bash
# Check OpenAI API status: https://status.openai.com
# Verify CHAT_MODEL is set to "gpt-4o-mini" (not gpt-4-turbo)
# Check Qdrant response time
# Review backend logs for bottlenecks
# Consider reducing max_tokens in rag_service.py
```

#### 7. Embedding Script Fails

**Symptom**: `AttributeError` or `No files found`

**Solution**:
```bash
# Verify book path exists
ls -la ../docs/

# Check for .md and .mdx files
find ../docs/ -name "*.md" -o -name "*.mdx"

# Verify OPENAI_EMBEDDING_MODEL in .env
echo $OPENAI_EMBEDDING_MODEL

# Should be: text-embedding-3-small
```

### Getting Help

1. **Check logs**: `docker-compose logs -f backend`
2. **Review API docs**: `https://api.yourdomain.com/docs`
3. **Consult specs**: `specs/001-rag-chatbot/spec.md`
4. **Database status**: Neon Console
5. **Vector DB status**: Qdrant Cloud Console
6. **OpenAI status**: https://status.openai.com

---

## Security Checklist

Before production deployment:

- [ ] All secrets in environment variables (not in code)
- [ ] BETTER_AUTH_SECRET is strong (32+ random characters)
- [ ] HTTPS enabled for all endpoints
- [ ] CORS configured with specific origins (not `*`)
- [ ] Rate limiting enabled and tested
- [ ] Database uses SSL/TLS (sslmode=require)
- [ ] No API keys committed to Git
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS protection (input sanitization)
- [ ] Session cookies are HTTP-only and Secure
- [ ] Regular dependency updates (`npm audit`, `pip check`)
- [ ] Error messages don't leak sensitive info
- [ ] Logs don't contain passwords or API keys

---

## Rollback Procedure

If deployment fails:

### 1. Rollback Database

```bash
# Rollback last migration
cd backend
alembic downgrade -1

# Or rollback to specific version
alembic downgrade <revision_id>
```

### 2. Rollback Backend

```bash
# Docker: use previous image
docker-compose down
docker-compose up -d --build

# Git: revert to previous commit
git revert HEAD
git push

# Or checkout previous tag
git checkout v1.0.0
docker-compose up -d --build
```

### 3. Rollback Frontend

```bash
# Re-deploy previous build
vercel --prod --force

# Or rollback in Vercel dashboard
```

### 4. Rollback Embeddings

```bash
# Re-run embedding script with previous doc version
python scripts/embed_book_content.py \
  --book-path ../docs/ \
  --collection-name humanoid-robotics-book-v1 \
  --doc-version v1.0.0
```

---

## Next Steps

After successful deployment:

1. **Monitor performance** for first 24-48 hours
2. **Collect user feedback** on chatbot quality
3. **Review logs** for errors or warnings
4. **Test all features** end-to-end
5. **Set up alerts** for downtime or errors
6. **Document any customizations** made during deployment
7. **Plan content updates** and re-embedding schedule

For detailed implementation information, see:
- `specs/001-rag-chatbot/spec.md` - Feature specification
- `specs/001-rag-chatbot/quickstart.md` - Development quickstart
- `README.md` - Project overview

---

**Deployment Version**: 1.0.0
**Last Updated**: 2025-12-11
**Maintained By**: Development Team
