# Creating the Test User

This guide explains how to create the test user (`test@example.com` / `Test123!`) in your database.

## Easiest Method: Use the Signup API

If your backend is running, simply register the user via the API:

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Test123!"}'
```

Or use the signup form in the frontend at `/auth/signup`

## Method 2: Using Python Script

Run the script in your backend environment (requires passlib installed):

```bash
cd backend
python scripts/create_test_user.py
```

This will generate the SQL INSERT statement with the properly hashed password.

## Method 3: Python One-Liner

Generate just the password hash:

```bash
cd backend
python -c "from passlib.context import CryptContext; pwd_context = CryptContext(schemes=['argon2', 'bcrypt'], deprecated='auto'); print(pwd_context.hash('Test123!', scheme='argon2'))"
```

Then use the output hash in this SQL:

```sql
INSERT INTO users (email, password_hash, created_at, updated_at)
VALUES (
    'test@example.com',
    'YOUR_HASH_HERE',  -- paste the hash from the Python command
    NOW(),
    NOW()
)
ON CONFLICT (email) DO UPDATE
SET
    password_hash = EXCLUDED.password_hash,
    updated_at = NOW();
```

## Method 4: Direct psql with Environment Variable

If you have the hash, you can execute directly:

```bash
export TEST_HASH="your_generated_hash_here"
psql "$DATABASE_URL" -c "INSERT INTO users (email, password_hash, created_at, updated_at) VALUES ('test@example.com', '$TEST_HASH', NOW(), NOW()) ON CONFLICT (email) DO UPDATE SET password_hash = EXCLUDED.password_hash, updated_at = NOW();"
```

## Verification

After creating the user, verify it exists:

```bash
psql "$DATABASE_URL" -c "SELECT id, email, created_at FROM users WHERE email = 'test@example.com';"
```

## Test Credentials

- **Email**: `test@example.com`
- **Password**: `Test123!`

These credentials can be auto-filled using the "Use Test Credentials" button on the login page.
