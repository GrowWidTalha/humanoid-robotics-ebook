-- SQL Script to Add Test User
-- Email: test@example.com
-- Password: Test123!
--
-- IMPORTANT: You need to generate the password hash first using Python/passlib
-- See instructions in create_test_user.py or run it with your backend environment

-- Option 1: If you have a pre-generated hash, use this template:
-- Replace YOUR_ARGON2_HASH_HERE with the actual hash

INSERT INTO users (email, password_hash, created_at, updated_at)
VALUES (
    'test@example.com',
    'YOUR_ARGON2_HASH_HERE',  -- Replace with actual Argon2 hash
    NOW(),
    NOW()
)
ON CONFLICT (email) DO UPDATE
SET
    password_hash = EXCLUDED.password_hash,
    updated_at = NOW();

-- ============================================================================
-- To generate the password hash:
-- ============================================================================
--
-- Method 1: Using Python (in your backend environment with dependencies installed)
-- -------------------------------------------------------------------------
-- $ cd backend
-- $ python scripts/create_test_user.py
--
-- Method 2: Using Python one-liner
-- -------------------------------------------------------------------------
-- $ cd backend
-- $ python -c "from passlib.context import CryptContext; pwd_context = CryptContext(schemes=['argon2', 'bcrypt'], deprecated='auto'); print(pwd_context.hash('Test123!', scheme='argon2'))"
--
-- Method 3: Via Backend API (if running)
-- -------------------------------------------------------------------------
-- Just use the signup endpoint:
-- POST http://localhost:8000/api/auth/register
-- Body: {"email": "test@example.com", "password": "Test123!"}
--
-- This is the EASIEST method - just register via the API!
-- ============================================================================
