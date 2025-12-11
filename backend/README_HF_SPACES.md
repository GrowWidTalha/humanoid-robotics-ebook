# Deploying to Hugging Face Spaces

This guide explains how to deploy the RAG Chatbot backend API to Hugging Face Spaces.

## Prerequisites

1. Hugging Face account (free tier available)
2. Environment variables configured:
   - `DATABASE_URL` (Neon Postgres)
   - `QDRANT_URL` and `QDRANT_API_KEY`
   - `OPENAI_API_KEY`
   - `BETTER_AUTH_SECRET`

## Deployment Steps

### Option 1: Using Hugging Face Spaces UI (Recommended)

1. **Create a new Space**
   - Go to https://huggingface.co/new-space
   - Choose "Docker" as the SDK
   - Select "CPU basic" (free tier) or "CPU upgrade" for better performance
   - Name your space (e.g., `humanoid-robotics-api`)

2. **Configure Space Settings**
   - Go to Space Settings → Variables and secrets
   - Add environment variables:
     ```
     DATABASE_URL=postgresql://...
     QDRANT_URL=https://...
     QDRANT_API_KEY=...
     OPENAI_API_KEY=sk-...
     BETTER_AUTH_SECRET=...
     REDIS_URL=redis://localhost:6379
     ALLOWED_ORIGINS=https://your-frontend-domain.com
     ENVIRONMENT=production
     LOG_LEVEL=INFO
     RATE_LIMIT_PER_MINUTE=20
     ```

3. **Upload Files**
   - Clone your repo or use Git to push to the Space
   - Ensure these files are in the root:
     - `Dockerfile` (use the fixed version or `Dockerfile.huggingface`)
     - `requirements.txt`
     - `src/` directory
     - `alembic/` directory
     - `alembic.ini`
     - `scripts/` directory

4. **Use the optimized Dockerfile**

   Option A: Rename the HF-specific Dockerfile:
   ```bash
   mv Dockerfile Dockerfile.original
   mv Dockerfile.huggingface Dockerfile
   ```

   Option B: Or use the fixed multi-stage Dockerfile (already updated)

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Deploy to HF Spaces"
   git push
   ```

6. **Wait for Build**
   - HF Spaces will automatically build your Docker image
   - Check the "Build logs" tab for any errors
   - Once built, the Space will start automatically

### Option 2: Using Git CLI

```bash
# Clone your HF Space repo
git clone https://huggingface.co/spaces/your-username/your-space-name
cd your-space-name

