# Backend Deployment Guide

## Hugging Face Spaces Configuration

### Required Environment Variables

When deploying to Hugging Face Spaces, you must configure the following environment variable to allow cross-origin requests from your GitHub Pages frontend:

#### ALLOWED_ORIGINS

**Value:**
```
https://growwidtalha.github.io
```

**How to Set:**
1. Go to your Hugging Face Space: https://huggingface.co/spaces/growwithtalha/humanoid-robotics-rag
2. Click on **Settings** (gear icon)
3. Scroll to **Variables and secrets**
4. Add or update the environment variable:
   - **Name**: `ALLOWED_ORIGINS`
   - **Value**: `https://growwidtalha.github.io`
5. Click **Save**
6. **Restart the Space** for changes to take effect

### Authentication Cookie Configuration

The backend uses HTTP-only cookies with the following settings for cross-origin authentication:

- **Cookie name**: `auth_token`
- **HttpOnly**: `true` (JavaScript cannot access)
- **Secure**: `true` (only sent over HTTPS)
- **SameSite**: `none` (allows cross-origin cookie sending)
- **Max-Age**: 7 days (604800 seconds)

**Important**: The `samesite="none"` setting is required because:
- Frontend: `https://growwidtalha.github.io` (GitHub Pages)
- Backend: `https://growwithtalha-humanoid-robotics-rag.hf.space` (Hugging Face)

These are different domains, so `samesite="lax"` (default) would block the cookie from being sent with cross-origin requests.

### CORS Configuration

The backend CORS middleware is configured to:
- **Allow credentials**: `true` (required for cookies)
- **Allow origins**: Loaded from `ALLOWED_ORIGINS` environment variable
- **Allow methods**: `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`
- **Allow headers**: All (`*`)
- **Expose headers**: `X-Request-ID`

### Troubleshooting

#### Issue: `/auth/me` returns 401 Unauthorized

**Symptoms:**
- Login succeeds (returns user data)
- Cookie is set in browser
- `/auth/me` request returns 401

**Causes:**
1. **ALLOWED_ORIGINS not set**: Backend rejects cross-origin requests
2. **Cookie not sent**: Browser doesn't send cookie due to SameSite restriction
3. **Frontend not using credentials**: Axios must have `withCredentials: true`

**Solutions:**

1. **Check ALLOWED_ORIGINS**:
   ```bash
   # In Hugging Face Spaces settings, verify:
   ALLOWED_ORIGINS=https://growwidtalha.github.io
   ```

2. **Verify cookie settings in browser DevTools**:
   - Open DevTools → Application tab → Cookies
   - Check `https://growwithtalha-humanoid-robotics-rag.hf.space`
   - Should see `auth_token` with:
     - `SameSite`: `None`
     - `Secure`: `✓`
     - `HttpOnly`: `✓`

3. **Verify frontend Axios configuration**:
   ```typescript
   // src/services/apiClient.ts should have:
   const apiClient = axios.create({
     baseURL: API_URL,
     withCredentials: true, // ← Required!
   });
   ```

4. **Check CORS preflight response**:
   - Open DevTools → Network tab
   - Look for OPTIONS request to `/api/auth/me`
   - Response headers should include:
     - `Access-Control-Allow-Origin: https://growwidtalha.github.io`
     - `Access-Control-Allow-Credentials: true`

#### Issue: Cookie not visible in browser

**Solution**: Cookies from cross-origin domains are only visible when you:
1. Open DevTools
2. Go to Application → Cookies
3. Select the **backend domain** (not frontend domain)
4. Look for `auth_token` under `https://growwithtalha-humanoid-robotics-rag.hf.space`

The cookie won't appear under `https://growwidtalha.github.io` because it's set by the backend domain.

### Testing the Fix

After deploying these changes and updating environment variables:

1. **Clear all cookies**:
   ```
   DevTools → Application → Clear storage → Clear site data
   ```

2. **Test signup flow**:
   ```
   1. Go to https://growwidtalha.github.io/humanoid-robotics-ebook/auth/signup
   2. Create account
   3. Check DevTools console for "[AuthVerify] ✓ Signup persistence verified"
   4. Verify navbar shows user email dropdown
   ```

3. **Test login flow**:
   ```
   1. Logout
   2. Go to /auth/login
   3. Login with credentials
   4. Check console for "[AuthVerify] ✓ Login persistence verified"
   5. Verify navbar shows user dropdown
   ```

4. **Test page refresh**:
   ```
   1. While logged in, refresh the page
   2. Verify you remain authenticated
   3. Verify navbar still shows user dropdown
   ```

5. **Test /auth/me directly**:
   ```bash
   # After logging in, check cookies in browser
   curl -X GET 'https://growwithtalha-humanoid-robotics-rag.hf.space/api/auth/me' \
     -H 'Cookie: auth_token=YOUR_TOKEN_FROM_BROWSER' \
     -H 'Origin: https://growwidtalha.github.io'

   # Should return 200 with user data
   ```

### Additional Environment Variables

Complete list of required environment variables for Hugging Face Spaces:

```bash
# Database
DATABASE_URL=postgresql://...

# Qdrant Vector Database
QDRANT_URL=https://...
QDRANT_API_KEY=...
QDRANT_COLLECTION_NAME=humanoid-robotics-book-v1

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini

# Authentication
BETTER_AUTH_SECRET=...  # Generate with: openssl rand -hex 32
SESSION_EXPIRY_DAYS=7

# CORS (CRITICAL for production)
ALLOWED_ORIGINS=https://growwidtalha.github.io

# Application
ENVIRONMENT=production
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_PER_MINUTE=20
REDIS_URL=redis://localhost:6379  # If using Redis
```

### Security Considerations

1. **Never expose BETTER_AUTH_SECRET**: Keep it secret in HF Spaces variables
2. **HTTPS only**: Both frontend and backend must use HTTPS for secure cookies
3. **Specific origins**: Never use `*` for `ALLOWED_ORIGINS` when using credentials
4. **Token expiry**: Sessions expire after 7 days by default
5. **HTTP-only cookies**: JavaScript cannot access the auth token

### Deployment Checklist

- [ ] Set `ALLOWED_ORIGINS=https://growwidtalha.github.io` in HF Spaces
- [ ] Set `ENVIRONMENT=production` in HF Spaces
- [ ] Deploy backend with `samesite="none"` cookie settings
- [ ] Deploy frontend with `withCredentials: true` in Axios
- [ ] Clear browser cookies and test signup
- [ ] Test login flow
- [ ] Test page refresh (auth persistence)
- [ ] Test `/auth/me` endpoint directly
- [ ] Verify cookies visible in DevTools under backend domain

## Local Development

For local development, use `samesite="lax"` (safer) since frontend and backend are on same origin (localhost):

```python
# For local development only:
response.set_cookie(
    key="auth_token",
    value=token,
    httponly=True,
    secure=False,  # Allow HTTP in development
    samesite="lax",  # Safe for same-origin
    max_age=60 * 60 * 24 * 7
)
```

Consider using environment-based configuration:

```python
from src.config.settings import settings

samesite = "none" if settings.is_production else "lax"
secure = settings.is_production

response.set_cookie(
    key="auth_token",
    value=token,
    httponly=True,
    secure=secure,
    samesite=samesite,
    max_age=60 * 60 * 24 * 7
)
```
