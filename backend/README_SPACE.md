---
title: Humanoid Robotics RAG API
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
---

# Humanoid Robotics RAG Chatbot API

This is the backend API for the Humanoid Robotics interactive learning platform with RAG-powered AI chatbot.

## Features

- 🤖 RAG (Retrieval Augmented Generation) chatbot
- 📚 Semantic search over robotics textbook content
- 🔐 User authentication with session management
- 💾 Persistent chat history
- ⚡ Fast responses with GPT-4o-mini

## API Documentation

Once the Space is running, visit:
- **Swagger UI**: `/api/docs`
- **Health Check**: `/health`

## Environment Variables Required

Make sure to set these in your Space Settings:

- `DATABASE_URL` - Neon Postgres connection string
- `QDRANT_URL` - Qdrant Cloud cluster URL
- `QDRANT_API_KEY` - Qdrant API key
- `OPENAI_API_KEY` - OpenAI API key
- `BETTER_AUTH_SECRET` - Random 32+ character secret
- `ALLOWED_ORIGINS` - Frontend domain (comma-separated)

## Usage

### Health Check
```bash
curl https://your-space.hf.space/health
```

### Create Account
```bash
curl -X POST https://your-space.hf.space/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "SecurePass123", "name": "User"}'
```

### Chat with AI
```bash
curl -X POST https://your-space.hf.space/api/chat/message \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your-session-cookie" \
  -d '{"message": "What is ROS 2?", "query_mode": "full_book"}'
```

## Tech Stack

- FastAPI (Python 3.11)
- PostgreSQL (Neon)
- Qdrant (vector database)
- OpenAI GPT-4o-mini & text-embedding-3-small
- Better Auth

## Links

- [Project Repository](#)
- [Frontend Demo](#)
- [Documentation](#)