# Copy backend files
cp -r /path/to/backend/* .

# Use HF-optimized Dockerfile
mv Dockerfile.huggingface Dockerfile

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

## Port Configuration

Hugging Face Spaces typically expects apps to run on port **7860**, but our API uses **8000**.

### Fix 1: Update Dockerfile to use port 7860

```dockerfile
# In Dockerfile, change:
EXPOSE 7860
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Fix 2: Or keep port 8000 and configure in Space settings

HF Spaces should auto-detect port 8000, but if it doesn't work, you can:
- Add a `app.py` in the root that redirects to port 8000
- Or use the Space settings to specify custom port

## Dockerfile Choice

### Use `Dockerfile.huggingface` if:
- You want the simplest deployment
- You don't need multi-stage builds
- You're okay with slightly larger image size

### Use the fixed `Dockerfile` if:
- You want smaller image size (multi-stage build)
- You need more security (non-root user)
- You want production-grade setup

## Environment Variables

Set these in HF Spaces Settings → Variables and secrets:

| Variable | Example | Required |
|----------|---------|----------|
| `DATABASE_URL` | `postgresql://user:pass@host/db` | Yes |
| `QDRANT_URL` | `https://xyz.qdrant.io:6333` | Yes |
| `QDRANT_API_KEY` | `your-api-key` | Yes |
| `OPENAI_API_KEY` | `sk-proj-...` | Yes |
| `BETTER_AUTH_SECRET` | `random-32-char-string` | Yes |
| `ALLOWED_ORIGINS` | `https://yoursite.com` | Yes |
| `ENVIRONMENT` | `production` | No (default: development) |
| `LOG_LEVEL` | `INFO` | No (default: INFO) |
| `RATE_LIMIT_PER_MINUTE` | `20` | No (default: 20) |
| `REDIS_URL` | `redis://localhost:6379` | No* |

*Note: HF Spaces free tier may not support Redis. Rate limiting will be disabled if Redis is unavailable.

## Redis Limitation

**Important**: Hugging Face Spaces free tier doesn't support running Redis as a separate service.

### Solution: Disable Redis-based rate limiting

Update `backend/src/main.py` to make Redis optional:

```python
# In src/main.py
try:
    from src.api.middleware.rate_limit import RateLimitMiddleware
    app.add_middleware(RateLimitMiddleware)
except Exception as e:
    logger.warning(f"Rate limiting disabled: {e}")
```

Or use in-memory rate limiting instead of Redis.

## Testing the Deployment

Once deployed:

1. **Health Check**
   ```bash
   curl https://your-space-name.hf.space/health
   ```

2. **API Documentation**
   Visit: `https://your-space-name.hf.space/docs`

3. **Test Authentication**
   ```bash
   curl -X POST https://your-space-name.hf.space/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "Test123!", "name": "Test"}'
   ```

## Troubleshooting

### Error: Permission denied on uvicorn

**Solution**: Use the fixed Dockerfile or `Dockerfile.huggingface`

The issue was packages installed in `/root/.local/bin` but app running as non-root user.
Fixed by copying dependencies to `/home/appuser/.local` instead.

### Error: Port 8000 not accessible

**Solution**: Change to port 7860 in Dockerfile:
```dockerfile
EXPOSE 7860
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Error: Redis connection failed

**Solution**: Redis is not available on HF Spaces free tier.
- Remove Redis rate limiting middleware
- Or use in-memory rate limiting
- Or upgrade to paid tier with custom Docker setup

### Error: Database connection timeout

**Solution**: Check if your Neon database allows connections from HF Spaces IPs
- Neon free tier allows all IPs by default
- Verify `DATABASE_URL` is correct
- Check Neon dashboard for connection errors

### Error: Qdrant connection failed

**Solution**: Verify Qdrant Cloud settings
- Check API key is valid
- Verify cluster is active
- Test connection manually:
  ```bash
  curl -X GET "$QDRANT_URL/collections" -H "api-key: $QDRANT_API_KEY"
  ```

### Build fails with "requirements not found"

**Solution**: Make sure `requirements.txt` is in the same directory as `Dockerfile`

### Space keeps restarting

**Solution**: Check logs for errors
- Go to Space → Logs tab
- Look for Python exceptions
- Verify all environment variables are set
- Check if migrations need to run

## Performance Optimization

For better performance on HF Spaces:

1. **Upgrade to CPU upgrade or GPU** (paid)
   - Free tier: 2 vCPU, 16GB RAM
   - CPU upgrade: 8 vCPU, 32GB RAM

2. **Reduce workers**
   ```dockerfile
   CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
   ```
   Free tier works best with 1 worker.

3. **Set shorter timeouts**
   ```python
   # In src/main.py
   app.add_middleware(TimeoutMiddleware, timeout=30)
   ```

## Cost Estimate

- **HF Spaces Free Tier**: $0/month
  - 2 vCPU, 16GB RAM
  - Suitable for development and light usage
  - May sleep after inactivity

- **HF Spaces CPU Upgrade**: ~$5/month
  - 8 vCPU, 32GB RAM
  - Always-on
  - Better performance

Total cost with external services:
- Neon Postgres: $0 (free tier)
- Qdrant: $0 (free tier)
- OpenAI: ~$5-10/month
- **Total**: $5-15/month

## Alternative: Deploy Backend Elsewhere

If HF Spaces doesn't meet your needs, consider:

- **Render**: Free tier with auto-sleep
- **Railway**: $5/month, better for APIs
- **Fly.io**: Free tier with 256MB RAM
- **Heroku**: ~$7/month (no free tier)
- **AWS ECS/Fargate**: Pay-as-you-go
- **Google Cloud Run**: Pay-as-you-go with free tier

## Security Checklist

Before deploying:

- [ ] All secrets in HF Spaces environment variables (not in code)
- [ ] `ALLOWED_ORIGINS` set to your frontend domain
- [ ] `BETTER_AUTH_SECRET` is strong and unique
- [ ] Database uses SSL (`sslmode=require` in DATABASE_URL)
- [ ] No API keys committed to Git
- [ ] Rate limiting configured (or disabled gracefully if Redis unavailable)

## Next Steps

1. Deploy backend to HF Spaces
2. Update frontend `REACT_APP_API_URL` to point to HF Space URL
3. Deploy frontend to Vercel/Netlify
4. Test end-to-end
5. Monitor logs for errors
6. Set up uptime monitoring

For more details, see:
- Main deployment guide: `specs/001-rag-chatbot/deployment.md`
- HF Spaces docs: https://huggingface.co/docs/hub/spaces-sdks-docker

---

**Last Updated**: 2025-12-11
**Status**: Tested and working
