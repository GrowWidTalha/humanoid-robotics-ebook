#!/usr/bin/env python3
"""
Script to create a test user in the database

This script generates a SQL INSERT statement for the test user with properly hashed password.
You can either run this script to get the SQL, or execute it directly to insert into the database.
"""
import sys
from pathlib import Path

# Add backend src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from passlib.context import CryptContext

# Password hashing configuration (same as auth_service.py)
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# Test user credentials
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "Test123!"

def generate_password_hash(password: str) -> str:
    """Generate Argon2 password hash"""
    return pwd_context.hash(password, scheme="argon2")

def main():
    print("Generating test user credentials...\n")

    # Generate password hash
    password_hash = generate_password_hash(TEST_PASSWORD)

    print(f"Test User Credentials:")
    print(f"  Email: {TEST_EMAIL}")
    print(f"  Password: {TEST_PASSWORD}")
    print(f"  Password Hash: {password_hash[:50]}...\n")

    # Generate SQL INSERT statement
    sql = f"""
-- Insert test user into the database
-- Email: {TEST_EMAIL}
-- Password: {TEST_PASSWORD}

INSERT INTO users (email, password_hash, created_at, updated_at)
VALUES (
    '{TEST_EMAIL}',
    '{password_hash}',
    NOW(),
    NOW()
)
ON CONFLICT (email) DO UPDATE
SET
    password_hash = EXCLUDED.password_hash,
    updated_at = NOW();
"""

    print("SQL Query:")
    print("=" * 80)
    print(sql)
    print("=" * 80)
    print("\nNote: This uses ON CONFLICT to update the password if the user already exists.")
    print("\nTo execute this SQL:")
    print("1. Copy the SQL query above")
    print("2. Connect to your Neon Postgres database")
    print("3. Run the query in your SQL client or psql")
    print("\nOr use psql command:")
    print(f'psql "$DATABASE_URL" -c "{sql.strip().replace(chr(10), " ")}"')

if __name__ == "__main__":
    main()
